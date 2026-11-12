# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-distance-problem/. The authors are listed in prov/9K8HSX.jsonl.

"""Two exact algorithms for the minimum distance of a linear code over GF(q), q prime.

min_distance_plain enumerates all q^k - 1 nonzero messages.
min_distance_brouwer is Brouwer's algorithm: it finds m pairwise disjoint
information sets I_1, ..., I_m, a generator matrix G_j that is systematic on
each I_j, and enumerates the messages of weight w = 1, 2, ... for every G_j.
After round w, every codeword not yet seen has weight at least w + 1 on each
I_j, so its weight is at least m (w + 1). The search stops when the best
weight found is at most this lower bound.

Both functions take a generator matrix of full rank k >= 1 and return
(d, the number of codewords they computed).
"""

from itertools import combinations, product

Matrix = list[list[int]]


def weight(v: list[int]) -> int:
    return sum(1 for x in v if x)


def combine(g: Matrix, rows: tuple[int, ...], coeffs: tuple[int, ...], q: int) -> list[int]:
    n = len(g[0])
    out = [0] * n
    for i, a in zip(rows, coeffs):
        row = g[i]
        for j in range(n):
            out[j] = (out[j] + a * row[j]) % q
    return out


def min_distance_plain(g: Matrix, q: int = 2) -> tuple[int, int]:
    """Weight of the lightest nonzero codeword over all q^k - 1 messages. Cost: Θ(q^k n k)."""
    k = len(g)
    best, count = len(g[0]) + 1, 0
    for m in product(range(q), repeat=k):
        if any(m):
            count += 1
            best = min(best, weight(combine(g, tuple(range(k)), m, q)))
    return best, count


def systematic_on(g: Matrix, allowed: list[int], q: int) -> tuple[Matrix, list[int]] | None:
    """Row reduce g with pivots only in the allowed columns.

    Returns (G', pivots) with G' systematic on the pivot columns, or None when
    the allowed columns have rank less than k.
    """
    m = [list(r) for r in g]
    k = len(m)
    pivots: list[int] = []
    rank = 0
    for col in allowed:
        piv = next((i for i in range(rank, k) if m[i][col] % q), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        inv = pow(m[rank][col], q - 2, q)
        m[rank] = [x * inv % q for x in m[rank]]
        for i in range(k):
            if i != rank and m[i][col]:
                f = m[i][col]
                m[i] = [(x - f * y) % q for x, y in zip(m[i], m[rank])]
        pivots.append(col)
        rank += 1
        if rank == k:
            return m, pivots
    return None


def disjoint_information_sets(g: Matrix, q: int) -> list[Matrix]:
    """Greedy: take an information set among the columns not used yet, while one exists."""
    n = len(g[0])
    used: set[int] = set()
    mats: list[Matrix] = []
    while True:
        res = systematic_on(g, [j for j in range(n) if j not in used], q)
        if res is None:
            return mats
        mat, pivots = res
        mats.append(mat)
        used.update(pivots)


def min_distance_brouwer(g: Matrix, q: int = 2) -> tuple[int, int]:
    """Brouwer's algorithm with disjoint information sets. Returns (d, codewords computed)."""
    k, n = len(g), len(g[0])
    mats = disjoint_information_sets(g, q)
    m = len(mats)
    best, count = n + 1, 0
    for w in range(1, k + 1):
        for gj in mats:
            for rows in combinations(range(k), w):
                # Scalar multiples have the same weight: fix the first coefficient to 1.
                for rest in product(range(1, q), repeat=w - 1):
                    count += 1
                    best = min(best, weight(combine(gj, rows, (1,) + rest, q)))
        if best <= m * (w + 1):
            return best, count
    return best, count
