# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cooper-harvey-kennedy-dominance/. The authors are listed in prov/0T0R8F.jsonl.

import random

import pytest

import toyir
from cooper_harvey_kennedy_dominance import _postorder, cfg_idom, chk, chk_idom

# The irreducible example of the page: r, a, b, c, d, e are 0 .. 5.
PAGE = [(0, 1), (0, 2), (1, 3), (2, 4), (2, 5), (3, 4), (4, 3), (4, 5), (5, 4)]

# The example of the Lengauer-Tarjan page.
LT = [(0, 1), (1, 2), (2, 3), (2, 4), (3, 4), (3, 7), (4, 5), (5, 6), (6, 3), (7, 8), (8, 6)]

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


def brute_dom(n, edges, root):
    """dom[v] = the set of dominators of v, by the definition: d dominates v
    if v is reachable and deleting d makes v unreachable (or d = v)."""
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
    return dom


def brute_idom(n, edges, root):
    dom = brute_dom(n, edges, root)
    out = [-1] * n
    for v, ds in dom.items():
        if v != root:
            strict = ds - {v}
            out[v] = max(strict, key=lambda x: len(dom[x]))
    return out


def max_retreating(n, edges, root):
    """The largest number of retreating edges on a simple path from root, for
    the DFS order that chk uses. An edge (u, v) is retreating if v does not
    come after u in reverse postorder."""
    succ = [[] for _ in range(n)]
    for a, b in edges:
        succ[a].append(b)
    post = _postorder(n, succ, root)
    po = [-1] * n
    for i, v in enumerate(post):
        po[v] = i
    best = 0
    on_path = [False] * n
    stack = [(root, 0, 0)]
    on_path[root] = True
    while stack:
        v, i, k = stack[-1]
        best = max(best, k)
        if i < len(succ[v]):
            stack[-1] = (v, i + 1, k)
            w = succ[v][i]
            if not on_path[w]:
                on_path[w] = True
                stack.append((w, 0, k + (1 if po[w] >= po[v] else 0)))
        else:
            on_path[v] = False
            stack.pop()
    return best


def is_reducible(n, edges, root):
    """Reachable part only: the graph without its back edges (t, h), where h
    dominates t, has no cycle."""
    dom = brute_dom(n, edges, root)
    keep = [(a, b) for a, b in edges if a in dom and b not in dom[a]]
    indeg = [0] * n
    for _, b in keep:
        indeg[b] += 1
    ready = [v for v in dom if indeg[v] == 0]
    done = 0
    while ready:
        v = ready.pop()
        done += 1
        for a, b in keep:
            if a == v:
                indeg[b] -= 1
                if indeg[b] == 0:
                    ready.append(b)
    return done == len(dom)


def test_page_example() -> None:
    idom, passes = chk(6, PAGE, 0)
    assert idom == [-1, 0, 0, 0, 0, 0]
    assert passes == 3
    assert max_retreating(6, PAGE, 0) == 2
    assert not is_reducible(6, PAGE, 0)


def test_lengauer_tarjan_example() -> None:
    assert chk_idom(9, LT, 0) == [-1, 0, 1, 2, 2, 4, 2, 3, 7]
    assert chk_idom(9, LT, 0) == brute_idom(9, LT, 0)


def test_odd_sum_program() -> None:
    prog = toyir.parse(ODD_SUM)
    assert cfg_idom(prog) == {"B1": None, "B2": "B1", "B3": "B2", "B4": "B3", "B5": "B3", "B6": "B2"}
    assert toyir.run(prog, [6]) == ("ret", 9)


def test_single_vertex() -> None:
    assert chk(1, [], 0) == ([-1], 1)
    assert chk_idom(1, [(0, 0)], 0) == [-1]


def test_star_and_diamond() -> None:
    n = 8
    edges = [(0, v) for v in range(1, n)] + [(3, 4), (4, 5), (7, 1)]
    assert chk_idom(n, edges, 0) == [-1] + [0] * (n - 1)
    assert chk_idom(4, [(0, 1), (0, 2), (1, 3), (2, 3)], 0) == [-1, 0, 0, 0]


def test_unreachable_and_other_root() -> None:
    edges = [(0, 1), (1, 2), (3, 2), (2, 0)]
    assert chk_idom(4, edges, 0) == [-1, 0, 1, -1]
    assert chk_idom(4, edges, 3) == [2, 0, 3, -1]


def test_self_loops_and_parallel_edges() -> None:
    edges = [(0, 1), (0, 1), (1, 1), (1, 2), (2, 2), (2, 1)]
    assert chk_idom(3, edges, 0) == [-1, 0, 1]


def test_long_paths() -> None:
    n = 20_000
    path = [(i, i + 1) for i in range(n - 1)]
    assert chk(n, path, 0) == ([-1] + list(range(n - 1)), 2)
    idom = chk_idom(n, path + [(i, 0) for i in range(n)], 0)
    assert idom == [-1] + list(range(n - 1))
    idom = chk_idom(n, path + [(i, i + 2) for i in range(n - 2)], 0)
    assert idom == [-1] + [0] * (n - 1)
    # The far end has an edge back to every vertex. The answer is the path,
    # but each intersect in pass 2 climbs a long chain.
    k = 1500
    path = [(i, i + 1) for i in range(k - 1)]
    idom = chk_idom(k, path + [(k - 1, i) for i in range(1, k - 1)], 0)
    assert idom == [-1] + list(range(k - 1))


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        chk(0, [], 0)
    with pytest.raises(ValueError):
        chk(2, [(0, 3)], 0)
    with pytest.raises(ValueError):
        chk(2, [], 2)


def test_random_against_definition() -> None:
    rng = random.Random(41)
    for _ in range(1500):
        n = rng.randint(1, 10)
        m = rng.randint(0, 3 * n)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        root = rng.randrange(n)
        assert chk_idom(n, edges, root) == brute_idom(n, edges, root)


def test_pass_bounds() -> None:
    # Proved on the page: at most d + 2 passes, where d is the largest number
    # of retreating edges on a simple path from the root, and at most 2
    # passes on a reducible graph.
    rng = random.Random(43)
    seen_reducible = seen_irreducible = 0
    for _ in range(1500):
        n = rng.randint(1, 8)
        m = rng.randint(0, 3 * n)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        _, passes = chk(n, edges, 0)
        assert 1 <= passes <= max_retreating(n, edges, 0) + 2
        if is_reducible(n, edges, 0):
            seen_reducible += 1
            assert passes <= 2
        else:
            seen_irreducible += 1
    assert seen_reducible > 100 and seen_irreducible > 100


def test_toy_ir_cfgs() -> None:
    rng = random.Random(47)
    for trial in range(300):
        prog = toyir.random_program(rng, 4, 8, acyclic=trial % 3 == 0)
        labels = list(prog.blocks)
        index = {lab: i for i, lab in enumerate(labels)}
        edges = [(index[a], index[b]) for a, b in toyir.edges(prog)]
        want = brute_idom(len(labels), edges, 0)
        got = cfg_idom(prog)
        assert got == {lab: (labels[want[i]] if want[i] != -1 else None) for i, lab in enumerate(labels)}
        # Every block is reachable, so only the entry has no idom.
        assert [lab for lab in labels if got[lab] is None] == [labels[0]]
