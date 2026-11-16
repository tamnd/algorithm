# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/apsp-negative-triangle-equivalence/. The authors are listed in prov/ZT8VGE.jsonl.

"""The subcubic reductions between APSP, the min-plus product and negative triangle.

A tripartite instance has parts I, J and K, given by three matrices:
A[i][j] is the weight of the edge between i in I and j in J, B[j][k] the
weight of the edge between j in J and k in K, and D[i][k] the weight of the
edge between k in K and i in I. None means that the edge is missing. The
weight of the triangle (i, j, k) is A[i][j] + B[j][k] + D[i][k].

A detector is a function detect(A, B, D, I, J, K) that returns True when the
subgraph on the index lists I, J and K has a triangle of negative weight. The
reductions use it as a black box.
"""

from math import ceil, log2

Matrix = list[list]


def _halves(xs: list[int]) -> list[list[int]]:
    if len(xs) <= 1:
        return [xs]
    h = len(xs) // 2
    return [xs[:h], xs[h:]]


def find_negative_triangle(A: Matrix, B: Matrix, D: Matrix,
                           I: list[int], J: list[int], K: list[int], detect):
    """Return a negative triangle (i, j, k) of the subgraph on I, J and K.

    The subgraph must have one. Each round keeps one of at most 8 subgraphs
    that has a negative triangle, so it makes at most 8 calls per round and
    at most ceil(log2(max part size)) rounds.
    """
    while len(I) > 1 or len(J) > 1 or len(K) > 1:  # @line L14
        parts = [(I2, J2, K2) for I2 in _halves(I) for J2 in _halves(J) for K2 in _halves(K)]  # @line L15
        for I2, J2, K2 in parts:
            if detect(A, B, D, I2, J2, K2):  # @line L16
                I, J, K = I2, J2, K2
                break
        else:
            raise ValueError("the subgraph has no negative triangle")
    return I[0], J[0], K[0]  # @line L17


def groups(m: int, s: int) -> list[list[int]]:
    """Split 0..m-1 into consecutive groups of at most s indices."""
    return [list(range(t, min(t + s, m))) for t in range(0, m, s)]


def all_pairs_negative_triangle(A: Matrix, B: Matrix, D: Matrix, detect) -> set[tuple[int, int]]:
    """Return the set of pairs (i, k) whose edge lies on a negative triangle.

    The detector is called only on subgraphs with at most s vertices per part,
    where s = ceil(n^(1/3)) and n is the largest part size.
    """
    nI, nJ = len(A), len(B)
    nK = len(B[0]) if nJ else 0
    n = max(nI, nJ, nK, 1)
    s = 1
    while s ** 3 < n:  # @line L7
        s += 1
    D = [row[:] for row in D]  # the deletions below must not change the input
    Y: set[tuple[int, int]] = set()  # @line L8
    for Ia in groups(nI, s):  # @line L9
        for Jb in groups(nJ, s):
            for Kc in groups(nK, s):
                while detect(A, B, D, Ia, Jb, Kc):  # @line L10
                    i, j, k = find_negative_triangle(A, B, D, Ia, Jb, Kc, detect)  # @line L11
                    Y.add((i, k))  # @line L12
                    D[i][k] = None
    return Y  # @line L13


def min_plus_via_negative_triangle(A: Matrix, B: Matrix, detect) -> Matrix:
    """The min-plus product C[i][k] = min over j of A[i][j] + B[j][k].

    None stands for +infinity. Every entry is found by a binary search, and
    all the searches run in parallel: each round makes one call to
    all_pairs_negative_triangle. The number of rounds is ceil(log2(4M + 2)),
    where M is the largest absolute value of a finite entry.
    """
    nI, nJ = len(A), len(B)
    nK = len(B[0]) if nJ else 0
    M = max([abs(x) for row in A + B for x in row if x is not None], default=0)
    top = 2 * M + 1  # stands for +infinity: every finite entry of C is at most 2M
    lo = [[-2 * M] * nK for _ in range(nI)]  # @line L1
    hi = [[top] * nK for _ in range(nI)]
    while any(lo[i][k] < hi[i][k] for i in range(nI) for k in range(nK)):  # @line L2
        mid = [[(lo[i][k] + hi[i][k]) // 2 for k in range(nK)] for i in range(nI)]  # @line L3
        D = [[-(mid[i][k] + 1) for k in range(nK)] for i in range(nI)]
        Y = all_pairs_negative_triangle(A, B, D, detect)  # @line L4
        for i in range(nI):  # @line L5
            for k in range(nK):
                if lo[i][k] == hi[i][k]:
                    continue
                if (i, k) in Y:
                    hi[i][k] = mid[i][k]
                else:
                    lo[i][k] = mid[i][k] + 1
    return [[None if lo[i][k] == top else lo[i][k] for k in range(nK)] for i in range(nI)]  # @line L6


def search_rounds(M: int) -> int:
    """The number of rounds of min_plus_via_negative_triangle for entries bounded by M."""
    return ceil(log2(4 * M + 2))


def negative_triangle_via_min_plus(A: Matrix, B: Matrix, D: Matrix, product) -> bool:
    """One min-plus product and O(n^2) more work decide negative triangle."""
    C = product(A, B)
    return any(
        C[i][k] is not None and D[i][k] is not None and C[i][k] + D[i][k] < 0
        for i in range(len(C))
        for k in range(len(C[i]))
    )


def apsp_via_min_plus(W: Matrix, product) -> Matrix:
    """Distances by repeated squaring; W has no negative cycle, None means no edge."""
    n = len(W)
    dist = [[0 if i == j else W[i][j] for j in range(n)] for i in range(n)]
    length = 1
    while length < n - 1:
        dist = product(dist, dist)
        length *= 2
    return dist


def min_plus_via_apsp(A: Matrix, B: Matrix, apsp) -> Matrix:
    """One APSP call on a layered graph with 3n vertices gives the min-plus product."""
    nI, nJ = len(A), len(B)
    nK = len(B[0]) if nJ else 0
    N = nI + nJ + nK
    W: Matrix = [[None] * N for _ in range(N)]
    for i in range(nI):
        for j in range(nJ):
            W[i][nI + j] = A[i][j]
    for j in range(nJ):
        for k in range(nK):
            W[nI + j][nI + nJ + k] = B[j][k]
    dist = apsp(W)
    return [[dist[i][nI + nJ + k] for k in range(nK)] for i in range(nI)]


def tripartite_copy(W: Matrix) -> tuple[Matrix, Matrix, Matrix]:
    """Map a directed graph to a tripartite instance with the same answer.

    The triangle (i, j, k) of the copy has weight W[i][j] + W[j][k] + W[k][i].
    Self-loops are dropped, so the three vertices of a negative triangle of
    the copy are distinct vertices of the graph.
    """
    n = len(W)
    E = [[None if i == j else W[i][j] for j in range(n)] for i in range(n)]
    A = [row[:] for row in E]
    B = [row[:] for row in E]
    D = [[E[k][i] for k in range(n)] for i in range(n)]
    return A, B, D
