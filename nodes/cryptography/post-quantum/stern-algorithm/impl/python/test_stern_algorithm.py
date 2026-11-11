# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stern-algorithm/. The authors are listed in prov/3YXVP5.jsonl.
"""Tests for Stern's algorithm on random binary codes.

Stern's algorithm is an attack, not a standard, so there are no official test
vectors. The tests check the output against brute force on small codes, the
mean number of rounds against the formula, and the work against the
Lee-Brickell algorithm on the same instances.
"""

import random
from itertools import combinations

from stern_algorithm import (
    column,
    eliminate,
    lee_brickell,
    rank,
    random_instance,
    stern,
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


def findable(h, x, n, p, l):
    """True if some round of Stern can return the solution x: there is a set
    S2 of 2p support positions such that the other support columns are
    independent, the columns outside S2 have rank r, and w - 2p <= r - l."""
    r = len(h)
    supp = [c for c in range(n) if (x >> c) & 1]
    if len(supp) - 2 * p > r - l or 2 * p > n - r:
        return False
    for s2 in combinations(supp, 2 * p):
        s1 = [column(h, c) for c in supp if c not in s2]
        rest = [column(h, c) for c in range(n) if c not in s2]
        if rank(s1) == len(s1) and rank(rest) == r:
            return True
    return False


def test_page_example():
    """The worked example of the page: a [8, 4] code, w = 3, p = 1, l = 1."""
    h = [0b10110001, 0b01100010, 0b11000100, 0b00111000]
    # Columns 0..3 are the identity, so U = I for this choice of columns.
    assert [column(h, j) for j in range(4, 8)] == [0b1001, 0b1011, 0b0110, 0b0101]
    e = (1 << 1) | (1 << 4) | (1 << 7)
    s = syndrome(h, e)
    assert s == 0b1110
    rows, s2 = eliminate(h, s, [0, 1, 2, 3])
    assert rows == h and s2 == s
    # Window: row 0. Left half {4, 5}, right half {6, 7}.
    left = {j: (s2 ^ column(h, j)) & 1 for j in (4, 5)}
    right = {j: column(h, j) & 1 for j in (6, 7)}
    assert left == {4: 1, 5: 1}
    assert right == {6: 0, 7: 1}
    # Two collisions on key 1: (4, 7) and (5, 7).
    t = s2 ^ column(h, 4) ^ column(h, 7)
    assert t == 0b0010 and weight(t) == 1
    t_bad = s2 ^ column(h, 5) ^ column(h, 7)
    assert t_bad == 0
    found = (1 << 1) | (1 << 4) | (1 << 7)
    assert syndrome(h, found) == s


def test_against_brute_force():
    """Every output is a true solution, and a findable solution is found."""
    rng = random.Random(1989)
    found_count = 0
    for _ in range(500):
        n = rng.randint(6, 11)
        k = rng.randint(2, n - 3)
        p = rng.randint(0, 1)
        l = rng.randint(0, 2)
        w = rng.randint(2 * p, min(2 * p + n - k - l, 4))
        h, s, _ = random_instance(n, k, w, rng)
        sols = brute_force(h, s, n, w)
        ok = any(findable(h, x, n, p, l) for x in sols)
        e, _, _ = stern(h, s, n, w, p, l, rng, max_iter=20000 if ok else 300)
        if e is not None:
            assert e in sols
            found_count += 1
        if ok:
            assert e is not None
    assert found_count > 300


def test_rounds_match_the_formula():
    """Mean rounds on random [60, 30] codes with w = 6, p = 1 and l = 4."""
    rng = random.Random(31415)
    n, k, w, p, l, trials = 60, 30, 6, 1, 4, 100
    total = 0
    for _ in range(trials):
        h, s, e = random_instance(n, k, w, rng)
        found, rounds, _ = stern(h, s, n, w, p, l, rng)
        assert found is not None and syndrome(h, found) == s and weight(found) == w
        total += rounds
    expected = 1 / success_probability(n, k, w, p, l)
    assert abs(expected - 14.88) < 0.01
    assert abs(total / trials - expected) < 0.25 * expected


def test_less_work_than_lee_brickell_on_the_same_instances():
    """Stern (p = 1, l = 4) forms fewer column sums than Lee-Brickell (p = 2)."""
    rng = random.Random(2718)
    n, k, w, trials = 60, 30, 6, 60
    stern_work = lb_work = stern_rounds = lb_rounds = 0
    for _ in range(trials):
        h, s, _ = random_instance(n, k, w, rng)
        e1, r1, w1 = stern(h, s, n, w, 1, 4, rng)
        e2, r2, w2 = lee_brickell(h, s, n, w, 2, rng)
        assert syndrome(h, e1) == s and syndrome(h, e2) == s
        stern_work += w1
        lb_work += w2
        stern_rounds += r1
        lb_rounds += r2
    assert stern_work < lb_work
    assert stern_rounds > lb_rounds
