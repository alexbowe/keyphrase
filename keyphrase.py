# Python libs
import re
from math import log

# Third Party Libs
from dumbo import *
from nltk.probability import FreqDist
import nltk
import sys

# My Libs
from mycorpus import stopwords

# Run Flags
DEBUG = 0

# Program Variables
titleWeight = 3
minLength = 3
maxLength = 40
maxGram = 4
min_tf_idf = 0.11
separator = ','

sentence_re = r'''(?x)      # set flag to allow verbose regexps
      ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*            # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
    | \.\.\.                # ellipsis
    | [][.,;"'?():-_`]      # these are separate tokens
'''

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

import pickle
infile = open('pos_tag.pkl', 'rb')
pos = pickle.load(infile)
infile.close()

grammar = r"""
    NBAR:
        {<NN.*|JJ*>*<NN.*>}
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}
"""
chunker = nltk.RegexpParser(grammar)

def leaves(tree):
    for subtree in tree.subtrees(filter = lambda t: t.node=='NP'):
        yield subtree.leaves()

def normalise(word):
    word = word.lower()
    word = stemmer.stem_word(word)
    return word

def acceptableWord(word):
    accepted = bool(minLength <= len(word) <= maxLength
        and word.lower() not in stopwords )
    return accepted

def acceptableGram(gram):
    return bool(1 <= len(gram) <= maxGram)

def rPrecision(a, b):
    a = set(a)
    b = set(b)
    overlap = len(a.intersection(b))
    return float(overlap)/max(len(a), len(b))

# Mapper: Extracts Terms from a Document
# IN : key = (docname, line#), value = line
# OUT: (docname, term), 1
# Requires -addpath yes flag
@opt("addpath", "yes")
def termMapper( (docname, lineNum), line):
    toks = nltk.regexp_tokenize(line, sentence_re)
    toks = [ lemmatizer.lemmatize(t) for t in toks ]
    postoks = pos.tag(toks)
    tree = chunker.parse(postoks)
    
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf if acceptableWord(w) ]
        weight = 1
        if lineNum is 0: weight = titleWeight
        yield (docname, term), 1 * weight

# IN : (docname, term), n
# OUT: docname, (term, n)
# n - term-count for the doc
def docTermCountMapper( (docname, term), n):
    yield docname, (term, n)
    
# IN : docname, (term, n)-list
# OUT: (term, docname), (n, N)
# n - term-count for the doc
# N - term-count for all docs
def docTermCountReducer(docname, values):
    values = list(values)
    # Total count of term across all docs
    N = sum(n for (term, n) in values)
    for (term, n) in values:
        yield (term, docname), (n, N)

# IN : (term, docname), (n, N)
# OUT: term, (docname, n, N, 1)
# n - term-count for the doc
# N - term-count for all docs
def corpusTermCountMapper( (term, docname), (n, N) ):
    yield term, (docname, n, N, 1)

class CorpusTermCountReducer:
    def __init__(self):
        # get -param doccount
        self.doccount = float(self.params['doccount'])
    def __call__(self, term, values):
        values = list(values)
        m = sum(c for (docname, n, N, c) in values)
        idf = log(self.doccount / m)
        for (docname, n, N) in (v[:3] for v in values):
            tf = (float(n)/N)
            yield docname, (term, tf * idf)

def finalMapper(docname, (term, tf_idf) ):
    if tf_idf >= min_tf_idf:
        yield docname, term

def finalReducer(docname, terms):
    # upper = terms[:n]
    # lower = terms[n:]
    # for a in upper:
    #     for b in lower:
    #         r = rPrecision(a, b)
    terms = [' '.join(t) for t in terms if acceptableGram(t)]
    yield docname, separator.join(terms)

def runner(job):
    job.additer(termMapper, sumreducer, combiner = sumreducer)
    job.additer(docTermCountMapper, docTermCountReducer)
    job.additer(corpusTermCountMapper, CorpusTermCountReducer)
    job.additer(finalMapper, finalReducer)

if __name__ == "__main__":
    main(runner)
