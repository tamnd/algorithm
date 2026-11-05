# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hao-orlin/. The authors are listed in prov/X5P88R.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from hao_orlin import hao_orlin

S, A, B, C, D, T = range(6)
RUNNING = [(S, A, 10), (S, C, 10), (A, B, 4), (A, C, 2), (A, D, 8), (C, D, 9), (D, B, 6), (B, T, 10), (D, T, 10)]


def cut(edges, side):
    return sum(c for u, v, c in edges if u in side and v not in side)


def brute(n, edges):
    best = None
    for k in range(1, n):
        for side in combinations(range(n), k):
            c = cut(edges, set(side))
            best = c if best is None else min(best, c)
    return best


def check(n, edges):
    value, side = hao_orlin(n, edges)
    assert 0 < len(side) < n
    assert cut(edges, set(side)) == value
    assert value == brute(n, edges)
    return value, side


def test_running_network_has_a_zero_cut() -> None:
    # nothing enters s, so the cut V - {s} has capacity 0
    assert check(6, RUNNING) == (0, [A, B, C, D, T])


def test_running_network_with_return_arc() -> None:
    edges = RUNNING + [(T, S, 15)]
    log = []
    value, side = hao_orlin(6, edges, lambda *a: log.append(a))
    assert (value, side) == (9, [C])
    assert len(log) == 10
    assert min(v for r, _, v, _ in log if r == "forward") == 10
    check(6, edges)


def test_no_path_and_zero_capacity() -> None:
    assert check(3, [(0, 1, 5), (2, 1, 5)])[0] == 0
    assert check(2, [(0, 1, 0), (1, 0, 3)])[0] == 0
    assert check(2, [])[0] == 0


def test_antiparallel_edges() -> None:
    edges = [(0, 1, 3), (1, 0, 2), (1, 2, 4), (2, 1, 1), (2, 0, 5), (0, 2, 1)]
    # the six cuts: {0} 4, {1} 6, {2} 6, {0, 1} 5, {0, 2} 4, {1, 2} 7
    assert check(3, edges) == (4, [0])


def test_undirected_cycle() -> None:
    n = 6
    edges = []
    for i in range(n):
        edges += [(i, (i + 1) % n, 1), ((i + 1) % n, i, 1)]
    assert check(n, edges)[0] == 2


def test_fractions_and_floats() -> None:
    edges = [(0, 1, Fraction(1, 2)), (1, 2, Fraction(1, 3)), (2, 0, Fraction(1, 6)), (1, 0, Fraction(1, 7))]
    check(3, edges)
    value, _ = hao_orlin(2, [(0, 1, 0.5), (1, 0, 0.25)])
    assert value == 0.25


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        hao_orlin(1, [])
    with pytest.raises(ValueError):
        hao_orlin(2, [(0, 1, -1)])
    with pytest.raises(ValueError):
        hao_orlin(2, [(0, 2, 1)])


def test_random_against_brute_force() -> None:
    rng = random.Random(1994)
    for _ in range(700):
        n = rng.randint(2, 7)
        edges = [(rng.randrange(n), rng.randrange(n), rng.choice([0, 1, 2, 3, 5, 8])) for _ in range(rng.randint(0, 18))]
        check(n, edges)


def test_random_dense_strongly_connected() -> None:
    rng = random.Random(7)
    for _ in range(150):
        n = rng.randint(3, 8)
        edges = [(i, (i + 1) % n, rng.randint(1, 4)) for i in range(n)]
        edges += [(rng.randrange(n), rng.randrange(n), rng.randint(0, 9)) for _ in range(3 * n)]
        check(n, edges)
