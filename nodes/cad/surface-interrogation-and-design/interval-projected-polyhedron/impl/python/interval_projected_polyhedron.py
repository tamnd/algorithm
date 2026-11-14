# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-projected-polyhedron/. The authors are listed in prov/V244NY.jsonl.

"""The interval projected polyhedron solver for polynomial systems in a box.

A polynomial in n variables is a dict that maps an exponent tuple to a
rational coefficient. The box is a list of n pairs (a_j, b_j). The solver
writes every equation in the tensor product Bernstein basis of the box, with
each coefficient held as a float interval that contains the exact value. For
each axis j it projects the control points (i_j / d_j, b_I) of each equation
onto the plane of u_j and f, and keeps the part of the axis f = 0 inside the
convex hull of the projection. The box shrinks to the product of these parts,
or is split in two when it does not shrink enough, until its sides are shorter
than eps.

Boxes are kept with exact rational ends, so that the interval coefficients
always belong to the box they are stored with. All float operations on the
coefficients round outward by one unit in the last place.
"""

from fractions import Fraction
from math import comb, inf, nextafter, prod


# ---- outward rounded interval arithmetic -----------------------------------

def down(x):
    return nextafter(x, -inf)


def up(x):
    return nextafter(x, inf)


def enclose(q):
    """The smallest float interval that contains the rational number q."""
    f = float(q)
    F = Fraction(f)
    if F == q:
        return (f, f)
    if F < q:
        return (f, up(f))
    return (down(f), f)


def i_add(a, b):
    return (down(a[0] + b[0]), up(a[1] + b[1]))


def i_mul(a, b):
    p = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return (down(min(p)), up(max(p)))


# ---- tensors of Bernstein coefficients, stored flat in row major order -----

def strides(shape):
    out = [1] * len(shape)
    for j in range(len(shape) - 2, -1, -1):
        out[j] = out[j + 1] * shape[j + 1]
    return out


