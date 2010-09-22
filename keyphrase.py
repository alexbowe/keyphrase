# Python libs
import re

# Third Party Libs
from dumbo import opt, run
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
numKeyphrases = 10
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

# Takes (filename, line-num) pairs as keys, and a segment of text as the value
# Outputs filenames as keys, and a list of (word, freq) pairs
# Requires -addpath yes flag
@opt("addpath", "yes")
def mapper(key, value):
    if DEBUG and key[1] is 0:
        import sys
        sys.stderr.write(str(key[0]) + ", " + str(key[1]) +": " + value + "\n")
    fd = FreqDist()
    value = stripChars.sub(' ', value)
    toks = word_tokenize(value)
    postoks = nltk.tag.pos_tag(toks)
    #cleanToks = list(cleanWords(toks))
    
    t = chunker.parse(postoks)
    for l in genNPLeaves(t):
        words = map(lambda w:w[0], l)
        words = list(cleanWords(words))
        gram = ' '.join(words)
        fd.inc(gram, 1)
    
    #for n in range(1,4):
    #    for gram in genNGrams(cleanToks, n, 5):
    #        gram = ' '.join(gram)
    #        import math
    #        # rating needed here, if i use a FreqDist
    #        fd.inc(gram, math.log(n))
    
    yield key[0], fd.items()

# Takes filenames as keys, and a list of (word, freq) pairs
# Outputs filename as key, and a comma separated string of top N words
def reducer(key, values):
    fd = FreqDist()
    for row in values:
        for word, freq in row:
            fd.inc(word, freq)
    keyphrases = fd.keys()[:numKeyphrases]
    yield key, separator.join(keyphrases)

if __name__ == "__main__":
    run(mapper, reducer)
