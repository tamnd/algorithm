# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bond-energy-algorithm/. The authors are listed in prov/J9KWFD.jsonl.

"""The bond energy algorithm (BEA) and the split step of vertical fragmentation.

Attributes are numbered 0 to n - 1. A workload is a list of queries; query q
uses the set of attributes use[q] and runs freq[q] times in total (summed over
all sites). The attribute affinity matrix is

    aff[i][j] = sum of freq[q] over the queries q that use both i and j.

The bond of two columns x and y of a symmetric non-negative matrix M is
bond(x, y) = sum over z of M[z][x] * M[z][y]. For an order of the columns
(and the same order of the rows), the global affinity measure is

    AM = sum over j of bond(c_j, c_(j-1)) + bond(c_j, c_(j+1)),

with bond 0 for a neighbor outside the order. It is the measure of
effectiveness of McCormick, Schweitzer and White for a symmetric matrix whose
rows and columns are permuted together.
"""

from itertools import permutations
from collections.abc import Sequence

Matrix = list[list[int]]


def affinity_matrix(n: int, use: Sequence[set[int]], freq: Sequence[int]) -> Matrix:
    """aff[i][j]: the total frequency of the queries that use both attribute i and attribute j."""
    aff = [[0] * n for _ in range(n)]
    for attrs, f in zip(use, freq):
        for i in attrs:
            for j in attrs:
                aff[i][j] += f
    return aff


def bond(m: Matrix, x: int | None, y: int | None) -> int:
    """sum_z m[z][x] * m[z][y]; 0 when x or y is an empty neighbor (None)."""
    if x is None or y is None:
        return 0
    return sum(row[x] * row[y] for row in m)


def global_affinity(m: Matrix, order: Sequence[int]) -> int:
    """AM of a column order: twice the sum of the bonds of neighboring columns."""
    return 2 * sum(bond(m, order[k], order[k + 1]) for k in range(len(order) - 1))


def measure_of_effectiveness(m: Matrix, order: Sequence[int]) -> int:
    """McCormick's ME of the matrix with rows and columns both permuted by order, by its definition:
    1/2 * sum_ij a_ij (a_i,j-1 + a_i,j+1 + a_i-1,j + a_i+1,j), with zero outside the matrix."""
    n = len(order)
    a = [[m[order[i]][order[j]] for j in range(n)] for i in range(n)]
    get = lambda i, j: a[i][j] if 0 <= i < n and 0 <= j < n else 0
    total = 0
    for i in range(n):
        for j in range(n):
            total += a[i][j] * (get(i, j - 1) + get(i, j + 1) + get(i - 1, j) + get(i + 1, j))
    return total // 2


def cont(m: Matrix, left: int | None, k: int, right: int | None) -> int:
    """The change of AM when column k goes between left and right."""
    return 2 * bond(m, left, k) + 2 * bond(m, k, right) - 2 * bond(m, left, right)


def bea(m: Matrix, trace: list | None = None) -> tuple[list[int], Matrix]:
    """BEA as used for vertical fragmentation: insert the columns in index order,
    each at the position of largest contribution (the leftmost one on a tie).
    Return the column order and the clustered matrix (rows in the same order)."""
    n = len(m)
    order = list(range(min(n, 2)))  # @line L1
    for k in range(2, n):  # @line L2
        best_loc, best = 0, None
        for loc in range(len(order) + 1):  # @line L3
            left = order[loc - 1] if loc > 0 else None
            right = order[loc] if loc < len(order) else None
            c = cont(m, left, k, right)  # @line L4
            if trace is not None:
                trace.append((k, loc, c))
            if best is None or c > best:
                best_loc, best = loc, c
        order.insert(best_loc, k)  # @line L5
    clustered = [[m[i][j] for j in order] for i in order]  # @line L6
    return order, clustered  # @line L7


def bea_original(m: Matrix, first: int = 0) -> list[int]:
    """The form of McCormick et al.: at each step try every unplaced column at every
    position and place the one with the largest contribution (cheapest insertion)."""
    n = len(m)
    if n == 0:
        return []
    order = [first]
    rest = [k for k in range(n) if k != first]
    while rest:
        best = None
        for k in rest:
            for loc in range(len(order) + 1):
                left = order[loc - 1] if loc > 0 else None
                right = order[loc] if loc < len(order) else None
                c = cont(m, left, k, right)
                if best is None or c > best[0]:
                    best = (c, k, loc)
        _, k, loc = best
        order.insert(loc, k)
        rest.remove(k)
    return order


def best_order(m: Matrix) -> tuple[int, list[int]]:
    """The largest AM over all orders, by brute force (small n only)."""
    n = len(m)
    if n > 8:
        raise ValueError("brute force is for at most 8 columns")
    best, arg = -1, list(range(n))
    for perm in permutations(range(n)):
        v = global_affinity(m, perm)
        if v > best:
            best, arg = v, list(perm)
    return best, arg


def split_scores(order: Sequence[int], use: Sequence[set[int]], freq: Sequence[int]) -> list[tuple[int, int, int, int]]:
    """For each split point i (top = order[:i], bottom = order[i:]) return
    (CTQ, CBQ, COQ, z) with z = CTQ * CBQ - COQ ** 2. Queries with no attribute are ignored."""
    out = []
    for i in range(1, len(order)):
        top, bottom = set(order[:i]), set(order[i:])
        ctq = cbq = coq = 0
        for attrs, f in zip(use, freq):
            if not attrs:
                continue
            if attrs <= top:
                ctq += f
            elif attrs <= bottom:
                cbq += f
            else:
                coq += f
        out.append((ctq, cbq, coq, ctq * cbq - coq * coq))
    return out


def split(order: Sequence[int], use: Sequence[set[int]], freq: Sequence[int],
          key: Sequence[int] = ()) -> tuple[list[int], list[int]]:
    """Cut the clustered order in two at the split point of largest z (the first one on a tie).
    The key attributes are added to both fragments."""
    if len(order) < 2:
        raise ValueError("need at least two non-key attributes to split")
    scores = split_scores(order, use, freq)
    i = max(range(len(scores)), key=lambda t: (scores[t][3], -t)) + 1
    top = list(key) + [a for a in order[:i] if a not in key]
    bottom = list(key) + [a for a in order[i:] if a not in key]
    return top, bottom
