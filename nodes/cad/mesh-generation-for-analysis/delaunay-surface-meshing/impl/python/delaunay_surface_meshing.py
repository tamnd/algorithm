# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delaunay-surface-meshing/. The authors are listed in prov/8F2351.jsonl.

"""Boissonnat and Oudot's Delaunay refinement surface mesher (2005).

The surface S is the zero set of a polynomial F with integer coefficients: a
sphere or a torus. It is known to the mesher only through an oracle that, given
a segment or a ray, returns the points where it meets S. The mesher keeps the
3D Delaunay triangulation of the sample E, finds the restricted Delaunay
triangles (those whose dual Voronoi edge meets S), and inserts the center c of
any surface Delaunay ball B(c, r) with r > sigma(c), until there is none.

Coordinates are integers. A new vertex is the exact intersection of a Voronoi
edge with S, located to within a small fraction of a unit and rounded once to
the integer grid, so it lies within one unit of S. All predicates on the
current points are exact: orientation and insphere signs use int arithmetic,
and the question whether a Voronoi edge meets S is answered by an exact Sturm
sequence on a polynomial with integer coefficients. Radii and sigma are
compared in floating point, which only decides which balls count as bad.
"""

import math
import random
from fractions import Fraction
from typing import Callable, Dict, List, Optional, Sequence, Set, Tuple, Union

from mg2geom import cross, dist2, dot, insphere, orient3d, sub

Tet = Tuple[int, int, int, int]
Face = Tuple[int, int, int]
GHOST = -1  # the vertex at infinity; a tetrahedron with it is a hull face


# polynomials in one variable s: lists of coefficients, index = power
def padd(p: Sequence, q: Sequence) -> list:
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)]


def pmul(p: Sequence, q: Sequence) -> list:
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def peval(p: Sequence, x):
    v = 0
    for c in reversed(p):
        v = v * x + c
    return v


def _trim(p: Sequence) -> list:
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def _sign(x) -> int:
    return (x > 0) - (x < 0)


def _rem(a: Sequence, b: Sequence) -> list:
    a = [Fraction(x) for x in a]
    while len(a) >= len(b) and not (len(a) == 1 and a[0] == 0):
        c = a[-1] / b[-1]
        sh = len(a) - len(b)
        for i in range(len(b)):
            a[sh + i] -= c * b[i]
        a.pop()
        a = _trim(a) if a else [Fraction(0)]
    return a


def sturm(p: Sequence) -> List[list]:
    """The Sturm sequence p, p', -rem(p, p'), ... of a nonzero polynomial."""
    p = _trim(p)
    seq = [p]
    if len(p) == 1:
        return seq
    seq.append([i * p[i] for i in range(1, len(p))])
    while len(seq[-1]) > 1:
        r = _rem(seq[-2], seq[-1])
        if len(r) == 1 and r[0] == 0:
            break
        seq.append([-x for x in r])
    return seq


def _variations(seq: List[list], x) -> int:
    """Sign changes of the sequence at x; x = None means +infinity, '-' means -infinity."""
    signs = []
    for q in seq:
        if x is None:
            s = _sign(q[-1])
        elif x == "-":
            s = _sign(q[-1]) * (-1) ** (len(q) - 1)
        else:
            s = _sign(peval(q, x))
        if s:
            signs.append(s)
    return sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])


def count_roots(seq: List[list], lo, hi) -> int:
    """Number of distinct real roots of seq[0] in (lo, hi] (Sturm's theorem)."""
    return _variations(seq, lo) - _variations(seq, hi)


def _quo(a: Sequence, b: Sequence) -> list:
    """The quotient of a by b, for b dividing a exactly."""
    a = [Fraction(x) for x in a]
    q = [Fraction(0)] * (len(a) - len(b) + 1)
    for sh in range(len(a) - len(b), -1, -1):
        c = a[sh + len(b) - 1] / b[-1]
        q[sh] = c
        for i in range(len(b)):
            a[sh + i] -= c * b[i]
    return _trim(q)


def root_bound(p: Sequence) -> Fraction:
    """Cauchy's bound: every real root has absolute value below it."""
    p = _trim(p)
    return 1 + max(Fraction(abs(c), abs(p[-1])) for c in p[:-1])


