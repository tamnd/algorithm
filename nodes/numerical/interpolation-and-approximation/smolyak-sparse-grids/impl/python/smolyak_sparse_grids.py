# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smolyak-sparse-grids/. The authors are listed in prov/Y27RRZ.jsonl.

"""Smolyak sparse grid polynomial interpolation on [-1, 1]^d.

A(L, d) f = sum over multi-indices i >= 1 with max(d, L + 1) <= |i| <= d + L of
    (-1)^(d + L - |i|) * C(d - 1, d + L - |i|) * (U^(i_1) x ... x U^(i_d)) f,

where U^i is 1D Lagrange interpolation on m(i) nested nodes, m(1) = 1 and
m(i) = 2^(i-1) + 1. Node families: "chebyshev" (Clenshaw-Curtis points
-cos(pi k), floats) and "equispaced" (2k - 1, exact with Fraction).
A node is identified by its exact position k = j / (m - 1) in [0, 1].
"""

import math
from fractions import Fraction


def _positions(i):
    m = 1 if i == 1 else 2 ** (i - 1) + 1
    if m == 1:
        return [Fraction(1, 2)]
    return [Fraction(j, m - 1) for j in range(m)]


def _coord(k, family):
    if family == "chebyshev":
        if k == Fraction(1, 2):
            return 0.0
        return -math.cos(math.pi * k)
    if family == "equispaced":
        return 2 * k - 1
    raise ValueError("unknown node family")


def _indices(d, lo, hi):
    """Multi-indices i in N^d, i_j >= 1, with lo <= |i| <= hi."""
    out = []
    cur = [1] * d
    def rec(j, used):
        if j == d:
            if used >= lo:
                out.append(tuple(cur))
            return
        rest = d - j - 1
        for v in range(1, hi - used - rest + 1):
            cur[j] = v
            rec(j + 1, used + v)
    rec(0, 0)
    return out


def smolyak_fit(f, d, level, family="chebyshev"):
    """Sample f on the sparse grid; return a model for smolyak_eval."""
    if d < 1 or level < 0:
        raise ValueError("need d >= 1 and level >= 0")
    q = d + level
    terms = []
    values = {}
    for i in _indices(d, max(d, level + 1), q):                   # @line L1
        c = (-1) ** (q - sum(i)) * math.comb(d - 1, q - sum(i))   # @line L2
        grids = [_positions(ij) for ij in i]
        terms.append((c, i))
        def walk(j, key):
            if j == d:
                if key not in values:
                    values[key] = f(*[_coord(k, family) for k in key])  # @line L3
                return
            for k in grids[j]:
                walk(j + 1, key + (k,))
        walk(0, ())
    return (d, family, terms, values)


def _lagrange_weights(nodes, t):
    w = []
    for a, xa in enumerate(nodes):
        p = 1
        for b, xb in enumerate(nodes):
            if b != a:
                p = p * (t - xb) / (xa - xb)
        w.append(p)
    return w


def smolyak_eval(model, t):
    """Evaluate the sparse grid interpolant at the point t (a sequence)."""
    d, family, terms, values = model
    if len(t) != d:
        raise ValueError("point has wrong dimension")
    cache = {}
    s = 0
    for c, i in terms:
        ws = []
        for j, ij in enumerate(i):
            if (j, ij) not in cache:
                pos = _positions(ij)
                cache[(j, ij)] = (pos, _lagrange_weights(
                    [_coord(k, family) for k in pos], t[j]))
            ws.append(cache[(j, ij)])
        part = 0
        def walk(j, key, w):
            nonlocal part
            if j == d:
                part = part + w * values[key]
                return
            for k, wk in zip(*ws[j]):
                walk(j + 1, key + (k,), w * wk)
        walk(0, (), 1)
        s = s + c * part                                          # @line L4
    return s                                                      # @line L5


def sparse_grid_points(model):
    """The distinct sample points, as coordinate tuples."""
    d, family, _, values = model
    return [tuple(_coord(k, family) for k in key) for key in values]
