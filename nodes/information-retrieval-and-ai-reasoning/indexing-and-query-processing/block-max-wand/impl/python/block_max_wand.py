# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-max-wand/. The authors are listed in prov/MB0KJQ.jsonl.
"""Block-Max WAND top-k evaluation of a ranked query.

An index maps each term to its posting list: a list of (docid, weight)
pairs in increasing docid order, with weights at least 0. The score of a
document is the sum of the weights of the query terms that it contains.
A document matches when it contains at least one query term. Results rank
by score descending, then by docid ascending.

Each list is cut into blocks of b consecutive postings. For each block the
index stores its last docid and its largest weight, the block max. The
method first finds a WAND pivot with the list-wide upper bounds. Then it
checks the pivot again with the block maxes of the blocks that can hold
it. If that sum is not greater than the threshold, no document from the
pivot up to the end of the shortest of those blocks can enter the top k,
and the cursors jump past that range.

This version moves all the cursors up to the pivot when the block check
fails. Other implementations move only one cursor; both are safe. The
method is safe when the score arithmetic is exact.
"""

import heapq
import math
from bisect import bisect_left

END = math.inf  # the docid of a cursor that is past the end of its list


class Stats:
    """Work counters: documents fully scored and posting weights read."""

    def __init__(self):
        self.scored = 0
        self.postings = 0


class Cursor:
    """A cursor on one posting list, with block metadata.

    The block pointer moves on its own (a shallow move) and reads only the
    block metadata, not the postings.
    """

    def __init__(self, postings, stats, b):
        self.ids = [d for d, _ in postings]
        self.ws = [w for _, w in postings]
        self.ub = max(self.ws, default=0)
        self.last = [self.ids[min(i + b, len(self.ids)) - 1] for i in range(0, len(self.ids), b)]
        self.bmax = [max(self.ws[i:i + b]) for i in range(0, len(self.ids), b)]
        self.blk = 0
        self.i = 0
        self.stats = stats

    def docid(self):
        return self.ids[self.i] if self.i < len(self.ids) else END

    def weight(self):
        self.stats.postings += 1
        return self.ws[self.i]

    def next(self):
        self.i += 1

    def next_geq(self, d):
        """Move to the first posting with docid >= d."""
        self.i = bisect_left(self.ids, d, self.i)

    def shallow(self, d):
        """Move the block pointer to the first block whose last docid >= d."""
        self.blk = bisect_left(self.last, d, self.blk)

    def block_max(self):
        """The block max of the current block, or 0 past the last block."""
        return self.bmax[self.blk] if self.blk < len(self.bmax) else 0

    def block_last(self):
        """The last docid of the current block, or END past the last block."""
        return self.last[self.blk] if self.blk < len(self.last) else END


class TopK:
    """The best k (docid, score) pairs seen so far.

    The heap holds (score, -docid), so its minimum is the entry that the
    tie rule ranks last. A new document replaces it only on a strictly
    greater score.
    """

    def __init__(self, k):
        self.k = k
        self.heap = []

    def threshold(self):
        """The lowest score in a full heap, or None while it is not full."""
        return self.heap[0][0] if len(self.heap) == self.k else None

    def offer(self, d, s):
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, (s, -d))
        elif s > self.heap[0][0]:
            heapq.heapreplace(self.heap, (s, -d))

    def result(self):
        return sorted(((-nd, s) for s, nd in self.heap), key=lambda p: (-p[1], p[0]))


def find_pivot(cursors, theta):
    """The least p whose prefix bound sum beats the threshold, or None."""
    acc = 0
    for p, c in enumerate(cursors):
        if c.docid() == END:
            return None
        acc = acc + c.ub
        if theta is None or acc > theta:
            return p
    return None


def block_max_wand(index, query, k, b=64):
    """Return (the top k as a list of (docid, score), Stats).

    query is a list of distinct terms; b is the block size.
    """
    stats = Stats()
    if k <= 0:
        return [], stats
    by_query = [Cursor(index.get(t, []), stats, b) for t in query]  # @line L1
    cursors = list(by_query)
    top = TopK(k)  # @line L2
    while True:  # @line L3
        cursors.sort(key=lambda c: c.docid())  # @line L4
        theta = top.threshold()
        p = find_pivot(cursors, theta)  # @line L5
        if p is None:  # @line L6
            return top.result(), stats
        d = cursors[p].docid()  # @line L7
        while p + 1 < len(cursors) and cursors[p + 1].docid() == d:  # @line L8
            p += 1
        bsum = 0
        for c in cursors[:p + 1]:  # @line L9
            c.shallow(d)
            bsum = bsum + c.block_max()
        if theta is None or bsum > theta:  # @line L10
            if cursors[0].docid() == d:  # @line L11
                s = 0
                for c in by_query:
                    if c.docid() == d:
                        s = s + c.weight()
                        c.next()
                stats.scored += 1
                top.offer(d, s)  # @line L12
            else:  # @line L13
                j = p
                while cursors[j].docid() == d:
                    j -= 1
                cursors[j].next_geq(d)
        else:  # @line L14
            nxt = min(c.block_last() for c in cursors[:p + 1]) + 1  # @line L15
            if p + 1 < len(cursors):
                nxt = min(nxt, cursors[p + 1].docid())
            for c in cursors[:p + 1]:  # @line L16
                c.next_geq(nxt)


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


def daat_scored(index, query):
    """The number of documents that plain DAAT scores: the matching ones."""
    union = set()
    for t in query:
        union.update(d for d, _ in index.get(t, []))
    return len(union)
