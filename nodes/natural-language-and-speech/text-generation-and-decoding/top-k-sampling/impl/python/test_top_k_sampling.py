# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/top-k-sampling/. The authors are listed in prov/CNGCHZ.jsonl.

import itertools
import random
from fractions import Fraction as F

from nlslog import argmax, softmax
from top_k_sampling import top_k_distribution, top_k_sample, top_k_sample_logits, top_k_set

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
    assert top_k_set(P, 1) == [0]
    assert top_k_distribution(P, 2) == [F(8, 13), F(5, 13), 0, 0, 0, 0]
    assert top_k_distribution(P, 3) == [F(1, 2), F(5, 16), F(3, 16), 0, 0, 0]
    assert top_k_distribution(P, 6) == P
    assert top_k_distribution(P, 100) == P


def test_kept_set_has_maximum_mass_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 7)
        p = random_fractions(rng, n)
        for k in range(1, n + 2):
            kept = top_k_set(p, k)
            m = min(k, n)
            assert len(kept) == m and len(set(kept)) == m
            best = max(sum(p[i] for i in c) for c in itertools.combinations(range(n), m))
            assert sum(p[i] for i in kept) == best
            # every kept token is at least as probable as every dropped one
            dropped = [i for i in range(n) if i not in kept]
            if dropped:
                assert min(p[i] for i in kept) >= max(p[i] for i in dropped)


def test_tie_rule_smaller_index_first() -> None:
    p = [F(1, 10), F(3, 10), F(3, 10), F(3, 10)]
    assert top_k_set(p, 2) == [1, 2]
    assert top_k_set(p, 3) == [1, 2, 3]


def test_inverse_transform_is_exact_on_a_grid() -> None:
    n = 1600
    for k, q in ((2, top_k_distribution(P, 2)), (3, top_k_distribution(P, 3))):
        src = GridU(n * 13)
        counts = [0] * len(P)
        for _ in range(n * 13):
            counts[top_k_sample(P, k, src)] += 1
        assert [F(c, n * 13) for c in counts] == q


def test_k_equal_one_is_greedy() -> None:
    rng = random.Random(2)
    for _ in range(200):
        p = [rng.random() for _ in range(5)]
        assert top_k_sample(p, 1, rng) == argmax(p)


def test_sampling_frequencies() -> None:
    rng = random.Random(3)
    probs = [float(x) for x in P]
    draws = 20000
    counts = [0] * len(P)
    for _ in range(draws):
        counts[top_k_sample(probs, 3, rng)] += 1
    expected = [0.5, 0.3125, 0.1875, 0.0, 0.0, 0.0]
    for c, e in zip(counts, expected):
        assert abs(c / draws - e) < 0.01
    assert counts[3:] == [0, 0, 0]


def test_zero_mass_token_is_never_drawn() -> None:
    rng = random.Random(4)
    p = [0.5, 0.0, 0.5, 0.0]
    assert top_k_set(p, 3) == [0, 2, 1]
    seen = {top_k_sample(p, 3, rng) for _ in range(2000)}
    assert seen == {0, 2}


def test_kept_set_does_not_depend_on_temperature() -> None:
    rng = random.Random(5)
    for _ in range(100):
        z = [rng.uniform(-5, 5) for _ in range(8)]
        sets = [top_k_set(softmax(z, t), 3) for t in (0.5, 1.0, 2.0)]
        assert sets[0] == sets[1] == sets[2]
    assert top_k_sample_logits([2.0, 1.0, 0.0], 1, rng, temperature=3.0) == 0


def test_bad_arguments() -> None:
    for bad in (lambda: top_k_set(P, 0), lambda: top_k_distribution([0, 0], 1)):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("no ValueError")
