# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/program-dependence-graph/. The authors are listed in prov/AK2XM4.jsonl.

import random

import toyir
from program_dependence_graph import (
    ENTRY,
    EXIT,
    PDG,
    START,
    augmented_cfg,
    block_control_dependences,
    control_dependences,
    data_dependences,
)

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


# ------------------------------------------------------------ brute force


def reaches(succ, a, b, banned):
    """Does a reach b without passing through banned?"""
    if a == banned:
        return False
    seen, stack = {a}, [a]
    while stack:
        v = stack.pop()
        if v == b:
            return True
        for w in succ[v]:
            if w != banned and w not in seen:
                seen.add(w)
                stack.append(w)
    return False


def pdom(succ, exit_node, y, z):
    """y post-dominates z: every path from z to the exit contains y."""
    return y == z or not reaches(succ, z, exit_node, y)


def cd_by_paths(nodes, succ, exit_node):
    """Control dependence by the path definition of Ferrante, Ottenstein and
    Warren: y is control dependent on x through the edge x -> s if a path
    x, s, ..., y exists on which y post-dominates every node after x, and y
    does not strictly post-dominate x. The paths are enumerated."""
    pd = {(y, z): pdom(succ, exit_node, y, z) for y in nodes for z in nodes}
    out = set()
    for x in nodes:
        for s in succ[x]:
            for y in nodes:
                if y != x and pd[(y, x)]:
                    continue  # y strictly post-dominates x

                def walk(z, seen):
                    if not pd[(y, z)]:
                        return False
                    if z == y:
                        return True
                    for w in succ[z]:
                        if w not in seen and walk(w, seen | {w}):
                            return True
                    return False

                if walk(s, {s}):
                    out.add((x, y, s))
    return out


def dd_by_paths(prog):
    """Flow dependences by search over instruction positions: the definition
    of v at d reaches the use u if some path from just after d to u has no
    other definition of v."""
    pos = {}
    for label, b in prog.blocks.items():
        pos[label] = list(b.instrs) + [b.term]

    def after(node):
        label, i = node
        if i < len(pos[label]) - 1:
            return [(label, i + 1)]
        return [(s, 0) for s in toyir.succs(prog, label)]

    def reads(node):
        label, i = node
        ins = pos[label][i]
        return toyir.term_uses(ins) if i == len(pos[label]) - 1 else toyir.uses(ins)

    def writes(node):
        label, i = node
        if i == len(pos[label]) - 1:
            return None
        return toyir.defs(pos[label][i])

    defs = [(ENTRY, p, [(prog.entry, 0)]) for p in prog.params]
    for label in prog.blocks:
        for i in range(len(pos[label]) - 1):
            v = writes((label, i))
            if v is not None:
                defs.append(((label, i), v, after((label, i))))
    out = set()
    for d, v, starts in defs:
        seen, stack = set(starts), list(starts)
        while stack:
            n = stack.pop()
            if v in reads(n):
                out.add((d, n, v))
            if writes(n) == v:
                continue
            for w in after(n):
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
    return out


def random_cfg(rng, n):
    """A random digraph on 0 .. n-1 with entry 0, exit n-1 and a START node
    as in the PDG, kept only if every node is reachable and reaches the exit."""
    while True:
        succ = {v: [] for v in range(n)}
        for v in range(n - 1):
            k = rng.randint(1, 2)
            succ[v] = sorted(set(rng.randrange(n) for _ in range(k)))
        nodes = list(range(n)) + [START]
        succ[START] = [0, n - 1]
        ok = all(reaches(succ, START, v, None) and reaches(succ, v, n - 1, None) for v in range(n))
        if ok:
            return nodes, succ


# ------------------------------------------------------------ the page example


def test_page_example_control():
    prog = toyir.parse(ODD_SUM)
    cd = {(x, y) for x, y, s in block_control_dependences(prog)}
    assert cd == {
        (START, "B1"), (START, "B2"), (START, "B6"),
        ("B2", "B2"), ("B2", "B3"), ("B2", "B5"),
        ("B3", "B4"),
    }
    labelled = {(x, y, s) for x, y, s in block_control_dependences(prog) if x == "B3"}
    assert labelled == {("B3", "B4", "B4")}


