# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thermal-driven-3d-floorplanning/. The authors are listed in prov/RF40PK.jsonl.

import itertools
import math
import random

from thermal_driven_3d_floorplanning import (
    SINK,
    Floorplan,
    cost,
    perturb,
    realize,
    stack_top_temperature,
    terms,
    thermal_floorplan,
)

MODEL = (4, (1.0, 1.0), 0.5)  # 4 x 4 tiles, r_1 = r_2 = 1, r_b = 0.5


def all_floorplans(n, n_layers):
    for assign in itertools.product(range(n_layers), repeat=n):
        groups = [[b for b in range(n) if assign[b] == k] for k in range(n_layers)]
        pairs = [[(list(p), list(m)) for p in itertools.permutations(g) for m in itertools.permutations(g)]
                 for g in groups]
        for combo in itertools.product(*pairs):
            for rot in itertools.product([False, True], repeat=n):
                yield Floorplan([(list(p), list(m)) for p, m in combo], list(rot))


def random_instance(rng, n):
    blocks = [(rng.choice([1.0, 2.0, 3.0]), rng.choice([1.0, 2.0]), rng.choice([0.1, 1.0, 5.0])) for _ in range(n)]
    nets = [rng.sample(range(n), 2) for _ in range(n)]
    return blocks, nets


def valid(blocks, fp):
    seen = []
    for gp, gm in fp.layers:
        assert sorted(gp) == sorted(gm)
        seen += gp
    assert sorted(seen) == list(range(len(blocks)))
    x, y, lay, dims = realize(blocks, fp)
    for a, b in itertools.combinations(range(len(blocks)), 2):
        if lay[a] == lay[b]:
            apart = (x[a] + dims[a][0] <= x[b] + 1e-9 or x[b] + dims[b][0] <= x[a] + 1e-9
                     or y[a] + dims[a][1] <= y[b] + 1e-9 or y[b] + dims[b][1] <= y[a] + 1e-9)
            assert apart
    return True


def test_closed_form_is_the_resistor_chain():
    rng = random.Random(11)
    for _ in range(200):
        L = rng.randint(1, 5)
        p = [rng.uniform(0, 3) for _ in range(L)]
        r = [rng.uniform(0.1, 2) for _ in range(L)]
        rb = rng.uniform(0.1, 1)
        t = SINK + rb * sum(p)  # the base carries all the power
        for i in range(L):
            t += r[i] * sum(p[i:])  # resistor i carries the power of layers i and above
        assert math.isclose(stack_top_temperature(p, r, rb), t)


def test_hot_block_next_to_the_sink_is_cooler():
    blocks = [(2.0, 2.0, 5.0), (2.0, 2.0, 1.0)]  # same size, one hot and one cool
    hot_low = Floorplan([([0], [0]), ([1], [1])], [False, False])
    hot_high = Floorplan([([1], [1]), ([0], [0])], [False, False])
    _, _, _, t_low = terms(blocks, [[0, 1]], hot_low, MODEL)
    _, _, _, t_high = terms(blocks, [[0, 1]], hot_high, MODEL)
    # rise = r_b (q_0 + q_1) + r_1 (q_0 + q_1) + r_2 q_top
    assert math.isclose(t_low, 0.5 * 6 + 1.0 * 6 + 1.0 * 1)
    assert math.isclose(t_high, 0.5 * 6 + 1.0 * 6 + 1.0 * 5)


def test_moves_keep_a_valid_floorplan():
    rng = random.Random(5)
    for _ in range(20):
        blocks, _ = random_instance(rng, rng.randint(2, 7))
        fp = Floorplan([(list(range(len(blocks))), list(range(len(blocks)))), ([], [])], [False] * len(blocks))
        for _ in range(100):
            new, kind = perturb(blocks, fp, rng, 0.5)
            if kind is not None:
                assert valid(blocks, new)
                fp = new


def test_annealing_against_exhaustive_optimum():
    rng = random.Random(3)
    hits3 = 0
    for _ in range(15):
        blocks, nets = random_instance(rng, 3)
        fp, c, norm = thermal_floorplan(blocks, nets, 2, (1, 1, 1, 1), MODEL, seed=1)
        assert valid(blocks, fp)
        assert math.isclose(c, cost(blocks, nets, fp, MODEL, (1, 1, 1, 1), norm))
        opt = min(cost(blocks, nets, f, MODEL, (1, 1, 1, 1), norm) for f in all_floorplans(3, 2))
        assert c >= opt - 1e-9
        hits3 += c <= opt + 1e-9
    assert hits3 == 15
    rng = random.Random(4)
    hits4 = 0
    for _ in range(2):
        blocks, nets = random_instance(rng, 4)
        fp, c, norm = thermal_floorplan(blocks, nets, 2, (1, 1, 1, 1), MODEL, seed=1)
        opt = min(cost(blocks, nets, f, MODEL, (1, 1, 1, 1), norm) for f in all_floorplans(4, 2))
        assert c >= opt - 1e-9
        hits4 += c <= opt + 1e-9
    assert hits4 == 2


def test_thermal_weight_lowers_the_peak():
    rng = random.Random(8)
    lower = 0
    for _ in range(3):
        blocks, nets = random_instance(rng, 5)
        a, _, _ = thermal_floorplan(blocks, nets, 2, (1, 1, 1, 0), MODEL, seed=2)
        b, _, _ = thermal_floorplan(blocks, nets, 2, (1, 1, 1, 3), MODEL, seed=2)
        lower += terms(blocks, nets, b, MODEL)[3] <= terms(blocks, nets, a, MODEL)[3] + 1e-9
    assert lower == 3