def fibers(shape, axis):
    """The lists of flat indices of the lines of the tensor along an axis."""
    st = strides(shape)
    out = []
    for base in range(prod(shape)):
        if (base // st[axis]) % shape[axis] == 0:
            out.append([base + i * st[axis] for i in range(shape[axis])])
    return out


def bernstein_tensor(poly, box):
    """Exact Bernstein coefficients of poly on the box, as (shape, flat list)."""
    n = len(box)
    degs = [max((e[j] for e in poly), default=0) for j in range(n)]
    shape = tuple(d + 1 for d in degs)
    st = strides(shape)
    flat = [Fraction(0)] * prod(shape)
    for e, c in poly.items():
        flat[sum(e[j] * st[j] for j in range(n))] += Fraction(c)
    for j in range(n):
        a, b = Fraction(box[j][0]), Fraction(box[j][1])
        h, d = b - a, degs[j]
        for fib in fibers(shape, j):
            c = [flat[k] for k in fib]
            # c(a + h u) in powers of u, then u^k = sum_i C(i, k) / C(d, k) B_i(u)
            cs = [sum(c[m] * comb(m, k) * a ** (m - k) for m in range(k, d + 1)) * h ** k for k in range(d + 1)]
            bs = [sum(Fraction(comb(i, k), comb(d, k)) * cs[k] for k in range(i + 1)) for i in range(d + 1)]
            for i, k in enumerate(fib):
                flat[k] = bs[i]
    return shape, flat


def split(coefs, shape, axis, t):
    """De Casteljau subdivision at the float t in [0, 1] along an axis, in
    interval arithmetic: the coefficients on [0, t] and on [t, 1]."""
    T = (t, t)
    S = enclose(1 - Fraction(t))
    left, right = list(coefs), list(coefs)
    for fib in fibers(shape, axis):
        row = [coefs[k] for k in fib]
        L, R = [row[0]], [row[-1]]
        while len(row) > 1:
            row = [i_add(i_mul(S, row[i]), i_mul(T, row[i + 1])) for i in range(len(row) - 1)]
            L.append(row[0])
            R.append(row[-1])
        R.reverse()
        for i, k in enumerate(fib):
            left[k], right[k] = L[i], R[i]
    return left, right


# ---- the projection step ---------------------------------------------------

def hull_axis_interval(points):
    """The interval of t with (t, 0) in the convex hull of the points (t, f),
    exactly, from the zero points and the crossings of the segments between a
    point with f > 0 and a point with f < 0. None when it is empty."""
    cands = [t for t, f in points if f == 0]
    pos = [p for p in points if p[1] > 0]
    neg = [p for p in points if p[1] < 0]
    cands += [(fp * tq - fq * tp) / (fp - fq) for tp, fp in pos for tq, fq in neg]
    if not cands:
        return None
    return min(cands), max(cands)


def project(coefs, shape, axis):
    """The local interval [s, t] of u_axis outside of which this equation has
    no zero in the box, rounded outward to floats, or None."""
    d = shape[axis] - 1
    st = strides(shape)[axis]
    lo = [inf] * (d + 1)
    hi = [-inf] * (d + 1)
    for k, (a, b) in enumerate(coefs):
        i = (k // st) % (d + 1)
        lo[i] = min(lo[i], a)
        hi[i] = max(hi[i], b)
    if d == 0:  # the equation does not depend on this variable
        return (0.0, 1.0) if lo[0] <= 0 <= hi[0] else None
    pts = []
    for i in range(d + 1):
        pts.append((Fraction(i, d), Fraction(lo[i])))
        pts.append((Fraction(i, d), Fraction(hi[i])))
    r = hull_axis_interval(pts)
    if r is None:
        return None
    return max(0.0, enclose(r[0])[0]), min(1.0, enclose(r[1])[1])


def restrict(X, Bs, shapes, lo, hi):
    """The box and the coefficients over the local box prod [lo_j, hi_j], or
    over a slightly larger box with float split parameters."""
    X = list(X)
    for j in range(len(X)):
        s, t = lo[j], hi[j]
        a, b = X[j]
        h = b - a
        start, end = Fraction(0), Fraction(1)
        if t < 1:
            Bs = [split(B, sh, j, t)[0] for B, sh in zip(Bs, shapes)]
            end = Fraction(t)
        if s > 0 and t > 0:
            r = enclose(Fraction(s) / end)[0]  # r * end <= s
            if r > 0:
                Bs = [split(B, sh, j, r)[1] for B, sh in zip(Bs, shapes)]
                start = Fraction(r) * end
        X[j] = (a + h * start, a + h * end)
    return X, Bs


def merge(boxes, gap):
    """Group boxes whose distance in the max norm is at most gap, and return
    the bounding box of each group as float intervals rounded outward."""
    parent = list(range(len(boxes)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i in range(len(boxes)):
        for k in range(i):
            if all(boxes[i][j][0] <= boxes[k][j][1] + gap and boxes[k][j][0] <= boxes[i][j][1] + gap for j in range(len(boxes[i]))):
                parent[find(i)] = find(k)
    groups = {}
    for i, X in enumerate(boxes):
        groups.setdefault(find(i), []).append(X)
    out = []
    for g in groups.values():
        n = len(g[0])
        out.append(tuple((enclose(min(X[j][0] for X in g))[0], enclose(max(X[j][1] for X in g))[1]) for j in range(n)))
    return sorted(out)


def ipp(polys, box, eps=1e-9, max_steps=100000):
    """All roots of the system polys = 0 in the box, as a sorted list of small
    boxes, each the bounding box of a group of boxes at most eps apart. Every
    root in the box lies in one of them. Also returns the raw boxes, with
    exact rational ends; each passed the projection test and has all sides
    shorter than eps."""
    n = len(box)
    X0 = [(Fraction(a), Fraction(b)) for a, b in box]
    shapes, B0 = [], []
    for p in polys:
        shape, flat = bernstein_tensor(p, X0)  # @line L1
        shapes.append(shape)
        B0.append([enclose(x) for x in flat])
    stack, out = [(X0, B0)], []  # @line L2
    steps = 0
    while stack:  # @line L3
        steps += 1
        if steps > max_steps:
            raise RuntimeError("too many steps")
        X, Bs = stack.pop()
        widths = [b - a for a, b in X]
        jstar = max(range(n), key=lambda j: widths[j])
        lo, hi = [0.0] * n, [1.0] * n
        empty = False
        for j in range(n):  # @line L4
            for B, sh in zip(Bs, shapes):
                r = project(B, sh, j)
                if r is None:
                    empty = True
                    break
                lo[j], hi[j] = max(lo[j], r[0]), min(hi[j], r[1])
            if empty or lo[j] > hi[j]:
                empty = True
                break
        if empty:  # @line L5
            continue
        if max(widths) < eps:  # @line L6
            out.append(X)
            continue
        X, Bs = restrict(X, Bs, shapes, lo, hi)  # @line L7
        if X[jstar][1] - X[jstar][0] > widths[jstar] / 2:  # @line L8
            a, b = X[jstar]
            m = (a + b) / 2
            halves = [split(B, sh, jstar, 0.5) for B, sh in zip(Bs, shapes)]
            for side, (lo_, hi_) in ((0, (a, m)), (1, (m, b))):
                Y = list(X)
                Y[jstar] = (lo_, hi_)
                stack.append((Y, [hv[side] for hv in halves]))
        else:
            stack.append((X, Bs))  # @line L9
    return merge(out, Fraction(eps)), out  # @line L10
