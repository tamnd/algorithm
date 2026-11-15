# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/briggs-optimistic-coloring/. The authors are listed in prov/Y67E03.jsonl.

import itertools
import random

import toyir
from briggs_optimistic_coloring import allocate, briggs_color, interference, is_mem, prepare, simplify


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


def chaitin_spills(adj, k, cost):
    """Chaitin's allocator spills every spill choice of the same simplify."""
    return {v for v, chosen in simplify(adj, k, cost) if chosen}


def check(adj, k, cost=None):
    """Returns (Briggs colors all, Chaitin colors all)."""
    cost = cost or {v: 1 for v in adj}
    color, spilled = briggs_color(adj, k, cost)
    assert set(color) | spilled == set(adj) and not set(color) & spilled
    assert all(0 <= c < k for c in color.values())
    assert all(color[a] != color[b] for a in color for b in adj[a] if b in color)
    chaitin = chaitin_spills(adj, k, cost)
    # Optimistic coloring spills only nodes that Chaitin spills.
    assert spilled <= chaitin
    # Chaitin colors the graph exactly when its k-core is empty.
    assert bool(chaitin) == bool(k_core(adj, k))
    if not spilled:
        assert k_colorable(adj, k)
    return not spilled, not chaitin


def test_every_graph_up_to_5_nodes():
    gains = 0
    for n in range(1, 6):
        pairs = list(itertools.combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            adj = graph(n, [p for i, p in enumerate(pairs) if mask >> i & 1])
            for k in (1, 2, 3):
                briggs, chaitin = check(adj, k)
                assert briggs or not chaitin
                gains += briggs and not chaitin
    assert gains > 0


def test_random_graphs_up_to_10_nodes():
    rng = random.Random(1989)
    gains = 0
    for _ in range(400):
        n = rng.randint(6, 10)
        p = rng.choice((0.2, 0.35, 0.5))
        adj = graph(n, [e for e in itertools.combinations(range(n), 2) if rng.random() < p])
        cost = {v: rng.randint(1, 9) for v in adj}
        for k in (2, 3, 4):
            briggs, chaitin = check(adj, k, cost)
            gains += briggs and not chaitin
    assert gains > 0


def test_cycle_of_four():
    c4 = graph(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    assert chaitin_spills(c4, 2, {v: 1 for v in c4})
    color, spilled = briggs_color(c4, 2)
    assert not spilled and sorted(color.values()) == [0, 0, 1, 1]


def test_prism_is_3_colorable_but_briggs_spills():
    # Two triangles 0 3 4 and 1 2 5 joined by a perfect matching.
    prism = graph(6, [(0, 3), (0, 4), (0, 5), (1, 2), (1, 4), (1, 5), (2, 3), (2, 5), (3, 4)])
    assert k_colorable(prism, 3)
    color, spilled = briggs_color(prism, 3)
    assert spilled == {0}


LOOP = """
# params: n
L0:
  d = n
  jump L1
L1:
  a = d + 1
  b = a + d
  c = a + 1
  d = b - c
  d = d % c
  br d L1 L2
L2:
  ret d
"""


def test_page_example():
    prog = toyir.parse(LOOP)
    adj = interference(prepare(prog))
    assert {v: adj[v] for v in "abcd"} == {"a": {"b", "d"}, "b": {"a", "c"}, "c": {"b", "d"}, "d": {"a", "c"}}
    assert chaitin_spills(adj, 2, {v: 1 for v in adj})
    out, rounds, spilled = allocate(prog, 2)
    assert rounds == 1 and spilled == []
    for n in range(-4, 8):
        assert toyir.run(out, [n]) == toyir.run(prog, [n])


def registers(prog):
    names = set()
    for b in prog.blocks.values():
        for ins in b.instrs:
            names.add(ins[1])
            names.update(toyir.uses(ins))
        names.update(toyir.term_uses(b.term))
    return {a for a in names if not is_mem(a)}


def test_random_programs_keep_their_outcome():
    rng = random.Random(94)
    for trial in range(150):
        prog = toyir.random_program(rng, rng.randint(2, 7), rng.randint(1, 6), trial % 2 == 0)
        for k in (2, 3, 4, 5):
            out, rounds, spilled = allocate(prog, k)
            assert registers(out) <= {"r%d" % i for i in range(k)}
            for _ in range(4):
                args = [rng.randint(-4, 6), rng.randint(-4, 6)]
                assert toyir.run(out, args, fuel=100000) == toyir.run(prog, args, fuel=100000)
