from dumbo import opt, run
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.probability import FreqDist

stopwords = stopwords.words('english')
numKeyphrases = 10
separator = ','

@opt("addpath", "yes")
def mapper(key, value):
    fd = FreqDist()
    for word in value.split():
        word = word.lower()
        if word not in stopwords:
            word = PorterStemmer().stem_word(word)
            fd.inc(word, 1)
    yield key[0], fd.items()

def reducer(key, values):
    fd = FreqDist()
    for row in values:
        for word, freq in row:
            fd.inc(word, freq)
    yield key, separator.join(fd.keys()[:numKeyphrases])

if __name__ == "__main__":
    run(mapper, reducer)
