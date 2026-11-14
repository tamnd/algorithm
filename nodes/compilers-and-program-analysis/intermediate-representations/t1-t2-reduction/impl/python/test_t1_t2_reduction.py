# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t1-t2-reduction/. The authors are listed in prov/VPKTQX.jsonl.

import random

import pytest

import toyir
from t1_t2_reduction import cfg_is_reducible, is_reducible, t1_t2_reduce

NESTED = """
B0:
  i = 0
  s = 0
  jump B1
B1:
  t = i < n
  br t B2 B6
B2:
  j = 0
  jump B3
B3:
  u = j < i
  br u B4 B5
B4:
  s = s + j
  j = j + 1
  jump B3
B5:
  i = i + 1
  jump B1
B6:
  ret s
"""

STUCK = """
r:
  br p A B
A:
  x = x + 1
  br q B C
B:
  x = x * 2
  br q A C
C:
  ret x
"""

ODD_SUM = """
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


def graph(prog):
    labels = list(prog.blocks)
    index = {lab: i for i, lab in enumerate(labels)}
    return labels, [(index[a], index[b]) for a, b in toyir.edges(prog)]


def reach(n, succ, root, banned):
    """The vertices that root reaches without passing through banned."""
    if banned == root:
        return set()
    seen = {root}
    stack = [root]
    while stack:
        v = stack.pop()
        for w in succ[v]:
            if w != banned and w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def brute_reducible(n, edges, root):
    """Reducibility by the definition: compute the dominators by deleting
    each vertex in turn, drop the back edges (t, h) with h dominating t, and
    check that what is left has no cycle."""
    succ = [[] for _ in range(n)]
    for a, b in edges:
        succ[a].append(b)
    full = reach(n, succ, root, -1)
    dom = {v: {v} for v in full}
    for d in full:
        r = reach(n, succ, root, d)
        for v in full:
            if v not in r:
                dom[v].add(d)
    fwd = {v: set() for v in full}
    for a, b in edges:
        if a in full and b not in dom[a]:
            fwd[a].add(b)
    indeg = {v: 0 for v in full}
    for a in fwd:
        for b in fwd[a]:
            indeg[b] += 1
    queue = [v for v in full if indeg[v] == 0]
    count = 0
    while queue:
        v = queue.pop()
        count += 1
        for w in fwd[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                queue.append(w)
    return count == len(full)


def naive_reduce(n, edges, root, rng):
    """Apply T1 and T2 in a random order until neither applies. Returns the
    number of vertices left."""
    succ = [[] for _ in range(n)]
    for a, b in edges:
        succ[a].append(b)
    full = reach(n, succ, root, -1)
    s = {v: set() for v in full}
    for a, b in edges:
        if a in full:
            s[a].add(b)
    while True:
        moves = []
        for v in s:
            if v in s[v]:
                moves.append(("T1", v))
            preds = [u for u in s if v in s[u]]
            if v != root and len(preds) == 1 and preds[0] != v:
                moves.append(("T2", v, preds[0]))
        if not moves:
            return len(s)
        move = rng.choice(moves)
        if move[0] == "T1":
            s[move[1]].discard(move[1])
        else:
            v, u = move[1], move[2]
            s[u].discard(v)
            s[u] |= s[v]
            del s[v]


def random_graph(rng):
    n = rng.randint(1, 8)
    m = rng.randint(n, 3 * n)
    return n, [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]


def test_nested_loops_reduce_to_one_node():
    labels, edges = graph(toyir.parse(NESTED))
    left, left_edges, steps = t1_t2_reduce(len(labels), edges, 0)
    assert left == [0] and left_edges == []
    named = [(s[0],) + tuple(labels[x] for x in s[1:]) for s in steps]
    assert named == [
        ("T2", "B2", "B1"),
        ("T2", "B4", "B3"),
        ("T1", "B3"),
        ("T2", "B3", "B1"),
        ("T2", "B5", "B1"),
        ("T1", "B1"),
        ("T2", "B1", "B0"),
        ("T2", "B6", "B0"),
    ]


def test_smallest_irreducible_graph_is_stuck():
    prog = toyir.parse(STUCK)
    labels, edges = graph(prog)
    left, left_edges, steps = t1_t2_reduce(len(labels), edges, 0)
    assert steps == []
    assert left == [0, 1, 2, 3]
    assert left_edges == [(0, 1), (0, 2), (1, 2), (1, 3), (2, 1), (2, 3)]
    assert not cfg_is_reducible(prog)
    assert not brute_reducible(len(labels), edges, 0)


def test_odd_sum_program():
    prog = toyir.parse(ODD_SUM)
    assert cfg_is_reducible(prog)
    assert toyir.run(prog, [6]) == ("ret", 9)


def test_small_cases():
    assert t1_t2_reduce(1, [], 0) == ([0], [], [])
    assert t1_t2_reduce(1, [(0, 0)], 0) == ([0], [], [("T1", 0)])
    # Parallel edges count as one edge.
    assert t1_t2_reduce(2, [(0, 1), (0, 1)], 0) == ([0], [], [("T2", 1, 0)])
    # A cycle through the root is reducible.
    assert is_reducible(3, [(0, 1), (1, 2), (2, 0)], 0)
    # The root keeps its in-edges until a T1 removes them.
    assert t1_t2_reduce(2, [(0, 1), (1, 0)], 0) == ([0], [], [("T2", 1, 0), ("T1", 0)])


def test_unreachable_part_is_ignored():
    # 3, 4 and 5 form an irreducible pattern that the root 0 does not reach.
    edges = [(0, 1), (1, 2), (3, 4), (3, 5), (4, 5), (5, 4), (4, 1)]
    left, left_edges, _ = t1_t2_reduce(6, edges, 0)
    assert left == [0] and left_edges == []
    # With root 3 the same graph is irreducible.
    assert not is_reducible(6, edges, 3)


def test_bad_input():
    with pytest.raises(ValueError):
        t1_t2_reduce(0, [], 0)
    with pytest.raises(ValueError):
        t1_t2_reduce(2, [], 2)
    with pytest.raises(ValueError):
        t1_t2_reduce(2, [(0, 2)], 0)


def test_random_graphs_match_the_definition():
    rng = random.Random(53)
    seen = [0, 0]
    for _ in range(1500):
        n, edges = random_graph(rng)
        root = rng.randrange(n)
        want = brute_reducible(n, edges, root)
        assert is_reducible(n, edges, root) == want
        seen[want] += 1
    assert min(seen) > 100


def test_every_order_gives_the_same_answer():
    rng = random.Random(59)
    for _ in range(400):
        n, edges = random_graph(rng)
        want = is_reducible(n, edges, 0)
        for _ in range(4):
            assert (naive_reduce(n, edges, 0, rng) == 1) == want


def test_limit_graph_is_stuck_and_counts_match():
    rng = random.Random(61)
    for _ in range(800):
        n, edges = random_graph(rng)
        left, left_edges, steps = t1_t2_reduce(n, edges, 0)
        succ = [[] for _ in range(n)]
        for a, b in edges:
            succ[a].append(b)
        size = len(reach(n, succ, 0, -1))
        assert sum(1 for s in steps if s[0] == "T2") == size - len(left)
        assert 0 in left
        assert all(a != b for a, b in left_edges)
        for v in left:
            if v != 0:
                assert sum(1 for a, b in left_edges if b == v) >= 2


def test_random_toy_programs():
    rng = random.Random(67)
    seen = [0, 0]
    for _ in range(300):
        prog = toyir.random_program(rng, 3, rng.randint(2, 9), rng.random() < 0.3)
        labels, edges = graph(prog)
        want = brute_reducible(len(labels), edges, 0)
        assert cfg_is_reducible(prog) == want
        seen[want] += 1
    assert seen[1] > 100


def test_long_graphs():
    n = 20000
    chain = [(i, i + 1) for i in range(n - 1)]
    assert is_reducible(n, chain + [(i + 1, i) for i in range(n - 1)], 0)
    assert is_reducible(n, chain + [(n - 1, 0)], 0)
    # Two entries into one long cycle: irreducible.
    assert not is_reducible(n, chain + [(n - 1, 1), (0, n // 2)], 0)
