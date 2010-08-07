from dumbo import opt, run
from nltk.corpus import stopwords
from nltk.probability import FreqDist

stopwords = stopwords.words('english')
numKeyphrases = 10

@opt("addpath", "yes")
def mapper(key, value):
    for word in value.split():
        #stem word
        #stop word
        yield key[0], (word, 1)

def reducer(key,value):
    fd = FreqDist()
    for word, freq in value:
        fd.inc(word, freq)
    yield key, fd.keys()[:numKeyphrases]

if __name__ == "__main__":
    run(mapper, reducer)
