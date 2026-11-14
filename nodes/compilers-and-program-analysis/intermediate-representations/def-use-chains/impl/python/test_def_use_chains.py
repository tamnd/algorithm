# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/def-use-chains/. The authors are listed in prov/XZ8C52.jsonl.

import random

import pytest

import toyir
from def_use_chains import chains, reaching

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

PHI = """
B0:
  br c B1 B2
B1:
  x1 = 1
  jump B3
B2:
  x2 = 2
  jump B3
B3:
  x3 = phi [B1: x1, B2: x2]
  y = x3 + c
  ret y
"""


def brute_chains(prog):
    """The chains by the definition, one graph search per definition over
    the graph of program points. Point (lab, i) is instruction i of block
    lab, and (lab, len(instrs)) is its terminator. A phi operand from p is
    a use at the end of p."""
    du = {}
    starts = {}
    for x in prog.params:
        starts[(prog.entry, -1, x)] = (prog.entry, 0)
    for lab, block in prog.blocks.items():
        for i, ins in enumerate(block.instrs):
            x = toyir.defs(ins)
            if x is not None:
                starts[(lab, i, x)] = (lab, i + 1)
    for d, start in starts.items():
        x = d[2]
        found = set()
        seen = {start}
        stack = [start]
        while stack:
            lab, i = stack.pop()
            block = prog.blocks[lab]
            if i < len(block.instrs):
                ins = block.instrs[i]
                if ins[0] != "phi" and x in toyir.uses(ins):
                    found.add((lab, i, x))
                if toyir.defs(ins) == x:
                    continue
                nxt = [(lab, i + 1)]
            else:
                if x in toyir.term_uses(block.term):
                    found.add((lab, i, x))
                nxt = []
                for s in toyir.succs(prog, lab):
                    for k, ins in enumerate(prog.blocks[s].instrs):
                        if ins[0] == "phi" and ins[2].get(lab) == x:
                            found.add((s, k, x))
                    nxt.append((s, 0))
            for q in nxt:
                if q not in seen:
                    seen.add(q)
                    stack.append(q)
        du[d] = sorted(found)
    return du


def path_pairs(prog, path):
    """The (definition, use) pairs that one run along the block path shows:
    each use is linked to the last definition of its name before it."""
    last = {x: (prog.entry, -1, x) for x in prog.params}
    pairs = set()
    prev = None
    for lab in path:
        block = prog.blocks[lab]
        incoming = []
        for i, ins in enumerate(block.instrs):
            if ins[0] == "phi":
                a = ins[2].get(prev)
                if isinstance(a, str) and a in last:
                    pairs.add((last[a], (lab, i, a)))
                incoming.append((ins[1], (lab, i, ins[1])))
                continue
            for x, site in incoming:
                last[x] = site
            incoming = []
            for x in toyir.uses(ins):
                if x in last:
                    pairs.add((last[x], (lab, i, x)))
            x = toyir.defs(ins)
            if x is not None:
                last[x] = (lab, i, x)
        for x, site in incoming:
            last[x] = site
        for x in toyir.term_uses(block.term):
            if x in last:
                pairs.add((last[x], (lab, len(block.instrs), x)))
        prev = lab
    return pairs


def as_pairs(du):
    return {(d, u) for d, us in du.items() for u in us}


def all_uses(prog):
    out = set()
    for lab, block in prog.blocks.items():
        for i, ins in enumerate(block.instrs):
            names = ins[2].values() if ins[0] == "phi" else toyir.uses(ins)
            for x in names:
                if isinstance(x, str):
                    out.add((lab, i, x))
        for x in toyir.term_uses(block.term):
            out.add((lab, len(block.instrs), x))
    return out


def test_odd_sum_chains():
    prog = toyir.parse(ODD_SUM)
    du, ud = chains(prog)
    assert du[("B1", 0, "i")] == [("B2", 0, "i"), ("B3", 0, "i"), ("B4", 0, "i"), ("B5", 0, "i")]
    assert du[("B5", 0, "i")] == du[("B1", 0, "i")]
    assert du[("B1", 1, "s")] == [("B4", 0, "s"), ("B6", 0, "s")]
    assert du[("B4", 0, "s")] == [("B4", 0, "s"), ("B6", 0, "s")]
    assert du[("B1", -1, "n")] == [("B2", 0, "n")]
    assert ud[("B6", 0, "s")] == [("B1", 1, "s"), ("B4", 0, "s")]
    assert ud[("B2", 1, "t1")] == [("B2", 0, "t1")]
    assert sum(len(us) for us in du.values()) == 15
    assert reaching(prog)[2] == 3
    assert toyir.run(prog, [6]) == ("ret", 9)


