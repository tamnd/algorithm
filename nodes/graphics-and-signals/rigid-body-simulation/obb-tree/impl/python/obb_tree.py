# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/obb-tree/. The authors are listed in prov/FZV7G9.jsonl.

"""An OBB tree over the triangles of a 2D object, and the overlap query of two such trees.

Each node stores an oriented box. The axes of the box are the principal axes of the convex hull
of the vertices below the node: the eigenvectors of the covariance of the hull boundary, with a
uniform density along the edges. This is the 2D form of the rule of Gottschalk, Lin and Manocha,
who use the area-weighted covariance of the hull triangles in 3D. A node splits along the
longest axis of its box at the mean of the projected triangle centroids, or at the median if the
mean puts all triangles on one side.

The query takes the pose (R, t) of the object B in the frame of A. It moves the boxes of B on the
fly, so the tree of a rigid object never needs a rebuild. Two boxes in 2D are disjoint exactly
when one of the 4 box axes separates them, the 2D form of the 15 axes in 3D.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

EPS = 1e-9  # the boxes grow by EPS times the scale, so that rounding cannot make the test miss a contact


def _sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def _dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    """Andrew's monotone chain, counterclockwise, without collinear points."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower: list = []
    for p in pts:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list = []
    for p in reversed(pts):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def principal_axis(points):
    """The unit eigenvector of the largest eigenvalue of the covariance of the hull boundary."""
    hull = convex_hull(points)
    if len(hull) == 1:
        return (1.0, 0.0)
    if len(hull) == 2:
        d = _sub(hull[1], hull[0])
        L = math.hypot(*d)
        return (d[0] / L, d[1] / L)
    total = mx = my = sxx = sxy = syy = 0.0
    for i in range(len(hull)):
        a, b = hull[i], hull[(i + 1) % len(hull)]
        L = math.dist(a, b)
        total += L
        mx += L * (a[0] + b[0]) / 2
        my += L * (a[1] + b[1]) / 2
        # the integral of x x^T along the segment, divided by its length: (a a^T + b b^T) / 3 + (a b^T + b a^T) / 6
        sxx += L * ((a[0] * a[0] + b[0] * b[0]) / 3 + a[0] * b[0] / 3)
        syy += L * ((a[1] * a[1] + b[1] * b[1]) / 3 + a[1] * b[1] / 3)
        sxy += L * ((a[0] * a[1] + b[0] * b[1]) / 3 + (a[0] * b[1] + b[0] * a[1]) / 6)
    mx, my = mx / total, my / total
    cxx, cyy, cxy = sxx / total - mx * mx, syy / total - my * my, sxy / total - mx * my
    theta = 0.5 * math.atan2(2 * cxy, cxx - cyy)
    return (math.cos(theta), math.sin(theta))


@dataclass
class OBB:
    center: tuple
    u: tuple  # the first unit axis; the second axis is (-u[1], u[0])
    half: tuple  # the half extents along u and along the second axis

    @property
    def v(self):
        return (-self.u[1], self.u[0])

    def corners(self):
        c, u, v, (hu, hv) = self.center, self.u, self.v, self.half
        return [(c[0] + su * hu * u[0] + sv * hv * v[0], c[1] + su * hu * u[1] + sv * hv * v[1]) for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]

    def moved(self, R, t):
        """The box under the rigid motion x -> R x + t, with R a 2 by 2 rotation matrix."""
        c = apply(R, t, self.center)
        u = (R[0][0] * self.u[0] + R[0][1] * self.u[1], R[1][0] * self.u[0] + R[1][1] * self.u[1])
        return OBB(c, u, self.half)


def fit_obb(points) -> OBB:
    u = principal_axis(points)
    v = (-u[1], u[0])
    pu = [_dot(p, u) for p in points]
    pv = [_dot(p, v) for p in points]
    a, b = (min(pu) + max(pu)) / 2, (min(pv) + max(pv)) / 2
    scale = max(1.0, max(abs(x) for p in points for x in p))
    hu, hv = (max(pu) - min(pu)) / 2 + EPS * scale, (max(pv) - min(pv)) / 2 + EPS * scale
    return OBB((a * u[0] + b * v[0], a * u[1] + b * v[1]), u, (hu, hv))


