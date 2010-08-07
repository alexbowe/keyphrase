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
    
# extract document id in mapper
# mapper() -> stop-filtered stemmed words (or bi-words) + key, 1
# sumreduce combiner
# reducer() -> reads values into DistFreq and prints the top ten
    
def reducer(key,values):
    for words in values:
        yield key, values

if __name__ == "__main__":
    run(mapper)
