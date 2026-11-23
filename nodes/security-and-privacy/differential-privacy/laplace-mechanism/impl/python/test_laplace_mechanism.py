# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplace-mechanism/. The authors are listed in prov/ZJZCN9.jsonl.

import itertools
import math
import random
from collections import Counter
from fractions import Fraction

import dpkit
from laplace_mechanism import (
    laplace_error_bound,
    laplace_from_uniform,
    laplace_log_density,
    laplace_mechanism,
    laplace_scale,
    laplace_tail,
)

UNIVERSE = (0, 1, 2)


def histogram(x):
    return [sum(1 for r in x if r == v) for v in UNIVERSE]


def all_datasets(max_n):
    for n in range(max_n + 1):
        for x in itertools.combinations_with_replacement(UNIVERSE, n):
            yield x


# ---------------------------------------------------------------- dpkit self-test


def test_dpkit_neighbors_match_multiset_distance():
    rng = random.Random(11)
    for _ in range(500):
        n = rng.randint(0, 4)
        x = tuple(rng.choice(UNIVERSE) for _ in range(n))
        cx = Counter(x)
        got = {tuple(sorted(y)) for y in dpkit.neighbors_add_remove(x, UNIVERSE)}
        assert len(got) == len(dpkit.neighbors_add_remove(x, UNIVERSE))
        want = set()
        for m in range(n - 1, n + 2):
            for y in itertools.combinations_with_replacement(UNIVERSE, max(m, 0)):
                if m < 0:
                    continue
                cy = Counter(y)
                diff = sum(abs(cx[v] - cy[v]) for v in UNIVERSE)
                if diff == 1:
                    want.add(tuple(sorted(y)))
        assert got == want
        got_r = {tuple(sorted(y)) for y in dpkit.neighbors_replace(x, UNIVERSE)}
        want_r = set()
        for y in itertools.combinations_with_replacement(UNIVERSE, n):
            cy = Counter(y)
            if sum(abs(cx[v] - cy[v]) for v in UNIVERSE) == 2:
                want_r.add(tuple(sorted(y)))
        assert got_r == want_r


def _rr_pmf(x):
    # randomized response with e^epsilon = 3 on a dataset of one bit
    v = x[0]
    return {v: Fraction(3, 4), 1 - v: Fraction(1, 4)}


def test_dpkit_randomized_response_is_exactly_ln3_dp():
    pairs = [((0,), (1,))]
    assert dpkit.max_privacy_loss(_rr_pmf((0,)), _rr_pmf((1,))) == math.log(3)
    assert dpkit.is_pure_dp(_rr_pmf, pairs, math.log(3))
    assert not dpkit.is_pure_dp(_rr_pmf, pairs, math.log(3) - 0.01)
    assert dpkit.is_approx_dp(_rr_pmf, pairs, math.log(3), 0.0)
    assert not dpkit.is_approx_dp(_rr_pmf, pairs, 0.0, 0.49)
    loss = dpkit.privacy_loss(_rr_pmf((0,)), _rr_pmf((1,)))
    assert math.isclose(loss[0], math.log(3)) and math.isclose(loss[1], -math.log(3))


def test_dpkit_hockey_stick():
    p = {0: Fraction(3, 4), 1: Fraction(1, 4)}
    q = {0: Fraction(1, 4), 1: Fraction(3, 4)}
    assert dpkit.hockey_stick(p, p, 0.0) == 0.0
    assert dpkit.hockey_stick(p, p, 1.0) == 0.0
    assert math.isclose(dpkit.hockey_stick(p, q, 0.0), 0.5)  # total variation distance
    assert dpkit.hockey_stick(p, q, math.log(3)) <= 1e-15
    assert math.isclose(dpkit.hockey_stick(p, q, math.log(2)), 0.75 - 2 * 0.25)
    assert math.isclose(dpkit.hockey_stick({0: 1.0}, {1: 1.0}, 5.0), 1.0)
    assert dpkit.max_privacy_loss({0: 1.0}, {1: 1.0}) == math.inf
    assert dpkit.max_privacy_loss({}, {1: 1.0}) == -math.inf


def test_dpkit_renyi_of_bernoulli():
    p = {0: Fraction(3, 4), 1: Fraction(1, 4)}
    q = {0: Fraction(1, 4), 1: Fraction(3, 4)}
    # order 2: ln(sum p^2 / q) = ln(9/4 + 1/12) = ln(7/3)
    assert math.isclose(dpkit.renyi_divergence(p, q, 2.0), math.log(7 / 3))
    rng = random.Random(12)
    for _ in range(500):
        a, b = rng.uniform(0.01, 0.99), rng.uniform(0.01, 0.99)
        alpha = rng.uniform(1.1, 8.0)
        closed = math.log(a**alpha * b ** (1 - alpha) + (1 - a) ** alpha * (1 - b) ** (1 - alpha)) / (alpha - 1)
        got = dpkit.renyi_divergence({1: a, 0: 1 - a}, {1: b, 0: 1 - b}, alpha)
        assert math.isclose(got, closed, rel_tol=1e-9, abs_tol=1e-12)
    # near alpha = 1 it tends to the KL divergence, which is ln(3)/2 here
    assert abs(dpkit.renyi_divergence(p, q, 1.0 + 1e-7) - math.log(3) / 2) < 1e-6
    assert dpkit.renyi_divergence({0: 1.0}, {1: 1.0}, 2.0) == math.inf


