# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fritsch-carlson-monotone-interpolation/. The authors are listed in prov/YBFHVG.jsonl.
import math
import random

import pytest

from fritsch_carlson_monotone_interpolation import MonotoneCubic, monotone_slopes


def reference_slopes(x, y):
    """Independent restatement of the method, written with alpha and beta."""
    n = len(x) - 1
    h = [x[k + 1] - x[k] for k in range(n)]
    dl = [(y[k + 1] - y[k]) / h[k] for k in range(n)]
    if n == 1:
        return [dl[0], dl[0]]
    d = []
    for k in range(n + 1):
        if k == 0 or k == n:
            j = 0 if k == 0 else n - 1
            i = 1 if k == 0 else n - 2
            s = ((2 * h[j] + h[i]) * dl[j] - h[j] * dl[i]) / (h[j] + h[i])
            if (s > 0) != (dl[j] > 0) or s == 0 or dl[j] == 0:
                s = 0.0
            elif (dl[j] > 0) != (dl[i] > 0) and dl[i] != 0 and abs(s) > 3 * abs(dl[j]):
                s = 3 * dl[j]
            d.append(s)
        elif (dl[k - 1] > 0 and dl[k] > 0) or (dl[k - 1] < 0 and dl[k] < 0):
            w = h[k - 1] + h[k]
            d.append(h[k] / w * dl[k - 1] + h[k - 1] / w * dl[k])
        else:
            d.append(0.0)
    for k in range(n):
        if dl[k] == 0:
            d[k] = d[k + 1] = 0.0
            continue
        a, b = d[k] / dl[k], d[k + 1] / dl[k]
        if a * a + b * b > 9:
            t = 3 / math.sqrt(a * a + b * b)
            d[k], d[k + 1] = t * a * dl[k], t * b * dl[k]
    return d


def rand_data(rng, n, kind):
    x = sorted(rng.sample(range(-500, 500), n + 1))
    x = [v / 10 for v in x]
    if kind == "inc":
        y = sorted(rng.uniform(-5, 5) for _ in range(n + 1))
    elif kind == "flat":
        y = sorted(rng.choice([0.0, 1.0, 2.0, rng.uniform(0, 3)]) for _ in range(n + 1))
    else:
        y = [rng.uniform(-5, 5) for _ in range(n + 1)]
    return x, y


def test_slopes_match_reference():
    rng = random.Random(1980)
    for trial in range(600):
        n = rng.randint(1, 12)
        x, y = rand_data(rng, n, ("inc", "flat", "any")[trial % 3])
        got = monotone_slopes(x, y)
        ref = reference_slopes(x, y)
        for u, v in zip(got, ref):
            assert abs(u - v) <= 1e-12 * (1 + abs(v))


def test_shape_preservation():
    rng = random.Random(1984)
    for trial in range(300):
        n = rng.randint(1, 10)
        x, y = rand_data(rng, n, ("inc", "flat", "any")[trial % 3])
        s = MonotoneCubic(x, y)
        for k in range(n):
            lo, hi = min(y[k], y[k + 1]), max(y[k], y[k + 1])
            tol = 1e-12 * (1 + abs(lo) + abs(hi))
            prev = y[k]
            for i in range(1, 41):
                t = x[k] + (x[k + 1] - x[k]) * i / 40
                v = s(t)
                # no overshoot: stays within the data range of the interval
                assert lo - tol <= v <= hi + tol
                # monotone in the direction of the data
                if y[k + 1] > y[k]:
                    assert v >= prev - tol
                elif y[k + 1] < y[k]:
                    assert v <= prev + tol
                else:
                    assert abs(v - y[k]) <= tol
                prev = v


def test_interpolates_and_linear_exact():
    rng = random.Random(1977)
    for _ in range(200):
        n = rng.randint(1, 10)
        x, y = rand_data(rng, n, "any")
        s = MonotoneCubic(x, y)
        for xi, yi in zip(x, y):
            assert s(xi) == yi
        a, b = rng.uniform(-3, 3), rng.uniform(-3, 3)
        lin = MonotoneCubic(x, [a + b * v for v in x])
        for _ in range(10):
            t = rng.uniform(x[0], x[-1])
            assert abs(lin(t) - (a + b * t)) <= 1e-12 * (1 + abs(a) + abs(b) * 50)


def test_slopes_inside_circle():
    rng = random.Random(1972)
    for _ in range(300):
        n = rng.randint(2, 10)
        x, y = rand_data(rng, n, "any")
        d = monotone_slopes(x, y)
        for k in range(n):
            dl = (y[k + 1] - y[k]) / (x[k + 1] - x[k])
            if dl == 0:
                assert d[k] == 0 and d[k + 1] == 0
            else:
                a, b = d[k] / dl, d[k + 1] / dl
                assert a >= 0 and b >= 0
                assert a * a + b * b <= 9 * (1 + 1e-12)


def test_convergence_smooth_monotone():
    errs = []
    for n in (10, 20, 40, 80):
        x = [i / n for i in range(n + 1)]
        s = MonotoneCubic(x, [math.exp(v) for v in x])
        errs.append(max(abs(math.exp(t) - s(t)) for t in (i / (8 * n) for i in range(8 * n + 1))))
    for e1, e2 in zip(errs, errs[1:]):
        assert e1 / e2 > 7.0  # observed order about 3


def test_page_example():
    s = MonotoneCubic([0, 1, 2, 3, 4, 5], [0, 0.1, 0.2, 2, 2.1, 2.2])
    assert abs(s(2.5) - 1.1) < 1e-14
    assert abs(s(1.5) - 0.11663) < 1e-5
    d = monotone_slopes([0, 1, 2, 3, 4, 5], [0, 0.1, 0.2, 2, 2.1, 2.2])
    assert abs(d[1] - 0.0314054) < 1e-6 and abs(d[2] - 0.298352) < 1e-6


def test_edges():
    s = MonotoneCubic([3.0], [7.0])
    assert s(-1) == 7.0 and s(10) == 7.0
    s = MonotoneCubic([2.0, 0.0], [5.0, 1.0])  # unsorted, two nodes: linear
    assert s(1.0) == 3.0 and s(0.0) == 1.0 and s(2.0) == 5.0
    s = MonotoneCubic([3, 1, 2], [1, 0, 1])  # unsorted with a flat interval
    assert s(2.5) == 1.0
    with pytest.raises(ValueError):
        MonotoneCubic([0, 1, 1], [0, 1, 2])
    with pytest.raises(ValueError):
        MonotoneCubic([], [])
    # tiny secants do not overflow
    s = MonotoneCubic([0, 1, 2], [0, 1e-310, 1.0])
    assert all(math.isfinite(s(t / 10)) for t in range(21))
