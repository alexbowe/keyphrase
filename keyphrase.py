from dumbo import opt, run
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.probability import FreqDist

stopwords = stopwords.words('english')
numKeyphrases = 10
separator = ','

@opt("addpath", "yes")
def mapper(key, value):
    for word in value.split():
        word = word.lower()
        if word not in stopwords:
            word = PorterStemmer().stem_word(word)
            yield key[0], (word, 1)

def combiner(key, values):
    fd = FreqDist()
    for word, freq in values:
        fd.inc(word, freq)
    for word, freq in fd.items():
        yield key, (word, freq)

def reducer(key, values):
    fd = FreqDist()
    for word, freq in values:
        fd.inc(word, freq)
    yield key, separator.join(fd.keys()[:numKeyphrases])

if __name__ == "__main__":
    run(mapper, reducer, combiner)
