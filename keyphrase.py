from dumbo import opt, run
from nltk.stem.porter import PorterStemmer
from nltk.probability import FreqDist
from nltk import word_tokenize

import mycorpus

stopwords = mycorpus.stopwords
numKeyphrases = 10
separator = ','

# Takes (filename, line-num) pairs as keys, and a segment of text as the value
# Outputs filenames as keys, and a list of (word, freq) pairs
# Requires -addpath yes flag
@opt("addpath", "yes")
def mapper(key, value):
    fd = FreqDist()
    for word in word_tokenize(value):
        word = word.lower()
        # TODO: Strip unwanted symbols (quotes, %, etc...)
        # check length, and chunking
        if word not in stopwords:
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
