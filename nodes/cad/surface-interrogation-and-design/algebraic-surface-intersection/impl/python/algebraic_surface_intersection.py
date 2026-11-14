# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algebraic-surface-intersection/. The authors are listed in prov/38DDQS.jsonl.

"""Intersection of a Bezier patch with an implicit algebraic surface.

The patch r(u, v) on [0, 1] x [0, 1] is given by its control net, the second
surface by a polynomial f(x, y, z), a dictionary that maps an exponent triple
(a, b, c) to the coefficient of x^a y^b z^c. Substituting r into f gives one
polynomial g(u, v) = f(r(u, v)), whose zero set in the parameter box is the
intersection curve. The code forms g in tensor product Bernstein form with
exact rational arithmetic, subdivides the box until each piece either holds no
zero of g, by the signs of its coefficients, or holds a curve that is a graph
over one parameter, by the signs of the coefficients of a derivative. In such
a piece the boundary points of the curve are paired in order and each arc is
traced by bisection. The arcs are chained into curves. Pieces smaller than
2^-max_depth that are neither are returned as candidates for singular points.
"""

from fractions import Fraction
from math import comb
from typing import Sequence

from si1geom import Vec, bernstein, pmul, ppow, pscale, padd, real_roots

Grid = list  # a (p + 1) x (q + 1) list of lists of Bernstein coefficients


def bern_product(A: Grid, B: Grid) -> Grid:
    """Bernstein coefficients of the product of two tensor product polynomials."""
    p, q, r, s = len(A) - 1, len(A[0]) - 1, len(B) - 1, len(B[0]) - 1
    C = [[Fraction(0)] * (q + s + 1) for _ in range(p + r + 1)]
    for a in range(p + 1):
        for b in range(q + 1):
            x = A[a][b] * comb(p, a) * comb(q, b)
            if x == 0:
                continue
            for c in range(r + 1):
                for d in range(s + 1):
                    if B[c][d] != 0:
                        C[a + c][b + d] += x * B[c][d] * comb(r, c) * comb(s, d)
    return [[C[i][j] / (comb(p + r, i) * comb(q + s, j)) for j in range(q + s + 1)] for i in range(p + r + 1)]


def substitute(P: Sequence[Sequence[Vec]], f: dict) -> Grid:
    """Exact Bernstein coefficients of g = f(r(u, v)), of bidegree (k m, k n)."""
    m, n = len(P) - 1, len(P[0]) - 1
    coords = [[[Fraction(P[i][j][c]) for j in range(n + 1)] for i in range(m + 1)] for c in range(3)]
    ones = [[Fraction(1)] * (n + 1) for _ in range(m + 1)]
    k = max(sum(e) for e in f)
    powers = [{0: [[Fraction(1)]]} for _ in range(3)]

    def power(c: int, e: int) -> Grid:
        if e not in powers[c]:
            powers[c][e] = bern_product(power(c, e - 1), coords[c])
        return powers[c][e]

    G = [[Fraction(0)] * (k * n + 1) for _ in range(k * m + 1)]
    for (a, b, c), coef in f.items():
        T = bern_product(bern_product(power(0, a), power(1, b)), power(2, c))
        for _ in range(k - a - b - c):
            T = bern_product(T, ones)
        cf = Fraction(coef)
        for i in range(k * m + 1):
            for j in range(k * n + 1):
                G[i][j] += cf * T[i][j]
    return G


def _halves(c: list) -> tuple:
    left, right, cur = [c[0]], [c[-1]], list(c)
    while len(cur) > 1:
        cur = [(cur[i] + cur[i + 1]) / 2 for i in range(len(cur) - 1)]
        left.append(cur[0])
        right.append(cur[-1])
    return left, right[::-1]


def _split(G: Grid) -> list:
    """The four quarters of G, in the order (low u, low v), (low u, high v), (high u, low v), (high u, high v)."""
    M, N = len(G) - 1, len(G[0]) - 1
    lo = [[None] * (N + 1) for _ in range(M + 1)]
    hi = [[None] * (N + 1) for _ in range(M + 1)]
    for j in range(N + 1):
        a, b = _halves([G[i][j] for i in range(M + 1)])
        for i in range(M + 1):
            lo[i][j], hi[i][j] = a[i], b[i]
    out = []
    for H in (lo, hi):
        rows = [_halves(H[i]) for i in range(M + 1)]
        out.append([rows[i][0] for i in range(M + 1)])
        out.append([rows[i][1] for i in range(M + 1)])
    return out


def _strict_sign(vals) -> int:
    vals = list(vals)
    if all(x > 0 for x in vals):
        return 1
    if all(x < 0 for x in vals):
        return -1
    return 0


def _edge_roots(c: list) -> list:
    """Roots in [0, 1] of the univariate Bernstein polynomial with coefficients c."""
    d = len(c) - 1
    poly = [Fraction(0)]
    for i, x in enumerate(c):
        if x != 0:
            poly = padd(poly, pscale(x * comb(d, i), pmul(ppow([0, 1], i), ppow([1, -1], d - i))))
    return real_roots(poly, 0.0, 1.0)


def _eval(Gf: Grid, s: float, t: float) -> float:
    bs, bt = bernstein(len(Gf) - 1, s), bernstein(len(Gf[0]) - 1, t)
    return sum(bs[i] * sum(bt[j] * Gf[i][j] for j in range(len(bt))) for i in range(len(bs)))