def roots_in(p: Sequence, lo, hi, tol: Fraction) -> List[Fraction]:
    """The distinct real roots of p in [lo, hi], each to within tol.

    lo is a Fraction or '-' for minus infinity; hi a Fraction or None for plus
    infinity. The number of roots is exact; only their positions are approximate.
    A repeated root is first removed by dividing p by gcd(p, p'), so that every
    remaining root is simple and Sturm's theorem counts the roots in (a, b]
    even when a or b is a root.
    """
    p = _trim(p)
    if len(p) == 1:
        if p[0] == 0:
            raise ValueError("the line lies in the surface")
        return []
    seq = sturm(p)
    if len(seq[-1]) > 1:  # p has a repeated root: keep its square-free part, same distinct roots
        p = _quo(p, seq[-1])
        seq = sturm(p)
    out = []
    if lo == "-":
        lo = -root_bound(p)
    elif peval(p, lo) == 0:
        out.append(Fraction(lo))
    if hi is None:
        hi = root_bound(p)
    stack = [(Fraction(lo), Fraction(hi))]
    while stack:
        a, b = stack.pop()
        n = count_roots(seq, a, b)
        if n == 0:
            continue
        sa, sb = _sign(peval(p, a)), _sign(peval(p, b))
        if n == 1 and sb == 0:
            out.append(b)
        elif n == 1 and sa * sb < 0:
            while b - a > tol:  # one simple root, where p changes sign
                m = (a + b) / 2
                sm = _sign(peval(p, m))
                if sm == 0:
                    a = b = m
                elif sm == sa:
                    a = m
                else:
                    b = m
            out.append((a + b) / 2)
        elif b - a <= tol:
            out.append(b if sb == 0 else (a + b) / 2)
        else:
            m = (a + b) / 2
            stack.append((m, b))
            stack.append((a, m))
    return sorted(out)


def _sq(a, b) -> list:
    """(a + b s)^2."""
    return [a * a, 2 * a * b, b * b]


class Sphere:
    """The sphere |x| = R. Its medial axis is the center, so lfs = R everywhere."""

    euler = 2

    def __init__(self, R: int):
        if int(R) != R or R <= 0:
            raise ValueError("R must be a positive integer")
        self.R = int(R)

    def poly(self, A: Sequence[int], B: Sequence[int], W: int) -> list:
        """W^2 F((A + s B) / W) as a polynomial in s with integer coefficients."""
        p = [-self.R * self.R * W * W]
        for k in range(3):
            p = padd(p, _sq(A[k], B[k]))
        return p

    def distance(self, p: Sequence) -> float:
        return abs(math.sqrt(sum(float(x) ** 2 for x in p)) - self.R)

    def lfs(self, p: Sequence) -> float:
        return float(self.R)

    def project(self, p: Sequence[float]) -> tuple:
        n = math.sqrt(sum(x * x for x in p))
        return tuple(x * self.R / n for x in p)

    def normal(self, p: Sequence[float]) -> tuple:
        n = math.sqrt(sum(x * x for x in p))
        return tuple(x / n for x in p)

    def seeds(self, rng: random.Random) -> List[tuple]:
        """Four points of a randomly rotated regular tetrahedron on the sphere."""
        q = _random_rotation(rng)
        base = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
        return [self.project(_apply(q, v)) for v in base]


