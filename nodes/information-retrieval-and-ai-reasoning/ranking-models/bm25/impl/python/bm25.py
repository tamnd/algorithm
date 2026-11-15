# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bm25/. The authors are listed in prov/T2NA0M.jsonl.
"""Okapi BM25 over a small in-memory collection.

All logs are natural logs. The score of document d for query q is

    sum over distinct t in q of  IDF(t) * tf (k1 + 1) / (tf + k1 (1 - b + b |d| / avgdl)) * QTF(t)

where QTF is qtf when k3 is None (k3 infinite), and (k3 + 1) qtf / (k3 + qtf) otherwise.
"""

import math
from typing import Optional


def idf_lucene(n_docs: int, df: int) -> float:
    """The idf of Lucene's BM25, ln(1 + (N - df + 0.5) / (df + 0.5)). Always positive."""
    return math.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))


def idf_rsj(n_docs: int, df: int) -> float:
    """The Robertson-Sparck Jones weight with no relevance information, ln((N - df + 0.5) / (df + 0.5)).

    It is 0 when df = N / 2 and negative when df > N / 2.
    """
    return math.log((n_docs - df + 0.5) / (df + 0.5))


IDFS = {"lucene": idf_lucene, "rsj": idf_rsj}


class BM25:
    """A BM25 index over documents given as token lists, keyed by comparable ids."""

    def __init__(self, docs: dict, k1: float = 1.2, b: float = 0.75,
                 k3: Optional[float] = None, idf: str = "lucene") -> None:
        if k1 < 0 or not 0 <= b <= 1:
            raise ValueError("need k1 >= 0 and 0 <= b <= 1")
        self.k1, self.b, self.k3 = k1, b, k3
        self.idf_fn = IDFS[idf]
        self.n_docs = len(docs)
        self.length = {d: len(toks) for d, toks in docs.items()}
        total = sum(self.length.values())
        self.avgdl = total / self.n_docs if self.n_docs else 0.0
        self.postings: dict = {}  # term -> list of (doc id, tf), in increasing id order
        for d in sorted(docs):
            counts: dict = {}
            for t in docs[d]:
                counts[t] = counts.get(t, 0) + 1
            for t, f in counts.items():
                self.postings.setdefault(t, []).append((d, f))

    def df(self, term: str) -> int:
        return len(self.postings.get(term, ()))

    def idf(self, term: str) -> float:
        return self.idf_fn(self.n_docs, self.df(term))

    def length_factor(self, doc_id) -> float:
        """B(d) = 1 - b + b |d| / avgdl, the pivoted length normalizer with slope b."""
        return 1.0 - self.b + self.b * self.length[doc_id] / self.avgdl

    def tf_part(self, tf: int, doc_id) -> float:
        """tf (k1 + 1) / (tf + k1 B(d)): 0 at tf = 0, increasing, and below k1 + 1."""
        return tf * (self.k1 + 1.0) / (tf + self.k1 * self.length_factor(doc_id))

    def qtf_part(self, qtf: int) -> float:
        if self.k3 is None:
            return float(qtf)
        return (self.k3 + 1.0) * qtf / (self.k3 + qtf)

    def rank(self, query: list, k: Optional[int] = None) -> list:
        """Documents that contain at least one query term, as (id, score) pairs.

        Order: score descending, then id ascending. Term-at-a-time with one accumulator per document.
        Cost: O(sum of df over the query terms) plus a sort of the matching documents.
        """
        qtf: dict = {}
        for t in query:
            qtf[t] = qtf.get(t, 0) + 1
        acc: dict = {}
        for t, f in qtf.items():
            plist = self.postings.get(t)
            if not plist:
                continue
            w = self.idf(t) * self.qtf_part(f)
            for d, tf in plist:
                acc[d] = acc.get(d, 0.0) + w * self.tf_part(tf, d)
        out = sorted(acc.items(), key=lambda p: (-p[1], p[0]))
        return out if k is None else out[:k]
