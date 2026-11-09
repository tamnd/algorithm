# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/failed-literal-probing/. The authors are listed in prov/SWRBBT.jsonl.

import itertools
import random

from failed_literal_probing import probe, simplify, unit_propagate


def models(clauses: list[list[int]], n: int) -> set[tuple[bool, ...]]:
    out = set()
    for bits in itertools.product([False, True], repeat=n):
        if all(any(bits[abs(a) - 1] == (a > 0) for a in c) for c in clauses):
            out.add(bits)
    return out


def random_cnf(rng: random.Random, n: int, m: int) -> list[list[int]]:
    cnf = []
    for _ in range(m):
        k = rng.choice([2, 2, 3])
        vs = rng.sample(range(1, n + 1), min(k, n))
        cnf.append([v if rng.random() < 0.5 else -v for v in vs])
    return cnf


PAGE = [[-1, 2], [-1, 3], [-2, -3, 4], [-1, -4], [1, 5, 6], [-5, 7], [-6, 7]]


def test_page_example() -> None:
    assert unit_propagate(PAGE, {1: True}) is None  # x1 fails
    fixed = probe(PAGE, 7)
    assert fixed == {1: False, 7: True}
    assert models(PAGE, 7) == models(simplify(PAGE, fixed), 7)


def test_units_are_implied_and_fixpoint() -> None:
    rng = random.Random(1990)
    for _ in range(500):
        n = rng.randint(1, 9)
        f = random_cnf(rng, n, rng.randint(1, 4 * n))
        mf = models(f, n)
        fixed = probe(f, n)
        if fixed is None:
            assert not mf
            continue
        for v, b in fixed.items():  # every unit holds in every model
            assert all(m[v - 1] == b for m in mf)
        assert models(simplify(f, fixed), n) == mf
        for x in range(1, n + 1):  # no failed literal is left
            if x not in fixed:
                pos = unit_propagate(f, {**fixed, x: True})
                neg = unit_propagate(f, {**fixed, x: False})
                assert pos is not None and neg is not None
                assert not any(v not in fixed and neg.get(v) == b for v, b in pos.items())


def test_probing_is_incomplete() -> None:
    # all 8 clauses over 3 variables: unsatisfiable, yet no literal fails
    f = [[a * 1, b * 2, c * 3] for a in (1, -1) for b in (1, -1) for c in (1, -1)]
    assert not models(f, 3)
    assert probe(f, 3) == {}
