# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-value-numbering/. The authors are listed in prov/CJTBEP.jsonl.

import random

import toyir
from local_value_numbering import evaluate, lvn, lvn_block

PAGE = """
# params: x, y, d
entry:
  a = x + y
  b = y + x
  a = 17
  c = x + y
  e = c * 1
  f = a * 2
  g = x / d
  h = x / d
  k = d / d
  r = g - h
  t = c + f
  t = t + h
  t = t + k
  t = t + r
  ret t
"""

PAGE_AFTER = """
# params: x, y, d
entry:
  a = x + y
  b = a
  a = 17
  c = b
  e = c
  f = 34
  g = x / d
  h = g
  k = d / d
  r = 0
  t = c + f
  t = t + h
  t = t + k
  t = t
  ret t
"""

# The classic block of Cooper and Torczon: d = a - d is redundant, but
# c = b + c is not, because b was redefined in between.
CLASSIC = """
# params: b, c, d
entry:
  a = b + c
  b = a - d
  c = b + c
  d = a - d
  ret d
"""

# f adds its second argument to the cell p and returns the new value, so two
# equal calls give different results.
FUNC_F = toyir.parse(
    """
# params: p, a
entry:
  v = *p
  v = v + a
  *p = v
  ret v
"""
)

MEMORY = """
# params: x
entry:
  p = alloc
  *p = x
  u = *p
  *p = 5
  v = *p
  s = call f(p, x)
  t = call f(p, x)
  w = u + v
  w = w + s
  w = w + t
  ret w
"""


def count_ops(prog, args, fuel=10000):
    """Run a program without memory, phis or calls, and count the executed
    op instructions. Returns (outcome, count) with the outcome of toyir.run."""
    env = dict(zip(prog.params, args))
    label = prog.entry
    count = 0
    steps = 0

    def val(a):
        return a if isinstance(a, int) else env[a]

    while True:
        blk = prog.blocks[label]
        for ins in blk.instrs:
            steps += 1
            if steps > fuel:
                return ("fuel",), count
            if ins[0] == "const":
                env[ins[1]] = ins[2]
            elif ins[0] == "copy":
                env[ins[1]] = val(ins[2])
            else:
                count += 1
                r = evaluate(ins[2], val(ins[3]), val(ins[4]))
                if r is None:
                    return ("trap",), count
                env[ins[1]] = r
        steps += 1
        if steps > fuel:
            return ("fuel",), count
        t = blk.term
        if t[0] == "ret":
            return ("ret", val(t[1])), count
        if t[0] == "jump":
            label = t[1]
        else:
            label = t[2] if val(t[1]) != 0 else t[3]


def add_redundancy(rng, prog):
    """Insert, some instructions after an op instruction, a recomputation of
    the same operation into a variable x_i, sometimes with the operands
    swapped. The loop counters are never written."""
    names = ["x%d" % i for i in range(5)]
    for blk in prog.blocks.values():
        out = []
        pending = []
        for ins in blk.instrs:
            out.append(ins)
            if pending and rng.random() < 0.5:
                out.append(pending.pop(0))
            if ins[0] == "op" and rng.random() < 0.6:
                op, a, b = ins[2], ins[3], ins[4]
                if op in ("+", "*", "&", "|", "^", "==", "!=") and rng.random() < 0.5:
                    a, b = b, a
                pending.append(("op", rng.choice(names), op, a, b))
        blk.instrs = out + pending
    return prog


def same_shape(p, q):
    """The i-th instruction keeps its kind or becomes a const or a copy, and
    the destination and the terminators do not change."""
    assert list(p.blocks) == list(q.blocks)
    for label in p.blocks:
        a, b = p.blocks[label], q.blocks[label]
        assert a.term == b.term
        assert len(a.instrs) == len(b.instrs)
        for i, j in zip(a.instrs, b.instrs):
            if i[0] in ("op",):
                assert j == i or j[0] in ("const", "copy")
                assert j[1] == i[1]
            else:
                assert j == i


