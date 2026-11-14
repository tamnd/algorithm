# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sea-of-nodes/. The authors are listed in prov/Q4NRFR.jsonl.

import random

import toyir
from sea_of_nodes import build, roundtrip, schedule

LOOP = """# params: n
B1:
  i = 0
  s = 0
  jump B2
B2:
  t1 = i < n
  br t1 B3 B4
B3:
  k = n * 4
  s = s + k
  i = i + 1
  jump B2
B4:
  ret s
"""

DIAMOND = """# params: a, b, c
B1:
  br c B2 B3
B2:
  x = a + b
  jump B4
B3:
  y = a + b
  x = y * 2
  jump B4
B4:
  ret x
"""


def ops_by_block(prog):
    return {label: [i for i in b.instrs if i[0] == "op"] for label, b in prog.blocks.items()}


# ------------------------------------------------------------ brute force


def reaches(prog, a, b, banned):
    if a == banned:
        return False
    seen, stack = {a}, [a]
    while stack:
        v = stack.pop()
        if v == b:
            return True
        for w in toyir.succs(prog, v):
            if w != banned and w not in seen:
                seen.add(w)
                stack.append(w)
    return False


def dominates(prog, a, b):
    """a dominates b: b cannot be reached from the entry without a."""
    return a == b or not reaches(prog, prog.entry, b, a)


def check_strict_ssa(prog):
    """Each name is defined once, and each definition dominates its uses; a
    phi operand counts as a use at the end of its predecessor."""
    where = {p: (prog.entry, -1) for p in prog.params}
    for label, b in prog.blocks.items():
        for i, ins in enumerate(b.instrs):
            x = toyir.defs(ins)
            assert x not in where, "two definitions of %s" % x
            where[x] = (label, i)

    def ok(name, label, i):
        dl, di = where[name]
        if dl == label:
            return di < i
        return dominates(prog, dl, label)

    for label, b in prog.blocks.items():
        for i, ins in enumerate(b.instrs):
            if ins[0] == "phi":
                for p, a in ins[2].items():
                    if isinstance(a, str):
                        assert ok(a, p, len(prog.blocks[p].instrs) + 1)
            else:
                for a in toyir.uses(ins):
                    assert ok(a, label, i)
        for a in toyir.term_uses(b.term):
            assert ok(a, label, len(b.instrs))


# ------------------------------------------------------------ page examples


def test_loop_invariant_value_leaves_the_loop():
    out = roundtrip(toyir.parse(LOOP))
    ops = ops_by_block(out)
    assert [i[2:] for i in ops["B1"]] == [("*", "n", 4)]
    assert sorted(i[2] for i in ops["B3"]) == ["+", "+"]
    for n in range(-2, 8):
        assert toyir.run(out, [n]) == toyir.run(toyir.parse(LOOP), [n])
    assert toyir.run(out, [4]) == ("ret", 64)


def test_equal_values_are_made_once_and_hoisted():
    out = roundtrip(toyir.parse(DIAMOND))
    ops = ops_by_block(out)
    assert [i[2:] for i in ops["B1"]] == [("+", "a", "b")]
    assert ops["B2"] == []
    assert [i[2] for i in ops["B3"]] == ["*"]
    phis = [i for i in out.blocks["B4"].instrs if i[0] == "phi"]
    assert len(phis) == 1


def test_a_division_stays_in_its_block():
    prog = toyir.parse("# params: a, b, c\nB1:\n  br c B2 B3\nB2:\n  q = a / b\n  jump B3\nB3:\n  ret a\n")
    out = roundtrip(prog)
    assert [i[2] for i in ops_by_block(out)["B2"]] == ["/"]
    assert ops_by_block(out)["B1"] == []
    assert toyir.run(out, [1, 0, 0]) == ("ret", 1)
    assert toyir.run(out, [1, 0, 1]) == ("trap",)


def test_graph_shape():
    g = build(toyir.parse(LOOP))
    kinds = [n.kind for n in g.nodes]
    # B2 gets a phi for each of i, k, n, s and t1. The phi of n is trivial
    # and removed; those of k and t1 have no use and are not scheduled.
    assert kinds.count("Phi") == 4
    out, _ = schedule(g, ["B1", "B2", "B3", "B4"])
    assert sum(1 for i in out.blocks["B2"].instrs if i[0] == "phi") == 2
    assert kinds.count("Region") == 4
    assert kinds.count("If") == 1 and kinds.count("Return") == 1
    # The floating multiply has no control input.
    mul = [n for n in g.nodes if n.kind == "Op" and n.val == "*"]
    assert len(mul) == 1 and [i.kind for i in mul[0].inputs] == ["Param", "Const"]


# ------------------------------------------------------------ random programs


def test_random_programs_keep_their_outcomes():
    rng = random.Random(20261115)
    compared = 0
    for k in range(400):
        prog = toyir.random_program(rng, rng.randint(2, 5), rng.randint(1, 8), acyclic=(k % 2 == 0))
        out = roundtrip(prog)
        for _ in range(6):
            args = [rng.randint(-4, 7) for _ in prog.params]
            want = toyir.run(prog, args)
            if want == ("fuel",):
                continue
            assert toyir.run(out, args, fuel=200000) == want
            compared += 1
    assert compared > 2000


def test_random_programs_give_strict_ssa():
    rng = random.Random(3)
    for k in range(300):
        prog = toyir.random_program(rng, rng.randint(2, 5), rng.randint(1, 8), acyclic=(k % 3 == 0))
        check_strict_ssa(roundtrip(prog))


def test_no_more_operations_than_the_source():
    rng = random.Random(5)
    for k in range(300):
        prog = toyir.random_program(rng, rng.randint(2, 5), rng.randint(1, 8), acyclic=(k % 2 == 0))
        out = roundtrip(prog)
        before = sum(1 for b in prog.blocks.values() for i in b.instrs if i[0] == "op")
        after = sum(1 for b in out.blocks.values() for i in b.instrs if i[0] == "op")
        assert after <= before


def test_trapping_operations_keep_their_block():
    rng = random.Random(9)
    for k in range(200):
        prog = toyir.random_program(rng, rng.randint(2, 5), rng.randint(1, 8), acyclic=(k % 2 == 0))
        g = build(prog)
        out, block = schedule(g, list(prog.blocks))
        for n in g.roots:
            if n.kind == "Op":
                region = n.inputs[0]
                assert block[n.id] == g.label_of[region.id]
