# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ssapre/. The authors are listed in prov/H6X0KK.jsonl.
import random
from collections import Counter

import toyir
import ssapre as S

PAGE_BEFORE = """# params: a, b, c, n
B0:
  i = 0
  br c B1 B2
B1:
  x = a + b
  jump B3
B2:
  x = 0
  jump B3
B3:
  y = a + b
  i = i + 1
  d = i < n
  br d B3 B4
B4:
  ret y
"""

PAGE_AFTER = """# params: a, b, c, n
B0:
  i = 0
  br c B1 B2
B1:
  pre.0 = a + b
  x = pre.0
  jump B3
B2:
  x = 0
  pre.0 = a + b
  jump B3
B3:
  y = pre.0
  i = i + 1
  d = i < n
  br d B3_B3 B4
B3_B3:
  jump B3
B4:
  ret y
"""

FUEL = 100000


def counts(prog, path):
    c = Counter()
    for b in path:
        for ins in prog.blocks[b].instrs:
            e = S.expression(ins)
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
            yield dense(rng, rng.randint(2, 8), acyclic)


ARGS = [(0, 0), (1, 0), (0, 1), (2, 3), (-2, 2), (3, -1), (2, 2), (-1, -1)]


def busy_points(p, e):
    """The oracle: the earliest safe points of e, on the graph with one node
    for each instruction and terminator. Busy code motion computes e exactly
    there, and it is computationally optimal (Knoop, Ruthing and Steffen).
    Also returns the down-safe nodes."""
    nodes, succ = [], {}
    for b, blk in p.blocks.items():
        k = len(blk.instrs)
        for i in range(k + 1):
            nodes.append((b, i))
            succ[(b, i)] = [(b, i + 1)] if i < k else [(s, 0) for s in toyir.succs(p, b)]
    pred = {n: [] for n in nodes}
    for n in nodes:
        for s in succ[n]:
            pred[s].append(n)

    def instr(n):
        blk = p.blocks[n[0]]
        return blk.instrs[n[1]] if n[1] < len(blk.instrs) else None

    comp = {n: S.expression(instr(n)) == e for n in nodes}
    kill = {n: instr(n) is not None and instr(n)[1] in e[1:] for n in nodes}
    ant = {n: True for n in nodes}
    changed = True
    while changed:
        changed = False
        for n in reversed(nodes):
            out = bool(succ[n]) and all(ant[s] for s in succ[n])
            new = comp[n] or (out and not kill[n])
            if new != ant[n]:
                ant[n] = new
                changed = True
    av_out = {n: True for n in nodes}
    av_in = {}
    changed = True
    while changed:
        changed = False
        for n in nodes:
            av_in[n] = bool(pred[n]) and all(av_out[q] for q in pred[n])
            new = (ant[n] or av_in[n]) and not kill[n]
            if new != av_out[n]:
                av_out[n] = new
                changed = True
    return {n for n in nodes if ant[n] and not av_in[n]}, ant


# ------------------------------------------------------------------- tests


def test_page_example():
    p = toyir.parse(PAGE_BEFORE)
    q = S.ssapre(p)
    assert toyir.show(q) == PAGE_AFTER
    for args in [(2, 3, 1, 3), (2, 3, 0, 3), (0, 0, 1, 0), (5, -1, 0, 1)]:
        assert toyir.run(q, args) == toyir.run(p, args)
    e = ("+", "a", "b")
    path = ["B0", "B1", "B3", "B3_B3", "B3", "B3_B3", "B3", "B4"]
    assert counts(S.normalize(p), path)[e] == 4 and counts(q, path)[e] == 1
    plans = {e: (phis, reals) for e, phis, reals in S.plan(S.normalize(p))}
    f = plans[e][0]["B3"]
    assert (f.down_safe, f.can_be_avail, f.later, f.will_be_avail) == (True, True, False, True)
    assert sorted((b, o.defn is None, o.real, o.insert) for b, o in f.ops.items()) == [
        ("B1", False, True, False), ("B2", True, False, True), ("B3_B3", False, True, False)]
    # i + 1: the Φ at B3 is down-safe, but no operand is available, so it
    # stays "later" and the addition is not moved.
    g = plans[("+", "i", 1)][0]["B3"]
    assert (g.down_safe, g.can_be_avail, g.later) == (True, True, True)
    # i < n: i changes before the comparison, so the Φ is not down-safe.
    h = plans[("<", "i", "n")][0]["B3"]
    assert (h.down_safe, h.can_be_avail) == (False, False)


def test_same_outcome_on_random_programs():
    for prog in programs(1, 400):
        q = S.ssapre(prog)
        for args in ARGS:
            want = toyir.run(prog, args, FUEL)
            assert want != ("fuel",)
            assert toyir.run(q, args, FUEL) == want


def test_never_more_evaluations_and_optimal_on_every_path():
    better = 0
    for prog in programs(2, 600):
        if not toyir.is_acyclic(prog):
            continue
        p = S.normalize(prog)
        q = S.ssapre(prog)
        assert list(q.blocks) == list(p.blocks)
        exprs = {S.expression(ins) for blk in p.blocks.values() for ins in blk.instrs} - {None}
        best = {e: busy_points(p, e)[0] for e in exprs}
        for path in toyir.paths(p):
            old, new = counts(p, path), counts(q, path)
            assert set(new) <= set(old)
            for e in old:
                opt = sum(1 for (b, _) in best[e] if b in path)
                assert new[e] <= old[e]
                assert new[e] == opt
                better += new[e] < old[e]
    assert better > 50


def test_insertions_are_down_safe():
    inserted = 0
    for prog in programs(3, 400):
        p = S.normalize(prog)
        for e, phis, reals in S.plan(p):
            _, ant = busy_points(p, e)
            for f in phis.values():
                for pred, o in f.ops.items():
                    if o.insert:
                        assert f.down_safe and f.will_be_avail
                        assert ant[(pred, len(p.blocks[pred].instrs))]
                        inserted += 1
    assert inserted > 100


DO_WHILE = """# params: a, b, n
B0:
  i = 0
  jump B1
B1:
  x = a / b
  i = i + 1
  c = i < n
  br c B1 B2
B2:
  ret x
"""

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


def test_loop_invariant_leaves_a_loop_that_runs_once():
    p = toyir.parse(DO_WHILE)
    q = S.ssapre(p)
    assert q.blocks["B0"].instrs[-1] == ("op", "pre.0", "/", "a", "b")
    assert q.blocks["B1"].instrs[0] == ("copy", "x", "pre.0")
    assert toyir.run(q, (7, 2, 3)) == toyir.run(p, (7, 2, 3)) == ("ret", 3)
    assert toyir.run(q, (7, 0, 3)) == ("trap",)


def test_no_hoisting_out_of_a_loop_that_may_not_run():
    p = toyir.parse(ZERO_TRIP)
    q = S.ssapre(p)
    for b, blk in q.blocks.items():
        for ins in blk.instrs:
            if S.expression(ins) == ("/", "a", "b"):
                assert b == "B2"
    assert toyir.run(q, (1, 0, 0)) == ("ret", 0)
    assert toyir.run(q, (1, 0, 2)) == ("trap",)
