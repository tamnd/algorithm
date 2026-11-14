# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modular-fixture-design/. The authors are listed in prov/SBR91R.jsonl.

"""All planar modular fixtures with three locators and a clamp, after
Brost and Goldberg (1996).

Model, as on the page:
- The part is a simple polygon with rational vertices in counterclockwise
  order. It may be placed at any rotation and translation.
- The fixture plate has holes at the integer points. A locator is a point
  at a hole. The clamp is anchored at a hole v outside the part and pushes
  along one axis direction (+x, -x, +y or -y) until it meets the part,
  at distance at most `reach`.
- All four contacts are frictionless points in the relative interior of
  an edge, never at a vertex. The contact force is along the inner normal
  of the edge.
- A fixture must have form closure: the four contact wrenches positively
  span R^3.

Poses are computed exactly. The angle of a pose solves a linear equation in
cos and sin, so its coordinates lie in a field Q(sqrt(D)) with D rational,
and every test below is an exact sign test in that field.
"""

from collections import namedtuple
from fractions import Fraction
from math import isqrt

Fixture = namedtuple("Fixture", ["locators", "edges", "pose", "clamp"])
# locators: three lattice points (q1 < q2 < q3, q1 = (0, 0))
# edges: the edge index touched by each locator
# pose: (c, s, tx, ty), world point = R(c, s) x + (tx, ty)
# clamp: (v, direction, edge index, contact point)

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Q2:
    """a + b sqrt(D) with rational a, b and a fixed rational D >= 0 that is
    not the square of a rational (or b = 0)."""

    __slots__ = ("a", "b", "d")

    def __init__(self, a, b=0, d=0):
        self.a = a if type(a) is Fraction else Fraction(a)
        self.b = b if type(b) is Fraction else Fraction(b)
        self.d = d if type(d) is Fraction else Fraction(d)

    def __add__(self, x):
        if isinstance(x, Q2):
            return Q2(self.a + x.a, self.b + x.b, self.d)
        return Q2(self.a + x, self.b, self.d)

    __radd__ = __add__

    def __neg__(self):
        return Q2(-self.a, -self.b, self.d)

    def __sub__(self, x):
        if isinstance(x, Q2):
            return Q2(self.a - x.a, self.b - x.b, self.d)
        return Q2(self.a - x, self.b, self.d)

    def __rsub__(self, x):
        return Q2(x - self.a, -self.b, self.d)

    def __mul__(self, x):
        if isinstance(x, Q2):
            return Q2(self.a * x.a + self.b * x.b * self.d, self.a * x.b + self.b * x.a, self.d)
        return Q2(self.a * x, self.b * x, self.d)

    __rmul__ = __mul__

    def __truediv__(self, x):
        if not isinstance(x, Q2):
            return Q2(self.a / x, self.b / x, self.d)
        n = x.a * x.a - x.b * x.b * self.d
        return self * Q2(x.a / n, -x.b / n, self.d)

    def sign(self):
        sa = (self.a > 0) - (self.a < 0)
        sb = (self.b > 0) - (self.b < 0)
        if sb == 0 or sa == sb:
            return sa if sa else sb
        if sa == 0:
            return sb
        # Opposite signs: compare a^2 with b^2 D. They differ, since sqrt(D) is irrational.
        return sa if self.a * self.a > self.b * self.b * self.d else sb

    def __float__(self):
        return float(self.a) + float(self.b) * float(self.d) ** 0.5

    def __repr__(self):
        return f"Q2({self.a}, {self.b}, {self.d})"


def _rational_sqrt(x):
    """sqrt(x) as a Fraction if x is the square of a rational, else None."""
    p, q = x.numerator, x.denominator
    rp, rq = isqrt(p), isqrt(q)
    if rp * rp == p and rq * rq == q:
        return Fraction(rp, rq)
    return None


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def edges_of(poly):
    """Edge k runs from poly[k] to poly[k+1]. Returns (start, end, outward normal, offset h)
    with the edge on the line m . x = h."""
    out = []
    n = len(poly)
    for k in range(n):
        p = tuple(Fraction(v) for v in poly[k])
        q = tuple(Fraction(v) for v in poly[(k + 1) % n])
        m = (q[1] - p[1], p[0] - q[0])  # outward for a counterclockwise polygon
        out.append((p, q, m, dot(m, p)))
    return out


def diameter_sq(poly):
    pts = [tuple(Fraction(v) for v in p) for p in poly]
    return max(dot((a[0] - b[0], a[1] - b[1]), (a[0] - b[0], a[1] - b[1])) for a in pts for b in pts)


