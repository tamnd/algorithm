# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aggressive-dead-code-elimination/. The authors are listed in prov/VFFWX5.jsonl.

import random

import toyir
from aggressive_dead_code_elimination import adce, mark, may_trap

PAGE = """
# params: a, b
entry:
  s = 0
  i = 0
  q = a / b
  jump h
h:
  t = i < 3
  br t body done
body:
  s = s + i
  k = s & 1
  br k odd even
odd:
  s = s + 1
  jump join
even:
  s = s - 1
  jump join
join:
  i = i + 1
  jump h
done:
  r = a + i
  ret r
"""

PAGE_AFTER = """
# params: a, b
entry:
  i = 0
  q = a / b
  jump h
h:
  t = i < 3
  br t body done
body:
  jump join
join:
  i = i + 1
  jump h
done:
  r = a + i
  ret r
"""

# A loop with no marked statement. Its branch is replaced by a jump to the
# nearest useful post-dominator, out. Jumping back to w, one of the old
# targets, would loop forever.
USELESS_LOOP = """
# params: a
entry:
  j = 0
  jump w
w:
  j = j + 1
  k = j < 5
  br k w out
out:
  ret a
"""

# With a != 0 the input loops forever in code with no marked statement.
# ADCE assumes that such a loop ends, and the output returns 1.
ENDLESS = """
# params: a
entry:
  i = 0
  jump h
h:
  i = i + 0
  br a h done
done:
  ret 1
"""

# f adds v to the cell q points to and returns the new value.
FUNC_F = toyir.parse("# params: q, v\nentry:\n  w = *q\n  s = w + v\n  *q = s\n  ret s\n")


def steps(prog, args, funcs=None, limit=4096):
    """The number of instructions and terminators a run executes."""
    if toyir.run(prog, args, fuel=limit, funcs=funcs) == ("fuel",):
        return None
    lo, hi = 0, limit
    while lo < hi:
        mid = (lo + hi) // 2
        if toyir.run(prog, args, fuel=mid, funcs=funcs) == ("fuel",):
            lo = mid + 1
        else:
            hi = mid
    return lo


def size(prog):
    return sum(len(blk.instrs) + 1 for blk in prog.blocks.values())


def add_memory(rng, prog, nvars):
    """Insert memory operations: a heap cell p, a pointer r to x3, and stores,
    loads and calls of f at random places."""
    xs = ["x%d" % i for i in range(nvars)]
    entry = prog.blocks[prog.entry]
    entry.instrs += [("alloc", "p"), ("store", "p", 0), ("addr", "r", "x3")]
    for label, blk in prog.blocks.items():
        out = []
        start = len(blk.instrs) if label == prog.entry else 0
        for i, ins in enumerate(blk.instrs):
            out.append(ins)
            if label == prog.entry and i < start - 1:
                continue
            u = rng.random()
            if u < 0.12:
                out.append(("store", "p", rng.choice(xs)))
            elif u < 0.2:
                out.append(("load", rng.choice(xs), "p"))
            elif u < 0.26:
                out.append(("call", rng.choice(xs), "f", ["p", rng.choice(xs)]))
            elif u < 0.32:
                out.append(("store", "r", rng.choice(xs)))
            elif u < 0.38:
                out.append(("load", rng.choice(xs), "r"))
        blk.instrs = out
    return prog


def test_page_example():
    p = toyir.parse(PAGE)
    q = adce(p)
    assert toyir.show(q) == toyir.show(toyir.parse(PAGE_AFTER))
    for a in range(-4, 5):
        for b in (-2, 0, 3):
            assert toyir.run(p, [a, b]) == toyir.run(q, [a, b])
    assert toyir.run(q, [5, 0]) == ("trap",)
    assert toyir.run(q, [5, 2]) == ("ret", 8)
    assert (steps(p, [5, 2]), steps(q, [5, 2])) == (35, 22)


def test_useless_loop_jumps_to_useful_postdominator():
    p = toyir.parse(USELESS_LOOP)
    q = adce(p)
    assert q.blocks["w"].instrs == []
    assert q.blocks["w"].term == ("jump", "out")
    assert toyir.run(q, [4]) == toyir.run(p, [4]) == ("ret", 4)