def test_page_example():
    p = toyir.parse(PAGE)
    q = lvn(p)
    assert toyir.show(q) == toyir.show(toyir.parse(PAGE_AFTER))
    for x in range(-6, 7):
        for y in range(-3, 4):
            for d in range(-3, 4):
                assert toyir.run(p, [x, y, d]) == toyir.run(q, [x, y, d])
    out, before = count_ops(p, [7, 2, 3])
    out2, after = count_ops(q, [7, 2, 3])
    assert out == out2 == ("ret", 9 + 34 + 2 + 1 + 0)
    assert (before, after) == (13, 6)
    # A zero divisor still traps at the first division.
    assert toyir.run(q, [7, 2, 0]) == ("trap",)


def test_classic_block():
    q = lvn(toyir.parse(CLASSIC))
    instrs = q.blocks["entry"].instrs
    assert instrs[2] == ("op", "c", "+", "b", "c")
    assert instrs[3] == ("copy", "d", "b")


def test_traps_are_kept():
    src = """
# params: x, y
entry:
  a = 0 / y
  b = y / y
  c = y % y
  e = x << y
  f = 7 / 0
  g = 1 << 64
  ret a
"""
    p = toyir.parse(src)
    q = lvn(p)
    assert q.blocks["entry"].instrs == p.blocks["entry"].instrs
    assert toyir.run(q, [3, 0]) == ("trap",)


def test_safe_identities():
    src = """
# params: x
entry:
  a = x * 0
  b = x % 1
  c = x - x
  e = x / 1
  f = x << 0
  g = x ^ x
  h = x <= x
  ret a
"""
    q = lvn(toyir.parse(src))
    kinds = [ins[0] for ins in q.blocks["entry"].instrs]
    assert kinds == ["const", "const", "const", "copy", "copy", "const", "const"]


def test_memory_and_calls_are_kept():
    p = toyir.parse(MEMORY)
    q = lvn(p)
    assert q.blocks["entry"].instrs == p.blocks["entry"].instrs
    for x in range(-4, 5):
        out = toyir.run(p, [x], funcs={"f": FUNC_F})
        assert out == toyir.run(q, [x], funcs={"f": FUNC_F})
    # u = x, v = 5, s = 5 + x, t = 5 + 2x
    assert toyir.run(q, [3], funcs={"f": FUNC_F}) == ("ret", 3 + 5 + 8 + 11)


def test_folding_uses_truncating_division():
    q = lvn(toyir.parse("# params: x\nentry:\n  a = -7 / 2\n  b = -7 % 2\n  c = 42 / -5\n  ret a\n"))
    assert q.blocks["entry"].instrs == [("const", "a", -3), ("const", "b", -1), ("const", "c", -8)]


def test_redefined_holder():
    src = """
# params: x, y
entry:
  a = x + y
  a = 0
  b = x + y
  ret b
"""
    q = lvn(toyir.parse(src))
    # No name holds x + y any more, so the operation is kept.
    assert q.blocks["entry"].instrs[2] == ("op", "b", "+", "x", "y")


def test_random_programs():
    rng = random.Random(20261115)
    hits = 0
    for trial in range(300):
        p = toyir.random_program(rng, 5, rng.randint(2, 8), acyclic=trial % 2 == 0)
        if trial % 3:
            add_redundancy(rng, p)
        q = lvn(p)
        same_shape(p, q)
        for _ in range(12):
            args = [rng.randint(-6, 6), rng.randint(-6, 6)]
            a, n1 = count_ops(p, args)
            b, n2 = count_ops(q, args)
            assert a == toyir.run(p, args)
            assert a == b
            assert n2 <= n1
            hits += n2 < n1
    assert hits > 100


def test_block_function_matches():
    rng = random.Random(7)
    p = add_redundancy(rng, toyir.random_program(rng, 4, 3, acyclic=True))
    for label, blk in p.blocks.items():
        assert lvn(p).blocks[label].instrs == lvn_block(blk.instrs)
