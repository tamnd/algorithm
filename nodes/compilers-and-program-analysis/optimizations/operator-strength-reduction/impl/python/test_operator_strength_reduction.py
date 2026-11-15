# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/operator-strength-reduction/. The authors are listed in prov/VGSWKK.jsonl.

import random

import pytest

import toyir
from operator_strength_reduction import check_ssa, osr

PAGE = """
# params: k, n
entry:
  jump h
h:
  i = phi [entry: 0, body: i2]
  s = phi [entry: 0, body: s2]
  c = i < n
  br c body done
body:
  x = i * 4
  y = x + 5
  s2 = s + y
  i2 = i + 1
  jump h
done:
  ret s
"""

PAGE_OUT = """
# params: k, n
entry:
  osr6 = n * 4
  osr7 = osr6 + 5
  jump h
h:
  osr4 = phi [entry: 5, body: osr5]
  s = phi [entry: 0, body: s2]
  c = osr4 < osr7
  br c body done
body:
  osr3 = osr4
  y = osr3
  s2 = s + y
  osr5 = osr4 + 4
  jump h
done:
  ret s
"""

FUNC_F = toyir.parse("# params: u\nentry:\n  v = u * 3\n  w = v - 1\n  ret w\n")
FUNCS = {"f": FUNC_F}


def kinds(prog, kind):
    return [ins for blk in prog.blocks.values() for ins in blk.instrs if ins[0] == kind]


def ops(prog, op):
    return [ins for ins in kinds(prog, "op") if ins[2] == op]


def same(p, q, args, funcs=None, fuel=20000):
    a = toyir.run(p, args, fuel, funcs)
    b = toyir.run(q, args, fuel, funcs)
    assert a[0] != "fuel"
    assert a == b, (args, a, b, toyir.show(p), toyir.show(q))
    return a


def test_page_example():
    p = toyir.parse(PAGE)
    st = {}
    q = osr(p, st)
    assert toyir.show(q) == toyir.show(toyir.parse(PAGE_OUT))
    assert st == {"replaced": 2, "tests": 1}
    assert ops(q, "*") == [("op", "osr6", "*", "n", 4)]
    for n in range(-3, 9):
        same(p, q, [7, n])
    assert toyir.run(q, [0, 3]) == ("ret", 27)


def test_input_is_not_changed():
    p = toyir.parse(PAGE)
    before = toyir.show(p)
    osr(p)
    assert toyir.show(p) == before


def test_stores_and_calls_are_kept():
    p = toyir.parse("""
# params: n
entry:
  m = alloc
  *m = 0
  jump h
h:
  i = phi [entry: 1, body: i2]
  c = i <= n
  br c body done
body:
  x = i * 5
  *m = x
  r = call f(x)
  i2 = i + r
  jump h
done:
  v = *m
  ret v
""")
    q = osr(p)
    assert len(kinds(q, "store")) == 2
    assert len(kinds(q, "call")) == 1
    assert len(kinds(q, "load")) == 1
    assert len(kinds(q, "alloc")) == 1
    for n in range(-2, 40):
        same(p, q, [n], FUNCS)


def test_no_trap_is_added_or_removed():
    p = toyir.parse("""
# params: a, n
entry:
  jump h
h:
  i = phi [entry: -2, body: i2]
  c = i < n
  br c body done
body:
  d = a / i
  x = i * 3
  y = d + x
  i2 = i + 1
  jump h
done:
  ret i
""")
    q = osr(p)
    assert ops(q, "/") == [("op", "d", "/", "a", "i")]
    outs = {same(p, q, [a, n])[0] for a in range(-3, 4) for n in range(-4, 4)}
    assert outs == {"ret", "trap"}


def test_negative_multiplier_swaps_the_test():
    p = toyir.parse("""
# params: n
entry:
  jump h
h:
  i = phi [entry: 0, body: i2]
  s = phi [entry: 0, body: s2]
  c = i < n
  br c body done
body:
  x = i * -2
  s2 = s + x
  i2 = i + 1
  jump h
done:
  ret s
""")
    st = {}
    q = osr(p, st)
    assert st["tests"] == 1
    (cmp,) = ops(q, "<")
    m = [ins for ins in ops(q, "*") if ins[3] == "n"]
    assert cmp[3] == m[0][1]  # the sides are swapped: -2 * n < -2 * i
    for n in range(-3, 9):
        same(p, q, [n])


