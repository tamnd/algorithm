# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nucleus-sampling/. The authors are listed in prov/G371BC.jsonl.

import itertools
import random
from fractions import Fraction as F

from nlslog import argmax
from nucleus_sampling import nucleus_distribution, nucleus_sample, nucleus_sample_logits, nucleus_set

# the, a, cat, dog, sat, ran
P = [F(2, 5), F(1, 4), F(3, 20), F(1, 10), F(3, 50), F(1, 25)]


class GridU:
    """A fake random source that returns the points j / n, j = 0 ... n - 1, in turn."""

    def __init__(self, n):
        self.n = n
        self.j = 0

    def random(self):
        u = F(self.j, self.n)
        self.j += 1
        return u


def random_fractions(rng, n):
    w = [rng.randint(0, 9) for _ in range(n)]
    if sum(w) == 0:
        w[0] = 1
    return [F(x, sum(w)) for x in w]


def test_example_values() -> None:
    assert nucleus_set(P, F(1, 2)) == [0, 1]
    assert nucleus_set(P, F(13, 20)) == [0, 1]
    assert nucleus_set(P, F(9, 10)) == [0, 1, 2, 3]
    assert nucleus_distribution(P, F(9, 10)) == [F(4, 9), F(5, 18), F(1, 6), F(1, 9), 0, 0]
    assert nucleus_set(P, F(95, 100)) == [0, 1, 2, 3, 4]
    assert sum(P[i] for i in nucleus_set(P, F(95, 100))) == F(24, 25)
    assert nucleus_set(P, F(1)) == [0, 1, 2, 3, 4, 5]


def test_smallest_set_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(250):
        n = rng.randint(1, 7)
        probs = random_fractions(rng, n)
        for p in (F(1, 10), F(1, 3), F(1, 2), F(7, 10), F(9, 10), F(1)):
            kept = nucleus_set(probs, p)
            mass = sum(probs[i] for i in kept)
            assert mass >= p
            sizes = [
                len(c)
                for m in range(1, n + 1)
                for c in itertools.combinations(range(n), m)
                if sum(probs[i] for i in c) >= p
            ]
            assert len(kept) == min(sizes)
            # among the smallest sets, the nucleus has the largest mass
            best = max(sum(probs[i] for i in c) for c in itertools.combinations(range(n), len(kept)))
            assert mass == best
            # no proper prefix reaches p
            assert sum(probs[i] for i in kept[:-1]) < p


def test_adapts_to_the_shape() -> None:
    peaked = [F(90, 100), F(5, 100), F(3, 100), F(2, 100)]
    flat = [F(1, 10)] * 10
    assert len(nucleus_set(peaked, F(9, 10))) == 1
    assert len(nucleus_set(flat, F(9, 10))) == 9


def test_float_rounding_pitfall() -> None:
    assert 0.7 + 0.2 < 0.9
    assert nucleus_set([0.7, 0.2, 0.1], 0.9) == [0, 1, 2]
    assert nucleus_set([F(7, 10), F(2, 10), F(1, 10)], F(9, 10)) == [0, 1]


def test_zero_mass_tokens_stay_out() -> None:
    assert nucleus_set([F(1, 2), F(0), F(1, 2)], F(1)) == [0, 2]
    assert nucleus_set([0.5, 0.0, 0.5], 1.0) == [0, 2]
    # a float sum that never reaches 1
    probs = [0.1] * 10 + [0.0]
    c = 0.0
    for x in probs:
        c = c + x
    assert c < 1.0
    assert nucleus_set(probs, 1.0) == list(range(10))


def test_inverse_transform_is_exact_on_a_grid() -> None:
    n = 18 * 400
    q = nucleus_distribution(P, F(9, 10))
    src = GridU(n)
    counts = [0] * len(P)
    for _ in range(n):
        counts[nucleus_sample(P, F(9, 10), src)] += 1
    assert [F(c, n) for c in counts] == q


def test_sampling_frequencies() -> None:
    rng = random.Random(3)
    probs = [float(x) for x in P]
    draws = 20000
    counts = [0] * len(P)
    for _ in range(draws):
        counts[nucleus_sample(probs, 0.85, rng)] += 1
    expected = [4 / 9, 5 / 18, 1 / 6, 1 / 9, 0.0, 0.0]
    for c, e in zip(counts, expected):
        assert abs(c / draws - e) < 0.01
    assert counts[4:] == [0, 0]


def test_small_p_is_greedy_and_temperature_changes_the_set() -> None:
    rng = random.Random(4)
    for _ in range(200):
        probs = [rng.random() + 0.01 for _ in range(6)]
        s = sum(probs)
        probs = [x / s for x in probs]
        assert nucleus_set(probs, 1e-9) == [argmax(probs)]
    logits = [2.0, 1.0, 0.0]
    # T = 1 gives (0.665, 0.245, 0.090), T = 0.5 gives (0.867, 0.117, 0.016)
    assert nucleus_sample_logits(logits, 0.8, rng, temperature=0.5) == 0
    seen = {nucleus_sample_logits(logits, 0.8, rng, temperature=1.0) for _ in range(500)}
    assert seen == {0, 1}


def test_bad_threshold() -> None:
    for p in (0, -0.1, 1.5):
        try:
            nucleus_set(P, p)
        except ValueError:
            pass
        else:
            raise AssertionError("no ValueError")
