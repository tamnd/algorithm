# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plotkin-bound/. The authors are listed in prov/PY83ZY.jsonl.

import random
from itertools import product
from math import log2

from plotkin_bound import (
    hadamard_codes, is_hadamard, min_distance, paley, plotkin_binary, plotkin_binary_refined,
    plotkin_q, plotkin_rate, plotkin_shortened, sylvester,
)

# A_2(n, d) for even d, copied from A. E. Brouwer, Table of general binary codes,
# https://aeb.win.tue.nl/codes/binary-1.html (all the entries with n <= 2d and d = 4 to 12).
BROUWER_EVEN = {
    (6, 4): 4, (7, 4): 8, (8, 4): 16,
    (9, 6): 4, (10, 6): 6, (11, 6): 12, (12, 6): 24,
    (9, 8): 2, (10, 8): 2, (11, 8): 2, (12, 8): 4, (13, 8): 4, (14, 8): 8, (15, 8): 16, (16, 8): 32,
    (11, 10): 2, (12, 10): 2, (13, 10): 2, (14, 10): 2, (15, 10): 4, (16, 10): 4, (17, 10): 6,
    (18, 10): 10, (19, 10): 20, (20, 10): 40,
    (13, 12): 2, (14, 12): 2, (15, 12): 2, (16, 12): 2, (17, 12): 2, (18, 12): 4, (19, 12): 4,
    (20, 12): 6, (21, 12): 8, (22, 12): 12, (23, 12): 24, (24, 12): 48,
}


def test_levenshtein_tightness_on_table() -> None:
    # For even d and n < 2d the refined bound equals A_2(n, d); also A_2(2d, d) = 4d.
    for (n, d), a in BROUWER_EVEN.items():
        assert plotkin_binary_refined(n, d) == a
        if 2 * d > n:
            assert plotkin_binary(n, d) >= a
        # odd distance: A_2(n - 1, d - 1) = A_2(n, d)
        assert plotkin_binary_refined(n - 1, d - 1) == a


def test_q_ary_formula_matches_binary() -> None:
    for n in range(1, 30):
        for d in range(1, n + 1):
            b = plotkin_binary(n, d)
            qv = plotkin_q(2, n, d)
            assert (b is None) == (qv is None)
            if b is not None:
                assert b <= qv <= b + 1  # the binary form gains from the parity of M


def test_bound_on_random_greedy_codes() -> None:
    rng = random.Random(1960)
    for _ in range(200):
        q = rng.choice([2, 3])
        n = rng.randint(2, 6)
        d = rng.randint(1, n)
        allw = list(product(range(q), repeat=n))
        rng.shuffle(allw)
        code: list[tuple[int, ...]] = []
        for x in allw:
            if all(sum(a != b for a, b in zip(x, c)) >= d for c in code):
                code.append(x)
        v = plotkin_q(q, n, d)
        if v is not None:
            assert len(code) <= v
        assert len(code) <= plotkin_shortened(q, n, d)


def test_hadamard_matrices() -> None:
    for r in range(5):
        assert is_hadamard(sylvester(r))
    for p in (3, 7, 11, 19):
        assert is_hadamard(paley(p))


def test_hadamard_codes_meet_plotkin() -> None:
    for h in (sylvester(3), sylvester(4), paley(11), paley(19)):
        n = len(h)
        codes = hadamard_codes(h)
        a, b, c = codes["A"], codes["B"], codes["C"]
        assert len(set(a)) == n and min_distance(a) == n // 2
        assert len(set(b)) == 2 * n and min_distance(b) == n // 2 - 1
        assert len(set(c)) == 2 * n and min_distance(c) == n // 2
        # A: length n - 1, distance n/2, 2d > n - 1
        assert plotkin_binary(n - 1, n // 2) == n
        # C: length n = 2d, bound 4d = 2n
        assert plotkin_binary_refined(n, n // 2) == 2 * n


def test_asymptotic_values() -> None:
    assert abs(plotkin_rate(0.25) - 0.5) < 1e-12
    assert plotkin_rate(0.5) == 0.0
    assert abs(plotkin_rate(0.5, 3) - 0.25) < 1e-12
    for delta in (0.1, 0.2, 0.3, 0.4):
        n = 3000
        d = int(delta * n)
        r = log2(plotkin_shortened(2, n, d)) / n
        assert abs(r - plotkin_rate(d / n)) < 0.01


def test_not_applicable() -> None:
    assert plotkin_binary(10, 5) is None
    assert plotkin_q(3, 9, 6) is None
    assert plotkin_q(3, 8, 6) == 9  # 6 / (6 - 16/3) = 9
    assert plotkin_binary(5, 3) == 6  # 2 floor(3 / 1); the true A_2(5, 3) is 4
    assert plotkin_binary_refined(5, 3) == 4  # 2 floor(4 / 2), the odd-d form is exact here

