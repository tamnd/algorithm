# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pc-2/. The authors are listed in prov/JNRB9Z.jsonl.

import itertools
import random

from pc_2 import full_relations, get, pc2


def random_csp(rng: random.Random, n: int, d: int, density: float, tight: float):
    domains = [set(range(d)) for _ in range(n)]
    for dom in domains:
        for a in range(d):
            if rng.random() < 0.1:
                dom.discard(a)
    cons = {}
    for i, j in itertools.combinations(range(n), 2):
        if rng.random() < density:
            cons[(i, j)] = {(a, b) for a in range(d) for b in range(d) if rng.random() > tight}
    return domains, cons


def solutions(domains, cons):
    rel = full_relations([set(d) for d in domains], cons)
    return [t for t in itertools.product(*[sorted(d) for d in domains])
            if all((t[i], t[j]) in r for (i, j), r in rel.items())]


def reference(domains, cons):
    """Revise every triple until a full pass changes nothing, then drop dead values."""
    dom = [set(d) for d in domains]
    rel = full_relations(dom, cons)
    n = len(dom)
    changed = True
    while changed:
        changed = False
        for (i, j) in rel:
            for k in range(n):
                if k in (i, j):
                    continue
                rik, rkj = get(rel, i, k), get(rel, k, j)
                keep = {(a, b) for a, b in rel[(i, j)]
                        if any((a, c) in rik and (c, b) in rkj for c in dom[k])}
                if keep != rel[(i, j)]:
                    rel[(i, j)] = keep
                    changed = True
    for i in range(n):
        for j in range(n):
            if i != j:
                dom[i] &= {a for a, _ in get(rel, i, j)}
    rel = {(i, j): {(a, b) for a, b in r if a in dom[i] and b in dom[j]} for (i, j), r in rel.items()}
    return dom, rel


def strongly_path_consistent(dom, rel) -> bool:
    n = len(dom)
    for i, j in itertools.permutations(range(n), 2):
        rij = get(rel, i, j)
        if any(a not in dom[i] or b not in dom[j] for a, b in rij):
            return False
        if any(not any((a, b) in rij for b in dom[j]) for a in dom[i]):
            return False  # arc consistency fails
        for k in range(n):
            if k in (i, j):
                continue
            rik, rkj = get(rel, i, k), get(rel, k, j)
            if any(not any((a, c) in rik and (c, b) in rkj for c in dom[k]) for a, b in rij):
                return False
    return True


def test_triangle_two_colours() -> None:
    ne = {(1, 2), (2, 1)}
    ok, dom, rel = pc2([{1, 2}] * 3, {(0, 1): ne, (1, 2): ne, (0, 2): ne})
    assert ok is False


def test_example_four_cycle() -> None:
    ne = {(0, 1), (1, 0)}
    cons = {(0, 1): ne, (1, 2): ne, (2, 3): ne, (0, 3): ne}
    stats: dict[str, int] = {}
    ok, dom, rel = pc2([{0, 1}] * 4, cons, stats)
    assert ok and dom == [{0, 1}] * 4
    assert rel[(0, 2)] == {(0, 0), (1, 1)}
    assert rel[(1, 3)] == {(0, 0), (1, 1)}
    assert all(rel[k] == ne for k in cons)
    assert stats["revisions"] == 16


def test_edges() -> None:
    assert pc2([], {})[0] is True
    assert pc2([{1, 2}], {})[1] == [{1, 2}]
    ok, dom, rel = pc2([{0, 1}, {0, 1, 2}], {(0, 1): {(0, 1), (1, 1)}})
    assert ok and dom == [{0, 1}, {1}]
    assert pc2([{0}, {0}], {(1, 0): set()})[0] is False


def test_random_against_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(250):
        n, d = rng.randint(1, 5), rng.randint(1, 3)
        domains, cons = random_csp(rng, n, d, rng.random(), rng.random() * 0.6)
        stats: dict[str, int] = {}
        ok, dom, rel = pc2(domains, cons, stats)
        sols = solutions(domains, cons)
        for t in sols:  # no pair or value of a solution is removed
            assert all(t[i] in dom[i] for i in range(n))
            assert all((t[i], t[j]) in r for (i, j), r in rel.items())
        if not ok:
            assert sols == []
            continue
        assert strongly_path_consistent(dom, rel)
        assert (dom, rel) == reference(domains, cons)
        bound = n * (n - 1) * (n - 2) // 2 + n * (n - 1) * (n - 2) * d * d
        assert stats["revisions"] <= bound
        assert stats["checks"] <= stats["revisions"] * d ** 3


def test_boolean_binary_is_decided() -> None:
    # Binary Boolean relations are closed under majority, so strong path consistency decides them.
    rng = random.Random(6)
    for _ in range(300):
        n = rng.randint(1, 6)
        domains, cons = random_csp(rng, n, 2, rng.random(), rng.random() * 0.6)
        ok, _, _ = pc2(domains, cons)
        assert ok == bool(solutions(domains, cons))
