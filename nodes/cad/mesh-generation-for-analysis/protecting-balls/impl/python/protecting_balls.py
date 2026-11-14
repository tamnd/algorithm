# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/protecting-balls/. The authors are listed in prov/EADV10.jsonl.

"""Protecting balls for the sharp edges of a domain, turned into weighted points.

The sharp features are a 1-complex in R^3: vertices with integer coordinates
and straight segments that meet only at shared endpoints, at any angle, however
small. PROTECT puts a ball on every vertex and a chain of balls along every
segment, with radii that shrink near a vertex where two segments meet at a
small angle. Each ball B(x, r) becomes the weighted point (x, r^2).

The layout is computed in floating point, then the centers (rational points of
the segments) and radii (rationals) are fixed, and the protection properties
are checked exactly with Fraction arithmetic:

  (a) adjacent balls of a chain overlap and neither contains the other's center:
      max(r_p, r_q) < |pq| < r_p + r_q;
  (b) balls that are not adjacent are disjoint;
  (c) no ball meets a piece [p, q] of a chain unless it is centered at p or q.

restricted_pairs computes, exactly, which pairs of sites have power cells that
meet at a point of a segment, using the lower envelope of affine functions;
restricted_pairs_brute does the same from scratch in O(n^2). With (a) and (c),
the pairs on each segment are exactly the consecutive balls of its chain, for
any set of unweighted points added to the sites.
"""

import math
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Set, Tuple

Point = Sequence


def sub(a: Point, b: Point) -> tuple:
    return tuple(x - y for x, y in zip(a, b))


def dot(a: Point, b: Point):
    return sum(x * y for x, y in zip(a, b))


def cross(a: Point, b: Point) -> tuple:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dist2(a: Point, b: Point):
    d = sub(a, b)
    return dot(d, d)


def point_seg_dist2(p: Point, a: Point, b: Point):
    """Squared distance from p to the closed segment ab. Exact for int or Fraction input."""
    d = sub(b, a)
    dd = dot(d, d)
    t = dot(sub(p, a), d)
    if t <= 0:
        return dist2(p, a)
    if t >= dd:
        return dist2(p, b)
    if isinstance(t, float) or isinstance(dd, float):
        tt = t / dd
    else:
        tt = Fraction(t) / dd
    q = tuple(ai + tt * di for ai, di in zip(a, d))
    return dist2(p, q)


def seg_seg_dist2(a: Point, b: Point, c: Point, d: Point) -> Fraction:
    """Exact squared distance between closed segments ab and cd (integer or rational input)."""
    best = min(point_seg_dist2(a, c, d), point_seg_dist2(b, c, d), point_seg_dist2(c, a, b), point_seg_dist2(d, a, b))
    u, v, w = sub(b, a), sub(d, c), sub(a, c)
    A, B, C = dot(u, u), dot(u, v), dot(v, v)
    den = A * C - B * B
    if den != 0:
        D, E = dot(u, w), dot(v, w)
        s = Fraction(B * E - C * D, 1) / den
        t = Fraction(A * E - B * D, 1) / den
        if 0 <= s <= 1 and 0 <= t <= 1:
            p = tuple(ai + s * ui for ai, ui in zip(a, u))
            q = tuple(ci + t * vi for ci, vi in zip(c, v))
            best = min(best, dist2(p, q))
    return Fraction(best)


class Ball:
    """A protecting ball B(center, r); vertex is set for a vertex ball, seg for a segment ball."""

    __slots__ = ("center", "r", "vertex", "seg")

    def __init__(self, center: tuple, r: Fraction, vertex: Optional[int] = None, seg: Optional[int] = None):
        self.center = center
        self.r = r
        self.vertex = vertex
        self.seg = seg

    def weighted(self) -> Tuple[tuple, Fraction]:
        return self.center, self.r * self.r


