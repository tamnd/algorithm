# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/impact-ordered-index/. The authors are listed in prov/BBYS9T.jsonl.
"""An impact-ordered index and score-at-a-time (SAAT) query evaluation.

A document-ordered index maps each term to a list of (docid, weight)
pairs in increasing docid order. The impact-ordered index stores, for each
term, a list of segments (impact, docids): the impact is a positive
integer, the docids of a segment are in increasing order, and the segments
are in decreasing order of impact. The score of a document is the sum of
the impacts of the query terms that it contains.

saat reads the segments of all query terms in one global order: impact
descending, then query position. It adds each impact to an accumulator.
It has three stop rules:

  "none"    read every segment. Safe: the exact top k.
  "safe"    stop when the top k documents and their order are fixed. The
            docids and their order are exact; the scores returned are lower
            bounds of the true scores.
  "budget"  stop after a fixed number of postings (anytime ranking). This
            is approximate: each score is the sum of the postings read so
            far, which is at most the true score.
"""

import heapq
import math


class Stats:
    """Work counters: accumulators created and postings read."""

    def __init__(self):
        self.scored = 0
        self.postings = 0


def build(index, levels=None):
    """Build an impact-ordered index from a document-ordered one.

    With levels = None the weights must already be positive integers, and
    they are the impacts. Otherwise each weight w becomes the impact
    1 + floor((levels - 1) * w / W), where W is the largest weight in the
    index, so the impacts are in 1..levels.
    """
    top = max((w for p in index.values() for _, w in p), default=0)
    impacts = {}
    for t, plist in index.items():
        groups = {}
        for d, w in plist:
            if levels is None:
                if w != int(w) or w < 1:
                    raise ValueError("impacts must be positive integers")
                a = int(w)
            else:
                a = 1 + math.floor((levels - 1) * w / top) if top > 0 else 1
            groups.setdefault(a, []).append(d)
        impacts[t] = [(a, groups[a]) for a in sorted(groups, reverse=True)]
    return impacts


def to_document_order(impacts):
    """The document-ordered index with the impacts as weights."""
    index = {}
    for t, segs in impacts.items():
        index[t] = sorted((d, a) for a, ids in segs for d in ids)
    return index


def ranked(acc, n):
    """The n best (docid, score) pairs of the accumulators, by the tie rule."""
    return heapq.nsmallest(n, acc.items(), key=lambda p: (-p[1], p[0]))


def order_is_fixed(acc, k, rest):
    """True when no further postings can change the top k or its order.

    rest bounds the score that any document can still gain. Each of the top
    k must beat the next one by more than rest, and the k-th must beat every
    other document, including those with no accumulator yet, by more than
    rest.
    """
    if len(acc) < k:
        return False
    best = ranked(acc, k + 1)
    for i in range(k - 1):
        if best[i][1] <= best[i + 1][1] + rest:
            return False
    below = best[k][1] if len(best) > k else 0
    return best[k - 1][1] > max(below, 0) + rest


def saat(impacts, query, k, stop="none", budget=0):
    """Return (the top k as a list of (docid, score), Stats)."""
    stats = Stats()
    if k <= 0:
        return [], stats
    lists = [impacts.get(t, []) for t in query]
    segs = sorted(  # @line L1
        (-a, pos, j) for pos, plist in enumerate(lists) for j, (a, _) in enumerate(plist)
    )
    nxt = [plist[0][0] if plist else 0 for plist in lists]  # next unread impact
    acc = {}  # @line L2
    for neg_a, pos, j in segs:  # @line L3
        if stop == "safe" and order_is_fixed(acc, k, sum(nxt)):  # @line L4
            break
        a = -neg_a
        for d in lists[pos][j][1]:  # @line L5
            if stop == "budget" and stats.postings >= budget:
                break
            stats.postings += 1
            acc[d] = acc.get(d, 0) + a  # @line L6
        if stop == "budget" and stats.postings >= budget:
            break
        nxt[pos] = lists[pos][j + 1][0] if j + 1 < len(lists[pos]) else 0
    stats.scored = len(acc)
    return ranked(acc, k), stats  # @line L7


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
