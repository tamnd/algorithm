# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/good-turing-estimation/. The authors are listed in prov/7B0QFN.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from good_turing_estimation import (
    counts_of_counts,
    good_turing,
    raw_good_turing,
    turing_counts,
    type_counts,
    unseen_type_probability,
)

SAMPLE = "a a a b b c d e".split()


def test_check_values() -> None:
    c = type_counts(SAMPLE)
    assert counts_of_counts(c) == {1: 3, 2: 1, 3: 1}
    p, p0, rstar = good_turing(c)
    assert p0 == F(3, 8)
    assert rstar[1] == F(2, 3)
    assert rstar[2] == 3
    assert rstar[3] == 3  # N_4 = 0, so the raw count is kept
    # S = 3 * 2/3 + 1 * 3 + 1 * 3 = 8, and the seen mass is 5/8
    assert p["a"] == p["b"] == F(5, 8) * F(3, 8)
    assert p["c"] == F(5, 8) * F(2, 3) / 8
    assert p0 + sum(p.values()) == 1


def test_raw_formula() -> None:
    p, p0 = raw_good_turing(type_counts(SAMPLE))
    assert p == {"a": 0, "b": F(3, 8), "c": F(1, 12), "d": F(1, 12), "e": F(1, 12)}
    assert p0 + sum(p.values()) == 1


def test_cut_off() -> None:
    c = type_counts(SAMPLE)
    p, p0, rstar = good_turing(c, k=1)
    assert rstar == {1: F(2, 3), 2: 2, 3: 3}
    assert p0 + sum(p.values()) == 1
    p, p0, rstar = good_turing(c, k=0)
    assert rstar == {1: 1, 2: 2, 3: 3}
    assert p["a"] == F(5, 8) * F(3, 8)


def test_all_singletons() -> None:
    p, p0, _ = good_turing({"x": 1, "y": 1})
    assert p0 == 1
    assert all(v == 0 for v in p.values())


def test_errors() -> None:
    with pytest.raises(ValueError):
        good_turing({})
    with pytest.raises(ValueError):
        good_turing({"x": 0})
    with pytest.raises(ValueError):
        unseen_type_probability(F(1, 2), 0)
    assert unseen_type_probability(F(3, 8), 3) == F(1, 8)


def test_random_samples_are_proper() -> None:
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randrange(1, 60)
        types = rng.randrange(1, 15)
        tokens = [rng.randrange(types) for _ in range(n)]
        c = type_counts(tokens)
        k = rng.choice([None, 1, 2, 5])
        p, p0, rstar = good_turing(c, k)
        assert p0 + sum(p.values()) == 1
        assert all(0 <= v <= 1 for v in p.values())
        nr = counts_of_counts(c)
        assert rstar == turing_counts(nr, k)
        # the raw formula moves the tokens of each count s >= 2 down to the types seen s - 1 times
        raw, raw0 = raw_good_turing(c)
        kept = sum(s * nr[s] for s in nr if s >= 2 and s - 1 in nr)
        assert sum(raw.values()) == F(kept, n)
        assert (raw0 + sum(raw.values()) == 1) == all(s - 1 in nr for s in nr if s >= 2)


def test_expected_mass_identity() -> None:
    """E[mass of the types seen r times in N draws] = (r + 1) E[N_(r+1) in N + 1 draws] / (N + 1)."""
    dist = [F(1, 2), F(1, 3), F(1, 6)]
    for n in range(1, 6):
        for r in range(0, n + 1):
            lhs = F(0)
            for seq in itertools.product(range(3), repeat=n):
                w = F(1)
                for s in seq:
                    w *= dist[s]
                lhs += w * sum(dist[i] for i in range(3) if seq.count(i) == r)
            rhs = F(0)
            for seq in itertools.product(range(3), repeat=n + 1):
                w = F(1)
                for s in seq:
                    w *= dist[s]
                rhs += w * sum(1 for i in range(3) if seq.count(i) == r + 1)
            assert lhs == F(r + 1, n + 1) * rhs


def test_unseen_mass_on_zipf_data() -> None:
    """On average over many samples, N_1 / N is close to the true mass of the unseen types."""
    rng = random.Random(11)
    weights = [1 / (i + 1) for i in range(40)]
    z = sum(weights)
    probs = [w / z for w in weights]
    est, true = 0.0, 0.0
    trials, n = 400, 60
    for _ in range(trials):
        tokens = rng.choices(range(40), weights=probs, k=n)
        c = type_counts(tokens)
        _, p0, _ = good_turing(c)
        est += float(p0)
        true += sum(probs[i] for i in range(40) if i not in c)
    assert abs(est / trials - true / trials) < 0.02
