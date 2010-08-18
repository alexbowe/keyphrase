# Python libs
import re
from string import *

# Third Party Libs
from dumbo import opt, run
from nltk.stem.porter import PorterStemmer
from nltk.probability import FreqDist
from nltk import word_tokenize

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
    # Strip unwanted symbols (quotes, %, etc...)
    cleanword = stripChars.sub(' ', word)
    cleanword = rstrip(cleanword, '.')
    cleanword = strip(cleanword, '-')
    return cleanword

# Takes (filename, line-num) pairs as keys, and a segment of text as the value
# Outputs filenames as keys, and a list of (word, freq) pairs
# Requires -addpath yes flag
@opt("addpath", "yes")
def mapper(key, value):
    fd = FreqDist()
    # TODO: chunking or multi-grams
    value = stripChars.sub(' ', value)
    for word in word_tokenize(value):
        word = cleanUpWord(word)
        if acceptable(word):
            word = word.lower()
            word = PorterStemmer().stem_word(word)
            fd.inc(word, 1)
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
