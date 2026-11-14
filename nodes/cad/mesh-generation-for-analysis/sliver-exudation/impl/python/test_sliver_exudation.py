# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliver-exudation/. The authors are listed in prov/4WRSY6.jsonl.

import math
import random
from fractions import Fraction as F
from functools import lru_cache

import pytest

from mg2geom import circumcenter3, dihedral_angles_deg, dist2, insphere, orient3d, sub
from sliver_exudation import OMEGA, Exuder, critical_weight, faces_of, min_dihedral, power_test, sliver_exudation

S = 1000


def jittered_grid(seed, g, jit):
    """g^3 points near the grid points (i, j, k) * S, each coordinate moved by at most jit."""
    r = random.Random(seed)
    return [
        (i * S + r.randint(-jit, jit), j * S + r.randint(-jit, jit), k * S + r.randint(-jit, jit))
        for i in range(1, g + 1)
        for j in range(1, g + 1)
        for k in range(1, g + 1)
    ]


EXAMPLE = (2, 3, 100)  # seed, g, jitter: 27 inner points in a box of side 4000
OTHER = (1, 3, 150)


@lru_cache(maxsize=None)
def pumped(case):
    """Run the pumps one at a time and record the global minimum dihedral angle after each."""
    seed, g, jit = case
    e = Exuder((g + 1) * S, jittered_grid(seed, g, jit))
    before = (frozenset(e.tets), min_dihedral(e.pts, e.tets))
    mins = [before[1]]
    for u in range(8, len(e.pts)):
        e.pump(u)
        mins.append(min_dihedral(e.pts, e.tets))
    return e, before, mins


