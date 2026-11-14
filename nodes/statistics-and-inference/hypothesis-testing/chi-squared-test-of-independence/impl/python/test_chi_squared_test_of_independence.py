# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chi-squared-test-of-independence/. The authors are listed in prov/E5V169.jsonl.

import math
import random
from fractions import Fraction

import pytest

from chi_squared_test_of_independence import chi_squared_independence

TREATMENT = [[20, 15, 5], [10, 20, 30]]


def exact_pearson(table: list[list[int]]) -> Fraction:
    rows = [sum(row) for row in table]
    cols = [sum(col) for col in zip(*table)]
    n = sum(rows)
    return sum(
        (Fraction(table[i][j]) - Fraction(rows[i] * cols[j], n)) ** 2 / Fraction(rows[i] * cols[j], n)
        for i in range(len(rows))
        for j in range(len(cols))
    )


def compositions(n: int, k: int):
    if k == 1:
        yield (n,)
        return
    for first in range(n + 1):
        for rest in compositions(n - first, k - 1):
            yield (first, *rest)


def multinomial_pmf(counts: tuple[int, ...], probs: list[float]) -> float:
    coef = math.factorial(sum(counts))
    for c in counts:
        coef //= math.factorial(c)
    return coef * math.prod(p**c for p, c in zip(probs, counts))


def rejects(table: list[list[int]], **kw) -> bool:
    # A table with an empty row or column has no test; count it as not rejected.
    try:
        return chi_squared_independence(table, **kw)[2] <= 0.05
    except ValueError:
        return False


def exact_size(n: int, pr: list[float], pc: list[float], **kw) -> float:
    r, c = len(pr), len(pc)
    w = [pr[i] * pc[j] for i in range(r) for j in range(c)]
    total = 0.0
    for cnt in compositions(n, r * c):
        if rejects([list(cnt[i * c : (i + 1) * c]) for i in range(r)], **kw):
            total += multinomial_pmf(cnt, w)
    return total


def test_page_examples() -> None:
    x2, df, p = chi_squared_independence(TREATMENT)
    assert (df, x2) == (2, pytest.approx(18.650794, abs=1e-6))
    assert p == pytest.approx(8.9132e-05, rel=1e-4)
    g2, df, p = chi_squared_independence(TREATMENT, statistic="g")
    assert (df, g2) == (2, pytest.approx(19.899774, abs=1e-6))
    assert p == pytest.approx(4.7733e-05, rel=1e-4)
    x2, df, p = chi_squared_independence([[12, 5], [7, 16]])
    assert (df, x2, p) == (1, pytest.approx(6.319892, abs=1e-6), pytest.approx(0.011939, abs=1e-6))
    x2, df, p = chi_squared_independence([[12, 5], [7, 16]], yates=True)
    assert (x2, p) == (pytest.approx(4.812286, abs=1e-6), pytest.approx(0.028258, abs=1e-6))


def test_statistic_against_fractions() -> None:
    assert exact_pearson(TREATMENT) == Fraction(1175, 63)
    rng = random.Random(3)
    for _ in range(300):
        r, c = rng.randint(2, 5), rng.randint(2, 5)
        table = [[rng.randint(0, 30) for _ in range(c)] for _ in range(r)]
        if min(map(sum, table)) == 0 or min(map(sum, zip(*table))) == 0:
            continue
        x2, df, _ = chi_squared_independence(table)
        assert df == (r - 1) * (c - 1)
        assert x2 == pytest.approx(float(exact_pearson(table)), rel=1e-12, abs=1e-12)


def test_two_by_two_closed_forms() -> None:
    rng = random.Random(4)
    for _ in range(300):
        a, b, c, d = (rng.randint(0, 25) for _ in range(4))
        r1, r2, c1, c2 = a + b, c + d, a + c, b + d
        if 0 in (r1, r2, c1, c2):
            continue
        n = r1 + r2
        den = r1 * r2 * c1 * c2
        x2 = chi_squared_independence([[a, b], [c, d]])[0]
        assert x2 == pytest.approx(n * (a * d - b * c) ** 2 / den, rel=1e-12, abs=1e-12)
        # The square of the pooled two-proportion z statistic.
        p1, p2, pooled = a / r1, c / r2, c1 / n
        z = (p1 - p2) / math.sqrt(pooled * (1 - pooled) * (1 / r1 + 1 / r2))
        assert x2 == pytest.approx(z * z, rel=1e-9, abs=1e-12)
        yates = chi_squared_independence([[a, b], [c, d]], yates=True)[0]
        excess = max(0.0, abs(a * d - b * c) - n / 2)
        assert yates == pytest.approx(n * excess**2 / den, rel=1e-12, abs=1e-12)