def test_endless_useless_loop_is_assumed_to_end():
    p = toyir.parse(ENDLESS)
    q = adce(p)
    assert toyir.run(p, [1]) == ("fuel",)
    assert toyir.run(q, [1]) == ("ret", 1)
    assert toyir.run(p, [0]) == toyir.run(q, [0]) == ("ret", 1)


def test_branch_that_guards_a_store_is_kept():
    src = """
# params: a
entry:
  p = alloc
  *p = 0
  c = a < 3
  br c yes no
yes:
  *p = 7
  jump no
no:
  v = *p
  ret v
"""
    p = toyir.parse(src)
    q = adce(p)
    assert q.blocks["entry"].term == ("br", "c", "yes", "no")
    assert ("store", "p", 7) in q.blocks["yes"].instrs
    for a in range(0, 6):
        assert toyir.run(q, [a]) == toyir.run(p, [a])


def test_stores_calls_and_traps_are_kept():
    src = """
# params: a, b
entry:
  p = alloc
  *p = a
  w = call f(p, b)
  d = a / b
  e = a << b
  z = a % 4
  u = a >> 2
  ret 0
"""
    p = toyir.parse(src)
    q = adce(p)
    kinds = [ins[0] for ins in q.blocks["entry"].instrs]
    assert kinds == ["alloc", "store", "call", "op", "op"]
    assert [ins[2] for ins in q.blocks["entry"].instrs[3:]] == ["/", "<<"]
    funcs = {"f": FUNC_F}
    assert toyir.run(q, [3, 0], funcs=funcs) == toyir.run(p, [3, 0], funcs=funcs) == ("trap",)
    assert toyir.run(q, [3, 70], funcs=funcs) == ("trap",)
    assert toyir.run(q, [3, 1], funcs=funcs) == ("ret", 0)


def test_address_taken_name_is_kept():
    src = """
# params: a
entry:
  x = a + 1
  r = &x
  y = *r
  ret y
"""
    p = toyir.parse(src)
    q = adce(p)
    assert ("op", "x", "+", "a", 1) in q.blocks["entry"].instrs
    assert toyir.run(q, [4]) == ("ret", 5)


def test_may_trap():
    assert may_trap(("op", "x", "/", "a", "b"))
    assert may_trap(("op", "x", "%", "a", 0))
    assert not may_trap(("op", "x", "/", "a", -3))
    assert may_trap(("op", "x", "<<", "a", 64))
    assert not may_trap(("op", "x", ">>", "a", 63))
    assert not may_trap(("op", "x", "+", "a", "b"))


def test_errors():
    for src in (
        "entry:\n  jump b\nb:\n  x = phi [entry: 1]\n  ret x\n",
        "entry:\n  jump l\nl:\n  jump l\n",
    ):
        try:
            adce(toyir.parse(src))
        except ValueError:
            continue
        raise AssertionError("expected ValueError")


def test_random_programs():
    rng = random.Random(2026)
    funcs = {"f": FUNC_F}
    removed = 0
    jumps = 0
    traps = 0
    for trial in range(240):
        nvars = 5
        p = toyir.random_program(rng, nvars, rng.randint(4, 8), acyclic=trial % 2 == 0)
        if trial % 3:
            add_memory(rng, p, nvars)
        q = adce(p)
        assert size(q) <= size(p)
        removed += size(p) - size(q)
        marked, _, _ = mark(p)
        jumps += sum(
            1
            for b, blk in p.blocks.items()
            if blk.term[0] == "br" and (b, len(blk.instrs)) not in marked
        )
        for _ in range(6):
            args = [rng.randint(-5, 5), rng.randint(-5, 5)]
            out = toyir.run(p, args, funcs=funcs)
            assert out != ("fuel",)
            assert toyir.run(q, args, funcs=funcs) == out
            traps += out == ("trap",)
            assert steps(q, args, funcs) <= steps(p, args, funcs)
    assert removed > 1000
    assert jumps > 50
    assert traps > 20
