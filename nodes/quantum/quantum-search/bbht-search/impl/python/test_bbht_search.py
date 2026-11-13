# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bbht-search/. The authors are listed in prov/TE4YP7.jsonl.

import math
import random
from fractions import Fraction

from bbht_search import (
    LAMBDA,
    bbht_search,
    default_budget,
    grover_state,
    next_m,
    num_choices,
)

TOL = 1e-9


def marked_f(n_items: int, n_marked: int, seed: int):
    marked = set(random.Random(seed).sample(range(n_items), n_marked))
    return marked, (lambda x, s=marked: 1 if x in s else 0)


def round_success(n_items: int, n_marked: int, c: int) -> float:
    """Lemma 2: the mean of sin^2((2j + 1) theta) over 0 <= j < c."""
    theta = math.asin(math.sqrt(n_marked / n_items))
    s2 = math.sin(2 * theta)
    if s2 < 1e-12:
        return sum(math.sin((2 * j + 1) * theta) ** 2 for j in range(c)) / c
    return 0.5 - math.sin(4 * c * theta) / (4 * c * s2)


def exact_expectation(n_items: int, n_marked: int) -> tuple[float, float]:
    """E[Grover iterations] and E[rounds] of BBHT-SEARCH with no budget."""
    m = Fraction(1)
    reach = 1.0
    e_iter = 0.0
    e_rounds = 0.0
    while True:
        c = num_choices(m, n_items)
        q = round_success(n_items, n_marked, c)
        if m * m >= n_items:
            # From here on every round is the same: a geometric tail.
            return e_iter + reach * ((c - 1) / 2) / q, e_rounds + reach / q
        e_iter += reach * (c - 1) / 2
        e_rounds += reach
        reach *= 1.0 - q
        m = next_m(m, n_items)


def rounds_tail(n_items: int, n_marked: int, r: int) -> float:
    """P(no success in the first r rounds)."""
    m = Fraction(1)
    reach = 1.0
    for _ in range(r):
        reach *= 1.0 - round_success(n_items, n_marked, num_choices(m, n_items))
        m = next_m(m, n_items)
    return reach


def test_lemma2_against_simulator() -> None:
    for n_items in range(2, 33):
        for n_marked in range(0, n_items + 1):
            marked, f = marked_f(n_items, n_marked, 31 * n_items + n_marked)
            probs = [sum(abs(grover_state(n_items, f, j)[x]) ** 2 for x in marked)
                     for j in range(math.isqrt(n_items) + 2)]
            for c in range(1, len(probs) + 1):
                assert abs(sum(probs[:c]) / c - round_success(n_items, n_marked, c)) < TOL


def test_lemma2_quarter() -> None:
    # P_c >= 1/4 once c >= 1 / sin(2 theta).
    for n_items in range(2, 257):
        for n_marked in range(1, n_items):
            s2 = math.sin(2 * math.asin(math.sqrt(n_marked / n_items)))
            c = math.ceil(1 / s2)
            assert round_success(n_items, n_marked, c) >= 0.25 - TOL


def test_expected_iterations_bound() -> None:
    # Exact expectation for every N <= 256 and 1 <= M <= 3N/4:
    # E[iterations] <= 9 m0 (the bound proved on the page) and in fact
    # <= 2.4 m0, with m0 = 1 / sin(2 theta) <= sqrt(N / M).
    worst = 0.0
    for n_items in range(2, 257):
        for n_marked in range(1, 3 * n_items // 4 + 1):
            e_iter, e_rounds = exact_expectation(n_items, n_marked)
            m0 = 1 / math.sin(2 * math.asin(math.sqrt(n_marked / n_items)))
            assert m0 <= math.sqrt(n_items / n_marked) + TOL
            assert e_iter <= 9 * m0
            worst = max(worst, e_iter / m0)
            assert e_rounds <= math.log(m0, 6 / 5) + 6
    assert worst <= 2.4


def test_large_m_needs_few_rounds() -> None:
    # M > 3N/4: the first round is j = 0, a classical sample.
    for n_items in range(4, 129):
        for n_marked in range(3 * n_items // 4 + 1, n_items + 1):
            e_iter, e_rounds = exact_expectation(n_items, n_marked)
            assert e_iter + e_rounds <= 2.1


def test_example_table() -> None:
    # N = 64, M = 2: the numbers in the example of the page.
    assert [num_choices(m, 64) for m in _ms(64, 12)] == [1, 2, 2, 2, 3, 3, 3, 4, 5, 6, 7, 8]
    e_iter, e_rounds = exact_expectation(64, 2)
    assert abs(e_iter - 3.372) < 1e-3
    assert abs(e_rounds - 5.249) < 1e-3


def _ms(n_items: int, count: int) -> list[Fraction]:
    out = [Fraction(1)]
    while len(out) < count:
        out.append(next_m(out[-1], n_items))
    return out


def test_seeded_rounds_distribution() -> None:
    # N = 64, M = 2, 3000 seeded runs. Each empirical tail P(rounds > r) is
    # within the Hoeffding tolerance sqrt(ln(2 / 1e-3) / (2 * 3000)) < 0.036
    # of the exact value.
    rng = random.Random(7)
    marked, f = marked_f(64, 2, 99)
    runs = 3000
    counts = []
    for _ in range(runs):
        x, used, rounds = bbht_search(64, f, rng)
        assert x in marked
        counts.append(rounds)
    tol = math.sqrt(math.log(2 / 1e-3) / (2 * runs))
    for r in range(1, 9):
        empirical = sum(1 for c in counts if c > r) / runs
        assert abs(empirical - rounds_tail(64, 2, r)) < tol


def test_no_marked_item_hits_the_budget() -> None:
    rng = random.Random(3)
    for n_items in (16, 64):
        f = lambda x: 0
        x, used, rounds = bbht_search(n_items, f, rng)
        assert x is None
        budget = default_budget(n_items)
        assert budget <= used < budget + math.isqrt(n_items) + 1


def test_large_m_seeded() -> None:
    rng = random.Random(11)
    for n_marked in (49, 56, 64):
        marked, f = marked_f(64, n_marked, n_marked)
        for _ in range(50):
            x, used, rounds = bbht_search(64, f, rng)
            assert x in marked


def test_lambda_range() -> None:
    try:
        bbht_search(8, lambda x: 0, random.Random(0), lam=Fraction(4, 3))
    except ValueError:
        pass
    else:
        raise AssertionError("lam = 4/3 must be rejected")
    assert 1 < LAMBDA < Fraction(4, 3)
