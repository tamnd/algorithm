# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/equivalent-literal-substitution/. The authors are listed in prov/5XGNFS.jsonl.

import itertools
import random

from equivalent_literal_substitution import els, reconstruct, sccs


def sat(clauses: list[list[int]], a: dict[int, bool]) -> bool:
    return all(any(a[abs(x)] == (x > 0) for x in c) for c in clauses)


def models(clauses: list[list[int]], variables: list[int]) -> list[dict[int, bool]]:
    out = []
    for bits in itertools.product([False, True], repeat=len(variables)):
        a = dict(zip(variables, bits))
        if sat(clauses, a):
            out.append(a)
    return out


def random_cnf(rng: random.Random, n: int, m: int) -> list[list[int]]:
    cnf = []
    for _ in range(m):
        k = rng.choice([2, 2, 2, 3])
        k = min(k, n)
        vs = rng.sample(range(1, n + 1), k)
        cnf.append([v if rng.random() < 0.5 else -v for v in vs])
    return cnf


def test_sccs_deep_chain() -> None:
    n = 5000
    succ = {i: [i + 1] for i in range(1, n)}
    succ[n] = [1]
    comps = sccs(list(range(1, n + 1)), succ)
    assert len(comps) == 1 and len(comps[0]) == n


def test_page_example() -> None:
    f = [[-1, 2], [-2, 3], [-3, 1], [1, 4, 5], [-2, -4], [3, -5, 6]]
    g, rep = els(f)
    assert rep == {2: 1, 3: 1}
    assert g == [[-1, -4], [1, -5, 6], [1, 4, 5]]
    assert len(models(f, list(range(1, 7)))) == len(models(g, [1, 4, 5, 6]))


def test_unsat_cycle() -> None:
    g, _ = els([[-1, 2], [-2, -1], [1, 3], [-3, 1], [1, -2], [-1, -3]])
    assert g is None


def test_model_bijection_and_reconstruction() -> None:
    rng = random.Random(1987)
    for _ in range(400):
        n = rng.randint(1, 8)
        f = random_cnf(rng, n, rng.randint(1, 3 * n))
        g, rep = els(f)
        all_vars = list(range(1, n + 1))
        mf = models(f, all_vars)
        if g is None:
            assert not mf
            continue
        kept = [v for v in all_vars if v not in rep]
        mg = models(g, kept)
        assert len(mg) == len(mf)  # x is a function of its representative
        seen = set()
        for a in mg:
            b = reconstruct(a, rep)
            assert sat(f, b)
            seen.add(tuple(b[v] for v in all_vars))
        assert len(seen) == len(mf)
