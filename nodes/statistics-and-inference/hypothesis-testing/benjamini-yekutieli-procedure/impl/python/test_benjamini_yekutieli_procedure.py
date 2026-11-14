# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/benjamini-yekutieli-procedure/. The authors are listed in prov/HW5E27.jsonl.

import itertools
import math
import random
import statistics
from fractions import Fraction

import pytest

from benjamini_yekutieli_procedure import by, harmonic

BH95 = [0.0001, 0.0004, 0.0019, 0.0095, 0.0201, 0.0278, 0.0298, 0.0344, 0.0459, 0.3240, 0.4262, 0.5719, 0.6528, 0.7590, 1.000]


def bh_reference(p: list, q) -> list[bool]:
    """Benjamini-Hochberg as the largest self-consistent set: S = {i : m p_i <= s q} with |S| >= s, s largest."""
    m = len(p)
    for s in range(m, 0, -1):
        chosen = [m * v <= s * q for v in p]
        if sum(chosen) >= s:
            return chosen
    return [False] * m


def test_harmonic() -> None:
    assert harmonic(4, exact=True) == Fraction(25, 12)
    assert harmonic(15) == pytest.approx(3.318228993, abs=1e-9)


def test_worked_example_by_hand() -> None:
    reject, adjusted = by(BH95, 0.05)
    # Thresholds k * 0.05 / (15 * 3.3182) = k * 0.0010046: 0.0019 <= 0.0030 passes, and 0.0095 > 0.0040,
    # ..., 0.0459 > 0.0090, 0.3240 > 0.0100 all fail, so the last passing rank is 3.
    assert [i for i, r in enumerate(reject) if r] == [0, 1, 2]
    c = harmonic(15)
    assert adjusted[:4] == pytest.approx([15 * c * 0.0001, 15 * c * 0.0004 / 2, 15 * c * 0.0019 / 3, 15 * c * 0.0095 / 4])


def test_equals_bh_at_reduced_level() -> None:
    rng = random.Random(2001)
    for _ in range(400):
        m = rng.randint(1, 12)
        p = [Fraction(rng.randint(0, 200), 1000) for _ in range(m)]
        q = Fraction(rng.randint(1, 20), 20)
        reject, adjusted = by(p, q)
        assert reject == bh_reference(p, q / harmonic(m, exact=True))
        assert reject == [a <= q for a in adjusted]


def test_floats_agree_with_fractions() -> None:
    rng = random.Random(3)
    for _ in range(300):
        m = rng.randint(1, 30)
        p = [rng.random() ** 4 for _ in range(m)]
        fp = [Fraction(v) for v in p]
        # Random floats do not fall within rounding error of a threshold, so the decisions must agree.
        assert by(p, 0.1)[0] == by(fp, Fraction(1, 10))[0]


def test_invalid_input() -> None:
    assert by([], 0.1) == ([], [])
    with pytest.raises(ValueError):
        by([0.5], 1.5)
    with pytest.raises(ValueError):
        by([-0.1], 0.1)


def worst_case_law(m: int, q: Fraction) -> list[tuple[Fraction, list]]:
    """A joint law of m valid null p-values under which BH at level q has FDR exactly q (1 + 1/2 + ... + 1/m).

    With probability q / k, choose k indices at random, set them to k q / m, and set the rest to 1.
    With the remaining probability 1 - q c_m, set all to 1. Each marginal has P(p <= k q / m) = k q / m.
    """
    law = []
    for k in range(1, m + 1):
        subsets = list(itertools.combinations(range(m), k))
        for s in subsets:
            law.append((q / k / len(subsets), [k * q / m if i in s else Fraction(1) for i in range(m)]))
    rest = 1 - q * harmonic(m, exact=True)
    assert rest >= 0
    law.append((rest, [Fraction(1)] * m))
    return law


def exact_fdr(law, procedure, m0: int) -> Fraction:
    total = Fraction(0)
    for prob, p in law:
        reject = procedure(p)
        r = sum(reject)
        if r:
            total += prob * Fraction(sum(reject[:m0]), r)
    return total


def test_bh_bound_is_attained_and_by_level_is_exact() -> None:
    for m in range(1, 6):
        q = Fraction(1, 4)
        law = worst_case_law(m, q)
        assert sum(w for w, _ in law) == 1
        for i in range(m):  # the marginals are valid and exact at the thresholds
            for u in [Fraction(j, 40) for j in range(41)]:
                assert sum(w for w, p in law if p[i] <= u) <= u
            for k in range(1, m + 1):
                assert sum(w for w, p in law if p[i] <= k * q / m) == k * q / m
        c = harmonic(m, exact=True)
        assert exact_fdr(law, lambda p: bh_reference(p, q), m) == q * c
        # The same law built for level q / c makes BY at q reach FDR exactly q.
        law_by = worst_case_law(m, q / c)
        assert exact_fdr(law_by, lambda p: by(p, q)[0], m) == q


def test_bound_under_arbitrary_dependence_exactly() -> None:
    """Null p-values uniform on {1/n, ..., 1}, coupled through random permutations of one uniform index."""
    rng = random.Random(7)
    n = 24
    for _ in range(300):
        m = rng.randint(2, 6)
        m0 = rng.randint(1, m)
        q = Fraction(rng.randint(1, 6), 20)
        perms = [rng.sample(range(1, n + 1), n) for _ in range(m)]
        alt = [Fraction(rng.randint(0, n), 4 * n) for _ in range(m - m0)]
        law = []
        for u in range(n):
            nulls = [Fraction(perms[i][u], n) for i in range(m0)]
            noise = [min(Fraction(1), a + Fraction(perms[m0 + j][u], 8 * n)) for j, a in enumerate(alt)]
            law.append((Fraction(1, n), nulls + noise))
        c = harmonic(m, exact=True)
        assert exact_fdr(law, lambda p: by(p, q)[0], m0) <= Fraction(m0, m) * q
        assert exact_fdr(law, lambda p: bh_reference(p, q), m0) <= Fraction(m0, m) * q * c


def test_monte_carlo_independent() -> None:
    """Under independence BY is BH at q / c_m, so its FDR is exactly (m0/m) q / c_m."""
    rng = random.Random(1165)
    nd = statistics.NormalDist()
    m, m0, q, reps = 20, 10, 0.2, 6000
    total = 0.0
    for _ in range(reps):
        z = [rng.gauss(0, 1) + (3.0 if i >= m0 else 0.0) for i in range(m)]
        reject, _ = by([nd.cdf(-v) for v in z], q)
        r = sum(reject)
        total += sum(reject[:m0]) / r if r else 0.0
    target = m0 / m * q / harmonic(m)
    # target = 0.0278; the false discovery proportion is in [0, 1] with mean target, so its standard deviation is
    # below sqrt(target) = 0.167 and four standard errors are below 0.009.
    assert abs(total / reps - target) < 0.009
    assert math.isclose(target, 0.02779, abs_tol=1e-4)
