# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/statistical-static-timing-analysis/. The authors are listed in prov/XMR9Q0.jsonl.

import math
import random

import pytest

from statistical_static_timing_analysis import (
    Canonical,
    add,
    cdf,
    clark_max,
    constant,
    pdf,
    statistical_static_timing_analysis,
    timing_yield,
)


def sample(x, z, rng):
    """One sample of canonical form x for the global values z and a fresh private value."""
    return x.mean + sum(c * zi for c, zi in zip(x.coeffs, z)) + x.rand * rng.gauss(0.0, 1.0)


def monte_carlo(n, edges, at_start, m, samples, rng, target):
    """Sample every delay and compute the exact longest path to target per sample.

    The vertices are numbered in topological order."""
    into = [[] for _ in range(n)]
    for u, v, d in edges:
        into[v].append((u, d))
    values = []
    for _ in range(samples):
        z = [rng.gauss(0.0, 1.0) for _ in range(m)]
        at = [0.0] * n
        for v in range(n):
            if not into[v]:
                at[v] = sample(at_start[v], z, rng)
            else:
                at[v] = max(at[u] + sample(d, z, rng) for u, d in into[v])
        values.append(at[target])
    mu = sum(values) / samples
    sd = math.sqrt(sum((x - mu) ** 2 for x in values) / (samples - 1))
    return mu, sd, values


def random_dag(rng, n, m, spread):
    edges = []
    for v in range(1, n):
        for u in rng.sample(range(v), min(v, rng.randint(1, 3))):
            d = Canonical(rng.uniform(1.0, 4.0), tuple(rng.uniform(0.0, spread) for _ in range(m)),
                          rng.uniform(0.0, spread))
            edges.append((u, v, d))
    return edges


def test_max_of_two_independent_standard_normals():
    c, t = clark_max(Canonical(0.0, (), 1.0), Canonical(0.0, (), 1.0))
    assert t == pytest.approx(0.5)
    assert c.mean == pytest.approx(1.0 / math.sqrt(math.pi), abs=1e-12)
    assert c.variance() == pytest.approx(1.0 - 1.0 / math.pi, abs=1e-12)


def test_max_with_itself_and_with_a_shift_is_exact():
    a = Canonical(2.0, (0.3, -0.4), 0.0)
    c, t = clark_max(a, a)
    assert c == a and t == 1.0
    b = Canonical(1.5, (0.3, -0.4), 0.0)  # a - b is the constant 0.5
    c, t = clark_max(b, a)
    assert c == a and t == 0.0


def test_clark_moments_and_covariance_against_monte_carlo():
    rng = random.Random(3)
    a = Canonical(1.0, (0.8, 0.1), 0.5)
    b = Canonical(1.2, (0.3, 0.6), 0.4)
    c, t = clark_max(a, b)
    samples = 100000
    xs, z0s = [], []
    for _ in range(samples):
        z = [rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)]
        xs.append(max(sample(a, z, rng), sample(b, z, rng)))
        z0s.append(z[0])
    mu = sum(xs) / samples
    var = sum((x - mu) ** 2 for x in xs) / (samples - 1)
    cov0 = sum((x - mu) * z for x, z in zip(xs, z0s)) / (samples - 1)
    se = math.sqrt(var / samples)
    assert abs(c.mean - mu) < 4 * se
    assert abs(c.variance() - var) < 0.02 * var
    assert abs(c.coeffs[0] - cov0) < 0.02
    assert abs(c.coeffs[0] - (t * 0.8 + (1 - t) * 0.3)) < 1e-12


def test_residual_is_never_clamped():
    # Bessel's inequality: Var(max) >= sum of squared covariances with the
    # independent unit sources, so the private term needs no clamping.
    rng = random.Random(5)
    for _ in range(2000):
        m = rng.randint(0, 4)
        a = Canonical(rng.uniform(-2, 2), tuple(rng.uniform(-1, 1) for _ in range(m)), rng.uniform(0, 1))
        b = Canonical(rng.uniform(-2, 2), tuple(rng.uniform(-1, 1) for _ in range(m)), rng.uniform(0, 1))
        c, t = clark_max(a, b)
        cov = sum(x * y for x, y in zip(a.coeffs, b.coeffs))
        theta2 = a.variance() + b.variance() - 2 * cov
        if theta2 <= 1e-300:
            continue
        theta = math.sqrt(theta2)
        alpha = (a.mean - b.mean) / theta
        second = ((a.mean ** 2 + a.variance()) * cdf(alpha) + (b.mean ** 2 + b.variance()) * cdf(-alpha)
                  + (a.mean + b.mean) * theta * pdf(alpha))
        assert c.variance() == pytest.approx(second - c.mean ** 2, abs=1e-9)


