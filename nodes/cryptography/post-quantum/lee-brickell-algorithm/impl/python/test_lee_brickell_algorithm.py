# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lee-brickell-algorithm/. The authors are listed in prov/XC780W.jsonl.
"""Tests for the Lee-Brickell algorithm on random binary codes.

The Lee-Brickell algorithm is an attack, not a standard, so there are no
official test vectors. The tests check the output against brute force on small
codes, and the mean number of rounds against the formula
1 / sum_{i <= p} C(k, i) C(n - k, w - i) / C(n, w). They also compare the
rounds with p = 2 against the rounds with p = 0 (Prange) on the same instances.
"""

import random
from itertools import combinations

from lee_brickell_algorithm import (
    column,
    eliminate,
    lee_brickell,
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


def independent_support(h, e, n):
    """True if the columns of H on the support of e are linearly independent."""
    cols = [column(h, c) for c in range(n) if (e >> c) & 1]
    return rank(cols) == len(cols)


def test_page_example():
    """The [7, 4] Hamming code example of the page, with p = 1."""
    h = [0b1010101, 0b1100110, 0b1111000]
    e = 1 << 4
    s = syndrome(h, e)
    assert s == 0b101
    rows, s2 = eliminate(h, s, [0, 1, 3])
    assert s2 == 0b101
    # Column 5 (index 4) after the elimination is (1, 0, 1); adding it to s' gives 0.
    assert column(rows, 4) == 0b101
    assert weight(s2 ^ column(rows, 4)) == 0
    found, rounds = lee_brickell(h, s, 7, 1, 1, random.Random(1))
    assert found == e and rounds == 1


def test_against_brute_force():
    """Every output is a true solution, and a solution is found whenever some
    solution has independent support columns."""
    rng = random.Random(2025)
    for _ in range(500):
        n = rng.randint(6, 14)
        k = rng.randint(1, n - 3)
        w = rng.randint(0, min(4, n - k + 1))
        p = rng.randint(0, 2)
        h, s, _ = random_instance(n, k, w, rng)
        sols = brute_force(h, s, n, w)
        e, _ = lee_brickell(h, s, n, w, p, rng, max_iter=2000)
        if e is not None:
            assert e in sols
        if w - p <= n - k and any(independent_support(h, x, n) for x in sols):
            assert e is not None


def test_p_zero_is_prange():
    """With p = 0 the success probability is the one of Prange."""
    from math import comb
    assert success_probability(60, 30, 6, 0) == comb(30, 6) / comb(60, 6)


def test_rounds_match_the_formula():
    """Mean rounds on random [60, 30] codes with w = 6 and p = 2."""
    rng = random.Random(4242)
    n, k, w, p, trials = 60, 30, 6, 2, 120
    total = 0
    for _ in range(trials):
        h, s, e = random_instance(n, k, w, rng)
        found, rounds = lee_brickell(h, s, n, w, p, rng)
        assert found is not None and syndrome(h, found) == s and weight(found) == w
        total += rounds
    expected = 1 / success_probability(n, k, w, p)
    assert abs(expected - 2.982) < 0.001
    assert abs(total / trials - expected) < 0.25 * expected


def test_fewer_rounds_than_prange_on_the_same_instances():
    """p = 2 needs far fewer rounds than p = 0 on the same [50, 25] instances."""
    rng = random.Random(99)
    n, k, w, trials = 50, 25, 5, 40
    prange_rounds = lb_rounds = 0
    for _ in range(trials):
        h, s, _ = random_instance(n, k, w, rng)
        _, a = lee_brickell(h, s, n, w, 0, rng)
        _, b = lee_brickell(h, s, n, w, 2, rng)
        prange_rounds += a
        lb_rounds += b
    ratio = success_probability(n, k, w, 2) / success_probability(n, k, w, 0)
    assert ratio > 10
    assert prange_rounds > 4 * lb_rounds
