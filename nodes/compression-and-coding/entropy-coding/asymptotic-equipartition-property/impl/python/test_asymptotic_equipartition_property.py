# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asymptotic-equipartition-property/. The authors are listed in prov/02QMVF.jsonl.

import itertools
from fractions import Fraction
from math import log2

from asymptotic_equipartition_property import bernoulli_entropy, sample_entropy, typical_set, typical_weights


def brute_force(n: int, p: Fraction, eps: float) -> tuple[Fraction, int]:
    H = bernoulli_entropy(float(p))
    prob, size = Fraction(0), 0
    for x in itertools.product((0, 1), repeat=n):
        k = sum(x)
        if abs(sample_entropy(n, k, float(p)) - H) <= eps:
            prob += p ** k * (1 - p) ** (n - k)
            size += 1
    return prob, size


def test_matches_enumeration_for_small_n() -> None:
    for p in (Fraction(1, 10), Fraction(1, 3), Fraction(2, 5)):
        for eps in (0.05, 0.2):
            for n in range(1, 13):
                assert typical_set(n, p, eps) == brute_force(n, p, eps)


def test_upper_bound_on_size_for_every_n() -> None:
    for p in (Fraction(1, 10), Fraction(1, 4), Fraction(1, 3)):
        H = bernoulli_entropy(float(p))
        for eps in (0.02, 0.1, 0.3):
            for n in (1, 5, 10, 50, 100, 500, 1000):
                prob, size = typical_set(n, p, eps)
                assert size == 0 or log2(size) <= n * (H + eps) + 1e-9
                assert 0 <= prob <= 1


def test_probability_tends_to_one_and_lower_bound_on_size() -> None:
    p, eps = Fraction(1, 10), 0.1
    H = bernoulli_entropy(float(p))
    probs = {}
    for n in (100, 200, 500, 1000, 2000):
        prob, size = typical_set(n, p, eps)
        probs[n] = float(prob)
        if prob > 1 - eps:
            assert log2(size) >= log2(1 - eps) + n * (H - eps) - 1e-9
    assert probs[100] < probs[200] < probs[500] < probs[1000] < probs[2000]
    assert probs[500] > 1 - eps
    assert probs[2000] > 0.99999


def test_exact_values_used_on_the_page() -> None:
    p, eps = Fraction(1, 10), 0.1
    assert typical_weights(100, 0.1, eps) == list(range(7, 14))
    prob, size = typical_set(100, p, eps)
    assert abs(float(prob) - 0.75896759) < 1e-8
    assert abs(log2(size) / 100 - 0.52885853) < 1e-8
    prob, _ = typical_set(1000, p, eps)
    assert abs(float(prob) - 0.99905983) < 1e-8


def test_fair_coin_every_sequence_is_typical() -> None:
    for n in (1, 10, 100):
        prob, size = typical_set(n, Fraction(1, 2), 0.01)
        assert prob == 1 and size == 2 ** n


def test_typical_set_is_small_fraction_of_all_sequences() -> None:
    # For p = 1/10 and eps = 0.1 the set holds almost all the probability
    # but only about 2^(0.556 n) of the 2^n sequences.
    prob, size = typical_set(1000, Fraction(1, 10), 0.1)
    assert prob > 0.999
    assert log2(size) < 0.57 * 1000
