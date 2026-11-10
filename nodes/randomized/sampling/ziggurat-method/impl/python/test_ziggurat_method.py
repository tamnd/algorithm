# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ziggurat-method/. The authors are listed in prov/0RX5CX.jsonl.

import math
import random

import pytest

from ziggurat_method import Ziggurat, build_table, f, normal_tail, tail_area


def phi(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def ks_statistic(xs, cdf) -> float:
    xs = sorted(xs)
    m = len(xs)
    d = 0.0
    for i, x in enumerate(xs):
        c = cdf(x)
        d = max(d, (i + 1) / m - c, c - i / m)
    return d


def ks_threshold(m: int, alpha: float = 1e-9) -> float:
    # Dvoretzky-Kiefer-Wolfowitz with Massart's constant: Pr[D > t] <= 2 exp(-2 m t^2).
    return math.sqrt(math.log(2.0 / alpha) / (2.0 * m))


class Fixed:
    """A fake generator that replays given values."""

    def __init__(self, ints, reals):
        self.ints = list(ints)
        self.reals = list(reals)

    def randrange(self, n):
        k = self.ints.pop(0)
        assert 0 <= k < n
        return k

    def random(self):
        return self.reals.pop(0)


def test_table_equal_areas_and_cover() -> None:
    n = 128
    x, y, v = build_table(n)
    # The base layer: rectangle [0, r] x [0, f(r)] plus the tail.
    assert abs(x[1] * f(x[1]) + tail_area(x[1]) - v) < 1e-15
    assert abs(x[0] * f(x[1]) - v) < 1e-15
    for i in range(1, n):
        assert abs(x[i] * (y[i + 1] - y[i]) - v) < 1e-15
        assert x[i] > x[i + 1]
        if i < n - 1:
            assert abs(y[i + 1] - f(x[i + 1])) < 1e-15
    assert x[n] == 0.0 and y[n] >= 1.0
    assert abs(v - 9.91256303526217e-3) < 1e-12


def test_published_r_misses_the_cover() -> None:
    # With the published r the top layer ends about 4e-11 below f(0) = 1.
    with pytest.raises(ValueError):
        build_table(128, 3.442619855899)


def test_example_paths() -> None:
    z = Ziggurat()
    x, y = z.x, z.y
    # Fast path in layer 5: u = 0.5 * x[5] < x[6].
    rng = Fixed([5], [0.7, 0.5])
    assert z.sample(rng) == -0.5 * x[5]
    # Layer 5, u = 0.99 * x[5] > x[6]: a low point is accepted, a high one is not.
    u = 0.99 * x[5]
    assert u > x[6] and y[5] < f(u) < y[6]
    t = (f(u) - y[5]) / (y[6] - y[5])
    rng = Fixed([5], [0.1, 0.99, t * 0.5])
    assert z.sample(rng) == u
    rng = Fixed([5, 5], [0.1, 0.99, t + (1 - t) * 0.5, 0.1, 0.5])
    assert z.sample(rng) == 0.5 * x[5]


def test_marginal_ks() -> None:
    rng = random.Random(2000)
    z = Ziggurat()
    m = 40000
    xs = [z.sample(rng) for _ in range(m)]
    assert ks_statistic(xs, phi) < ks_threshold(m)


def test_moments_cdf_points_tail_and_rates() -> None:
    rng = random.Random(5)
    z = Ziggurat()
    m = 200000
    xs, total, fast = [], 0, 0
    for _ in range(m):
        v, tries, fp = z.sample_counted(rng)
        xs.append(v)
        total += tries
        fast += fp
    for t in [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0]:
        frac = sum(1 for a in xs if a <= t) / m
        assert abs(frac - phi(t)) < 6 * math.sqrt(0.25 / m)
    mean = sum(xs) / m
    var = sum(a * a for a in xs) / m
    kurt = sum(a ** 4 for a in xs) / m
    assert abs(mean) < 0.015 and abs(var - 1) < 0.02 and abs(kurt - 3) < 0.1
    # Values beyond r come only from the tail method; their count is binomial.
    p = math.erfc(z.r / math.sqrt(2.0))
    k = sum(1 for a in xs if abs(a) > z.r)
    assert abs(k - m * p) < 6 * math.sqrt(m * p)
    # Tries per variate: N v / sqrt(pi / 2), about 1.0124.
    acc = math.sqrt(math.pi / 2.0) / (z.n * z.v)
    sd = math.sqrt((1 - acc) / acc ** 2 / m)
    assert abs(total / m - 1 / acc) < 6 * sd
    # The fast path on the first try: about 0.9724.
    pf = sum(z.x[i + 1] / z.x[i] for i in range(z.n)) / z.n
    assert abs(fast / m - pf) < 6 * math.sqrt(pf * (1 - pf) / m)


def tail_cdf(r):
    return lambda t: 1.0 - math.erfc(t / math.sqrt(2.0)) / math.erfc(r / math.sqrt(2.0))


def test_tail_method_ks() -> None:
    rng = random.Random(11)
    r = 3.44261985589
    m = 20000
    xs = [normal_tail(r, rng) for _ in range(m)]
    assert min(xs) > r
    assert ks_statistic(xs, tail_cdf(r)) < ks_threshold(m)


def test_wrong_variants_fail() -> None:
    rng = random.Random(13)
    r = 3.44261985589
    m = 20000
    # Tail without the acceptance test: r plus an exponential with rate r.
    xs = [r - math.log(1.0 - rng.random()) / r for _ in range(m)]
    assert ks_statistic(xs, tail_cdf(r)) > ks_threshold(m)
    # Layers of equal height, not equal area, chosen uniformly: the rejection
    # inside each layer is right, but the layer choice is not.
    n = 128
    w = [8.0] + [math.sqrt(-2.0 * math.log(k / n)) for k in range(1, n)]
    ys = []
    while len(ys) < m:
        k = rng.randrange(n)
        s = 1.0 if rng.random() < 0.5 else -1.0
        u = rng.random() * w[k]
        h = (k + rng.random()) / n
        if h < f(u):
            ys.append(s * u)
    assert ks_statistic(ys, phi) > ks_threshold(m)
