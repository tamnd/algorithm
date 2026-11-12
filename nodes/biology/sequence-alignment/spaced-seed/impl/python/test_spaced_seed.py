# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spaced-seed/. The authors are listed in prov/0TDJNQ.jsonl.

import random

import pytest

from spaced_seed import (
    PATTERNHUNTER,
    expected_hits,
    hit_probability,
    hit_probability_brute,
    hits,
    seed_hit_pairs,
    weight,
)


def test_patternhunter_seed_shape() -> None:
    assert PATTERNHUNTER == "111010010100110111"
    assert len(PATTERNHUNTER) == 18
    assert weight(PATTERNHUNTER) == 11


def test_dp_matches_brute_force() -> None:
    for seed in ("1", "11", "111", "101", "1101", "1011", "11011", "1001", "110101"):
        for length in range(0, 11):
            for p in (0.3, 0.5, 0.7, 0.9):
                assert hit_probability(seed, length, p) == pytest.approx(
                    hit_probability_brute(seed, length, p), abs=1e-12
                )


def test_exact_counts_at_one_half() -> None:
    # At p = 1/2 each 0/1 region of length 12 has probability 2^-12,
    # so 4096 times the probability is the number of regions with a hit.
    assert round(hit_probability("1111", 12, 0.5) * 4096) == 1224
    assert round(hit_probability("11011", 12, 0.5) * 4096) == 1312
    assert round(hit_probability_brute("11011", 12, 0.5) * 4096) == 1312


def test_patternhunter_beats_contiguous_on_64_columns() -> None:
    contiguous = "1" * 11
    a = hit_probability(contiguous, 64, 0.7)
    b = hit_probability(PATTERNHUNTER, 64, 0.7)
    assert round(a, 4) == 0.3002
    assert round(b, 4) == 0.4671
    # but the expected number of hits is lower for the spaced seed
    assert expected_hits(PATTERNHUNTER, 64, 0.7) < expected_hits(contiguous, 64, 0.7)


def test_short_regions_favor_the_contiguous_seed() -> None:
    # On a region of length 18 the spaced seed has 1 placement and the
    # contiguous seed has 8, so the contiguous seed wins.
    assert hit_probability("1" * 11, 18, 0.7) > hit_probability(PATTERNHUNTER, 18, 0.7)
    assert hit_probability(PATTERNHUNTER, 18, 0.7) == pytest.approx(0.7**11)


def test_periodic_mismatches() -> None:
    region = ("1" * 7 + "0") * 8  # a mismatch at every eighth column
    assert hits("1" * 11, region) == []
    assert hits(PATTERNHUNTER, region)[:3] == [1, 4, 9]


def test_monte_carlo_agrees() -> None:
    rng = random.Random(3)
    trials, p, length = 20000, 0.7, 64
    got = 0
    for _ in range(trials):
        r = "".join("1" if rng.random() < p else "0" for _ in range(length))
        got += bool(hits(PATTERNHUNTER, r))
    # standard error is about 0.0035; allow four of them
    assert abs(got / trials - hit_probability(PATTERNHUNTER, length, p)) < 0.015


def test_seed_hit_pairs_against_naive_scan() -> None:
    rng = random.Random(5)
    seed = "1101"
    for _ in range(50):
        x = "".join(rng.choice("ACGT") for _ in range(rng.randint(0, 30)))
        y = "".join(rng.choice("ACGT") for _ in range(rng.randint(0, 30)))
        naive = [
            (i, j)
            for i in range(len(x) - len(seed) + 1)
            for j in range(len(y) - len(seed) + 1)
            if all(x[i + t] == y[j + t] for t, c in enumerate(seed) if c == "1")
        ]
        assert seed_hit_pairs(x, y, seed) == naive


def test_bad_seeds() -> None:
    for bad in ("", "0110", "1102", "10"):
        with pytest.raises(ValueError):
            hit_probability(bad, 10, 0.5)
