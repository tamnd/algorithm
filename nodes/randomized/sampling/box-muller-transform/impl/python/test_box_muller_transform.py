# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/box-muller-transform/. The authors are listed in prov/D2WV7Z.jsonl.

import math
import random

from box_muller_transform import box_muller, box_muller_inverse


def phi(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def ks_statistic(xs, cdf) -> float:
    xs = sorted(xs)
    m = len(xs)
    d = 0.0
    for i, x in enumerate(xs):
        f = cdf(x)
        d = max(d, (i + 1) / m - f, f - i / m)
    return d


def ks_threshold(m: int, alpha: float = 1e-9) -> float:
    # Dvoretzky-Kiefer-Wolfowitz with Massart's constant: Pr[D > t] <= 2 exp(-2 m t^2).
    return math.sqrt(math.log(2.0 / alpha) / (2.0 * m))


def pairs(seed: int, m: int):
    rng = random.Random(seed)
    return [box_muller(rng) for _ in range(m)]


def test_example() -> None:
    rng = random.Random(1)
    z1, z2 = box_muller(rng)
    assert abs(z1 - 0.3087) < 1e-4 and abs(z2 - (-0.4396)) < 1e-4


def test_known_points() -> None:
    class Fixed:
        def __init__(self, vals):
            self.vals = list(vals)

        def random(self):
            return self.vals.pop(0)

    z1, z2 = box_muller(Fixed([0.75, 0.1]))  # U1 = 0.25, U2 = 0.1
    assert abs(z1 - 1.3471) < 1e-4 and abs(z2 - 0.9787) < 1e-4
    z1, z2 = box_muller(Fixed([1.0 - math.exp(-2.0), 0.25]))
    assert abs(z1) < 1e-12 and abs(z2 - 2.0) < 1e-12
    z1, z2 = box_muller(Fixed([0.0, 0.0]))
    assert (z1, z2) == (0.0, 0.0)


def test_inverse_round_trip() -> None:
    rng = random.Random(4)
    for _ in range(1000):
        state = rng.getstate()
        u1 = 1.0 - rng.random()
        u2 = rng.random()
        rng.setstate(state)
        z1, z2 = box_muller(rng)
        v1, v2 = box_muller_inverse(z1, z2)
        assert abs(v1 - u1) < 1e-9
        assert min(abs(v2 - u2), 1.0 - abs(v2 - u2)) < 1e-9


def test_marginals_ks() -> None:
    ps = pairs(2024, 40000)
    t = ks_threshold(40000)
    assert ks_statistic([a for a, _ in ps], phi) < t
    assert ks_statistic([b for _, b in ps], phi) < t


def test_cdf_points_moments_and_correlation() -> None:
    m = 100000
    ps = pairs(7, m)
    zs = [a for a, _ in ps] + [b for _, b in ps]
    for x in [-2.0, -1.0, 0.0, 0.5, 1.0, 2.0]:
        frac = sum(1 for z in zs if z <= x) / len(zs)
        assert abs(frac - phi(x)) < 6 * math.sqrt(0.25 / m)
    mean = sum(zs) / len(zs)
    var = sum(z * z for z in zs) / len(zs)
    kurt = sum(z ** 4 for z in zs) / len(zs)
    assert abs(mean) < 0.02 and abs(var - 1) < 0.03 and abs(kurt - 3) < 0.15
    corr = sum(a * b for a, b in ps) / m
    corr_sq = sum((a * a - 1) * (b * b - 1) for a, b in ps) / (2 * m)
    assert abs(corr) < 0.02 and abs(corr_sq) < 0.04


def test_bounded_by_float_grid() -> None:
    bound = math.sqrt(2 * 53 * math.log(2))
    assert abs(bound - 8.5717) < 1e-4
    for a, b in pairs(5, 20000):
        assert abs(a) <= bound and abs(b) <= bound


def test_wrong_variant_fails() -> None:
    # Without the factor 2 inside the root, the variance is 1/2: the KS test must reject it.
    rng = random.Random(9)
    m = 20000
    xs = []
    for _ in range(m):
        u1 = 1.0 - rng.random()
        u2 = rng.random()
        xs.append(math.sqrt(-math.log(u1)) * math.cos(2 * math.pi * u2))
    assert ks_statistic(xs, phi) > ks_threshold(m)
