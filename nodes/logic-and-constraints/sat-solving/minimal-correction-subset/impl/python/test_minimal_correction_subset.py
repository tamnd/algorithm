# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimal-correction-subset/. The authors are listed in prov/W95AD0.jsonl.

import itertools
import random

from minimal_correction_subset import (Oracle, all_mcses, all_muses, cld_mcs, linear_mcs,
                                       minimal_hitting_sets)

PAGE = [[1], [-1, 2], [-2], [-1, 3], [-3, 2], [3, 4]]


def satisfiable(clauses: list[list[int]]) -> bool:
    vs = sorted({abs(a) for c in clauses for a in c})
    for bits in itertools.product([False, True], repeat=len(vs)):
        val = dict(zip(vs, bits))
        if all(any(val[abs(a)] == (a > 0) for a in c) for c in clauses):
            return True
    return False


def brute(soft: list[list[int]], hard: list[list[int]]) -> tuple[set, set]:
    """All MCSes and all MUSes, from the satisfiability of every subset."""
    m = len(soft)
    sat = {s: satisfiable(hard + [soft[i] for i in s])
           for r in range(m + 1) for s in itertools.combinations(range(m), r)}
    unsat = [set(s) for s, ok in sat.items() if not ok]
    muses = {s for s, ok in sat.items() if not ok and not any(u < set(s) for u in unsat)}
    corr = [set(range(m)) - set(s) for s, ok in sat.items() if ok]
    mcses = {tuple(sorted(c)) for c in corr if not any(d < c for d in corr)}
    return mcses, muses


def is_correction_set(soft, hard, c) -> bool:
    return satisfiable(hard + [soft[i] for i in range(len(soft)) if i not in c])


def check_mcs(soft, hard, mcs) -> None:
    assert is_correction_set(soft, hard, set(mcs))
    for r in range(len(mcs)):  # every proper subset fails
        for s in itertools.combinations(mcs, r):
            assert not is_correction_set(soft, hard, set(s))


def random_formula(rng: random.Random, n: int, m: int) -> list[list[int]]:
    out = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), rng.randint(1, min(3, n)))
        out.append([v if rng.random() < 0.5 else -v for v in vs])
    return out


def test_page_example() -> None:
    assert sorted(all_mcses(PAGE)) == [[0], [1, 3], [1, 4], [2]]
    assert all_muses(PAGE) == [[0, 1, 2], [0, 2, 3, 4]]
    for algo in (linear_mcs, cld_mcs):
        check_mcs(PAGE, [], algo(PAGE))


def test_unsatisfiable_hard_part() -> None:
    assert linear_mcs([[1]], [[2], [-2]]) is None
    assert cld_mcs([[1]], [[2], [-2]]) is None


def test_against_brute_force() -> None:
    rng = random.Random(2008)
    for _ in range(80):
        n = rng.randint(2, 6)
        soft = random_formula(rng, n, rng.randint(3, 10))
        hard = []
        if rng.random() < 0.3:
            h = random_formula(rng, n, rng.randint(1, 2))
            if satisfiable(h):
                hard = h
        mcses, muses = brute(soft, hard)
        for algo in (linear_mcs, cld_mcs):
            o = Oracle()
            mcs = algo(soft, hard, o)
            check_mcs(soft, hard, mcs)
            assert tuple(mcs) in mcses
            assert o.calls <= len(soft) + 2
        found = all_mcses(soft, hard)
        assert len(found) == len(mcses)  # each MCS is found once
        assert {tuple(c) for c in found} == mcses
        # The duality, both ways.
        assert {tuple(s) for s in minimal_hitting_sets([list(c) for c in mcses])} == muses
        if muses:
            assert {tuple(s) for s in minimal_hitting_sets([list(s) for s in muses])} == mcses


def test_satisfiable_formula_has_only_the_empty_mcs() -> None:
    f = [[1, 2], [-1], [-2, 3]]
    assert linear_mcs(f) == [] and cld_mcs(f) == []
    assert all_mcses(f) == [[]] and all_muses(f) == []


def test_minimal_hitting_sets() -> None:
    assert minimal_hitting_sets([[1, 2], [2, 3], [3, 1]]) == [[1, 2], [1, 3], [2, 3]]
    assert minimal_hitting_sets([[1], [1, 2]]) == [[1]]
    assert minimal_hitting_sets([]) == [[]]