def all_path_lengths(n, edges, v):
    """Brute force: lengths of all paths from a start point to v."""
    into = [[] for _ in range(n)]
    for u, w, d in edges:
        into[w].append((u, d))
    if not into[v]:
        return [0.0]
    return [x + d.mean for u, d in into[v] for x in all_path_lengths(n, edges, u)]


def test_deterministic_delays_give_the_longest_path():
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randint(2, 8)
        m = rng.randint(0, 2)
        edges = []
        for v in range(1, n):
            for u in rng.sample(range(v), min(v, rng.randint(0, 3))):
                edges.append((u, v, constant(rng.randint(-3, 9), m)))
        rng.shuffle(edges)
        start = {v: constant(0, m) for v in range(n) if all(w != v for _, w, _ in edges)}
        at = statistical_static_timing_analysis(n, edges, start)
        for v in range(n):
            assert at[v].variance() == 0.0
            assert at[v].mean == max(all_path_lengths(n, edges, v))


def test_chain_is_exact():
    rng = random.Random(13)
    m = 2
    edges = [(k, k + 1, Canonical(rng.uniform(1, 3), (rng.uniform(0, 0.5), rng.uniform(-0.5, 0.5)),
                                  rng.uniform(0, 0.5))) for k in range(6)]
    at = statistical_static_timing_analysis(7, edges, {0: constant(1.0, m)})
    mean = 1.0 + sum(d.mean for _, _, d in edges)
    coeffs = [sum(d.coeffs[i] for _, _, d in edges) for i in range(m)]
    rand2 = sum(d.rand ** 2 for _, _, d in edges)
    assert at[6].mean == pytest.approx(mean, abs=1e-12)
    assert list(at[6].coeffs) == pytest.approx(coeffs, abs=1e-12)
    assert at[6].rand ** 2 == pytest.approx(rand2, abs=1e-12)
    mu, sd, _ = monte_carlo(7, edges, {0: constant(1.0, m)}, m, 20000, rng, 6)
    assert abs(mu - mean) < 4 * sd / math.sqrt(20000)
    assert abs(sd - at[6].std()) < 0.03 * sd


def test_diamond_example():
    edges = [(0, 1, Canonical(3.0, (0.4,), 0.3)), (0, 2, Canonical(2.6, (0.1,), 0.5)),
             (1, 3, Canonical(2.0, (0.2,), 0.2)), (2, 3, Canonical(2.5, (0.3,), 0.2))]
    at = statistical_static_timing_analysis(4, edges, {0: constant(0.0, 1)})
    out = at[3]
    assert out.mean == pytest.approx(5.3235, abs=1e-4)
    assert out.coeffs[0] == pytest.approx(0.4883, abs=1e-4)
    assert out.std() == pytest.approx(0.6288, abs=1e-4)
    # Only one max of two jointly Gaussian path delays: the moments are exact.
    rng = random.Random(7)
    mu, sd, values = monte_carlo(4, edges, {0: constant(0.0, 1)}, 1, 50000, rng, 3)
    assert abs(mu - out.mean) < 4 * sd / math.sqrt(50000)
    assert abs(sd - out.std()) < 0.02 * sd
    # The shape is not Gaussian, so the yield is close but not exact.
    for q in (5.5, 6.0, 6.5):
        empirical = sum(x <= q for x in values) / len(values)
        assert abs(empirical - timing_yield(out, q)) < 0.01


def test_random_dags_against_monte_carlo():
    # Measured tolerance, not a theorem: mean and standard deviation within
    # 0.12 standard deviations of a Monte Carlo estimate with 3000 samples.
    rng = random.Random(1)
    for _ in range(12):
        n = rng.randint(4, 8)
        m = rng.randint(1, 3)
        edges = random_dag(rng, n, m, 0.5)
        at = statistical_static_timing_analysis(n, edges, {0: constant(0.0, m)})
        mu, sd, _ = monte_carlo(n, edges, {0: constant(0.0, m)}, m, 3000, rng, n - 1)
        assert abs(at[-1].mean - mu) < 0.12 * sd
        assert abs(at[-1].std() - sd) < 0.12 * sd


def test_sum_and_yield():
    a = Canonical(1.0, (0.3, 0.4), 1.2)
    b = Canonical(2.0, (0.1, -0.4), 0.5)
    s = add(a, b)
    assert s.mean == 3.0 and s.coeffs == pytest.approx((0.4, 0.0))
    assert s.rand == pytest.approx(1.3)
    assert timing_yield(s, 3.0) == pytest.approx(0.5)
    assert timing_yield(constant(2.0, 2), 2.0) == 1.0
    assert timing_yield(constant(2.0, 2), 1.9) == 0.0


def test_errors():
    d = constant(1.0, 0)
    with pytest.raises(ValueError):
        statistical_static_timing_analysis(2, [(0, 1, d), (1, 0, d)], {})
    with pytest.raises(ValueError):
        statistical_static_timing_analysis(2, [(0, 1, d)], {})