class Protection:
    """The balls, and for each segment the chain of ball indices from its first to its second endpoint."""

    def __init__(self, points, segments, c, balls, chains):
        self.points = points
        self.segments = segments
        self.c = c
        self.balls: List[Ball] = balls
        self.chains: List[List[int]] = chains

    def adjacent_pairs(self) -> Set[Tuple[int, int]]:
        out = set()
        for ch in self.chains:
            for i, j in zip(ch, ch[1:]):
                out.add((min(i, j), max(i, j)))
        return out

    def weighted_points(self) -> List[Tuple[tuple, Fraction]]:
        return [b.weighted() for b in self.balls]


def check_complex(points: Sequence[Point], segments: Sequence[Tuple[int, int]]) -> None:
    """Raise ValueError unless the segments form a proper 1-complex on the given vertices."""
    n = len(points)
    seen = set()
    used = set()
    for i, j in segments:
        if not (0 <= i < n and 0 <= j < n) or i == j:
            raise ValueError("bad segment")
        key = (min(i, j), max(i, j))
        if key in seen:
            raise ValueError("duplicate segment")
        seen.add(key)
        used.update(key)
    if len(used) != n:
        raise ValueError("every vertex must be an endpoint of a segment")
    for k, (i, j) in enumerate(segments):
        for l in range(k + 1, len(segments)):
            p, q = segments[l]
            shared = {i, j} & {p, q}
            if not shared:
                if seg_seg_dist2(points[i], points[j], points[p], points[q]) == 0:
                    raise ValueError("segments cross")
            else:
                (s,) = shared
                a = sub(points[j if s == i else i], points[s])
                b = sub(points[q if s == p else p], points[s])
                if cross(a, b) == (0, 0, 0) and dot(a, b) > 0:
                    raise ValueError("segments overlap")


def _fseg_dist(p, a, b) -> float:
    return math.sqrt(float(point_seg_dist2(tuple(map(float, p)), tuple(map(float, a)), tuple(map(float, b)))))


def _fsegseg(a, b, c, d) -> float:
    return math.sqrt(float(seg_seg_dist2(a, b, c, d)))


def _sin_min_angle(points, segments, e: int, end: int) -> float:
    """sin of the smallest angle at vertex `end` between segment e and the other segments there, capped at 90 degrees."""
    i, j = segments[e]
    other = j if end == i else i
    a = sub(points[other], points[end])
    best = 1.0
    for k, (p, q) in enumerate(segments):
        if k == e or end not in (p, q):
            continue
        b = sub(points[q if end == p else p], points[end])
        if dot(a, b) <= 0:
            continue
        s = math.sqrt(dot(cross(a, b), cross(a, b)) / (dot(a, a) * dot(b, b)))
        best = min(best, s)
    return best


def _dyadic(x: float, bits: int) -> Fraction:
    """x rounded down to a multiple of 2^-bits, so a radius never grows."""
    return Fraction(math.floor(x * (1 << bits)), 1 << bits)


class _Rho:
    """rho(s) = c min(H, s su, (L - s) sv) on [0, L], and phi(s) = integral of ds / rho."""

    def __init__(self, c, H, su, sv, L):
        self.c, self.H, self.su, self.sv, self.L = c, H, su, sv, L

    def __call__(self, s: float) -> float:
        return self.c * min(self.H, s * self.su, (self.L - s) * self.sv)

    def phi(self, s0: float, s1: float, steps: int = 400) -> float:
        # the integrand is 1 / (piecewise linear), smooth between breakpoints; a fine
        # midpoint rule on a geometric grid is accurate far beyond what is needed
        tot = 0.0
        h = (s1 - s0) / steps
        for k in range(steps):
            tot += h / self(s0 + (k + 0.5) * h)
        return tot


def _solve(fn, x0: float) -> float:
    x = x0
    for _ in range(100):
        x = fn(x)
    return x


