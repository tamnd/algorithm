# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shannon-entropy/. The authors are listed in prov/A13CS0.jsonl.

import math
import random

import pytest

from shannon_entropy import empirical_h0, empirical_hk, entropy


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) <= tol


def random_dist(rng: random.Random, m: int) -> list[float]:
    w = [rng.random() for _ in range(m)]
    s = sum(w)
    return [x / s for x in w]


def test_small_values() -> None:
    assert close(entropy([1.0]), 0.0)
    assert close(entropy([0.5, 0.5]), 1.0)
    assert close(entropy([0.25] * 4), 2.0)
    assert close(entropy([0.5, 0.25, 0.25]), 1.5)
    assert close(entropy([0.5, 0.5], base=math.e), math.log(2))
    assert close(entropy([1.0, 0.0, 0.0]), 0.0)


def test_input_checks() -> None:
    with pytest.raises(ValueError):
        entropy([0.5, 0.6])
    with pytest.raises(ValueError):
        entropy([1.5, -0.5])


def test_bounds_and_uniform_maximum() -> None:
    rng = random.Random(1)
    for m in range(1, 12):
        assert close(entropy([1 / m] * m), math.log2(m))
        for _ in range(50):
            p = random_dist(rng, m)
            h = entropy(p)
            assert -1e-12 <= h <= math.log2(m) + 1e-12


def test_grouping_axiom() -> None:
    # Shannon 1948, Section 6: H(1/2, 1/3, 1/6) = H(1/2, 1/2) + (1/2) H(2/3, 1/3).
    assert close(entropy([1 / 2, 1 / 3, 1 / 6]), entropy([0.5, 0.5]) + 0.5 * entropy([2 / 3, 1 / 3]))


def test_independent_pair_adds() -> None:
    rng = random.Random(2)
    for _ in range(50):
        p = random_dist(rng, 3)
        q = random_dist(rng, 4)
        joint = [a * b for a in p for b in q]
        assert close(entropy(joint), entropy(p) + entropy(q))


def test_concavity() -> None:
    rng = random.Random(3)
    for _ in range(200):
        p = random_dist(rng, 5)
        q = random_dist(rng, 5)
        t = rng.random()
        mix = [t * a + (1 - t) * b for a, b in zip(p, q)]
        assert entropy(mix) >= t * entropy(p) + (1 - t) * entropy(q) - 1e-12


def test_mississippi() -> None:
    s = "mississippi"
    # counts i:4, s:4, p:2, m:1
    expected = (4 * math.log2(11 / 4) * 2 + 2 * math.log2(11 / 2) + math.log2(11)) / 11
    assert close(empirical_h0(s), expected)
    assert close(empirical_h0(s), 1.8230679822736610, 1e-12)
    # contexts of length 1: m -> i; i -> s, s, p; s -> s, i, s, i; p -> p, i
    h1 = (3 * entropy([2 / 3, 1 / 3]) + 4 * 1.0 + 2 * 1.0) / 11
    assert close(empirical_hk(s, 1), h1)
    assert close(empirical_hk(s, 2), 2 / 11)
    assert close(empirical_hk(s, 5), 0.0)


def test_empty_and_constant() -> None:
    assert empirical_h0("") == 0.0
    assert empirical_hk("", 2) == 0.0
    assert empirical_h0("aaaa") == 0.0
    assert empirical_hk("abababab", 1) == 0.0


def test_h0_bounds() -> None:
    rng = random.Random(4)
    for _ in range(100):
        sigma = rng.randint(1, 6)
        s = [rng.randrange(sigma) for _ in range(rng.randint(1, 60))]
        h = empirical_h0(s)
        assert -1e-12 <= h <= math.log2(sigma) + 1e-12


def test_hk_non_increasing_in_k() -> None:
    rng = random.Random(5)
    for _ in range(100):
        sigma = rng.randint(2, 4)
        s = "".join(rng.choice("abcd"[:sigma]) for _ in range(rng.randint(1, 80)))
        prev = empirical_hk(s, 0)
        for k in range(1, 8):
            cur = empirical_hk(s, k)
            assert cur <= prev + 1e-12
            prev = cur


def test_h0_equals_entropy_of_frequencies() -> None:
    s = "abracadabra"
    freqs = [5 / 11, 2 / 11, 2 / 11, 1 / 11, 1 / 11]
    assert close(empirical_h0(s), entropy(freqs))
