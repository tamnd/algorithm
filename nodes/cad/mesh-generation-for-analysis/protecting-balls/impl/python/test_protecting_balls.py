# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/protecting-balls/. The authors are listed in prov/EADV10.jsonl.

import math
import random
from fractions import Fraction as F
from itertools import combinations

import pytest

from protecting_balls import (
    Ball,
    Protection,
    _fsegseg,
    _sin_min_angle,
    check_complex,
    dist2,
    nearest_power,
    point_seg_dist2,
    protect,
    restricted_pairs,
    restricted_pairs_brute,
    seg_seg_dist2,
    sub,
    violations,
)

# a triangle with a 10 degree angle at O, and a segment OC at right angles to it
P = [(0, 0, 0), (1000, 0, 0), (985, 174, 0), (0, 0, 1000)]
S = [(0, 1), (0, 2), (1, 2), (0, 3)]


@pytest.fixture(scope="module")
def example():
    return protect(P, S)


def chain_pairs(prot, e):
    ch = prot.chains[e]
    return {(min(i, j), max(i, j)) for i, j in zip(ch, ch[1:])}


def rand_complex(rng, nv=5, ne=6, span=1000, far=150):
    while True:
        pts = [tuple(rng.randint(-span, span) for _ in range(3)) for _ in range(nv)]
        segs = set()
        while len(segs) < ne:
            i, j = rng.sample(range(nv), 2)
            segs.add((min(i, j), max(i, j)))
        segs = sorted(segs)
        if len({x for s in segs for x in s}) < nv:
            continue
        try:
            check_complex(pts, segs)
        except ValueError:
            continue
        if all(
            seg_seg_dist2(pts[a], pts[b], pts[p], pts[q]) >= far * far
            for k, (a, b) in enumerate(segs)
            for (p, q) in segs[k + 1 :]
            if not {a, b} & {p, q}
        ):
            return pts, segs


def admissible_points(rng, prot, k, lo=-100, hi=1100):
    out = []
    while len(out) < k:
        x = tuple(rng.randint(lo, hi) for _ in range(3))
        if all(dist2(x, b.center) >= b.r**2 for b in prot.balls):
            out.append((x, F(0)))
    return out


def near_curve_points(rng, prot, k):
    """Unweighted points just outside the balls, next to the pieces of the chains."""
    out = []
    pieces = [(p, q) for ch in prot.chains for p, q in zip(ch, ch[1:])]
    while len(out) < k:
        p, q = rng.choice(pieces)
        a, b = prot.balls[p].center, prot.balls[q].center
        t = F(rng.randint(1, 99), 100)
        m = tuple(x + t * (y - x) for x, y in zip(a, b))
        off = tuple(F(rng.randint(-40, 40)) for _ in range(3))
        x = tuple(mi + oi for mi, oi in zip(m, off))
        if all(dist2(x, bb.center) >= bb.r**2 for bb in prot.balls):
            out.append((x, F(0)))
    return out


# --- exact geometry -----------------------------------------------------------


def test_seg_seg_distance_against_sampling():
    rng = random.Random(1)
    for _ in range(40):
        a, b, c, d = (tuple(rng.randint(-20, 20) for _ in range(3)) for _ in range(4))
        exact = float(seg_seg_dist2(a, b, c, d))
        best = min(
            dist2(tuple(x + i / 40 * (y - x) for x, y in zip(a, b)), tuple(x + j / 40 * (y - x) for x, y in zip(c, d)))
            for i in range(41)
            for j in range(41)
        )
        assert exact <= best + 1e-9
        assert math.sqrt(best) - math.sqrt(exact) <= 2.0


def test_point_seg_distance():
    assert point_seg_dist2((0, 5, 0), (-3, 0, 0), (3, 0, 0)) == 25
    assert point_seg_dist2((7, 0, 0), (-3, 0, 0), (3, 0, 0)) == 16
    assert point_seg_dist2((1, 1, 1), (0, 0, 0), (2, 2, 0)) == 1


# --- the restricted pairs on a segment -------------------------------------------


