def tfidf(n, N, d, D):
    """
    Calculates TF-IDF score from:
                Term count in document,
                Number of terms in document,
                Number of documents this term appears in,
                Total number of documents
    """
    from math import log
    tf = float(n)/N
    idf = log(float(D) / d)
    return tf * idf

# n - term-count for the doc
# N - term-count for all docs
# payload - optional package that gets carried to the end
# IN : (docname, term), (payload, n)
# OUT: docname, (term, payload, n)
def docTermCountMapper( (docname, term), (payload, n)):
    yield docname, (term, payload, n)
    
# IN : docname, (term, payload, n)-list
# OUT: (term, docname), (payload, n, N)
def docTermCountReducer(docname, values):
    values = list(values)
    # Total count of term across all docs
    N = sum(n for (term, payload, n) in values)
    for (term, payload, n) in values:
        yield (term, docname), (payload, n, N)

# IN : (term, docname), (payload, n, N)
# OUT: term, (docname, payload, n, N, 1)
def corpusTermCountMapper( (term, docname), (payload, n, N) ):
    yield term, (docname, payload, n, N, 1)

def corpusTermCountCombiner(term, values):
    values = list(values)
    d = sum(v[-1] for v in values)
    for v in values:
        v = list(v)
        yield term, tuple(v[:-1] + [d])

# IN : term, (docname, (payload, n, N, 1)
# OUT: term, (docname, payload, n, N, 1)
def corpusTermCountReducer(term, values):
    values = list(values)
    d = sum(c for (docname, payload, n, N, c) in values)
    for (docname, payload, n, N) in (v[:4] for v in values):
        yield docname, (term, payload, n, N, d)

def add_iters(job):
    #from dumbo import *
    job.additer(docTermCountMapper, docTermCountReducer)
    job.additer(corpusTermCountMapper, corpusTermCountReducer,
        combiner = corpusTermCountCombiner)
