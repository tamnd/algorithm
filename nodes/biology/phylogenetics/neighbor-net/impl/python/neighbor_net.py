# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neighbor-net/. The authors are listed in prov/DQBMCY.jsonl.

"""NeighborNet (Bryant and Moulton 2004): a circular order and weighted circular splits.

Part 1 finds a circular order of the taxa by agglomeration. Nodes are grouped
in clusters of one or two adjacent nodes. Each round picks two clusters by the
neighbor-joining criterion on average cluster distances, then one node in each
by the same criterion with the nodes of the two clusters taken separately, and
joins them. A node with two neighbors in a cluster is reduced: the chain
x - y - z becomes u - v with

    d(u, a) = (alpha + beta) d(x, a) + gamma d(y, a)
    d(v, a) = alpha d(y, a) + (beta + gamma) d(z, a)
    d(u, v) = alpha d(x, y) + beta d(x, z) + gamma d(y, z)

and alpha = beta = gamma = 1/3. At the end, the reductions are undone in
reverse order, which turns u, v back into x, y, z in the circular order.

Part 2 fits nonnegative weights to all circular splits of that order by
least squares with the Lawson-Hanson active set method, in exact arithmetic.
"""

from fractions import Fraction
from itertools import combinations
from typing import Dict, FrozenSet, List, Optional, Sequence, Tuple

Matrix = Sequence[Sequence[Fraction]]
THIRD = Fraction(1, 3)


def find_ordering(d: Matrix, alpha: Fraction = THIRD, beta: Fraction = THIRD, gamma: Fraction = THIRD) -> List[int]:
    n = len(d)
    if n <= 3:
        return list(range(n))
    dist: Dict[int, Dict[int, Fraction]] = {i: {j: Fraction(d[i][j]) for j in range(n)} for i in range(n)}
    clusters: List[List[int]] = [[i] for i in range(n)]  # @line L1
    history: List[Tuple[int, int, int, int, int]] = []
    nxt = n

    def dd(a: int, b: int) -> Fraction:
        return Fraction(0) if a == b else dist[a][b]

    def dc(p: List[int], q: List[int]) -> Fraction:
        return sum((dd(a, b) for a in p for b in q), Fraction(0)) / (len(p) * len(q))

    while sum(len(c) for c in clusters) > 3:  # @line L2
        m = len(clusters)
        rows = [sum((dc(clusters[i], clusters[k]) for k in range(m) if k != i), Fraction(0)) for i in range(m)]
        best = None
        for i, j in combinations(range(m), 2):  # @line L3
            q = (m - 2) * dc(clusters[i], clusters[j]) - rows[i] - rows[j]
            if best is None or q < best[0]:
                best = (q, i, j)
        _, i, j = best
        ci, cj = clusters[i], clusters[j]
        others = [c for t, c in enumerate(clusters) if t not in (i, j)]
        parts = others + [[x] for x in ci] + [[x] for x in cj]
        mh = len(parts)
        best2 = None
        for xi in ci:  # @line L4
            for xj in cj:
                q = (mh - 2) * dd(xi, xj)
                q -= sum((dc([xi], p) for p in parts), Fraction(0))
                q -= sum((dc([xj], p) for p in parts), Fraction(0))
                if best2 is None or q < best2[0]:
                    best2 = (q, xi, xj)
        _, xi, xj = best2
        left = ci if ci[-1] == xi else ci[::-1]  # xi at the right end
        right = cj if cj[0] == xj else cj[::-1]  # xj at the left end
        chain = left + right  # @line L5
        while len(chain) >= 3:  # @line L6
            x, y, z = chain[0], chain[1], chain[2]
            u, v = nxt, nxt + 1
            nxt += 2
            dist[u], dist[v] = {}, {}
            for a in list(dist):
                if a in (u, v, x, y, z):
                    continue
                dist[u][a] = dist[a][u] = (alpha + beta) * dd(x, a) + gamma * dd(y, a)
                dist[v][a] = dist[a][v] = alpha * dd(y, a) + (beta + gamma) * dd(z, a)
            dist[u][v] = dist[v][u] = alpha * dd(x, y) + beta * dd(x, z) + gamma * dd(y, z)
            for g in (x, y, z):
                del dist[g]
                for a in dist:
                    dist[a].pop(g, None)
            history.append((u, v, x, y, z))
            chain = [u, v] + chain[3:]
        clusters = others + [chain]
    # With at most 3 nodes left, every order is circular and keeps each pair adjacent.
    order = [x for c in clusters for x in c]  # @line L7
    for u, v, x, y, z in reversed(history):  # @line L8
        k = len(order)
        p, q = order.index(u), order.index(v)
        if (p + 1) % k == q:
            seq = [x, y, z]
        elif (q + 1) % k == p:
            seq = [z, y, x]
            p, q = q, p
        else:
            raise AssertionError("u and v are not adjacent")
        # replace the adjacent pair at positions p, p+1 (mod k) by seq
        rot = order[p:] + order[:p]
        order = seq + rot[2:]
    return order


