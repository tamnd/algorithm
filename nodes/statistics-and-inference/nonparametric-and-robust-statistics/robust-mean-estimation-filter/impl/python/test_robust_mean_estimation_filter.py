# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robust-mean-estimation-filter/. The authors are listed in prov/VJ455W.jsonl.

import math
import random

import pytest

from robust_mean_estimation_filter import (
    contaminated_gaussian,
    coordinatewise_median,
    default_threshold,
    filter_mean,
    norm,
    sample_mean,
    top_eigen,
    weighted_cov,
)

EXAMPLE = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1), (4, 4), (4, 4)]


def taus(xs, mu, v):
    return [sum(a * (b - m) for a, b, m in zip(v, x, mu)) ** 2 for x in xs]


def test_example():
    trace = []
    mu = filter_mean(EXAMPLE, 0.2, trace=trace)
    assert default_threshold(0.2) == pytest.approx(1.9657, abs=1e-4)
    assert len(trace) == 2
    assert trace[0]["mean"] == pytest.approx([0.8, 0.8])
    assert trace[0]["lambda"] == pytest.approx(5.72)
    # tau_i * 100 = 18, 338, 18, 338, 8, 648, 128, 128, 2048, 2048; the new weights are (1 - tau_i / 20.48) / 10.
    want = [2030, 1710, 2030, 1710, 2040, 1400, 1920, 1920, 0, 0]
    assert trace[1]["weights"] == pytest.approx([v / 20480 for v in want], abs=1e-7)
    assert trace[1]["lambda"] == pytest.approx(0.7737, abs=1e-4)
    assert mu == pytest.approx([8 / 123, 8 / 123], abs=1e-6)
    assert sample_mean(EXAMPLE) == pytest.approx([0.8, 0.8])
    assert coordinatewise_median(EXAMPLE) == [0.5, 0.5]


def test_power_iteration_on_a_known_matrix():
    lam, v = top_eigen([[3.16, 2.56], [2.56, 3.16]])
    assert lam == pytest.approx(5.72, abs=1e-10)
    assert abs(v[0]) == pytest.approx(math.sqrt(0.5), abs=1e-6)
    assert v[0] * v[1] > 0


def test_weighted_average_of_tau_is_lambda():
    xs, _ = contaminated_gaussian(400, 6, 0.1, 8.0, seed=11)
    trace = []
    filter_mean(xs, 0.1, trace=trace)
    assert len(trace) >= 2
    for t in trace:
        w, mu = t["weights"], t["mean"]
        lam, v = top_eigen(weighted_cov(xs, w, mu), seed=t["round"])
        tau = taus(xs, mu, v)
        assert sum(wi * ti for wi, ti in zip(w, tau)) / sum(w) == pytest.approx(lam, rel=1e-9)


def test_terminates_even_with_a_zero_threshold():
    rng = random.Random(4)
    xs = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(25)]
    trace = []
    mu = filter_mean(xs, 0.1, threshold=0.0, trace=trace)
    alive = [sum(1 for w in t["weights"] if w > 0) for t in trace]
    assert all(b < a for a, b in zip(alive, alive[1:]))
    assert len(trace) <= len(xs)
    assert alive[-1] >= 1
    assert all(math.isfinite(v) for v in mu)
    # All remaining points tie at tau_max: line L7 returns the weighted mean.
    assert filter_mean([(-1.0, 0.0), (1.0, 0.0)], 0.1, threshold=0.0) == pytest.approx([0.0, 0.0])


def test_removal_lemma_in_every_round():
    """When the bad points carry at least half of the weighted tau, they lose at least as much weight."""
    xs, bad = contaminated_gaussian(1000, 10, 0.1, 8.0, seed=0)
    trace = []
    filter_mean(xs, 0.1, trace=trace)
    held = 0
    for t, nxt in zip(trace, trace[1:]):
        w, mu = t["weights"], t["mean"]
        _, v = top_eigen(weighted_cov(xs, w, mu), seed=t["round"])
        tau = taus(xs, mu, v)
        good_mass = sum(wi * ti for wi, ti, b in zip(w, tau, bad) if not b)
        bad_mass = sum(wi * ti for wi, ti, b in zip(w, tau, bad) if b)
        lost_good = sum(a - b2 for a, b2, b in zip(w, nxt["weights"], bad) if not b)
        lost_bad = sum(a - b2 for a, b2, b in zip(w, nxt["weights"], bad) if b)
        tau_max = max(ti for ti, wi in zip(tau, w) if wi > 0)
        assert lost_good == pytest.approx(good_mass / tau_max, rel=1e-6)
        assert lost_bad == pytest.approx(bad_mass / tau_max, rel=1e-6)
        if good_mass <= bad_mass:
            held += 1
            assert lost_good <= lost_bad + 1e-12
    # Measured: the condition held in rounds 0 and 1 and failed in round 2 of 3.
    assert len(trace) == 4 and held == 2
    final = trace[-1]["weights"]
    lost_good = 0.9 - sum(wi for wi, b in zip(final, bad) if not b)
    lost_bad = 0.1 - sum(wi for wi, b in zip(final, bad) if b)
    assert lost_good == pytest.approx(0.0386, abs=1e-4)
    assert lost_bad == pytest.approx(0.0948, abs=1e-4)


@pytest.mark.parametrize("shift, seed", [(4.0, 0), (4.0, 1), (8.0, 0), (8.0, 1)])
def test_filter_against_the_sample_mean(shift, seed):
    """Measured on 1000 points in 10 dimensions with 10% shifted points; the true mean is 0."""
    xs, bad = contaminated_gaussian(1000, 10, 0.1, shift, seed)
    err_filter = norm(filter_mean(xs, 0.1))
    err_mean = norm(sample_mean(xs))
    err_oracle = norm(sample_mean([x for x, b in zip(xs, bad) if not b]))
    assert err_mean > 0.09 * shift
    assert err_filter < 0.25
    assert err_filter < err_mean / 1.7
    assert err_filter < err_oracle + 0.15


def test_error_does_not_grow_with_the_dimension():
    """Measured with a shift of 20: the coordinatewise median error grows with d, the filter error does not."""
    errs = {}
    for d in (5, 10, 20):
        xs, bad = contaminated_gaussian(1000, d, 0.1, 20.0, seed=3)
        oracle = norm(sample_mean([x for x, b in zip(xs, bad) if not b]))
        errs[d] = (norm(filter_mean(xs, 0.1)), norm(coordinatewise_median(xs)), norm(sample_mean(xs)), oracle)
    for d, (f, med, mean, oracle) in errs.items():
        assert f < oracle + 0.05
        assert mean > 1.9
    assert errs[5][1] < errs[10][1] < errs[20][1]
    assert errs[20][1] > 4 * errs[20][0]


def test_clean_data_gives_the_sample_mean():
    xs, _ = contaminated_gaussian(1000, 10, 0.0, 0.0, seed=7)
    trace = []
    mu = filter_mean(xs, 0.1, trace=trace)
    assert len(trace) == 1
    assert mu == pytest.approx(sample_mean(xs))
