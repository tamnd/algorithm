# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aitken-delta-squared/. The authors are listed in prov/3C5CRR.jsonl.

import math
import random
from fractions import Fraction as F

from aitken_delta_squared import aitken, aitken_table


def textbook(s0, s1, s2):
    """The symmetric form (s0 s2 - s1^2) / (s2 - 2 s1 + s0), used as an exact oracle."""
    return (s0 * s2 - s1 * s1) / (s2 - 2 * s1 + s0)


def test_random_against_oracle():
    rng = random.Random(1926)
    count = 0
    for _ in range(600):
        s = [F(rng.randint(-99, 99), rng.randint(1, 9)) for _ in range(rng.randint(3, 8))]
        t = aitken(s)
        assert len(t) == len(s) - 2
        for k, v in enumerate(t):
            if s[k + 2] - 2 * s[k + 1] + s[k] != 0:
                assert v == textbook(s[k], s[k + 1], s[k + 2])
                count += 1
    assert count > 2000


def test_exact_on_geometric_error():
    rng = random.Random(1964)
    for _ in range(300):
        lim = F(rng.randint(-50, 50), rng.randint(1, 7))
        c = F(rng.randint(1, 30), rng.randint(1, 7)) * rng.choice([-1, 1])
        lam = F(rng.choice([v for v in range(-9, 10) if v not in (0, 5)]), 5)  # includes |lam| > 1
        s = [lim + c * lam ** k for k in range(6)]
        assert all(v == lim for v in aitken(s))


def test_page_examples():
    assert aitken([F(1), F(2, 3), F(13, 15)]) == [F(19, 24)]
    assert aitken([F(1), F(3), F(7), F(15)]) == [F(-1), F(-1)]  # 1 + 2 + 4 + ... -> -1
    x = [1.0]
    for _ in range(2):
        x.append(math.cos(x[-1]))
    assert abs(aitken(x)[0] - 0.7280103614676171) < 1e-15


def test_linear_convergence_is_accelerated():
    # Henrici: e_{k+1} = (lam + eps_k) e_k with eps_k -> 0 and lam != 1 gives (t_k - s)/e_k -> 0
    rng = random.Random(1878)
    for _ in range(100):
        lam = rng.choice([rng.uniform(-0.99, -0.05), rng.uniform(0.05, 0.9)])
        lim, e = 0.0, rng.uniform(0.5, 1.0)  # limit 0 keeps the errors representable
        s = []
        for k in range(40):
            s.append(lim + e)
            e *= lam + 1.0 / (k + 2) ** 2
        t = aitken(s)
        ratios = [abs((t[k] - lim) / (s[k] - lim)) for k in range(10, 30)]
        assert ratios[-1] < 0.2 * ratios[0] + 1e-9
        assert ratios[-1] < 0.05


def test_leibniz_and_iteration():
    s, acc = [], F(0)
    for j in range(12):
        acc += F((-1) ** j, 2 * j + 1)
        s.append(acc)
    cols = aitken_table(s)
    assert len(cols) == 6 and len(cols[-1]) == 2
    errs = [abs(float(c[0]) - math.pi / 4) for c in cols]
    assert all(a > 10 * b for a, b in zip(errs, errs[1:]))
    assert errs[3] < 2e-6


def test_logarithmic_not_accelerated():
    # s_k = s + a/k: t_k - s = a / (2(k + 1)) exactly; only a factor 2 is gained
    s = [F(7) + F(3, k) for k in range(1, 30)]
    for k, v in enumerate(aitken(s)):
        kk = k + 1
        assert v - 7 == F(3, 2 * (kk + 1))
    acc, z, part = F(0), math.pi ** 2 / 6, []
    for j in range(1, 60):
        acc += F(1, j * j)
        part.append(acc)
    t = aitken(part)
    r = (z - float(t[50])) / (z - float(part[50]))
    assert 0.4 < r < 0.55


def test_edges_and_floating_point():
    assert aitken([]) == [] and aitken([1.0]) == [] and aitken([1.0, 2.0]) == []
    assert aitken([F(5)] * 4) == [F(5), F(5)]
    assert aitken([F(1), F(2), F(3)]) == [None]  # arithmetic: no finite limit
    assert aitken_table([F(1), F(2), F(3), F(4)]) == [[F(1), F(2), F(3), F(4)]]
    # the stable form beats the symmetric form on geometric data in floating point
    rng = random.Random(2004)
    good = bad = 0.0
    for _ in range(3000):
        lim, lam = rng.uniform(-10, 10), rng.uniform(-0.95, 0.95)
        c = rng.uniform(-1, 1) * 10 ** rng.uniform(-8, 0)
        s = [lim + c * lam ** j for j in range(3)]
        t = aitken(s)[0]
        if t is None or s[2] - 2 * s[1] + s[0] == 0:
            continue
        good += abs(t - lim)
        bad += abs(textbook(*s) - lim)
    assert good < 1e-6 and bad > 1e3 * good