def test_restricted_pairs_matches_brute_force():
    rng = random.Random(2)
    for trial in range(150):
        a = tuple(rng.randint(-50, 50) for _ in range(3))
        b = tuple(rng.randint(-50, 50) for _ in range(3))
        if a == b:
            continue
        sites = []
        for _ in range(rng.randint(1, 12)):
            s = tuple(rng.randint(-60, 60) for _ in range(3))
            w = F(rng.choice([0, 0, rng.randint(0, 900)]))
            sites.append((s, w))
        # degenerate inputs: a site mirrored across the line has the same power
        # function along it, and a repeated site ties everywhere
        if trial % 3 == 0 and sites:
            s, w = sites[0]
            d = sub(b, a)
            e = sub(s, a)
            t = F(sum(x * y for x, y in zip(e, d)), sum(x * x for x in d))
            foot = tuple(ai + t * di for ai, di in zip(a, d))
            sites.append((tuple(2 * f - x for f, x in zip(foot, s)), w))
        if trial % 5 == 0 and sites:
            sites.append(sites[-1])
        assert restricted_pairs(a, b, sites) == restricted_pairs_brute(a, b, sites)


def test_restricted_pairs_three_way_tie():
    # three unweighted sites equidistant from the midpoint (5, 0, 0) of the segment
    a, b = (0, 0, 0), (10, 0, 0)
    sites = [((0, 0, 0), F(0)), ((10, 0, 0), F(0)), ((5, 5, 0), F(0))]
    got = restricted_pairs(a, b, sites)
    assert got == restricted_pairs_brute(a, b, sites) == {(0, 1), (0, 2), (1, 2)}


# --- the protection -------------------------------------------------------------------


def test_example(example):
    prot = example
    assert violations(prot) == []
    assert [len(ch) - 2 for ch in prot.chains] == [38, 38, 9, 9]
    assert [float(b.r) for b in prot.balls[:4]] == pytest.approx([125.0, 21.8307, 21.8307, 125.0], abs=1e-3)
    ch = prot.chains[0]
    radii = [float(prot.balls[i].r) for i in ch[1:-1]]
    assert radii[0] == pytest.approx(5.56, abs=0.01)
    assert max(radii) == pytest.approx(35.34, abs=0.01)
    # near the 10 degree corner the radii grow by about 6 percent per ball
    assert radii[1] / radii[0] == pytest.approx(1.0615, abs=1e-3)
    # on OC, at right angles to everything, they grow by about a third
    oc = [float(prot.balls[i].r) for i in prot.chains[3][1:-1]]
    assert oc[1] / oc[0] == pytest.approx(1.324, abs=1e-3)
    for e, (u, v) in enumerate(S):
        assert prot.chains[e][0] == u and prot.chains[e][-1] == v
        for i in prot.chains[e][1:-1]:
            assert prot.balls[i].seg == e


def test_centers_lie_on_their_segments(example):
    for e, (u, v) in enumerate(S):
        for i in example.chains[e]:
            assert point_seg_dist2(example.balls[i].center, P[u], P[v]) == 0


def test_random_complexes_pass_the_exact_check():
    rng = random.Random(3)
    for c in (0.3, 0.45):
        pts, segs = rand_complex(rng, nv=4, ne=5)
        prot = protect(pts, segs, c)  # raises if the exact check fails
        assert violations(prot) == []


def test_violations_detects_each_property(example):
    balls = [Ball(b.center, b.r, b.vertex, b.seg) for b in example.balls]
    ch = example.chains[3]
    i, j = ch[2], ch[3]
    # (a): shrink two neighbors until they no longer overlap
    small = list(balls)
    small[i] = Ball(balls[i].center, balls[i].r / 4, seg=3)
    small[j] = Ball(balls[j].center, balls[j].r / 4, seg=3)
    kinds = {v[0] for v in violations(Protection(P, S, 0.25, small, example.chains))}
    assert "a" in kinds
    # (b) and (c): grow one ball over its neighbor's neighbor
    big = list(balls)
    big[i] = Ball(balls[i].center, balls[i].r * 3, seg=3)
    kinds = {v[0] for v in violations(Protection(P, S, 0.25, big, example.chains))}
    assert {"a", "b", "c"} <= kinds


def test_c_below_one_half_is_needed_for_the_check():
    # two balls on OA and OB at the same distance from O are
    # 2 sin(5 degrees) s apart, and both have radius about c sin(10 degrees) s
    assert violations(protect(P, S, 0.5, check=False)) == []
    with pytest.raises(ValueError):
        protect(P, S, 0.55)


