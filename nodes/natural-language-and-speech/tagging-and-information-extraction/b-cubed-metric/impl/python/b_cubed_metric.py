# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-cubed-metric/. The authors are listed in prov/3YEMMH.jsonl.

"""The B-cubed coreference score (Bagga and Baldwin 1998), and the MUC score for contrast.

A clustering is a list of clusters, each a collection of mention ids; the key
(gold) and the response (system) clusterings must cover the same mentions,
each mention exactly once. All values are exact Fractions.

B-cubed: for each mention m, let K(m) be its key cluster and R(m) its response
cluster. Its precision is |K(m) & R(m)| / |R(m)| and its recall is
|K(m) & R(m)| / |K(m)|. The score averages these over the mentions, with equal
weights, and F is the harmonic mean of the two averages.

MUC (Vilain et al. 1995): recall is the sum over key clusters K of
|K| - |p(K)|, divided by the sum of |K| - 1, where p(K) is the set of parts
that the response cuts K into. Precision swaps the roles of key and response.
"""

from fractions import Fraction
from typing import Dict, Hashable, Iterable, List, Sequence, Tuple

Clustering = Sequence[Iterable[Hashable]]


def index(clusters: Clustering) -> Tuple[List[frozenset], Dict[Hashable, int]]:
    """The clusters as frozensets, and the cluster number of each mention."""
    sets = [frozenset(c) for c in clusters]
    where: Dict[Hashable, int] = {}
    for k, c in enumerate(sets):
        if not c:
            raise ValueError("empty cluster")
        for m in c:
            if m in where:
                raise ValueError("mention in two clusters: %r" % (m,))
            where[m] = k
    return sets, where


def _check(key: Clustering, response: Clustering):
    ks, kw = index(key)
    rs, rw = index(response)
    if set(kw) != set(rw):
        raise ValueError("key and response must cover the same mentions")
    return ks, kw, rs, rw


def harmonic(p: Fraction, r: Fraction) -> Fraction:
    return 2 * p * r / (p + r) if p + r else Fraction(0)


def b_cubed(key: Clustering, response: Clustering) -> Tuple[Fraction, Fraction, Fraction]:
    """B-cubed precision, recall and F1, each mention with weight 1/N."""
    ks, kw, rs, rw = _check(key, response)
    n = len(kw)
    if n == 0:
        return Fraction(0), Fraction(0), Fraction(0)
    p = r = Fraction(0)
    for m in kw:  # @line L1
        k, s = ks[kw[m]], rs[rw[m]]
        both = len(k & s)  # @line L2
        p += Fraction(both, len(s))  # @line L3
        r += Fraction(both, len(k))  # @line L4
    p, r = p / n, r / n  # @line L5
    return p, r, harmonic(p, r)  # @line L6


def _muc_recall(ks: List[frozenset], rw: Dict[Hashable, int]) -> Fraction:
    num = den = 0
    for k in ks:
        parts = {rw[m] for m in k}
        num += len(k) - len(parts)
        den += len(k) - 1
    return Fraction(num, den) if den else Fraction(0)


def muc(key: Clustering, response: Clustering) -> Tuple[Fraction, Fraction, Fraction]:
    """MUC precision, recall and F1 (a ratio with a zero denominator is taken as 0)."""
    ks, kw, rs, rw = _check(key, response)
    r = _muc_recall(ks, rw)
    p = _muc_recall(rs, kw)
    return p, r, harmonic(p, r)