def poses(edge_list, sites, chosen):
    """All poses (c, s, tx, ty) that put sites[k] on the line of edge chosen[k].

    With R m_a the rotated normal, the conditions are (R m_a) . t = (R m_a) . q_a - h_a.
    Three equations in t are consistent if and only if
    A cos + B sin + C0 = 0, with cofactors C_a that do not depend on the rotation.
    """
    ms = [edge_list[e][2] for e in chosen]
    hs = [edge_list[e][3] for e in chosen]
    cof = [cross(ms[1], ms[2]), cross(ms[2], ms[0]), cross(ms[0], ms[1])]
    if all(c == 0 for c in cof):
        return []  # all three normals parallel: never form closure
    a_ = sum(cof[i] * dot(ms[i], sites[i]) for i in range(3))
    b_ = sum(cof[i] * cross(ms[i], sites[i]) for i in range(3))
    c0 = -sum(cof[i] * hs[i] for i in range(3))
    r2 = a_ * a_ + b_ * b_
    if r2 == 0:
        return []  # no pose, or a continuum of poses that cannot have form closure
    disc = r2 - c0 * c0
    if disc < 0:
        return []
    root = _rational_sqrt(disc)
    if root is not None:
        cands = [(Q2((-a_ * c0 + sg * b_ * root) / r2), Q2((-b_ * c0 - sg * a_ * root) / r2)) for sg in (1, -1)]
    else:
        cands = [(Q2(-a_ * c0 / r2, sg * b_ / r2, disc), Q2(-b_ * c0 / r2, -sg * a_ / r2, disc)) for sg in (1, -1)]
    if disc == 0:
        cands = cands[:1]
    # Translation from two equations whose normals are not parallel.
    i, j = next((i, j) for i, j in ((0, 1), (1, 2), (2, 0)) if cross(ms[i], ms[j]) != 0)
    det = cross(ms[i], ms[j])
    out = []
    for c, s in cands:
        rm_i = rot(c, s, ms[i])
        rm_j = rot(c, s, ms[j])
        r_i = dot(rm_i, sites[i]) - hs[i]
        r_j = dot(rm_j, sites[j]) - hs[j]
        tx = (r_i * rm_j[1] - r_j * rm_i[1]) / det
        ty = (rm_i[0] * r_j - rm_j[0] * r_i) / det
        out.append((c, s, tx, ty))
    return out


def rot(c, s, v):
    return (c * v[0] - s * v[1], s * v[0] + c * v[1])


def to_world(pose, x):
    c, s, tx, ty = pose
    r = rot(c, s, x)
    return (r[0] + tx, r[1] + ty)


def strictly_inside_edge(world_edge, point):
    """Is point (known to be on the line of the edge) strictly between its ends?"""
    p, q = world_edge
    d = (q[0] - p[0], q[1] - p[1])
    u = dot((point[0] - p[0], point[1] - p[1]), d)
    return _sign(u) > 0 and _sign(dot(d, d) - u) > 0


def _sign(x):
    if isinstance(x, Q2):
        return x.sign()
    return (x > 0) - (x < 0)


def _contact_wrench(normal_in, point):
    return (normal_in[0], normal_in[1], cross(point, normal_in))


def _det3(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def form_closure(wrenches):
    """Four planar wrenches positively span R^3 if and only if they have rank 3
    and the null vector of signed 3 x 3 minors has all entries of one strict sign."""
    lam = []
    for i in range(4):
        rest = [wrenches[j] for j in range(4) if j != i]
        lam.append(_sign(_det3(rest)) * (-1) ** i)
    return all(x > 0 for x in lam) or all(x < 0 for x in lam)


def _point_in_or_on(world_poly, v):
    """0 if v is strictly outside the polygon, 1 if inside or on the boundary."""
    n = len(world_poly)
    inside = False
    for k in range(n):
        p, q = world_poly[k], world_poly[(k + 1) % n]
        # On the boundary?
        if _sign(cross((q[0] - p[0], q[1] - p[1]), (v[0] - p[0], v[1] - p[1]))) == 0:
            if _sign(dot((v[0] - p[0], v[1] - p[1]), (v[0] - q[0], v[1] - q[1]))) <= 0:
                return 1
        # Crossing number with the ray to +x, half-open rule.
        if (_sign(p[1] - v[1]) > 0) != (_sign(q[1] - v[1]) > 0):
            # The crossing is to the right of v if and only if this cross
            # product has the sign of q_y - p_y.
            side = _sign(cross((q[0] - p[0], q[1] - p[1]), (v[0] - p[0], v[1] - p[1])))
            if (side > 0) == (_sign(q[1] - p[1]) > 0):
                inside = not inside
    return 1 if inside else 0


def _seg_point_dist(a, b, p):
    dx, dy = b[0] - a[0], b[1] - a[1]
    ll = dx * dx + dy * dy
    u = 0.0 if ll == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / ll))
    ex, ey = a[0] + u * dx - p[0], a[1] + u * dy - p[1]
    return (ex * ex + ey * ey) ** 0.5


def _may_hit(fw, v, d, r, eps=1e-7):
    """A float filter that never rejects a real hit: is the segment from v to
    v + r d within eps of some edge?"""
    w = (v[0] + r * d[0], v[1] + r * d[1])
    n = len(fw)
    for k in range(n):
        p, q = fw[k], fw[(k + 1) % n]
        c1 = (q[0] - p[0]) * (v[1] - p[1]) - (q[1] - p[1]) * (v[0] - p[0])
        c2 = (q[0] - p[0]) * (w[1] - p[1]) - (q[1] - p[1]) * (w[0] - p[0])
        c3 = (w[0] - v[0]) * (p[1] - v[1]) - (w[1] - v[1]) * (p[0] - v[0])
        c4 = (w[0] - v[0]) * (q[1] - v[1]) - (w[1] - v[1]) * (q[0] - v[0])
        if c1 * c2 <= 0 and c3 * c4 <= 0:
            return True
        if min(_seg_point_dist(p, q, v), _seg_point_dist(p, q, w), _seg_point_dist(v, w, p), _seg_point_dist(v, w, q)) <= eps:
            return True
    return False


