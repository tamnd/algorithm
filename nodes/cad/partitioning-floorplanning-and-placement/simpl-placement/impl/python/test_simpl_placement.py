# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simpl-placement/. The authors are listed in prov/S9RKW6.jsonl.

import random
from fractions import Fraction
from itertools import permutations

from simpl_placement import (
    b2b_edges,
    hpwl_points,
    lookahead_legalize,
    lower_bound,
    pin_points,
    quadratic_cost,
    simpl,
)


def instance(rng, n, K, S, q=4):
    pads = [(0, rng.randint(0, K)), (S, rng.randint(0, K)), (rng.randint(0, S), 0), (rng.randint(0, S), K)][:q]
    nets = []
    for i in range(n):  # a net to a pad or to an earlier cell, so every cell is tied to a pad
        nets.append([i, n + rng.randrange(q)] if i == 0 or rng.random() < 0.3 else [i, rng.randrange(i)])
    for _ in range(n // 2):
        nets.append(rng.sample(range(n + q), rng.randint(2, 3)))
    return nets, pads


def legal(x, r, W, K, S):
    used = set()
    for i in range(len(x)):
        if not (0 <= r[i] < K and 0 <= x[i] and x[i] + W[i] <= S):
            return False
        for s in range(x[i], x[i] + W[i]):
            if (r[i], s) in used:
                return False
            used.add((r[i], s))
    return True


def direct_hpwl(x, r, W, nets, pads):
    """HPWL computed from scratch with doubled integer coordinates, then halved."""
    total = 0
    for e in nets:
        xs, ys = [], []
        for p in e:
            if p < len(x):
                xs.append(2 * x[p] + W[p])
                ys.append(2 * r[p] + 1)
            else:
                xs.append(2 * pads[p - len(x)][0])
                ys.append(2 * pads[p - len(x)][1])
        total += max(xs) - min(xs) + max(ys) - min(ys)
    return Fraction(total, 2)


def exhaustive_optimum(n, nets, pads, K, S):
    sites = [(s, r) for r in range(K) for s in range(S)]
    return min(direct_hpwl([p[0] for p in perm], [p[1] for p in perm], [1] * n, nets, pads)
               for perm in permutations(sites, n))


def test_b2b_cost_is_twice_the_span_at_the_build_point():
    rng = random.Random(1)
    checked = 0
    for _ in range(200):
        pts = rng.randint(2, 9)
        coord = [Fraction(rng.randint(0, 40), 4) for _ in range(pts)]
        nets = [rng.sample(range(pts), rng.randint(2, min(5, pts))) for _ in range(rng.randint(1, 4))]
        weights = [rng.randint(1, 3) for _ in nets]
        eps = Fraction(1, 8)
        edges = b2b_edges(coord, nets, weights, eps)
        expect = 0
        for e, w in zip(nets, weights):
            vals = [coord[p] for p in e]
            if all(abs(coord[a] - coord[b]) >= eps or a == b for a in e for b in e):
                expect += 2 * w * (max(vals) - min(vals))
            else:
                expect = None
                break
        if expect is not None:
            checked += 1
            assert quadratic_cost(coord, edges) == expect
    assert checked >= 40


def test_page_example_of_lookahead_legalization():
    tx = [1.2, 1.5, 1.8, 2.1, 2.4, 2.0]
    ty = [0.9, 1.1, 0.8, 1.2, 1.0, 0.6]
    assert lookahead_legalize(tx, ty, [1] * 6, 2, 4) == ([1, 1, 2, 2, 3, 3], [0, 1, 0, 1, 1, 0])


def test_lookahead_legalization_is_legal():
    rng = random.Random(2)
    for _ in range(300):
        K, S = rng.randint(1, 5), rng.randint(3, 12)
        W = []
        while sum(W) < 0.7 * K * S - 3:
            W.append(rng.choice([1, 1, 2, 3]))
        tx = [rng.uniform(0, S) for _ in W]
        ty = [rng.uniform(0, K) for _ in W]
        try:
            x, r = lookahead_legalize(tx, ty, W, K, S)
        except ValueError:
            continue
        assert legal(x, r, W, K, S)


def test_lower_bound_with_strong_anchors_reaches_the_anchors():
    rng = random.Random(3)
    n, K, S = 8, 3, 6
    nets, pads = instance(rng, n, K, S)
    anchors = [(rng.uniform(0, S), rng.uniform(0, K)) for _ in range(n)]
    cx, cy = lower_bound([S / 2] * n, [K / 2] * n, n, nets, [1] * len(nets), pads, anchors, alpha=1e7)
    assert all(abs(cx[i] - anchors[i][0]) < 1e-4 and abs(cy[i] - anchors[i][1]) < 1e-4 for i in range(n))


def test_simpl_is_legal_and_its_hpwl_matches_a_direct_sum():
    rng = random.Random(11)
    for _ in range(4):
        n, K, S = 30, 6, 10
        W = [rng.choice([1, 1, 2]) for _ in range(n)]
        nets, pads = instance(rng, n, K, S)
        hist = []
        x, r = simpl(n, nets, pads, W, K, S, history=hist, iterations=8)
        assert legal(x, r, W, K, S)
        value = hpwl_points(pin_points(x, r, W, pads), nets, [1] * len(nets))
        assert value == direct_hpwl(x, r, W, nets, pads)
        assert value == min(ub for _, ub in hist)


def test_simpl_never_beats_the_exhaustive_optimum_on_6_cells():
    rng = random.Random(10)
    for _ in range(3):
        n, K, S = 6, 2, 4
        nets, pads = instance(rng, n, K, S)
        x, r = simpl(n, nets, pads, [1] * n, K, S)
        assert legal(x, r, [1] * n, K, S)
        assert direct_hpwl(x, r, [1] * n, nets, pads) >= exhaustive_optimum(n, nets, pads, K, S)
