# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-online-changepoint-detection/. The authors are listed in prov/KJZYAX.jsonl.
import math
import random
from fractions import Fraction

from bayesian_online_changepoint_detection import (
    BetaBernoulli,
    GaussianKnownVariance,
    bocpd,
    constant_hazard,
    map_run_lengths,
)


def compositions(n):
    """All ordered lists of positive segment lengths that add up to n (2^(n-1) of them)."""
    if n == 0:
        yield []
        return
    for first in range(1, n + 1):
        for rest in compositions(n - first):
            yield [first] + rest


def beta_bernoulli_marginal(seg, a, b):
    h = sum(seg)
    k = len(seg) - h
    num = math.prod((a + i for i in range(h)), start=Fraction(1)) * math.prod((b + j for j in range(k)), start=Fraction(1))
    den = math.prod((a + b + i for i in range(h + k)), start=Fraction(1))
    return num / den


def gaussian_marginal(seg, mu0, s0, s):
    """Density of a segment under x ~ N(mu0 1, s^2 I + s0^2 1 1^T), by Sherman-Morrison."""
    m = len(seg)
    d = [x - mu0 for x in seg]
    q = (sum(v * v for v in d) - s0 * s0 * sum(d) ** 2 / (s * s + m * s0 * s0)) / (s * s)
    log_det = 2 * m * math.log(s) + math.log(1 + m * s0 * s0 / (s * s))
    return math.exp(-0.5 * q - 0.5 * log_det - 0.5 * m * math.log(2 * math.pi))


def enumerate_posterior(xs, marginal, hazard, one=1):
    """P(r_n = r | x) and p(x) by summing over every segmentation of x_1..x_n."""
    n = len(xs)
    joint = {}
    for lengths in compositions(n):
        w = one
        for j, length in enumerate(lengths):
            for r in range(1, length):
                w = w * (1 - hazard(r))
            if j < len(lengths) - 1:
                w = w * hazard(length)
        pos = 0
        for length in lengths:
            w = w * marginal(xs[pos:pos + length])
            pos += length
        joint[lengths[-1]] = joint.get(lengths[-1], 0) + w
    z = sum(joint.values())
    return {r: v / z for r, v in sorted(joint.items())}, z


def test_worked_example():
    xs = [0.2, -0.5, 0.4, 3.9, 4.3, 3.6]
    post, _ = bocpd(xs, GaussianKnownVariance(0.0, 3.0, 1.0), constant_hazard(10))
    assert map_run_lengths(post) == [1, 2, 3, 1, 2, 3]
    assert abs(post[3][1] - 0.7985) < 1e-4
    assert abs(post[5][3] - 0.9394) < 1e-4


def test_edge_cases():
    post, ev = bocpd([], BetaBernoulli(), constant_hazard(5))
    assert post == [] and ev == 1
    post, ev = bocpd([1], BetaBernoulli(), constant_hazard(5))
    assert post == [{1: 1}] and ev == Fraction(1, 2)


def test_beta_bernoulli_matches_enumeration_exact():
    rng = random.Random(2007)
    hazards = [constant_hazard(Fraction(3)), constant_hazard(Fraction(7, 2)), lambda r: Fraction(1, r + 1)]
    for trial in range(120):
        n = rng.randint(1, 8)
        xs = [rng.randint(0, 1) for _ in range(n)]
        a, b = Fraction(rng.randint(1, 4)), Fraction(rng.randint(1, 4), rng.randint(1, 2))
        hz = hazards[trial % 3]
        post, ev = bocpd(xs, BetaBernoulli(a, b), hz)
        for t in range(1, n + 1):
            want, z = enumerate_posterior(xs[:t], lambda seg: beta_bernoulli_marginal(seg, a, b), hz, Fraction(1))
            assert post[t - 1] == want
        assert ev == z


def test_gaussian_matches_enumeration():
    rng = random.Random(1)
    for trial in range(500):
        n = rng.randint(1, 7)
        xs = [rng.gauss(rng.choice([0.0, 3.0]), 1.0) for _ in range(n)]
        mu0, s0, s = rng.uniform(-1, 1), rng.uniform(0.5, 3), rng.uniform(0.5, 2)
        lam = rng.uniform(2, 20)
        post, ev = bocpd(xs, GaussianKnownVariance(mu0, s0, s), constant_hazard(lam))
        want, z = enumerate_posterior(xs, lambda seg: gaussian_marginal(seg, mu0, s0, s), constant_hazard(lam))
        assert set(post[-1]) == set(want)
        assert all(abs(post[-1][r] - want[r]) < 1e-12 for r in want)
        assert abs(ev - z) <= 1e-12 * z


def test_pruning_is_close_and_keeps_few_run_lengths():
    rng = random.Random(3)
    xs = []
    for k in range(10):
        mu = rng.choice([-3.0, 0.0, 3.0])
        xs += [rng.gauss(mu, 1.0) for _ in range(30)]
    model = GaussianKnownVariance(0.0, 3.0, 1.0)
    exact, _ = bocpd(xs, model, constant_hazard(30))
    pruned, _ = bocpd(xs, model, constant_hazard(30), prune=1e-6)
    assert map_run_lengths(exact) == map_run_lengths(pruned)
    assert max(len(p) for p in pruned) <= 100
    assert len(exact[-1]) == len(xs)
    gap = max(abs(e[r] - p.get(r, 0.0)) for e, p in zip(exact, pruned) for r in e)
    assert gap < 1e-4
