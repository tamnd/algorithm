# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generational-search/. The authors are listed in prov/WF74QR.jsonl.

import itertools
import random

import toyir
from generational_search import brute_force_solver, generational, holds

LO, HI = -8, 8

PAGE = """
# params: a, b, c
entry:
  n = 0
  t = a == 7
  br t i1 j1
i1:
  n = n + 1
  jump j1
j1:
  t = b == 5
  br t i2 j2
i2:
  n = n + 1
  jump j2
j2:
  t = c == 3
  br t i3 j3
i3:
  n = n + 1
  jump j3
j3:
  u = 2 <= n
  br u bad ok
bad:
  ret 1
ok:
  ret 0
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
    """A plain concrete run, written apart from the search code:
    (labels, outcome kind, index of the trapping instruction)."""
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


def counting_solver():
    inner = brute_force_solver()
    calls = {"sat": 0, "unsat": 0}

    def solve(conds, k, hint):
        m = inner(conds, k, hint)
        calls["sat" if m is not None else "unsat"] += 1
        return m

    return solve, calls


def check_complete(prog):
    solve, calls = counting_solver()
    runs = generational(prog, solve)
    found = [r.path() for r in runs]
    assert len(found) == len(set(found)), "a path was explored twice"
    assert set(found) == brute_paths(prog)
    for i, r in enumerate(runs):
        assert all(LO <= a <= HI for a in r.args)
        assert r.outcome == toyir.run(prog, r.args)
        if i > 0:
            p = runs[r.parent]
            assert p.bound <= r.flip < len(p.conds)
            assert r.bound == r.flip + 1
            assert r.conds[: r.flip] == p.conds[: r.flip]
            assert r.conds[r.flip] == (p.conds[r.flip][0], not p.conds[r.flip][1])
    assert calls["sat"] == len(runs) - 1
    assert calls["sat"] + calls["unsat"] == sum(len(r.conds) - r.bound for r in runs)
    return runs


def test_page_example():
    prog = toyir.parse(PAGE)
    runs = check_complete(prog)
    assert [tuple(r.args) for r in runs] == [
        (0, 0, 0),
        (7, 0, 0),
        (0, 5, 0),
        (0, 0, 3),
        (7, 5, 0),
        (7, 0, 3),
        (0, 5, 3),
        (7, 5, 3),
    ]
    assert [r.outcome[1] for r in runs] == [0, 0, 0, 0, 1, 1, 1, 1]
    assert [r.score for r in runs] == [5, 1, 1, 1, 1, 0, 0, 0]
    assert [r.bound for r in runs] == [0, 1, 2, 3, 2, 3, 3, 3]
    # The last test of the program is on a constant, so no run records it.
    assert all(len(r.conds) == 3 for r in runs)


def test_the_solver_keeps_the_hint():
    solve = brute_force_solver()
    cond = (("op", "==", ("in", 1), ("k", 5)), True)
    assert solve([cond], 3, [4, 0, -2]) == [4, 5, -2]
    assert solve([(cond[0], False)], 3, [4, 0, -2]) == [4, 0, -2]
    assert solve([cond, (cond[0], False)], 3, [4, 0, -2]) is None


def test_implicit_trap_condition():
    runs = check_complete(toyir.parse(DIVIDE))
    assert sorted(r.outcome for r in runs) == [("ret", 1), ("ret", 2), ("ret", 3), ("trap",)]


def test_counted_loop_stops_at_the_box():
    runs = check_complete(toyir.parse(COUNT))
    assert sorted(r.args[0] for r in runs) == list(range(0, 9))


def ladder(rng, k):
    """k tests in a row on linear terms of x, y and the running sum s, with a
    division by s at the end."""
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
    sizes = [len(check_complete(ladder(rng, rng.randint(2, 5)))) for _ in range(12)]
    assert max(sizes) >= 10


def test_random_loop_free_programs():
    rng = random.Random(20261115)
    for _ in range(80):
        check_complete(toyir.random_program(rng, rng.randint(2, 4), rng.randint(2, 7), acyclic=True))


def test_random_programs_with_loops():
    rng = random.Random(7)
    for _ in range(30):
        check_complete(toyir.random_program(rng, rng.randint(2, 4), rng.randint(3, 7), acyclic=False))


def test_path_condition_is_exact():
    rng = random.Random(11)
    for _ in range(30):
        prog = toyir.random_program(rng, 3, rng.randint(2, 6), acyclic=rng.random() < 0.5)
        runs = generational(prog)
        for v in box(2):
            hits = [r for r in runs if holds(r.conds, v)]
            assert len(hits) == 1 and hits[0].path() == trace(prog, v)


def test_budget():
    prog = toyir.parse(PAGE)
    runs = generational(prog, max_runs=5)
    assert len(runs) == 5
    assert runs[-1].outcome == ("ret", 1)
