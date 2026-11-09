# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-objective-simulated-annealing/. The authors are listed in prov/DTW645.jsonl.

import itertools
import math
import random

from multi_objective_simulated_annealing import accept_probability, dominates, mosa, weakly_dominates

W = (0.5, 0.5)


def test_example() -> None:
    x = (4, 4)
    assert accept_probability(x, (5, 2), W, 1, "sum") == 1
    assert math.isclose(accept_probability(x, (5, 2), W, 1, "product"), math.exp(-0.5))
    assert math.isclose(accept_probability(x, (5, 5), W, 1, "sum"), math.exp(-1))
    assert math.isclose(accept_probability(x, (5, 5), W, 1, "product"), math.exp(-1))
    assert math.isclose(accept_probability(x, (6, 3), W, 1, "sum"), math.exp(-0.5))
    assert math.isclose(accept_probability(x, (6, 3), W, 1, "product"), math.exp(-1))
    assert math.isclose(accept_probability(x, (6, 3), W, 0.5, "sum"), math.exp(-1))


def test_rule_properties() -> None:
    rng = random.Random(1)
    for _ in range(2000):
        p = rng.randint(1, 4)
        w = [rng.choice((0.25, 0.5, 1.0, 2.0)) for _ in range(p)]
        a = tuple(rng.randint(0, 5) for _ in range(p))
        b = tuple(rng.randint(0, 5) for _ in range(p))
        t = rng.choice((0.1, 1.0, 5.0))
        ps, pp = accept_probability(a, b, w, t, "sum"), accept_probability(a, b, w, t, "product")
        assert 0 < pp <= ps <= 1
        if weakly_dominates(b, a):
            assert pp == ps == 1
        if dominates(a, b):
            assert ps < 1 and pp < 1
            assert accept_probability(a, b, w, t / 2, "sum") <= ps
        # the sum rule is the Metropolis rule for h = w . f
        h = sum(wm * (v - u) for wm, u, v in zip(w, a, b))
        assert math.isclose(ps, min(1.0, math.exp(-h / t)))
        # both rules satisfy detailed balance for the Boltzmann weights exp(-h / T)
        for rule in ("sum", "product"):
            fwd = accept_probability(a, b, w, t, rule)
            back = accept_probability(b, a, w, t, rule)
            assert math.isclose(fwd, back * math.exp(-h / t), rel_tol=1e-9, abs_tol=1e-300)


def bits(n):
    return lambda r: tuple(r.randint(0, 1) for _ in range(n))


def flip_one(x, r):
    i = r.randrange(len(x))
    return x[:i] + (1 - x[i],) + x[i + 1 :]


def two_knapsacks(x):
    w1 = [3, 1, 4, 1, 5, 9, 2]
    w2 = [2, 7, 1, 8, 2, 8, 1]
    return (-sum(a * b for a, b in zip(x, w1)), -sum((1 - a) * b for a, b in zip(x, w2)))


def front(images):
    return {y for y in images if not any(dominates(z, y) for z in images)}


def test_archive_is_front_of_seen() -> None:
    for seed, rule in [(1, "sum"), (2, "product"), (3, "sum")]:
        rng = random.Random(seed)
        seen = set()
        start = bits(7)(random.Random(seed))
        seen.add(two_knapsacks(start))

        def hook(cur, y, archive, temp):
            seen.add(y[1])
            imgs = [z for _, z in archive]
            assert len(set(imgs)) == len(imgs) and set(imgs) == front(seen)
            assert cur[1] == two_knapsacks(cur[0]) and temp > 0

        out = mosa(bits(7), two_knapsacks, flip_one, (0.5, 0.5), 20.0, 0.98, 300, rng, rule, hook)
        assert out


def test_weighted_minimizers_are_pareto_optimal() -> None:
    space = list(itertools.product((0, 1), repeat=7))
    images = {two_knapsacks(x) for x in space}
    pareto = front(images)
    for w in [(0.5, 0.5), (0.1, 0.9), (0.8, 0.2)]:
        best = min(sum(a * b for a, b in zip(w, y)) for y in images)
        mins = {y for y in images if sum(a * b for a, b in zip(w, y)) == best}
        assert mins <= pareto
