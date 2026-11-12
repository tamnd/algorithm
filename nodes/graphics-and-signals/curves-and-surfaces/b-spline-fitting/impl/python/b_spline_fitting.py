# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-spline-fitting/. The authors are listed in prov/JDHTCP.jsonl.

"""Least-squares fitting of a B-spline curve with a fixed knot vector.

Data points Q[0..m] in R^d with parameters t[0..m], a degree p and a knot
vector U of n + p + 2 knots. The result is the n + 1 control points P that
minimize sum_k |Q[k] - C(t[k])|^2, where C(t) = sum_i N_{i,p}(t) P[i].
The normal equations (N^T N) P = N^T Q have a band matrix of half bandwidth p,
solved here by a band LDL^T factorization without square roots, so that
Fraction inputs give the exact minimizer.
Cost: O(m p^2 + n p^2 + (m + n) p d) time and O(n p + n d) space.
Precondition: U nondecreasing, t[k] in [U[p], U[n+1]], and N has full column
rank (Schoenberg-Whitney: some increasing sites t[k_0] < ... < t[k_n] have
N_{i,p}(t[k_i]) != 0). Otherwise a zero pivot raises ValueError.
"""

import math
from typing import List, Sequence, Tuple

Point = Tuple


def find_span(U: Sequence, p: int, n: int, t) -> int:
    """The index s with U[s] <= t < U[s+1] and p <= s <= n; t = U[n+1] gives s = n."""
    if t >= U[n + 1]:
        return n
    lo, hi = p, n + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if t < U[mid]:
            hi = mid
        else:
            lo = mid
    return lo


def basis_funs(s: int, t, p: int, U: Sequence) -> list:
    """The p + 1 basis values N_{s-p,p}(t), ..., N_{s,p}(t) (triangular Cox-de Boor scheme)."""
    N = [t - t + 1] + [0] * p
    left = [0] * (p + 1)
    right = [0] * (p + 1)
    for j in range(1, p + 1):
        left[j] = t - U[s + 1 - j]
        right[j] = U[s + j] - t
        saved = 0
        for r in range(j):
            tmp = N[r] / (right[r + 1] + left[j - r])
            N[r] = saved + right[r + 1] * tmp
            saved = left[j - r] * tmp
        N[j] = saved
    return N


def fit(Q: Sequence[Point], t: Sequence, U: Sequence, p: int) -> List[Point]:
    """The control points of the least-squares B-spline fit."""
    n = len(U) - p - 2
    m = len(Q) - 1
    if n < 0 or len(t) != m + 1:
        raise ValueError("need len(U) >= p + 2 and one parameter per data point")
    d = len(Q[0])
    zero = t[0] - t[0]
    # band[i][j] holds A[i][i - j] for j = 0 .. p (the lower half and the diagonal)
    band = [[zero] * (p + 1) for _ in range(n + 1)]  # @line L1
    rhs = [[zero] * d for _ in range(n + 1)]
    for k in range(m + 1):  # @line L2
        s = find_span(U, p, n, t[k])  # @line L3
        B = basis_funs(s, t[k], p, U)
        for a in range(p + 1):  # @line L4
            i = s - p + a
            for b in range(a + 1):
                band[i][a - b] += B[a] * B[b]
        for a in range(p + 1):  # @line L5
            row = rhs[s - p + a]
            for c in range(d):
                row[c] += B[a] * Q[k][c]
    L, D = band_ldl(band, p)  # @line L6
    return band_solve(L, D, rhs, p)  # @line L7


def band_ldl(band, p: int):
    """Factor A = L D L^T for a symmetric positive definite band matrix (lower band storage)."""
    N = len(band)
    L = [[0] * (p + 1) for _ in range(N)]  # L[i][j] = L(i, i - j), unit diagonal
    D = [0] * N
    for i in range(N):
        for j in range(max(0, i - p), i + 1):
            acc = band[i][i - j]
            for k in range(max(0, i - p), j):
                acc -= L[i][i - k] * L[j][j - k] * D[k]
            if j == i:
                if acc <= 0:
                    raise ValueError("normal matrix is singular: the sites violate the Schoenberg-Whitney condition")
                D[i] = acc
                L[i][0] = 1
            else:
                L[i][i - j] = acc / D[j]
    return L, D


def band_solve(L, D, rhs, p: int) -> List[Point]:
    """Solve L D L^T x = rhs (vector right-hand sides)."""
    N = len(D)
    y = [row[:] for row in rhs]
    for i in range(N):
        for k in range(max(0, i - p), i):
            y[i] = [a - L[i][i - k] * b for a, b in zip(y[i], y[k])]
    z = [[a / D[i] for a in y[i]] for i in range(N)]
    for i in range(N - 1, -1, -1):
        for k in range(i + 1, min(N, i + p + 1)):
            z[i] = [a - L[k][k - i] * b for a, b in zip(z[i], z[k])]
    return [tuple(r) for r in z]


def evaluate(P: Sequence[Point], U: Sequence, p: int, t) -> Point:
    """The point C(t) of the B-spline curve."""
    n = len(P) - 1
    s = find_span(U, p, n, t)
    B = basis_funs(s, t, p, U)
    return tuple(sum(B[a] * P[s - p + a][c] for a in range(p + 1)) for c in range(len(P[0])))


def chord_length_parameters(Q: Sequence[Point]) -> List[float]:
    """Parameters in [0, 1] proportional to the cumulative chord length (floats)."""
    acc = [0.0]
    for a, b in zip(Q, Q[1:]):
        acc.append(acc[-1] + math.sqrt(sum((y - x) ** 2 for x, y in zip(a, b))))
    total = acc[-1]
    return [x / total for x in acc]


def averaged_knots(t: Sequence, n: int, p: int) -> list:
    """A clamped knot vector for n + 1 control points, with inner knots spread over the sites.

    Each inner knot is a convex combination of two neighbouring sites, so that every
    knot span holds sites. Precondition: m >= n, sorted sites.
    """
    m = len(t) - 1
    lo, hi = t[0], t[-1]
    U = [lo] * (p + 1)
    ratio = (m + 1) / (n - p + 1)
    for j in range(1, n - p + 1):
        x = j * ratio
        i = int(x)
        a = x - i
        U.append((1 - a) * t[i - 1] + a * t[i])
    return U + [hi] * (p + 1)
