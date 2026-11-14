# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-exact-test/. The authors are listed in prov/PNP35A.jsonl.

import itertools
import math
from fractions import Fraction

import pytest

from fisher_exact_test import fisher_exact, hypergeometric_weights


def test_page_examples() -> None:
    cases = {
        (4, 0, 0, 4): (Fraction(1, 70), Fraction(1), Fraction(1, 35)),
        (10, 3, 2, 15): (Fraction(619, 1330665), None, Fraction(3571, 6653325)),
        (1, 9, 11, 3): (None, Fraction(41, 29716), Fraction(41, 14858)),
        (7, 2, 3, 8): (Fraction(293, 8398), None, Fraction(293, 4199)),
        (12, 5, 7, 16): (Fraction(67703, 4989450), None, Fraction(118933, 4989450)),
    }
    for table, expected in cases.items():
        for alt, want in zip(("greater", "less", "two-sided"), expected):
            if want is not None:
                assert fisher_exact(*table, alt, exact=True) == want
                assert fisher_exact(*table, alt) == float(want)


def test_weights_are_products_of_binomials() -> None:
    for r1 in range(0, 25):
        for r2 in range(0, 25):
            for c1 in range(0, r1 + r2 + 1):
                lo, w = hypergeometric_weights(r1, r2, c1)
                want = [math.comb(r1, k) * math.comb(r2, c1 - k) for k in range(lo, min(r1, c1) + 1)]
                assert w == want
                assert sum(w) == math.comb(r1 + r2, c1)


def brute_force(a: int, b: int, c: int, d: int) -> dict[str, Fraction]:
    # Label n items; the first r1 form row 1. Every choice of the c1 items in
    # column 1 is equally likely under the null. Count the choices.
    r1, n, c1 = a + b, a + b + c + d, a + c
    counts: dict[int, int] = {}
    for chosen in itertools.combinations(range(n), c1):
        k = sum(1 for i in chosen if i < r1)
        counts[k] = counts.get(k, 0) + 1
    total = sum(counts.values())
    return {
        "greater": Fraction(sum(v for k, v in counts.items() if k >= a), total),
        "less": Fraction(sum(v for k, v in counts.items() if k <= a), total),
        "two-sided": Fraction(sum(v for v in counts.values() if v <= counts[a]), total),
    }


def test_against_enumeration_of_labelings() -> None:
    checked = 0
    for n in range(0, 9):
        for a, b, c in itertools.product(range(n + 1), repeat=3):
            d = n - a - b - c
            if d < 0:
                continue
            want = brute_force(a, b, c, d)
            for alt, value in want.items():
                assert fisher_exact(a, b, c, d, alt, exact=True) == value
            checked += 1
    assert checked == 495


def test_conditional_size_at_most_alpha() -> None:
    # For every set of margins with n <= 20, the conditional rejection
    # probability at alpha = 0.05 is at most 0.05, in exact arithmetic.
    alpha = Fraction(1, 20)
    for r1 in range(1, 11):
        for r2 in range(1, 11):
            for c1 in range(1, r1 + r2):
                lo, w = hypergeometric_weights(r1, r2, c1)
                total = sum(w)
                for alt in ("greater", "less", "two-sided"):
                    size = sum(
                        w[i]
                        for i in range(len(w))
                        if fisher_exact(lo + i, r1 - lo - i, c1 - lo - i, r2 - c1 + lo + i, alt, exact=True) <= alpha
                    )
                    assert Fraction(size, total) <= alpha


def unconditional_size(reject: list[tuple[int, int]], p: float) -> float:
    return math.fsum(
        math.comb(10, x1) * math.comb(10, x2) * p ** (x1 + x2) * (1 - p) ** (20 - x1 - x2) for x1, x2 in reject
    )


def test_unconditional_size_is_well_below_alpha() -> None:
    # Two binomial rows with 10 trials each and a common p. Measured on a grid.
    for alt, n_reject, max_size in (("two-sided", 34, 0.0127792), ("greater", 23, 0.0210953)):
        reject = [(x1, x2) for x1 in range(11) for x2 in range(11) if fisher_exact(x1, 10 - x1, x2, 10 - x2, alt) <= 0.05]
        assert len(reject) == n_reject
        sizes = [unconditional_size(reject, k / 1000) for k in range(1, 1000)]
        k = max(range(999), key=sizes.__getitem__)
        assert (k + 1) / 1000 == 0.5
        assert sizes[k] == pytest.approx(max_size, abs=1e-7)
        exact_half = Fraction(sum(math.comb(10, x1) * math.comb(10, x2) for x1, x2 in reject), 2**20)
        assert float(exact_half) == pytest.approx(sizes[k], rel=1e-12)