def protect(points: Sequence[Point], segments: Sequence[Tuple[int, int]], c: float = 0.25, check: bool = True) -> Protection:
    """Protecting balls for the sharp segments; raises ValueError if the exact check fails.

    The ball size factor c must be below 1/2 for the properties to be guaranteed.
    check=False skips the exact check, to measure what happens with larger balls.
    """
    if not 0 < c:
        raise ValueError("c must be positive")
    check_complex(points, segments)
    n = len(points)
    inc: Dict[int, List[int]] = {v: [] for v in range(n)}
    for k, (i, j) in enumerate(segments):
        inc[i].append(k)
        inc[j].append(k)
    length = [math.sqrt(dist2(points[i], points[j])) for i, j in segments]

    balls: List[Ball] = []
    rv: List[float] = []
    for v in range(n):
        H = min((_fseg_dist(points[v], points[p], points[q]) for p, q in segments if v not in (p, q)), default=math.inf)
        r = c * min(H, min(length[k] for k in inc[v]) / 2)  # @line L1
        R = _dyadic(r, 24)
        balls.append(Ball(tuple(Fraction(x) for x in points[v]), R, vertex=v))
        rv.append(float(R))

    chains: List[List[int]] = []
    for e, (u, v) in enumerate(segments):
        L = length[e]
        H = min(
            (_fsegseg(points[u], points[v], points[p], points[q]) for p, q in segments if not {u, v} & {p, q}),
            default=math.inf,
        )
        rho = _Rho(c, H, _sin_min_angle(points, segments, e, u), _sin_min_angle(points, segments, e, v), L)  # @line L2
        sa = _solve(lambda s: rv[u] + rho(s) / 2, rv[u])  # @line L3
        sb = _solve(lambda s: L - rv[v] - rho(s) / 2, L - rv[v])
        Phi = rho.phi(sa, sb)
        if Phi <= 0.7:  # @line L4
            pos = [(sa + sb) / 2]
        else:
            m = math.ceil(Phi / 1.4)
            pos = [sa]
            for k in range(1, m):
                # next center one m-th of Phi further along in phi
                lo, hi = pos[-1], sb
                for _ in range(50):
                    mid = (lo + hi) / 2
                    if rho.phi(pos[-1], mid, 40) < Phi / m:
                        lo = mid
                    else:
                        hi = mid
                pos.append((lo + hi) / 2)
            pos.append(sb)
        ts = [_dyadic(s / L, 32) for s in pos]
        d = sub(points[v], points[u])
        chain = [u]
        full = [0.0] + [float(t) * L for t in ts] + [L]
        for k, t in enumerate(ts):
            s = full[k + 1]
            gap = min(s - full[k], full[k + 2] - s)
            r = min(rho(s), 0.9 * gap)  # @line L5
            center = tuple(Fraction(a) + t * di for a, di in zip(points[u], d))
            balls.append(Ball(center, _dyadic(r, 24), seg=e))
            chain.append(len(balls) - 1)
        chain.append(v)
        chains.append(chain)

    prot = Protection(points, segments, c, balls, chains)
    bad = violations(prot) if check else []  # @line L6
    if bad:
        raise ValueError("protection check failed: %s" % (bad[:3],))
    return prot  # @line L7


def violations(prot: Protection) -> List[tuple]:
    """Every failure of the protection properties (a), (b), (c), checked exactly."""
    balls = prot.balls
    adj = prot.adjacent_pairs()
    bad = []
    for i, j in sorted(adj):
        d2 = dist2(balls[i].center, balls[j].center)
        ri, rj = balls[i].r, balls[j].r
        if not (max(ri, rj) ** 2 < d2 < (ri + rj) ** 2):
            bad.append(("a", i, j))
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if (i, j) in adj:
                continue
            if dist2(balls[i].center, balls[j].center) <= (balls[i].r + balls[j].r) ** 2:
                bad.append(("b", i, j))
    for ch in prot.chains:
        for p, q in zip(ch, ch[1:]):
            a, b = balls[p].center, balls[q].center
            for k, ball in enumerate(balls):
                if k in (p, q):
                    continue
                if point_seg_dist2(ball.center, a, b) <= ball.r ** 2:
                    bad.append(("c", k, p, q))
    for ch in prot.chains:
        if len(ch) < 3:
            bad.append(("chain", ch))
    return bad


