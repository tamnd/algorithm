# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mixed-integer-quadrangulation/. The authors are listed in prov/SKTZEV.jsonl.

"""The rounding step of mixed-integer quadrangulation, on a toy grid.

This is a toy, not MIQ. There is no cross field, no singularity and no seam.
What it keeps is the mixed-integer problem that MIQ solves: a convex
quadratic energy in the parameter values, some of which must be integers,
solved by greedy rounding (Bommes, Zimmer and Kobbelt 2009).

The toy is one coordinate u of a parameterization of a grid of vertices
(i, j). Each edge (a, b) asks for u_b - u_a = t_ab, where the targets t come
from a guiding field (h times the x step, with a small change per edge).
Every vertex of a feature column must lie on one integer iso-line u = k, so
the whole column is one integer variable. Vertex (0, 0) is pinned to 0.

    E(u) = sum over edges (u_b - u_a - t_ab)^2

All arithmetic is exact (Fraction).
"""

import itertools
from fractions import Fraction

from mp3geom import solve


def round_half_up(x):
    return (Fraction(x) + Fraction(1, 2)).__floor__()


def toy_grid(xs, ny, h, features, bend=None):
    """Variables and energy terms of the toy grid.

    xs: the x coordinates of the columns, ny: the number of rows minus 1,
    h: the target number of grid lines per unit length, features: the indices
    of the feature columns, bend: optional {edge: change of target}.
    Returns (number of variables, terms [(a, b, t)], integer variables, pinned {var: value}).
    """
    var = {}
    nxt = 0
    for i in range(len(xs)):
        if i in features:
            for j in range(ny + 1):
                var[(i, j)] = nxt
            nxt += 1
        else:
            for j in range(ny + 1):
                var[(i, j)] = nxt
                nxt += 1
    bend = bend or {}
    terms = []
    for i in range(len(xs)):
        for j in range(ny + 1):
            if i + 1 < len(xs):
                e = ((i, j), (i + 1, j))
                terms.append((var[e[0]], var[e[1]], h * (xs[i + 1] - xs[i]) + bend.get(e, 0)))
            if j + 1 <= ny:
                e = ((i, j), (i, j + 1))
                terms.append((var[e[0]], var[e[1]], bend.get(e, 0)))
    integer = sorted({var[(i, 0)] for i in features})
    pinned = {var[(0, 0)]: 0}
    return nxt, terms, integer, pinned


def energy(terms, x):
    return sum((x[b] - x[a] - t) ** 2 for a, b, t in terms if a != b)


def minimize(n, terms, fixed):
    """The continuous minimizer of the energy with the fixed variables held. Exact."""
    free = [k for k in range(n) if k not in fixed]
    col = {k: c for c, k in enumerate(free)}
    m = len(free)
    a = [[Fraction(0)] * m for _ in range(m)]
    r = [[Fraction(0)] for _ in range(m)]
    for p, q, t in terms:
        if p == q:
            continue
        # gradient of (x_q - x_p - t)^2 / 2: +(x_q - x_p - t) for q, -(...) for p
        for v, s in ((q, 1), (p, -1)):
            if v not in col:
                continue
            for w, s2 in ((q, 1), (p, -1)):
                if w in col:
                    a[col[v]][col[w]] += s * s2
                else:
                    r[col[v]][0] -= s * s2 * fixed[w]
            r[col[v]][0] += s * t
    sol = solve(a, r) if m else []
    x = dict(fixed)
    for k in free:
        x[k] = sol[col[k]][0]
    return [Fraction(x[k]) for k in range(n)]


def greedy_rounding(n, terms, integer, pinned):
    """Bommes, Zimmer and Kobbelt's greedy rounding. Returns (x, order of rounding)."""
    fixed = dict(pinned)
    order = []
    todo = [k for k in integer if k not in fixed]
    x = minimize(n, terms, fixed)  # @line L1
    while todo:  # @line L2
        k = min(todo, key=lambda v: (abs(x[v] - round_half_up(x[v])), v))  # @line L3
        fixed[k] = Fraction(round_half_up(x[k]))  # @line L4
        order.append(k)
        todo.remove(k)
        x = minimize(n, terms, fixed)  # @line L5
    return x, order  # @line L6


def direct_rounding(n, terms, integer, pinned):
    """Round all integer variables of the relaxed solution at once, then re-solve the rest."""
    x = minimize(n, terms, dict(pinned))
    fixed = dict(pinned)
    for k in integer:
        if k not in fixed:
            fixed[k] = Fraction(round_half_up(x[k]))
    return minimize(n, terms, fixed)


def brute_force(n, terms, integer, pinned, radius=2):
    """The best integer assignment in a box of the given radius around the relaxed solution."""
    x = minimize(n, terms, dict(pinned))
    todo = [k for k in integer if k not in pinned]
    best = None
    for combo in itertools.product(*[range(round_half_up(x[k]) - radius, round_half_up(x[k]) + radius + 1) for k in todo]):
        fixed = dict(pinned)
        fixed.update(zip(todo, (Fraction(c) for c in combo)))
        y = minimize(n, terms, fixed)
        e = energy(terms, y)
        if best is None or e < best[0]:
            best = (e, y)
    return best[1]
