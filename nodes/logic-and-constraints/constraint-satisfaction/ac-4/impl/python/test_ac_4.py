# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ac-4/. The authors are listed in prov/ZP1QQ8.jsonl.

import itertools
import random
from collections import deque

from ac_4 import ac4, directed


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
    rel = directed(cons)
    return [t for t in itertools.product(*[sorted(d) for d in domains])
            if all((t[i], t[j]) in r for (i, j), r in rel.items())]


def is_arc_consistent(dom, cons) -> bool:
    rel = directed(cons)
    return all(any((a, b) in r for b in dom[j]) for (i, j), r in rel.items() for a in dom[i])


def ac3(domains, cons):
    """Reference AC-3 that does not stop at a wipe-out, so that it returns the full closure."""
    rel = directed(cons)
    dom = [set(d) for d in domains]
    queue = deque(rel)
    inq = set(rel)
    while queue:
        i, j = queue.popleft()
        inq.discard((i, j))
        gone = [a for a in dom[i] if not any((a, b) in rel[(i, j)] for b in dom[j])]
        if gone:
            dom[i] -= set(gone)
            for k, m in rel:
                if m == i and k != j and (k, i) not in inq:
                    queue.append((k, i))
                    inq.add((k, i))
    return dom


def test_example_chain() -> None:
    lt = {(a, b) for a in range(1, 4) for b in range(1, 4) if a < b}
    stats: dict[str, int] = {}
    ok, dom = ac4([{1, 2, 3}] * 3, {(0, 1): lt, (1, 2): lt}, stats)
    assert ok and dom == [{1}, {2}, {3}]
    assert stats["checks"] == 36


def test_triangle_is_arc_consistent_but_unsolvable() -> None:
    ne = {(1, 2), (2, 1)}
    cons = {(0, 1): ne, (1, 2): ne, (0, 2): ne}
    ok, dom = ac4([{1, 2}] * 3, cons)
    assert ok and dom == [{1, 2}] * 3
    assert solutions(dom, cons) == []


def test_edges() -> None:
    assert ac4([], {}) == (True, [])
    assert ac4([{5}], {}) == (True, [{5}])
    assert ac4([set()], {})[0] is False
    ok, dom = ac4([{0, 1}, {0, 1}, {7}], {(0, 1): set()})
    assert ok is False and dom == [set(), set(), {7}]


def test_random_against_brute_force_and_ac3() -> None:
    rng = random.Random(4)
    for _ in range(600):
        n, d = rng.randint(1, 6), rng.randint(1, 4)
        domains, cons = random_csp(rng, n, d, rng.random(), rng.random() * 0.7)
        stats: dict[str, int] = {}
        ok, dom = ac4(domains, cons, stats)
        sols = solutions(domains, cons)
        for t in sols:
            assert all(t[i] in dom[i] for i in range(n))
        # AC-4 and AC-3 give the same closure, also when it has an empty domain
        assert dom == ac3(domains, cons)
        assert is_arc_consistent(dom, cons)
        assert ok == all(dom)
        if not ok:
            assert sols == []
        e = len(cons)
        assert stats["checks"] <= 2 * e * d * d
        assert stats["decrements"] <= 2 * e * d * d
