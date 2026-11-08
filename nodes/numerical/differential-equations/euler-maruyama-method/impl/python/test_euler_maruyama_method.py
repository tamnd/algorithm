# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-maruyama-method/. The authors are listed in prov/YNYFA8.jsonl.

import math
import random
from fractions import Fraction

import pytest

from euler_maruyama_method import coarsen, euler_maruyama, step_count

MU, SIG = 2.0, 1.0


def gbm_a(t, x):
    return MU * x


def gbm_b(t, x):
    return SIG * x


def test_worked_example():
    inc = [Fraction(3, 10), Fraction(-1, 5), Fraction(1, 10), Fraction(1, 4)]
    r = euler_maruyama(lambda t, x: 2 * x, lambda t, x: x, Fraction(0), Fraction(1),
                       Fraction(1), Fraction(1, 4), increments=inc, keep_path=True)
    assert [x for _, x in r.path] == [1, Fraction(9, 5), Fraction(117, 50),
                                      Fraction(468, 125), Fraction(819, 125)]
    assert r.x == Fraction(819, 125) and r.steps == 4 and r.evals == 4
    exact = math.exp(1.5 + 0.45)
    assert abs(exact - 7.028688) < 1e-6


def test_zero_noise_is_euler():
    r = euler_maruyama(lambda t, x: -2 * t * x * x, lambda t, x: 0.0, 0.0, 1.0, 1.0, 0.2,
                       rng=random.Random(1))
    assert abs(r.x - 0.507060) < 1e-6


def test_random_linear_sde_exact_against_product_formula():
    rng = random.Random(20241108)
    for _ in range(600):
        mu = Fraction(rng.randint(-20, 20), 10)
        sig = Fraction(rng.randint(-20, 20), 10)
        n = rng.randint(0, 6)
        h = Fraction(1, rng.randint(1, 8))
        inc = [Fraction(rng.randint(-50, 50), 100) for _ in range(n)]
        x0 = Fraction(rng.randint(-9, 9), 3)
        r = euler_maruyama(lambda t, x: mu * x, lambda t, x: sig * x, Fraction(0), x0,
                           n * h, h, increments=inc)
        want = x0
        for w in inc:
            want *= 1 + mu * h + sig * w
        assert r.x == want and r.steps == n


def test_weak_mean_exact_and_monte_carlo():
    # E[X_N] = (1 + mu h)^N exactly for geometric Brownian motion; weak error O(h)
    rng = random.Random(5)
    n, M = 8, 4000
    h = 1.0 / n
    xs = [euler_maruyama(gbm_a, gbm_b, 0.0, 1.0, 1.0, h, rng=rng).x for _ in range(M)]
    mean = sum(xs) / M
    sd = math.sqrt(sum((x - mean) ** 2 for x in xs) / (M - 1))
    assert abs(mean - (1 + MU * h) ** n) < 4 * sd / math.sqrt(M)
    weak = [math.exp(MU) - (1 + MU / 2 ** k) ** (2 ** k) for k in range(2, 9)]
    ratios = [weak[i] / weak[i + 1] for i in range(len(weak) - 1)]
    assert all(1.6 < q < 2.1 for q in ratios)


def _slope(hs, es):
    xs = [math.log(v) for v in hs]
    ys = [math.log(v) for v in es]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    return sum((p - mx) * (q - my) for p, q in zip(xs, ys)) / sum((p - mx) ** 2 for p in xs)


