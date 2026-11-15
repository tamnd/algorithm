# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chaitin-register-allocation/. The authors are listed in prov/D7BWHP.jsonl.

import itertools
import random

import toyir
from chaitin_register_allocation import allocate, chaitin_color, interference, is_mem


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
    """Delete nodes of degree < k until none is left; what stays is the k-core."""
    left = set(adj)
    changed = True
    while changed:
        changed = False
        for v in sorted(left):
            if len(adj[v] & left) < k:
                left.discard(v)
                changed = True
    return left


def check(adj, k):
    color, spilled = chaitin_color(adj, k)
    if spilled:
        assert color == {}
    else:
        assert set(color) == set(adj)
        assert all(0 <= c < k for c in color.values())
        assert all(color[a] != color[b] for a in adj for b in adj[a])
    # Chaitin spills exactly when the k-core is not empty.
    assert bool(spilled) == bool(k_core(adj, k))
    # A graph that simplify colors is k-colorable; the converse fails.
    if not spilled:
        assert k_colorable(adj, k)
    return bool(spilled)


def test_every_graph_up_to_5_nodes():
    missed = 0
    for n in range(1, 6):
        pairs = list(itertools.combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            adj = graph(n, [p for i, p in enumerate(pairs) if mask >> i & 1])
            for k in (1, 2, 3):
                if check(adj, k) and k_colorable(adj, k):
                    missed += 1
    assert missed > 0


def test_random_graphs_up_to_10_nodes():
    rng = random.Random(1981)
    for _ in range(400):
        n = rng.randint(6, 10)
        p = rng.choice((0.2, 0.35, 0.5))
        adj = graph(n, [e for e in itertools.combinations(range(n), 2) if rng.random() < p])
        for k in (2, 3, 4):
            check(adj, k)


def test_cycle_of_four_spills_with_two_colors():
    c4 = graph(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    color, spilled = chaitin_color(c4, 2)
    assert spilled and k_colorable(c4, 2)
    color, spilled = chaitin_color(c4, 3)
    assert not spilled and len(set(color.values())) == 2


def test_spill_choice_uses_cost_per_degree():
    # K4 with k = 3: node 3 is the cheapest per edge.
    k4 = graph(4, list(itertools.combinations(range(4), 2)))
    _, spilled = chaitin_color(k4, 3, {0: 9, 1: 9, 2: 9, 3: 2})
    assert spilled == {3}


def test_copy_does_not_interfere():
    prog = toyir.parse("# params: a\nL:\n  b = a\n  c = a + b\n  ret c\n")
    adj, moves = interference(prog)
    assert "b" not in adj["a"]
    assert moves == [("b", "a")]


def test_dead_definition_interferes():
    prog = toyir.parse("# params: a\nL:\n  d = 5\n  ret a\n")
    adj, _ = interference(prog)
    assert adj["d"] == {"a"}


PAGE = """
# params: p
L0:
  a = p + 1
  b = p + 2
  c = a + b
  d = a * c
  e = b * d
  ret e
"""


def test_page_example():
    prog = toyir.parse(PAGE)
    adj, _ = interference(prog)
    assert adj == {
        "p": {"a"},
        "a": {"p", "b", "c"},
        "b": {"a", "c", "d"},
        "c": {"a", "b"},
        "d": {"b"},
        "e": set(),
    }
    out, rounds, spilled = allocate(prog, 3)
    assert rounds == 1 and spilled == []
    out, rounds, spilled = allocate(prog, 2)
    # Spilling c does not break the triangle: the reload of c still meets a and b.
    assert rounds == 4 and spilled == ["c", "a", "b"]
    for p in range(-3, 4):
        assert toyir.run(out, [p]) == toyir.run(prog, [p])


def registers(prog):
    names = set()
    for b in prog.blocks.values():
        for ins in b.instrs:
            names.add(ins[1])
            names.update(toyir.uses(ins))
        names.update(toyir.term_uses(b.term))
    return {a for a in names if not is_mem(a)}


def test_random_programs_keep_their_outcome():
    rng = random.Random(82)
    for trial in range(150):
        prog = toyir.random_program(rng, rng.randint(2, 7), rng.randint(1, 6), trial % 2 == 0)
        for k in (2, 3, 4, 5):
            out, rounds, spilled = allocate(prog, k)
            assert registers(out) <= {"r%d" % i for i in range(k)}
            for _ in range(4):
                args = [rng.randint(-4, 6), rng.randint(-4, 6)]
                assert toyir.run(out, args, fuel=100000) == toyir.run(prog, args, fuel=100000)
