# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delaunay-surface-meshing/. The authors are listed in prov/8F2351.jsonl.

import math
import random
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations

import pytest

from delaunay_surface_meshing import (
    GHOST,
    Mesher,
    Sphere,
    Torus,
    count_roots,
    delaunay_surface_mesh,
    faces_of,
    peval,
    pmul,
    roots_in,
    sturm,
)
from mg2geom import cross, dist2, dot, insphere, orient3d, sub

R = 1 << 20
SPHERE = Sphere(R)
TORUS = Torus(3 << 18, 1 << 18)  # lfs = r = 2^18 everywhere
LFS = {"sphere": R, "torus": 1 << 18}
SURF = {"sphere": SPHERE, "torus": TORUS}
CASES = [("sphere", F(1, 2), 1), ("torus", F(3, 2), 1), ("sphere", F(3, 10), 2)]
ROUND = math.sqrt(3) / 2  # rounding to the grid moves a point at most this far
# a computed center is within 1/8 of the exact point of S on the Voronoi edge, then rounded


@lru_cache(maxsize=None)
def run(kind, eps, seed):
    return delaunay_surface_mesh(SURF[kind], float(eps * LFS[kind]), seed=seed)


def edge_count(T):
    E = Counter()
    for f in T:
        for e in combinations(f, 2):
            E[e] += 1
    return E


def brute_restricted(S, pts):
    """Restricted Delaunay triangles straight from the definition: abc is one if some
    point of S has a, b, c among its nearest sample points (an empty ball centered on S)."""
    out = set()
    n = len(pts)
    for i, j, k in combinations(range(n), 3):
        a, b, c = pts[i], pts[j], pts[k]
        u, v = sub(b, a), sub(c, a)
        nn = cross(u, v)
        W = 2 * dot(nn, nn)
        if W == 0:
            continue
        # the points equidistant from a, b, c: (N + s W nn) / W
        N = tuple(W * a[t] + dot(u, u) * cross(v, nn)[t] + dot(v, v) * cross(nn, u)[t] for t in range(3))
        cf = [x / W for x in N]
        others = sorted((p for q, p in enumerate(pts) if q not in (i, j, k)), key=lambda p: math.dist(p, cf))
        lo, hi, empty = None, None, False  # bounds on s as (numerator, positive denominator)
        aa = dot(a, a)
        for p in others:
            # |x - p|^2 >= |x - a|^2  <=>  alpha + s beta >= 0
            d = sub(a, p)
            alpha = 2 * dot(d, N) + W * (dot(p, p) - aa)
            beta = 2 * W * dot(d, nn)
            if beta == 0:
                empty = alpha < 0
            elif beta > 0:  # s >= -alpha / beta
                if lo is None or -alpha * lo[1] > lo[0] * beta:
                    lo = (-alpha, beta)
            else:  # s <= alpha / -beta
                if hi is None or alpha * hi[1] < hi[0] * -beta:
                    hi = (alpha, -beta)
            if empty or (lo is not None and hi is not None and lo[0] * hi[1] > hi[0] * lo[1]):
                empty = True
                break
        if empty:
            continue
        G = S.poly(N, tuple(W * x for x in nn), W)
        lo = "-" if lo is None else F(*lo)
        hi = None if hi is None else F(*hi)
        if roots_in(G, lo, hi, F(1, 1 << 30)):
            out.add((i, j, k))
    return out


# the exact tools


def test_sturm_counts_and_locates_roots():
    rng = random.Random(5)
    for _ in range(40):
        roots = sorted({F(rng.randint(-40, 40), rng.randint(1, 6)) for _ in range(rng.randint(1, 4))})
        p = [1]
        for x in roots:
            p = pmul(p, [-x.numerator, x.denominator])
        if rng.random() < 0.3:
            p = pmul(p, [1, 0, 1])  # s^2 + 1 adds no real root
        if rng.random() < 0.3:
            p = pmul(p, [-roots[0].numerator, roots[0].denominator])  # a double root counts once
        seq = sturm(p)
        lo, hi = F(rng.randint(-50, 0)), F(rng.randint(0, 50))
        a, b = lo + F(1, 1000), hi + F(1, 1000)  # not roots, so the count is exact even for p
        assert count_roots(seq, a, b) == sum(1 for x in roots if a < x <= b)
        got = roots_in(p, lo, hi, F(1, 1000))
        want = [x for x in roots if lo <= x <= hi]
        assert len(got) == len(want)
        assert all(abs(g - w) <= F(1, 1000) for g, w in zip(got, want))
        assert len(roots_in(p, "-", None, F(1, 1000))) == len(roots)


