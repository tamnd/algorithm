# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/concolic-testing/. The authors are listed in prov/C4AWCW.jsonl.

import collections
import itertools
import random

import toyir
from concolic_testing import brute_force_solver, concolic, concolic_run, holds

LO, HI = -8, 8

PAGE = """
# params: x, y
entry:
  z = y * 2
  t = z == x
  br t then miss
then:
  w = y + 3
  u = w < x
  br u bug near
miss:
  ret 0
bug:
  ret 1
near:
  ret 2
"""

DIVIDE = """
# params: x, y
entry:
  d = x - y
  t = d < 0
  br t lt ge
lt:
  u = x == y
  br u dead r1
ge:
  q = 12 / d
  v = q == 3
  br v r2 r3
dead:
  ret 9
r1:
  ret 1
r2:
  ret 2
r3:
  ret 3
"""

COUNT = """
# params: n
entry:
  i = 0
  jump head
head:
  t = i < n
  br t body exit
body:
  i = i + 1
  jump head
exit:
  ret i
"""


def trace(prog, args):
    """A plain concrete run that records the path, written apart from the
    concolic code: (labels, outcome kind, index of the trapping instruction)."""
    env = dict(zip(prog.params, args))
    label = prog.entry
    labels = [label]

    def val(a):
        return a if isinstance(a, int) else env[a]

    while True:
        block = prog.blocks[label]
        for idx, ins in enumerate(block.instrs):
            if ins[0] == "const":
                env[ins[1]] = ins[2]
            elif ins[0] == "copy":
                env[ins[1]] = val(ins[2])
            else:
                a, b = val(ins[3]), val(ins[4])
                if ins[2] in ("/", "%") and b == 0:
                    return (tuple(labels), "trap", idx)
                if ins[2] in ("<<", ">>") and not 0 <= b <= 63:
                    return (tuple(labels), "trap", idx)
                env[ins[1]] = toyir._binop(ins[2], a, b)
        t = block.term
        if t[0] == "ret":
            return (tuple(labels), "ret", None)
        label = t[1] if t[0] == "jump" else (t[2] if val(t[1]) != 0 else t[3])
        labels.append(label)


def box(k):
    return itertools.product(range(LO, HI + 1), repeat=k)


def brute_paths(prog):
    out = set()
    for v in box(len(prog.params)):
        p = trace(prog, v)
        assert p[1] == toyir.run(prog, v)[0]
        out.add(p)
    return out


def check_complete(prog):
    runs = concolic(prog)
    found = [r.path() for r in runs]
    assert len(found) == len(set(found)), "a path was explored twice"
    assert set(found) == brute_paths(prog)
    for r in runs:
        assert all(LO <= a <= HI for a in r.args)
        assert r.outcome == toyir.run(prog, r.args)
    return runs


def test_page_example():
    prog = toyir.parse(PAGE)
    runs = check_complete(prog)
    assert [r.args for r in runs] == [[0, 0], [8, 4], [-8, -8]]
    assert [r.outcome for r in runs] == [("ret", 2), ("ret", 1), ("ret", 0)]
    counts = collections.Counter(toyir.run(prog, v) for v in box(2))
    assert counts == {("ret", 0): 280, ("ret", 2): 8, ("ret", 1): 1}


def test_first_run_conditions():
    run = concolic_run(toyir.parse(PAGE), [0, 0])
    two_y = ("op", "*", ("in", 1), ("k", 2))
    assert run.conds == [
        (("op", "==", two_y, ("in", 0)), True),
        (("op", "<", ("op", "+", ("in", 1), ("k", 3)), ("in", 0)), False),
    ]


def test_implicit_trap_condition():
    prog = toyir.parse(DIVIDE)
    runs = check_complete(prog)
    assert sorted(r.outcome for r in runs) == [("ret", 1), ("ret", 2), ("ret", 3), ("trap",)]
    trap = [r for r in runs if r.outcome == ("trap",)][0]
    assert trap.conds[-1] == (("op", "-", ("in", 0), ("in", 1)), False)


def test_counted_loop_stops_at_the_box():
    runs = check_complete(toyir.parse(COUNT))
    assert [r.args for r in runs] == [[n] for n in range(0, 9)]


def test_random_loop_free_programs():
    rng = random.Random(20261115)
    for _ in range(80):
        prog = toyir.random_program(rng, rng.randint(2, 4), rng.randint(2, 7), acyclic=True)
        check_complete(prog)


def test_random_programs_with_loops():
    rng = random.Random(7)
    for _ in range(30):
        prog = toyir.random_program(rng, rng.randint(2, 4), rng.randint(3, 7), acyclic=False)
        check_complete(prog)


def ladder(rng, k):
    """k tests in a row on linear terms of x, y and the running sum s, with a
    division by s at the end. Up to 2^k paths, plus the traps."""
    lines = ["# params: x, y", "entry:", "  s = 0", "  jump T0"]
    for i in range(k):
        a, b, c = rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-6, 6)
        lines += ["T%d:" % i, "  e = x * %d" % a, "  f = y * %d" % b, "  g = e + f", "  g = g + s"]
        lines += ["  t = g < %d" % c, "  br t A%d C%d" % (i, i)]
        lines += ["A%d:" % i, "  s = s + x", "  jump T%d" % (i + 1)]
        lines += ["C%d:" % i, "  s = s - %d" % rng.randint(1, 3), "  jump T%d" % (i + 1)]
    lines += ["T%d:" % k, "  r = 12 / s", "  ret r"]
    return toyir.parse("\n".join(lines))


def test_random_ladders():
    rng = random.Random(5)
    sizes = []
    for _ in range(12):
        runs = check_complete(ladder(rng, rng.randint(2, 5)))
        sizes.append(len(runs))
    assert max(sizes) >= 10


def test_path_condition_is_exact():
    rng = random.Random(11)
    for _ in range(40):
        prog = toyir.random_program(rng, 3, rng.randint(2, 6), acyclic=rng.random() < 0.5)
        runs = concolic(prog)
        for v in box(2):
            p = trace(prog, v)
            hits = [r for r in runs if holds(r.conds, v)]
            assert len(hits) == 1 and hits[0].path() == p


def test_solver_calls():
    rng = random.Random(3)
    for _ in range(40):
        prog = toyir.random_program(rng, 3, rng.randint(2, 7), acyclic=True)
        inner = brute_force_solver()
        calls = {"sat": 0, "unsat": 0}

        def solve(conds, k):
            m = inner(conds, k)
            calls["sat" if m is not None else "unsat"] += 1
            return m

        runs = concolic(prog, solve)
        assert calls["sat"] == len(runs) - 1
        assert calls["sat"] + calls["unsat"] <= sum(len(r.conds) for r in runs)


def test_start_input_outside_the_order():
    prog = toyir.parse(PAGE)
    runs = concolic(prog, start=[8, 4])
    assert runs[0].outcome == ("ret", 1)
    assert {r.path() for r in runs} == brute_paths(prog)
