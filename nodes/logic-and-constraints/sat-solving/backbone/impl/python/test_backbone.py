# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backbone/. The authors are listed in prov/3CT6YF.jsonl.

import itertools
import random

from backbone import backbone


def brute_backbone(clauses: list[list[int]], n: int) -> set[int] | None:
    ms = [b for b in itertools.product([False, True], repeat=n)
          if all(any(b[abs(a) - 1] == (a > 0) for a in c) for c in clauses)]
    if not ms:
        return None
    out = set()
    for v in range(1, n + 1):
        if all(m[v - 1] for m in ms):
            out.add(v)
        elif not any(m[v - 1] for m in ms):
            out.add(-v)
    return out


def random_cnf(rng: random.Random, n: int, m: int) -> list[list[int]]:
    cnf = []
    for _ in range(m):
        k = rng.randint(1, min(3, n))
        vs = rng.sample(range(1, n + 1), k)
        cnf.append([v if rng.random() < 0.5 else -v for v in vs])
    return cnf


def test_page_example() -> None:
    f = [[1, 2], [-1, 2], [-2, 3, 4], [-3, -4], [3, 5]]
    bb, calls = backbone(f, 5)
    assert bb == {2} == brute_backbone(f, 5)
    assert calls <= 6


def test_against_brute_force() -> None:
    rng = random.Random(2015)
    for _ in range(400):
        n = rng.randint(1, 12)
        f = random_cnf(rng, n, rng.randint(1, 4 * n))
        bb, calls = backbone(f, n)
        assert bb == brute_backbone(f, n)
        assert calls <= n + 1


def test_unsat_and_empty() -> None:
    assert backbone([[1], [-1]], 1) == (None, 1)
    assert backbone([], 3) == (set(), 4)
