# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zuker-algorithm/. The authors are listed in prov/V18HE3.jsonl.

import random
from typing import Iterator

from zuker_algorithm import INF, Model, can_pair, energy, to_dot_bracket, zuker, zuker_tables


def all_structures(s: str, m: int) -> Iterator[list[tuple[int, int]]]:
    """Every secondary structure of s, by brute force over the partner of the first base."""

    def rec(i: int, j: int) -> Iterator[list[tuple[int, int]]]:
        if j - i < 1:
            yield []
            return
        yield from rec(i + 1, j)
        for k in range(i + m + 1, j + 1):
            if can_pair(s[i], s[k]):
                for inner in rec(i + 1, k - 1):
                    for outer in rec(k + 1, j):
                        yield [(i, k)] + inner + outer

    yield from rec(0, len(s) - 1)


def brute_mfe(s: str, model: Model) -> float:
    return min(energy(s, t, model) for t in all_structures(s, model.m))


def check(s: str, model: Model) -> None:
    best, st = zuker(s, model)
    assert best == brute_mfe(s, model), (s, model)
    assert energy(s, st, model) == best


def test_hairpin_example() -> None:
    model = Model()
    best, st = zuker("GGGAAACCC", model)
    assert to_dot_bracket(9, st) == "(((...)))"
    assert best == -6 - 6 + 6


def test_energy_evaluator() -> None:
    model = Model(a=3, b=1, c=1)
    s = "GGGAAACCAAAGGAAACCCC"
    # one multiloop closed by (0, 19) with branches (2, 7) and (11, 16)
    st = [(0, 19), (1, 18), (2, 7), (11, 16)]
    e = energy(s, st, model)
    stack = -(3 + 3)
    hp = 3 + 4
    multi = 3 + 1 * 3 + 1 * ((19 - 1 - 1 - 1) - 6 - 6)
    hp2 = 3 + 4
    assert e == stack + multi + hp + hp2


def test_against_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(250):
        n = rng.randint(0, 14)
        s = "".join(rng.choice("ACGU") for _ in range(n))
        check(s, Model())


def test_gc_rich_and_parameters() -> None:
    rng = random.Random(9)
    for _ in range(150):
        n = rng.randint(8, 15)
        s = "".join(rng.choice("GCGCAU") for _ in range(n))
        model = Model(
            m=rng.choice((0, 1, 3)),
            hairpin_init=rng.randint(0, 5),
            bulge_init=rng.randint(0, 3),
            interior_init=rng.randint(0, 3),
            a=rng.randint(-2, 4),
            b=rng.randint(-1, 2),
            c=rng.randint(0, 2),
            max_loop=rng.choice((0, 1, 2, 4, 30)),
        )
        check(s, model)


def test_loop_limit_matters() -> None:
    # A long interior loop is forbidden with max_loop = 2, so the outer helix cannot close it.
    s = "GGGAAAAGGGAAACCCAAAACCC"
    free = zuker(s, Model(max_loop=30))[0]
    limited = zuker(s, Model(max_loop=2))[0]
    assert limited >= free
    assert limited == brute_mfe(s, Model(max_loop=2))


def test_tables_infinite_where_no_pair() -> None:
    s = "AAAAAAAA"
    V, WM1, WM, F = zuker_tables(s)
    assert all(v == INF for row in V for v in row)
    assert F[len(s)] == 0
