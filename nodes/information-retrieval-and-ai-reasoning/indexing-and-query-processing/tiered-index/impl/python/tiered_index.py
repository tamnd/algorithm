# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tiered-index/. The authors are listed in prov/J6839A.jsonl.
"""A tiered index and top-k query evaluation over its tiers.

A document-ordered index maps each term to a list of (docid, weight)
pairs in increasing docid order, with weights at least 0. The score of a
document is the sum of the weights of the query terms that it contains.
A document matches when it contains at least one query term. Results rank
by score descending, then by docid ascending.

The tiered index cuts each posting list by global weight thresholds
tau_1 > tau_2 > ... > tau_r > 0. Tier 1 holds the postings with weight at
least tau_1, tier j the postings with tau_j <= w < tau_(j-1), and the last
tier, r + 1, the postings with w < tau_r. Each tier list is in docid order.

search reads the tiers in order. For each document that it meets for the
first time it computes the full score by random access to the
document-ordered lists. It has two stop rules:

  "safe"    after tier j, stop when the k-th best full score is at least
            the sum of tau_j over the query terms. Every unseen document
            has a smaller score, so the result is the exact top k.
  "approx"  after a tier, stop when at least k documents have been seen.
            This is the rule in Manning, Raghavan and Schuetze, 7.2.1. It
            returns true scores, but can miss documents of the true top k.
"""

import heapq
import math


class Stats:
    """Work counters: documents fully scored, tier postings read, random
    accesses made, and tiers read."""

    def __init__(self):
        self.scored = 0
        self.postings = 0
        self.lookups = 0
        self.tiers = 0


def build(index, taus):
    """Build the tiers. taus is strictly decreasing and positive."""
    tiers = [{} for _ in range(len(taus) + 1)]
    for t, plist in index.items():
        for d, w in plist:
            j = 0
            while j < len(taus) and w < taus[j]:
                j += 1
            tiers[j].setdefault(t, []).append(d)
    return tiers


def best_k(full, k):
    """The k best (docid, score) pairs, by the tie rule."""
    return heapq.nsmallest(k, full.items(), key=lambda p: (-p[1], p[0]))


def search(index, tiers, taus, query, k, stop="safe"):
    """Return (the top k as a list of (docid, score), Stats)."""
    stats = Stats()
    if k <= 0:
        return [], stats
    lookup = [dict(index.get(t, [])) for t in query]
    full = {}  # @line L1
    for j, tier in enumerate(tiers):  # @line L2
        stats.tiers += 1
        for t in query:  # @line L3
            for d in tier.get(t, []):
                stats.postings += 1
                if d not in full:  # @line L4
                    s = 0
                    for table in lookup:
                        stats.lookups += 1
                        if d in table:
                            s = s + table[d]
                    stats.scored += 1
                    full[d] = s  # @line L5
        if j == len(taus):
            break
        if stop == "approx" and len(full) >= k:  # @line L6
            break
        if stop == "safe" and len(full) >= k:  # @line L7
            bound = taus[j] * len(query)
            if best_k(full, k)[-1][1] >= bound:
                break
    return best_k(full, k), stats  # @line L8


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
