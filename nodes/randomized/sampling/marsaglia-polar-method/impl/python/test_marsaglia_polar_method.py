# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marsaglia-polar-method/. The authors are listed in prov/E555BW.jsonl.

import math
import random

from marsaglia_polar_method import polar_method, polar_method_counted


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


class Fixed:
    def __init__(self, vals):
        self.vals = list(vals)

    def random(self):
        return self.vals.pop(0)


def test_example() -> None:
    # V = (0.6, 0.0) is accepted: S = 0.36, F = sqrt(-2 ln 0.36 / 0.36).
    (z1, z2), tries = polar_method_counted(Fixed([0.8, 0.5]))
    assert tries == 1 and abs(z1 - 1.4294) < 1e-4 and z2 == 0.0
    # (0.9, 0.9) is outside the disk, then (-0.3, 0.4) with S = 0.25 is accepted.
    (z1, z2), tries = polar_method_counted(Fixed([0.95, 0.95, 0.35, 0.7]))
    assert tries == 2
    assert abs(z1 - (-0.3) * math.sqrt(-2 * math.log(0.25) / 0.25)) < 1e-9
    assert abs(z2 - 0.4 * math.sqrt(-2 * math.log(0.25) / 0.25)) < 1e-9


def test_rejects_origin_and_corners() -> None:
    (z1, z2), tries = polar_method_counted(Fixed([0.5, 0.5, 0.0, 0.0, 0.75, 0.5]))
    assert tries == 3 and z2 == 0.0 and z1 > 0


def test_marginals_ks() -> None:
    rng = random.Random(2024)
    m = 40000
    ps = [polar_method(rng) for _ in range(m)]
    t = ks_threshold(m)
    assert ks_statistic([a for a, _ in ps], phi) < t
    assert ks_statistic([b for _, b in ps], phi) < t


def test_cdf_points_moments_correlation_and_tries() -> None:
    rng = random.Random(7)
    m = 100000
    ps, total = [], 0
    for _ in range(m):
        p, tries = polar_method_counted(rng)
        ps.append(p)
        total += tries
    # Tries are geometric with mean 4/pi and variance (1 - pi/4) / (pi/4)^2.
    sd = math.sqrt((1 - math.pi / 4) / (math.pi / 4) ** 2 / m)
    assert abs(total / m - 4 / math.pi) < 6 * sd
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


def test_wrong_variant_fails() -> None:
    # Forgetting the division by S in line L5 gives a wrong law.
    rng = random.Random(9)
    m = 20000
    xs = []
    while len(xs) < m:
        v1 = 2.0 * rng.random() - 1.0
        v2 = 2.0 * rng.random() - 1.0
        s = v1 * v1 + v2 * v2
        if 0.0 < s < 1.0:
            xs.append(v1 * math.sqrt(-2.0 * math.log(s)))
    assert ks_statistic(xs, phi) > ks_threshold(m)