def test_page_example_data():
    prog = toyir.parse(ODD_SUM)
    dd = data_dependences(prog)
    names = {}
    for label, b in prog.blocks.items():
        for i, ins in enumerate(b.instrs):
            names[(label, i)] = toyir._show_instr(ins)
        names[(label, len(b.instrs))] = toyir._show_term(b.term)
    names[ENTRY] = "ENTRY"
    got = {(names[d], names[u], v) for d, u, v in dd}
    assert got == {
        ("i = 0", "t1 = i < n", "i"),
        ("i = 0", "t2 = i % 2", "i"),
        ("i = 0", "s = s + i", "i"),
        ("i = 0", "i = i + 1", "i"),
        ("i = i + 1", "t1 = i < n", "i"),
        ("i = i + 1", "t2 = i % 2", "i"),
        ("i = i + 1", "s = s + i", "i"),
        ("i = i + 1", "i = i + 1", "i"),
        ("ENTRY", "t1 = i < n", "n"),
        ("t1 = i < n", "br t1 B3 B6", "t1"),
        ("t2 = i % 2", "br t2 B4 B5", "t2"),
        ("s = 0", "s = s + i", "s"),
        ("s = 0", "ret s", "s"),
        ("s = s + i", "s = s + i", "s"),
        ("s = s + i", "ret s", "s"),
    }


def test_pdg_nodes_and_edges():
    prog = toyir.parse(ODD_SUM)
    g = PDG(prog)
    assert len(g.nodes) == 1 + 3 + 2 + 2 + 2 + 2 + 1
    # s = s + i is the first instruction of B4, which depends on the branch of B3.
    assert g.control_parents(("B4", 0)) == {(("B3", 1), "B4")}
    assert g.control_parents(("B6", 0)) == {(ENTRY, "B1")}
    assert g.control_parents(("B2", 1)) == {(ENTRY, "B1"), (("B2", 1), "B3")}
    assert g.data_parents(("B4", 0)) == {(("B1", 1), "s"), (("B4", 0), "s"), (("B1", 0), "i"), (("B5", 0), "i")}


def test_slices():
    prog = toyir.parse(ODD_SUM)
    g = PDG(prog)
    everything = set(g.nodes)
    jumps = {("B1", 2), ("B4", 1), ("B5", 1)}
    assert g.slice(("B6", 0)) == everything - jumps
    assert g.slice(("B5", 0)) == {ENTRY, ("B1", 0), ("B5", 0), ("B2", 0), ("B2", 1)}


def test_diamond():
    prog = toyir.parse("B0:\n  br a B1 B2\nB1:\n  x = 1\n  jump B3\nB2:\n  x = 2\n  jump B3\nB3:\n  ret x\n")
    cd = block_control_dependences(prog)
    assert cd == {(START, "B0", "B0"), (START, "B3", "B0"), ("B0", "B1", "B1"), ("B0", "B2", "B2")}


# ------------------------------------------------------------ against brute force


def test_control_dependence_random_cfgs():
    rng = random.Random(20261115)
    for _ in range(400):
        n = rng.randint(2, 7)
        nodes, succ = random_cfg(rng, n)
        assert control_dependences(nodes, succ, n - 1) == cd_by_paths(nodes, succ, n - 1)


def test_control_dependence_random_programs():
    rng = random.Random(7)
    for k in range(300):
        prog = toyir.random_program(rng, rng.randint(2, 4), rng.randint(1, 8), acyclic=(k % 2 == 0))
        nodes, succ = augmented_cfg(prog)
        expected = cd_by_paths(nodes, succ, EXIT)
        assert block_control_dependences(prog) == expected
        assert PDG(prog).block_cd == expected


def test_data_dependence_random_programs():
    rng = random.Random(11)
    for k in range(300):
        prog = toyir.random_program(rng, rng.randint(2, 5), rng.randint(1, 8), acyclic=(k % 3 == 0))
        assert data_dependences(prog) == dd_by_paths(prog)