def test_phi_operands_are_used_at_the_predecessor():
    prog = toyir.parse(PHI)
    du, ud = chains(prog)
    assert du[("B1", 0, "x1")] == [("B3", 0, "x1")]
    assert du[("B2", 0, "x2")] == [("B3", 0, "x2")]
    assert ud[("B3", 1, "x3")] == [("B3", 0, "x3")]
    assert du == brute_chains(prog)
    with pytest.raises(ValueError):
        chains(toyir.parse("A:\n  x = phi [Z: 1]\n  ret x\n"))


def test_du_and_ud_are_inverse():
    rng = random.Random(71)
    for _ in range(200):
        prog = toyir.random_program(rng, 4, rng.randint(1, 8), rng.random() < 0.5)
        du, ud = chains(prog)
        assert as_pairs(du) == {(d, u) for u, ds in ud.items() for d in ds}
        assert set(ud) == all_uses(prog)


def test_undefined_and_unreachable():
    prog = toyir.parse("""
# params: a
A:
  br a B C
B:
  y = 1
  jump C
C:
  z = y + a
  ret z
D:
  y = 7
  jump C
""")
    du, ud = chains(prog)
    # On the path A, C no definition of y comes first; the chain lists only B.
    # D is unreachable, but a path from its definition to the use exists.
    assert ud[("C", 0, "y")] == [("B", 0, "y"), ("D", 0, "y")]
    assert ud[("C", 0, "a")] == [("A", -1, "a")]
    assert du == brute_chains(prog)


def test_loop_back_to_the_entry():
    prog = toyir.parse("""
# params: n
E:
  t = n < 3
  n = n + 1
  br t E X
X:
  ret n
""")
    du, ud = chains(prog)
    assert ud[("E", 0, "n")] == [("E", -1, "n"), ("E", 1, "n")]
    assert ud[("X", 0, "n")] == [("E", 1, "n")]
    assert du == brute_chains(prog)


def test_random_programs_match_the_definition():
    rng = random.Random(73)
    for _ in range(300):
        prog = toyir.random_program(rng, 4, rng.randint(1, 8), rng.random() < 0.4)
        du, _ = chains(prog)
        assert du == brute_chains(prog)


def test_acyclic_programs_match_all_paths():
    rng = random.Random(79)
    for _ in range(300):
        prog = toyir.random_program(rng, 4, rng.randint(1, 8), True)
        du, _ = chains(prog)
        seen = set()
        for path in toyir.paths(prog):
            seen |= path_pairs(prog, path)
        assert as_pairs(du) == seen


def test_random_walks_stay_inside_the_chains():
    rng = random.Random(83)
    for _ in range(300):
        prog = toyir.random_program(rng, 4, rng.randint(2, 8), False)
        pairs = as_pairs(chains(prog)[0])
        for _ in range(5):
            path = [prog.entry]
            while toyir.succs(prog, path[-1]) and len(path) < 40:
                path.append(rng.choice(toyir.succs(prog, path[-1])))
            assert path_pairs(prog, path) <= pairs


def test_passes_bound_on_reducible_programs():
    # Reaching definitions in reverse postorder: random programs are
    # reducible, so their loop connectedness is small.
    rng = random.Random(89)
    worst = 0
    for _ in range(300):
        prog = toyir.random_program(rng, 4, rng.randint(1, 9), False)
        worst = max(worst, reaching(prog)[2])
    assert 2 <= worst <= 4


def join_program(k):
    lines = ["T1:"]
    for i in range(1, k + 1):
        lines.append("T%d:" % i if i > 1 else "")
        nxt = "T%d" % (i + 1) if i < k else "D%d" % i
        lines.append("  br c D%d %s" % (i, nxt))
    for i in range(1, k + 1):
        lines += ["D%d:" % i, "  x = %d" % i, "  jump J"]
    lines.append("J:")
    for j in range(k):
        lines.append("  y%d = x + %d" % (j, j))
    lines.append("  ret x")
    return toyir.parse("\n".join(line for line in lines if line))


def test_k_definitions_and_k_uses_give_k_squared_chains():
    for k in (2, 5, 20):
        prog = join_program(k)
        du, _ = chains(prog)
        links = sum(len(us) for d, us in du.items() if d[2] == "x")
        assert links == k * (k + 1)
        assert du == brute_chains(prog)


def test_bigger_program():
    rng = random.Random(97)
    prog = toyir.random_program(rng, 6, 60, False)
    du, _ = chains(prog)
    assert du == brute_chains(prog)
