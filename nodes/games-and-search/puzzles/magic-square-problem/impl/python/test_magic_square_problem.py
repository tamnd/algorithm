# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/magic-square-problem/. The authors are listed in prov/DGVTGW.jsonl.

import random

from magic_square_problem import (complement, count_brute_force, count_order_four, is_magic, lux,
                                  magic_constant, magic_square, normal_form, siamese, symmetries)


def test_constructions_are_magic() -> None:
    for n in range(3, 23):
        sq = magic_square(n)
        assert is_magic(sq), n
        assert all(sum(row) == magic_constant(n) for row in sq)
    assert magic_square(2) is None
    assert magic_square(1) == [[1]]


def test_each_method() -> None:
    assert siamese(3) == [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
    assert complement(4) == [[16, 2, 3, 13], [5, 11, 10, 8], [9, 7, 6, 12], [4, 14, 15, 1]]
    assert all(is_magic(siamese(n)) for n in range(3, 22, 2))
    assert all(is_magic(complement(n)) for n in range(4, 25, 4))
    assert all(is_magic(lux(n)) for n in range(6, 31, 4))
    assert magic_constant(3) == 15 and magic_constant(4) == 34 and magic_constant(5) == 65


def test_is_magic_rejects() -> None:
    sq = siamese(5)
    sq[0][0], sq[0][1] = sq[0][1], sq[0][0]
    assert not is_magic(sq)
    assert not is_magic([[1, 1], [1, 1]])
    # Semi-magic: rows and columns sum to 15, diagonals do not.
    assert not is_magic([[1, 5, 9], [6, 7, 2], [8, 3, 4]])


def test_order_three_by_brute_force() -> None:
    squares = count_brute_force(3)
    assert len(squares) == 8
    assert {tuple(map(tuple, normal_form(s))) for s in squares} == {((2, 7, 6), (9, 5, 1), (4, 3, 8))}
    assert len({tuple(map(tuple, s)) for s in symmetries(siamese(3))}) == 8
    assert count_brute_force(2) == []


def test_symmetries_and_complement_keep_magic() -> None:
    rng = random.Random(71)
    for n in (4, 5, 6, 8):
        sq = magic_square(n)
        for img in symmetries(sq):
            assert is_magic(img)
        comp = [[n * n + 1 - v for v in row] for row in sq]
        assert is_magic(comp)
        r = rng.randrange(n)
        assert sum(sq[r]) == magic_constant(n)


def test_order_four_count() -> None:
    assert count_order_four() == 880
