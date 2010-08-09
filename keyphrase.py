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

# Intermediate combiner... interested in knowing if there is a difference
# when using this approach in the mapper instead... to avoid context switching
# and sorting
def combiner(key, values):
    fd = FreqDist()
    # Sum frequencies
    for word, freq in values:
        fd.inc(word, freq)
    # Yield word/frequency tuples
    for word, freq in fd.items():
        yield key, (word, freq)

def reducer(key, values):
    fd = FreqDist()
    for word, freq in values:
        fd.inc(word, freq)
    yield key, separator.join(fd.keys()[:numKeyphrases])

if __name__ == "__main__":
    run(mapper, reducer, combiner)
