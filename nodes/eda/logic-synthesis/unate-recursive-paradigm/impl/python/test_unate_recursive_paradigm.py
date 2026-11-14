# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unate-recursive-paradigm/. The authors are listed in prov/VCCME7.jsonl.

import itertools
import random

from unate_recursive_paradigm import (
    cofactor,
    complement,
    contains,
    is_unate,
    splitting_variable,
    tautology,
)


def points(cover: list[str], n: int) -> set[int]:
    """The truth table of a cover, as a set of minterms (x_1 is the high bit)."""
    out = set()
    for m in range(2 ** n):
        bits = format(m, "b").zfill(n) if n else ""
        if any(all(ch == "-" or ch == b for ch, b in zip(c, bits)) for c in cover):
            out.add(m)
    return out


def random_cover(rng: random.Random, n: int, k: int, p: float) -> list[str]:
    return ["".join(rng.choice("01") if rng.random() < p else "-" for _ in range(n)) for _ in range(k)]


def test_small_cases() -> None:
    assert tautology(["1-", "0-"], 2)
    assert not tautology(["1-", "-1"], 2)  # unate, no universal cube
    assert tautology(["11", "0-", "-0"], 2)
    assert not tautology([], 3)
    assert tautology(["---"], 3)
    assert complement([], 2) == ["--"]
    assert complement(["--"], 2) == []
    assert sorted(complement(["10-"], 3)) == ["-1-", "0--"]


def test_unate_rule() -> None:
    assert is_unate(["1-0", "-10", "1--"], 3)
    assert not is_unate(["1-", "0-"], 2)
    assert cofactor(["1-0", "0-1", "--1"], 0, "1") == ["--0", "--1"]
    # x3 is binate and in all three cubes; x1 is binate and in two.
    assert splitting_variable(["1-0", "0-1", "--1"], 3) == 2
    assert splitting_variable(["1--", "-1-"], 3) == 0  # unate: the first of the most used


def test_tautology_against_truth_table() -> None:
    rng = random.Random(21)
    for _ in range(1500):
        n = rng.randint(1, 6)
        cover = random_cover(rng, n, rng.randint(0, 12), rng.choice((0.3, 0.5, 0.7)))
        assert tautology(cover, n) == (len(points(cover, n)) == 2 ** n)


def test_complement_against_truth_table() -> None:
    rng = random.Random(22)
    for _ in range(800):
        n = rng.randint(1, 6)
        cover = random_cover(rng, n, rng.randint(0, 10), rng.choice((0.3, 0.5, 0.7)))
        comp = complement(cover, n)
        assert points(comp, n) == set(range(2 ** n)) - points(cover, n)
        assert len(set(comp)) == len(comp)


def test_complement_of_all_two_variable_covers() -> None:
    cubes = ["".join(t) for t in itertools.product("01-", repeat=2)]
    for k in range(4):
        for cover in itertools.combinations(cubes, k):
            comp = complement(list(cover), 2)
            assert points(comp, 2) == set(range(4)) - points(list(cover), 2)


def test_contains_against_truth_table() -> None:
    rng = random.Random(23)
    for _ in range(800):
        n = rng.randint(1, 6)
        cover = random_cover(rng, n, rng.randint(0, 10), 0.5)
        d = random_cover(rng, n, 1, 0.5)[0]
        assert contains(cover, d) == (points([d], n) <= points(cover, n))


def test_exponential_complement() -> None:
    # x1 y1 + x2 y2 + x3 y3 has a complement of 2^3 cubes, and none can be dropped.
    cover = ["11----", "--11--", "----11"]
    comp = complement(cover, 6)
    assert len(comp) == 8
    assert points(comp, 6) == set(range(64)) - points(cover, 6)