class Torus:
    """The torus at distance r from the circle of radius R in the plane z = 0.

    With R >= 2 r its medial axis is that circle together with the z axis, so
    lfs = r everywhere.
    """

    euler = 0

    def __init__(self, R: int, r: int):
        if int(R) != R or int(r) != r or r <= 0 or R < 2 * r:
            raise ValueError("need integers R >= 2 r > 0")
        self.R, self.r = int(R), int(r)

    def poly(self, A: Sequence[int], B: Sequence[int], W: int) -> list:
        """W^4 F((A + s B) / W) with F = (|x|^2 + R^2 - r^2)^2 - 4 R^2 (x^2 + y^2)."""
        R2, r2, W2 = self.R * self.R, self.r * self.r, W * W
        xy = padd(_sq(A[0], B[0]), _sq(A[1], B[1]))
        q = padd(padd(xy, _sq(A[2], B[2])), [(R2 - r2) * W2])
        return padd(pmul(q, q), [-4 * R2 * W2 * c for c in xy])

    def _core(self, p: Sequence[float]) -> tuple:
        rho = math.hypot(p[0], p[1])
        return (self.R * p[0] / rho, self.R * p[1] / rho, 0.0)

    def distance(self, p: Sequence) -> float:
        q = [float(x) for x in p]
        return abs(math.hypot(math.hypot(q[0], q[1]) - self.R, q[2]) - self.r)

    def lfs(self, p: Sequence) -> float:
        return float(self.r)

    def normal(self, p: Sequence[float]) -> tuple:
        c = self._core(p)
        d = sub(p, c)
        n = math.sqrt(dot(d, d))
        return tuple(x / n for x in d)

    def project(self, p: Sequence[float]) -> tuple:
        c = self._core(p)
        return tuple(c[k] + self.r * v for k, v in enumerate(self.normal(p)))

    def seeds(self, rng: random.Random) -> List[tuple]:
        """Four points spread around the torus, at random angles."""
        out = []
        a0 = rng.uniform(0, 2 * math.pi)
        for i in range(4):
            a = a0 + i * math.pi / 2
            b = rng.uniform(0, 2 * math.pi)
            rho = self.R + self.r * math.cos(b)
            out.append((rho * math.cos(a), rho * math.sin(a), self.r * math.sin(b)))
        return out


