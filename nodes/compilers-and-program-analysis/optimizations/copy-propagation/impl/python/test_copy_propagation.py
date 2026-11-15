# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/copy-propagation/. The authors are listed in prov/3N51WA.jsonl.

import random

import toyir
from copy_propagation import (
    available_copies,
    copy_propagation,
    propagate,
    remove_dead_copies,
)

PAGE = """
# params: a, n
entry:
  b = a
  c = b
  br n left right
left:
  d = c + 1
  b = 7
  jump join
right:
  d = c * 2
  jump join
join:
  e = c + b
  e = e + d
  ret e
"""

PAGE_AFTER = """
# params: a, n
entry:
  b = a
  br n left right
left:
  d = a + 1
  b = 7
  jump join
right:
  d = a * 2
  jump join
join:
  e = a + b
  e = e + d
  ret e
"""

# y = a is killed inside the loop by a = a + 1, so the use of y in the
# loop must stay.
LOOP = """
# params: a
entry:
  y = a
  i = 0
  s = 0
  jump h
h:
  t = i < 3
  br t body done
body:
  z = y + i
  s = s + z
  a = a + 1
  i = i + 1
  jump h
done:
  r = s + a
  ret r
"""

ADDRESS = """
# params: x
entry:
  p = &x
  y = x
  *p = 5
  z = y + 0
  ret z
"""

CALL = """
# params: x
entry:
  p = &x
  y = x
  w = call f(p)
  z = y + w
  ret z
"""

# f stores 100 through its pointer argument and returns 1.
FUNC_F = toyir.parse("# params: q\nentry:\n  *q = 100\n  ret 1\n")


def steps(prog, args, funcs=None, limit=4096):
    """The number of instructions and terminators a run executes, found as
    the smallest fuel for which toyir.run does not run out."""
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


def add_copies(rng, prog, nvars):
    """Insert copies x_i = x_j at random places, so that chains of copies and
    copies killed on some paths appear."""
    xs = ["x%d" % i for i in range(nvars)]
    for label, blk in prog.blocks.items():
        out = []
        # In the entry, wait until every x_i has a value.
        defined = set(prog.params) if label == prog.entry else set(xs)
        for ins in blk.instrs:
            if defined >= set(xs) and rng.random() < 0.5:
                out.append(("copy", rng.choice(xs), rng.choice(xs)))
            out.append(ins)
            defined.add(toyir.defs(ins))
        blk.instrs = out
    return prog


def test_page_example():
    p = toyir.parse(PAGE)
    q, rounds = copy_propagation(p)
    assert toyir.show(q) == toyir.show(toyir.parse(PAGE_AFTER))
    assert rounds == 3
    for a in range(-5, 6):
        for n in (0, 1):
            assert toyir.run(p, [a, n]) == toyir.run(q, [a, n])


def test_page_available_sets():
    inn = available_copies(toyir.parse(PAGE))
    assert inn["left"] == {("b", "a"), ("c", "b")}
    assert inn["join"] == set()
    # After the first round c = b has become c = a, which survives b = 7.
    p1, _ = propagate(toyir.parse(PAGE))
    assert available_copies(p1)["join"] == {("c", "a")}


def test_copy_killed_in_loop():
    p = toyir.parse(LOOP)
    q, _ = copy_propagation(p)
    assert ("op", "z", "+", "y", "i") in q.blocks["body"].instrs
    for a in range(-4, 5):
        assert toyir.run(p, [a]) == toyir.run(q, [a]) == ("ret", 3 * a + 3 + 3 + a)


def test_store_through_pointer_kills_copy():
    p = toyir.parse(ADDRESS)
    q, _ = copy_propagation(p)
    assert ("op", "z", "+", "y", 0) in q.blocks["entry"].instrs
    assert toyir.run(q, [9]) == toyir.run(p, [9]) == ("ret", 9)


def test_call_kills_copy_of_address_taken_name():
    p = toyir.parse(CALL)
    q, _ = copy_propagation(p)
    assert ("op", "z", "+", "y", "w") in q.blocks["entry"].instrs
    assert toyir.run(q, [9], funcs={"f": FUNC_F}) == ("ret", 10)


def test_stores_and_calls_are_kept():
    src = """
# params: x
entry:
  p = alloc
  y = x
  *p = y
  w = call f(p)
  u = *p
  r = u + w
  ret r
"""
    p = toyir.parse(src)
    q, _ = copy_propagation(p)
    kinds = [ins[0] for ins in q.blocks["entry"].instrs]
    assert kinds == ["alloc", "store", "call", "load", "op"]
    assert q.blocks["entry"].instrs[1] == ("store", "p", "x")
    for x in range(-3, 4):
        assert toyir.run(p, [x], funcs={"f": FUNC_F}) == toyir.run(q, [x], funcs={"f": FUNC_F}) == ("ret", 101)


def test_division_keeps_its_trap():
    src = "# params: a, b\nentry:\n  c = b\n  q = a / c\n  ret q\n"
    p = toyir.parse(src)
    q, _ = copy_propagation(p)
    assert q.blocks["entry"].instrs == [("op", "q", "/", "a", "b")]
    assert toyir.run(q, [5, 0]) == ("trap",)
    assert toyir.run(q, [-7, 2]) == ("ret", -3)


def test_phi_is_rejected():
    p = toyir.parse("entry:\n  jump b\nb:\n  x = phi [entry: 1]\n  ret x\n")
    try:
        copy_propagation(p)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_random_programs():
    rng = random.Random(1115)
    better = 0
    traps = 0
    max_rounds = 0
    for trial in range(220):
        nvars = 5
        p = toyir.random_program(rng, nvars, rng.randint(4, 8), acyclic=trial % 2 == 0)
        add_copies(rng, p, nvars)
        q, rounds = copy_propagation(p)
        max_rounds = max(max_rounds, rounds)
        # The dead copies are gone: a second removal finds nothing.
        assert toyir.show(remove_dead_copies(q)) == toyir.show(q)
        for _ in range(6):
            args = [rng.randint(-5, 5), rng.randint(-5, 5)]
            out = toyir.run(p, args)
            assert out == toyir.run(q, args)
            traps += out == ("trap",)
            s1, s2 = steps(p, args), steps(q, args)
            assert s2 <= s1
            better += s2 < s1
    assert better > 600
    assert traps > 20
    assert max_rounds <= 6
