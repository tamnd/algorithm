# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-support/. The authors are listed in prov/YRE332.jsonl.

"""Tree supports by greedy merging of support cones, after Vanek, Garcia Galicia and Benes (2014).

The points that need support are sampled on the overhang facets of a mesh and
at its local minimum vertices. Each point can be supported from below by a
strut inside its downward cone of slope k (horizontal distance at most k times
the drop). The method sweeps down: it always merges the two active points whose
cones meet highest, if the merge makes the support shorter, and it ends every
remaining active point with a vertical pillar to the plate z = 0.

This is a simplified version. Struts may pass through the part: the method
does not test the cones against the mesh and never lands a strut on the part.

All decisions are exact. Coordinates are int or Fraction. A merge point is
rounded to a grid of step 1/grid and then lowered so that it lies inside both
cones exactly; square roots are bounded above with math.isqrt.
"""

import heapq
import math
from fractions import Fraction


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def is_overhang(p, q, r, s2):
    """Downward facet tilted less than the critical angle from the horizontal.

    s2 = sin^2 of the self-supporting angle measured from the vertical
    (1/2 for 45 degrees). The facet needs support if n_z < 0 and
    n_z^2 > s2 |n|^2. Facets on the plate (all z = 0) need none.
    """
    if p[2] == 0 and q[2] == 0 and r[2] == 0:
        return False
    n = cross(sub(q, p), sub(r, p))
    nn = n[0] * n[0] + n[1] * n[1] + n[2] * n[2]
    return n[2] < 0 and n[2] * n[2] > s2 * nn


def support_points(vertices, faces, s2, m):
    """Points that need support: a barycentric grid of step 1/m on each overhang
    facet, and every vertex strictly below all its neighbours. Points on the
    plate are left out."""
    pts = set()
    for a, b, c in faces:
        p, q, r = vertices[a], vertices[b], vertices[c]
        if not is_overhang(p, q, r, s2):
            continue
        for i in range(m + 1):
            for j in range(m + 1 - i):
                w = (Fraction(i, m), Fraction(j, m), Fraction(m - i - j, m))
                x = tuple(w[0] * p[t] + w[1] * q[t] + w[2] * r[t] for t in range(3))
                if x[2] > 0:
                    pts.add(x)
    nbrs = {i: set() for i in range(len(vertices))}
    for a, b, c in faces:
        nbrs[a] |= {b, c}
        nbrs[b] |= {a, c}
        nbrs[c] |= {a, b}
    for i, v in enumerate(vertices):
        if v[2] > 0 and nbrs[i] and all(vertices[j][2] > v[2] for j in nbrs[i]):
            pts.add(tuple(Fraction(x) for x in v))
    return sorted(pts)


def sqrt_up(x, prec=1 << 24):
    """A rational upper bound of sqrt(x) for a rational x >= 0, within about 1/prec."""
    x = Fraction(x)
    a, b = x.numerator, x.denominator
    r = math.isqrt(a * b * prec * prec)
    if r * r == a * b * prec * prec:
        return Fraction(r, b * prec)
    return Fraction(r + 1, b * prec)


def shorter(a2, b2, c):
    """Exact test sqrt(a2) + sqrt(b2) < c for rationals a2, b2 >= 0."""
    if c <= 0:
        return False
    d = c * c - a2 - b2
    return d > 0 and 4 * a2 * b2 < d * d


def dist2(a, b):
    d = sub(a, b)
    return d[0] * d[0] + d[1] * d[1] + d[2] * d[2]


def merge(p, q, k, grid):
    """Return (m, saves) for the points p and q with p[2] >= q[2]."""
    dz = p[2] - q[2]
    h2 = (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2  # @line L14
    if h2 <= k * k * dz * dz:  # @line L15
        return q, shorter(dist2(p, q), 0, p[2])
    big_d = math.sqrt(h2)  # only to place m; feasibility is restored exactly below  # @line L16
    s = (float(k * dz) + big_d) / (2 * big_d)
    mx = Fraction(round(float(p[0] + (q[0] - p[0]) * s) * grid), grid)  # @line L17
    my = Fraction(round(float(p[1] + (q[1] - p[1]) * s) * grid), grid)
    hp = sqrt_up((mx - p[0]) ** 2 + (my - p[1]) ** 2)
    hq = sqrt_up((mx - q[0]) ** 2 + (my - q[1]) ** 2)
    mz = min(p[2] - hp / k, q[2] - hq / k)  # @line L18
    m = (mx, my, mz)
    saves = mz > 0 and shorter(dist2(p, m), dist2(q, m), p[2] + q[2] - mz)  # @line L19
    return m, saves  # @line L20


def tree_support(points, k=1, grid=1 << 10):
    """Return (nodes, struts). struts are (upper, lower) index pairs into nodes.

    nodes starts with the given points. Every point is the top of a path of
    struts that ends on the plate z = 0.
    """
    k = Fraction(k)
    nodes = [tuple(Fraction(x) for x in p) for p in points]
    active = set(range(len(nodes)))  # @line L1
    struts = []
    heap = []
    counter = 0

    def push(i, j):
        nonlocal counter
        a, b = (i, j) if nodes[i][2] >= nodes[j][2] else (j, i)
        m, saves = merge(nodes[a], nodes[b], k, grid)
        if saves:
            counter += 1
            heapq.heappush(heap, (-m[2], counter, a, b, m))

    order = sorted(active)
    for x in range(len(order)):  # @line L2
        for y in range(x + 1, len(order)):
            push(order[x], order[y])
    while heap:  # @line L3
        _, _, a, b, m = heapq.heappop(heap)  # @line L4
        if a not in active or b not in active:  # @line L5
            continue
        active -= {a, b}  # @line L6
        if m == nodes[b]:  # @line L7
            struts.append((a, b))
            new = b
        else:
            same = [r for r in active if nodes[r] == m]  # reuse an equal active point
            if same:
                new = same[0]
            else:
                nodes.append(m)  # @line L8
                new = len(nodes) - 1
            struts += [(a, new), (b, new)]
        active.add(new)  # @line L9
        for r in sorted(active - {new}):  # @line L10
            push(new, r)  # @line L11
    for a in sorted(active):  # @line L12
        p = nodes[a]
        nodes.append((p[0], p[1], Fraction(0)))
        struts.append((a, len(nodes) - 1))
    return nodes, struts  # @line L13


def total_length(nodes, struts):
    return sum(math.sqrt(float(dist2(nodes[a], nodes[b]))) for a, b in struts)


if __name__ == "__main__":
    pts = [(0, 0, 4), (2, 0, 4), (6, 0, 4)]
    nodes, struts = tree_support(pts)
    for a, b in struts:
        print([str(x) for x in nodes[a]], "->", [str(x) for x in nodes[b]])
    print(total_length(nodes, struts), sum(p[2] for p in pts))
