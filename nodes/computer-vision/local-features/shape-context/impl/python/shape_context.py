# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shape-context/. The authors are listed in prov/A629T3.jsonl.

"""Shape context descriptors and shape matching by assignment.

Points are (x, y) pairs. For a point p_i, the shape context is the histogram
of the vectors p_j - p_i, j != i, in log-polar bins. Distances are divided by
the mean distance over all n^2 ordered pairs (Belongie, Malik and Puzicha 2002,
Section 3.3), and the radial bins are uniform in log r over [1/8, 2), as in
Appendix A of the paper. Vectors outside that range are not counted. The angle
is atan2(dy, dx) in [0, 2 pi), cut into equal bins. Each histogram is divided
by its total so that it sums to 1 (it stays 0 if no vector falls in a bin).

The cost of matching p_i with q_j is the chi-square statistic
C_ij = 1/2 sum_k (h_i(k) - h_j(k))^2 / (h_i(k) + h_j(k)), with 0/0 taken as 0.
The matching is the assignment of least total cost, found by the Hungarian
method in O(N^3) time. Dummy rows or columns with the constant cost eps_d make
the matrix square and let outliers stay unmatched.
"""

import math
from typing import List, Optional, Sequence, Tuple

Point = Tuple[float, float]


def mean_distance(points: Sequence[Point]) -> float:
    """Mean distance over all n^2 ordered pairs, including i = j."""
    n = len(points)
    total = 0.0
    for a in points:
        for b in points:
            total += math.hypot(b[0] - a[0], b[1] - a[1])
    return total / (n * n)


def shape_contexts(points: Sequence[Point], n_r: int = 5, n_theta: int = 12,
                   r_inner: float = 0.125, r_outer: float = 2.0) -> List[List[float]]:
    """Normalized log-polar histograms, one for each point, with n_r * n_theta bins."""
    n = len(points)
    alpha = mean_distance(points)  # @line L1
    log_in = math.log(r_inner)
    log_span = math.log(r_outer) - log_in
    out = []
    for i in range(n):  # @line L2
        h = [0.0] * (n_r * n_theta)
        xi, yi = points[i]
        for j in range(n):
            if j == i:
                continue
            dx, dy = points[j][0] - xi, points[j][1] - yi
            r = math.hypot(dx, dy) / alpha
            if r < r_inner or r >= r_outer:
                continue
            kr = int(n_r * (math.log(r) - log_in) / log_span)  # @line L3
            kr = min(kr, n_r - 1)
            t = math.atan2(dy, dx) % (2.0 * math.pi)
            kt = min(int(n_theta * t / (2.0 * math.pi)), n_theta - 1)
            h[kr * n_theta + kt] += 1.0  # @line L4
        s = sum(h)
        if s > 0:
            h = [x / s for x in h]  # @line L5
        out.append(h)
    return out


def chi2_cost(h1: Sequence[float], h2: Sequence[float]) -> float:
    """The chi-square cost 1/2 sum (a - b)^2 / (a + b), with 0/0 = 0."""
    c = 0.0
    for a, b in zip(h1, h2):
        if a + b > 0:
            c += (a - b) * (a - b) / (a + b)
    return 0.5 * c


def hungarian(cost: Sequence[Sequence[float]]) -> List[int]:
    """Least-cost assignment of a square matrix: row i goes to column result[i].

    The shortest augmenting path form of the Hungarian method with row and
    column potentials, O(n^3) time.
    """
    n = len(cost)
    inf = float("inf")
    u = [0.0] * (n + 1)
    v = [0.0] * (n + 1)
    p = [0] * (n + 1)  # p[j]: the row matched to column j (1-based), 0 if none
    way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [inf] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = inf
            j1 = 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    result = [0] * n
    for j in range(1, n + 1):
        result[p[j] - 1] = j - 1
    return result


def match_shapes(p: Sequence[Point], q: Sequence[Point], eps_d: Optional[float] = None,
                 **kw) -> Tuple[List[int], float]:
    """Match the points of p to the points of q.

    Returns (m, total): m[i] is the index in q matched to p[i], or -1 when p[i]
    goes to a dummy, and total is the cost of the real pairs plus eps_d for each
    point of the larger set (or both) that goes to a dummy.
    """
    hp = shape_contexts(p, **kw)
    hq = shape_contexts(q, **kw)
    m = len(q)
    c = [[chi2_cost(a, b) for b in hq] for a in hp]  # @line L6
    return assign_with_dummies(c, m, eps_d)


def pad_with_dummies(c: Sequence[Sequence[float]], m: int, eps_d: Optional[float]) -> List[List[float]]:
    """Make the n x m cost matrix square with dummy rows and columns.

    With eps_d given, the result is (n + m) x (n + m): each real point can go
    to a dummy at the cost eps_d, and a dummy pair costs 0. Without eps_d, the
    smaller side is padded to max(n, m) with the cost 1, the largest possible
    chi-square cost, which is then the same for every assignment.
    """
    n = len(c)
    if eps_d is None and n == m:
        return [list(row) for row in c]
    eps = 1.0 if eps_d is None else eps_d
    size = n + m if eps_d is not None else max(n, m)
    full = [[0.0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if i < n and j < m:
                full[i][j] = c[i][j]
            elif i < n or j < m:
                full[i][j] = eps
    return full


def assign_with_dummies(c: Sequence[Sequence[float]], m: int, eps_d: Optional[float] = None) -> Tuple[List[int], float]:
    """Least-cost matching of rows to the m columns of c, with dummies; -1 means a dummy."""
    n = len(c)
    full = pad_with_dummies(c, m, eps_d)  # @line L7
    assign = hungarian(full)  # @line L8
    total = sum(full[i][assign[i]] for i in range(len(full)))
    out = [assign[i] if assign[i] < m else -1 for i in range(n)]
    return out, total  # @line L9
