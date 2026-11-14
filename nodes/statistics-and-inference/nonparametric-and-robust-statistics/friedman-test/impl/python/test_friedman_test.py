# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/friedman-test/. The authors are listed in prov/DRZ1M4.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from friedman_test import doubled_midranks, friedman, q_statistic, rank_sum_counts

ROWS = [[8.2, 7.1, 9.0], [6.5, 6.1, 7.4], [7.9, 7.0, 8.8], [5.5, 5.9, 6.8],
        [9.1, 8.0, 8.7], [6.8, 6.0, 7.7], [7.2, 6.9, 7.0], [8.0, 7.5, 8.5]]


def midranks(row: list[float]) -> list[Fraction]:
    return [sum(1 for t in row if t < v) + Fraction(sum(1 for t in row if t == v) + 1, 2) for v in row]


def q_direct(blocks: list[list[float]]) -> Fraction:
    """Q = (b (k - 1) / SS_W-total) x sum of squared deviations of the column mean ranks,
    computed from Fractions with no doubling: an independent formula."""
    b, k = len(blocks), len(blocks[0])
    ranks = [midranks(row) for row in blocks]
    mean = Fraction(k + 1, 2)
    col_means = [sum(r[j] for r in ranks) / b for j in range(k)]
    ss_total = sum((v - mean) ** 2 for r in ranks for v in r)
    if ss_total == 0:
        return Fraction(0)
    return b * b * (k - 1) * sum((m - mean) ** 2 for m in col_means) / ss_total


def brute_force_p(blocks: list[list[float]]) -> Fraction:
    """Permute every block in all k! ways (positions, so tied values count separately)."""
    k = len(blocks[0])
    q_obs = q_direct(blocks)
    perms = [list(itertools.permutations(row)) for row in blocks]
    hits = total = 0
    for choice in itertools.product(*perms):
        total += 1
        hits += q_direct([list(row) for row in choice]) >= q_obs
    assert total == math.factorial(k) ** len(blocks)
    return Fraction(hits, total)


def test_page_examples() -> None:
    assert q_statistic(ROWS) == Fraction(43, 4)
    assert friedman(ROWS, "exact", exact=True)[1] == Fraction(221, 93312)
    assert friedman(ROWS)[1] == pytest.approx(0.0046309187, abs=1e-9)
    rows2 = [[1, 2, 2], [3, 3, 1], [2, 1, 3], [1, 2, 3], [1, 1, 2]]
    assert q_statistic(rows2) == Fraction(42, 17)
    assert friedman(rows2, "exact", exact=True)[1] == Fraction(29, 81)


def test_two_formulas_agree() -> None:
    rng = random.Random(1)
    for _ in range(300):
        b, k = rng.randint(1, 6), rng.randint(2, 5)
        blocks = [[rng.randint(0, 3) for _ in range(k)] for _ in range(b)]
        assert q_statistic(blocks) == q_direct(blocks)


def test_untied_closed_form() -> None:
    rng = random.Random(2)
    for _ in range(100):
        b, k = rng.randint(1, 8), rng.randint(2, 6)
        blocks = [rng.sample(range(100), k) for _ in range(b)]
        col = [sum(Fraction(r, 2) for r in (doubled_midranks(row)[j] for row in blocks)) for j in range(k)]
        want = Fraction(12, b * k * (k + 1)) * sum(c * c for c in col) - 3 * b * (k + 1)
        assert q_statistic(blocks) == want


def test_exact_against_all_permutations() -> None:
    rng = random.Random(3)
    for _ in range(30):
        b, k = rng.choice([(1, 3), (2, 3), (3, 3), (4, 2), (5, 2), (2, 4), (3, 2)])
        blocks = [[rng.randint(0, 3) for _ in range(k)] for _ in range(b)]
        assert friedman(blocks, "exact", exact=True)[1] == brute_force_p(blocks)


def test_two_treatments_is_the_sign_test() -> None:
    rng = random.Random(4)
    for _ in range(100):
        b = rng.randint(1, 12)
        blocks = [rng.sample(range(50), 2) for _ in range(b)]  # no ties within a block
        s = sum(1 for x, y in blocks if y > x)
        assert q_statistic(blocks) == Fraction((2 * s - b) ** 2, b)  # (S - b/2)^2 / (b/4)
        tail = sum(math.comb(b, j) for j in range(min(s, b - s) + 1))
        assert friedman(blocks, "exact", exact=True)[1] == min(Fraction(1), Fraction(2 * tail, 2**b))


def test_exact_critical_values_k3() -> None:
    def tail(b: int, q: Fraction) -> Fraction:
        counts = rank_sum_counts([[1, 2, 3]] * b)
        hits = sum(c for s, c in counts.items()
                   if Fraction(12, 12 * b) * sum(Fraction(x, 2) ** 2 for x in s) - 12 * b >= q)
        return Fraction(hits, 6**b)

    assert tail(6, Fraction(7)) == Fraction(25, 864)  # 0.0289, the 5% point for b = 6
    assert tail(4, Fraction(5991, 1000)) == Fraction(5, 72)  # 0.0694: chi-square is liberal here
    assert sum(rank_sum_counts([[1, 2, 3]] * 5).values()) == 6**5


def test_chi_square_size_monte_carlo() -> None:
    rng = random.Random(52)
    r, alpha = 1500, 0.05
    hits = sum(friedman([[rng.gauss(0.0, 1.0) for _ in range(3)] for _ in range(20)])[1] <= alpha
               for _ in range(r))
    assert abs(hits / r - alpha) <= 4 * math.sqrt(alpha * (1 - alpha) / r)


def test_edges() -> None:
    with pytest.raises(ValueError):
        friedman([])
    with pytest.raises(ValueError):
        friedman([[1.0]])
    with pytest.raises(ValueError):
        friedman([[1.0, 2.0], [1.0]])
    assert friedman([[1.0, 1.0], [2.0, 2.0]], "exact", exact=True) == (0.0, 1)
