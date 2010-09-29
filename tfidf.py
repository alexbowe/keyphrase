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

def docTermCountMapper( (docname, term), (payload, n)):
    """
    Reorders input for next phase (which is per document).
    
    OUT: docname, (term, payload, n)
    n is the number of occurences of this term in this document.
    """
    yield docname, (term, payload, n)
    
def docTermCountReducer(docname, values):
    """
    Calculates the total count of terms in this document.
    
    OUT: (term, docname), (payload, n, N)
    n is the number of occurences of this term in this document.
    N is the total number of terms in this document.
    """
    values = list(values)
    # Total count of term across all docs
    N = sum(n for (term, payload, n) in values)
    for (term, payload, n) in values:
        yield (term, docname), (payload, n, N)

# IN : (term, docname), (payload, n, N)
# OUT: term, (docname, payload, n, N, 1)
def corpusTermCountMapper( (term, docname), (payload, n, N) ):
    """
    Reorders the input to enable counting of how many documents
    this term appears in.
    
    OUT: term, (docname, payload, n, N, 1)
    n is the number of occurences of this term in this document.
    N is the total number of terms in this document.
    """
    yield term, (docname, payload, n, N, 1)

def corpusTermCountCombiner(term, values):
    """Combiner to sum the count of how many documents this term appears in."""
    values = list(values)
    d = sum(v[-1] for v in values)
    for v in values:
        v = list(v)
        yield term, tuple(v[:-1] + [d])

def corpusTermCountReducer(term, values):
    """
    Reorders the output to be per document (rather than per term) and
    finishes summing the number of times the term appears across the corpus.
    
    OUT: docname, (term, payload, n, N, d)
    n is the number of occurences of this term in this document.
    N is the total number of terms in this document.
    d is the number of documents this term appears in.
    """
    values = list(values)
    d = sum(c for (docname, payload, n, N, c) in values)
    for (docname, payload, n, N) in (v[:4] for v in values):
        yield docname, (term, payload, n, N, d)

def add_iters(job):
    """Utility function for adding the TFIDF iterations in the right order."""
    job.additer(docTermCountMapper, docTermCountReducer)
    job.additer(corpusTermCountMapper, corpusTermCountReducer,
        combiner = corpusTermCountCombiner)
