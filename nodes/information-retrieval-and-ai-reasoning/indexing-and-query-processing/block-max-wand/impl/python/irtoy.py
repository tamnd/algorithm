# SPDX-License-Identifier: MIT
# Shared helper of the information retrieval pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""The toy collection of the information retrieval pages.

Eight short documents, four queries with graded judgments and one fixed
run. Tokens are the lower-case words split on spaces, with no stemming
and no stop words. The helper holds only the data and the statistics
tokenize, tf, df, cf, doc_len and avgdl. Scoring and metrics live on the
pages that define them.
"""

DOCS = {
    1: "binary search finds a key in a sorted array",
    2: "merge sort merges two sorted runs into one sorted array",
    3: "an inverted index maps each term to a posting list",
    4: "a posting list is a sorted list of document ids",
    5: "skip pointers speed up the merge of two posting lists",
    6: "a hash table finds a key in constant expected time",
    7: "search engines rank documents by a score for the query",
    8: "the sorted array of ids is compressed with gap encoding",
}

N = len(DOCS)

QUERIES = {
    "q1": "sorted array search",
    "q2": "posting list merge",
    "q3": "rank documents",
    "q4": "quantum circuit",
}

# Graded judgments: 2 is highly relevant, 1 is relevant, absent is 0.
QRELS = {
    "q1": {1: 2, 2: 1, 8: 1},
    "q2": {5: 2, 4: 1, 3: 1},
    "q3": {7: 2},
    "q4": {},
}

# A fixed run for the metric pages, as scores per query.
RUN = {
    "q1": {1: 2.0, 6: 2.0, 8: 1.5, 2: 1.0, 4: 1.0},
}


def tokenize(text):
    """Lower-case words split on spaces."""
    return text.lower().split()


_TOKENS = {d: tokenize(t) for d, t in DOCS.items()}


def tf(term, doc_id):
    """Number of times term occurs in document doc_id."""
    return _TOKENS[doc_id].count(term)


def df(term):
    """Number of documents that contain term."""
    return sum(1 for toks in _TOKENS.values() if term in toks)


def cf(term):
    """Number of occurrences of term in the whole collection."""
    return sum(toks.count(term) for toks in _TOKENS.values())


def doc_len(doc_id):
    """Number of tokens in document doc_id."""
    return len(_TOKENS[doc_id])


def avgdl():
    """Average document length in tokens."""
    return sum(len(toks) for toks in _TOKENS.values()) / N
