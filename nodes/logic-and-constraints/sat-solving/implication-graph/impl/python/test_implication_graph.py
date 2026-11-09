# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implication-graph/. The authors are listed in prov/2V1W4P.jsonl.

import random

import pytest

from implication_graph import ImplicationGraph


def table(n: int, clauses) -> int:
    """Bitset over the 2^n assignments of the models of the clauses."""
    size = 1 << n
    full = (1 << size) - 1
    xs = []
    for v in range(n):
        period = 1 << (v + 1)
        block = ((1 << (1 << v)) - 1) << (1 << v)
        xs.append(block * sum(1 << (i * period) for i in range(size // period)))
    f = full
    for c in clauses:
        b = 0
        for q in c:
            b |= xs[q - 1] if q > 0 else full ^ xs[-q - 1]
        f &= b
    return f


def propagate(g: ImplicationGraph, clauses) -> list[int] | None:
    """Naive unit propagation into g. Return a false clause, or None."""
    changed = True
    while changed:
        changed = False
        for c in clauses:
            vals = [g.value(q) for q in c]
            if 1 in vals:
                continue
            free = [q for q, s in zip(c, vals) if s == 0]
            if not free:
                return list(c)
            if len(free) == 1:
                g.imply(free[0], c)
                changed = True
    return None


def brute_force_uips(g: ImplicationGraph) -> list[int]:
    """Nodes u of the conflict level such that removing u cuts every path from
    the decision of that level to the conflict node."""
    assert g.kappa is not None
    d = max(g.level[w] for w in g.kappa)
    succ: dict[object, list[object]] = {v: [] for v in g.trail}
    for v in g.trail:
        for w in g.preds[v]:
            succ[w].append(v)
    for w in g.kappa:
        succ[w].append("kappa")
    delta = g.trail[g.lim[d - 1]]
    out = []
    for u in g.trail:
        if g.level[u] != d:
            continue
        if u == delta:
            out.append(u)
            continue
        seen = {delta}
        stack = [delta]
        hit = False
        while stack:
            v = stack.pop()
            if v == "kappa":
                hit = True
                break
            for w in succ[v]:
                if w != u and w not in seen:
                    seen.add(w)
                    stack.append(w)
        if not hit:
            out.append(u)
    return sorted(out, key=lambda v: -g.pos[v])


EXAMPLE = [[1, 2], [1, 3, 7], [-2, -3, 4], [-4, 5, 8], [-4, 6, 9], [-5, -6]]


def test_page_example() -> None:
    g = ImplicationGraph(9)
    for lit in (-7, -8, -9):
        g.decide(lit)
        assert propagate(g, EXAMPLE) is None
    g.decide(-1)
    confl = propagate(g, EXAMPLE)
    assert confl == [-5, -6]
    g.conflict(confl)
    assert g.trail == [-7, -8, -9, -1, 2, 3, 4, 5, 6]
    assert g.preds[4] == [2, 3] and g.preds[5] == [4, -8] and g.preds[6] == [4, -9]
    assert g.uips() == [4, -1]
    clause, b = g.first_uip_clause()
    assert clause == [-4, 9, 8] and b == 3
    assert g.check_invariant()
    g.backjump(b)
    assert g.trail == [-7, -8, -9] and g.kappa is None
    g.imply(-4, clause)
    assert g.preds[-4] == [-9, -8]


def test_errors() -> None:
    g = ImplicationGraph(2)
    g.decide(1)
    with pytest.raises(ValueError):
        g.decide(-1)
    with pytest.raises(ValueError):
        g.imply(2, [2, 1])
    with pytest.raises(ValueError):
        g.uips()
    g.imply(2, [2, -1])
    g.conflict([-1, -2])
    assert g.uips() == [1]  # the edge 1 -> kappa bypasses node 2
    assert g.first_uip_clause() == ([-1], 0)


def test_random_runs_against_brute_force() -> None:
    rng = random.Random(1996)
    conflicts = 0
    for _ in range(800):
        n = rng.randint(3, 10)
        f = []
        for _ in range(rng.randint(2 * n, 5 * n)):
            vs = rng.sample(range(1, n + 1), rng.randint(2, 3))
            f.append([v if rng.random() < 0.5 else -v for v in vs])
        models = table(n, f)
        full = (1 << (1 << n)) - 1
        g = ImplicationGraph(n)
        learned: list[list[int]] = []
        confl = propagate(g, f)
        for _ in range(60):
            if confl is None:
                free = [v for v in range(1, n + 1) if g.value(v) == 0]
                if not free:
                    assert all(any(g.value(q) == 1 for q in c) for c in f)
                    break
                v = rng.choice(free)
                g.decide(v if rng.random() < 0.5 else -v)
                confl = propagate(g, f + learned)
                assert g.check_invariant()
                continue
            if g.decision_level() == 0:
                assert models == 0
                break
            model_trail = [(x, g.level[x]) for x in g.trail]
            conflicts += 1
            g.conflict(confl)
            assert g.check_invariant()
            ups = g.uips()
            assert ups == brute_force_uips(g)
            clause, b = g.first_uip_clause()
            assert -clause[0] == ups[0]
            d = g.decision_level()
            assert [g.level[-q] for q in clause].count(d) == 1
            assert all(g.value(q) == -1 for q in clause)
            assert b == max((g.level[-q] for q in clause[1:]), default=0)
            # the learned clause follows from F
            cb = table(n, [clause]) if clause else 0
            assert models & (full ^ cb) == 0
            g.backjump(b)
            assert g.check_invariant()
            assert [(x, lv) for x, lv in model_trail if lv <= b] == [(x, g.level[x]) for x in g.trail]
            assert g.value(clause[0]) == 0 and all(g.value(q) == -1 for q in clause[1:])
            learned.append(clause)
            g.imply(clause[0], clause)
            confl = propagate(g, f + learned)
    assert conflicts > 600
