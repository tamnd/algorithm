# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chien-search/. The authors are listed in prov/GDVWFM.jsonl.

import random

from chien_search import chien_search, chien_search_direct, locate_errors
from gf import GF2m

F16 = GF2m(4, 0b10011)  # x^4 + x + 1
F256 = GF2m(8, 0x11D)  # x^8 + x^4 + x^3 + x^2 + 1


def locator(field: GF2m, positions: list[int]) -> list[int]:
    lam = [1]
    for i in positions:
        lam = field.pmul(lam, [1, field.alpha(i)])  # 1 - X x = 1 + X x in characteristic 2
    return lam


def test_worked_example() -> None:
    a = F16.alpha
    lam = [1, a(12), a(9)]  # (1 - a^2 x)(1 - a^7 x)
    assert chien_search(F16, lam, 15) == [2, 7]
    assert locate_errors(F16, lam, 15) == [2, 7]


def test_edges() -> None:
    assert chien_search(F16, [1], 15) == []
    assert locate_errors(F16, [1], 15) == []
    assert chien_search(F16, [5], 15) == []
    assert locate_errors(F16, [0, 1], 15) is None  # Lambda_0 = 0 is not a locator
    # root at alpha^0, position 0, and at the last position n - 1
    assert chien_search(F16, locator(F16, [0, 14]), 15) == [0, 14]
    # all 15 positions
    assert chien_search(F16, locator(F16, list(range(15))), 15) == list(range(15))


def test_too_few_roots_is_a_failure() -> None:
    # Every Lambda = 1 + c1 x + c2 x^2 with c2 != 0: two distinct roots, a double root
    # (c1 = 0), or no root in GF(16) (irreducible). Only the first case locates errors.
    kinds = {0: 0, 1: 0, 2: 0}
    for c1 in range(16):
        for c2 in range(1, 16):
            lam = [1, c1, c2]
            roots = chien_search(F16, lam, 15)
            kinds[len(roots)] += 1
            assert locate_errors(F16, lam, 15) == (roots if len(roots) == 2 else None)
    # 105 products of two distinct (1 - X x), 15 squares, 120 irreducible quadratics
    assert kinds == {2: 105, 1: 15, 0: 120}


def test_shortened_code_range() -> None:
    # a shortened code of length 10: only positions 0 .. 9 are real
    lam = locator(F16, [3, 12])
    assert chien_search(F16, lam, 15) == [3, 12]
    assert chien_search(F16, lam, 10) == [3]
    assert locate_errors(F16, lam, 10) is None  # one root outside the code: a decoder failure


def test_random_against_direct_evaluation() -> None:
    rng = random.Random(1964)
    for field in (F16, F256):
        n = field.n
        for _ in range(400):
            nu = rng.randrange(0, 9)
            lam = [rng.randrange(1, field.q)] + [rng.randrange(field.q) for _ in range(nu)]
            assert chien_search(field, lam, n) == chien_search_direct(field, lam, n)


def test_random_locators() -> None:
    rng = random.Random(4)
    for _ in range(300):
        pos = sorted(rng.sample(range(255), rng.randrange(0, 17)))
        assert locate_errors(F256, locator(F256, pos), 255) == pos
