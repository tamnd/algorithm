# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimal-unsatisfiable-subset/. The authors are listed in prov/V0RSZE.jsonl.

import itertools
import math
import random

from minimal_unsatisfiable_subset import Oracle, deletion_mus, quickxplain

PAGE = [[1], [-1, 2], [-2], [-1, 3], [-3, 2], [3, 4]]


def satisfiable(clauses: list[list[int]]) -> bool:
    vs = sorted({abs(a) for c in clauses for a in c})
    for bits in itertools.product([False, True], repeat=len(vs)):
        val = dict(zip(vs, bits))
        if all(any(val[abs(a)] == (a > 0) for a in c) for c in clauses):
            return True
    return False


def all_muses(soft: list[list[int]], hard: list[list[int]]) -> set[tuple[int, ...]]:
    out = set()
    for r in range(len(soft) + 1):
        for s in itertools.combinations(range(len(soft)), r):
            if any(set(t) <= set(s) for t in out):
                continue  # a superset of an MUS is not minimal
            if not satisfiable(hard + [soft[i] for i in s]):
                out.add(s)
    return out


def check_mus(soft: list[list[int]], hard: list[list[int]], mus: list[int]) -> None:
    assert not satisfiable(hard + [soft[i] for i in mus])
    if len(mus) <= 7:  # every proper subset, literally
        for r in range(len(mus)):
            for s in itertools.combinations(mus, r):
                assert satisfiable(hard + [soft[i] for i in s])
    else:  # the maximal proper subsets; smaller ones follow by monotonicity
        for i in mus:
            assert satisfiable(hard + [soft[j] for j in mus if j != i])


def qx_bound(m: int, k: int) -> int:
    depth = math.ceil(math.log2(m)) if m > 1 else 0
    return 2 + sum(min(2 ** d, 2 * k) for d in range(1, depth + 1))


def random_formula(rng: random.Random, n: int, m: int) -> list[list[int]]:
    out = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), rng.randint(1, min(3, n)))
        out.append([v if rng.random() < 0.5 else -v for v in vs])
    return out


def test_page_example() -> None:
    o = Oracle()
    assert deletion_mus(PAGE, oracle=o) == [0, 2, 3, 4]
    assert o.calls == len(PAGE) + 1
    o = Oracle()
    assert quickxplain(PAGE, oracle=o) == [0, 1, 2]
    assert o.calls <= qx_bound(len(PAGE), 3)
    assert all_muses(PAGE, []) == {(0, 1, 2), (0, 2, 3, 4)}


def test_satisfiable_input_has_no_mus() -> None:
    f = [[1, 2], [-1], [-2, 3]]
    assert deletion_mus(f) is None and quickxplain(f) is None


def test_against_brute_force() -> None:
    rng = random.Random(1987)
    tried = 0
    while tried < 80:
        n = rng.randint(2, 6)
        m = rng.randint(4, 11)
        soft = random_formula(rng, n, m)
        if satisfiable(soft):
            continue
        tried += 1
        hard = []
        if rng.random() < 0.3:  # move a few clauses to the hard part
            cut = rng.randint(1, 2)
            if satisfiable(soft[:cut]):
                hard, soft = soft[:cut], soft[cut:]
        muses = all_muses(soft, hard)
        for algo in (deletion_mus, quickxplain):
            o = Oracle()
            mus = algo(soft, hard, o)
            check_mus(soft, hard, mus)
            assert tuple(mus) in muses
            if algo is deletion_mus:
                assert o.calls == len(soft) + 1
            else:
                assert o.calls <= qx_bound(len(soft), len(mus))


def test_minimal_unsatisfiable_formulas_have_more_clauses_than_variables() -> None:
    # Tarsi's lemma: a minimally unsatisfiable formula has m >= n + 1.
    rng = random.Random(5)
    for _ in range(200):
        f = random_formula(rng, rng.randint(2, 8), rng.randint(4, 16))
        if satisfiable(f):
            continue
        mus = [f[i] for i in deletion_mus(f)]
        assert len(mus) >= len({abs(a) for c in mus for a in c}) + 1


def test_quickxplain_beats_deletion_on_a_small_core() -> None:
    # 2 conflicting units hidden among 62 satisfiable clauses.
    soft = [[v] for v in range(3, 65)]
    soft[17] = [1]
    soft[40] = [-1]
    o1, o2 = Oracle(), Oracle()
    assert deletion_mus(soft, oracle=o1) == quickxplain(soft, oracle=o2) == [17, 40]
    assert o1.calls == 63
    assert o2.calls <= qx_bound(62, 2) < 63
