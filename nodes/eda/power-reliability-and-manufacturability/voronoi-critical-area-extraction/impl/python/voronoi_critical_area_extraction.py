# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/voronoi-critical-area-extraction/. The authors are listed in prov/VXSKTK.jsonl.
"""Critical area for shorts of axis-parallel rectangles under square (L-infinity) defects.

The layout is a list of rectangles (x1, y1, x2, y2, net) with x1 < x2 and y1 < y2,
and the window is (X1, Y1, X2, Y2). Coordinates are ints or Fractions; all geometry
is exact. A defect of radius r centred at p is the square p + [-r, r]^2.

build_faces computes the second order L-infinity Voronoi structure of the nets inside
the window by incremental insertion of rectangles. It returns convex faces, and on each
face the distance h1 to the nearest net and the distance h2 to the second nearest net
are affine functions. h2 is the critical radius, so the critical area for shorts is
A(r) = sum over faces of the area where h2 <= r.

An affine function is a tuple (a, b, c) meaning a*x + b*y + c. None stands for +infinity.
"""

import math
from fractions import Fraction


def evaluate(f, p):
    return f[0] * p[0] + f[1] * p[1] + f[2]


def minus(f, g):
    return (f[0] - g[0], f[1] - g[1], f[2] - g[2])


def split(poly, f):
    """Split a convex polygon by the line f = 0.

    Returns (part with f <= 0, part with f >= 0). A part with zero area is None.
    """
    vals = [evaluate(f, p) for p in poly]
    if all(v <= 0 for v in vals):
        return poly, None
    if all(v >= 0 for v in vals):
        return None, poly
    neg, pos = [], []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        vp, vq = vals[i], vals[(i + 1) % n]
        if vp <= 0:
            neg.append(p)
        if vp >= 0:
            pos.append(p)
        if (vp < 0 < vq) or (vq < 0 < vp):
            t = vp / (vp - vq)
            x = (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
            neg.append(x)
            pos.append(x)
    return neg, pos


def area(poly):
    s = 0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(Fraction(s)) / 2


def distance_pieces(rect):
    """The five affine pieces whose maximum is the L-infinity distance to the rectangle."""
    a, c, b, d = (Fraction(v) for v in rect[:4])
    return [(-1, 0, a), (1, 0, -b), (0, -1, c), (0, 1, -d), (0, 0, 0)]


def surely_at_least(pieces, h, poly):
    """True if max(pieces) >= h on all of poly, shown by one piece >= h at every vertex."""
    for g in pieces:
        if all(evaluate(minus(g, h), p) >= 0 for p in poly):
            return True
    return False


def by_piece(poly, pieces):
    """Split poly into convex parts, each with the piece that is the maximum on it."""
    parts = [(poly, pieces[0])]
    for g in pieces[1:]:
        nxt = []
        for q, m in parts:
            low, high = split(q, minus(g, m))
            if low is not None:
                nxt.append((low, m))
            if high is not None:
                nxt.append((high, g))
        parts = nxt
    return parts


def insert(faces, rect):
    net = rect[4]
    pieces = distance_pieces(rect)  # @line L3
    out = []
    for poly, nu, h1, h2 in faces:  # @line L4
        if nu == net and surely_at_least(pieces, h1, poly):  # @line L5
            out.append((poly, nu, h1, h2))
            continue
        if nu != net and h2 is not None and surely_at_least(pieces, h2, poly):
            out.append((poly, nu, h1, h2))
            continue
        for q, g in by_piece(poly, pieces):  # @line L6
            if nu is None:
                out.append((q, net, g, None))  # @line L7
            elif nu == net:
                low, high = split(q, minus(g, h1))  # @line L8
                if low is not None:
                    out.append((low, nu, g, h2))
                if high is not None:
                    out.append((high, nu, h1, h2))
            else:
                low, high = split(q, minus(g, h1))  # @line L9
                if low is not None:
                    out.append((low, net, g, h1))  # @line L10
                if high is not None:
                    if h2 is None:
                        out.append((high, nu, h1, g))
                    else:
                        mid, top = split(high, minus(g, h2))
                        if mid is not None:
                            out.append((mid, nu, h1, g))  # @line L11
                        if top is not None:
                            out.append((top, nu, h1, h2))  # @line L12
    return out


def build_faces(rects, window):
    X1, Y1, X2, Y2 = (Fraction(v) for v in window)
    faces = [([(X1, Y1), (X2, Y1), (X2, Y2), (X1, Y2)], None, None, None)]  # @line L1
    for rect in rects:  # @line L2
        faces = insert(faces, rect)
    return faces


def critical_area(faces, r):
    """Exact critical area for shorts at defect radius r."""
    r = Fraction(r)
    total = Fraction(0)
    for poly, _, _, h2 in faces:
        if h2 is None:
            continue
        low, _ = split(poly, (h2[0], h2[1], h2[2] - r))  # @line L13
        if low is not None:
            total += area(low)
    return total


def survival(t, r0):
    """P(R >= t) for Stapper's radius density r/r0^2 below r0 and r0^2/r^3 above."""
    if t <= r0:
        return 1.0 - t * t / (2.0 * r0 * r0)
    return r0 * r0 / (2.0 * t * t)


def moment(k, lo, hi, r0):
    """Integral of r^k f(r) over [lo, hi] for Stapper's density, with 0 <= lo <= hi."""
    total = 0.0
    a, b = lo, min(hi, r0)
    if a < b:
        total += (b ** (k + 2) - a ** (k + 2)) / ((k + 2) * r0 * r0)
    a, b = max(lo, r0), hi
    if a < b:
        if k == 0:
            total += r0 * r0 * (1.0 / (2 * a * a) - 1.0 / (2 * b * b))
        elif k == 1:
            total += r0 * r0 * (1.0 / a - 1.0 / b)
        else:
            total += r0 * r0 * math.log(b / a)
    return total


def average_critical_area(faces, r0):
    """The integral of A(r) f(r) dr under Stapper's density with peak r0.

    On one face the area where h2 <= r is quadratic in r between consecutive vertex
    values of h2, so each piece is found exactly from three values and integrated
    in closed form.
    """
    r0 = float(r0)
    total = 0.0
    for poly, _, _, h2 in faces:
        if h2 is None:
            continue
        vals = sorted(set(evaluate(h2, p) for p in poly))
        whole = area(poly)
        for lo, hi in zip(vals, vals[1:]):
            mid = (lo + hi) / 2
            ys = []
            for r in (lo, mid, hi):
                low, _ = split(poly, (h2[0], h2[1], h2[2] - r))
                ys.append(area(low) if low is not None else Fraction(0))
            # Quadratic through (lo, y0), (mid, y1), (hi, y2), as c0 + c1 r + c2 r^2.
            h = (hi - lo) / 2
            c2 = (ys[0] - 2 * ys[1] + ys[2]) / (2 * h * h)
            c1 = (ys[2] - ys[0]) / (2 * h) - 2 * c2 * mid
            c0 = ys[1] - c1 * mid - c2 * mid * mid
            flo, fhi = float(lo), float(hi)
            total += float(c0) * moment(0, flo, fhi, r0) + float(c1) * moment(1, flo, fhi, r0) + float(c2) * moment(2, flo, fhi, r0)  # @line L14
        total += float(whole) * survival(float(vals[-1]), r0)
    return total


def voronoi_critical_area(rects, window, r0):
    """Build the faces once; return them, the function r -> A(r) and the average."""
    faces = build_faces(rects, window)
    return faces, (lambda r: critical_area(faces, r)), average_critical_area(faces, r0)  # @line L15


def linf_distance(p, rect):
    x, y = p
    return max(rect[0] - x, x - rect[2], rect[1] - y, y - rect[3], 0)


def critical_radius(p, rects):
    """Distance from p to the second nearest net, computed directly."""
    best = {}
    for rect in rects:
        d = linf_distance(p, rect)
        if rect[4] not in best or d < best[rect[4]]:
            best[rect[4]] = d
    ds = sorted(best.values())
    return ds[1] if len(ds) > 1 else None


def face_of(faces, p):
    """A face whose closed polygon contains p."""
    for face in faces:
        poly = face[0]
        n = len(poly)
        sign = 0
        inside = True
        for i in range(n):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
            cr = (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1)
            if cr != 0:
                s = 1 if cr > 0 else -1
                if sign == 0:
                    sign = s
                elif s != sign:
                    inside = False
                    break
        if inside:
            return face
    return None