def rejection_probability(reject: list[tuple[int, int]], p1: float, p2: float) -> float:
    return math.fsum(
        math.comb(10, x1) * p1**x1 * (1 - p1) ** (10 - x1) * math.comb(10, x2) * p2**x2 * (1 - p2) ** (10 - x2)
        for x1, x2 in reject
    )


def test_boschloo_raised_level_and_power() -> None:
    # Boschloo: reject when Fisher's one-sided p <= t, with t the largest
    # attainable value whose unconditional size stays <= 0.05 on the grid.
    pv = {(x1, x2): fisher_exact(x1, 10 - x1, x2, 10 - x2, "greater") for x1 in range(11) for x2 in range(11)}
    grid = [k / 1000 for k in range(1, 1000)]
    best = None
    for t in sorted(set(pv.values())):
        reject = [key for key, v in pv.items() if v <= t]
        if max(rejection_probability(reject, p, p) for p in grid) > 0.05:
            break
        best = t
    assert best == pytest.approx(0.0849012, abs=1e-7)
    fisher = [key for key, v in pv.items() if v <= 0.05]
    boschloo = [key for key, v in pv.items() if v <= best]
    assert (len(fisher), len(boschloo)) == (23, 27) and set(fisher) < set(boschloo)
    assert rejection_probability(fisher, 0.7, 0.2) == pytest.approx(0.62163, abs=1e-5)
    assert rejection_probability(boschloo, 0.7, 0.2) == pytest.approx(0.73345, abs=1e-5)
    assert rejection_probability(fisher, 0.6, 0.3) == pytest.approx(0.24736, abs=1e-5)
    assert rejection_probability(boschloo, 0.6, 0.3) == pytest.approx(0.35856, abs=1e-5)


def test_symmetries() -> None:
    for table in ((3, 7, 9, 1), (5, 5, 2, 8), (0, 4, 6, 2), (12, 5, 7, 16)):
        a, b, c, d = table
        for alt in ("greater", "less", "two-sided"):
            p = fisher_exact(a, b, c, d, alt, exact=True)
            assert fisher_exact(a, c, b, d, alt, exact=True) == p  # transpose
            assert fisher_exact(d, c, b, a, alt, exact=True) == p  # swap rows and columns
        assert fisher_exact(c, d, a, b, "greater", exact=True) == fisher_exact(a, b, c, d, "less", exact=True)
        assert fisher_exact(c, d, a, b, "two-sided", exact=True) == fisher_exact(a, b, c, d, "two-sided", exact=True)


def test_large_table_is_exact() -> None:
    # Equal row totals make the null law symmetric, so the two-sided value is
    # twice the upper tail. A log-space sum gives an independent reference.
    p = fisher_exact(300, 200, 150, 350, exact=True)
    upper = fisher_exact(300, 200, 150, 350, "greater", exact=True)
    assert p == 2 * upper
    log_total = math.lgamma(1001) - math.lgamma(451) - math.lgamma(551)

    def log_w(k: int) -> float:
        return (
            math.lgamma(501) - math.lgamma(k + 1) - math.lgamma(501 - k)
            + math.lgamma(501) - math.lgamma(451 - k) - math.lgamma(51 + k)
        )

    reference = math.fsum(math.exp(log_w(k) - log_total) for k in range(300, 451))
    assert float(upper) == pytest.approx(reference, rel=1e-9)
    assert float(upper) == pytest.approx(6.702494878e-22, rel=1e-9)
    lo, w = hypergeometric_weights(500, 500, 450)
    assert sum(w) == math.comb(1000, 450)
    assert fisher_exact(300, 200, 150, 350) == float(p)


def test_errors() -> None:
    with pytest.raises(ValueError):
        fisher_exact(1, -1, 2, 3)
    with pytest.raises(ValueError):
        fisher_exact(1, 2, 3, 4, "both")
    with pytest.raises(ValueError):
        fisher_exact(1.0, 2, 3, 4)  # type: ignore[arg-type]
