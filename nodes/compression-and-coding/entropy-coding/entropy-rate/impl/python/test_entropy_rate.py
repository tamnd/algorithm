# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/entropy-rate/. The authors are listed in prov/7JPQ0Z.jsonl.

import math

import pytest

from entropy_rate import (
    empirical_block_entropy, markov_block_entropy, markov_entropy_rate, sample_markov, stationary_distribution,
)


def h(p: float) -> float:
    return 0.0 if p in (0.0, 1.0) else -p * math.log2(p) - (1 - p) * math.log2(1 - p)


TWO = [[0.9, 0.1], [0.3, 0.7]]


def test_two_state_chain() -> None:
    mu = stationary_distribution(TWO)
    assert mu == pytest.approx([0.75, 0.25], abs=1e-12)
    rate = markov_entropy_rate(TWO)
    assert rate == pytest.approx(0.75 * h(0.1) + 0.25 * h(0.3), abs=1e-12)
    assert rate == pytest.approx(0.5720694199996, abs=1e-10)


def test_iid_rows_give_entropy_of_the_row() -> None:
    P = [[0.5, 0.25, 0.25]] * 3
    assert markov_entropy_rate(P) == pytest.approx(1.5, abs=1e-12)


def test_periodic_chain() -> None:
    # The lazy iteration finds mu = (1/2, 1/2) although P itself is periodic. The rate is 0.
    P = [[0.0, 1.0], [1.0, 0.0]]
    assert stationary_distribution(P) == pytest.approx([0.5, 0.5], abs=1e-12)
    assert markov_entropy_rate(P) == 0.0


def test_stationary_is_fixed_point() -> None:
    P = [[0.5, 0.5, 0.0], [0.2, 0.3, 0.5], [0.1, 0.0, 0.9]]
    mu = stationary_distribution(P)
    assert sum(mu) == pytest.approx(1.0)
    for j in range(3):
        assert sum(mu[i] * P[i][j] for i in range(3)) == pytest.approx(mu[j], abs=1e-12)


def test_block_entropy_per_symbol_decreases_to_rate() -> None:
    rate = markov_entropy_rate(TWO)
    vals = [markov_block_entropy(TWO, k) / k for k in range(1, 200)]
    assert all(a >= b for a, b in zip(vals, vals[1:]))
    assert vals[-1] - rate < 0.0013
    assert all(v >= rate for v in vals)


def test_sampled_block_entropy_approaches_rate() -> None:
    seq = sample_markov(TWO, 100_000, seed=1)
    rate = markov_entropy_rate(TWO)
    for k in (1, 2, 4, 8):
        emp = empirical_block_entropy(seq, k) / k
        exact = markov_block_entropy(TWO, k) / k
        assert abs(emp - exact) < 0.015
    # The conditional entropy of the next symbol given the last k is the rate for k >= 1.
    for k in (1, 2, 3):
        diff = empirical_block_entropy(seq, k + 1) - empirical_block_entropy(seq, k)
        assert abs(diff - rate) < 0.015
    # The gap to the rate shrinks as the blocks grow.
    gaps = [empirical_block_entropy(seq, k) / k - rate for k in (1, 2, 4, 8)]
    assert gaps[0] > gaps[1] > gaps[2] > gaps[3] > 0


def test_three_state_sample() -> None:
    P = [[0.5, 0.5, 0.0], [0.2, 0.3, 0.5], [0.1, 0.0, 0.9]]
    seq = sample_markov(P, 100_000, seed=2)
    rate = markov_entropy_rate(P)
    diff = empirical_block_entropy(seq, 3) - empirical_block_entropy(seq, 2)
    assert abs(diff - rate) < 0.02


def test_bad_matrix() -> None:
    with pytest.raises(ValueError):
        stationary_distribution([[0.5, 0.4], [0.5, 0.5]])
