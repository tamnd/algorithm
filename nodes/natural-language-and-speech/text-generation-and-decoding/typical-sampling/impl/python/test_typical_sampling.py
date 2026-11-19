# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/typical-sampling/. The authors are listed in prov/T8X2CS.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

from typical_sampling import (
    entropy,
    typical_distribution,
    typical_order,
    typical_sample,
    typical_sample_logits,
    typical_set,
)

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
    h = entropy(P)
    assert abs(h - 1.525476) < 1e-6
    assert abs(h / math.log(2) - 2.200797) < 1e-6
    d = [abs(-math.log(x) - h) for x in P]
    for got, want in zip(d, (0.6092, 0.1392, 0.3716, 0.7771, 1.2879, 1.6934)):
        assert abs(got - want) < 1e-4
    assert typical_order(P) == [1, 2, 0, 3, 4, 5]
    assert typical_set(P, F(1, 5)) == [1]
    assert typical_set(P, F(1, 2)) == [1, 2, 0]
    assert typical_distribution(P, F(1, 2)) == [F(1, 2), F(5, 16), F(3, 16), 0, 0, 0]
    assert typical_set(P, F(9, 10)) == [1, 2, 0, 3]
    assert typical_set(P, F(95, 100)) == [1, 2, 0, 3, 4]
    assert typical_set(P, F(1)) == [1, 2, 0, 3, 4, 5]


def test_kept_tokens_are_the_closest_and_the_prefix_is_shortest() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 8)
        probs = random_fractions(rng, n)
        h = entropy(probs)
        for tau in (F(1, 10), F(1, 4), F(1, 2), F(9, 10), F(1)):
            kept = typical_set(probs, tau)
            assert sum(probs[i] for i in kept) >= tau
            assert sum(probs[i] for i in kept[:-1]) < tau
            assert all(probs[i] > 0 for i in kept)
            dropped = [i for i in range(n) if probs[i] > 0 and i not in kept]
            if dropped:
                worst_kept = max(abs(-math.log(probs[i]) - h) for i in kept)
                best_dropped = min(abs(-math.log(probs[i]) - h) for i in dropped)
                assert worst_kept <= best_dropped


def test_the_set_does_not_depend_on_the_log_base() -> None:
    rng = random.Random(2)
    for _ in range(200):
        probs = random_fractions(rng, rng.randint(1, 8))
        h2 = -sum(float(x) * math.log2(x) for x in probs if x > 0)
        d2 = {i: abs(-math.log2(probs[i]) - h2) for i in range(len(probs)) if probs[i] > 0}
        # the order of the code (in nats) is also sorted by the distances in
        # bits; exact ties between different probabilities, such as
        # (1/4, 1/4, 1/2), are broken by rounding, so allow 1e-9
        order = typical_order(probs)
        assert sorted(order) == sorted(d2)
        for a, b in zip(order, order[1:]):
            assert d2[a] <= d2[b] + 1e-9


def test_uniform_keeps_a_prefix_by_index() -> None:
    for n in range(1, 12):
        probs = [F(1, n)] * n
        for tau in (F(1, 10), F(1, 3), F(1, 2), F(9, 10), F(1)):
            m = math.ceil(tau * n)
            assert typical_set(probs, tau) == list(range(m))


def test_can_drop_the_most_probable_token() -> None:
    assert 0 not in typical_set(P, F(1, 5))
    assert typical_set(P, F(1, 5)) == [1]


def test_greedy_set_differs_from_the_optimization_of_the_paper() -> None:
    # minimize the sum of |H + log p| over sets of mass >= tau (Equation 12 of
    # Meister et al.), against the greedy prefix that the method uses
    for probs, tau, greedy, optimum in (
        ([F(4, 10), F(3, 10), F(2, 10), F(1, 10)], F(35, 100), [1, 2], (0,)),
        ([F(1, 2), F(1, 4), F(1, 8), F(1, 8)], F(3, 10), [1, 0], (0,)),
    ):
        h = entropy(probs)
        n = len(probs)
        best = min(
            (c for m in range(1, n + 1) for c in itertools.combinations(range(n), m) if sum(probs[i] for i in c) >= tau),
            key=lambda c: sum(abs(h + math.log(probs[i])) for i in c),
        )
        assert typical_set(probs, tau) == greedy
        assert best == optimum
        assert typical_order(probs)[0] not in best


def test_inverse_transform_is_exact_on_a_grid() -> None:
    n = 1600
    q = typical_distribution(P, F(1, 2))
    src = GridU(n)
    counts = [0] * len(P)
    for _ in range(n):
        counts[typical_sample(P, F(1, 2), src)] += 1
    assert [F(c, n) for c in counts] == q


def test_sampling_frequencies() -> None:
    rng = random.Random(3)
    probs = [float(x) for x in P]
    draws = 20000
    counts = [0] * len(P)
    for _ in range(draws):
        counts[typical_sample(probs, 0.5, rng)] += 1
    expected = [0.5, 0.3125, 0.1875, 0.0, 0.0, 0.0]
    for c, e in zip(counts, expected):
        assert abs(c / draws - e) < 0.01
    assert typical_sample_logits([0.0, 0.0, -50.0], 1.0, rng) in (0, 1)


def test_bad_arguments() -> None:
    for bad in (lambda: typical_set(P, 0), lambda: typical_set(P, F(3, 2)), lambda: typical_set([0, 0], F(1, 2))):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("no ValueError")
