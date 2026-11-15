# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/worklist-dataflow-algorithm/. The authors are listed in prov/5353DC.jsonl.

import random

import toyir
from toyir import defs, parse, paths, preds, random_program, succs, term_uses, uses
from worklist_dataflow_algorithm import (
    ANALYSES,
    NAC,
    TOP,
    available_expressions,
    constant_propagation,
    live_variables,
    reaching_definitions,
    solve,
    very_busy_expressions,
)

EX = """
# params: n, x
entry:
  i = 0
  s = 0
  jump head
head:
  t = i < n
  br t body done
body:
  a = x * 2
  u = i & 1
  br u odd next
odd:
  s = s + a
  jump next
next:
  i = i + 1
  jump head
done:
  ret s
"""

DIAMOND = """
# params: c
entry:
  br c left right
left:
  x = 2
  y = 3
  jump join
right:
  x = 3
  y = 2
  jump join
join:
  z = x + y
  ret z
"""

GENKILL = ["reaching-definitions", "live-variables", "available-expressions", "very-busy-expressions"]


def exits(prog):
    return [n for n in prog.blocks if prog.blocks[n].term[0] == "ret"]


# ------------------------------------------------------------ reference: MOP


def mop(prog, an, inclusive=False):
    """Meet over all paths by enumeration on an acyclic CFG, in CFG terms
    (IN for a forward problem, OUT for a backward one). With inclusive=True
    the paths also run through the block itself (OUT for a forward problem,
    IN for a backward one)."""
    res = {n: an.top for n in prog.blocks}
    j = 1 if inclusive else 0
    for p in paths(prog):
        for k in range(len(p)):
            if an.forward:
                head, rest = p[k], p[:k + j]
            else:
                head, rest = p[k], list(reversed(p[k + 1 - j:]))
            v = an.boundary
            for b in rest:
                v = an.transfer(b, v)
            res[head] = an.meet(res[head], v)
    return res


def walk_facts(prog, labels, kind, exprs):
    """The fact of one path, by the meaning of the problem, without gen and
    kill sets. labels are the blocks, in program order, that the path runs
    through after (forward) or before (backward) the point."""
    events = []
    for b in labels:
        blk = prog.blocks[b]
        for i, ins in enumerate(blk.instrs):
            events += [("use", a) for a in uses(ins)]
            if ins[0] == "op":
                events.append(("eval", ins[2:]))
            events.append(("def", defs(ins), (b, i)))
        events += [("use", a) for a in term_uses(blk.term)]
    if kind == "reaching-definitions":
        last = {}
        for e in events:
            if e[0] == "def":
                last[e[1]] = e[2]
        return frozenset(last.values())
    if kind == "available-expressions":
        avail = set()
        for e in events:
            if e[0] == "eval":
                avail.add(e[1])
            elif e[0] == "def":
                avail = {f for f in avail if e[1] not in (f[1], f[2])}
        return frozenset(avail)
    if kind == "live-variables":
        live, written = set(), set()
        for e in events:
            if e[0] == "use" and e[1] not in written:
                live.add(e[1])
            elif e[0] == "def":
                written.add(e[1])
        return frozenset(live)
    busy, dead = set(), set()
    for e in events:
        if e[0] == "eval" and e[1] not in dead:
            busy.add(e[1])
        elif e[0] == "def":
            dead |= {f for f in exprs if e[1] in (f[1], f[2]) and f not in busy}
    return frozenset(busy)


def by_meaning(prog, kind):
    an = ANALYSES[kind](prog)
    exprs = an.universe
    res = {n: an.top for n in prog.blocks}
    for p in paths(prog):
        for k in range(len(p)):
            labels = p[:k] if an.forward else p[k + 1:]
            res[p[k]] = an.meet(res[p[k]], walk_facts(prog, labels, kind, exprs))
    return res


# ------------------------------------------------- reference: round robin


def round_robin(prog, an):
    """Kleene iteration from top over all blocks until nothing changes."""
    nodes = list(prog.blocks)
    p = preds(prog)
    ins = {n: an.top for n in nodes}
    changed = True
    while changed:
        changed = False
        for n in nodes:
            if an.forward:
                v = an.boundary if n == prog.entry else an.top
                for q in p[n]:
                    v = an.meet(v, an.transfer(q, ins[q]))
            else:
                v = an.boundary if prog.blocks[n].term[0] == "ret" else an.top
                for q in succs(prog, n):
                    v = an.meet(v, an.transfer(q, ins[q]))
            if v != ins[n]:
                ins[n] = v
                changed = True
    return ins


