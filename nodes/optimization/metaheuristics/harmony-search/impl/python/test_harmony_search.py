# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harmony-search/. The authors are listed in prov/YB0SC1.jsonl.

import math
import random

from harmony_search import harmony_search, improvise, mu_plus_one_es, sphere


def close(freq: float, p: float, trials: int) -> bool:
    return abs(freq - p) < 5 * math.sqrt(p * (1 - p) / trials)


def test_improvise_distribution() -> None:
    memory = [[0.0], [1.0], [2.0]]
    hmcr, par, bw = 0.7, 0.4, 0.1
    rng = random.Random(1)
    trials = 40000
    exact = [0, 0, 0]
    near = 0
    far = 0
    for _ in range(trials):
        x = improvise(memory, hmcr, par, bw, [-10.0], [10.0], rng)[0]
        if x in (0.0, 1.0, 2.0):
            exact[int(x)] += 1
        elif any(0 < abs(x - m) <= bw for m in (0.0, 1.0, 2.0)):
            near += 1
        else:
            far += 1
    for k in range(3):
        assert close(exact[k] / trials, hmcr * (1 - par) / 3, trials)  # memory, no pitch change
    # Pitch adjustment gives a point within bw of a memory value; a random draw lands there with probability 0.6 / 20.
    p_near = hmcr * par + (1 - hmcr) * 3 * 2 * bw / 20
    assert close(near / trials, p_near, trials)
    assert close(far / trials, 1 - hmcr * (1 - par) - p_near, trials)


def test_pitch_adjustment_and_random_selection() -> None:
    rng = random.Random(2)
    memory = [[1.0, -2.0], [3.0, 0.5]]
    for _ in range(2000):
        x = improvise(memory, 1.0, 1.0, 0.25, [-5.0, -5.0], [5.0, 5.0], rng)
        for j in range(2):
            assert min(abs(x[j] - m[j]) for m in memory) <= 0.25
    xs = [improvise(memory, 0.0, 1.0, 0.25, [-5.0, 0.0], [5.0, 1.0], rng) for _ in range(20000)]
    assert all(-5.0 <= x[0] <= 5.0 and 0.0 <= x[1] <= 1.0 for x in xs)
    assert abs(sum(x[1] for x in xs) / len(xs) - 0.5) < 5 * math.sqrt(1 / 12 / len(xs))
    # Clipping keeps a pitch-adjusted coordinate in the box.
    edge = [[5.0]]
    assert all(-5.0 <= improvise(edge, 1.0, 1.0, 3.0, [-5.0], [5.0], rng)[0] <= 5.0 for _ in range(500))


def test_memory_invariants() -> None:
    seen = []

    def check(t, memory, values):
        assert len(memory) == 6
        assert all(-5.0 <= v <= 5.0 for x in memory for v in x)
        assert values == [sphere(x) for x in memory]
        seen.append(sorted(values))

    harmony_search(sphere, [-5.0] * 3, [5.0] * 3, 6, 0.9, 0.3, 0.05, 500, random.Random(3), check)
    for prev, cur in zip(seen, seen[1:]):
        assert all(c <= p for p, c in zip(prev, cur))
        assert cur == prev or sum(cur) < sum(prev)


def test_harmony_search_is_a_mu_plus_one_es() -> None:
    # Weyland (2010): the same random draws give the same run, step by step.
    def floor_sphere(x):
        return float(math.floor(sphere(x)))  # many ties, to check the tie rules too

    for f in (sphere, floor_sphere):
        for seed in range(4):
            hs_log, es_log = [], []
            hs = harmony_search(f, [-5.0] * 4, [5.0] * 4, 7, 0.85, 0.35, 0.2, 400, random.Random(seed), lambda t, m, v: hs_log.append((m, v)))
            es = mu_plus_one_es(f, [-5.0] * 4, [5.0] * 4, 7, 0.85, 0.35, 0.2, 400, random.Random(seed), lambda t, m, v: es_log.append((m, v)))
            assert hs_log == es_log
            assert hs[1] == es[1] and hs[2] == es[2]


def test_fixed_seed_on_the_sphere() -> None:
    best, value, hist = harmony_search(sphere, [-5.0] * 5, [5.0] * 5, 10, 0.9, 0.3, 0.01, 20000, random.Random(0))
    assert value < 1e-7 and value == sphere(best)
    assert all(hist[t + 1] <= hist[t] for t in range(len(hist) - 1))