def _random_rotation(rng: random.Random) -> list:
    q = [rng.gauss(0, 1) for _ in range(4)]
    n = math.sqrt(sum(x * x for x in q))
    w, x, y, z = (v / n for v in q)
    return [
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
        [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
        [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
    ]


def _apply(m: list, v: Sequence) -> tuple:
    return tuple(sum(m[i][j] * v[j] for j in range(3)) for i in range(3))


def _round(p: Sequence) -> tuple:
    return tuple(int(round(x)) for x in p)


def faces_of(t: Tet) -> List[Face]:
    return [t[:i] + t[i + 1 :] for i in range(4)]


def circumcenter_hom(a, b, c, d) -> Tuple[tuple, int]:
    """The circumcenter of a tetrahedron as N / W with integer N and W > 0."""
    u, v, w = sub(b, a), sub(c, a), sub(d, a)
    det = dot(u, cross(v, w))
    if det == 0:
        raise ValueError("flat tetrahedron")
    uu, vv, ww = dot(u, u), dot(v, v), dot(w, w)
    cvw, cwu, cuv = cross(v, w), cross(w, u), cross(u, v)
    N = tuple(2 * det * a[k] + uu * cvw[k] + vv * cwu[k] + ww * cuv[k] for k in range(3))
    W = 2 * det
    return (N, W) if W > 0 else (tuple(-x for x in N), -W)


class Mesher:
    """The 3D Delaunay triangulation of the sample, kept with hull (ghost) tetrahedra,
    and its restricted Delaunay triangles."""

    def __init__(self, surface, sigma: Union[float, Callable], seed: int = 0, max_vertices: int = 2000):
        self.S = surface
        self.sigma = sigma if callable(sigma) else (lambda p, s=float(sigma): s)
        self.max_vertices = max_vertices
        self.rng = random.Random(seed)
        self.pts: List[tuple] = []
        self.tets: Set[Tet] = set()
        self.face_tets: Dict[Face, Set[Tet]] = {}
        self.cc: Dict[Tet, Tuple[tuple, int]] = {}
        self.inside: Optional[tuple] = None
        self.balls: Dict[Face, List[tuple]] = {}  # restricted face -> [(center, r, sigma(center))]
        self.persistent: List[Face] = []
        self.log: List[tuple] = []  # (center, r, sigma) of each inserted point

    # the oracle: where a Voronoi edge meets S
    def voronoi_edge(self, f: Face) -> Tuple[tuple, tuple, int, Optional[int]]:
        """The Voronoi edge dual to face f as (A, B, W, end): the points (A + s B) / W
        for s in [0, end], with end = None for a ray."""
        t1, t2 = self.face_tets[f]
        if t1[0] == GHOST:
            t1, t2 = t2, t1
        N1, W1 = self.cc[t1]
        if t2[0] != GHOST:
            N2, W2 = self.cc[t2]
            A = tuple(x * W2 for x in N1)
            return A, tuple(N2[k] * W1 - A[k] for k in range(3)), W1 * W2, 1
        a, b, c = (self.pts[v] for v in f)
        d = self.pts[next(v for v in t1 if v not in f)]
        n = cross(sub(b, a), sub(c, a))
        if dot(n, sub(d, a)) > 0:
            n = tuple(-x for x in n)
        return N1, tuple(W1 * x for x in n), W1, None

    def surface_balls(self, f: Face) -> List[tuple]:
        A, B, W, end = self.voronoi_edge(f)
        G = self.S.poly(A, B, W)  # @line L3
        length = math.sqrt(sum(float(x) ** 2 for x in B)) / W
        tol = Fraction(1, 8) / max(1, math.ceil(length))
        out = []
        a = self.pts[f[0]]
        for s in roots_in(G, Fraction(0), end, tol):
            x = tuple((A[k] + s * B[k]) / W for k in range(3))
            c = _round(x)
            r = math.sqrt(float(dist2(x, a)))
            out.append((c, r, self.sigma(c)))
        return out

    # Bowyer-Watson insertion with ghost tetrahedra
    def conflicts(self, t: Tet, p: tuple) -> bool:
        if t[0] == GHOST:
            f = [self.pts[v] for v in t[1:]]
            o = orient3d(*f, p)
            if o == 0:
                raise ValueError("degenerate input: a point on the plane of a hull face")
            return _sign(o) != _sign(orient3d(*f, self.inside))
        return insphere(*[self.pts[v] for v in t], p) > 0

    def _add_tet(self, t: Tet) -> None:
        t = tuple(sorted(t))
        if t[0] != GHOST:
            self.cc[t] = circumcenter_hom(*[self.pts[v] for v in t])
        self.tets.add(t)
        for f in faces_of(t):
            self.face_tets.setdefault(f, set()).add(t)

    def _remove_tet(self, t: Tet) -> None:
        self.tets.discard(t)
        self.cc.pop(t, None)
        for f in faces_of(t):
            s = self.face_tets[f]
            s.discard(t)
            if not s:
                del self.face_tets[f]

    def insert(self, p: tuple, hint: Sequence[Tet] = ()) -> int:
        if len(self.pts) >= self.max_vertices:
            raise RuntimeError("too many vertices")
        if p in self.pts:
            raise ValueError("repeated point")
        start = next((t for t in hint if t in self.tets and self.conflicts(t, p)), None)
        if start is None:
            start = next(t for t in sorted(self.tets) if self.conflicts(t, p))
        cavity = {start}
        stack = [start]
        while stack:
            t = stack.pop()
            for f in faces_of(t):
                for u in self.face_tets[f]:
                    if u not in cavity and self.conflicts(u, p):
                        cavity.add(u)
                        stack.append(u)
        boundary = []
        for t in cavity:
            for f in faces_of(t):
                if not any(u in cavity for u in self.face_tets[f] if u != t):
                    boundary.append(f)
        self.pts.append(p)
        v = len(self.pts) - 1
        for t in cavity:
            self._remove_tet(t)
        new = []
        for f in boundary:
            real = [self.pts[w] for w in f if w != GHOST]
            if len(real) == 3 and orient3d(*real, p) == 0:
                raise ValueError("degenerate input: cospherical or coplanar points")
            self._add_tet(f + (v,))
            new.append(tuple(sorted(f + (v,))))
        return v

    def _start(self, pts: Sequence[tuple]) -> None:
        """The first tetrahedron and its four hull faces, then the other points."""
        a, b, c = pts[0], pts[1], pts[2]
        i = next(i for i in range(3, len(pts)) if orient3d(a, b, c, pts[i]) != 0)
        first = [a, b, c, pts[i]]
        self.pts = list(first)
        self.inside = tuple(Fraction(sum(q[k] for q in first), 4) for k in range(3))
        self._add_tet((0, 1, 2, 3))
        for f in faces_of((0, 1, 2, 3)):
            self._add_tet((GHOST,) + f)
        for q in pts[3:i] + pts[i + 1 :]:
            self.insert(q)

    # restricted Delaunay triangles
    def update_faces(self, faces) -> None:
        for f in faces:
            if GHOST in f:
                continue
            if f not in self.face_tets:
                self.balls.pop(f, None)
                continue
            b = self.surface_balls(f)
            if b:
                self.balls[f] = b
            else:
                self.balls.pop(f, None)

    def restricted(self) -> Set[Face]:
        return set(self.balls)

    def worst_ball(self) -> Optional[tuple]:
        best = None
        for f in sorted(self.balls):
            for c, r, sg in self.balls[f]:
                if r > sg and (best is None or r / sg > best[0]):
                    best = (r / sg, f, c, r, sg)
        return best

    def initial_sample(self) -> List[tuple]:
        """Section 7 of the paper: three points of S near each seed, forming a persistent facet."""
        seeds = self.S.seeds(self.rng)
        out = []
        for x in seeds:
            d = min(math.dist(x, y) for y in seeds if y is not x)
            rad = 0.99 * min(d / 6, self.S.lfs(x), self.sigma(_round(x)) / 6)
            for _ in range(50):
                tri = self._triangle_near(x, rad)
                if tri is not None:
                    out.extend(tri)
                    break
            else:
                raise RuntimeError("no persistent facet found near a seed")
        return out

    def _triangle_near(self, x: tuple, rad: float) -> Optional[List[tuple]]:
        n = self.S.normal(x)
        e = (1.0, 0.0, 0.0) if abs(n[0]) < 0.9 else (0.0, 1.0, 0.0)
        t1 = cross(n, e)
        l1 = math.sqrt(dot(t1, t1))
        t1 = tuple(v / l1 for v in t1)
        t2 = cross(n, t1)
        a0 = self.rng.uniform(0, 2 * math.pi)
        tri = []
        for i in range(3):
            a = a0 + i * 2 * math.pi / 3 + self.rng.uniform(-0.3, 0.3)
            q = tuple(x[k] + 0.5 * rad * (math.cos(a) * t1[k] + math.sin(a) * t2[k]) for k in range(3))
            tri.append(_round(self.S.project(q)))
        if len(set(tri)) < 3:
            return None
        # the line through the circumcenter, normal to the triangle, must meet S inside B(x, rad)
        a, b, c = tri
        u, v = sub(b, a), sub(c, a)
        nn = cross(u, v)
        W = 2 * dot(nn, nn)
        if W == 0:
            return None
        N = tuple(W * a[k] + dot(u, u) * cross(v, nn)[k] + dot(v, v) * cross(nn, u)[k] for k in range(3))
        G = self.S.poly(N, tuple(W * k for k in nn), W)
        for s in roots_in(G, "-", None, Fraction(1, 1 << 40)):
            y = tuple(float((N[k] + s * W * nn[k]) / W) for k in range(3))
            if math.dist(y, x) < rad:
                return tri
        return None

    def run(self) -> None:
        init = self.initial_sample()  # @line L1
        self._start(init)  # @line L2
        self.persistent = [tuple(sorted(self.pts.index(q) for q in init[i : i + 3])) for i in range(0, len(init), 3)]
        self.update_faces(list(self.face_tets))
        while True:
            w = self.worst_ball()  # @line L4
            if w is None:
                break
            _, f, c, r, sg = w  # @line L5
            old = set(self.tets)
            self.insert(c, sorted(self.face_tets[f]))  # @line L6
            self.log.append((c, r, sg))
            gone = old - self.tets
            born = self.tets - old
            touched = {g for t in gone | born for g in faces_of(t)}
            self.update_faces(sorted(touched))  # @line L7


def delaunay_surface_mesh(surface, sigma: Union[float, Callable], seed: int = 0, max_vertices: int = 2000) -> Mesher:
    """Mesh the surface until every surface Delaunay ball B(c, r) has r <= sigma(c).

    sigma is a number or a function of a point, in the integer units of the
    surface, and must be positive and 1-Lipschitz. Returns the Mesher: pts holds
    the sample and restricted() the triangles of the restricted Delaunay
    triangulation, as triples of indices into pts.
    """
    m = Mesher(surface, sigma, seed, max_vertices)
    m.run()
    return m  # @line L8
