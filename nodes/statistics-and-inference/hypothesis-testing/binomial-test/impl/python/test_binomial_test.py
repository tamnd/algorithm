# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binomial-test/. The authors are listed in prov/P6MXFM.jsonl.

import itertools
import math
from fractions import Fraction

import pytest

from binomial_test import binomial_pmf, binomial_test


def exact_pmf(n: int, p: Fraction) -> list[Fraction]:
    return [math.comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n + 1)]


def exact_p_value(x: int, n: int, p: Fraction, alternative: str, rule: str) -> Fraction:
    w = exact_pmf(n, p)
    upper, lower = sum(w[x:]), sum(w[: x + 1])
    if alternative == "greater":
        return upper
    if alternative == "less":
        return lower
    if rule == "double":
        return min(Fraction(1), 2 * min(lower, upper))
    return sum(v for v in w if v <= w[x])


def test_page_examples() -> None:
    assert binomial_test(8, 10, 0.5) == pytest.approx(7 / 64, abs=1e-15)
    assert binomial_test(8, 10, 0.5, "greater") == pytest.approx(7 / 128, abs=1e-15)
    assert binomial_test(5, 10, 0.2, "greater") == pytest.approx(0.0327934976, abs=1e-12)
    assert binomial_test(5, 10, 0.2) == pytest.approx(0.0327934976, abs=1e-12)
    assert binomial_test(5, 10, 0.2, rule="double") == pytest.approx(0.0655869952, abs=1e-12)
    assert binomial_test(0, 10, 0.2) == pytest.approx(0.228248064, abs=1e-12)
    assert binomial_test(0, 10, 0.2, rule="double") == pytest.approx(0.2147483648, abs=1e-12)
    assert binomial_test(9, 12, 0.5, "greater") == pytest.approx(299 / 4096, abs=1e-15)


def test_against_exact_fractions() -> None:
    for p in (Fraction(1, 10), Fraction(1, 5), Fraction(1, 3), Fraction(1, 2), Fraction(3, 4)):
        for n in range(0, 26):
            for x in range(n + 1):
                for alternative in ("greater", "less", "two-sided"):
                    for rule in ("minlike", "double"):
                        want = exact_p_value(x, n, p, alternative, rule)
                        got = binomial_test(x, n, float(p), alternative, rule)
                        assert abs(got - float(want)) <= 1e-12, (x, n, p, alternative, rule)


def test_against_sequences() -> None:
    # Brute force: enumerate all 2^n outcome sequences of the n trials.
    p = Fraction(1, 3)
    for n in range(0, 13):
        prob = {}
        for seq in itertools.product((0, 1), repeat=n):
            k = sum(seq)
            prob[seq] = p**k * (1 - p) ** (n - k)
        for x in range(n + 1):
            greater = sum(v for s, v in prob.items() if sum(s) >= x)
            less = sum(v for s, v in prob.items() if sum(s) <= x)
            assert abs(binomial_test(x, n, 1 / 3, "greater") - float(greater)) <= 1e-12
            assert abs(binomial_test(x, n, 1 / 3, "less") - float(less)) <= 1e-12


def test_size_never_exceeds_alpha() -> None:
    # The exact null probability of the rejection region {x : p(x) <= alpha}.
    for p in (Fraction(1, 10), Fraction(1, 4), Fraction(1, 2), Fraction(2, 3)):
        for n in (1, 5, 10, 17, 30):
            w = exact_pmf(n, p)
            for alpha in (Fraction(1, 100), Fraction(1, 20), Fraction(1, 10)):
                for alternative in ("greater", "less", "two-sided"):
                    for rule in ("minlike", "double"):
                        size = sum(
                            w[x]
                            for x in range(n + 1)
                            if binomial_test(x, n, float(p), alternative, rule) <= float(alpha)
                        )
                        assert size <= alpha


def test_attained_size_example() -> None:
    w = exact_pmf(10, Fraction(1, 2))
    region = [x for x in range(11) if binomial_test(x, 10, 0.5, "greater") <= 0.05]
    assert region == [9, 10]
    assert sum(w[x] for x in region) == Fraction(11, 1024)


def test_tail_far_out() -> None:
    # The upper tail is summed directly, so a tiny p-value keeps its digits.
    want = Fraction(sum(math.comb(1000, k) for k in range(700, 1001)), 2**1000)
    got = binomial_test(700, 1000, 0.5, "greater")
    assert got == pytest.approx(float(want), rel=1e-9)
    assert got < 1e-37


def test_edges() -> None:
    assert binomial_test(0, 0, 0.3) == 1.0
    assert binomial_test(0, 5, 0.0) == 1.0
    assert binomial_test(1, 5, 0.0, "greater") == 0.0
    assert binomial_test(5, 5, 1.0) == 1.0
    assert binomial_test(4, 5, 1.0, "less") == 0.0
    assert binomial_pmf(3, 0.5) == pytest.approx([1 / 8, 3 / 8, 3 / 8, 1 / 8])
    for bad in ((6, 5, 0.5), (-1, 5, 0.5), (2, 5, 1.5)):
        with pytest.raises(ValueError):
            binomial_test(*bad)
    with pytest.raises(ValueError):
        binomial_test(2, 5, 0.5, "both")


def test_monotone_in_x() -> None:
    values = [binomial_test(x, 40, 0.3, "greater") for x in range(41)]
    assert all(a >= b for a, b in zip(values, values[1:]))
