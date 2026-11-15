# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazy-code-motion/. The authors are listed in prov/AQQH48.jsonl.
import random
from collections import Counter

import toyir
import lazy_code_motion as L

PAGE_BEFORE = """# params: a, b, n
B0:
  i = 0
  br n B1 B2
B1:
  x = a * b
  jump B3
B2:
  a = a + 1
  jump B3
B3:
  i = i + 1
  y = a * b
  c = i < n
  br c B3 B4
B4:
  z = a * b
  ret z
"""

PAGE_AFTER = """# params: a, b, n
B0:
  i = 0
  br n B1 B2
B1:
  pre.0 = a * b
  x = pre.0
  jump B3
B2:
  a = a + 1
  pre.0 = a * b
  jump B3
B3:
  i = i + 1
  y = pre.0
  c = i < n
  br c B3_B3 B4
B3_B3:
  jump B3
B4:
  z = pre.0
  ret z
"""

PAGE_BUSY = """# params: a, b, n
B0:
  i = 0
  pre.2 = i + 1
  br n B1 B2
B1:
  pre.0 = a * b
  x = pre.0
  jump B3
B2:
  pre.1 = a + 1
  a = pre.1
  pre.0 = a * b
  jump B3
B3:
  i = pre.2
  pre.3 = i < n
  y = pre.0
  c = pre.3
  br c B3_B3 B4
B3_B3:
  pre.2 = i + 1
  jump B3
B4:
  z = pre.0
  ret z
"""

FUEL = 100000


def busy(prog):
    """Busy code motion: insert at the earliest points and replace every
    original computation."""
    p = L.normalize(prog)
    a = L.analyses(p)
    return L.rewrite(p, a["exprs"], a["earliest"], a["use"])


def counts(prog, path):
    c = Counter()
    for b in path:
        for ins in prog.blocks[b].instrs:
            e = L.expression(ins)
            if e is not None:
                c[e] += 1
    return c


VARS = ("x0", "x1", "x2")


def dense_instr(rng):
    r = rng.random()
    if r < 0.2:
        x = rng.choice(VARS)
        return ("op", x, "+", x, 1)
    if r < 0.3:
        return ("copy", rng.choice(VARS), rng.choice(VARS))
    x = rng.choice(VARS + ("y0", "y1"))
    return ("op", x, rng.choice(("+", "/")), rng.choice(VARS), rng.choice(VARS + (2,)))


def dense(rng, nblocks, acyclic, most=3):
    """A random program over few names and two operators, so the same
    expression is often computed on several paths. Division by a variable
    can trap. The control flow and the loop counters come from
    toyir.random_program."""
    prog = toyir.random_program(rng, 3, nblocks, acyclic)
    for blk in prog.blocks.values():
        new = []
        for ins in blk.instrs:
            if ins[0] in ("op", "copy") and ins[1] in VARS:
                for _ in range(rng.randint(1, most)):
                    new.append(dense_instr(rng))
            else:
                new.append(ins)
        blk.instrs = new
    return prog


def programs(seed, n):
    rng = random.Random(seed)
    for k in range(n):
        acyclic = k % 2 == 0
        if k % 3 == 0:
            yield toyir.random_program(rng, rng.randint(2, 4), rng.randint(2, 7), acyclic)
        else:
            yield dense(rng, rng.randint(2, 7), acyclic)


ARGS = [(0, 0), (1, 0), (0, 1), (2, 3), (-2, 2), (3, -1), (2, 2), (-1, -1)]


def node_paths(prog):
    out = []
    for path in toyir.paths(prog):
        ns = []
        for b in path:
            ns += [(b, i) for i in range(len(prog.blocks[b].instrs) + 1)]
        out.append(ns)
    return out


def up_safe(g, comp, killn):
    """Up-safe: on every path from the entry, e was computed and no operand
    changed since."""
    up_in = {n: True for n in g.nodes}
    up_out = {n: True for n in g.nodes}
    changed = True
    while changed:
        changed = False
        for n in g.nodes:
            inn = bool(g.pred[n]) and all(up_out[p] for p in g.pred[n])
            out = (inn or n in comp) and n not in killn
            if (inn, out) != (up_in[n], up_out[n]):
                up_in[n], up_out[n] = inn, out
                changed = True
    return up_in


def admissible(g, comp, killn, ins):
    """True if t = e is valid at every original computation of e when it
    is computed before each node of ins."""
    vout = {n: True for n in g.nodes}
    before = {}
    changed = True
    while changed:
        changed = False
        for n in g.nodes:
            inn = bool(g.pred[n]) and all(vout[p] for p in g.pred[n])
            before[n] = inn or n in ins
            out = before[n] and n not in killn
            if out != vout[n]:
                vout[n] = out
                changed = True
    return all(before[n] for n in comp)


def lifetime(g, comp, ins):
    """The nodes after which t is live."""
    live_before = {n: False for n in g.nodes}
    live_out = {n: False for n in g.nodes}
    changed = True
    while changed:
        changed = False
        for n in reversed(g.nodes):
            out = any(live_before[s] for s in g.succ[n])
            before = n not in ins and (n in comp or out)
            if (out, before) != (live_out[n], live_before[n]):
                live_out[n], live_before[n] = out, before
                changed = True
    return frozenset(n for n in g.nodes if live_out[n])


