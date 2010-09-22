# Python libs
import re

# Third Party Libs
from dumbo import *
from nltk.stem.porter import PorterStemmer
from nltk.probability import FreqDist
from nltk import word_tokenize
import nltk

# My Libs
import mycorpus

# Run Flags
DEBUG = 0

# Program Variables
stopwords = mycorpus.stopwords
badChars = re.compile(r'[^\w\-\/\.]')
stripChars = re.compile(r'[,\'\"\d]')
minLength = 3
maxLength = 40
separator = ','

def acceptableLength(word):
    return minLength <= len(word) <= maxLength

def isClean(word):
    return not bool(badChars.search(word))

def acceptable(word):
    accepted = bool( isClean(word) and acceptableLength(word) and
        word.lower() not in stopwords )
    if DEBUG and not accepted:
        import sys
        sys.stderr.write("Not accepted: " + word + "\n")
    return accepted

def cleanUpWord(word):
    from string import strip, rstrip
    # Strip unwanted symbols (quotes, %, etc...)
    cleanword = stripChars.sub(' ', word)
    cleanword = rstrip(cleanword, '.')
    cleanword = strip(cleanword, '-')
    return cleanword

def genNGrams(words, n):
    for index, word in enumerate(words):
        ngram = words[index:index+n]
        if len(ngram) is n:
            yield ngram
            
def genNGramsWindowed(words, n, w=0):
    if w < n:
        w = n
    for index, word in enumerate(words):
        window = words[index+1:index+w]
        from itertools import combinations
        if len(window) > n -1:
            for c in combinations(window, n-1):
                ngram = [word] + list(c)
                if len(ngram) is n:
                    yield ngram
            
def genNPLeaves(tree):
    for subtree in tree.subtrees(filter=lambda t:t.node=='NP'):
        yield subtree.leaves()

# could change this to a function per word for map()
def cleanWords(toks):
    for word in toks:
        # clean up
        word = cleanUpWord(word)
        if acceptable(word):
            word = word.lower()
            word = PorterStemmer().stem_word(word)
            yield word

grammar = "NP: {<DT>?<JJ>*<NN>+}"
chunker = nltk.RegexpParser(grammar)

# Mapper: Extracts Terms from a Document
# IN : key = (docname, line#), value = line
# OUT: (docname, term), 1
# Requires -addpath yes flag
@opt("addpath", "yes")
def termMapper( (docname, lineNum), line):
    if DEBUG and lineNum is 0:
        import sys
        sys.stderr.write(str(docname) + ", " + str(lineNum) +": " + line + "\n")
    toks = word_tokenize(line)
    postoks = nltk.tag.pos_tag(toks)
    chunkTree = chunker.parse(postoks)
    
    for leaf in genNPLeaves(chunkTree):
        words = map(lambda w:w[0], leaf)
        words = list(cleanWords(words))
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

from math import log
class CorpusTermCountReducer:
    def __init__(self):
        self.doccount = float(self.params['doccount'])
    def __call__(self, term, values):
        values = list(values)
        m = sum(c for (docname, n, N, c) in values)
        for (docname, n, N) in (v[:3] for v in values):
            yield (term, docname), (float(n)/N) * log(self.doccount / m)

def finalMapper((term, docname), tf_idf):
    yield docname, (term, tf_idf)

def finalReducer(docname, values):
    fd = FreqDist()
    for (term, tf_idf) in values:
        fd.inc(term, tf_idf)
    phrases = fd.keys()[:10]
    yield docname, separator.join(phrases)

def runner(job):
    job.additer(termMapper, sumreducer, combiner = sumreducer)
    job.additer(docTermCountMapper, docTermCountReducer)
    job.additer(corpusTermCountMapper, CorpusTermCountReducer)
    job.additer(finalMapper, finalReducer)

if __name__ == "__main__":
    main(runner)
