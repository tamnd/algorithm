# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamilton-jacobi-reachability/. The authors are listed in prov/CFEBTN.jsonl.

"""Backward reachable tubes by a Lax-Friedrichs scheme on a grid.

The system is x' = f(x, u, d). The control u wants to reach the target set
{x : g(x) <= 0} and the disturbance d tries to prevent this. The value
V(x, tau) solves, in time to go tau >= 0,

    dV/dtau = min(0, H(x, grad V)),   V(x, 0) = g(x),
    H(x, p) = min over u of max over d of p . f(x, u, d).

The backward reachable tube of horizon T is {x : V(x, T) <= 0} (Mitchell,
Bayen and Tomlin 2005). With G = -H the equation reads
dV/dtau = -max(0, G(x, grad V)), and the scheme is

    V_new = V - dtau * max(0, G(x, pbar) - sum_i alpha_i (p+_i - p-_i) / 2),

with pbar = (p+ + p-) / 2 and one-sided differences p- and p+. It is
monotone if alpha_i >= max |dG/dp_i| on the grid and
dtau * sum_i alpha_i / dx_i <= 1.

A grid is a list of (lo, hi, k) per axis: k equally spaced nodes from lo to
hi. V is a flat list in row-major order (the last axis runs fastest). At
the edge of the grid the missing neighbor is filled by linear extrapolation,
so the one-sided difference there equals the inner one.

Cost: K = ceil(T sum_i alpha_i / dx_i) time steps, each O(n) work per
node, so O(K n M) for M = k_1 ... k_n nodes. M grows like k^n: this is the
curse of dimensionality of the method.
"""

import math

__all__ = ["grid_points", "hj_reach", "zero_crossings_1d"]


def grid_points(grid):
    """Return (points, strides, steps): the nodes in row-major order."""
    axes = [[lo + (hi - lo) * j / (k - 1) for j in range(k)] for lo, hi, k in grid]
    steps = [(hi - lo) / (k - 1) for lo, hi, k in grid]
    sizes = [k for _, _, k in grid]
    strides = [1] * len(grid)
    for i in range(len(grid) - 2, -1, -1):
        strides[i] = strides[i + 1] * sizes[i + 1]
    points = [[]]
    for ax in axes:
        points = [p + [v] for p in points for v in ax]
    return points, strides, steps


def hj_reach(grid, g, G, alpha, T, cfl=1.0):
    """Return (points, V, K): V(x, T) on the grid and the number K of time steps.

    g(x) is the target function, G(x, p) = -H(x, p), alpha a list with
    alpha_i >= max |dG/dp_i| on the grid, T >= 0 the horizon. cfl <= 1.
    """
    if not 0 < cfl <= 1:
        raise ValueError("hj_reach: cfl must be in (0, 1]")
    points, strides, steps = grid_points(grid)
    sizes = [k for _, _, k in grid]
    if min(sizes) < 2:
        raise ValueError("hj_reach: each axis needs at least 2 nodes")
    n = len(grid)
    v = [float(g(x)) for x in points]  # @line L1
    rate = sum(a / h for a, h in zip(alpha, steps))
    big_k = 0 if T == 0 else max(1, math.ceil(T * rate / cfl - 1e-12))  # @line L2
    dtau = T / big_k if big_k else 0.0
    m = len(points)
    index = [[(j // strides[i]) % sizes[i] for i in range(n)] for j in range(m)]
    for _ in range(big_k):  # @line L3
        gh = [0.0] * m
        for j in range(m):  # @line L4
            pm = [0.0] * n
            pp = [0.0] * n
            for i in range(n):
                s, h, pos, k = strides[i], steps[i], index[j][i], sizes[i]
                if pos == 0:
                    pp[i] = (v[j + s] - v[j]) / h
                    pm[i] = pp[i]
                elif pos == k - 1:
                    pm[i] = (v[j] - v[j - s]) / h
                    pp[i] = pm[i]
                else:
                    pm[i] = (v[j] - v[j - s]) / h  # @line L5
                    pp[i] = (v[j + s] - v[j]) / h
            pbar = [(a + b) / 2 for a, b in zip(pm, pp)]
            gh[j] = G(points[j], pbar) - sum(alpha[i] * (pp[i] - pm[i]) / 2 for i in range(n))  # @line L6
        v = [vj - dtau * max(0.0, gj) for vj, gj in zip(v, gh)]  # @line L7
    return points, v, big_k  # @line L8


def zero_crossings_1d(xs, v):
    """Return the points where the piecewise linear interpolant of v changes sign."""
    out = []
    for a, b, va, vb in zip(xs, xs[1:], v, v[1:]):
        if (va <= 0) != (vb <= 0):
            out.append(a + (b - a) * va / (va - vb))
    return out
