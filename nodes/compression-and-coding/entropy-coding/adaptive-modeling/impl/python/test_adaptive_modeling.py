# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-modeling/. The authors are listed in prov/XX6766.jsonl.

import itertools
import math
import random
from fractions import Fraction

from adaptive_modeling import (
    HalvingModel, escape_probabilities, kt_length, laplace_closed_form_length, laplace_length, ml_length,
    model_length, sequential_probability,
)


def h(p: float) -> float:
    return 0.0 if p in (0, 1) else -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


def test_example() -> None:
    seq = [0, 0, 1, 0]
    assert sequential_probability(seq, 2, Fraction(1, 2)) == Fraction(5, 128)
    assert sequential_probability(seq, 2, Fraction(1)) == Fraction(1, 20)
    assert abs(ml_length(seq) - (-3 * math.log2(0.75) - math.log2(0.25))) < 1e-12


def test_regret_bounds_exhaustive() -> None:
    # For every binary string up to length 12: KT regret <= lg(n)/2 + 1, Laplace <= lg(n + 1).
    for n in range(1, 13):
        for seq in itertools.product((0, 1), repeat=n):
            seq = list(seq)
            ml = ml_length(seq)
            assert kt_length(seq) - ml <= 0.5 * math.log2(n) + 1 + 1e-9
            assert laplace_length(seq) - ml <= math.log2(n + 1) + 1e-9


def test_laplace_length_depends_only_on_counts() -> None:
    rng = random.Random(5)
    for _ in range(50):
        k = rng.randint(2, 6)
        seq = [rng.randrange(k) for _ in range(rng.randint(1, 60))]
        counts = [seq.count(s) for s in range(k)]
        exact = -math.log2(sequential_probability(seq, k, Fraction(1)))
        assert abs(exact - laplace_closed_form_length(counts)) < 1e-9
        rng.shuffle(seq)
        assert abs(laplace_length(seq, k) - exact) < 1e-9


def test_iid_sources_against_ideal() -> None:
    rng = random.Random(1981)
    for p in (0.01, 0.1, 0.3, 0.5):
        for n in (100, 1000, 20000):
            seq = [int(rng.random() < p) for _ in range(n)]
            ml = ml_length(seq)
            kt, lap = kt_length(seq), laplace_length(seq)
            assert 0 <= kt - ml <= 0.5 * math.log2(n) + 1
            assert 0 <= lap - ml <= math.log2(n + 1)
        # Per symbol, the KT length approaches the entropy of the source.
        assert abs(kt / n - h(p)) < 0.02


def test_escape_methods_sum_to_one() -> None:
    counts = {"a": 5, "b": 2, "r": 2, "c": 1, "d": 1}  # abracadabra
    expected_escape = {"A": Fraction(1, 12), "B": Fraction(5, 11), "C": Fraction(5, 16), "D": Fraction(5, 22)}
    expected_a = {"A": Fraction(5, 12), "B": Fraction(4, 11), "C": Fraction(5, 16), "D": Fraction(9, 22)}
    for method in "ABCD":
        probs, esc = escape_probabilities(method, counts)
        assert sum(probs.values()) + esc == 1
        assert esc == expected_escape[method]
        assert probs["a"] == expected_a[method]
    rng = random.Random(7)
    for _ in range(100):
        counts = {s: rng.randint(1, 30) for s in range(rng.randint(1, 10))}
        for method in "ABCD":
            probs, esc = escape_probabilities(method, counts)
            assert sum(probs.values()) + esc == 1 and esc > 0


def test_halving_follows_a_changing_source() -> None:
    rng = random.Random(1987)
    seq = []
    for block in range(20):
        p = 0.05 if block % 2 == 0 else 0.95
        seq += [int(rng.random() < p) for _ in range(2000)]
    plain = model_length(seq, HalvingModel(2))
    halved = model_length(seq, HalvingModel(2, increment=32, limit=1024))
    assert halved < 0.6 * plain
    # On a stationary source, halving costs little.
    seq = [int(rng.random() < 0.2) for _ in range(40000)]
    plain = model_length(seq, HalvingModel(2))
    halved = model_length(seq, HalvingModel(2, increment=32, limit=1024))
    assert plain <= halved <= 1.03 * plain