def _lines(a: Point, b: Point, sites: Sequence[Tuple[Point, Fraction]]) -> List[Tuple[Fraction, Fraction]]:
    """Power distance from x(t) = a + t (b - a) to each site, minus the common term |b - a|^2 t^2."""
    d = sub(b, a)
    out = []
    for s, w in sites:
        e = sub(a, s)
        out.append((Fraction(2 * dot(d, e)), Fraction(dot(e, e) - w)))
    return out


def restricted_pairs(a: Point, b: Point, sites: Sequence[Tuple[Point, Fraction]]) -> Set[Tuple[int, int]]:
    """Pairs {i, j} of sites whose power cells share a point of the segment ab (lower envelope, exact)."""
    lines = _lines(a, b, sites)
    groups: Dict[Tuple[Fraction, Fraction], List[int]] = {}
    for i, ln in enumerate(lines):
        groups.setdefault(ln, []).append(i)
    # lower envelope of the distinct lines: slopes decreasing, keep the lowest intercept per slope
    best: Dict[Fraction, Fraction] = {}
    for m, q in groups:
        if m not in best or q < best[m]:
            best[m] = q
    order = sorted(best.items(), key=lambda mq: -mq[0])

    def meet(l1, l2) -> Fraction:
        return (l2[1] - l1[1]) / (l1[0] - l2[0])

    hull: List[Tuple[Fraction, Fraction]] = []
    for ln in order:
        while len(hull) >= 2 and meet(hull[-2], ln) < meet(hull[-2], hull[-1]):
            hull.pop()
        hull.append(ln)
    # interval of t where each hull line is minimal, clipped to [0, 1]
    iv = []
    for k, ln in enumerate(hull):
        lo = meet(hull[k - 1], ln) if k > 0 else None
        hi = meet(ln, hull[k + 1]) if k + 1 < len(hull) else None
        lo2 = Fraction(0) if lo is None else max(lo, Fraction(0))
        hi2 = Fraction(1) if hi is None else min(hi, Fraction(1))
        if lo2 <= hi2:
            iv.append((lo2, hi2, groups[ln]))
    out = set()
    for x in range(len(iv)):
        for i in iv[x][2]:
            for j in iv[x][2]:
                if i < j:
                    out.add((i, j))
        for y in range(x + 1, len(iv)):
            if max(iv[x][0], iv[y][0]) <= min(iv[x][1], iv[y][1]):
                for i in iv[x][2]:
                    for j in iv[y][2]:
                        out.add((min(i, j), max(i, j)))
    return out


def restricted_pairs_brute(a: Point, b: Point, sites: Sequence[Tuple[Point, Fraction]]) -> Set[Tuple[int, int]]:
    """Same as restricted_pairs, from the definition: the set where site i is nearest is an interval."""
    lines = _lines(a, b, sites)
    ivs = []
    for i, (mi, qi) in enumerate(lines):
        lo, hi = Fraction(0), Fraction(1)
        for j, (mj, qj) in enumerate(lines):
            if j == i:
                continue
            # need mi t + qi <= mj t + qj, that is (mi - mj) t <= qj - qi
            k, rhs = mi - mj, qj - qi
            if k == 0:
                if rhs < 0:
                    lo, hi = Fraction(1), Fraction(0)
            elif k > 0:
                hi = min(hi, rhs / k)
            else:
                lo = max(lo, rhs / k)
        ivs.append((lo, hi))
    out = set()
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            lo = max(ivs[i][0], ivs[j][0])
            hi = min(ivs[i][1], ivs[j][1])
            if lo <= hi:
                out.add((i, j))
    return out


def nearest_power(x: Point, sites: Sequence[Tuple[Point, Fraction]]) -> Tuple[Fraction, List[int]]:
    """The smallest power distance from x to the sites, and every site that attains it."""
    best, arg = None, []
    for i, (s, w) in enumerate(sites):
        p = dist2(x, s) - w
        if best is None or p < best:
            best, arg = p, [i]
        elif p == best:
            arg.append(i)
    return best, arg
