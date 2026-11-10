# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chekuri-khanna-ptas/. The authors are listed in prov/K6B73V.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from chekuri_khanna_ptas import (
    candidate_sets,
    chekuri_khanna_ptas,
    pack_exact,
    profit_classes,
)


def brute_force(sizes: list[int], profits: list[int], caps: list[int]) -> int:
    m = len(caps)
    best = 0
    for a in itertools.product(range(m + 1), repeat=len(sizes)):
        loads = [0] * m
        for x, b in zip(sizes, a):
            if b < m:
                loads[b] += x
        if all(loads[j] <= caps[j] for j in range(m)):
            best = max(best, sum(profits[i] for i in range(len(sizes)) if a[i] < m))
    return best


def check_packing(sizes: list[int], caps: list[int], bins: list[list[int]]) -> None:
    assert len(bins) == len(caps)
    flat = [i for b in bins for i in b]
    assert len(flat) == len(set(flat))
    for b, cap in zip(bins, caps):
        assert sum(sizes[i] for i in b) <= cap


def value(profits: list[int], bins: list[list[int]]) -> int:
    return sum(profits[i] for b in bins for i in b)


S = [6, 5, 5, 4, 3]
P = [9, 7, 7, 6, 3]
C = [10, 6]


def test_example() -> None:
    assert brute_force(S, P, C) == 23
    bins = chekuri_khanna_ptas(S, P, C, 1)
    check_packing(S, C, bins)
    assert bins == [[0, 3], [1]]
    assert value(P, bins) == 22
    bins = chekuri_khanna_ptas(S, P, C, Fraction(1, 2))
    check_packing(S, C, bins)
    assert value(P, bins) == 23


def test_classes_and_candidates() -> None:
    d = Fraction(1, 3)
    big_o = 9 * (1 + d) ** 3
    assert big_o == Fraction(64, 3)
    classes, a = profit_classes(S, P, [0, 1, 2, 3, 4], big_o, d)
    assert classes == [[4], [3, 1, 2], [0]]
    assert a == [Fraction(1024, 405), Fraction(65536, 10935), Fraction(262144, 32805)]
    sets = [u for o, _, _, u in candidate_sets(S, P, C, d) if o == big_o]
    assert len(sets) == 16
    assert [0, 1, 2] not in sets
    assert [0, 1, 3] in sets


def test_edges() -> None:
    assert chekuri_khanna_ptas([], [], [5], Fraction(1, 2)) == [[]]
    assert chekuri_khanna_ptas([7, 8], [3, 4], [5, 6], Fraction(1, 2)) == [[], []]
    assert chekuri_khanna_ptas([4], [5], [3, 4], Fraction(1, 2)) == [[], [0]]
    with pytest.raises(ValueError):
        chekuri_khanna_ptas([1], [1], [1], 0)
    with pytest.raises(ValueError):
        chekuri_khanna_ptas([1], [1], [1], Fraction(3, 2))


def test_pack_exact() -> None:
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randint(0, 6)
        m = rng.randint(1, 3)
        sizes = [rng.randint(1, 9) for _ in range(n)]
        caps = [rng.randint(1, 12) for _ in range(m)]
        items = list(range(n))
        bins = pack_exact(sizes, caps, items)
        fits = brute_force(sizes, [1] * n, caps) == n
        assert (bins is not None) == fits
        if bins is not None:
            check_packing(sizes, caps, bins)
            assert sorted(i for b in bins for i in b) == items


def random_instance(rng: random.Random) -> tuple[list[int], list[int], list[int]]:
    n = rng.randint(1, 6)
    m = rng.randint(1, 3)
    sizes = [rng.randint(1, 10) for _ in range(n)]
    profits = [rng.randint(1, 30) for _ in range(n)]
    caps = [rng.randint(3, 15) for _ in range(m)]
    return sizes, profits, caps


@pytest.mark.parametrize("eps", [Fraction(1), Fraction(1, 2), Fraction(1, 3)])
def test_ratio(eps: Fraction) -> None:
    rng = random.Random(2000)
    d = eps / 3
    for _ in range(60):
        sizes, profits, caps = random_instance(rng)
        opt = brute_force(sizes, profits, caps)
        bins = chekuri_khanna_ptas(sizes, profits, caps, eps)
        check_packing(sizes, caps, bins)
        alg = value(profits, bins)
        assert alg <= opt
        assert alg >= (1 - 2 * d - d * d) * opt
        assert alg >= (1 - eps) * opt


def test_candidate_bounds() -> None:
    rng = random.Random(2005)
    for d in [Fraction(1, 3), Fraction(1, 6)]:
        for _ in range(40):
            sizes, profits, caps = random_instance(rng)
            n = sum(1 for x in sizes if x <= max(caps))
            if n == 0:
                assert list(candidate_sets(sizes, profits, caps, d)) == []
                continue
            opt = brute_force(sizes, profits, caps)
            count: dict[Fraction, int] = {}
            shape: dict[Fraction, tuple[int, int]] = {}
            for o, h, big_d, _ in candidate_sets(sizes, profits, caps, d):
                count[o] = count.get(o, 0) + 1
                shape[o] = (h, big_d)
            big_j = math.ceil(math.log(n) / math.log(1 + d) - 1e-12) if n > 1 else 0
            assert len(count) <= big_j + 1
            for o, (h, big_d) in shape.items():
                assert big_d == int((1 + d) * h / (d * d))
                assert count[o] <= math.comb(big_d + h, h)
            # the grid holds a guess O with O <= OPT < (1 + d) O
            good = [o for o in count if o <= opt < (1 + d) * o]
            assert len(good) == 1
            # the guessing lemma: one candidate for that O fits and is good
            best = 0
            for o, _, _, u in candidate_sets(sizes, profits, caps, d):
                if o == good[0] and pack_exact(sizes, caps, u) is not None:
                    best = max(best, sum(profits[i] for i in u))
            assert best >= (1 - 2 * d - d * d) * opt
