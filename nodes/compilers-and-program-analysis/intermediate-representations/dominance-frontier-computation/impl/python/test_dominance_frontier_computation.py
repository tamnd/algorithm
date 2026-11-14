# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dominance-frontier-computation/. The authors are listed in prov/VKF111.jsonl.

import random

import toyir
from dominance_frontier_computation import (
    dominance_frontiers,
    dominance_frontiers_walk,
    immediate_dominators,
    iterated_dominance_frontier,
    program_frontiers,
    program_graph,
)

ODD_SUM = """
# params: n
B1:
  i = 0
  s = 0
  jump B2
B2:
  t1 = i < n
  br t1 B3 B6
B3:
  t2 = i % 2
  br t2 B4 B5
B4:
  s = s + i
  jump B5
B5:
  i = i + 1
  jump B2
B6:
  ret s
"""


# ------------------------------------------------------------ brute force


def _reach(succ, root, removed=None):
    if root == removed:
        return set()
    seen = {root}
    stack = [root]
    while stack:
        v = stack.pop()
        for w in succ[v]:
            if w != removed and w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def brute_dominators(succ, root):
    """D[v] = the set of dominators of v: d dominates v if removing d cuts v off."""
    nodes = _reach(succ, root)
    dom = {v: set() for v in nodes}
    for d in nodes:
        left = _reach(succ, root, d)
        for v in nodes:
            if v not in left:
                dom[v].add(d)
    return dom


def brute_frontiers(succ, root):
    """DF by the definition: x dom p for an edge (p, y), and not x sdom y."""
    dom = brute_dominators(succ, root)
    df = {v: set() for v in dom}
    for p in dom:
        for y in succ[p]:
            for x in dom[p]:
                if not (x in dom[y] and x != y):
                    df[x].add(y)
    return df


def brute_idf(df, s):
    """DF+ as the limit of DF_1 = DF(S), DF_(i+1) = DF(S + DF_i)."""
    cur = set()
    while True:
        nxt = set()
        for x in set(s) | cur:
            nxt |= df[x]
        if nxt == cur:
            return cur
        cur = nxt


def random_graph(rng, n):
    succ = {v: [] for v in range(n)}
    for _ in range(rng.randint(0, 3 * n)):
        a, b = rng.randrange(n), rng.randrange(n)
        if b not in succ[a]:
            succ[a].append(b)
    for v in range(1, n):
        if rng.random() < 0.8:
            a = rng.randrange(v)
            if v not in succ[a]:
                succ[a].append(v)
    return succ


def ladder(n):
    """n nested repeat-until loops: headers h, latches l, exit e."""
    succ = {}
    for i in range(1, n + 1):
        succ["h%d" % i] = ["h%d" % (i + 1)] if i < n else ["l%d" % n]
        succ["l%d" % i] = ["h%d" % i] + (["l%d" % (i - 1)] if i > 1 else ["e"])
    succ["e"] = []
    return succ


# ------------------------------------------------------------------ tests


def test_page_example():
    succ, root = program_graph(toyir.parse(ODD_SUM))
    want = {"B1": set(), "B2": {"B2"}, "B3": {"B2"}, "B4": {"B5"}, "B5": {"B2"}, "B6": set()}
    assert dominance_frontiers(succ, root) == want
    assert dominance_frontiers_walk(succ, root) == want
    df = dominance_frontiers(succ, root)
    assert iterated_dominance_frontier(df, {"B1", "B4"}) == {"B2", "B5"}
    assert iterated_dominance_frontier(df, {"B1", "B5"}) == {"B2"}


def test_idom_matches_brute_force():
    rng = random.Random(1)
    for _ in range(300):
        succ = random_graph(rng, rng.randint(1, 9))
        idom = immediate_dominators(succ, 0)
        dom = brute_dominators(succ, 0)
        assert set(idom) == set(dom)
        for v, d in idom.items():
            if v == 0:
                assert d is None
            else:
                # the immediate dominator is the strict dominator with the most dominators
                strict = dom[v] - {v}
                assert d == max(strict, key=lambda u: len(dom[u]))


def test_random_graphs():
    rng = random.Random(2)
    for _ in range(600):
        succ = random_graph(rng, rng.randint(1, 10))
        want = brute_frontiers(succ, 0)
        assert dominance_frontiers(succ, 0) == want
        assert dominance_frontiers_walk(succ, 0) == want


def test_random_programs():
    rng = random.Random(3)
    for k in range(300):
        prog = toyir.random_program(rng, 6, 8, acyclic=(k % 3 == 0))
        succ, root = program_graph(prog)
        want = brute_frontiers(succ, root)
        assert program_frontiers(prog) == want
        assert dominance_frontiers_walk(succ, root) == want


def test_iterated_frontier():
    rng = random.Random(4)
    for _ in range(400):
        n = rng.randint(1, 10)
        succ = random_graph(rng, n)
        df = dominance_frontiers(succ, 0)
        nodes = list(df)
        s = set(rng.sample(nodes, rng.randint(1, len(nodes))))
        got = iterated_dominance_frontier(df, s)
        assert got == brute_idf(df, s)
        # DF+ is closed: DF(S + DF+) is inside DF+
        closed = set()
        for x in s | got:
            closed |= df[x]
        assert closed <= got


def test_quadratic_family():
    for n in range(1, 12):
        succ = ladder(n)
        df = dominance_frontiers(succ, "h1")
        assert df == dominance_frontiers_walk(succ, "h1")
        assert len(df) == 2 * n + 1
        assert sum(len(x) for x in succ.values()) == 3 * n
        assert sum(len(x) for x in df.values()) == n * (n + 1)
        for i in range(1, n + 1):
            want = {"h%d" % j for j in range(1, i + 1)}
            assert df["h%d" % i] == want and df["l%d" % i] == want
        phis = sum(len(iterated_dominance_frontier(df, {"h1", "l%d" % i})) for i in range(1, n + 1))
        assert phis == n * (n + 1) // 2


def test_entry_with_predecessors():
    # The back edge 2 -> 0 enters the root, which has one predecessor.
    succ = {0: [1], 1: [2], 2: [0]}
    want = {0: {0}, 1: {0}, 2: {0}}
    assert brute_frontiers(succ, 0) == want
    assert dominance_frontiers(succ, 0) == want
    assert dominance_frontiers_walk(succ, 0) == want


def test_unreachable_nodes_are_ignored():
    succ = {0: [1], 1: [], 2: [1]}
    df = dominance_frontiers(succ, 0)
    assert df == {0: set(), 1: set()}
    assert dominance_frontiers_walk(succ, 0) == df