def test_surface_polynomial_is_the_implicit_function_on_the_line():
    rng = random.Random(6)
    for S, deg in ((SPHERE, 2), (TORUS, 4)):
        for _ in range(20):
            A = tuple(rng.randint(-(1 << 30), 1 << 30) for _ in range(3))
            B = tuple(rng.randint(-(1 << 30), 1 << 30) for _ in range(3))
            W = rng.randint(1, 1 << 10)
            s = F(rng.randint(-100, 100), rng.randint(1, 100))
            x = [(A[k] + s * B[k]) / W for k in range(3)]
            if S is SPHERE:
                val = sum(c * c for c in x) - R * R
            else:
                q = sum(c * c for c in x) + S.R ** 2 - S.r ** 2
                val = q * q - 4 * S.R ** 2 * (x[0] ** 2 + x[1] ** 2)
            assert peval(S.poly(A, B, W), s) == val * W ** deg


# the output


@pytest.mark.parametrize("case", CASES)
def test_every_vertex_lies_on_the_surface(case):
    m = run(*case)
    S = SURF[case[0]]
    assert max(S.distance(p) for p in m.pts) <= ROUND + 1 / 8


@pytest.mark.parametrize("case", CASES[:2] + [("torus", F(2), 1)])
def test_restricted_triangles_match_brute_force(case):
    m = run(*case)
    want = brute_restricted(SURF[case[0]], m.pts)
    assert m.restricted() == want


@pytest.mark.parametrize("case", CASES[:2] + [("torus", F(2), 1)])
def test_the_triangulation_is_delaunay(case):
    m = run(*case)
    n = len(m.pts)
    real = [t for t in m.tets if t[0] != GHOST]
    for t in real:
        P = [m.pts[v] for v in t]
        assert orient3d(*P) != 0
        assert all(insphere(*P, m.pts[q]) < 0 for q in range(n) if q not in t)
    for f, ts in m.face_tets.items():
        assert len(ts) == 2
    hull = [t[1:] for t in m.tets if t[0] == GHOST]
    for f in hull:  # every point is on the inner side of every hull face
        P = [m.pts[v] for v in f]
        sides = {(orient3d(*P, m.pts[q]) > 0) for q in range(n) if q not in f}
        assert len(sides) == 1
    used = {v for t in m.tets for v in t if v != GHOST}
    assert used == set(range(n))


@pytest.mark.parametrize("case", CASES)
def test_incremental_update_equals_a_fresh_computation(case):
    m = run(*case)
    fresh = {}
    for f in m.face_tets:
        if GHOST not in f:
            b = m.surface_balls(f)
            if b:
                fresh[f] = b
    assert fresh == m.balls


@pytest.mark.parametrize("case", CASES)
def test_no_bad_ball_is_left(case):
    """At the end every surface Delaunay ball B(c, r) has r <= sigma(c), which with
    sigma = eps lfs is Condition 1 of a loose eps-sample (Lemma 8.2)."""
    m = run(*case)
    kind, eps, _ = case
    assert m.balls
    for f, balls in m.balls.items():
        for c, r, sg in balls:
            assert r <= sg == float(eps * LFS[kind])
            assert SURF[kind].distance(c) <= ROUND + 1 / 8


@pytest.mark.parametrize("case", CASES)
def test_output_is_a_closed_two_manifold_of_the_right_genus(case):
    m = run(*case)
    T = m.restricted()
    E = edge_count(T)
    assert set(E.values()) == {2}
    V = {v for f in T for v in f}
    assert V == set(range(len(m.pts)))
    link = defaultdict(list)
    for f in T:
        for v in f:
            link[v].append(tuple(x for x in f if x != v))
    for v, edges in link.items():  # the link of every vertex is one cycle
        adj = defaultdict(list)
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        assert all(len(x) == 2 for x in adj.values())
        seen, stack = {edges[0][0]}, [edges[0][0]]
        while stack:
            for y in adj[stack.pop()]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        assert len(seen) == len(adj)
    assert len(V) - len(E) + len(T) == SURF[case[0]].euler
    # connected and orientable: orient one triangle and propagate across edges
    orient = {}
    first = min(T)
    orient[first] = first
    stack = [first]
    by_edge = defaultdict(list)
    for f in T:
        for e in combinations(f, 2):
            by_edge[e].append(f)
    while stack:
        f = stack.pop()
        o = orient[f]
        for i in range(3):
            a, b = o[i], o[(i + 1) % 3]
            for g in by_edge[tuple(sorted((a, b)))]:
                if g == f:
                    continue
                c = next(x for x in g if x not in (a, b))
                want = (b, a, c)
                if g in orient:
                    assert set(zip(orient[g], orient[g][1:] + orient[g][:1])) >= {(b, a)}
                else:
                    orient[g] = want
                    stack.append(g)
    assert len(orient) == len(T)