def obb_overlap(A: OBB, B: OBB) -> bool:
    """Separating axis test on the 4 axes of the two boxes: True if the closed boxes meet."""
    d = _sub(B.center, A.center)
    for L in (A.u, A.v, B.u, B.v):
        ra = A.half[0] * abs(_dot(L, A.u)) + A.half[1] * abs(_dot(L, A.v))
        rb = B.half[0] * abs(_dot(L, B.u)) + B.half[1] * abs(_dot(L, B.v))
        if abs(_dot(L, d)) > ra + rb:
            return False
    return True


def apply(R, t, p):
    return (R[0][0] * p[0] + R[0][1] * p[1] + t[0], R[1][0] * p[0] + R[1][1] * p[1] + t[1])


def rotation(angle):
    c, s = math.cos(angle), math.sin(angle)
    return ((c, -s), (s, c))


def triangles_overlap(T, U) -> bool:
    """Separating axis test on the 6 edge normals: True if the closed triangles meet."""
    for P in (T, U):
        for i in range(3):
            a, b = P[i], P[(i + 1) % 3]
            n = (a[1] - b[1], b[0] - a[0])
            p1 = [_dot(n, x) for x in T]
            p2 = [_dot(n, x) for x in U]
            if max(p1) < min(p2) or max(p2) < min(p1):
                return False
    return True


@dataclass
class Node:
    box: OBB
    tris: list  # the triangle indices below the node
    left: "Node | None" = None
    right: "Node | None" = None
    size: float = field(default=0.0)

    @property
    def leaf(self):
        return self.left is None


def build(tris) -> Node:
    """The OBB tree over the list of triangles (each a tuple of 3 points), one triangle per leaf."""
    return _build(tris, list(range(len(tris))))


def _build(tris, idx) -> Node:
    pts = [p for i in idx for p in tris[i]]
    box = fit_obb(pts)  # @line L1 L2 L3
    node = Node(box, idx, size=box.half[0] * box.half[1])
    if len(idx) == 1:  # @line L4
        return node
    axis = box.u if box.half[0] >= box.half[1] else box.v  # @line L5
    key = {i: _dot(axis, ((tris[i][0][0] + tris[i][1][0] + tris[i][2][0]) / 3, (tris[i][0][1] + tris[i][1][1] + tris[i][2][1]) / 3)) for i in idx}
    mean = sum(key.values()) / len(idx)
    lo = [i for i in idx if key[i] < mean]
    hi = [i for i in idx if key[i] >= mean]
    if not lo or not hi:  # @line L6
        s = sorted(idx, key=lambda i: key[i])
        lo, hi = s[: len(s) // 2], s[len(s) // 2:]
    node.left, node.right = _build(tris, lo), _build(tris, hi)  # @line L7
    return node


def overlap_pairs(A: Node, trisA, B: Node, trisB, R=((1.0, 0.0), (0.0, 1.0)), t=(0.0, 0.0)):
    """The pairs (i, j) such that triangle i of A meets triangle j of B moved by x -> R x + t.

    Returns the set of pairs and the number of box tests.
    """
    moved_tris = {}
    pairs = set()
    tests = 0
    stack = [(A, B)]  # @line L8
    while stack:
        a, b = stack.pop()
        tests += 1
        if not obb_overlap(a.box, b.box.moved(R, t)):  # @line L9
            continue
        if a.leaf and b.leaf:  # @line L10
            i, j = a.tris[0], b.tris[0]
            if j not in moved_tris:
                moved_tris[j] = tuple(apply(R, t, p) for p in trisB[j])
            if triangles_overlap(trisA[i], moved_tris[j]):
                pairs.add((i, j))
        elif b.leaf or (not a.leaf and a.size >= b.size):  # @line L11
            stack += [(a.left, b), (a.right, b)]
        else:
            stack += [(a, b.left), (a, b.right)]
    return pairs, tests