def safe_placements(prog, a, k, limit):
    """Every admissible placement of expression k at safe nodes, as pairs
    (set of nodes, evaluations per path). None if there are too many safe
    nodes."""
    g = a["graph"]
    bit = 1 << k
    comp = {n for n in g.nodes if a["use"][n] & bit}
    killn = {n for n in g.nodes if a["kill"][n] & bit}
    up = up_safe(g, comp, killn)
    safe = [n for n in g.nodes if a["ant_in"][n] & bit or up[n]]
    if len(safe) > limit:
        return None
    paths = node_paths(prog)
    out = []
    for mask in range(1 << len(safe)):
        ins = {safe[j] for j in range(len(safe)) if mask >> j & 1}
        if admissible(g, comp, killn, ins):
            out.append((ins, tuple(sum(n in ins for n in p) for p in paths)))
    return comp, out


# ------------------------------------------------------------------- tests


def test_page_example():
    p = toyir.parse(PAGE_BEFORE)
    q = L.lcm(p)
    assert toyir.show(q) == PAGE_AFTER
    assert toyir.show(busy(p)) == PAGE_BUSY
    for args in [(2, 3, 1), (2, 3, 4), (0, 0, 0), (5, -1, 2)]:
        assert toyir.run(q, args) == toyir.run(p, args)
    # One trip through the loop on the path through B1: a * b runs 3 times
    # before and once after.
    path = ["B0", "B1", "B3", "B4"]
    e = ("*", "a", "b")
    assert counts(p, path)[e] == 3 and counts(q, path)[e] == 1


def test_same_outcome_on_random_programs():
    for prog in programs(1, 400):
        q = L.lcm(prog)
        b = busy(prog)
        for args in ARGS:
            want = toyir.run(prog, args, FUEL)
            assert want != ("fuel",)
            assert toyir.run(q, args, FUEL) == want
            assert toyir.run(b, args, FUEL) == want


def test_never_more_evaluations_on_any_path():
    better = 0
    for prog in programs(2, 400):
        if not toyir.is_acyclic(prog):
            continue
        p = L.normalize(prog)
        q = L.lcm(prog)
        b = busy(prog)
        assert list(q.blocks) == list(p.blocks)
        for path in toyir.paths(p):
            old, new, bcm = counts(p, path), counts(q, path), counts(b, path)
            for e in old:
                assert new[e] <= old[e]
                assert new[e] == bcm[e]
                better += new[e] < old[e]
            assert set(new) <= set(old)
    assert better > 50


def test_computationally_and_lifetime_optimal():
    rng = random.Random(3)
    checked = optimal_others = 0
    for _ in range(250):
        prog = L.normalize(dense(rng, rng.randint(2, 4), True, most=2))
        a = L.analyses(prog)
        q = L.rewrite(prog, a["exprs"],
                      {n: a["latest"][n] & a["used_out"][n] for n in a["graph"].nodes},
                      {n: a["use"][n] & (~a["latest"][n] | a["used_out"][n]) for n in a["graph"].nodes})
        assert toyir.show(q) == toyir.show(L.lcm(prog))
        paths = node_paths(prog)
        for k, e in enumerate(a["exprs"]):
            bit = 1 << k
            got = safe_placements(prog, a, k, 10)
            if got is None:
                continue
            comp, places = got
            mine = {n for n in a["graph"].nodes
                    if a["latest"][n] & bit and (a["used_out"][n] | a["use"][n]) & bit}
            vec = tuple(sum(n in mine for n in p) for p in paths)
            # The placement model gives the counts of the real program.
            assert vec == tuple(counts(q, toyir.paths(prog)[i])[e] for i in range(len(paths)))
            assert any(ins == mine for ins, _ in places)
            life = lifetime(a["graph"], comp, mine)
            for ins, v in places:
                assert all(x <= y for x, y in zip(vec, v))
                if v == vec:
                    assert life <= lifetime(a["graph"], comp, ins)
                    optimal_others += ins != mine
            checked += 1
    assert checked > 300 and optimal_others > 50


CRITICAL = """# params: a, b, c, d
B0:
  br c B1 B2
B1:
  x = a / b
  jump B3
B2:
  br d B3 B4
B3:
  y = a / b
  ret y
B4:
  ret 0
"""


def test_critical_edge_gets_the_insertion():
    p = toyir.parse(CRITICAL)
    q = L.lcm(p)
    assert q.blocks["B2_B3"].instrs == [("op", "pre.0", "/", "a", "b")]
    assert q.blocks["B2"].instrs == [] and q.blocks["B0"].instrs == []
    e = ("/", "a", "b")
    assert counts(q, ["B0", "B1", "B3"])[e] == 1
    # b = 0 on the path to B4: no division runs there.
    assert toyir.run(p, (1, 0, 0, 0)) == toyir.run(q, (1, 0, 0, 0)) == ("ret", 0)


def test_without_split_no_safe_placement_removes_the_redundancy():
    p = toyir.parse(CRITICAL)
    a = L.analyses(p)  # the graph of p itself, with the critical edge
    comp, places = safe_placements(p, a, 0, 12)
    paths = toyir.paths(p)
    old = tuple(counts(p, path)[("/", "a", "b")] for path in paths)
    for _, v in places:
        assert v == old or any(x > y for x, y in zip(v, old))


ZERO_TRIP = """# params: a, b, n
B0:
  i = 0
  jump B1
B1:
  c = i < n
  br c B2 B3
B2:
  x = a / b
  i = i + 1
  jump B1
B3:
  ret i
"""


def test_no_hoisting_out_of_a_loop_that_may_not_run():
    p = toyir.parse(ZERO_TRIP)
    q = L.lcm(p)
    for b, blk in q.blocks.items():
        for ins in blk.instrs:
            if L.expression(ins) == ("/", "a", "b"):
                assert b == "B2"
    assert toyir.run(q, (1, 0, 0)) == ("ret", 0)
    assert toyir.run(q, (1, 0, 2)) == ("trap",)
