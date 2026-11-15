# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/document-at-a-time-evaluation/. The authors are listed in prov/CR25E3.jsonl.
"""Document-at-a-time (DAAT) evaluation of a ranked query.

An index maps each term to its posting list: a list of (docid, weight)
pairs in increasing docid order. The weight is the contribution of the
term to the score of the document, for example a BM25 term weight. The
score of a document for a query is the sum of the weights of the query
terms that it contains, added in query order. A document matches when it
contains at least one query term. Results rank by score descending, then
by docid ascending.
"""

import heapq
import math

END = math.inf  # the docid of a cursor that is past the end of its list


class Stats:
    """Work counters: documents fully scored and posting weights read."""

    def __init__(self):
        self.scored = 0
        self.postings = 0


class Cursor:
    """A forward-only cursor on one posting list."""

    def __init__(self, postings, stats):
        self.ids = [d for d, _ in postings]
        self.ws = [w for _, w in postings]
        self.i = 0
        self.stats = stats

    def docid(self):
        return self.ids[self.i] if self.i < len(self.ids) else END

    def weight(self):
        self.stats.postings += 1
        return self.ws[self.i]

    def next(self):
        self.i += 1


class TopK:
    """The best k (docid, score) pairs seen so far.

    The heap holds (score, -docid), so its minimum is the entry of lowest
    score and, among equal scores, of largest docid: the entry that the
    tie rule ranks last. A new document replaces it only on a strictly
    greater score. Documents arrive in increasing docid order, so an equal
    score never displaces a smaller docid.
    """

    def __init__(self, k):
        self.k = k
        self.heap = []

    def offer(self, d, s):
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, (s, -d))
            return True
        if s > self.heap[0][0]:
            heapq.heapreplace(self.heap, (s, -d))
            return True
        return False

    def result(self):
        return sorted(((-nd, s) for s, nd in self.heap), key=lambda p: (-p[1], p[0]))


def daat(index, query, k):
    """Return (the top k as a list of (docid, score), Stats).

    query is a list of distinct terms. Terms missing from the index have an
    empty posting list.
    """
    stats = Stats()
    if k <= 0:
        return [], stats
    cursors = [Cursor(index.get(t, []), stats) for t in query]  # @line L1
    top = TopK(k)  # @line L2
    d = min((c.docid() for c in cursors), default=END)  # @line L3
    while d != END:  # @line L4
        s = 0  # @line L5
        for c in cursors:  # @line L6
            if c.docid() == d:  # @line L7
                s = s + c.weight()
                c.next()
        stats.scored += 1
        top.offer(d, s)  # @line L8
        d = min(c.docid() for c in cursors)  # @line L9
    return top.result(), stats  # @line L10


def bm25_index(docs, k1=1.2, b=0.75):
    """Build an index of BM25 term weights with the Lucene IDF.

    docs maps docid to a list of tokens. The weight of t in d is
    IDF(t) * tf (k1 + 1) / (tf + k1 (1 - b + b |d| / avgdl)) with
    IDF(t) = ln(1 + (N - df + 0.5) / (df + 0.5)), which is positive.
    """
    n = len(docs)
    avgdl = sum(len(toks) for toks in docs.values()) / n
    counts = {}
    for d in sorted(docs):
        seen = {}
        for tok in docs[d]:
            seen[tok] = seen.get(tok, 0) + 1
        for t, f in seen.items():
            counts.setdefault(t, []).append((d, f))
    index = {}
    for t, plist in counts.items():
        df = len(plist)
        idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
        index[t] = [
            (d, idf * f * (k1 + 1) / (f + k1 * (1 - b + b * len(docs[d]) / avgdl)))
            for d, f in plist
        ]
    return index


def exhaustive_top_k(index, query, k, doc_ids):
    """Score every document of doc_ids, then sort. The reference method."""
    if k <= 0:
        return []
    lookup = [dict(index.get(t, [])) for t in query]
    scored = []
    for d in doc_ids:
        s = 0
        hit = False
        for table in lookup:
            if d in table:
                s = s + table[d]
                hit = True
        if hit:
            scored.append((d, s))
    scored.sort(key=lambda p: (-p[1], p[0]))
    return scored[:k]
