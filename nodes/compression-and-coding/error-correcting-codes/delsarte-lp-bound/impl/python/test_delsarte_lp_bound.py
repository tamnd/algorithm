# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delsarte-lp-bound/. The authors are listed in prov/P5EAGN.jsonl.

import random
from fractions import Fraction
from itertools import product
from math import comb, floor

import pytest

from delsarte_lp_bound import (
    check_dual_certificate, delsarte_inequalities, delsarte_lp, distance_distribution,
    krawtchouk, simplex_max,
)

# A_2(n, d) for even d, copied by hand from A. E. Brouwer, Table of general binary codes,
# https://aeb.win.tue.nl/codes/binary-1.html (rows n = 4 to 13, columns d = 4 to 12).
# Odd d follows from A_2(n, d) = A_2(n + 1, d + 1); d = 2 gives 2^(n - 1).
BROUWER_EVEN = {
    (4, 4): 2, (5, 4): 2, (6, 4): 4, (7, 4): 8, (8, 4): 16, (9, 4): 20, (10, 4): 40,
    (11, 4): 72, (12, 4): 144, (13, 4): 256,
    (6, 6): 2, (7, 6): 2, (8, 6): 2, (9, 6): 4, (10, 6): 6, (11, 6): 12, (12, 6): 24, (13, 6): 32,
    (8, 8): 2, (9, 8): 2, (10, 8): 2, (11, 8): 2, (12, 8): 4, (13, 8): 4,
    (10, 10): 2, (11, 10): 2, (12, 10): 2, (13, 10): 2,
    (12, 12): 2, (13, 12): 2,
}


def a2(n: int, d: int) -> int:
    if d == 1:
        return 2 ** n
    if d == 2:
        return 2 ** (n - 1)
    if d > n:
        return 1
    if d % 2:
        return BROUWER_EVEN[(n + 1, d + 1)]
    return BROUWER_EVEN[(n, d)]


# floor of the LP bound for binary codes and even d (n = 9 to 12)
LP_FLOOR = {(9, 4): 25, (10, 4): 42, (11, 4): 85, (12, 4): 170, (8, 6): 3, (10, 6): 6,
            (11, 6): 12, (12, 6): 24, (11, 8): 3, (12, 8): 4}


def test_krawtchouk_generating_function_and_orthogonality() -> None:
    for q in (2, 3):
        n = 6
        for x in range(n + 1):
            # sum_k K_k(x) z^k = (1 + (q - 1) z)^(n - x) (1 - z)^x, compared at z = 2
            lhs = sum(krawtchouk(n, k, x, q) * 2 ** k for k in range(n + 1))
            assert lhs == (1 + (q - 1) * 2) ** (n - x) * (1 - 2) ** x
        for k in range(n + 1):
            for m in range(n + 1):
                s = sum(comb(n, i) * (q - 1) ** i * krawtchouk(n, k, i, q) * krawtchouk(n, m, i, q)
                        for i in range(n + 1))
                assert s == (q ** n * comb(n, k) * (q - 1) ** k if k == m else 0)


def test_delsarte_inequalities_hold_for_codes() -> None:
    rng = random.Random(1973)
    for q, n in ((2, 8), (2, 10), (3, 5)):
        allw = list(product(range(q), repeat=n))
        for _ in range(30):
            code = rng.sample(allw, rng.randint(2, 40))
            b = delsarte_inequalities(distance_distribution(code, n), n, q)
            assert b[0] == len(code)
            assert all(bk >= 0 for bk in b)


def test_inequalities_give_dual_weights_for_linear_codes() -> None:
    # [7, 4] Hamming code: B_k = |C| * (number of dual words of weight k);
    # the dual is the [7, 3] simplex code with 7 words of weight 4.
    cols = [tuple((j >> i) & 1 for i in range(3)) for j in range(1, 8)]
    code = [w for w in product((0, 1), repeat=7)
            if all(sum(w[j] * cols[j][i] for j in range(7)) % 2 == 0 for i in range(3))]
    assert len(code) == 16
    b = delsarte_inequalities(distance_distribution(code, 7), 7)
    assert b == [16, 0, 0, 0, 112, 0, 0, 0]


def test_simplex_method_small_lps() -> None:
    f = Fraction
    # max 3x + 2y, x + y <= 4, x + 3y <= 6, x <= 3: optimum 11 at (3, 1)
    opt, x, y = simplex_max([f(3), f(2)], [[f(1), f(1)], [f(1), f(3)], [f(1), f(0)]], [f(4), f(6), f(3)])
    assert opt == 11 and x == [3, 1]
    assert sum(bi * yi for bi, yi in zip([4, 6, 3], y)) == 11  # strong duality
    with pytest.raises(ValueError):
        simplex_max([f(1), f(1)], [[f(1), f(-1)]], [f(1)])


def test_lp_bound_against_table() -> None:
    for n in range(4, 13):
        for d in range(2, n + 1):
            bound, dist, f = delsarte_lp(n, d)
            assert a2(n, d) <= floor(bound)
            assert check_dual_certificate(n, d, f) == bound  # the dual polynomial proves it
            assert all(v >= 0 for v in dist.values())
            if d % 2 == 0:
                be, _, fe = delsarte_lp(n, d, even=True)
                assert a2(n, d) <= floor(be) <= floor(bound)
                assert check_dual_certificate(n, d, fe, even=True) == be
    for (n, d), v in LP_FLOOR.items():
        assert floor(delsarte_lp(n, d)[0]) == v


def hamming_bound(n: int, d: int) -> int:
    return 2 ** n // sum(comb(n, i) for i in range((d - 1) // 2 + 1))


def test_lp_never_above_hamming() -> None:
    for n in range(2, 17):
        for d in range(1, n + 1):
            assert floor(delsarte_lp(n, d)[0]) <= hamming_bound(n, d)
    table = {(8, 6): 6, (12, 4): 315, (17, 4): 7281, (20, 6): 4969, (24, 8): 7216}
    for (n, d), h in table.items():
        assert hamming_bound(n, d) == h
    assert delsarte_lp(17, 4)[0] == Fraction(32768, 9)
    assert delsarte_lp(20, 6)[0] == Fraction(149504, 63)


def test_lp_meets_golay_and_hamming() -> None:
    assert delsarte_lp(23, 7)[0] == 4096
    bound, dist, _ = delsarte_lp(24, 8, even=True)
    assert bound == 4096
    assert {i: v for i, v in dist.items() if v} == {8: 759, 12: 2576, 16: 759, 24: 1}
    assert delsarte_lp(7, 3)[0] == 16
    assert delsarte_lp(15, 3)[0] == 2048