def _root_in(Gf: Grid, s: float, along_t: bool) -> float:
    """The root of the monotone function t -> g(s, t) (or s -> g(t, s)) in [0, 1], by bisection."""
    def h(t):
        return _eval(Gf, s, t) if along_t else _eval(Gf, t, s)
    a, b = 0.0, 1.0
    ha = h(a)
    for _ in range(60):
        mid = 0.5 * (a + b)
        hm = h(mid)
        if hm == 0:
            return mid
        if (hm < 0) == (ha < 0):
            a, ha = mid, hm
        else:
            b = mid
    return 0.5 * (a + b)


def _box_arcs(G: Grid, box: tuple, mono_v: bool, samples: int):
    """Arcs of g = 0 in a box where g is strictly monotone in v (mono_v) or in u.

    Returns None when the boundary points cannot be paired (an odd count)."""
    u0, u1, v0, v1 = box
    M, N = len(G) - 1, len(G[0]) - 1
    found = []
    for t in _edge_roots([G[i][0] for i in range(M + 1)]):
        found.append((u0 + t * (u1 - u0), v0))
    for t in _edge_roots([G[i][N] for i in range(M + 1)]):
        found.append((u0 + t * (u1 - u0), v1))
    for t in _edge_roots(G[0]):
        found.append((u0, v0 + t * (v1 - v0)))
    for t in _edge_roots(G[M]):
        found.append((u1, v0 + t * (v1 - v0)))
    pts = []
    for p in found:
        if all(abs(p[0] - q[0]) + abs(p[1] - q[1]) > 1e-10 for q in pts):
            pts.append(p)
    if len(pts) % 2:
        return None
    axis = 0 if mono_v else 1
    pts.sort(key=lambda p: p[axis])
    Gf = [[float(x) for x in row] for row in G]
    arcs = []
    for a, b in zip(pts[0::2], pts[1::2]):
        line = [a]
        for k in range(1, samples + 1):
            if mono_v:
                u = a[0] + (b[0] - a[0]) * k / (samples + 1)
                s = (u - u0) / (u1 - u0)
                line.append((u, v0 + (v1 - v0) * _root_in(Gf, s, True)))
            else:
                v = a[1] + (b[1] - a[1]) * k / (samples + 1)
                t = (v - v0) / (v1 - v0)
                line.append((u0 + (u1 - u0) * _root_in(Gf, t, False), v))
        line.append(b)
        arcs.append(line)
    return arcs


def algebraic_surface_intersection(P: Sequence[Sequence[Vec]], f: dict, max_depth: int = 10,
                                   samples: int = 4, stats: dict = None) -> tuple:
    """Return (curves, singular): polylines of (u, v) on g = 0, a closed one
    repeating its first point at the end, and the boxes (u0, u1, v0, v1) left
    unresolved at depth max_depth."""
    G0 = substitute(P, f)  # @line L1
    stack = [(G0, (0.0, 1.0, 0.0, 1.0), 0)]  # @line L2
    arcs, singular = [], []
    boxes = 0
    while stack:  # @line L3
        G, box, depth = stack.pop()
        boxes += 1
        if _strict_sign(x for row in G for x in row):  # @line L4
            continue
        M, N = len(G) - 1, len(G[0]) - 1
        sv = _strict_sign(G[i][j + 1] - G[i][j] for i in range(M + 1) for j in range(N))  # @line L5
        su = 0 if sv else _strict_sign(G[i + 1][j] - G[i][j] for i in range(M) for j in range(N + 1))
        if sv or su:
            got = _box_arcs(G, box, bool(sv), samples)  # @line L6
            if got is not None:
                arcs += got
                continue
        if depth < max_depth:  # @line L7
            u0, u1, v0, v1 = box
            um, vm = 0.5 * (u0 + u1), 0.5 * (v0 + v1)
            subs = ((u0, um, v0, vm), (u0, um, vm, v1), (um, u1, v0, vm), (um, u1, vm, v1))
            for Q, b in zip(_split(G), subs):
                stack.append((Q, b, depth + 1))
        else:
            singular.append(box)  # @line L8
    if stats is not None:
        stats["boxes"] = boxes

    ends = []  # @line L9

    def node(p) -> int:
        for k, q in enumerate(ends):
            if abs(p[0] - q[0]) + abs(p[1] - q[1]) <= 1e-8:
                return k
        ends.append(p)
        return len(ends) - 1

    adj = {}
    for e, line in enumerate(arcs):
        a, b = node(line[0]), node(line[-1])
        adj.setdefault(a, []).append((e, b, False))
        adj.setdefault(b, []).append((e, a, True))
    used = [False] * len(arcs)
    curves = []
    for s in [a for a in adj if len(adj[a]) % 2] + list(adj):
        while any(not used[e] for e, _, _ in adj[s]):
            cur, curve = s, [ends[s]]
            while True:
                nxt = next(((e, b, rev) for e, b, rev in adj[cur] if not used[e]), None)
                if nxt is None:
                    break
                e, b, rev = nxt
                used[e] = True
                piece = arcs[e][::-1] if rev else arcs[e]
                curve += piece[1:-1] + [ends[b]]
                cur = b
            curves.append(curve)
    return curves, singular  # @line L10
