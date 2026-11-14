# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lattice-evaluation-intersection/. The authors are listed in prov/WD4243.jsonl.

"""Lattice evaluation for the intersection of a Bezier patch and an implicit surface.

The patch r(u, v) on [0, 1] x [0, 1] is given by its control net. The second
surface is the zero set of a polynomial f(x, y, z), given as a dictionary that
maps an exponent triple (a, b, c) to the coefficient of x^a y^b z^c. The
method intersects the N + 1 parameter lines u = i/N and the N + 1 parameter
lines v = j/N with the surface: on each line, g = f(r) is one polynomial in
one unknown, and its real roots are the lattice points. In each cell of the
lattice the points on the boundary are linked in pairs, and the links are
chained into polylines in the parameter plane.
"""

from math import comb
from typing import Sequence

from si1geom import Vec, bernstein, lincomb, padd, patch_point, pmul, ppow, pscale, real_roots

Poly3 = dict  # (a, b, c) -> coefficient of x^a y^b z^c

SNAP = 1e-9  # a root this close to a lattice value is put on it


def eval_f(f: Poly3, q: Vec) -> float:
    return sum(c * q[0] ** a * q[1] ** b * q[2] ** e for (a, b, e), c in f.items())


def _bezier_power(Q: Sequence[Vec]) -> list:
    """Coordinate polynomials (power basis, in t) of the Bezier curve Q."""
    d = len(Q) - 1
    out = []
    for k in range(3):
        poly = [0.0]
        for i, q in enumerate(Q):
            b = pscale(comb(d, i) * q[k], pmul(ppow([0.0, 1.0], i), ppow([1.0, -1.0], d - i)))
            poly = padd(poly, b)
        out.append(poly)
    return out


def iso_polynomial(P: Sequence[Sequence[Vec]], f: Poly3, along_v: bool, value: float) -> list:
    """g(t) = f(r(value, t)) if along_v, else f(r(t, value)), in the power basis."""
    m, n = len(P) - 1, len(P[0]) - 1
    if along_v:
        B = bernstein(m, value)
        Q = [lincomb(B, [P[a][j] for a in range(m + 1)]) for j in range(n + 1)]
    else:
        B = bernstein(n, value)
        Q = [lincomb(B, P[i]) for i in range(m + 1)]
    X, Y, Z = _bezier_power(Q)
    g = [0.0]
    for (a, b, e), c in f.items():
        g = padd(g, pscale(c, pmul(pmul(ppow(X, a), ppow(Y, b)), ppow(Z, e))))
    return g


def _snap(t: float, N: int) -> float:
    k = round(t * N)
    return k / N if abs(t - k / N) <= SNAP else t


def _key(u: float, v: float) -> tuple:
    return (round(u * 1e9), round(v * 1e9))


def lattice_evaluation_intersection(P: Sequence[Sequence[Vec]], f: Poly3, N: int) -> tuple:
    """Return (polylines, unresolved, points).

    polylines: lists of (u, v); a closed one repeats its first point at the end.
    unresolved: the cells (i, j) whose boundary holds a number of points other
    than 0, 2 or 4.
    points: all lattice points (u, v), sorted.
    """
    pts = {}
    on_u = [[] for _ in range(N + 1)]  # on_u[i]: the v of the points on u = i/N
    on_v = [[] for _ in range(N + 1)]  # on_v[j]: the u of the points on v = j/N
    for i in range(N + 1):  # @line L1
        ui = i / N
        for t in real_roots(iso_polynomial(P, f, True, ui), 0.0, 1.0):
            v = _snap(t, N)
            on_u[i].append(v)
            pts[_key(ui, v)] = (ui, v)
    for j in range(N + 1):  # @line L2
        vj = j / N
        for t in real_roots(iso_polynomial(P, f, False, vj), 0.0, 1.0):
            u = _snap(t, N)
            on_v[j].append(u)
            pts[_key(u, vj)] = (u, vj)

    def g(u: float, v: float) -> float:
        return eval_f(f, patch_point(P, u, v))

    def at_s(i: int, j: int, s: float) -> tuple:
        """The point at boundary coordinate s in [0, 4) of cell (i, j), counterclockwise."""
        u0, v0, h = i / N, j / N, 1 / N
        side, x = int(s), s - int(s)
        return [(u0 + x * h, v0), (u0 + h, v0 + x * h), (u0 + h - x * h, v0 + h), (u0, v0 + h - x * h)][side]

    links = []
    unresolved = []
    for i in range(N):  # @line L3
        for j in range(N):
            u0, u1, v0, v1 = i / N, (i + 1) / N, j / N, (j + 1) / N
            found = {}  # @line L4
            for u in on_v[j]:
                if u0 <= u <= u1:
                    found.setdefault(_key(u, v0), (u - u0) * N)
            for v in on_u[i + 1]:
                if v0 <= v <= v1:
                    found.setdefault(_key(u1, v), 1 + (v - v0) * N)
            for u in on_v[j + 1]:
                if u0 <= u <= u1:
                    found.setdefault(_key(u, v1), 2 + (u1 - u) * N)
            for v in on_u[i]:
                if v0 <= v <= v1:
                    found.setdefault(_key(u0, v), 3 + (v1 - v) * N)
            ring = sorted(found.items(), key=lambda kv: kv[1])
            k = len(ring)
            if k == 2:  # @line L5
                links.append((ring[0][0], ring[1][0]))
            elif k == 4:  # @line L6
                s01 = 0.5 * (ring[0][1] + ring[1][1])
                arc = g(*at_s(i, j, s01))
                centre = g(0.5 * (u0 + u1), 0.5 * (v0 + v1))
                if centre * arc > 0:
                    links += [(ring[1][0], ring[2][0]), (ring[3][0], ring[0][0])]
                else:
                    links += [(ring[0][0], ring[1][0]), (ring[2][0], ring[3][0])]
            elif k > 0:  # @line L7
                unresolved.append((i, j))

    adj = {}  # @line L8
    for e, (a, b) in enumerate(links):
        adj.setdefault(a, []).append((b, e))
        adj.setdefault(b, []).append((a, e))
    used = [False] * len(links)
    polylines = []
    starts = [a for a in adj if len(adj[a]) % 2 == 1] + list(adj)
    for s in starts:
        while any(not used[e] for _, e in adj[s]):
            line = [s]
            cur = s
            while True:
                nxt = next(((b, e) for b, e in adj[cur] if not used[e]), None)
                if nxt is None:
                    break
                used[nxt[1]] = True
                cur = nxt[0]
                line.append(cur)
            polylines.append([pts[k] for k in line])
    return polylines, unresolved, sorted(pts.values())  # @line L9
