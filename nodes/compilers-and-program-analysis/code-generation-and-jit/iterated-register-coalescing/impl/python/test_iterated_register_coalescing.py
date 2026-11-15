# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterated-register-coalescing/. The authors are listed in prov/ZBH45M.jsonl.

import itertools
import random

import toyir
from iterated_register_coalescing import (
    allocate,
    briggs_ok,
    george_ok,
    interference,
    irc_color,
    is_mem,
    merge,
    prepare,
)


def graph(n, edges):
    adj = {v: set() for v in range(n)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def k_colorable(adj, k):
    """Exhaustive search: True when some map to 0 .. k-1 has no equal edge."""
    nodes = sorted(adj, key=lambda v: -len(adj[v]))
    color = {}

    def go(i):
        if i == len(nodes):
            return True
        v = nodes[i]
        used = {color[w] for w in adj[v] if w in color}
        for c in range(k):
            if c not in used:
                color[v] = c
                if go(i + 1):
                    return True
                del color[v]
        return False

    return go(0)


def k_core(adj, k):
    left = set(adj)
    changed = True
    while changed:
        changed = False
        for v in sorted(left):
            if len(adj[v] & left) < k:
                left.discard(v)
                changed = True
    return left


def check_merges(adj, k):
    """Returns how many merges of a k-colorable graph lose k-colorability."""
    colorable = k_colorable(adj, k)
    greedy = not k_core(adj, k)
    broken = 0
    for a, b in itertools.combinations(sorted(adj), 2):
        if b in adj[a]:
            continue
        m = merge(adj, a, b)
        m_colorable = k_colorable(m, k) if colorable else False
        broken += colorable and not m_colorable
        if briggs_ok(adj, a, b, k) or george_ok(adj, a, b, k) or george_ok(adj, b, a, k):
            # A conservative merge keeps k-colorability and an empty k-core.
            assert m_colorable or not colorable
            assert not k_core(m, k) or not greedy
    return broken


def test_every_graph_up_to_5_nodes():
    broken = 0
    for n in range(2, 6):
        pairs = list(itertools.combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            adj = graph(n, [p for i, p in enumerate(pairs) if mask >> i & 1])
            for k in (1, 2, 3):
                broken += check_merges(adj, k)
    assert broken > 0


def test_random_graphs_up_to_10_nodes():
    rng = random.Random(1996)
    for _ in range(120):
        n = rng.randint(6, 10)
        p = rng.choice((0.2, 0.35, 0.5))
        adj = graph(n, [e for e in itertools.combinations(range(n), 2) if rng.random() < p])
        for k in (2, 3):
            check_merges(adj, k)


def test_aggressive_merge_breaks_a_path():
    # The path a - x - y - b is 2-colorable; merging a and b makes a triangle.
    p4 = graph(4, [(0, 1), (1, 2), (2, 3)])
    assert k_colorable(p4, 2)
    assert not k_colorable(merge(p4, 0, 3), 2)
    assert not briggs_ok(p4, 0, 3, 2)
    assert not george_ok(p4, 0, 3, 2) and not george_ok(p4, 3, 0, 2)
    _, spilled, coalesced = irc_color(p4, [(0, 3)], 2, test="aggressive")
    assert spilled and coalesced == [0]
    color, spilled, coalesced = irc_color(p4, [(0, 3)], 2, test="briggs")
    assert not spilled and coalesced == []


def check_irc(adj, moves, k, test):
    color, spilled, coalesced = irc_color(adj, moves, k, test=test)
    assert set(color) | spilled == set(adj) and not set(color) & spilled
    assert all(0 <= c < k for c in color.values())
    assert all(color[a] != color[b] for a in color for b in adj[a] if b in color)
    for i in coalesced:
        x, y = moves[i]
        assert x not in adj[y]
        assert (x in spilled) == (y in spilled)
        assert x in spilled or color[x] == color[y]
    if test != "aggressive" and not k_core(adj, k):
        # No spill where Chaitin's allocator colors the graph.
        assert not spilled
    return spilled


def test_irc_on_random_graphs():
    rng = random.Random(300)
    aggressive_loss = 0
    for _ in range(300):
        n = rng.randint(2, 10)
        p = rng.choice((0.2, 0.35, 0.5))
        adj = graph(n, [e for e in itertools.combinations(range(n), 2) if rng.random() < p])
        moves = [tuple(rng.sample(range(n), 2)) for _ in range(rng.randint(0, n))]
        for k in (2, 3, 4):
            for test in ("briggs", "george", "either"):
                check_irc(adj, moves, k, test)
            if check_irc(adj, moves, k, "aggressive") and not k_core(adj, k):
                aggressive_loss += 1
    assert aggressive_loss > 0


PAGE = """
# params: p, q
L0:
  a = p + q
  b = a
  c = b * q
  d = c
  e = d + b
  ret e
"""


def test_page_example():
    prog = toyir.parse(PAGE)
    adj, moves = interference(prepare(prog))
    assert moves == [("d", "c"), ("b", "a")]
    out, rounds, spilled = allocate(prog, 2)
    assert rounds == 1 and spilled == []
    copies = [ins for b in out.blocks.values() for ins in b.instrs if ins[0] == "copy" and not is_mem(ins[2])]
    assert copies == []
    for p, q in itertools.product(range(-2, 3), repeat=2):
        assert toyir.run(out, [p, q]) == toyir.run(prog, [p, q])


PATH = """
# params: p
L0:
  y = p + 2
  x = p + 1
  br x L1 L2
L1:
  a = x + 1
  a = a + x
  b = a
  jump L3
L2:
  b = y + 1
  b = b + y
  jump L3
L3:
  ret b
"""


def test_aggressive_coalescing_spills_a_program():
    prog = toyir.parse(PATH)
    adj, moves = interference(prepare(prog))
    assert {v: adj[v] for v in "abxy"} == {"a": {"x"}, "x": {"a", "y"}, "y": {"x", "b", "p"}, "b": {"y"}}
    assert moves == [("b", "a")]
    assert allocate(prog, 2, "briggs")[1:] == (1, [])
    assert allocate(prog, 2, "george")[1:] == (1, [])
    assert allocate(prog, 2, "aggressive")[1:] == (2, ["y"])


def registers(prog):
    names = set()
    for b in prog.blocks.values():
        for ins in b.instrs:
            names.add(ins[1])
            names.update(toyir.uses(ins))
        names.update(toyir.term_uses(b.term))
    return {a for a in names if not is_mem(a)}


def test_random_programs_keep_their_outcome():
    rng = random.Random(18)
    for trial in range(120):
        prog = toyir.random_program(rng, rng.randint(2, 7), rng.randint(1, 6), trial % 2 == 0)
        for k in (2, 3, 4):
            for test in ("briggs", "either", "aggressive"):
                out, rounds, spilled = allocate(prog, k, test)
                assert registers(out) <= {"r%d" % i for i in range(k)}
                for _ in range(3):
                    args = [rng.randint(-4, 6), rng.randint(-4, 6)]
                    assert toyir.run(out, args, fuel=100000) == toyir.run(prog, args, fuel=100000)
