# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boykov-jolly-graph-cuts/. The authors are listed in prov/DCZHC7.jsonl.

import math
import random

import pytest

from boykov_jolly_graph_cuts import (
    InteractiveCut,
    boundary_weights,
    brute_force,
    energy,
    histogram_costs,
    seed_constant,
)


def random_case(rng, w, h, nseed):
    img = [[rng.choice((20, 60, 140, 220)) + rng.randrange(20) for _ in range(w)] for _ in range(h)]
    pix = list(range(w * h))
    rng.shuffle(pix)
    obj = pix[:nseed]
    bkg = pix[nseed:2 * nseed]
    return img, obj, bkg


def test_row_example():
    img = [[20, 40, 140, 200, 220]]
    c = InteractiveCut(img, [4], [0], 1.0, 30.0)
    assert abs(c.r_obj[0] - 1.6094) < 1e-4 and abs(c.r_obj[4] - 0.9163) < 1e-4
    assert abs(c.pairs[1][2] - 0.0039) < 1e-4 and abs(c.pairs[2][2] - 0.1353) < 1e-4
    assert abs(c.K - 1.9361) < 1e-4
    assert c.labels == [0, 0, 1, 1, 1]
    assert abs(c.g.flow - 3.4459) < 1e-4
    e = energy(c.labels, c.r_obj, c.r_bkg, c.pairs, 1.0)
    assert abs(e - 5.2785) < 1e-4
    assert c.add_seed(2, 0) == [0, 0, 0, 1, 1]
    assert abs(c.g.flow - 5.1868) < 1e-4
    assert abs(c.cut_value() - 1.9679) < 1e-4


def test_cut_is_constrained_minimum():
    rng = random.Random(1)
    for trial in range(25):
        w, h = rng.choice(((3, 3), (4, 3), (3, 4)))
        img, obj, bkg = random_case(rng, w, h, rng.randint(1, 2))
        lam = rng.choice((0.1, 0.5, 1.0, 3.0))
        eight = trial % 2 == 0
        c = InteractiveCut(img, obj, bkg, lam, 25.0, eight=eight)
        for p in obj:
            assert c.labels[p] == 1
        for p in bkg:
            assert c.labels[p] == 0
        best, _ = brute_force(w * h, set(obj), set(bkg), c.r_obj, c.r_bkg, c.pairs, lam)
        e = energy(c.labels, c.r_obj, c.r_bkg, c.pairs, lam)
        assert abs(e - best) < 1e-9
        const = seed_constant(obj, bkg, c.r_obj, c.r_bkg, lam)
        assert abs(c.g.flow - (best - const)) < 1e-9


def test_given_region_costs_four_neighbors():
    rng = random.Random(2)
    for _ in range(15):
        w, h = 4, 3
        img = [[rng.randrange(256) for _ in range(w)] for _ in range(h)]
        r_obj = [rng.uniform(0, 3) for _ in range(w * h)]
        r_bkg = [rng.uniform(0, 3) for _ in range(w * h)]
        c = InteractiveCut(img, [0], [11], 1.0, 40.0, eight=False, region=(r_obj, r_bkg))
        best, arg = brute_force(w * h, {0}, {11}, r_obj, r_bkg, c.pairs, 1.0)
        assert abs(energy(c.labels, r_obj, r_bkg, c.pairs, 1.0) - best) < 1e-9
        assert len(arg) >= 1


def test_added_seeds_reuse_flow():
    rng = random.Random(3)
    for _ in range(10):
        w, h = 4, 3
        img, obj, bkg = random_case(rng, w, h, 1)
        c = InteractiveCut(img, obj, bkg, 1.0, 25.0)
        free = [p for p in range(w * h) if p not in obj and p not in bkg]
        rng.shuffle(free)
        for p in free[:4]:
            label = rng.randrange(2)
            c.add_seed(p, label)
            o = [q for q in range(w * h) if q in c.obj]
            g = [q for q in range(w * h) if q in c.bkg]
            fresh = InteractiveCut(img, o, g, 1.0, 25.0, region=(c.r_obj, c.r_bkg))
            assert abs(c.cut_value() - fresh.g.flow) < 1e-9
            assert c.labels[p] == label
            best, _ = brute_force(w * h, set(o), set(g), c.r_obj, c.r_bkg, c.pairs, 1.0)
            assert abs(energy(c.labels, c.r_obj, c.r_bkg, c.pairs, 1.0) - best) < 1e-9
            for a in range(w * h + 2):
                for cap in c.g.res[a].values():
                    assert cap >= -1e-12


def test_large_lambda_follows_region_term():
    rng = random.Random(4)
    w, h = 4, 3
    img = [[rng.randrange(256) for _ in range(w)] for _ in range(h)]
    r_obj = [rng.uniform(0, 3) for _ in range(w * h)]
    r_bkg = [rng.uniform(0, 3) for _ in range(w * h)]
    c = InteractiveCut(img, [0], [11], 1000.0, 40.0, region=(r_obj, r_bkg))
    for p in range(1, 11):
        assert c.labels[p] == (1 if r_obj[p] < r_bkg[p] else 0)


def test_helpers_and_errors():
    img = [[0, 0], [255, 255]]
    costs = histogram_costs(img, [0, 1], 2, 255)
    assert abs(costs[0] + math.log(3 / 4)) < 1e-12
    assert abs(costs[2] + math.log(1 / 4)) < 1e-12
    pairs = boundary_weights(img, 10.0, eight=False)
    assert len(pairs) == 4
    with pytest.raises(ValueError):
        InteractiveCut(img, [0], [0], 1.0, 10.0)
    c = InteractiveCut(img, [0], [3], 1.0, 10.0)
    with pytest.raises(ValueError):
        c.add_seed(0, 0)
