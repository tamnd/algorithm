# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-ary-gray-code/. The authors are listed in prov/71AG12.jsonl.

import itertools
import random

import pytest

from k_ary_gray_code import k_ary_gray, rank, reflected_mixed_radix, unrank


def reflect(radices: list[int]) -> list[tuple[int, ...]]:
    """Reference: the reflected code by its recursive definition, low digit first."""
    lst: list[tuple[int, ...]] = [()]
    for m in radices:
        new: list[tuple[int, ...]] = []
        for d in range(m):
            block = lst if d % 2 == 0 else lst[::-1]
            new += [w + (d,) for w in block]
        lst = new
    return lst


def run(radices: list[int]) -> list[tuple[int, ...]]:
    return [tuple(a) for a in reflected_mixed_radix(radices)]


def test_example() -> None:
    got = ["".join(str(d) for d in reversed(w)) for w in k_ary_gray(2, 3)]
    assert got == ["00", "01", "02", "12", "11", "10", "20", "21", "22"]


def test_edges() -> None:
    assert run([]) == [()]
    assert k_ary_gray(0, 5) == [()]
    assert run([2]) == [(0,), (1,)]
    assert k_ary_gray(1, 4) == [(0,), (1,), (2,), (3,)]
    with pytest.raises(ValueError):
        run([3, 1])
    with pytest.raises(ValueError):
        unrank(6, [2, 3])


def test_matches_reference_and_unit_steps() -> None:
    for n in range(0, 4):
        for radices in itertools.product(range(2, 6), repeat=n):
            got = run(list(radices))
            assert got == reflect(list(radices))
            total = 1
            for x in radices:
                total *= x
            assert len(set(got)) == total
            for u, v in zip(got, got[1:]):
                diff = [i for i in range(n) if u[i] != v[i]]
                assert len(diff) == 1 and abs(u[diff[0]] - v[diff[0]]) == 1


def test_binary_case_is_brgc() -> None:
    for n in range(0, 11):
        codes = [sum(d << j for j, d in enumerate(w)) for w in k_ary_gray(n, 2)]
        assert codes == [i ^ (i >> 1) for i in range(1 << n)]


def test_rank_unrank_random() -> None:
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randrange(1, 6)
        radices = [rng.randrange(2, 7) for _ in range(n)]
        lst = run(radices)
        for r, w in enumerate(lst):
            assert tuple(unrank(r, radices)) == w
            assert rank(list(w), radices) == r
