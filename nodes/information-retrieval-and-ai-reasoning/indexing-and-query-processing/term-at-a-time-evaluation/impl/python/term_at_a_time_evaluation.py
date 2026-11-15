# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/term-at-a-time-evaluation/. The authors are listed in prov/AQAN27.jsonl.
"""Term-at-a-time (TAAT) evaluation of a ranked query.

An index maps each term to its posting list: a list of (docid, weight)
pairs in increasing docid order, with weights at least 0. The score of a
document is the sum of the weights of the query terms that it contains.
A document matches when it contains at least one query term. Results rank
by score descending, then by docid ascending.

taat is the plain method: one accumulator per matching document.
taat_maxscore is the max_score variant of Turtle and Flood: it reads the
terms in decreasing order of their upper bounds, and stops creating new
accumulators once no new document can reach the top k.
"""

import heapq
import math
from bisect import bisect_left


class Stats:
    """Work counters: accumulators created and posting weights read."""

    def __init__(self):
        self.scored = 0
        self.postings = 0


def best_k(acc, k):
    """The k best (docid, score) pairs of the accumulators, by the tie rule."""
    return heapq.nsmallest(k, acc.items(), key=lambda p: (-p[1], p[0]))


def taat(index, query, k):
    """Return (the top k as a list of (docid, score), Stats)."""
    stats = Stats()
    if k <= 0:
        return [], stats
    acc = {}  # @line L1
    for t in query:  # @line L2
        for d, w in index.get(t, []):  # @line L3
            stats.postings += 1
            acc[d] = acc[d] + w if d in acc else w  # @line L4
    stats.scored = len(acc)
    return best_k(acc, k), stats  # @line L5


def taat_maxscore(index, query, k):
    """TAAT that stops creating accumulators when they cannot matter.

    Before term i, R is the sum of the upper bounds of the terms not yet
    read. A document with no accumulator has a final score of at most R.
    Once the k-th largest accumulator is strictly greater than R, no such
    document can enter the top k, so only the existing accumulators are
    updated, by forward skips in the remaining lists.
    """
    stats = Stats()
    if k <= 0:
        return [], stats
    lists = [index.get(t, []) for t in query]
    ub = [max((w for _, w in p), default=0) for p in lists]
    order = sorted(range(len(query)), key=lambda i: -ub[i])  # @line M1
    acc = {}  # @line M2
    or_mode = True
    for pos, i in enumerate(order):  # @line M3
        rest = sum(ub[j] for j in order[pos:])
        if or_mode and len(acc) >= k and best_k(acc, k)[-1][1] > rest:  # @line M4
            or_mode = False
        if or_mode:  # @line M5
            for d, w in lists[i]:
                stats.postings += 1
                acc[d] = acc[d] + w if d in acc else w
        else:  # @line M6
            ids = [d for d, _ in lists[i]]
            j = 0
            for d in sorted(acc):
                j = bisect_left(ids, d, j)
                if j < len(ids) and ids[j] == d:
                    stats.postings += 1
                    acc[d] = acc[d] + lists[i][j][1]
    stats.scored = len(acc)
    return best_k(acc, k), stats  # @line M7


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