def check_fixed_point(prog, an, IN, OUT):
    p = preds(prog)
    for n in prog.blocks:
        if an.forward:
            v = an.boundary if n == prog.entry else an.top
            for q in p[n]:
                v = an.meet(v, OUT[q])
            assert IN[n] == v and OUT[n] == an.transfer(n, IN[n])
        else:
            v = an.boundary if prog.blocks[n].term[0] == "ret" else an.top
            for q in succs(prog, n):
                v = an.meet(v, IN[q])
            assert OUT[n] == v and IN[n] == an.transfer(n, OUT[n])


# --------------------------------------------- reference: concrete runs


def trace(prog, args, fuel=2000):
    """Run prog and record events: ("enter", L, env), ("use", x),
    ("eval", e) and ("def", x, (L, i)). Returns (events, outcome)."""
    env = dict(zip(prog.params, args))
    events = []
    label = prog.entry
    try:
        while True:
            events.append(("enter", label, dict(env)))
            blk = prog.blocks[label]
            for i, ins in enumerate(blk.instrs):
                fuel -= 1
                if fuel < 0:
                    return events, "fuel"
                events += [("use", a) for a in uses(ins)]
                def val(a):
                    return a if isinstance(a, int) else env[a]

                if ins[0] == "const":
                    env[ins[1]] = ins[2]
                elif ins[0] == "copy":
                    env[ins[1]] = val(ins[2])
                else:
                    events.append(("eval", ins[2:]))
                    env[ins[1]] = toyir._binop(ins[2], val(ins[3]), val(ins[4]))
                events.append(("def", ins[1], (label, i)))
            events += [("use", a) for a in term_uses(blk.term)]
            t = blk.term
            if t[0] == "ret":
                return events, "ret"
            if t[0] == "jump":
                label = t[1]
            else:
                c = t[1] if isinstance(t[1], int) else env[t[1]]
                label = t[2] if c != 0 else t[3]
    except toyir._Trap:
        return events, "trap"


def check_runs(prog, results, rng):
    IN = {k: results[k][0] for k in results}
    cp = constant_propagation(prog)
    for _ in range(12):
        args = [rng.randint(-5, 9) for _ in prog.params]
        events, outcome = trace(prog, args)
        last, avail = {}, set()
        for e in events:
            if e[0] == "enter":
                assert set(last.values()) <= IN["reaching-definitions"][e[1]]
                assert IN["available-expressions"][e[1]] <= avail
                for x, v in zip(cp.vars, IN["constant-propagation"][e[1]]):
                    if v == TOP:
                        assert x not in e[2]
                    elif v != NAC:
                        assert e[2].get(x, v) == v
            elif e[0] == "eval":
                avail.add(e[1])
            elif e[0] == "def":
                last[e[1]] = e[2]
                avail = {f for f in avail if e[1] not in (f[1], f[2])}
        live, busy = set(), set()
        exprs = ANALYSES["very-busy-expressions"](prog).universe
        for e in reversed(events):
            if e[0] == "enter":
                assert live <= IN["live-variables"][e[1]]
                if outcome == "ret":
                    assert IN["very-busy-expressions"][e[1]] <= busy
            elif e[0] == "use":
                live.add(e[1])
            elif e[0] == "eval":
                busy.add(e[1])
            elif e[0] == "def":
                live.discard(e[1])
                busy -= {f for f in exprs if e[1] in (f[1], f[2])}


# --------------------------------------------------------------- the tests


def show_set(v):
    out = []
    for e in v:
        if isinstance(e, str):
            out.append(e)
        elif isinstance(e[1], int):
            out.append("%s%d" % e)
        else:
            out.append("%s %s %s" % (e[1], e[0], e[2]))
    return sorted(out)


def test_running_example() -> None:
    prog = parse(EX)
    IN, OUT, st = solve(prog, live_variables(prog))
    assert show_set(IN["entry"]) == ["n", "x"]
    assert show_set(OUT["body"]) == ["a", "i", "n", "s", "x"]
    assert show_set(IN["done"]) == ["s"]
    assert st == {"transfers": 11, "meets": 13, "changes": 11, "max_changes": 3}
    IN, OUT, st = solve(prog, reaching_definitions(prog))
    assert show_set(IN["head"]) == ["body0", "body1", "entry0", "entry1", "head0", "next0", "odd0"]
    assert show_set(OUT["next"]) == ["body0", "body1", "entry1", "head0", "next0", "odd0"]
    assert st["transfers"] == 11
    IN, OUT, st = solve(prog, available_expressions(prog))
    assert show_set(IN["head"]) == []
    assert show_set(IN["next"]) == ["i & 1", "i < n", "x * 2"]
    assert show_set(IN["done"]) == ["i < n"]
    assert st["transfers"] == 6
    IN, OUT, st = solve(prog, very_busy_expressions(prog))
    assert show_set(IN["body"]) == ["i & 1", "i + 1", "x * 2"]
    assert show_set(OUT["entry"]) == ["i < n"]
    assert show_set(OUT["head"]) == []
    assert st["transfers"] == 6


