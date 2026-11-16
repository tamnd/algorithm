# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elastic-bands/. The authors are listed in prov/32ZJAX.jsonl.
"""Elastic bands with bubbles (Quinlan and Khatib) for a point robot in the plane.

The band is a list of bubble centers b_0, ..., b_m from the start to the
goal. The bubble at b is the open disc of radius rho(b), the distance from b
to the nearest obstacle, so every bubble is free of obstacles. The band is
valid when consecutive bubbles overlap:

    |b_(i+1) - b_i| < rho(b_i) + rho(b_(i+1))   for every i.

Then the polyline through the centers lies inside the union of the bubbles
and is free of collision. Every operation below keeps a valid band valid:
a bubble moves only if the new bubble still overlaps both neighbors, a new
bubble is inserted at the midpoint of two overlapping bubbles (which always
works), and a bubble is deleted only if its two neighbors overlap.

Each interior bubble feels a contraction force, the sum of the unit vectors
toward its two neighbors, and a repulsion force k_r (rho_0 - rho) grad rho
when rho < rho_0. The component along the band is removed, and the bubble
moves by alpha * rho * f, so big bubbles in open space move far and small
bubbles near obstacles move little.
"""

import math


def disc_world(discs):
    """rho(p) = distance to the nearest disc, and its gradient."""
    def rho(p):
        best, grad = math.inf, (0.0, 0.0)
        for ox, oy, r in discs:
            dx, dy = p[0] - ox, p[1] - oy
            dist = math.hypot(dx, dy)
            d = dist - r
            if d < best:
                best = d
                grad = (dx / dist, dy / dist) if dist > 0.0 else (0.0, 0.0)
        return best, grad
    return rho


def overlap(a, b, ra, rb):
    return math.hypot(b[0] - a[0], b[1] - a[1]) < ra + rb


def is_valid(band, rho):
    rs = [rho(b)[0] for b in band]
    if min(rs) <= 0.0:
        return False
    return all(overlap(band[i], band[i + 1], rs[i], rs[i + 1]) for i in range(len(band) - 1))


def segment_clearance(band, rho, per=20):
    """Smallest distance to the obstacles along the polyline, sampled."""
    best = math.inf
    for i in range(len(band) - 1):
        for j in range(per + 1):
            a = j / per
            p = (band[i][0] * (1 - a) + band[i + 1][0] * a, band[i][1] * (1 - a) + band[i + 1][1] * a)
            best = min(best, rho(p)[0])
    return best


def length(band):
    return sum(math.hypot(band[i + 1][0] - band[i][0], band[i + 1][1] - band[i][1]) for i in range(len(band) - 1))


def force(band, i, rho, k_c, k_r, rho0):
    b, prev, nxt = band[i], band[i - 1], band[i + 1]
    f = [0.0, 0.0]
    for q in (prev, nxt):
        dx, dy = q[0] - b[0], q[1] - b[1]
        d = math.hypot(dx, dy)
        if d > 0.0:
            f[0] += k_c * dx / d
            f[1] += k_c * dy / d
    r, g = rho(b)
    if r < rho0:
        f[0] += k_r * (rho0 - r) * g[0]
        f[1] += k_r * (rho0 - r) * g[1]
    tx, ty = nxt[0] - prev[0], nxt[1] - prev[1]
    tn = math.hypot(tx, ty)
    if tn > 0.0:
        tx, ty = tx / tn, ty / tn
        dot = f[0] * tx + f[1] * ty
        f[0] -= dot * tx
        f[1] -= dot * ty
    return f


def update(band, rho, k_c=1.0, k_r=4.0, rho0=0.3, alpha=0.3, rho_min=1e-3, ins=0.9, dele=0.5, tries=4):
    """One sweep over the band: moves, then insertions, then deletions. Returns a new band."""
    band = [tuple(b) for b in band]
    for i in range(1, len(band) - 1):  # @line L2
        r = rho(band[i])[0]  # @line L3
        f = force(band, i, rho, k_c, k_r, rho0)  # @line L4
        step = alpha * min(r, 1.0)
        for _ in range(tries):
            cand = (band[i][0] + step * f[0], band[i][1] + step * f[1])  # @line L5
            rc = rho(cand)[0]
            if (rc >= rho_min and overlap(cand, band[i - 1], rc, rho(band[i - 1])[0])
                    and overlap(cand, band[i + 1], rc, rho(band[i + 1])[0])):  # @line L6
                band[i] = cand
                break
            step *= 0.5
    out = [band[0]]
    for i in range(1, len(band)):  # @line L7
        a, b = out[-1], band[i]
        ra, rb = rho(a)[0], rho(b)[0]
        if math.hypot(b[0] - a[0], b[1] - a[1]) > ins * (ra + rb):
            out.append(((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0))
        out.append(b)
    band = out
    i = 1
    while i < len(band) - 1:  # @line L8
        a, c = band[i - 1], band[i + 1]
        if math.hypot(c[0] - a[0], c[1] - a[1]) < dele * (rho(a)[0] + rho(c)[0]):
            del band[i]
        else:
            i += 1
    return band


def elastic_band(band, rho, sweeps=100, **kw):
    """Run several sweeps against a fixed scene. Returns the band and the lengths."""
    lengths = [length(band)]
    for _ in range(sweeps):  # @line L1
        band = update(band, rho, **kw)
        lengths.append(length(band))
    return band, lengths  # @line L9


def polyline(points, step):
    """Resample a polyline so that consecutive points are at most step apart."""
    out = [tuple(points[0])]
    for a, b in zip(points, points[1:]):
        n = max(1, math.ceil(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        for j in range(1, n + 1):
            out.append((a[0] + (b[0] - a[0]) * j / n, a[1] + (b[1] - a[1]) * j / n))
    return out
