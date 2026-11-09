# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-sat/. The authors are listed in prov/WQ19T1.jsonl.

import itertools
import random

from incremental_sat import IncrementalSolver


def satisfiable(clauses: list[list[int]], n: int) -> bool:
    return any(all(any(b[abs(a) - 1] == (a > 0) for a in c) for c in clauses)
               for b in itertools.product([False, True], repeat=n))


def random_clause(rng: random.Random, n: int) -> list[int]:
    vs = rng.sample(range(1, n + 1), rng.randint(1, min(3, n)))
    return [v if rng.random() < 0.5 else -v for v in vs]


def test_page_example() -> None:
    s = IncrementalSolver()
    for c in [[-3, 1], [-4, -1], [-5, 2], [-1, -2, 6]]:
        s.add_clause(c)
    assert s.solve([3, 4, 5]) is False
    assert sorted(s.core) == [3, 4]
    assert s.solve([3, 5]) is True
    assert s.model[1] and s.model[2] and s.model[6]
    s.add_clause([-6])  # a new clause between calls
    assert s.solve([3, 5]) is False
    assert sorted(s.core) == [3, 5]
    assert s.solve([3]) is True
    assert s.solve([]) is True


def test_random_queries_against_brute_force() -> None:
    rng = random.Random(2003)
    for _ in range(60):
        n = rng.randint(3, 10)
        s = IncrementalSolver()
        f: list[list[int]] = []
        for _ in range(12):
            for _ in range(rng.randint(0, n)):
                c = random_clause(rng, n)
                f.append(c)
                s.add_clause(c)
            assume = [v if rng.random() < 0.5 else -v
                      for v in rng.sample(range(1, n + 1), rng.randint(0, n))]
            ok = s.solve(assume)
            assert ok == satisfiable(f + [[a] for a in assume], n)
            if ok:
                assert all(any(s.model.get(abs(a)) == (a > 0) for a in c) for c in f)
                assert all(s.model[abs(a)] == (a > 0) for a in assume)
            else:
                assert set(s.core) <= set(assume)
                assert not satisfiable(f + [[a] for a in s.core], n)


def test_activation_literals_retract_clauses() -> None:
    rng = random.Random(7)
    for _ in range(40):
        n = rng.randint(3, 8)
        groups = [[random_clause(rng, n) for _ in range(rng.randint(1, 2 * n))] for _ in range(3)]
        s = IncrementalSolver()
        sel = [n + 1 + g for g in range(3)]
        for g, cs in enumerate(groups):
            for c in cs:
                s.add_clause(c + [-sel[g]])
        for on in itertools.product([False, True], repeat=3):
            active = [c for g in range(3) if on[g] for c in groups[g]]
            assume = [sel[g] if on[g] else -sel[g] for g in range(3)]
            assert s.solve(assume) == satisfiable(active, n)
            if s.core:
                assert set(s.core) <= {sel[g] for g in range(3) if on[g]}


def test_learned_clauses_are_reused() -> None:
    # Pigeonhole formula with 5 pigeons and 4 holes behind one selector.
    p = lambda i, j: 4 * i + j + 1
    s = IncrementalSolver()
    sel = 21
    for i in range(5):
        s.add_clause([p(i, j) for j in range(4)] + [-sel])
    for j in range(4):
        for a in range(5):
            for b in range(a + 1, 5):
                s.add_clause([-p(a, j), -p(b, j), -sel])
    assert s.solve([sel]) is False and s.core == [sel]
    first = s.conflicts
    assert s.solve([sel]) is False
    second = s.conflicts - first
    assert 0 < first and second < first
    assert s.solve([]) is True
