from dumbo import opt, run
from nltk import probability

@opt("addpath", "yes")
def mapper(key, value):
    fd = probability.FreqDist()
    for word in value.split():
        #stem word
        #stop word
        fd.inc(word)
    yield key[0], fd.keys()[:3]
    
def reducer(key,values):
    for word in values:
        yield key, word

if __name__ == "__main__":
    run(mapper, reducer)
