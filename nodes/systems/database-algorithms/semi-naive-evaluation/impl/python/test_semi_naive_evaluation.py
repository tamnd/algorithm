# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semi-naive-evaluation/. The authors are listed in prov/EVCHB0.jsonl.

import random

from semi_naive_evaluation import count_true_instances, naive, semi_naive, semi_naive_basic

E = ("edge", ("X", "Y"))

TC_RIGHT = [
    (("path", ("X", "Y")), [("edge", ("X", "Y"))]),
    (("path", ("X", "Y")), [("edge", ("X", "Z")), ("path", ("Z", "Y"))]),
]
TC_LEFT = [
    (("path", ("X", "Y")), [("edge", ("X", "Y"))]),
    (("path", ("X", "Y")), [("path", ("X", "Z")), ("edge", ("Z", "Y"))]),
]
TC_DOUBLE = [
    (("path", ("X", "Y")), [("edge", ("X", "Y"))]),
    (("path", ("X", "Y")), [("path", ("X", "Z")), ("path", ("Z", "Y"))]),
]
SAME_GENERATION = [
    (("sg", ("X", "Y")), [("flat", ("X", "Y"))]),
    (("sg", ("X", "Y")), [("up", ("X", "U")), ("sg", ("U", "V")), ("down", ("V", "Y"))]),
]


def chain(n):
    return {("edge", (i, i + 1)) for i in range(1, n)}


def random_graph(rng, n, m):
    return {("edge", (rng.randrange(n), rng.randrange(n))) for _ in range(m)}


def reachable_pairs(edges):
    succ = {}
    for _, (a, b) in edges:
        succ.setdefault(a, set()).add(b)
    out = set()
    for s in succ:
        stack, seen = list(succ[s]), set()
        while stack:
            x = stack.pop()
            if x not in seen:
                seen.add(x)
                stack.extend(succ.get(x, ()))
        out |= {("path", (s, t)) for t in seen}
    return out


def test_chain_counts() -> None:
    # The example of the page: a chain of 4 nodes.
    db = chain(4)
    m1, f1 = naive(TC_RIGHT, db)
    m2, f2 = semi_naive(TC_RIGHT, db)
    assert m1 == m2 == db | reachable_pairs(db)
    assert f2 == 6 and f1 == 20
    db = chain(20)
    _, f1 = naive(TC_RIGHT, db)
    _, f2 = semi_naive(TC_RIGHT, db)
    assert f2 == 190 and f1 == 2660


def test_nonlinear_rule_counts() -> None:
    db = chain(10)
    m, f = semi_naive(TC_DOUBLE, db)
    mb, fb = semi_naive_basic(TC_DOUBLE, db)
    assert m == mb == db | reachable_pairs(db)
    assert f == count_true_instances(TC_DOUBLE, m)
    assert fb > f


def test_random_graphs_all_programs() -> None:
    rng = random.Random(31)
    for _ in range(200):
        db = random_graph(rng, rng.randint(1, 8), rng.randint(0, 14))
        expected = db | reachable_pairs(db)
        for prog in (TC_RIGHT, TC_LEFT, TC_DOUBLE):
            m1, f1 = naive(prog, db)
            m2, f2 = semi_naive(prog, db)
            m3, f3 = semi_naive_basic(prog, db)
            assert m1 == m2 == m3 == expected
            # Each true rule instance is fired exactly once.
            assert f2 == count_true_instances(prog, m2)
            assert f2 <= f3 and f2 <= f1
            if prog is not TC_DOUBLE:
                assert f3 == f2  # linear rules: the basic form repeats nothing either


def test_same_generation() -> None:
    rng = random.Random(32)
    for _ in range(200):
        n = rng.randint(1, 7)
        db = set()
        for name in ("up", "down", "flat"):
            db |= {(name, (rng.randrange(n), rng.randrange(n))) for _ in range(rng.randint(0, 8))}
        m1, f1 = naive(SAME_GENERATION, db)
        m2, f2 = semi_naive(SAME_GENERATION, db)
        assert m1 == m2
        assert f2 == count_true_instances(SAME_GENERATION, m2) <= f1


def random_program(rng):
    variables = "XYZW"
    program = []
    for _ in range(rng.randint(1, 4)):
        body = []
        for _ in range(rng.randint(1, 3)):
            pred = rng.choice(("e", "e", "p", "q"))
            body.append((pred, (rng.choice(variables), rng.choice(variables))))
        used = sorted({t for _, ts in body for t in ts})
        head = (rng.choice(("p", "q")), (rng.choice(used), rng.choice(used)))
        program.append((head, body))
    return program


def test_random_programs() -> None:
    rng = random.Random(33)
    for _ in range(500):
        program = random_program(rng)
        n = rng.randint(1, 5)
        db = {("e", (rng.randrange(n), rng.randrange(n))) for _ in range(rng.randint(0, 8))}
        m1, f1 = naive(program, db)
        m2, f2 = semi_naive(program, db)
        m3, _ = semi_naive_basic(program, db)
        assert m1 == m2 == m3
        assert f2 == count_true_instances(program, m2) <= f1


def test_edges() -> None:
    assert semi_naive(TC_RIGHT, set()) == (set(), 0)
    assert naive([], {("edge", (1, 2))}) == ({("edge", (1, 2))}, 0)
    loop = {("edge", (1, 1))}
    assert semi_naive(TC_RIGHT, loop)[0] == loop | {("path", (1, 1))}
    try:
        semi_naive(TC_RIGHT, {("path", (1, 2))})
    except ValueError:
        pass
    else:
        raise AssertionError("IDB facts in the database must be rejected")
