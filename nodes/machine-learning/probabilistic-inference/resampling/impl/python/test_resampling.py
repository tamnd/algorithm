# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/resampling/. The authors are listed in prov/DF7EPS.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

from resampling import SCHEMES, ess, multinomial_resample, residual_resample, stratified_resample, systematic_resample


class GridRng:
    """Returns the given uniforms in order, as exact fractions."""

    def __init__(self, values):
        self.values = list(values)
        self.k = 0

    def random(self):
        v = self.values[self.k]
        self.k += 1
        return v


def draws_and_grid(name, w):
    """The number of uniforms a scheme uses, and a grid size M such that all
    breakpoints of the output as a function of each uniform are multiples of 1/M."""
    n = len(w)
    d = math.lcm(*[x.denominator for x in w])
    if name == "systematic":
        return 1, d
    if name == "residual":
        r = n - sum(int(n * x) for x in w)
        return r, d * max(r, 1)
    return n, d


def exact_moments(name, w):
    """E[N_i] and E[N_i N_j] by enumeration of the midpoints of all grid cells.
    The output is constant on each cell, so the averages are exact."""
    n = len(w)
    k, m = draws_and_grid(name, w)
    mids = [F(2 * a + 1, 2 * m) for a in range(m)]
    total = 0
    mean = [F(0)] * n
    second = [[F(0)] * n for _ in range(n)]
    for us in itertools.product(mids, repeat=k):
        rng = GridRng(us)
        idx = SCHEMES[name](w, rng)
        assert rng.k == k and len(idx) == n
        cnt = [0] * n
        for i in idx:
            cnt[i] += 1
        for i in range(n):
            mean[i] += cnt[i]
            for j in range(n):
                second[i][j] += cnt[i] * cnt[j]
        total += 1
    mean = [x / total for x in mean]
    cov = [[second[i][j] / total - mean[i] * mean[j] for j in range(n)] for i in range(n)]
    return mean, cov


def var_of(cov, f):
    n = len(f)
    return sum(f[i] * cov[i][j] * f[j] for i in range(n) for j in range(n))


EXAMPLES = [
    [F(1, 6), F(1, 3), F(1, 2)],
    [F(1, 10), F(2, 10), F(3, 10), F(4, 10)],
    [F(1, 8), F(1, 8), F(1, 8), F(5, 8)],
    [F(0), F(3, 4), F(1, 4)],
    [F(1, 4)] * 4,
]


def test_unbiased_exact() -> None:
    for w in EXAMPLES:
        n = len(w)
        for name in SCHEMES:
            mean, _ = exact_moments(name, w)
            assert mean == [n * x for x in w], (name, w)


def test_variance_ordering_exact() -> None:
    fs_cache = {}
    for w in EXAMPLES:
        n = len(w)
        cov = {name: exact_moments(name, w)[1] for name in SCHEMES}
        fs = [list(f) for f in itertools.product([0, 1, 2], repeat=n)]
        for f in fs:
            vm = var_of(cov["multinomial"], f)
            m1 = sum(a * b for a, b in zip(w, f))
            m2 = sum(a * b * b for a, b in zip(w, f))
            assert vm == n * (m2 - m1 * m1)
            assert var_of(cov["residual"], f) <= vm
            assert var_of(cov["stratified"], f) <= vm
        fs_cache[tuple(w)] = cov
    # The contrived case: systematic is worse than multinomial.
    w = (F(1, 8), F(1, 8), F(1, 8), F(5, 8))
    f = [0, 1, 0, 1]
    cov = fs_cache[w]
    assert var_of(cov["systematic"], f) == 1
    assert var_of(cov["multinomial"], f) == F(3, 4)
    assert var_of(cov["stratified"], f) == F(1, 2)
    assert var_of(cov["residual"], f) == F(1, 2)


def test_floor_or_ceil() -> None:
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(1, 12)
        raw = [rng.randint(0, 9) for _ in range(n)]
        if sum(raw) == 0:
            raw[0] = 1
        w = [F(x, sum(raw)) for x in raw]
        u = F(rng.randint(0, 999), 1000)
        cnt = [0] * n
        for i in systematic_resample(w, GridRng([u])):
            cnt[i] += 1
        for i in range(n):
            assert math.floor(n * w[i]) <= cnt[i] <= math.ceil(n * w[i])
        cnt = [0] * n
        for i in residual_resample(w, rng):
            cnt[i] += 1
        for i in range(n):
            assert cnt[i] >= math.floor(n * w[i])


def test_shape_and_zero_weights() -> None:
    rng = random.Random(1)
    for name, fn in SCHEMES.items():
        assert fn([1.0], rng) == [0]
        idx = fn([0.0, 1.0, 0.0], rng)
        assert idx == [1, 1, 1], name
        w = [rng.random() for _ in range(50)]
        s = sum(w)
        w = [x / s for x in w]
        idx = fn(w, rng)
        assert len(idx) == 50 and idx == sorted(idx)
        assert all(0 <= i < 50 for i in idx)


def test_float_means() -> None:
    w = [0.05, 0.15, 0.3, 0.5]
    for name, fn in SCHEMES.items():
        rng = random.Random(42)
        reps = 4000
        cnt = [0] * 4
        for _ in range(reps):
            for i in fn(w, rng):
                cnt[i] += 1
        for i in range(4):
            assert abs(cnt[i] / reps - 4 * w[i]) < 0.05, name


def test_ess() -> None:
    assert ess([F(1, 4)] * 4) == 4
    assert ess([F(1), F(0), F(0)]) == 1
    assert ess([F(1, 2), F(1, 4), F(1, 4)]) == F(8, 3)
