# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazy-abstraction/. The authors are listed in prov/4S8GH7.jsonl.

import random

from lazy_abstraction import LazyAbstraction, lazy_abstraction

# L0: x := 0;  L1: while x < 2: x := x + 1;  L2: if x == 3 goto ERR (L3).
# The variable x ranges over 0 .. 3 and starts with any value.
LOOP = {
    "values": 4,
    "init_loc": 0,
    "init": {0, 1, 2, 3},
    "error": 3,
    "edges": [
        (0, 1, {v: [0] for v in range(4)}),
        (1, 1, {v: [v + 1] for v in range(4) if v < 2}),
        (1, 2, {v: [v] for v in range(4) if v >= 2}),
        (2, 3, {3: [3]}),
    ],
}


def explicit(program):
    """BFS over (location, valuation) pairs; True when the error location is reachable."""
    start = [(program["init_loc"], v) for v in program["init"]]
    seen, stack = set(start), list(start)
    while stack:
        l, v = stack.pop()
        if l == program["error"]:
            return True
        for src, dst, rel in program["edges"]:
            if src == l:
                for w in rel.get(v, ()):
                    if (dst, w) not in seen:
                        seen.add((dst, w))
                        stack.append((dst, w))
    return False


def check_invariant(program, inv):
    """The invariant holds initially, is closed under every edge, and excludes the error."""
    assert set(program["init"]) <= inv.get(program["init_loc"], frozenset())
    assert not inv.get(program["error"])
    for src, dst, rel in program["edges"]:
        for v in inv.get(src, ()):
            for w in rel.get(v, ()):
                assert w in inv.get(dst, frozenset())


def check_trace(program, trace):
    assert trace[0][0] == program["init_loc"] and trace[0][1] in program["init"]
    assert trace[-1][0] == program["error"]
    for (l, v), (m, w) in zip(trace, trace[1:]):
        assert any(s == l and d == m and w in rel.get(v, ()) for s, d, rel in program["edges"])


def test_loop():
    la = LazyAbstraction(LOOP)
    verdict, inv = la.run()
    assert verdict == "safe" and la.refinements == 1
    assert la.preds == {1: [frozenset({3})], 2: [frozenset({3})]}
    assert inv == {0: frozenset({0, 1, 2, 3}), 1: frozenset({0, 1, 2}), 2: frozenset({0, 1, 2}), 3: frozenset()}
    check_invariant(LOOP, inv)


def test_loop_with_bug():
    buggy = dict(LOOP)
    buggy["edges"] = LOOP["edges"][:1] + [(1, 1, {v: [v + 1] for v in range(4) if v < 3})] + LOOP["edges"][2:]
    verdict, trace = lazy_abstraction(buggy)
    assert verdict == "unsafe"
    assert trace == [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3)]
    check_trace(buggy, trace)


def rand_program(rng):
    L, V = rng.randint(2, 5), rng.randint(2, 6)
    edges = []
    for _ in range(rng.randint(1, 8)):
        src, dst = rng.randrange(L - 1), rng.randrange(L)
        rel = {v: rng.sample(range(V), rng.randint(1, 2)) for v in range(V) if rng.random() < 0.5}
        edges.append((src, dst, rel))
    init = set(rng.sample(range(V), rng.randint(1, V)))
    return {"values": V, "init_loc": 0, "init": init, "error": L - 1, "edges": edges}


def test_random_against_explicit_search():
    rng = random.Random(2002)
    count = {"safe": 0, "unsafe": 0}
    for _ in range(400):
        prog = rand_program(rng)
        verdict, out = lazy_abstraction(prog)
        count[verdict] += 1
        assert (verdict == "unsafe") == explicit(prog)
        if verdict == "safe":
            check_invariant(prog, out)
        else:
            check_trace(prog, out)
    assert count["safe"] > 50 and count["unsafe"] > 50


def test_predicates_stay_local():
    """A refinement adds predicates only at locations on the spurious path."""
    rng = random.Random(9)
    for _ in range(100):
        prog = rand_program(rng)
        la = LazyAbstraction(prog)
        la.run()
        for l, qs in la.preds.items():
            assert len(qs) == len(set(qs))
            assert all(0 < len(q) < prog["values"] for q in qs)
