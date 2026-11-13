# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-convolution/. The authors are listed in prov/BWFWVW.jsonl.

import random
from fractions import Fraction

from discrete_convolution import convolve, convolve_indexed, convolve_mode


def as_dict(values, start):
    return {start + i: v for i, v in enumerate(values)}


def defining_sum(x: dict, h: dict, n: int, lo: int, hi: int) -> Fraction:
    """(x * h)[n] = sum over all k of x[k] h[n - k], with k over a window that holds the support."""
    return sum((x.get(k, 0) * h.get(n - k, 0) for k in range(lo, hi + 1)), Fraction(0))


def random_fraction(rng: random.Random) -> Fraction:
    return Fraction(rng.randint(-9, 9), rng.randint(1, 5))


def test_example() -> None:
    assert convolve([1, 2, 3], [4, 5]) == [4, 13, 22, 15]
    assert convolve([1, 1, 1], [1, -1]) == [1, 0, 0, -1]


def test_against_defining_double_sum() -> None:
    rng = random.Random(7101)
    for _ in range(300):
        n, m = rng.randint(1, 9), rng.randint(1, 9)
        xs, hs = rng.randint(-5, 5), rng.randint(-5, 5)
        x = [random_fraction(rng) for _ in range(n)]
        h = [random_fraction(rng) for _ in range(m)]
        y, ys = convolve_indexed(x, xs, h, hs)
        xd, hd = as_dict(x, xs), as_dict(h, hs)
        assert ys == xs + hs and len(y) == n + m - 1
        for t in range(ys - 4, ys + len(y) + 4):
            want = defining_sum(xd, hd, t, -30, 30)
            got = y[t - ys] if ys <= t < ys + len(y) else 0
            assert got == want


def test_algebra_on_finite_sequences() -> None:
    rng = random.Random(7102)
    for _ in range(100):
        a = [random_fraction(rng) for _ in range(rng.randint(1, 6))]
        b = [random_fraction(rng) for _ in range(rng.randint(1, 6))]
        c = [random_fraction(rng) for _ in range(rng.randint(1, 6))]
        assert convolve(a, b) == convolve(b, a)
        assert convolve(convolve(a, b), c) == convolve(a, convolve(b, c))
        bc = [p + q for p, q in zip(b + [0] * len(c), c + [0] * len(b))]
        lhs = convolve(a, bc)
        rhs = [p + q for p, q in zip(convolve(a, b) + [0] * 10, convolve(a, c) + [0] * 10)]
        assert lhs == rhs[:len(lhs)]
        assert convolve(a, [1]) == a
        assert convolve(a, [0, 0, 1]) == [0, 0] + a


def test_sum_and_energy_identities() -> None:
    rng = random.Random(7103)
    for _ in range(100):
        a = [rng.randint(-9, 9) for _ in range(rng.randint(1, 8))]
        b = [rng.randint(-9, 9) for _ in range(rng.randint(1, 8))]
        y = convolve(a, b)
        assert sum(y) == sum(a) * sum(b)
        alt = lambda s: sum((-1) ** i * v for i, v in enumerate(s))
        assert alt(y) == alt(a) * alt(b)


def test_modes() -> None:
    x = [1, 2, 3, 4, 5]
    h = [1, 0, -1]
    full = convolve_mode(x, h, "full")
    assert full == [1, 2, 2, 2, 2, -4, -5]
    assert convolve_mode(x, h, "same") == [2, 2, 2, 2, -4]
    assert convolve_mode(x, h, "valid") == [2, 2, 2]
    assert convolve_mode([1, 2], [1, 2, 3], "valid") == []
    assert len(convolve_mode(x, [1, 1, 1, 1], "same")) == len(x)


def test_edges() -> None:
    assert convolve([], [1, 2]) == []
    assert convolve([3], [4]) == [12]
    assert convolve([0.5, 0.25], [2.0]) == [1.0, 0.5]
    assert convolve([1j, 1], [1j]) == [-1, 1j]
