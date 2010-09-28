# Python libs
import re
import pickle
from math import log, sqrt

# Third Party Libs
from dumbo import *
import nltk

# My Libs
from mycorpus import stopwords

# Program Variables
minLength = 3
maxLength = 40
maxGram = 4
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

with open('pos_tag.pkl', 'rb') as f:
    postagger = pickle.load(f)

grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}
        
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
    postoks = postagger.tag(toks)
    tree = chunker.parse(postoks)
    
    pos = 0
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf if acceptableWord(w) ]
        if not acceptableGram(t):
            continue
        payload = (lineNum is 0, pos)
        yield (docname, term), (payload, 1)
        pos += 1

def termReducer( (docname, term), values ):
    values = list(values)
    inT = [ inT for _,inT in (p for p,n in values)]
    inT = reduce(lambda a,b: a or b, inT)
    pos = min( [ pos for pos,_ in (p for p,n in values) ] )
    n = sum( [ n for p,n in values ] )
    payload = (inT, pos)
    yield (docname, term), (payload, n)

# n - term-count for the doc
# N - term-count for all docs
# payload - optional package that gets carried to the end
# IN : (docname, term), (payload, n)
# OUT: docname, (term, payload, n)
def docTermCountMapper( (docname, term), (payload, n)):
    yield docname, (term, payload, n)
    
# IN : docname, (term, payload, n)-list
# OUT: (term, docname), (payload, n, N)
def docTermCountReducer(docname, values):
    values = list(values)
    # Total count of term across all docs
    N = sum(n for (term, payload, n) in values)
    for (term, payload, n) in values:
        yield (term, docname), (payload, n, N)

# IN : (term, docname), (payload, n, N)
# OUT: term, (docname, payload, n, N, 1)
def corpusTermCountMapper( (term, docname), (payload, n, N) ):
    yield term, (docname, payload, n, N, 1)

class CorpusTermCountReducer:
    def __init__(self):
        # get -param doccount
        self.doccount = float(self.params['doccount'])
    def __call__(self, term, values):
        values = list(values)
        m = sum(c for (docname, payload, n, N, c) in values)
        idf = log(self.doccount / m)
        for (docname, payload, n, N) in (v[:4] for v in values):
            tf = (float(n)/N)
            relative_pos = float(payload[1])/n
            yield docname, (term, (payload[0], relative_pos), tf * idf)

def finalReducer(docname, values):
    terms = []
    fd = nltk.probability.FreqDist()
    values = list(values)
    for term, (inTitle, relative_pos), tf_idf in values:
        term_str = ' '.join(term)
        
        if inTitle:
            terms.append(term_str)
        else:
            score = tf_idf #* relative_pos
            fd.inc(term_str, score)
    
    terms += fd.keys()[:len(fd)*1/2]
    yield docname, separator.join(terms)

def runner(job):
    job.additer(termMapper, termReducer, combiner = termReducer)
    job.additer(docTermCountMapper, docTermCountReducer)
    job.additer(corpusTermCountMapper, CorpusTermCountReducer)
    job.additer(identitymapper, finalReducer)

if __name__ == "__main__":
    main(runner)
