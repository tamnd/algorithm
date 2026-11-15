# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sentential-decision-diagram/. The authors are listed in prov/YVT6ET.jsonl.
"""Tests of the SDD package against truth tables on at most 6 variables."""

import random

from sentential_decision_diagram import (
    AND,
    FALSE,
    OR,
    TRUE,
    SddManager,
    balanced,
    random_vtree,
    right_linear,
)


def table_of(mgr: SddManager, u: int, n: int) -> tuple:
    out = []
    for a in range(1 << n):
        asg = {v: bool((a >> (v - 1)) & 1) for v in range(1, n + 1)}
        out.append(mgr.evaluate(u, asg))
    return tuple(out)


def random_formula(rng: random.Random, n: int, depth: int):
    if depth == 0 or rng.random() < 0.2:
        v = rng.randint(1, n)
        return ("lit", v if rng.random() < 0.5 else -v)
    op = rng.choice(["and", "or", "not"])
    if op == "not":
        return ("not", random_formula(rng, n, depth - 1))
    return (op, random_formula(rng, n, depth - 1), random_formula(rng, n, depth - 1))


def formula_table(f, n: int) -> tuple:
    def ev(f, a):
        if f[0] == "lit":
            l = f[1]
            return bool((a >> (abs(l) - 1)) & 1) == (l > 0)
        if f[0] == "not":
            return not ev(f[1], a)
        if f[0] == "and":
            return ev(f[1], a) and ev(f[2], a)
        return ev(f[1], a) or ev(f[2], a)

    return tuple(ev(f, a) for a in range(1 << n))


def build(mgr: SddManager, f) -> int:
    if f[0] == "lit":
        return mgr.literal(f[1])
    if f[0] == "not":
        return mgr.negate(build(mgr, f[1]))
    a, b = build(mgr, f[1]), build(mgr, f[2])
    return mgr.apply(a, b, AND if f[0] == "and" else OR)


def vtrees(rng: random.Random, n: int):
    order = list(range(1, n + 1))
    rng.shuffle(order)
    return [right_linear(order), balanced(order), random_vtree(order, rng)]


def from_table(mgr: SddManager, table: tuple, n: int, rng: random.Random) -> int:
    """The DNF of the models, built term by term in a random order."""
    models = [a for a in range(1 << n) if table[a]]
    rng.shuffle(models)
    u = FALSE
    for a in models:
        lits = [v if (a >> (v - 1)) & 1 else -v for v in range(1, n + 1)]
        rng.shuffle(lits)
        t = TRUE
        for l in lits:
            t = mgr.conjoin(t, mgr.literal(l))
        u = mgr.disjoin(u, t)
    return u


def from_cnf_table(mgr: SddManager, table: tuple, n: int, rng: random.Random) -> int:
    """The CNF of the non-models, built clause by clause in a random order."""
    rows = [a for a in range(1 << n) if not table[a]]
    rng.shuffle(rows)
    u = TRUE
    for a in rows:
        lits = [-v if (a >> (v - 1)) & 1 else v for v in range(1, n + 1)]
        rng.shuffle(lits)
        c = FALSE
        for l in lits:
            c = mgr.disjoin(c, mgr.literal(l))
        u = mgr.conjoin(u, c)
    return u


def check_invariants(mgr: SddManager, u: int) -> None:
    vt = mgr.vtree
    for x in mgr.reachable(u):
        key = mgr.nodes[x]
        if key[0] != "dec":
            continue
        v = key[1]
        primes = [p for p, s in key[2]]
        subs = [s for p, s in key[2]]
        assert len(set(subs)) == len(subs)  # compressed
        assert not (len(key[2]) == 1)  # trimmed: no {(TRUE, a)}
        assert set(subs) != {TRUE, FALSE}  # trimmed: no {(a, TRUE), (not a, FALSE)}
        for p in primes:
            assert p != FALSE
            assert p == TRUE or vt.inside(mgr.vt[p], vt.left[v])
        for s in subs:
            assert s in (TRUE, FALSE) or vt.inside(mgr.vt[s], vt.right[v])
        # the primes form a partition
        acc = FALSE
        for i, p in enumerate(primes):
            for q in primes[i + 1 :]:
                assert mgr.conjoin(p, q) == FALSE
            acc = mgr.disjoin(acc, p)
        assert acc == TRUE