def test_ball_count_bound():
    rng = random.Random(4)
    cases = [(P, S, protect(P, S))]
    pts, segs = rand_complex(rng)
    cases.append((pts, segs, protect(pts, segs, 0.4, check=False)))
    for pts, segs, prot in cases:
        c = prot.c
        for e, (u, v) in enumerate(segs):
            L = math.sqrt(dist2(pts[u], pts[v]))
            H = min((_fsegseg(pts[u], pts[v], pts[p], pts[q]) for p, q in segs if not {u, v} & {p, q}), default=math.inf)
            su, sv = _sin_min_angle(pts, segs, e, u), _sin_min_angle(pts, segs, e, v)
            ru, rv = float(prot.balls[u].r), float(prot.balls[v].r)
            phi_bound = (L / H + math.log(L / ru) / su + math.log(L / rv) / sv) / c
            assert len(prot.chains[e]) - 2 <= phi_bound / 1.4 + 2


# --- what the protection buys ------------------------------------------------------------


def test_chain_is_restricted_for_any_unweighted_points(example):
    rng = random.Random(5)
    sites = example.weighted_points()
    extra = admissible_points(rng, example, 40) + near_curve_points(rng, example, 40)
    allsites = sites + extra
    for e, (u, v) in enumerate(S):
        got = restricted_pairs(P[u], P[v], allsites)
        assert got == chain_pairs(example, e)
    # the brute force agrees on one segment
    assert restricted_pairs_brute(P[2], P[1], allsites) == restricted_pairs(P[1], P[2], allsites)


def test_chain_holds_even_for_points_inside_balls(example):
    # the proof only uses that an unweighted point has power >= 0 everywhere
    rng = random.Random(6)
    pieces = [(p, q) for ch in example.chains for p, q in zip(ch, ch[1:])]
    extra = []
    for _ in range(30):
        p, q = rng.choice(pieces)
        a, b = example.balls[p].center, example.balls[q].center
        t = F(rng.randint(0, 100), 100)
        extra.append((tuple(x + t * (y - x) + rng.randint(-2, 2) for x, y in zip(a, b)), F(0)))
    allsites = example.weighted_points() + extra
    for e, (u, v) in enumerate(S):
        assert restricted_pairs(P[u], P[v], allsites) == chain_pairs(example, e)


def test_chain_on_random_complex():
    rng = random.Random(7)
    pts, segs = rand_complex(rng, nv=4, ne=5)
    prot = protect(pts, segs, 0.45)
    allsites = prot.weighted_points() + admissible_points(rng, prot, 15, -1100, 1100) + near_curve_points(rng, prot, 15)
    for e, (u, v) in enumerate(segs):
        assert restricted_pairs(pts[u], pts[v], allsites) == chain_pairs(prot, e)


