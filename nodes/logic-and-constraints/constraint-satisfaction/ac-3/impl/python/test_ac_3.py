# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ac-3/. The authors are listed in prov/QXMHYC.jsonl.

import itertools
import random

from ac_3 import ac3, directed


def random_csp(rng: random.Random, n: int, d: int, density: float, tight: float):
    domains = [set(range(d)) for _ in range(n)]
    for dom in domains:
        for a in range(d):
            if rng.random() < 0.15:
                dom.discard(a)
    cons = {}
    for i, j in itertools.combinations(range(n), 2):
        if rng.random() < density:
            cons[(i, j)] = {(a, b) for a in range(d) for b in range(d) if rng.random() > tight}
    return domains, cons


def solutions(domains, cons):
    """Brute force over all assignments."""
    rel = directed(cons)
    out = []
    for t in itertools.product(*[sorted(d) for d in domains]):
        if all((t[i], t[j]) in r for (i, j), r in rel.items()):
            out.append(t)
    return out


def is_arc_consistent(dom, cons) -> bool:
    rel = directed(cons)
    return all(any((a, b) in r for b in dom[j]) for (i, j), r in rel.items() for a in dom[i])


def ac1(domains, cons):
    """Reference: revise every arc until a full pass changes nothing."""
    rel = directed(cons)
    dom = [set(d) for d in domains]
    changed = True
    while changed:
        changed = False
        for (i, j), r in rel.items():
            for a in list(dom[i]):
                if not any((a, b) in r for b in dom[j]):
                    dom[i].discard(a)
                    changed = True
    return dom


def test_example_chain() -> None:
    lt = {(a, b) for a in range(1, 4) for b in range(1, 4) if a < b}
    stats: dict[str, int] = {}
    ok, dom = ac3([{1, 2, 3}] * 3, {(0, 1): lt, (1, 2): lt}, stats)
    assert ok and dom == [{1}, {2}, {3}]
    assert stats["revisions"] == 5


def test_triangle_is_arc_consistent_but_unsolvable() -> None:
    ne = {(1, 2), (2, 1)}
    cons = {(0, 1): ne, (1, 2): ne, (0, 2): ne}
    ok, dom = ac3([{1, 2}] * 3, cons)
    assert ok and dom == [{1, 2}] * 3
    assert solutions(dom, cons) == []


def test_edges() -> None:
    assert ac3([], {}) == (True, [])
    assert ac3([{1}], {}) == (True, [{1}])
    assert ac3([set()], {})[0] is False
    ok, _ = ac3([{0, 1}, {0, 1}], {(0, 1): set()})
    assert ok is False
    # both directions given: they are intersected
    ok, dom = ac3([{0, 1}, {0, 1}], {(0, 1): {(0, 0), (1, 1)}, (1, 0): {(0, 0)}})
    assert ok and dom == [{0}, {0}]


def test_random_against_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(600):
        n, d = rng.randint(1, 6), rng.randint(1, 4)
        domains, cons = random_csp(rng, n, d, rng.random(), rng.random() * 0.7)
        stats: dict[str, int] = {}
        ok, dom = ac3(domains, cons, stats)
        sols = solutions(domains, cons)
        # no value of a solution is removed
        for t in sols:
            assert all(t[i] in dom[i] for i in range(n))
        if not ok:
            assert sols == []
            assert any(not x for x in ac1(domains, cons))
            continue
        assert all(dom)
        assert is_arc_consistent(dom, cons)
        # the closure does not depend on the order of the revisions
        assert dom == ac1(domains, cons)
        keys = list(cons)
        rng.shuffle(keys)
        assert ac3(domains, {k: cons[k] for k in keys})[1] == dom
        # at most 2e(d + 1) revisions, each with at most d^2 checks
        e = len(cons)
        assert stats["revisions"] <= 2 * e * (d + 1)
        assert stats["checks"] <= stats["revisions"] * d * d
