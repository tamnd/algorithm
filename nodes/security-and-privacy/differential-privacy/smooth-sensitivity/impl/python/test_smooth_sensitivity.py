# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smooth-sensitivity/. The authors are listed in prov/0ZFFMP.jsonl.

import itertools
import math
import random

import dpkit
from smooth_sensitivity import (
    ball_sensitivity,
    cauchy_noise,
    laplace_noise,
    median,
    private_median_cauchy,
    private_median_laplace,
    smooth_sensitivity_median,
)


def _local_sensitivity(xs, lam):
    # Brute force: replace one value by 0 or lam (the extremes move the median the most).
    med = median(xs)
    best = 0.0
    for i in range(len(xs)):
        for v in (0, lam):
            ys = list(xs)
            ys[i] = v
            best = max(best, abs(median(ys) - med))
    return best


def _distance(a, b):
    # Replace distance between two multisets of the same size.
    ca, cb = {}, {}
    for v in a:
        ca[v] = ca.get(v, 0) + 1
    for v in b:
        cb[v] = cb.get(v, 0) + 1
    return len(a) - sum(min(c, cb.get(v, 0)) for v, c in ca.items())


def _brute_smooth(xs, beta, lam, everything):
    # Definition 2.2 of NRS: max over y of exp(-beta d(x, y)) LS(y), over all datasets on the grid.
    return max(math.exp(-beta * _distance(xs, y)) * ls for y, ls in everything)


def _all_datasets(n, lam):
    return [(y, _local_sensitivity(y, lam)) for y in itertools.combinations_with_replacement(range(lam + 1), n)]


def test_local_sensitivity_matches_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(500):
        n = rng.choice([1, 3, 5, 7])
        lam = rng.randrange(1, 10)
        xs = [rng.randrange(lam + 1) for _ in range(n)]
        assert ball_sensitivity(xs, 0, lam) == _local_sensitivity(xs, lam)


def test_smooth_sensitivity_matches_definition() -> None:
    # The closed form of NRS Proposition 3.4 against the definition, on every dataset of the grid.
    grids = {(n, lam): _all_datasets(n, lam) for n in (1, 3, 5) for lam in (1, 2, 4)}
    rng = random.Random(2)
    count = 0
    for (n, lam), everything in grids.items():
        for xs, _ in everything:
            beta = rng.choice([0.05, 0.3, 1.0, 2.5])
            got = smooth_sensitivity_median(xs, beta, lam)
            assert math.isclose(got, _brute_smooth(xs, beta, lam, everything), rel_tol=1e-12)
            count += 1
    assert count >= 100


def test_ball_sensitivity_matches_brute_force() -> None:
    # A(k, x) is the largest local sensitivity over the datasets within distance k.
    everything = _all_datasets(5, 3)
    for xs, _ in everything:
        for k in range(6):
            brute = max(ls for y, ls in everything if _distance(xs, y) <= k)
            assert ball_sensitivity(xs, k, 3) == brute


def test_smooth_bound_properties() -> None:
    # S* >= LS, and S*(x) <= exp(beta) S*(y) for neighbors (Definition 2.1 of NRS).
    rng = random.Random(3)
    for _ in range(500):
        n = rng.choice([3, 5, 9, 15])
        lam = 20
        beta = rng.choice([0.1, 0.5, 1.0])
        xs = [rng.randrange(lam + 1) for _ in range(n)]
        ys = list(xs)
        ys[rng.randrange(n)] = rng.randrange(lam + 1)
        sx = smooth_sensitivity_median(xs, beta, lam)
        sy = smooth_sensitivity_median(ys, beta, lam)
        assert sx >= _local_sensitivity(xs, lam) - 1e-12
        assert sx <= math.exp(beta) * sy * (1 + 1e-12)
        assert sy <= math.exp(beta) * sx * (1 + 1e-12)


def _cauchy_logpdf(xs, lam, epsilon):
    s = 6.0 * smooth_sensitivity_median(xs, epsilon / 6.0, lam) / epsilon
    c = median(xs)
    return lambda z: -math.log(math.pi * s) - math.log1p(((z - c) / s) ** 2)


