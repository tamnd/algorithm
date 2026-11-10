# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gelman-rubin-diagnostic/. The authors are listed in prov/T7ND6C.jsonl.

import math
import random

import pytest

from gelman_rubin_diagnostic import (
    potential_scale_reduction,
    rank_normalize,
    rank_normalized_split_rhat,
    split_rhat,
)


def ar1(phi, n, rng, start=None, mean=0.0, scale=1.0):
    sd = 1 / math.sqrt(1 - phi * phi)
    y = rng.gauss(0.0, sd) if start is None else start
    out = []
    for _ in range(n):
        y = phi * y + rng.gauss(0.0, 1.0)
        out.append(mean + scale * y)
    return out


def test_hand_example() -> None:
    r = potential_scale_reduction([[1, 2, 3, 4], [3, 4, 5, 6]])
    assert abs(r * r - 39 / 20) < 1e-12


def test_stationary_ar1_chains_give_one() -> None:
    rng = random.Random(1)
    chains = [ar1(0.9, 20_000, rng) for _ in range(4)]
    assert potential_scale_reduction(chains) < 1.01
    assert split_rhat(chains) < 1.01
    assert rank_normalized_split_rhat(chains) < 1.01


def test_overdispersed_short_chains_flagged() -> None:
    rng = random.Random(2)
    chains = [ar1(0.99, 200, rng, start=s) for s in (-50.0, -20.0, 20.0, 50.0)]
    assert potential_scale_reduction(chains) > 1.1
    assert rank_normalized_split_rhat(chains) > 1.1


def test_heuristic_rhat_squared_near_one_plus_tau_over_n() -> None:
    # for stationary chains, E[var_plus / W] is about 1 + (tau - 1) / n
    rng = random.Random(3)
    phi, n = 0.9, 400
    tau = (1 + phi) / (1 - phi)
    vals = [potential_scale_reduction([ar1(phi, n, rng) for _ in range(4)]) ** 2 for _ in range(300)]
    mean = sum(vals) / len(vals)
    assert abs((mean - 1) / ((tau - 1) / n) - 1) < 0.3


def test_different_means_flagged() -> None:
    rng = random.Random(4)
    chains = [ar1(0.5, 2000, rng, mean=mu) for mu in (0.0, 0.0, 2.0, 2.0)]
    assert potential_scale_reduction(chains) > 1.2


def test_split_detects_trend() -> None:
    rng = random.Random(5)
    n = 2000
    chains = [[3.0 * t / n + v for t, v in enumerate(ar1(0.5, n, rng))] for _ in range(4)]
    assert potential_scale_reduction(chains) < 1.02
    assert split_rhat(chains) > 1.1


def test_folding_detects_scale_difference() -> None:
    rng = random.Random(6)
    chains = [ar1(0.5, 5000, rng, scale=s) for s in (1.0, 1.0, 1.0, 3.0)]
    assert split_rhat(chains) < 1.02
    assert rank_normalized_split_rhat(chains) > 1.05


def test_bulk_rank_rhat_invariant_under_monotone_maps() -> None:
    rng = random.Random(7)
    chains = [ar1(0.8, 500, rng, mean=0.3 * j) for j in range(4)]
    a = potential_scale_reduction(rank_normalize(chains))
    b = potential_scale_reduction(rank_normalize([[math.exp(x) for x in c] for c in chains]))
    assert a == b


def test_cannot_prove_convergence() -> None:
    # target: equal mixture of N(-5, 1) and N(5, 1), mean 0; all chains stuck in the right mode
    rng = random.Random(8)
    chains = [ar1(0.5, 5000, rng, mean=5.0, scale=math.sqrt(0.75)) for _ in range(4)]
    assert rank_normalized_split_rhat(chains) < 1.01
    pooled_mean = sum(sum(c) for c in chains) / 20_000
    assert abs(pooled_mean - 5.0) < 0.1  # far from the true mean 0


def test_bad_inputs() -> None:
    with pytest.raises(ValueError):
        potential_scale_reduction([[1.0, 2.0]])
    with pytest.raises(ValueError):
        potential_scale_reduction([[1.0, 2.0], [1.0]])
