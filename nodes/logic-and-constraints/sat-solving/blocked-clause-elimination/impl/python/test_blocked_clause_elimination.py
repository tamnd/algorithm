# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blocked-clause-elimination/. The authors are listed in prov/GQDPDA.jsonl.

import itertools
import random

from blocked_clause_elimination import bce, is_blocked, reconstruct


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


def test_page_example() -> None:
    f = [[-1, -3], [1, -2], [2, 3], [-2, 4], [2, -4]]
    rest, stack = bce(f)
    assert rest == [[-1, -3], [1, -2], [2, 3]]
    assert stack == [([-2, 4], 4), ([2, -4], -4)]
    alpha = reconstruct({1: False, 2: False, 3: True, 4: True}, stack)
    assert alpha == {1: False, 2: False, 3: True, 4: False} and sat(f, alpha)


def test_equisatisfiable_and_reconstruction() -> None:
    rng = random.Random(2010)
    for _ in range(500):
        n = rng.randint(1, 9)
        f = random_cnf(rng, n, rng.randint(1, 3 * n))
        rest, stack = bce(f)
        any_model = False
        for a in assignments(n):
            if sat(rest, a):
                any_model = True
                assert sat(f, reconstruct(a, stack))
        assert any_model == any(sat(f, a) for a in assignments(n))


def test_fixpoint_and_confluence() -> None:
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(2, 7)
        f = [list(c) for c in {tuple(sorted(c)) for c in random_cnf(rng, n, rng.randint(2, 12))}]
        rest, _ = bce(f)
        sets = [set(c) for c in rest]
        for i, c in enumerate(sets):
            others = sets[:i] + sets[i + 1:]
            assert not any(is_blocked(c, lit, others) for lit in c)
        g = f[:]
        rng.shuffle(g)
        rest2, _ = bce([c[::-1] for c in g])
        assert sorted(rest) == sorted(rest2)


def test_pure_literal_and_tautology() -> None:
    rest, stack = bce([[1, 2], [1, -2], [-1, 1, 3]])
    assert rest == [] and len(stack) == 3