def test_dpkit_empirical_and_margin():
    assert dpkit.empirical_pmf([]) == {}
    assert dpkit.empirical_pmf([1, 1, 2, 3]) == {1: 0.5, 2: 0.25, 3: 0.25}
    assert math.isclose(dpkit.hoeffding_margin(2000, 0.01), math.sqrt(math.log(200) / 4000))
    assert dpkit.log_ratio_grid(lambda z: -abs(z), lambda z: -abs(z - 1), [-3, 0, 0.5, 4]) == 1.0


# ---------------------------------------------------------------- the Laplace mechanism


def test_check_values():
    b = laplace_scale(1.0, 0.5)
    assert b == 2.0
    assert math.isclose(2 * b * b, 8.0)
    assert math.isclose(laplace_tail(2 * math.log(10), b), 0.1)
    assert abs(2 * math.log(10) - 4.6052) < 5e-5


def test_quantile_against_cdf():
    rng = random.Random(21)

    def cdf(z, b):
        return 0.5 * math.exp(z / b) if z < 0 else 1 - 0.5 * math.exp(-z / b)

    assert laplace_from_uniform(0.0, 3.0) == 0.0
    for _ in range(500):
        b = rng.uniform(0.1, 10)
        u = rng.uniform(-0.499, 0.499)
        z = laplace_from_uniform(u, b)
        assert math.isclose(cdf(z, b), u + 0.5, rel_tol=1e-9, abs_tol=1e-12)


def _grid_check(relation, sensitivity, epsilon, n_max):
    b = laplace_scale(sensitivity, epsilon)
    grid = [(-2.0 + 0.5 * i, -2.0 + 0.5 * j, -2.0 + 0.5 * k) for i in range(0, 15, 2) for j in range(0, 15, 3) for k in range(0, 15, 3)]
    worst = 0.0
    for x in all_datasets(n_max):
        for y in relation(x, UNIVERSE):
            fx, fy = histogram(x), histogram(y)
            w = dpkit.log_ratio_grid(
                lambda z: laplace_log_density(z, fx, b),
                lambda z: laplace_log_density(z, fy, b),
                grid,
            )
            worst = max(worst, w)
    return worst


def test_privacy_on_a_grid_add_remove():
    # a histogram has l1 sensitivity 1 under add/remove
    worst = _grid_check(dpkit.neighbors_add_remove, 1.0, 0.5, 3)
    assert worst <= 0.5 + 1e-9
    assert worst >= 0.5 - 1e-9  # the bound is attained


def test_privacy_on_a_grid_replace():
    # under replace the sensitivity is 2; calibrating with 1 gives only 2 epsilon
    assert _grid_check(dpkit.neighbors_replace, 1.0, 0.5, 3) >= 1.0 - 1e-9
    assert _grid_check(dpkit.neighbors_replace, 2.0, 0.5, 3) <= 0.5 + 1e-9


def test_random_pairs_log_ratio():
    rng = random.Random(22)
    for _ in range(500):
        eps = rng.uniform(0.05, 3.0)
        b = laplace_scale(1.0, eps)
        x = tuple(rng.choice(UNIVERSE) for _ in range(rng.randint(0, 5)))
        ys = dpkit.neighbors_add_remove(x, UNIVERSE)
        y = rng.choice(ys)
        z = [rng.uniform(-6, 10) for _ in UNIVERSE]
        loss = laplace_log_density(z, histogram(x), b) - laplace_log_density(z, histogram(y), b)
        assert abs(loss) <= eps + 1e-9


def test_sampler_monte_carlo():
    rng = random.Random(23)
    n = 2000
    zs = [laplace_mechanism((), lambda x: [0.0], 1.0, 0.5, rng)[0] for _ in range(n)]
    m = dpkit.hoeffding_margin(n, 1e-3)
    tail = sum(1 for z in zs if abs(z) > 2 * math.log(10)) / n
    assert abs(tail - 0.1) <= m
    for t in (-3.0, -1.0, 0.0, 1.0, 3.0):
        cdf = 0.5 * math.exp(t / 2) if t < 0 else 1 - 0.5 * math.exp(-t / 2)
        assert abs(sum(1 for z in zs if z <= t) / n - cdf) <= m
    var = sum(z * z for z in zs) / n
    assert abs(var - 8.0) < 2.0


def test_accuracy_bound():
    rng = random.Random(24)
    x = (0, 0, 1, 2, 2, 2)
    fx = histogram(x)
    b = laplace_scale(1.0, 1.0)
    beta = 0.1
    bound = laplace_error_bound(3, b, beta)
    n = 2000
    bad = 0
    for _ in range(n):
        y = laplace_mechanism(x, histogram, 1.0, 1.0, rng)
        if max(abs(a - c) for a, c in zip(y, fx)) > bound:
            bad += 1
    assert bad / n <= beta + dpkit.hoeffding_margin(n, 1e-3)


def test_edges():
    rng = random.Random(25)
    assert laplace_mechanism((), lambda x: [], 1.0, 1.0, rng) == []
    for bad in ((0.0, 1.0), (1.0, 0.0), (-1.0, 1.0)):
        try:
            laplace_scale(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    try:
        laplace_from_uniform(-0.5, 1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
