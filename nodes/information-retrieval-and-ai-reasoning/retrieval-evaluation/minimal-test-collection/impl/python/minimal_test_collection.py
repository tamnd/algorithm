# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimal-test-collection/. The authors are listed in prov/19JM8C.jsonl.

from fractions import Fraction
from typing import Callable, Hashable, Optional, Sequence

Pair = tuple[Hashable, Hashable]


def coefficients(a: Sequence[Hashable], b: Sequence[Hashable]) -> tuple[list[Hashable], dict[Pair, Fraction]]:
    """Return the pooled documents (sorted) and c[(i, j)] for i <= j with
    R * (AP(a) - AP(b)) = sum of c[(i, j)] * x_i * x_j, where x_d is 1 if d is relevant.

    Precondition: a and b have no repeated document and the ids are comparable.
    For one ranking, c_ii = 1 / rank(i) and c_ij = 1 / max(rank(i), rank(j)).
    Exact fractions keep the signs exact. Time and space O(m^2) for m pooled documents.
    """
    ra = {d: r + 1 for r, d in enumerate(a)}
    rb = {d: r + 1 for r, d in enumerate(b)}
    docs = sorted(set(a) | set(b))

    def one(rank: dict, i: Hashable, j: Hashable) -> Fraction:
        if i in rank and j in rank:
            return Fraction(1, max(rank[i], rank[j]))
        return Fraction(0)

    c: dict[Pair, Fraction] = {}
    for x, i in enumerate(docs):
        for j in docs[x:]:
            c[(i, j)] = one(ra, i, j) - one(rb, i, j)
    return docs, c


def pair(c: dict[Pair, Fraction], i: Hashable, j: Hashable) -> Fraction:
    return c[(i, j)] if (i, j) in c else c[(j, i)]


def bounds(c: dict[Pair, Fraction], judged: dict[Hashable, int]) -> tuple[Fraction, Fraction]:
    """Return (lo, hi) with lo <= D <= hi for D = sum c_ij x_i x_j and every
    relevance of the documents not judged.

    A term with a judged nonrelevant document is 0, a term with two judged
    relevant documents is c_ij, and any other term lies between min(0, c_ij)
    and max(0, c_ij). Time O(m^2).
    """
    lo = hi = Fraction(0)
    for (i, j), v in c.items():
        xi, xj = judged.get(i), judged.get(j)
        if xi == 0 or xj == 0:
            continue
        if xi == 1 and xj == 1:
            lo += v
            hi += v
        else:
            lo += min(0, v)
            hi += max(0, v)
    return lo, hi


def weights(docs: Sequence[Hashable], c: dict[Pair, Fraction], judged: dict[Hashable, int], i: Hashable) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Return (wR, wN, vR, vN): the rise of lo and the fall of hi if i is judged
    relevant (R) or not relevant (N). Precondition: i is not judged. Time O(m)."""
    w_r = w_n = v_r = v_n = Fraction(0)
    for j in docs:
        xj = judged.get(j)
        if xj == 0:
            continue
        v = pair(c, i, j)
        if j == i or xj == 1:  # the term becomes the constant c_ij
            w_r += max(0, v)
            v_r += max(0, -v)
        w_n += max(0, -v)  # the term becomes 0
        v_n += max(0, v)
    return w_r, w_n, v_r, v_n


def minimal_test_collection(
    a: Sequence[Hashable],
    b: Sequence[Hashable],
    judge: Callable[[Hashable], int],
    p: Fraction = Fraction(1, 2),
    budget: Optional[int] = None,
) -> tuple[Optional[int], list[Hashable]]:
    """Judge pooled documents one at a time until the sign of AP(a) - AP(b) is fixed.

    Precondition: judge(d) returns 1 for a relevant document and 0 otherwise.
    Returns (sign, order). The sign is 1, -1 or 0 when every relevance of the
    documents not judged gives that sign of R * (AP(a) - AP(b)), and None when
    the budget runs out first. Each step costs O(m^2), so O(m^3) in total.
    """
    docs, c = coefficients(a, b)  # @line L1
    judged: dict[Hashable, int] = {}  # @line L2
    order: list[Hashable] = []
    while True:  # @line L3
        lo, hi = bounds(c, judged)  # @line L4
        if lo > 0:  # @line L5
            return 1, order
        if hi < 0:
            return -1, order
        if lo == hi:
            return 0, order
        if budget is not None and len(order) >= budget:  # @line L6
            return None, order
        best, best_score = None, Fraction(-1)
        for i in docs:  # @line L7
            if i in judged:
                continue
            w_r, w_n, v_r, v_n = weights(docs, c, judged, i)
            score = max(p * w_r, (1 - p) * w_n, p * v_r, (1 - p) * v_n)  # @line L8
            if score > best_score:  # @line L9
                best, best_score = i, score
        judged[best] = judge(best)  # @line L10
        order.append(best)