def test_constant_propagation_is_not_distributive() -> None:
    prog = parse(DIAMOND)
    an = constant_propagation(prog)
    IN, OUT, _ = solve(prog, an)
    z = an.index["z"]
    assert IN["join"][an.index["x"]] == NAC
    assert OUT["join"][z] == NAC
    assert mop(prog, an, inclusive=True)["join"][z] == 5
    left, right = OUT["left"], OUT["right"]
    assert an.transfer("join", left)[z] == 5 and an.transfer("join", right)[z] == 5
    assert an.meet(an.transfer("join", left), an.transfer("join", right))[z] == 5
    assert an.transfer("join", an.meet(left, right))[z] == NAC


def test_genkill_composition_and_distributivity() -> None:
    rng = random.Random(7)
    for _ in range(40):
        prog = random_program(rng, 4, rng.randint(2, 7), acyclic=rng.random() < 0.5)
        for kind in GENKILL:
            an = ANALYSES[kind](prog)
            universe = sorted(an.universe, key=repr)
            for label, b in prog.blocks.items():
                x = frozenset(e for e in universe if rng.random() < 0.5)
                y = frozenset(e for e in universe if rng.random() < 0.5)
                items = [(i, ins) for i, ins in enumerate(b.instrs)] + [(len(b.instrs), None)]
                if not an.forward:
                    items.reverse()
                v = x
                for i, ins in items:
                    g, k = an.step(label, i, ins)
                    v = frozenset(g) | (v - frozenset(k))
                assert an.transfer(label, x) == v
                assert an.transfer(label, an.meet(x, y)) == an.meet(an.transfer(label, x), an.transfer(label, y))


def acyclic_cases(seed, count):
    """MFP against MOP on random acyclic programs. Gen-kill problems must
    agree exactly; constant propagation must be below MOP. Returns the
    number of blocks where constant propagation is strictly below MOP."""
    rng = random.Random(seed)
    strict = 0
    for _ in range(count):
        prog = random_program(rng, 4, rng.randint(2, 8), acyclic=True)
        for kind in GENKILL:
            an = ANALYSES[kind](prog)
            IN, OUT, _ = solve(prog, an)
            mfp, mfp2 = (IN, OUT) if an.forward else (OUT, IN)
            assert mfp == mop(prog, an)
            assert mfp2 == mop(prog, an, inclusive=True)
            assert mfp == by_meaning(prog, kind)
        an = constant_propagation(prog)
        IN, OUT, _ = solve(prog, an)
        m, m2 = mop(prog, an), mop(prog, an, inclusive=True)
        for n in prog.blocks:
            assert an.leq(IN[n], m[n]) and an.leq(OUT[n], m2[n])
            strict += OUT[n] != m2[n]
    return strict


def test_acyclic_mfp_equals_mop() -> None:
    # 400 programs; constant propagation is strictly below MOP at 19 blocks.
    assert acyclic_cases(2024, 400) == 19


def test_constant_propagation_below_mop_on_diamonds() -> None:
    rng = random.Random(99)
    strict = 0
    for _ in range(100):
        a, b = rng.randint(0, 4), rng.randint(0, 4)
        text = DIAMOND.replace("x = 2", "x = A").replace("y = 3", "y = B")
        text = text.replace("x = 3", "x = B").replace("y = 2", "y = A")
        prog = parse(text.replace("A", str(a)).replace("B", str(b)))
        an = constant_propagation(prog)
        IN, OUT, _ = solve(prog, an)
        mo = mop(prog, an, inclusive=True)["join"]
        assert an.leq(OUT["join"], mo)
        assert mo[an.index["z"]] == a + b
        strict += OUT["join"] != mo
        assert (OUT["join"][an.index["z"]] == NAC) == (a != b)
        assert (OUT["join"] != mo) == (a != b)
    assert strict == 85


def test_cyclic_fixed_point_bounds_and_runs() -> None:
    rng = random.Random(31337)
    for _ in range(300):
        prog = random_program(rng, 4, rng.randint(3, 8), acyclic=False)
        nblocks = len(prog.blocks)
        nedges = len(toyir.edges(prog))
        results = {}
        for kind, mk in ANALYSES.items():
            an = mk(prog)
            IN, OUT, st = solve(prog, an)
            check_fixed_point(prog, an, IN, OUT)
            assert round_robin(prog, an) == (IN if an.forward else OUT)
            assert st["max_changes"] <= an.height
            assert st["transfers"] <= nblocks + st["changes"]
            assert st["meets"] <= (an.height + 1) * nedges
            results[kind] = (IN, OUT)
        check_runs(prog, results, rng)


def test_exits_and_boundary() -> None:
    prog = parse(EX)
    assert exits(prog) == ["done"]
    an = available_expressions(prog)
    assert an.boundary == frozenset() and an.top == an.universe
    IN, _, _ = solve(prog, an)
    assert IN["entry"] == frozenset()
