# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fincke-pohst-enumeration/. The authors are listed in prov/0T8BFG.jsonl.

from fractions import Fraction
from math import floor, isqrt
from typing import Optional, Sequence, Union

Number = Union[int, Fraction]


def _dot(u: Sequence[Fraction], v: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(u, v)), Fraction(0))


def _first_in_interval(c: Fraction, q: Fraction) -> Optional[int]:
    """The smallest integer x with (x - c)^2 <= q, or None if there is none (q >= 0)."""
    a = floor(c) - isqrt(floor(q)) - 1  # a <= c - sqrt(q)
    while (a - c) ** 2 > q and a <= c:
        a += 1
    return a if (a - c) ** 2 <= q else None


def fincke_pohst(
    basis: Sequence[Sequence[Number]],
    radius_sq: Number,
    target: Optional[Sequence[Number]] = None,
    nodes: Optional[list[int]] = None,
) -> list[list[int]]:
    """Fincke-Pohst enumeration of all lattice vectors in a ball.

    Input: n >= 1 linearly independent rows b_1..b_n of length m (int or Fraction,
    exact arithmetic), a squared radius R >= 0 and a target t (default 0).
    Output: every x in Z^n with ||t - (x_1 b_1 + ... + x_n b_n)||^2 <= R, in
    lexicographic order of (x_n, ..., x_1). If nodes is a list, nodes[0] is
    increased once per node of the search tree (one per accepted partial vector).
    Cost: O(n^2 m) arithmetic operations for Gram-Schmidt, plus O(n) per tree node;
    the number of nodes is at most sum_k prod_{i >= k} (2 sqrt(R) / ||b_i*|| + 1).
    Iterative, no recursion. Raises ValueError for dependent rows or bad lengths.
    """
    b = [[Fraction(c) for c in row] for row in basis]
    n = len(b)
    if n == 0:
        raise ValueError("need at least one basis row")
    m = len(b[0])
    t = [Fraction(0)] * m if target is None else [Fraction(c) for c in target]
    if any(len(row) != m for row in b) or len(t) != m:
        raise ValueError("all rows and the target must have the same length")
    r = Fraction(radius_sq)
    stars: list[list[Fraction]] = []
    norms: list[Fraction] = []
    mu = [[Fraction(0)] * n for _ in range(n)]
    for i, row in enumerate(b):  # @line L1
        w = row[:]
        for j in range(i):
            mu[i][j] = _dot(row, stars[j]) / norms[j]
            w = [a - mu[i][j] * c for a, c in zip(w, stars[j])]
        nw = _dot(w, w)
        if nw == 0:
            raise ValueError("the basis vectors are linearly dependent")
        stars.append(w)
        norms.append(nw)
    tau = [_dot(t, stars[j]) / norms[j] for j in range(n)]
    rho = [Fraction(0)] * (n + 1)
    rho[n] = _dot(t, t) - sum((tau[j] ** 2 * norms[j] for j in range(n)), Fraction(0))
    out: list[list[int]] = []
    if rho[n] > r:  # @line L2
        return out
    x = [0] * n
    c = [Fraction(0)] * n
    i, new = n - 1, True  # @line L3
    while i < n:  # @line L4
        if new:  # @line L5
            c[i] = tau[i] - sum((x[j] * mu[j][i] for j in range(i + 1, n)), Fraction(0))
            first = _first_in_interval(c[i], (r - rho[i + 1]) / norms[i])
            ok = first is not None
            if ok:
                x[i] = first
        else:
            x[i] += 1  # @line L6
            ok = True
        if not ok or rho[i + 1] + (x[i] - c[i]) ** 2 * norms[i] > r:  # @line L7
            i, new = i + 1, False
            continue
        rho[i] = rho[i + 1] + (x[i] - c[i]) ** 2 * norms[i]  # @line L8
        if nodes is not None:
            nodes[0] += 1
        if i == 0:  # @line L9
            out.append(x[:])
            new = False
        else:
            i, new = i - 1, True  # @line L10
    return out  # @line L11
