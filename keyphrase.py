# Python libs
import re
from math import log

# Third Party Libs
from dumbo import *
from nltk.stem.porter import PorterStemmer
from nltk.probability import FreqDist
import nltk

# My Libs
from mycorpus import stopwords

# Run Flags
DEBUG = 0

# Program Variables
minLength = 3
maxLength = 40
separator = ','

sentence_re = r'''(?x)      # set flag to allow verbose regexps
      ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*            # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
    | \.\.\.                # ellipsis
    | [][.,;"'?():-_`]      # these are separate tokens
'''

lemmatizer = nltk.WordNetLemmatizer()

grammar = r"""
    NP: {<JJ>*<NN|NNP>+}    # Adjectives and (proper) nouns
"""
chunker = nltk.RegexpParser(grammar)

def acceptable(word):
    accepted = bool(minLength <= len(word) <= maxLength
        and word.lower() not in stopwords )
    if DEBUG and not accepted:
        import sys
        sys.stderr.write("Not accepted: " + word + "\n")
    return accepted

def normalise(word):
    word = word.lower()
    word = PorterStemmer().stem_word(word)
    return word
            
def genNPLeaves(tree):
    for subtree in tree.subtrees(filter = lambda t:t.node=='NP'):
        yield subtree.leaves()

# Mapper: Extracts Terms from a Document
# IN : key = (docname, line#), value = line
# OUT: (docname, term), 1
# Requires -addpath yes flag
@opt("addpath", "yes")
def termMapper( (docname, lineNum), line):
    if DEBUG and lineNum is 0:
        import sys
        sys.stderr.write(str(docname) + ", " + str(lineNum) +": " + line + "\n")
    toks = nltk.regexp_tokenize(line, sentence_re)
    toks = [ lemmatizer.lemmatize(t) for t in toks ]
    postoks = nltk.tag.pos_tag(toks)
    chunkTree = chunker.parse(postoks)
    
    for leaf in genNPLeaves(chunkTree):
        words = [w for w,t in leaf]
        words = [ normalise(w) for w in words if acceptable(w) ]
        if len(words) > 0:
            term = ' '.join(words)
            yield (docname, term), 1

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
def corpusTermCountMapper( (term, docname), (n, N)):
    yield term, (docname, n, N, 1)

class CorpusTermCountReducer:
    def __init__(self):
        self.doccount = float(self.params['doccount'])
    def __call__(self, term, values):
        values = list(values)
        m = sum(c for (docname, n, N, c) in values)
        for (docname, n, N) in (v[:3] for v in values):
            yield (term, docname), (float(n)/N) * log(self.doccount / m)

def finalMapper((term, docname), tf_idf):
    if tf_idf >= 0.10:
        yield docname, term

def finalReducer(docname, terms):
    yield docname, separator.join(terms)

def runner(job):
    job.additer(termMapper, sumreducer, combiner = sumreducer)
    job.additer(docTermCountMapper, docTermCountReducer)
    job.additer(corpusTermCountMapper, CorpusTermCountReducer)
    job.additer(finalMapper, finalReducer)

if __name__ == "__main__":
    main(runner)