def middle_piece(prot, e):
    """The middle piece [p, q] of chain e, its midpoint m, a normal n, and D = |pq|^2."""
    ch = prot.chains[e]
    p, q = ch[len(ch) // 2], ch[len(ch) // 2 + 1]
    a, b = prot.balls[p].center, prot.balls[q].center
    m = tuple((x + y) / 2 for x, y in zip(a, b))
    d = sub(b, a)
    n = (-d[1], d[0], F(0)) if (d[0], d[1]) != (0, 0) else (F(1), F(0), F(0))
    return p, q, a, b, m, n, dist2(a, b)


def test_without_weights_a_point_in_the_balls_breaks_the_chain(example):
    # same centers with weight 0: an unweighted point close to the middle of a
    # piece takes a part of the edge, so p and q are no longer joined; with the
    # weights the same point changes nothing
    zero = [(b.center, F(0)) for b in example.balls]
    weighted = example.weighted_points()
    for e, (u, v) in enumerate(S):
        p, q, a, b, m, n, D = middle_piece(example, e)
        s = tuple(mi + F(1, 64) * ni for mi, ni in zip(m, n))
        assert dist2(s, a) < example.balls[p].r ** 2  # inside the protecting ball
        unw = restricted_pairs(P[u], P[v], zero + [(s, F(0))])
        assert (min(p, q), max(p, q)) not in unw
        assert any(len(zero) in pair for pair in unw)
        assert restricted_pairs(P[u], P[v], weighted + [(s, F(0))]) == chain_pairs(example, e)


def test_voronoi_points_inside_balls_only_without_weights(example):
    # put an unweighted point s just outside the balls, above the middle of a piece.
    # Without weights the point equidistant from p, q and s lies deep inside B_p, and
    # p, q, s are its nearest sites: a Voronoi edge passes through the protecting
    # ball, and a refinement step could insert a point there. With weights, the
    # point of equal power to p, q and s has power |z - s|^2 >= 0 to all three.
    weighted = example.weighted_points()
    zero = [(b.center, F(0)) for b in example.balls]
    for e in range(len(S)):
        p, q, a, b, m, n, D = middle_piece(example, e)
        N = sum(x * x for x in n)
        rp, rq = example.balls[p].r, example.balls[q].r
        # smallest t on a fine grid with s outside both balls of the piece
        step = F(math.sqrt(float(D / N))).limit_denominator(1000) / 1024
        t0 = math.sqrt(max(0.0, float((max(rp, rq) ** 2 - D / 4) / N)))
        t = F(math.floor(t0 / float(step)) - 2) * step
        while True:
            s = tuple(mi + t * ni for mi, ni in zip(m, n))
            if t > 0 and all(dist2(s, bb.center) >= bb.r**2 for bb in example.balls):
                break
            t += step
        # unweighted: z = m + y n with |z - p| = |z - s|
        y = (t * t * N - D / 4) / (2 * t * N)
        z = tuple(mi + y * ni for mi, ni in zip(m, n))
        best, arg = nearest_power(z, zero + [(s, F(0))])
        assert sorted(arg) == sorted([p, q, len(zero)])
        assert dist2(z, a) < rp**2
        # weighted: z' = a + alpha (b - a) + beta n with equal power to p, q and s
        alpha = F(1, 2) + (rp**2 - rq**2) / (2 * D)
        beta = (t * t * N + rp**2 + D / 4 - alpha * D) / (2 * t * N)
        zw = tuple(ai + alpha * (bi - ai) + beta * ni for ai, bi, ni in zip(a, b, n))
        pw = [dist2(zw, c) - w for c, w in (weighted[p], weighted[q], (s, F(0)))]
        assert pw[0] == pw[1] == pw[2] >= 0
        best, arg = nearest_power(zw, weighted + [(s, F(0))])
        if len(arg) >= 3:
            assert best >= 0


def test_no_point_is_in_three_balls(example):
    # property (b): only neighbors in a chain overlap, so a point with negative
    # power to its nearest sites has at most two of them, and they are neighbors
    rng = random.Random(8)
    sites = example.weighted_points()
    adj = example.adjacent_pairs()
    pieces = [(p, q) for ch in example.chains for p, q in zip(ch, ch[1:])]
    for _ in range(300):
        p, q = rng.choice(pieces)
        a, b = example.balls[p].center, example.balls[q].center
        t = F(rng.randint(0, 64), 64)
        x = tuple(xa + t * (xb - xa) + F(rng.randint(-64, 64), 16) for xa, xb in zip(a, b))
        inside = [i for i, (c, w) in enumerate(sites) if dist2(x, c) < w]
        assert len(inside) <= 2
        if len(inside) == 2:
            assert tuple(inside) in adj
        best, arg = nearest_power(x, sites + [(x, F(0))])
        if best < 0:
            assert len(arg) <= 2


def test_larger_balls_measured():
    # the exact check needs c < 1/2; with c = 1.2 it fails, yet on this example the
    # chains are still the restricted pairs for these random points
    rng = random.Random(9)
    prot = protect(P, S, 1.2, check=False)
    assert violations(prot)
    allsites = prot.weighted_points() + admissible_points(rng, prot, 60)
    for e, (u, v) in enumerate(S):
        assert restricted_pairs(P[u], P[v], allsites) == chain_pairs(prot, e)
    # with c = 1.6 they are not
    prot = protect(P, S, 1.6, check=False)
    allsites = prot.weighted_points() + admissible_points(rng, prot, 60)
    assert any(restricted_pairs(P[u], P[v], allsites) != chain_pairs(prot, e) for e, (u, v) in enumerate(S))


@pytest.mark.parametrize(
    "pts,segs",
    [
        ([(0, 0, 0), (10, 0, 0), (0, 10, 0), (10, 10, 0)], [(0, 3), (1, 2)]),  # crossing
        ([(0, 0, 0), (10, 0, 0), (20, 0, 0)], [(0, 1), (0, 2)]),  # overlapping
        ([(0, 0, 0), (10, 0, 0), (5, 5, 5)], [(0, 1)]),  # isolated vertex
        ([(0, 0, 0), (10, 0, 0)], [(0, 1), (1, 0)]),  # duplicate
        ([(0, 0, 0), (10, 0, 0)], [(0, 0)]),  # loop
    ],
)
def test_bad_input(pts, segs):
    with pytest.raises(ValueError):
        protect(pts, segs)


def test_bad_c():
    with pytest.raises(ValueError):
        protect(P, S, 0)