def test_apply_matches_truth_tables():
    rng = random.Random(1)
    for _ in range(120):
        n = rng.randint(1, 6)
        for vt in vtrees(rng, n):
            mgr = SddManager(vt)
            f = random_formula(rng, n, 5)
            g = random_formula(rng, n, 5)
            a, b = build(mgr, f), build(mgr, g)
            ta, tb = formula_table(f, n), formula_table(g, n)
            assert table_of(mgr, a, n) == ta
            assert table_of(mgr, mgr.conjoin(a, b), n) == tuple(x and y for x, y in zip(ta, tb))
            assert table_of(mgr, mgr.disjoin(a, b), n) == tuple(x or y for x, y in zip(ta, tb))
            assert table_of(mgr, mgr.negate(a), n) == tuple(not x for x in ta)
            check_invariants(mgr, mgr.conjoin(a, b))
            check_invariants(mgr, mgr.disjoin(a, b))


def test_canonical_for_a_fixed_vtree():
    rng = random.Random(2)
    for _ in range(80):
        n = rng.randint(1, 5)
        for vt in vtrees(rng, n):
            mgr = SddManager(vt)
            f = random_formula(rng, n, 5)
            t = formula_table(f, n)
            a = build(mgr, f)
            b = from_table(mgr, t, n, rng)
            c = from_cnf_table(mgr, t, n, rng)
            assert a == b == c
            assert mgr.negate(mgr.negate(a)) == a


def test_model_count_matches_brute_force():
    rng = random.Random(3)
    for _ in range(150):
        n = rng.randint(1, 6)
        for vt in vtrees(rng, n):
            mgr = SddManager(vt)
            f = random_formula(rng, n, 6)
            assert mgr.model_count(build(mgr, f)) == sum(formula_table(f, n))
    mgr = SddManager(balanced([1, 2, 3]))
    assert mgr.model_count(TRUE) == 8 and mgr.model_count(FALSE) == 0


def obdd_node_count(table: tuple, order: list[int], n: int) -> int:
    """The nodes of the reduced OBDD for the order: distinct non-constant subfunctions."""
    seen = set()
    for i in range(len(order) + 1):
        fixed = order[:i]
        for bits in range(1 << i):
            sub = []
            for a in range(1 << n):
                b = a
                for j, v in enumerate(fixed):
                    b = (b & ~(1 << (v - 1))) | (((bits >> j) & 1) << (v - 1))
                sub.append(table[b])
            sub = tuple(sub)
            if len(set(sub)) == 2:
                seen.add(sub)
    return len(seen)


def test_right_linear_vtree_gives_the_obdd():
    """On a right-linear vtree each node reached through subs is one node of the reduced OBDD."""
    rng = random.Random(4)
    for _ in range(100):
        n = rng.randint(1, 5)
        order = list(range(1, n + 1))
        rng.shuffle(order)
        mgr = SddManager(right_linear(order))
        f = random_formula(rng, n, 5)
        u = build(mgr, f)
        via_subs = set()
        stack = [u]
        while stack:
            x = stack.pop()
            if x in (TRUE, FALSE) or x in via_subs:
                continue
            via_subs.add(x)
            if mgr.nodes[x][0] == "dec":
                stack.extend(s for p, s in mgr.nodes[x][2])
        assert len(via_subs) == obdd_node_count(formula_table(f, n), order, n)
        for x in mgr.reachable(u):
            if mgr.nodes[x][0] == "dec":
                assert all(p == TRUE or mgr.nodes[p][0] == "lit" for p, s in mgr.nodes[x][2])


def test_worked_example():
    # f = (x1 and x2) or (x3 and x4) on the balanced vtree ((1, 2), (3, 4)).
    mgr = SddManager(balanced([1, 2, 3, 4]))
    x = {v: mgr.literal(v) for v in range(1, 5)}
    f = mgr.disjoin(mgr.conjoin(x[1], x[2]), mgr.conjoin(x[3], x[4]))
    key = mgr.nodes[f]
    assert key[0] == "dec" and key[1] == mgr.vtree.root
    elems = dict(key[2])
    a12 = mgr.conjoin(x[1], x[2])
    assert elems[a12] == TRUE
    assert elems[mgr.negate(a12)] == mgr.conjoin(x[3], x[4])
    assert mgr.model_count(f) == 7
    assert mgr.size(f) == 8
