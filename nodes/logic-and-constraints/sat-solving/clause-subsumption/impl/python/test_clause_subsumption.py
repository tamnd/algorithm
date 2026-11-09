# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clause-subsumption/. The authors are listed in prov/YEK621.jsonl.

import itertools
import random

from clause_subsumption import subsume


def models(clauses: list[list[int]], n: int) -> set[tuple[bool, ...]]:
    out = set()
    for bits in itertools.product([False, True], repeat=n):
        if all(any(bits[abs(a) - 1] == (a > 0) for a in c) for c in clauses):
            out.add(bits)
    return out


def random_cnf(rng: random.Random, n: int, m: int) -> list[list[int]]:
    cnf = []
    for _ in range(m):
        k = rng.randint(1, min(4, n))
        vs = rng.sample(range(1, n + 1), k)
        cnf.append([v if rng.random() < 0.5 else -v for v in vs])
    return cnf


def is_fixpoint(cnf: list[list[int]]) -> bool:
    sets = [set(c) for c in cnf]
    for i, c in enumerate(sets):
        for j, d in enumerate(sets):
            if i == j:
                continue
            if c <= d:
                return False
            diff = c - d
            if len(diff) == 1 and -next(iter(diff)) in d:
                return False
    return True


def test_page_example() -> None:
    f = [[1, 2, 3], [1, 2], [-1, 2, 4], [1, -2], [-3, 4, 2], [3, -4]]
    g = subsume(f)
    assert sorted(g) == sorted([[1], [2, 4], [3, -4]])
    assert models(f, 4) == models(g, 4)


def test_equivalent_and_fixpoint() -> None:
    rng = random.Random(2005)
    for _ in range(600):
        n = rng.randint(1, 8)
        f = random_cnf(rng, n, rng.randint(1, 14))
        g = subsume(f)
        assert models(f, n) == models(g, n)
        if g != [[]]:
            assert is_fixpoint(g)
            assert sum(map(len, g)) <= sum(len(set(c)) for c in f)
        else:
            assert not models(f, n)


def test_duplicates_tautologies_and_empty() -> None:
    assert subsume([[1, 2], [2, 1], [1, -1, 3]]) == [[1, 2]]
    assert subsume([[1], [-1]]) == [[]]
    assert subsume([[]]) == [[]]
    assert subsume([]) == []
