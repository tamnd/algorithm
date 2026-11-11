# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prange-algorithm/. The authors are listed in prov/HA6A5G.jsonl.
"""Tests for Prange's algorithm on random binary codes.

Prange's algorithm is an attack, not a standard, so there are no official test
vectors. The tests check the output against brute force on small codes, and
the mean iteration count against the formula C(n, w) / C(n - k, w).
"""

import random
from itertools import combinations

from prange_algorithm import (
    eliminate,
    prange,
    rank,
    random_instance,
    success_probability,
    syndrome,
    weight,
)


def brute_force(h, s, n, w):
    """All e of weight w with H e = s (the oracle)."""
    out = []
    for pos in combinations(range(n), w):
        e = sum(1 << c for c in pos)
        if syndrome(h, e) == s:
            out.append(e)
    return out


def test_page_example():
    """The [7, 4] Hamming code example of the page."""
    # Rows of H; bit j is column j (column j is the binary form of j + 1).
    h = [0b1010101, 0b1100110, 0b1111000]
    e = 1 << 4
    s = syndrome(h, e)
    assert s == 0b101
    res = eliminate(h, s, [0, 1, 3])
    assert res is not None
    rows, s2 = res
    for i, c in enumerate([0, 1, 3]):
        for j, row in enumerate(rows):
            assert ((row >> c) & 1) == (1 if i == j else 0)
    # Column 4 is not in {0, 1, 3}: that information set fails.
    assert weight(s2) != 1
    res = eliminate(h, s, [0, 1, 4])
    rows, s2 = res
    assert weight(s2) == 1
    found, _ = prange(h, s, 7, 1, random.Random(1))
    assert found == e


def test_eliminate_keeps_the_solution_set():
    rng = random.Random(7)
    for _ in range(200):
        n, k = 12, 6
        h, s, e = random_instance(n, k, 2, rng)
        cols = rng.sample(range(n), n - k)
        res = eliminate(h, s, cols)
        if res is None:
            continue
        rows, s2 = res
        # H e = s if and only if H' e = s', because U is invertible.
        assert syndrome(rows, e) == s2


def test_singular_selection_is_rejected():
    h = [0b0111, 0b0010]
    assert eliminate(h, 0, [0, 1]) is not None
    assert eliminate(h, 0, [2, 3]) is None


def independent_support(h, e, n):
    """True if the columns of H on the support of e are linearly independent."""
    cols = []
    for c in range(n):
        if (e >> c) & 1:
            cols.append(sum(((row >> c) & 1) << i for i, row in enumerate(h)))
    return rank(cols) == len(cols)


def test_against_brute_force():
    """Prange returns a true solution, and it finds one whenever some solution
    has independent columns (a solution that uses a zero column, for example,
    lies in no information set, so Prange cannot return it)."""
    rng = random.Random(2024)
    for _ in range(500):
        n = rng.randint(6, 14)
        k = rng.randint(1, n - 3)
        w = rng.randint(0, min(3, n - k))
        h, s, _ = random_instance(n, k, w, rng)
        sols = brute_force(h, s, n, w)
        e, _ = prange(h, s, n, w, rng, max_iter=3000)
        if any(independent_support(h, x, n) for x in sols):
            assert e is not None
        if e is not None:
            assert e in sols


def test_weight_zero():
    h = [0b1011, 0b0110]
    assert prange(h, 0, 4, 0, random.Random(3)) == (0, 1)


def test_iteration_count_matches_the_formula():
    """Mean iterations on random [60, 30] codes with w = 4 against 1/P."""
    rng = random.Random(12345)
    n, k, w, trials = 60, 30, 4, 150
    total = 0
    for _ in range(trials):
        h, s, e = random_instance(n, k, w, rng)
        found, it = prange(h, s, n, w, rng)
        assert found is not None and syndrome(h, found) == s and weight(found) == w
        total += it
    expected = 1 / success_probability(n, k, w)
    assert abs(expected - 17.79) < 0.01
    assert abs(total / trials - expected) < 0.25 * expected


def test_success_probability_values():
    assert abs(success_probability(60, 30, 4) - 27405 / 487635) < 1e-15
    assert success_probability(10, 5, 6) == 0.0