def first_hit(world_poly, v, d):
    """The first point of the boundary on the ray v + s d, s > 0, for an axis direction d.

    Returns (s, edge index) or None. Returns edge index -1 when the first
    point is a vertex or the ray runs along an edge.
    """
    best = None
    n = len(world_poly)
    ax, other = (0, 1) if d[0] != 0 else (1, 0)
    sgn = d[ax]
    for k in range(n):
        p, q = world_poly[k], world_poly[(k + 1) % n]
        dp = p[other] - v[other]
        dq = q[other] - v[other]
        sp, sq = _sign(dp), _sign(dq)
        if sp == 0 and sq == 0:
            # Edge on the line of the ray: the hit is at its nearer end, a vertex.
            for w in (p, q):
                s = (w[ax] - v[ax]) * sgn
                if _sign(s) > 0 and (best is None or _sign(s - best[0]) < 0):
                    best = (s, -1)
            continue
        if sp == sq:
            continue
        lam = dp / (dp - dq)  # point p + lam (q - p) is on the line of the ray
        x = p[ax] + lam * (q[ax] - p[ax])
        s = (x - v[ax]) * sgn
        if _sign(s) <= 0:
            continue
        at_vertex = sp == 0 or sq == 0
        if best is None or _sign(s - best[0]) < 0:
            best = (s, -1 if at_vertex else k)
        elif _sign(s - best[0]) == 0:
            best = (s, -1)
    return best


def fixtures(poly, reach=1):
    """Every fixture of the model, each once, with the smallest locator at the origin."""
    reach = Fraction(reach)
    edge_list = edges_of(poly)
    n = len(edge_list)
    d2 = diameter_sq(poly)  # @line L1
    dmax = isqrt(int(d2)) + 1
    origin = (0, 0)
    # Sites lexicographically after the origin, within the diameter.
    near = [
        (x, y)
        for x in range(0, dmax + 1)
        for y in range(-dmax, dmax + 1)
        if (x, y) > origin and x * x + y * y <= d2
    ]
    found = []
    for q2 in near:  # @line L2
        for q3 in near:
            if not q3 > q2:
                continue
            dx, dy = q3[0] - q2[0], q3[1] - q2[1]
            if dx * dx + dy * dy > d2:
                continue
            sites = (origin, q2, q3)
            for e1 in range(n):  # @line L3
                for e2 in range(n):
                    for e3 in range(n):
                        chosen = (e1, e2, e3)
                        for pose in poses(edge_list, sites, chosen):  # @line L4
                            found.extend(_complete(poly, edge_list, sites, chosen, pose, reach))
    return found


def _complete(poly, edge_list, sites, chosen, pose, reach):
    world = [to_world(pose, p) for p in poly]
    n = len(world)
    for k in range(3):  # @line L5
        e = chosen[k]
        if not strictly_inside_edge((world[e], world[(e + 1) % n]), sites[k]):
            return []
    c, s = pose[0], pose[1]
    wrenches = [_contact_wrench(rot(c, s, tuple(-v for v in edge_list[e][2])), q) for e, q in zip(chosen, sites)]
    # Candidate clamp holes: the bounding box of the placed part grown by the reach.
    fw = [(float(p[0]), float(p[1])) for p in world]
    xs = [p[0] for p in fw]
    ys = [p[1] for p in fw]
    r = float(reach)
    lo_x, hi_x = int(min(xs) - r) - 1, int(max(xs) + r) + 1
    lo_y, hi_y = int(min(ys) - r) - 1, int(max(ys) + r) + 1
    out = []
    for vx in range(lo_x, hi_x + 1):  # @line L6
        for vy in range(lo_y, hi_y + 1):
            v = (vx, vy)
            dirs = [dv for dv in DIRECTIONS if _may_hit(fw, v, dv, r)]
            if not dirs or _point_in_or_on(world, v):
                continue
            for dvec in dirs:
                hit = first_hit(world, v, dvec)  # @line L7
                if hit is None or hit[1] < 0 or _sign(hit[0] - reach) > 0:
                    continue
                e = hit[1]
                u = (v[0] + hit[0] * dvec[0], v[1] + hit[0] * dvec[1])
                if any(_sign(u[0] - q[0]) == 0 and _sign(u[1] - q[1]) == 0 for q in sites):
                    continue  # the clamp would touch the part at a locator
                normal_in = rot(c, s, tuple(-x for x in edge_list[e][2]))
                if form_closure(wrenches + [_contact_wrench(normal_in, u)]):  # @line L8
                    out.append(Fixture(sites, chosen, pose, (v, dvec, e, u)))
    return out