def test_name_multiplier_keeps_the_test():
    p = toyir.parse("""
# params: k, n
entry:
  jump h
h:
  i = phi [entry: 0, body: i2]
  s = phi [entry: 0, body: s2]
  c = i < n
  br c body done
body:
  x = i * k
  s2 = s + x
  i2 = i + 1
  jump h
done:
  ret s
""")
    st = {}
    q = osr(p, st)
    assert st == {"replaced": 1, "tests": 0}
    assert ("op", "c", "<", "i", "n") in kinds(q, "op")
    for k in (-2, 0, 3):
        for n in range(-2, 6):
            same(p, q, [k, n])


def test_non_candidates_are_kept():
    p = toyir.parse("""
# params: a, n
entry:
  jump h
h:
  i = phi [entry: 0, body: i2]
  s = phi [entry: 0, body: s4]
  c = i < n
  br c body done
body:
  x = i * i
  y = a - i
  s2 = s + x
  s3 = s2 + y
  s4 = s3 * 2
  i2 = i + 1
  jump h
done:
  ret s
""")
    st = {}
    q = osr(p, st)
    assert st["replaced"] == 0
    assert ("op", "x", "*", "i", "i") in kinds(q, "op")
    for a in (-1, 2):
        for n in range(-1, 6):
            same(p, q, [a, n])


def test_nested_loops():
    p = toyir.parse("""
# params: n, m
entry:
  jump h
h:
  i = phi [entry: 0, latch: i2]
  s = phi [entry: 0, latch: s2]
  c = i < n
  br c pre done
pre:
  jump h2
h2:
  j = phi [pre: i, l2: j2]
  t = phi [pre: s, l2: t2]
  d = j < m
  br d l2 latch
l2:
  x = j * 7
  t2 = t + x
  j2 = j + 1
  jump h2
latch:
  s2 = t + 1
  i2 = i + 1
  jump h
done:
  ret s
""")
    st = {}
    q = osr(p, st)
    # j * 7 becomes an inner induction variable that starts at i * 7, and
    # i * 7 becomes an outer one, so both tests are replaced and the only
    # multiplications left are in the entry block.
    assert st == {"replaced": 1, "tests": 2}
    assert [ins[3:] for ins in ops(q, "*")] == [("n", 7), ("m", 7)]
    assert all(ins in q.blocks["entry"].instrs for ins in ops(q, "*"))
    for n in range(-1, 5):
        for m in range(-1, 6):
            same(p, q, [n, m])


def test_errors():
    with pytest.raises(ValueError):
        osr(toyir.parse("# params: a\nentry:\n  x = a + 1\n  x = a + 2\n  ret x\n"))
    with pytest.raises(ValueError):
        osr(toyir.parse("# params: a\nentry:\n  p = &a\n  ret 0\n"))
    with pytest.raises(ValueError):
        osr(toyir.parse("entry:\n  ret 0\nlost:\n  jump entry\n"))
    with pytest.raises(ValueError):
        osr(toyir.parse("# params: a\nentry:\n  y = x + 1\n  x = a + 1\n  ret y\n"))
    with pytest.raises(ValueError):
        osr(toyir.parse("# params: a\nentry:\n  x = a + 1\n  ret x\nb:\n  ret 0\n"))
    with pytest.raises(ValueError):
        osr(toyir.parse("# params: a\nentry:\n  x = a + 1\n  br x entry out\nout:\n  ret x\n"))


# ------------------------------------------------------------ random programs