def test_cauchy_release_is_epsilon_dp_on_a_grid() -> None:
    # Pure DP: the log density ratio of neighbors stays within epsilon at every output.
    rng = random.Random(4)
    grid = [i / 4 for i in range(-400, 481)]
    worst = 0.0
    for _ in range(150):
        n, lam = rng.choice([3, 5, 7]), 10
        epsilon = rng.choice([0.5, 1.0, 2.0])
        xs = [rng.randrange(lam + 1) for _ in range(n)]
        ys = list(xs)
        ys[rng.randrange(n)] = rng.choice([0, lam, rng.randrange(lam + 1)])
        loss = dpkit.log_ratio_grid(_cauchy_logpdf(xs, lam, epsilon), _cauchy_logpdf(ys, lam, epsilon), grid)
        assert loss <= epsilon + 1e-9
        worst = max(worst, loss / epsilon)
    assert worst > 0.15  # the analysis has slack, but the loss is not trivial


def _laplace_pdf(xs, lam, epsilon, delta):
    beta = epsilon / (2.0 * math.log(2.0 / delta))
    b = 2.0 * smooth_sensitivity_median(xs, beta, lam) / epsilon
    c = median(xs)
    return lambda z: math.exp(-abs(z - c) / b) / (2 * b)


def test_laplace_release_is_approx_dp() -> None:
    # (epsilon, delta)-DP: the hockey-stick integral, by a fine Riemann sum, is at most delta.
    rng = random.Random(5)
    h = 0.02
    grid = [-60 + h * i for i in range(int(130 / h))]
    for _ in range(25):
        n, lam = 5, 10
        epsilon, delta = rng.choice([0.5, 1.0]), 0.05
        xs = [rng.randrange(lam + 1) for _ in range(n)]
        ys = list(xs)
        ys[rng.randrange(n)] = rng.choice([0, lam])
        p, q = _laplace_pdf(xs, lam, epsilon, delta), _laplace_pdf(ys, lam, epsilon, delta)
        for a, b in ((p, q), (q, p)):
            mass = h * sum(max(0.0, a(z) - math.exp(epsilon) * b(z)) for z in grid)
            assert mass <= delta + 1e-3


def test_example_values() -> None:
    xs = list(range(101))
    lam, epsilon = 100, 1.0
    assert median(xs) == 50
    assert _local_sensitivity(xs, lam) == 1
    assert [ball_sensitivity(xs, k, lam) for k in range(6)] == [1, 2, 3, 4, 5, 6]
    s = smooth_sensitivity_median(xs, epsilon / 6, lam)
    assert math.isclose(s, 6 * math.exp(-5 / 6), rel_tol=1e-12)
    assert 15.6 < 6 * s / epsilon < 15.7


def test_noise_samplers() -> None:
    rng = random.Random(6)
    n = 20000
    cauchy = [abs(cauchy_noise(rng)) <= 1.0 for _ in range(n)]
    lap = [abs(laplace_noise(2.0, rng)) > 3.0 for _ in range(n)]
    margin = dpkit.hoeffding_margin(n, 1e-6)
    assert abs(sum(cauchy) / n - 0.5) <= margin
    assert abs(sum(lap) / n - math.exp(-1.5)) <= margin


def test_release_centers_on_the_median() -> None:
    rng = random.Random(7)
    xs = [3, 5, 5, 6, 9]
    outs = [private_median_cauchy(xs, 10, 1.0, rng) for _ in range(4001)]
    assert abs(sorted(outs)[2000] - 5) < 1.0
    outs = [private_median_laplace(xs, 10, 1.0, 1e-3, rng) for _ in range(4001)]
    assert abs(sorted(outs)[2000] - 5) < 1.0


def test_bad_parameters() -> None:
    rng = random.Random(8)
    for call in (
        lambda: median([1, 2]),
        lambda: smooth_sensitivity_median([1], 0.0, 1),
        lambda: private_median_cauchy([1], 1, 0.0, rng),
        lambda: private_median_laplace([1], 1, 1.0, 0.0, rng),
    ):
        try:
            call()
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