def test_strong_order_half_geometric_brownian_motion():
    rng = random.Random(100)
    m_paths, nf = 600, 2 ** 9
    hf = 1.0 / nf
    levels = [2, 3, 4, 5, 6]
    err = {k: 0.0 for k in levels}
    for _ in range(m_paths):
        dw = [rng.gauss(0.0, math.sqrt(hf)) for _ in range(nf)]
        exact = math.exp((MU - SIG ** 2 / 2) + SIG * sum(dw))
        for k in levels:
            inc = coarsen(dw, nf // 2 ** k)
            x = euler_maruyama(gbm_a, gbm_b, 0.0, 1.0, 1.0, 1.0 / 2 ** k, increments=inc).x
            err[k] += abs(x - exact) / m_paths
    p = _slope([2.0 ** -k for k in levels], [err[k] for k in levels])
    assert 0.35 < p < 0.75


def test_strong_order_one_additive_noise():
    # dX = -X dt + 0.5 dW: additive noise, the scheme coincides with Milstein, order 1
    rng = random.Random(3)
    m_paths, nf = 200, 2 ** 10
    hf = 1.0 / nf
    levels = [2, 3, 4, 5]
    err = {k: 0.0 for k in levels}
    a = lambda t, x: -x
    b = lambda t, x: 0.5
    for _ in range(m_paths):
        dw = [rng.gauss(0.0, math.sqrt(hf)) for _ in range(nf)]
        ref = euler_maruyama(a, b, 0.0, 1.0, 1.0, hf, increments=dw).x
        for k in levels:
            x = euler_maruyama(a, b, 0.0, 1.0, 1.0, 1.0 / 2 ** k,
                               increments=coarsen(dw, nf // 2 ** k)).x
            err[k] += abs(x - ref) / m_paths
    p = _slope([2.0 ** -k for k in levels], [err[k] for k in levels])
    assert 0.8 < p < 1.2


def test_vector_system_two_noises():
    # independent components must match scalar runs driven by the same increments
    inc = [[0.1, -0.3], [0.2, 0.05], [-0.15, 0.4]]
    a = lambda t, x: [MU * x[0], -x[1]]
    b = lambda t, x: [[SIG * x[0], 0.0], [0.0, 0.5]]
    r = euler_maruyama(a, b, 0.0, [1.0, 2.0], 0.75, 0.25, increments=inc)
    r0 = euler_maruyama(gbm_a, gbm_b, 0.0, 1.0, 0.75, 0.25, increments=[w[0] for w in inc])
    r1 = euler_maruyama(lambda t, x: -x, lambda t, x: 0.5, 0.0, 2.0, 0.75, 0.25,
                        increments=[w[1] for w in inc])
    assert r.x == pytest.approx([r0.x, r1.x])
    rs = euler_maruyama(a, b, 0.0, [1.0, 2.0], 0.75, 0.25, rng=random.Random(2))
    assert len(rs.increments) == 3 and all(len(w) == 2 for w in rs.increments)


def test_edge_cases_grid_and_variance():
    assert step_count(0.0, 1.0, 0.1) == 10
    assert step_count(0.0, 1.0, 0.3) == 4
    r = euler_maruyama(gbm_a, gbm_b, 0.0, 1.0, 0.0, 0.1)
    assert r.steps == 0 and r.x == 1.0 and r.t == 0.0
    r = euler_maruyama(lambda t, x: 1.0, lambda t, x: 0.0, 0.0, 0.0, 0.3, 1.0)
    assert r.steps == 1 and r.t == 0.3 and abs(r.x - 0.3) < 1e-15
    r = euler_maruyama(lambda t, x: 1.0, lambda t, x: 0.0, 0.0, 0.0, 1.0, 0.3)
    assert r.steps == 4 and r.t == 1.0 and abs(r.x - 1.0) < 1e-12
    # the last, shortened step must draw an increment of variance 0.1, not 0.3
    rng = random.Random(9)
    last = []
    for _ in range(3000):
        rr = euler_maruyama(lambda t, x: 0.0, lambda t, x: 1.0, 0.0, 0.0, 1.0, 0.3, rng=rng)
        last.append(rr.increments[-1])
    var = sum(w * w for w in last) / len(last)
    assert abs(var - 0.1) < 0.012
    with pytest.raises(ValueError):
        euler_maruyama(gbm_a, gbm_b, 0.0, 1.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        euler_maruyama(gbm_a, gbm_b, 0.0, 1.0, 1.0, 0.5, increments=[0.1])


def test_mean_square_stability_threshold():
    # dX = lam X dt + s X dW: E[X_(n+1)^2] = ((1 + h lam)^2 + h s^2) E[X_n^2], exactly
    lam, s = -3.0, math.sqrt(3.0)
    for h, stable in ((0.2, True), (0.5, False)):
        factor = (1 + h * lam) ** 2 + h * s * s
        assert (factor < 1) == stable
    assert 2 * lam + s * s < 0  # the exact solution is mean-square stable