def circular_splits(order: Sequence[int]) -> List[FrozenSet[int]]:
    """All n(n-1)/2 splits whose sides are intervals of the circular order, as the side without order[0]."""
    n = len(order)
    out = []
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            out.append(frozenset(order[i:j]))
    return out


def _solve(a: List[List[Fraction]], b: List[Fraction]) -> Optional[List[Fraction]]:
    """Gaussian elimination in exact arithmetic; None if singular."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        piv = next((r for r in range(c, n) if m[r][c] != 0), None)
        if piv is None:
            return None
        m[c], m[piv] = m[piv], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [m[r][t] - f * m[c][t] for t in range(n + 1)]
    return [m[i][n] / m[i][i] for i in range(n)]


def design(n: int, splits: Sequence[FrozenSet[int]]) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    return pairs, [[1 if (i in s) != (j in s) else 0 for s in splits] for i, j in pairs]


def nnls(a: List[List[int]], b: List[Fraction]) -> List[Fraction]:
    """Lawson-Hanson: minimize |a w - b|^2 subject to w >= 0, exactly."""
    rows, cols = len(a), len(a[0]) if a else 0
    ata = [[sum((a[r][i] * a[r][j] for r in range(rows)), 0) for j in range(cols)] for i in range(cols)]
    atb = [sum((a[r][i] * b[r] for r in range(rows)), Fraction(0)) for i in range(cols)]
    w = [Fraction(0)] * cols
    passive: List[int] = []

    def grad() -> List[Fraction]:  # atb - ata w, the negative gradient / 2
        return [atb[i] - sum((ata[i][j] * w[j] for j in range(cols)), Fraction(0)) for i in range(cols)]

    def ls(p: List[int]) -> List[Fraction]:
        sol = _solve([[Fraction(ata[i][j]) for j in p] for i in p], [atb[i] for i in p])
        assert sol is not None, "the columns of a passive set are independent"
        z = [Fraction(0)] * cols
        for t, i in enumerate(p):
            z[i] = sol[t]
        return z

    while True:
        g = grad()
        cand = [i for i in range(cols) if i not in passive and g[i] > 0]
        if not cand:
            return w
        k = max(cand, key=lambda i: (g[i], -i))
        passive.append(k)
        while True:
            z = ls(passive)
            if all(z[i] > 0 for i in passive):
                w = z
                break
            step = min(w[i] / (w[i] - z[i]) for i in passive if z[i] <= 0)
            w = [w[i] + step * (z[i] - w[i]) for i in range(cols)]
            passive = [i for i in passive if w[i] > 0]


def neighbor_net(d: Matrix) -> Tuple[List[int], Dict[FrozenSet[int], Fraction]]:
    """Return the circular order and the circular splits with positive least squares weights.

    A split is the side that does not hold order[0].
    """
    n = len(d)
    for i in range(n):
        if d[i][i] != 0 or any(d[i][j] != d[j][i] for j in range(n)):
            raise ValueError("d must be symmetric with a zero diagonal")
    order = find_ordering(d)
    if n < 2:
        return order, {}
    splits = circular_splits(order)
    pairs, a = design(n, splits)
    w = nnls(a, [Fraction(d[i][j]) for i, j in pairs])  # @line L9
    return order, {s: x for s, x in zip(splits, w) if x > 0}  # @line L10
