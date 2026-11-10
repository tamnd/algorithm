# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gumbel-max-trick/. The authors are listed in prov/J19481.jsonl.

import itertools
import math
import random

import pytest

from gumbel_max_trick import (
    efraimidis_spirakis_top_k,
    gumbel_keys,
    gumbel_max,
    gumbel_top_k,
    plackett_luce,
)


def chi2(counts, probs, m):
    return sum((c - m * p) ** 2 / (m * p) for c, p in zip(counts, probs))


def test_example() -> None:
    w = [1, 2, 3, 4]
    phi = [math.log(x) for x in w]
    us = [0.3, 0.8, 0.5, 0.6]
    keys = gumbel_keys(phi, us)
    assert [round(k, 4) for k in keys] == [-0.1856, 2.1931, 1.4651, 2.058]
    order = sorted(range(4), key=keys.__getitem__, reverse=True)
    assert order == [1, 3, 2, 0]
    assert efraimidis_spirakis_top_k(w, us, 4) == order


def test_integral_formula() -> None:
    # Pr[argmax = i] = integral of w_i e^{-m} exp(-W e^{-m}) dm = w_i / W, by quadrature.
    w = [1.0, 2.0, 3.0, 4.0]
    W = sum(w)
    a, b, steps = -10.0, 40.0, 200000
    h = (b - a) / steps
    for wi in w:
        s = 0.0
        for j in range(steps + 1):
            m = a + j * h
            c = 0.5 if j in (0, steps) else 1.0
            s += c * wi * math.exp(-m) * math.exp(-W * math.exp(-m))
        assert abs(s * h - wi / W) < 1e-6


def test_same_order_as_efraimidis_spirakis() -> None:
    rng = random.Random(2006)
    for _ in range(2000):
        n = rng.randint(1, 8)
        w = [rng.uniform(0.1, 5.0) for _ in range(n)]
        us = [rng.random() or 0.5 for _ in range(n)]
        keys = gumbel_keys([math.log(x) for x in w], us)
        order = sorted(range(n), key=keys.__getitem__, reverse=True)
        assert efraimidis_spirakis_top_k(w, us, n) == order


def test_argmax_chi_squared() -> None:
    rng = random.Random(1954)
    w = [1, 2, 3, 4, 0.5]
    W = sum(w)
    m = 50000
    counts = [0] * len(w)
    for _ in range(m):
        counts[gumbel_max([math.log(x) for x in w], rng)] += 1
    assert chi2(counts, [x / W for x in w], m) < 45.0  # 4 degrees of freedom


def test_unnormalized_shift_invariance() -> None:
    # Adding a constant to every log weight does not change the argmax for the same noise.
    rng = random.Random(5)
    for _ in range(500):
        phi = [rng.uniform(-3, 3) for _ in range(5)]
        us = [rng.random() or 0.5 for _ in range(5)]
        k1 = gumbel_keys(phi, us)
        k2 = gumbel_keys([p + 100.0 for p in phi], us)
        assert max(range(5), key=k1.__getitem__) == max(range(5), key=k2.__getitem__)


def test_top_k_is_plackett_luce() -> None:
    rng = random.Random(2019)
    w = [1, 2, 3, 4]
    phi = [math.log(x) for x in w]
    m = 60000
    pairs = list(itertools.permutations(range(4), 2))
    counts = {p: 0 for p in pairs}
    for _ in range(m):
        s = gumbel_top_k(phi, 2, rng)
        assert len(set(s)) == 2
        counts[tuple(s)] += 1
    probs = [plackett_luce(w, p) for p in pairs]
    assert abs(sum(probs) - 1.0) < 1e-12
    assert chi2([counts[p] for p in pairs], probs, m) < 60.0  # 11 degrees of freedom


def test_wrong_noise_fails() -> None:
    # Exponential noise instead of Gumbel noise does not give w_i / W.
    rng = random.Random(9)
    w = [1, 2, 3, 4]
    W = sum(w)
    m = 50000
    counts = [0] * 4
    for _ in range(m):
        keys = [math.log(x) - math.log(1.0 - rng.random()) for x in w]
        counts[max(range(4), key=keys.__getitem__)] += 1
    assert chi2(counts, [x / W for x in w], m) > 45.0


def test_errors() -> None:
    with pytest.raises(ValueError):
        gumbel_top_k([0.0, 0.0], 3, random.Random(0))