# brute-force orthosphere: center z and squared radius Z2 with |p - z|^2 - Z2 = w_p for the four points
def orthosphere(pts, ws):
    a, wa = pts[0], ws[0]
    rows, rhs = [], []
    for p, w in zip(pts[1:], ws[1:]):
        rows.append([F(2 * (p[k] - a[k])) for k in range(3)])
        rhs.append(F(sum(p[k] ** 2 - a[k] ** 2 for k in range(3)) - w + wa))
    # Gaussian elimination in exact arithmetic
    m = [rows[i] + [rhs[i]] for i in range(3)]
    for c in range(3):
        piv = next(i for i in range(c, 3) if m[i][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for i in range(3):
            if i != c and m[i][c] != 0:
                f = m[i][c] / m[c][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[c])]
    z = tuple(m[i][3] / m[i][i] for i in range(3))
    return z, dist2(a, z) - wa


def random_weighted(r, n):
    pts = [tuple(r.randint(-20, 20) for _ in range(3)) for _ in range(n)]
    ws = [r.randint(0, 60) for _ in range(n)]
    return pts, ws


def test_power_test_matches_brute_force_orthosphere():
    r = random.Random(7)
    checked = signs = 0
    while checked < 300:
        pts, ws = random_weighted(r, 5)
        if orient3d(*pts[:4]) == 0:
            continue
        z, Z2 = orthosphere(pts[:4], ws[:4])
        pi = dist2(pts[4], z) - Z2 - ws[4]
        val = power_test(*pts, *ws)
        assert (val > 0) == (pi < 0) and (val == 0) == (pi == 0)
        assert val == -pi * abs(orient3d(*pts[:4]))
        assert critical_weight(*pts, *ws[:4]) == dist2(pts[4], z) - Z2
        # the order of the four points does not matter
        perm = [1, 0, 2, 3]
        assert power_test(*[pts[i] for i in perm], pts[4], *[ws[i] for i in perm], ws[4]) == val
        checked += 1
        signs += val > 0
    assert 0 < signs < 300


def test_power_test_with_zero_weights_is_insphere():
    r = random.Random(8)
    n = 0
    while n < 200:
        pts = [tuple(r.randint(-9, 9) for _ in range(3)) for _ in range(5)]
        if orient3d(*pts[:4]) == 0:
            continue
        assert power_test(*pts) == insphere(*pts)
        n += 1


def test_power_test_on_a_cube():
    c = [(x, y, z) for x in (0, 2) for y in (0, 2) for z in (0, 2)]
    t = (c[0], c[1], c[2], c[4])
    assert power_test(*t, (1, 1, 1)) > 0  # the center of the circumsphere
    assert power_test(*t, c[7]) == 0  # cospherical
    assert power_test(*t, (1, 1, 1), we=0) > 0
    # a center weight equal to its power distance makes it orthogonal: zero; more is a conflict, less is not
    pi = critical_weight(*t, (1, 1, 1))
    assert pi == dist2((1, 1, 1), (1, 1, 1)) - 3 == -3
    assert power_test(*t, (1, 1, 1), we=-3) == 0
    assert power_test(*t, (1, 1, 1), we=-4) < 0
    # (1, 1, 3) lies outside the circumsphere, power 4 - 3 = 1: a weight above 1 makes it conflict
    assert critical_weight(*t, (1, 1, 3)) == 1
    assert power_test(*t, (1, 1, 3)) < 0
    assert power_test(*t, (1, 1, 3), we=1) == 0
    assert power_test(*t, (1, 1, 3), we=2) > 0
    # a weight on the corner (0, 0, 2) pulls the orthosphere away from it, so (1, 1, 3) needs a larger weight
    assert critical_weight(*t, (1, 1, 3), 0, 4, 0, 0) > 1
    assert power_test(*t, (1, 1, 3), 0, 4, 0, 0, we=2) < 0


def test_flat_tetrahedron_raises():
    with pytest.raises(ValueError):
        power_test((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1))


def check_regular(e):
    """Every tetrahedron has positive volume and no weighted point conflicts with it."""
    P, W = e.pts, e.w
    vol = 0
    for t in e.tets:
        o = orient3d(*[P[x] for x in t])
        assert o > 0
        vol += o
        for v in range(len(P)):
            if v not in t:
                assert power_test(*[P[x] for x in t], P[v], *[W[x] for x in t], W[v]) <= 0
    assert vol == 6 * e.side**3
    # every point is a vertex, and every face is shared by two tetrahedra or lies on the box
    assert {v for t in e.tets for v in t} == set(range(len(P)))
    count = {}
    for t in e.tets:
        for f in faces_of(t):
            count[f] = count.get(f, 0) + 1
    for f, m in count.items():
        if m == 1:
            assert any(all(P[v][k] in (0, e.side) and P[v][k] == P[f[0]][k] for v in f) for k in range(3))
        else:
            assert m == 2


@pytest.mark.parametrize("case", [EXAMPLE, OTHER])
def test_initial_triangulation_is_delaunay(case):
    seed, g, jit = case
    e = Exuder((g + 1) * S, jittered_grid(seed, g, jit))
    assert all(w == 0 for w in e.w)
    check_regular(e)


@pytest.mark.parametrize("case", [EXAMPLE, OTHER])
def test_final_triangulation_is_regular_and_unique(case):
    e, _, _ = pumped(case)
    check_regular(e)
    fresh = e.triangulate(range(len(e.pts)))
    assert {tuple(sorted(t)) for t in fresh} == {tuple(sorted(t)) for t in e.tets}


@pytest.mark.parametrize("case", [EXAMPLE, OTHER])
def test_weight_property(case):
    e, _, _ = pumped(case)
    P = e.pts
    for u in range(len(P)):
        assert e.w[u] >= 0
        for v in range(len(P)):
            if v != u:
                # U <= OMEGA |uv|, so the spheres of radius sqrt(w) are disjoint
                assert e.w[u] <= OMEGA**2 * dist2(P[u], P[v])
                assert math.sqrt(e.w[u]) + math.sqrt(e.w[v]) < math.sqrt(dist2(P[u], P[v]))
    assert all(e.w[u] == 0 for u in range(8))


@pytest.mark.parametrize("case", [EXAMPLE, OTHER])
def test_minimum_dihedral_never_decreases(case):
    e, before, mins = pumped(case)
    assert len(e.log) == len(e.pts) - 8
    for u, w, wmax, ncand, zeta0, best in e.log:
        assert 0 <= w <= wmax and ncand >= 1
        assert best >= zeta0
    for a, b in zip(mins, mins[1:]):
        assert b >= a
    assert mins[-1] > mins[0]


def test_star_matches_fresh_triangulation():
    """The star computed from critical weights equals Bowyer-Watson from scratch with that weight."""
    r = random.Random(3)
    e = Exuder(3 * S, jittered_grid(5, 2, 150))
    P = e.pts
    for u in range(8, len(P)):
        rest = e.triangulate([v for v in range(len(P)) if v != u])
        crit = {t: critical_weight(*[P[x] for x in t], P[u], *[e.w[x] for x in t]) for t in rest}
        wmax = math.floor(OMEGA**2 * e.nearest2(u))
        for w in [0, wmax] + [r.randint(0, wmax) for _ in range(4)]:
            if w in crit.values():
                continue
            cavity, cone = e.star(rest, crit, u, w)
            e.w[u] = w
            fresh = e.triangulate(range(len(P)))
            e.w[u] = 0
            assert {tuple(sorted(t)) for t in (rest - cavity) | set(cone)} == {tuple(sorted(t)) for t in fresh}
        e.pump(u)


@pytest.mark.parametrize("u", [9, 18, 21, 26, 30])
def test_pump_finds_the_best_star(u):
    """Brute force: try the midpoint of every interval between critical weights, and many integers."""
    e = Exuder(4 * S, jittered_grid(*EXAMPLE))
    P = e.pts
    rest = e.triangulate([v for v in range(len(P)) if v != u])
    crit = {t: critical_weight(*[P[x] for x in t], P[u]) for t in rest}
    wmax = math.floor(OMEGA**2 * e.nearest2(u))
    cuts = sorted({c for c in crit.values() if 0 < c < wmax})
    trial = [F(0)] + [(lo + hi) / 2 for lo, hi in zip([F(0)] + cuts, cuts + [F(wmax)])]
    trial += [F(w) for w in range(1, wmax + 1, 499)]
    best = max(min_dihedral(P, e.star(rest, crit, u, w)[1]) for w in trial if w not in crit.values())
    e.pump(u)
    # the current weight 0, and at most one integer in each of the len(cuts) + 1 intervals
    assert e.log[-1][3] <= len(cuts) + 2
    assert e.log[-1][5] == pytest.approx(best, abs=1e-9)


def test_example_numbers():
    e, before, mins = pumped(EXAMPLE)
    P = e.pts
    tets0, min0 = before
    lo0 = [min(dihedral_angles_deg(*[P[v] for v in t])) for t in tets0]
    lo1 = [min(dihedral_angles_deg(*[P[v] for v in t])) for t in e.tets]
    assert (len(tets0), len(e.tets)) == (151, 139)
    assert round(min0, 2) == 0.14 and round(mins[-1], 2) == 5.20
    assert (sum(a < 5 for a in lo0), sum(a < 5 for a in lo1)) == (9, 0)
    assert (sum(a < 10 for a in lo0), sum(a < 10 for a in lo1)) == (17, 6)
    assert sum(1 for w in e.w if w) == 11
    # the worst sliver: four vertices near the face x = 3000, angles 0.14 and 179.78 degrees
    worst = min(tets0, key=lambda t: min(dihedral_angles_deg(*[P[v] for v in t])))
    assert sorted(worst) == [26, 27, 29, 30]
    ang = dihedral_angles_deg(*[P[v] for v in worst])
    assert round(max(ang), 2) == 179.78
    # its radius-edge ratio is small: the ratio does not see it
    cc = circumcenter3(*[P[v] for v in worst])
    lmin = min(dist2(P[a], P[b]) for a in worst for b in worst if a < b)
    assert dist2(cc, P[worst[0]]) / lmin < 9
    # the pump of vertex 26 removes it
    row = next(x for x in e.log if x[0] == 26)
    assert row[1] == 44845 and round(row[4], 2) == 0.14 and round(row[5], 2) == 5.47
    # the global minimum rises at the pumps of 26 and 30 only
    assert [i + 8 for i in range(len(mins) - 1) if mins[i + 1] > mins[i]] == [26, 30]


def test_second_example_worst_touches_a_corner():
    e, _, mins = pumped(OTHER)
    assert round(mins[0], 2) == 1.54 and round(mins[-1], 2) == 3.03
    worst = min(e.tets, key=lambda t: min(dihedral_angles_deg(*[e.pts[v] for v in t])))
    assert min(worst) < 8


def test_dihedral_lower_bound_from_volume_and_edge_ratio():
    """sin(theta) >= 8 Sigma / lambda^4 with Sigma = V / L^3 and lambda = D / L, on every tetrahedron."""
    for case in (EXAMPLE, OTHER):
        e, before, _ = pumped(case)
        P = e.pts
        for t in set(before[0]) | e.tets:
            q = [P[v] for v in t]
            V = F(abs(orient3d(*q)), 6)
            e2 = [dist2(q[a], q[b]) for a in range(4) for b in range(a + 1, 4)]
            L, D = math.sqrt(min(e2)), math.sqrt(max(e2))
            bound = 8 * float(V) * L / D**4  # 8 (V / L^3) / (D / L)^4
            theta = min(dihedral_angles_deg(*q))
            assert math.sin(math.radians(theta)) >= bound * (1 - 1e-9)


@pytest.mark.parametrize("case", [EXAMPLE, OTHER])
def test_longest_edge_bounded_by_orthoradius(case):
    """With the Weight Property, D^2 (1 - 4 OMEGA^2) <= 4 Z^2 for every tetrahedron of the output."""
    e, _, _ = pumped(case)
    P, W = e.pts, e.w
    for t in e.tets:
        q, ws = [P[v] for v in t], [W[v] for v in t]
        z, Z2 = orthosphere(q, ws)
        assert Z2 > 0
        for p, w in zip(q, ws):
            assert dist2(p, z) - Z2 == w
        D2 = max(dist2(q[a], q[b]) for a in range(4) for b in range(a + 1, 4))
        assert D2 * (1 - 4 * OMEGA**2) <= 4 * Z2


def test_entry_point_and_bad_input():
    e = sliver_exudation(2 * S, [(1000, 1000, 1000)])
    assert len(e.tets) == 12 and e.w[8] <= OMEGA**2 * 3 * 10**6
    check_regular(e)
    with pytest.raises(ValueError):
        Exuder(0, [])
    with pytest.raises(ValueError):
        Exuder(10, [(5, 5, 5)], omega=F(1, 2))
    with pytest.raises(ValueError):
        Exuder(10, [(5, 5, 5), (5, 5, 5)])
    with pytest.raises(ValueError):
        Exuder(10, [(0, 5, 5)])
    with pytest.raises(ValueError):
        Exuder(10, [(5, 5, 11)])