def test_one_degree_of_freedom_tail() -> None:
    for table in ([[12, 5], [7, 16]], [[40, 10], [30, 20]], [[3, 9], [8, 1]]):
        x2, _, p = chi_squared_independence(table)
        assert p == pytest.approx(math.erfc(math.sqrt(x2 / 2)), rel=1e-9)


def test_invariance() -> None:
    rng = random.Random(5)
    for _ in range(100):
        table = [[rng.randint(1, 20) for _ in range(4)] for _ in range(3)]
        base = chi_squared_independence(table)
        transposed = [list(col) for col in zip(*table)]
        assert chi_squared_independence(transposed)[0] == pytest.approx(base[0], rel=1e-12)
        shuffled = [row[:] for row in table]
        rng.shuffle(shuffled)
        order = list(range(4))
        rng.shuffle(order)
        shuffled = [[row[j] for j in order] for row in shuffled]
        assert chi_squared_independence(shuffled)[0] == pytest.approx(base[0], rel=1e-12)
        scaled = [[3 * o for o in row] for row in table]
        assert chi_squared_independence(scaled)[0] == pytest.approx(3 * base[0], rel=1e-12)
    # A table equal to the product of its margins gives X^2 = 0 and p = 1.
    x2, _, p = chi_squared_independence([[2, 4, 6], [3, 6, 9]])
    assert x2 == pytest.approx(0.0, abs=1e-12)
    assert p == pytest.approx(1.0)


def test_exact_size_by_enumeration() -> None:
    # Multinomial sampling of n units with independent row and column variables.
    assert exact_size(20, [0.5, 0.5], [0.5, 0.5]) == pytest.approx(0.051201, abs=1e-6)
    assert exact_size(40, [0.5, 0.5], [0.5, 0.5]) == pytest.approx(0.050821, abs=1e-6)
    assert exact_size(20, [0.5, 0.5], [0.5, 0.5], yates=True) == pytest.approx(0.012779, abs=1e-6)
    assert exact_size(40, [0.5, 0.5], [0.5, 0.5], yates=True) == pytest.approx(0.020629, abs=1e-6)
    assert exact_size(40, [0.8, 0.2], [0.8, 0.2]) == pytest.approx(0.041699, abs=1e-6)
    assert exact_size(15, [0.4, 0.6], [0.2, 0.3, 0.5]) == pytest.approx(0.041959, abs=1e-6)


def test_enumeration_against_brute_force_sampling() -> None:
    rng = random.Random(6)
    pr, pc = [0.4, 0.6], [0.2, 0.3, 0.5]
    cells = [(i, j) for i in range(2) for j in range(3)]
    weights = [pr[i] * pc[j] for i, j in cells]
    runs, rejected = 20000, 0
    for _ in range(runs):
        table = [[0, 0, 0], [0, 0, 0]]
        for i, j in rng.choices(cells, weights, k=15):
            table[i][j] += 1
        rejected += rejects(table)
    size = exact_size(15, pr, pc)
    assert abs(rejected / runs - size) < 4 * math.sqrt(size * (1 - size) / runs)


def test_errors() -> None:
    with pytest.raises(ValueError):
        chi_squared_independence([[1, 2]])
    with pytest.raises(ValueError):
        chi_squared_independence([[1, 2], [3]])
    with pytest.raises(ValueError):
        chi_squared_independence([[1, -2], [3, 4]])
    with pytest.raises(ValueError):
        chi_squared_independence([[0, 0], [3, 4]])
    with pytest.raises(ValueError):
        chi_squared_independence([[1, 2, 3], [3, 4, 5]], yates=True)
    with pytest.raises(ValueError):
        chi_squared_independence([[1, 2], [3, 4]], statistic="z")