@pytest.mark.parametrize("case", CASES)
def test_persistent_facets_stay(case):
    """Section 7: each initial triple has a surface Delaunay ball of radius at most sigma / 3,
    and Lemma 7.1: it is still a restricted triangle at the end."""
    kind, eps, seed = case
    m0 = Mesher(SURF[kind], float(eps * LFS[kind]), seed)
    init = m0.initial_sample()
    m0._start(init)
    m0.update_faces(list(m0.face_tets))
    pers = [tuple(sorted(m0.pts.index(q) for q in init[i : i + 3])) for i in range(0, len(init), 3)]
    for f in pers:
        assert any(r + ROUND <= sg / 3 for c, r, sg in m0.balls[f])
    m = run(*case)
    assert m.persistent == pers
    assert all(f in m.restricted() for f in m.persistent)


@pytest.mark.parametrize("case", CASES)
def test_inserted_points_are_far_apart(case):
    """Lemma 8.1: a point is inserted at distance r > sigma(c) from the sample (less rounding)."""
    m = run(*case)
    k = len(m.pts) - len(m.log)
    for i, (c, r, sg) in enumerate(m.log):
        assert m.pts[k + i] == c and r > sg
        d = min(math.sqrt(dist2(c, m.pts[j])) for j in range(k + i))
        assert d >= r - ROUND


def test_example_sphere():
    m = run("sphere", F(1, 2), 1)
    assert len(m.pts) == 41 and len(m.log) == 29 and len(m.restricted()) == 78
    ratios = [round(r / sg, 3) for c, r, sg in m.log]
    assert ratios[0] == 2.256 and ratios[4] == 1.793 and ratios[10] == 1.233 and ratios[-1] == 1.0
    assert all(x >= y - 0.01 for x, y in zip(ratios, ratios[1:]))  # the worst ratio falls, nearly monotone
    m0 = Mesher(SPHERE, R / 2, 1)
    m0._start(m0.initial_sample())
    m0.update_faces(list(m0.face_tets))
    r0 = sorted(round(r / sg, 3) for f in m0.balls for c, r, sg in m0.balls[f])
    assert len(m0.pts) == 12 and len(m0.balls) == 20
    assert r0[:4] == [0.082] * 4 and r0[4] > 1 and r0[-1] == 2.256
    # replay the loop: (points, restricted triangles, bad balls) before each insertion
    trace = []
    while True:
        bad = sum(1 for f in m0.balls for c, r, sg in m0.balls[f] if r > sg)
        trace.append((len(m0.pts), len(m0.balls), bad))
        w = m0.worst_ball()
        if w is None:
            break
        old = set(m0.tets)
        m0.insert(w[2], sorted(m0.face_tets[w[1]]))
        m0.update_faces(sorted({g for t in old ^ m0.tets for g in faces_of(t)}))
    assert [trace[k] for k in (0, 4, 10, 22, 28, 29)] == [
        (12, 20, 16),
        (16, 28, 24),
        (22, 40, 27),
        (34, 64, 11),
        (40, 76, 1),
        (41, 78, 0),
    ]
    assert all(t == 2 * p - 4 for p, t, _ in trace)  # a triangulated sphere at every step
    assert m0.pts == m.pts


def test_measured_versus_proved():
    """The guarantee needs sigma < 0.091 lfs. Measured: the torus comes out right at
    sigma = 1.5 lfs, 16 times the proved threshold, but not at 2 lfs, and the sizes
    stay below mu(S) / eps^2."""
    good = run("torus", F(3, 2), 1)
    assert len(good.pts) == 40 and set(edge_count(good.restricted()).values()) == {2}
    bad = run("torus", F(2), 1)
    assert len(bad.pts) == 20
    E = edge_count(bad.restricted())
    assert set(E.values()) != {2}
    V = {v for f in bad.restricted() for v in f}
    assert len(V) - len(E) + len(bad.restricted()) == 6
    mu = 4 * math.pi  # mu(S) = area / lfs^2 for the unit sphere
    for eps, seed in ((F(1, 2), 1), (F(3, 10), 2)):
        assert len(run("sphere", eps, seed).pts) < mu / float(eps) ** 2


def test_bad_input():
    with pytest.raises(ValueError):
        Sphere(0)
    with pytest.raises(ValueError):
        Torus(5, 3)
    with pytest.raises(RuntimeError):
        delaunay_surface_mesh(SPHERE, R / 5, seed=1, max_vertices=30)
