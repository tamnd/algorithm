# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/drat-proof/. The authors are listed in prov/9RG6K9.jsonl.

import itertools
import random

from drat_proof import (cdcl_with_proof, check_drat, format_drat, is_rat, is_rup,
                        parse_drat)

ALL8 = [[a * 1, b * 2, c * 3] for a in (1, -1) for b in (1, -1) for c in (1, -1)]


def models(clauses: list[list[int]], n: int) -> list[tuple[bool, ...]]:
    return [b for b in itertools.product([False, True], repeat=n)
            if all(any(b[abs(a) - 1] == (a > 0) for a in c) for c in clauses)]


def random_cnf(rng: random.Random, n: int, m: int) -> list[list[int]]:
    cnf = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), min(3, n))
        cnf.append([v if rng.random() < 0.5 else -v for v in vs])
    return cnf


def test_page_example() -> None:
    proof = parse_drat("1 2 0\n1 0\nd 1 2 0\n2 0\n0\n")
    assert check_drat(ALL8, proof) == (True, None)
    assert format_drat(proof) == "1 2 0\n1 0\nd 1 2 0\n2 0\n0\n"


def test_rat_unit_on_page() -> None:
    # (x1) is not RUP for ALL8, but it is RAT on x1.
    assert not is_rup(ALL8, [1])
    assert is_rat(ALL8, [1], 1)
    # Without the lemma (x2) the empty clause is not RUP.
    assert check_drat(ALL8, [("a", [1]), ("a", [])]) == (False, 1)


def test_broken_step_is_rejected() -> None:
    # Without (-x1 or -x2 or x3) the only model is x1 = x2 = 1, x3 = 0. The
    # lemma (-x1 or -x2) removes it, so it can be neither RUP nor RAT.
    f = [c for c in ALL8 if c != [-1, -2, 3]]
    assert len(models(f, 3)) == 1
    g = f + [[1, 2]]
    assert not is_rup(g, [-1, -2]) and not is_rat(g, [-1, -2], -1)
    assert check_drat(f, [("a", [1, 2]), ("a", [-1, -2]), ("a", [])]) == (False, 1)
    # The empty clause first is rejected when unit propagation finds no conflict.
    assert check_drat(ALL8, [("a", [])]) == (False, 0)
    # A proof without the empty clause is not a refutation.
    assert check_drat(ALL8, [("a", [1, 2])]) == (False, None)


def test_extension_definition_is_rat() -> None:
    f = [[1, 2], [-1, 3]]
    proof = [("a", [-4, 1]), ("a", [-4, 2]), ("a", [4, -1, -2])]
    assert check_drat(f, proof) == (False, None)  # accepted steps, no refutation
    assert not is_rup(f, [-4, 1])


def test_cdcl_proofs_are_accepted() -> None:
    rng = random.Random(9)
    unsat = 0
    for trial in range(300):
        n = rng.randint(3, 10)
        f = random_cnf(rng, n, rng.randint(2 * n, 6 * n))
        ms = models(f, n)
        model, proof = cdcl_with_proof(f, n, restart_every=rng.randint(1, 6), delete=trial % 2 == 0)
        if ms:
            assert model is not None
            assert all(any(model[abs(a)] == (a > 0) for a in c) for c in f)
        else:
            unsat += 1
            assert model is None
            assert check_drat(f, proof) == (True, None)
            assert check_drat(f, parse_drat(format_drat(proof))) == (True, None)
    assert unsat > 50


def test_proof_breaks_without_a_clause() -> None:
    # Remove one clause from an unsatisfiable formula so that it becomes
    # satisfiable. A sound checker must then reject the old proof.
    rng = random.Random(14)
    broken = 0
    while broken < 40:
        n = rng.randint(3, 9)
        f = random_cnf(rng, n, 5 * n)
        model, proof = cdcl_with_proof(f, n)
        if model is not None:
            continue
        g = f[: len(f) - 1]
        if not models(g, n):
            continue
        broken += 1
        ok, _ = check_drat(g, proof)
        assert not ok


def test_accepted_steps_preserve_satisfiability() -> None:
    rng = random.Random(3)
    for _ in range(400):
        n = rng.randint(2, 6)
        f = random_cnf(rng, n, rng.randint(1, 3 * n))
        c = [v if rng.random() < 0.5 else -v for v in rng.sample(range(1, n + 1), rng.randint(1, n))]
        before = bool(models(f, n))
        if is_rup(f, c):
            assert all(any(m[abs(a) - 1] == (a > 0) for a in c) for m in models(f, n))
        elif is_rat(f, c, c[0]):
            assert bool(models(f + [c], n)) == before
