# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rnc-perfect-matching/. The authors are listed in prov/7TA0S6.jsonl.

import random
from fractions import Fraction


def rnc_perfect_matching(
    n: int, edges: list[tuple[int, int]], trials: int = 20, rng: random.Random | None = None
) -> list[int] | None:
    """A perfect matching of a general graph, unweighted, by the Mulmuley-Vazirani-Vazirani method.

    The vertices are 0 .. n-1 and edges lists undirected edges (no loops; repeats
    are ignored). Returns mate with mate[v] the partner of v, or None. A returned
    matching is always checked and correct. None is always correct when the graph
    has no perfect matching; when it has one, None is returned with probability
    at most 2^(-trials). This is a sequential simulation: each trial does exact
    integer linear algebra, which the parallel algorithm does in O(log^2 n) depth.
    """
    rng = rng or random.Random()
    adj: set[tuple[int, int]] = set()
    for a, b in edges:
        if a == b or not (0 <= a < n and 0 <= b < n):
            raise ValueError("edges must join two different vertices in range")
        adj.add((min(a, b), max(a, b)))
    pairs = sorted(adj)
    m = len(pairs)
    for _ in range(trials):  # @line L1
        w = {e: rng.randint(1, max(1, 2 * m)) for e in pairs}  # @line L2
        mat = [[0] * n for _ in range(n)]  # @line L3
        for (i, j), wt in w.items():
            mat[i][j] = 1 << wt
            mat[j][i] = -(1 << wt)
        det = _determinant(mat)  # @line L4
        if det == 0:
            continue
        twice_w = _two_adic_valuation(det)  # @line L5
        if twice_w % 2:
            continue
        adjugate = _adjugate(mat, det)  # @line L6
        mate = [-1] * n
        ok = True
        for (i, j), wt in w.items():  # @line L7
            val = abs(adjugate[j][i]) << wt
            if val % (1 << twice_w) == 0 and (val >> twice_w) % 2 == 1:
                if mate[i] >= 0 or mate[j] >= 0:
                    ok = False
                    break
                mate[i], mate[j] = j, i
        if ok and all(x >= 0 for x in mate):  # @line L8
            return mate
    return None  # @line L9


def _two_adic_valuation(x: int) -> int:
    """The largest t with 2^t dividing the nonzero integer x."""
    x = abs(x)
    return (x & -x).bit_length() - 1


def _determinant(a: list[list[int]]) -> int:
    """Exact determinant of an integer matrix by Bareiss fraction-free elimination."""
    n = len(a)
    m = [row[:] for row in a]
    sign, prev = 1, 1
    for k in range(n - 1):
        if m[k][k] == 0:
            for r in range(k + 1, n):
                if m[r][k] != 0:
                    m[k], m[r] = m[r], m[k]
                    sign = -sign
                    break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = (m[i][j] * m[k][k] - m[i][k] * m[k][j]) // prev
        prev = m[k][k]
    return sign * m[n - 1][n - 1] if n else 1


def _adjugate(a: list[list[int]], det: int) -> list[list[int]]:
    """adj(a) = det(a) * a^(-1) for an invertible integer matrix, by exact Gauss-Jordan."""
    n = len(a)
    m = [[Fraction(x) for x in row] + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(a)]
    for k in range(n):
        p = next(r for r in range(k, n) if m[r][k] != 0)
        m[k], m[p] = m[p], m[k]
        piv = m[k][k]
        m[k] = [x / piv for x in m[k]]
        for r in range(n):
            if r != k and m[r][k] != 0:
                f = m[r][k]
                m[r] = [x - f * y for x, y in zip(m[r], m[k])]
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            v = m[i][n + j] * det
            assert v.denominator == 1
            row.append(int(v))
        out.append(row)
    return out