def gen(rng):
    """A random strict SSA program with params a, b, n. The outer loop runs
    at most 4 times and the inner loop at most 3 times, so it always ends."""
    rcs = ["a", "b", "n", "k1", "k2"]

    def rc():
        return rng.choice(rcs + [str(rng.randint(-3, 5)) for _ in range(3)])

    def cand(iv):
        form = rng.randrange(5)
        r = rc()
        return ["%s * %s" % (iv, r), "%s * %s" % (r, iv), "%s + %s" % (iv, r), "%s + %s" % (r, iv), "%s - %s" % (iv, r)][form]

    def other(iv):
        return rng.choice(["%s * %s" % (iv, iv), "%s - %s" % (rc(), iv), "%s & 3" % iv, "%s * %s" % (iv, "x1")])

    mem = rng.random() < 0.4
    call = rng.random() < 0.4
    inner = rng.random() < 0.6
    trap = rng.random() < 0.5
    cmp = rng.choice(["<", "<=", "!=", "=="])
    L = ["# params: a, b, n", "entry:"]
    L.append("  k1 = a + %d" % rng.randint(-2, 3))
    L.append("  k2 = b * %d" % rng.randint(-2, 3))
    if trap:
        L.append("  q0 = a / b")
    if mem:
        L += ["  m = alloc", "  *m = 0"]
    L += ["  jump h", "h:"]
    L.append("  c = phi [entry: 0, latch: c2]")
    L.append("  i = phi [entry: %s, latch: i3]" % rc())
    L.append("  j = phi [entry: %s, latch: j2]" % rc())
    L.append("  s = phi [entry: 0, latch: s3]")
    L.append("  t1 = c %s n" % cmp)
    L.append("  t2 = c < 4")
    L.append("  t = t1 & t2")
    L.append("  br t body done")
    L.append("body:")
    L.append("  x1 = %s" % cand(rng.choice(["i", "j", "c"])))
    L.append("  x2 = %s" % cand(rng.choice(["x1", "i", "j"])))
    L.append("  x3 = %s" % other(rng.choice(["i", "j", "c"])))
    L.append("  x4 = %s" % cand(rng.choice(["c", "x2"])))
    L.append("  tq = %s %s %s" % (rng.choice(["i", "j", "c"]), rng.choice(["<", "<=", "==", "!="]), rc()))
    if trap:
        L.append("  x5 = a / %s" % rng.choice(["i", "j", "x1"]))
    else:
        L.append("  x5 = x3 + 0")
    if mem:
        L.append("  *m = x2")
    if call:
        L.append("  x6 = call f(x4)")
    else:
        L.append("  x6 = x4 + tq")
    if inner:
        L += ["  jump h2", "h2:"]
        L.append("  ci = phi [body: 0, l2: ci2]")
        L.append("  p = phi [body: %s, l2: p2]" % rng.choice(["i", "x1", "0", "k1"]))
        L.append("  acc = phi [body: 0, l2: acc2]")
        L.append("  u1 = ci < b")
        L.append("  u2 = ci < 3")
        L.append("  u = u1 & u2")
        L.append("  br u l2 e2")
        L.append("l2:")
        L.append("  y1 = %s" % cand(rng.choice(["p", "ci"])))
        L.append("  y2 = %s" % cand(rng.choice(["i", "y1", "p"])))
        L.append("  acc1 = acc + y1")
        L.append("  acc2 = acc1 + y2")
        L.append("  p2 = p %s %s" % (rng.choice(["+", "-"]), rng.choice(["i", "k2", "2", "x1", "-1"])))
        L.append("  ci2 = ci + 1")
        L.append("  jump h2")
        L.append("e2:")
        last = "acc"
    else:
        last = "x5"
    L.append("  bc = c & 1")
    L.append("  br bc left right")
    L.append("left:")
    L.append("  iL = i + %s" % rc())
    L.append("  jump latch")
    L.append("right:")
    L.append("  iR = %s" % rng.choice(["i - %s" % rc(), "%s + i" % rc(), "i * 2", "iRx"]).replace("iRx", "i + 1"))
    L.append("  jump latch")
    L.append("latch:")
    L.append("  i3 = phi [left: iL, right: iR]")
    L.append("  j2 = j %s %s" % (rng.choice(["+", "-"]), rc()))
    L.append("  c2 = c + 1")
    L.append("  s1 = s + x1")
    L.append("  s2 = s1 + x6")
    L.append("  s4 = s2 + %s" % last)
    L.append("  s5 = s4 + x5")
    L.append("  s3 = s5 + x3")
    L.append("  jump h")
    L.append("done:")
    L.append("  z1 = %s" % cand(rng.choice(["i", "j", "c"])))
    L.append("  z2 = s + z1")
    if mem:
        L.append("  z3 = *m")
        L.append("  z4 = z2 + z3")
        L.append("  ret z4")
    else:
        L.append("  ret z2")
    return toyir.parse("\n".join(L) + "\n")


def test_random_programs():
    rng = random.Random(20011201)
    totals = {"replaced": 0, "tests": 0}
    outcomes = {"ret": 0, "trap": 0}
    for _ in range(600):
        p = gen(rng)
        st = {}
        q = osr(p, st)
        check_ssa(q)
        for key in totals:
            totals[key] += st[key]
        for _ in range(8):
            args = [rng.randint(-4, 6) for _ in range(3)]
            outcomes[same(p, q, args, FUNCS)[0]] += 1
    assert totals["replaced"] > 2400
    assert totals["tests"] > 1000
    assert outcomes["trap"] > 300 and outcomes["ret"] > 3000
