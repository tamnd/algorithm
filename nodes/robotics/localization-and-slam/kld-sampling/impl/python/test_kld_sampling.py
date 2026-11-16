# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kld-sampling/. The authors are listed in prov/ZKY15F.jsonl.

import bisect
import math
import random

import pytest

from kld_sampling import kld_bound, kld_mcl


def gamma_p(a, x):
    """The regularized lower incomplete gamma function P(a, x), by its series."""
    if x <= 0.0:
        return 0.0
    term = 1.0 / a
    s = term
    n = 0
    while abs(term) > 1e-17 * abs(s):
        n += 1
        term *= x / (a + n)
        s += term
    return s * math.exp(-x + a * math.log(x) - math.lgamma(a))


def chi2_quantile(dof, p):
    """The p quantile of the chi-square distribution, by bisection on its CDF."""
    lo, hi = 0.0, dof + 20.0 * math.sqrt(dof) + 50.0
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if gamma_p(dof / 2.0, mid / 2.0) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def test_chi2_quantile_helper_matches_known_values():
    assert chi2_quantile(1, 0.99) == pytest.approx(6.635, abs=1e-3)
    assert chi2_quantile(2, 0.99) == pytest.approx(9.210, abs=1e-3)
    assert chi2_quantile(3, 0.95) == pytest.approx(7.815, abs=1e-3)


def test_wilson_hilferty_is_close_to_the_exact_bound():
    eps = 0.05
    for delta in (0.01, 0.05, 0.1):
        for k in list(range(2, 12)) + [20, 50, 100, 300, 1000]:
            exact = chi2_quantile(k - 1, 1.0 - delta) / (2.0 * eps)
            # the approximation is worst for 1 degree of freedom
            rel = 0.03 if k == 2 else (0.015 if k <= 4 else 0.005)
            assert kld_bound(k, eps, delta) == pytest.approx(exact, rel=rel)


def test_bound_grows_with_k_and_shrinks_with_epsilon():
    values = [kld_bound(k, 0.05, 0.01) for k in range(1, 200)]
    assert values[0] == 0.0
    assert all(a < b for a, b in zip(values, values[1:]))
    assert kld_bound(20, 0.1, 0.01) == pytest.approx(kld_bound(20, 0.05, 0.01) / 2.0)
    # for large k, the bound is about (k - 1) / (2 epsilon)
    assert kld_bound(5001, 0.05, 0.01) / (5000 / 0.1) == pytest.approx(1.0, abs=0.05)
    with pytest.raises(ValueError):
        kld_bound(5, 0.0, 0.01)


def kl(p_hat, p):
    return sum(a * math.log(a / b) for a, b in zip(p_hat, p) if a > 0.0)


def test_bound_gives_the_coverage_asymptotically():
    # Draw n = the bound samples from a fixed distribution over k bins.
    # The KL divergence from the histogram to the true distribution is at
    # most epsilon in about 1 - delta of the trials (a large-n result).
    rng = random.Random(4)
    p = [0.05, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2]
    k, eps, delta = len(p), 0.05, 0.1
    n = math.ceil(kld_bound(k, eps, delta))
    cum = [sum(p[: i + 1]) for i in range(k)]
    trials, good = 1500, 0
    for _ in range(trials):
        c = [0] * k
        for _ in range(n):
            c[min(bisect.bisect_left(cum, rng.random()), k - 1)] += 1
        if kl([v / n for v in c], p) <= eps:
            good += 1
    assert 0.86 <= good / trials <= 0.94


# A ring of 30 m with a color in each 1 m cell; the bins are the cells.
C = 30
_R = random.Random(3)
COLORS = [_R.randrange(4) for _ in range(C)]


def color(x):
    return COLORS[int(x) % C]


def likelihood(z, x):
    return 0.85 if color(x) == z else 0.05


def motion(rng, x, u):
    return (x + u + rng.gauss(0.0, 0.1)) % C


def sense(rng, x):
    if rng.random() < 0.85:
        return color(x)
    return rng.choice([c for c in range(4) if c != color(x)])


def bin_of(x):
    return int(x * 2.0)  # bins of 0.5 m


def test_particles_shrink_when_the_belief_concentrates():
    rng = random.Random(2)
    belief = [(rng.uniform(0, C), 1.0) for _ in range(5000)]
    truth = 0.3
    sizes = []
    for _ in range(25):
        truth = motion(rng, truth, 1.0)
        belief = kld_mcl(belief, 1.0, sense(rng, truth), motion, likelihood, bin_of, rng)
        sizes.append(len(belief))
    assert sizes[0] > 800  # the global phase occupies all 60 bins: the bound is 872
    assert max(sizes[-5:]) < 200  # tracking occupies a few bins
    mean = sum(x * w for x, w in belief) / sum(w for _, w in belief)
    assert abs(mean - truth) < 0.5


def test_n_min_and_n_max():
    rng = random.Random(0)
    belief = [(5.2, 1.0)]
    # a still robot with no noise keeps one bin, so n_min particles are drawn
    out = kld_mcl(belief, 0.0, 0, lambda r, x, u: x, likelihood, bin_of, rng, n_min=10)
    assert len(out) == 10
    belief = [(rng.uniform(0, C), 1.0) for _ in range(100)]
    out = kld_mcl(belief, 0.0, 0, lambda r, x, u: r.uniform(0, 1000), likelihood, lambda x: int(x), rng, n_max=500)
    assert len(out) == 500
    with pytest.raises(ValueError):
        kld_mcl([(0.0, 0.0)], 0.0, 0, motion, likelihood, bin_of, rng)


def test_the_count_stops_at_the_bound():
    # The samples fill 20 bins in turn, so k reaches 20 after 20 samples and
    # the sampler stops at the first count that reaches the bound for k = 20.
    rng = random.Random(1)
    counter = iter(range(10 ** 6))
    out = kld_mcl([(0.0, 1.0)], 0.0, 0, lambda r, x, u: next(counter), lambda z, x: 1.0, lambda x: x % 20, rng, epsilon=0.05, delta=0.05)
    assert len(out) == math.ceil(kld_bound(20, 0.05, 0.05))
