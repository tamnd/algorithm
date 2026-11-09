# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounded-variable-elimination/. The authors are listed in prov/CFQP37.jsonl.

import itertools
import random

from bounded_variable_elimination import bve, reconstruct, resolve


def sat(clauses: list[list[int]], a: dict[int, bool]) -> bool:
    return all(any(a[abs(x)] == (x > 0) for x in c) for c in clauses)


def assignments(n: int):
    for bits in itertools.product([False, True], repeat=n):
        yield {i + 1: bits[i] for i in range(n)}


def random_cnf(rng: random.Random, n: int, m: int) -> list[list[int]]:
    cnf = []
    for _ in range(m):
        k = rng.randint(1, min(3, n))
        vs = rng.sample(range(1, n + 1), k)
        cnf.append([v if rng.random() < 0.5 else -v for v in vs])
    return cnf


def test_resolve() -> None:
    assert resolve(frozenset({1, 2}), frozenset({-1, 3}), 1) == frozenset({2, 3})
    assert resolve(frozenset({1, 2}), frozenset({-1, -2}), 1) is None


def test_page_example() -> None:
    # x5 = x, x1 = a, x2 = b, x3 = c, x4 = d
    f = [[5, 1], [5, 2], [-5, 3], [-5, -1, 4]]
    rest, stack = bve(f, frozen=frozenset({1, 2, 3, 4}))
    assert rest == [[-1, 2, 4], [1, 3], [2, 3]]
    assert sorted(stack) == [([-1, 4, -5], -5), ([1, 5], 5), ([2, 5], 5), ([3, -5], -5)]
    alpha = reconstruct({1: False, 2: True, 3: True, 4: False, 5: False}, stack)
    assert alpha[5] is True and sat(f, alpha)
    # without frozen variables the whole formula goes away
    rest, stack = bve(f)
    assert rest == [] and sat(f, reconstruct({v: False for v in range(1, 6)}, stack))


def test_equisatisfiable_and_reconstruction() -> None:
    rng = random.Random(2005)
    for _ in range(400):
        n = rng.randint(1, 9)
        f = random_cnf(rng, n, rng.randint(1, 4 * n))
        slack = rng.choice([0, 0, 2])
        rest, stack = bve(f, slack=slack)
        f_sat = any(sat(f, a) for a in assignments(n))
        if rest == [[]]:
            assert not f_sat
            continue
        if slack == 0:
            assert len(rest) <= len({frozenset(c) for c in f})
        any_model = False
        for a in assignments(n):
            if sat(rest, a):
                any_model = True
                assert sat(f, reconstruct(a, stack))
        assert any_model == f_sat


def test_frozen_variables_stay() -> None:
    rng = random.Random(9)
    for _ in range(100):
        n = rng.randint(2, 7)
        f = random_cnf(rng, n, rng.randint(1, 3 * n))
        frozen = frozenset(rng.sample(range(1, n + 1), 1))
        rest, stack = bve(f, frozen=frozen)
        assert all(abs(lit) not in frozen for _, lit in stack)
        if rest != [[]]:
            # over the frozen variables the projections agree
            v = next(iter(frozen))
            for val in (False, True):
                g = [c for c in rest if (v if val else -v) not in c]
                g = [[a for a in c if a != (-v if val else v)] for c in g]
                h = [c for c in f if (v if val else -v) not in c]
                h = [[a for a in c if a != (-v if val else v)] for c in h]
                assert any(sat(g, a) for a in assignments(n)) == any(sat(h, a) for a in assignments(n))
