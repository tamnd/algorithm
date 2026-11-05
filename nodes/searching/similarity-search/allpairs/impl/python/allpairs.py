# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/allpairs/. The authors are listed in prov/0NZTCD.jsonl.

from collections import Counter, defaultdict
from collections.abc import Sequence

SparseVector = dict[int, float]


def dot(x: SparseVector, y: SparseVector) -> float:
    if len(x) > len(y):
        x, y = y, x
    return sum(w * y[i] for i, w in x.items() if i in y)


def all_pairs(vectors: Sequence[SparseVector], t: float) -> list[tuple[int, int, float]]:
    """Return all (j, i, x_j . x_i) with j < i and dot product >= t, for nonnegative sparse vectors.

    All-Pairs of Bayardo, Ma and Srikant with the max-weight bound over the whole input.
    Time: O(N log N + C + sum of verified prefix lengths), where C is the number of index entries scanned.
    """
    if t <= 0:
        raise ValueError("the threshold must be positive")
    freq = Counter(i for x in vectors for i, w in x.items() if w > 0)
    rank = {i: r for r, (i, _) in enumerate(sorted(freq.items(), key=lambda kv: (-kv[1], kv[0])))}
    maxw: dict[int, float] = defaultdict(float)  # @line L1
    for x in vectors:
        for i, w in x.items():
            maxw[i] = max(maxw[i], w)
    out: list[tuple[int, int, float]] = []  # @line L2
    index: dict[int, list[tuple[int, float]]] = defaultdict(list)
    prefix: list[SparseVector] = []
    for xid, x in enumerate(vectors):  # @line L3
        out.extend((y, xid, s) for y, s in find_matches(x, index, prefix, t))  # @line L4
        b = 0.0  # @line L5
        unindexed: SparseVector = {}
        for i in sorted((i for i, w in x.items() if w > 0), key=rank.__getitem__):  # @line L6
            b += maxw[i] * x[i]  # @line L7
            if b >= t:  # @line L8
                index[i].append((xid, x[i]))
            else:
                unindexed[i] = x[i]
        prefix.append(unindexed)
    return out  # @line L9


def find_matches(
    x: SparseVector,
    index: dict[int, list[tuple[int, float]]],
    prefix: list[SparseVector],
    t: float,
) -> list[tuple[int, float]]:
    """Return (y, x . y) for each earlier vector y with x . y >= t."""
    acc: dict[int, float] = defaultdict(float)  # @line L10
    for i, w in x.items():  # @line L11
        for y, wy in index.get(i, ()):
            acc[y] += w * wy
    found = []
    for y, a in acc.items():  # @line L12
        if a > 0:
            s = a + dot(x, prefix[y])
            if s >= t:
                found.append((y, s))
    return found  # @line L13
