# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/factorial-design/. The authors are listed in prov/NCP43N.jsonl.

import random
from fractions import Fraction

import pytest

from factorial_design import contrasts_direct, effect_name, effects, runs, yates

EXAMPLE = [60, 72, 54, 68, 52, 83, 45, 80]  # (1), a, b, ab, c, ac, bc, abc


def sylvester(k: int) -> list[list[int]]:
    """The 2^k x 2^k Sylvester-Hadamard matrix, H_(s, x) = (-1)^popcount(s & x)."""
    n = 2 ** k
    return [[-1 if bin(s & x).count("1") % 2 else 1 for x in range(n)] for s in range(n)]


def test_example() -> None:
    assert yates(EXAMPLE) == [514, 92, -20, 6, 6, 40, 0, 2]
    e = effects(EXAMPLE)
    assert e["I"] == 64.25 and e["A"] == 23.0 and e["B"] == -5.0 and e["AC"] == 10.0
    assert e["AB"] == 1.5 and e["C"] == 1.5 and e["BC"] == 0.0 and e["ABC"] == 0.5


def test_yates_equals_direct_contrasts() -> None:
    rng = random.Random(1)
    for k in range(0, 9):
        y = [Fraction(rng.randint(-99, 99), rng.randint(1, 9)) for _ in range(2 ** k)]
        c = yates(y)
        if k <= 6:
            assert c == contrasts_direct(y)
            continue
        # for larger k, compare a few contrasts with their definition
        for s in rng.sample(range(2 ** k), 5):
            direct = sum(v * (-1) ** (bin(s).count("1") - bin(s & x).count("1")) for x, v in enumerate(y))
            assert c[s] == direct


def test_yates_is_a_walsh_hadamard_transform() -> None:
    # Contrast s = sum_x y_x prod_{i in s} (2 bit_i(x) - 1) = (-1)^|s| sum_x (-1)^|s & x| y_x
    # (each factor in s contributes -1 when its bit is 0): H y up to the sign (-1)^|s|.
    rng = random.Random(2)
    for k in range(1, 7):
        y = [rng.randint(-50, 50) for _ in range(2 ** k)]
        h = sylvester(k)
        hy = [sum(h[s][x] * y[x] for x in range(2 ** k)) for s in range(2 ** k)]
        c = yates(y)
        assert all(c[s] == (-1) ** bin(s).count("1") * hy[s] for s in range(2 ** k))


def test_standard_order_and_orthogonality() -> None:
    r = runs(3)
    assert r[:4] == [(-1, -1, -1), (1, -1, -1), (-1, 1, -1), (1, 1, -1)]
    assert [effect_name(s) for s in range(8)] == ["I", "A", "B", "AB", "C", "AC", "BC", "ABC"]
    cols = [[1 if v == 1 else -1 for v in col] for col in zip(*r)]
    for i in range(3):
        for j in range(3):
            assert sum(a * b for a, b in zip(cols[i], cols[j])) == (8 if i == j else 0)


def test_example_passes_and_interaction() -> None:
    y = EXAMPLE
    first = [y[0] + y[1], y[2] + y[3], y[4] + y[5], y[6] + y[7], y[1] - y[0], y[3] - y[2], y[5] - y[4], y[7] - y[6]]
    assert first == [132, 122, 135, 125, 12, 14, 31, 35]
    second = [first[0] + first[1], first[2] + first[3], first[4] + first[5], first[6] + first[7],
              first[1] - first[0], first[3] - first[2], first[5] - first[4], first[7] - first[6]]
    assert second == [254, 260, 26, 66, -10, -10, 2, 4]
    # the A effect at low C and at high C; AC is half their difference
    a_low_c = ((y[1] - y[0]) + (y[3] - y[2])) / 2
    a_high_c = ((y[5] - y[4]) + (y[7] - y[6])) / 2
    assert (a_low_c, a_high_c) == (13, 33) and (a_high_c - a_low_c) / 2 == effects(y)["AC"]
    # sums of squares c^2 / N
    assert [Fraction(c * c, 8) for c in yates(y)[1:]] == [1058, 50, Fraction(9, 2), Fraction(9, 2), 200, 0, Fraction(1, 2)]


def test_factorial_against_one_factor_at_a_time() -> None:
    # Var(effect) / sigma^2 is the sum of the squared coefficients of the linear estimator.
    factorial_a = [Fraction(1 if r[0] == 1 else -1, 4) for r in runs(3)]
    assert sum(c * c for c in factorial_a) == Fraction(1, 2)  # 8 runs
    # one factor at a time: (1), a, b, c, each repeated m times; A = mean(a) - mean((1))
    for m, var in ((2, Fraction(1)), (4, Fraction(1, 2))):
        coef = [Fraction(-1, m)] * m + [Fraction(1, m)] * m
        assert sum(c * c for c in coef) == var  # 4m runs in all
    # so 16 one-factor-at-a-time runs give the precision of 8 factorial runs


def contrast_column(s: int, k: int) -> list[int]:
    col = []
    for r in runs(k):
        v = 1
        for i in range(k):
            if (s >> i) & 1:
                v *= r[i]
        col.append(v)
    return col


def test_inverse_and_parseval() -> None:
    # y = H D c / N, and sum (y - mean)^2 = sum_{s > 0} c_s^2 / N
    k, n = 3, 8
    c = yates(EXAMPLE)
    h = sylvester(k)
    back = [Fraction(sum(h[x][s] * (-1) ** bin(s).count("1") * c[s] for s in range(n)), n) for x in range(n)]
    assert back == EXAMPLE
    mean = Fraction(sum(EXAMPLE), n)
    assert sum((v - mean) ** 2 for v in EXAMPLE) == Fraction(2635, 2) == sum(Fraction(v * v, n) for v in c[1:])


def test_non_examples() -> None:
    # one factor at a time from the base run (1): A = a - (1) = 12, but A is 13 at low C and 33 at high C
    assert EXAMPLE[1] - EXAMPLE[0] == 12
    # drop the run abc: every pair of distinct contrast columns now has inner product -1
    k = 3
    cols = [contrast_column(s, k)[:-1] for s in range(8)]
    for s in range(8):
        for t in range(8):
            ip = sum(a * b for a, b in zip(cols[s], cols[t]))
            assert ip == (7 if s == t else -1)


def test_errors() -> None:
    with pytest.raises(ValueError):
        yates([1.0, 2.0, 3.0])
