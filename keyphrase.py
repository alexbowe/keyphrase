from dumbo import *
import tfidf
import nltk

# Program Variables
minLength = 3
maxLength = 40
maxGram = 4
separator = ','             # Seps terms in output

# Used when tokenizing words
sentence_re = r'''(?x)      # set flag to allow verbose regexps
      ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*            # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
    | \.\.\.                # ellipsis
    | [][.,;"'?():-_`]      # these are separate tokens
'''

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

import pickle
with open('pos_tag.pkl', 'rb') as f:
    postagger = pickle.load(f)

grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""
chunker = nltk.RegexpParser(grammar)

def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.node=='NP'):
        yield subtree.leaves()

def normalise(word):
    """Normalises words to lowercase and stems it."""
    word = word.lower()
    word = stemmer.stem_word(word)
    return word

def acceptableWord(word):
    """Checks conditions for acceptable word: length, stopword."""
    from mycorpus import stopwords
    accepted = bool(minLength <= len(word) <= maxLength
        and word.lower() not in stopwords)
    return accepted

def acceptableGram(gram):
    """Checks that the n-gram is appropriate length."""
    return bool(1 <= len(gram) <= maxGram)

@opt("addpath", "yes")
def termMapper( (docname, lineNum), line):
    """    
    Tokenizes, Lemmatizes, POS-Tags and chunks to find noun phrases.
    
    Output: (docname, candidate), (payload, 1)
    
    A payload is information we want to carry through all MapReduce phases
    until we need it, e.g. If the term is in the title, or its position.
    """
    toks = nltk.regexp_tokenize(line, sentence_re)
    toks = [ lemmatizer.lemmatize(t) for t in toks ]
    postoks = postagger.tag(toks)
    tree = chunker.parse(postoks)
    
    position = 0
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf if acceptableWord(w) ]
        if not acceptableGram(t):
            continue
        # Titles appear on line 0
        payload = (lineNum is 0, position)
        yield (docname, term), (payload, 1)
        position += 1

def reducePayloads(a, b):
    """
    Reduces two payloads (corresponding to the same term), for use in a
    reducer/combiner.
    
    The reduction will return if it is in the title, and the earliest position.
    
    E.g: For a term that is in the title one time, and appears at position 5
    and 17:
    >>> reducePayloads( (True, 5), (False, 17) )
    (True, 5)
    """
    return a[0] or b[0], min(a[1], b[1])

def termReducer( (docname, term), values ):
    """Reduces the payload and sums the count over terms per document.
    Can be used as a combinator too.
    
    Output: (docname, candidate), (payload, # of occurences)
    """
    values = list(values)
    payload = reduce(reducePayloads, [p for p,n in values])
    n = sum( [ n for p,n in values ] )
    yield (docname, term), (payload, n)

class FinalReducer:
    """
    Ranks and outputs candidate terms. All title terms are output,
    and an upper fraction (based on score) of terms are further selected.
    """
    # Upper percentage of terms to output
    upper_fraction = 0.5
    
    def __init__(self):
        # requires -param doccount D
        self.doccount = float(self.params['doccount'])
    def __call__(self, docname, values):
        terms = []
        fd = nltk.probability.FreqDist()
        
        for (term, (inTitle, position), n, N, d) in values:
            #relativePos = float(position)/m
            term_str = ' '.join(term)
        
            if inTitle:
                terms.append(term_str)
            else:
                score = tfidf.tfidf(n, N, d, self.doccount)
                #score *= relative_pos
                fd.inc(term_str, score)
        
        # top upper_fraction of terms
        n = int(self.upper_fraction * len(fd))
        terms += fd.keys()[:n]
        yield docname, separator.join(terms)

def runner(job):
    job.additer(termMapper, termReducer, combiner = termReducer)
    tfidf.add_iters(job)
    job.additer(identitymapper, FinalReducer)

if __name__ == "__main__":
    main(runner)
