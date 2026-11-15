# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ssa-linear-scan/. The authors are listed in prov/SBG2CF.jsonl.

import random

import pytest

import toyir
from ssa_linear_scan import allocate, block_order, build_intervals, covers, linear_scan, prepare

DIAMOND = """# params: p
entry:
  a = p + 1
  br p L R
L:
  d = a - p
  jump J
R:
  b = p * 2
  c = b + p
  jump J
J:
  e = phi [L: d, R: c]
  ret e
"""


# ------------------------------------------------- SSA construction (Cytron)


def dominator_sets(prog):
    """Dom(v) = {v} + the meet of Dom(p) over the predecessors, by the plain
    fixed point."""
    labels = list(prog.blocks)
    pred = toyir.preds(prog)
    dom = {v: set(labels) for v in labels}
    dom[prog.entry] = {prog.entry}
    changed = True
    while changed:
        changed = False
        for v in labels:
            if v == prog.entry:
                continue
            ps = [dom[p] for p in pred[v]]
            new = {v} | (set.intersection(*ps) if ps else set())
            if new != dom[v]:
                dom[v], changed = new, True
    return dom


def idoms(dom):
    idom = {}
    for v in dom:
        strict = dom[v] - {v}
        for d in strict:
            if strict <= dom[d]:
                idom[v] = d
    return idom


def is_reducible(prog):
    """Reducible if and only if the graph without the edges u -> v with v
    dominating u is acyclic."""
    dom = dominator_sets(prog)
    indeg = {v: 0 for v in prog.blocks}
    fwd = {v: [w for w in toyir.succs(prog, v) if w not in dom[v]] for v in prog.blocks}
    for v in fwd:
        for w in fwd[v]:
            indeg[w] += 1
    work = [v for v in indeg if indeg[v] == 0]
    seen = 0
    while work:
        v = work.pop()
        seen += 1
        for w in fwd[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                work.append(w)
    return seen == len(prog.blocks)


def block_live_in(prog):
    live = {lab: set() for lab in prog.blocks}
    changed = True
    while changed:
        changed = False
        for lab in reversed(list(prog.blocks)):
            b = prog.blocks[lab]
            cur = set(toyir.term_uses(b.term))
            for s in toyir.succs(prog, lab):
                cur |= live[s]
            for ins in reversed(b.instrs):
                cur.discard(ins[1])
                cur |= set(toyir.uses(ins))
            if cur != live[lab]:
                live[lab], changed = cur, True
    return live


def to_ssa(prog):
    """Pruned SSA form: phis at the iterated dominance frontier where the
    name is live, then renaming along the dominator tree."""
    dom = dominator_sets(prog)
    idom = idoms(dom)
    pred = toyir.preds(prog)
    live = block_live_in(prog)
    df = {v: set() for v in prog.blocks}
    for v in prog.blocks:
        if len(pred[v]) >= 2:
            for p in pred[v]:
                r = p
                while r != idom.get(v):
                    df[r].add(v)
                    r = idom[r]
    defsites = {}
    for p in prog.params:
        defsites.setdefault(p, set()).add(prog.entry)
    for lab, b in prog.blocks.items():
        for ins in b.instrs:
            defsites.setdefault(ins[1], set()).add(lab)
    phis = {lab: [] for lab in prog.blocks}
    for x, sites in sorted(defsites.items()):
        work, placed = list(sites), set()
        while work:
            v = work.pop()
            for w in df[v]:
                if w not in placed:
                    placed.add(w)
                    if x in live[w]:
                        phis[w].append(x)
                    if w not in sites:
                        work.append(w)
    children = {v: [] for v in prog.blocks}
    for v, d in idom.items():
        children[d].append(v)
    count, stacks = {}, {p: [p] for p in prog.params}
    blocks, phi_name = {}, {}
    phi_args = {lab: {x: {} for x in phis[lab]} for lab in prog.blocks}

    def new(x):
        count[x] = count.get(x, 0) + 1
        name = "%s.%d" % (x, count[x])
        stacks.setdefault(x, []).append(name)
        return name

    def top(a):
        return stacks[a][-1] if isinstance(a, str) else a

    def walk(v):
        pushed = []
        for x in phis[v]:
            phi_name[(v, x)] = new(x)
            pushed.append(x)
        body = []
        for ins in prog.blocks[v].instrs:
            if ins[0] == "const":
                body.append(("const", None, ins[2]))
            elif ins[0] == "copy":
                body.append(("copy", None, top(ins[2])))
            else:
                body.append(("op", None, ins[2], top(ins[3]), top(ins[4])))
            body[-1] = (body[-1][0], new(ins[1])) + body[-1][2:]
            pushed.append(ins[1])
        t = prog.blocks[v].term
        if t[0] in ("br", "ret"):
            t = (t[0], top(t[1])) + t[2:]
        blocks[v] = (body, t)
        for s in toyir.succs(prog, v):
            for x in phis[s]:
                phi_args[s][x][v] = top(x)
        for c in sorted(children[v], key=list(prog.blocks).index):
            walk(c)
        for x in pushed:
            stacks[x].pop()

    walk(prog.entry)
    out = {}
    for lab in prog.blocks:
        body, t = blocks[lab]
        ph = [("phi", phi_name[(lab, x)], phi_args[lab][x]) for x in phis[lab]]
        out[lab] = toyir.Block(ph + body, t)
    return toyir.Program(list(prog.params), out)


def random_ssa(rng, acyclic):
    """A random reducible program and its SSA form."""
    while True:
        prog = toyir.random_program(rng, rng.randint(2, 6), rng.randint(1, 8), acyclic)
        if is_reducible(prog):
            return prog, to_ssa(prog)


# --------------------------------------------- independent liveness by search


def items_of(prog):
    """(label, kind, j, defs, reads) for the phi group (if any), each other
    instruction and the terminator of each block. A phi operand is read by
    the terminator of its predecessor."""
    items, first = [], {}
    for lab, b in prog.blocks.items():
        first[lab] = len(items)
        ph = [ins for ins in b.instrs if ins[0] == "phi"]
        body = [ins for ins in b.instrs if ins[0] != "phi"]
        if ph:
            items.append((lab, "phi", None, {i[1] for i in ph}, set()))
        for j, ins in enumerate(body):
            items.append((lab, "ins", j, {ins[1]}, set(toyir.uses(ins))))
        reads = set(toyir.term_uses(b.term))
        for s in toyir.succs(prog, lab):
            for ins in prog.blocks[s].instrs:
                if ins[0] == "phi" and isinstance(ins[2][lab], str):
                    reads.add(ins[2][lab])
        items.append((lab, "term", len(body), set(), reads))
    nxt = [[first[s] for s in toyir.succs(prog, it[0])] if it[1] == "term" else [n + 1] for n, it in enumerate(items)]
    return items, nxt


def brute_live_out(prog):
    """For each item, the names live just after it: a name is live if some
    path of items reaches a read of it with no definition before. Slots
    (mem.x) are left out."""
    items, nxt = items_of(prog)
    prv = [[] for _ in items]
    for n, ss in enumerate(nxt):
        for s in ss:
            prv[s].append(n)
    live_in = [set() for _ in items]
    for x in set().union(*(it[4] for it in items)) - {x for it in items for x in it[4] if x.startswith("mem.")}:
        work = [n for n, it in enumerate(items) if x in it[4]]
        seen = set(work)
        while work:
            v = work.pop()
            for p in prv[v]:
                if p not in seen and x not in items[p][3]:
                    seen.add(p)
                    work.append(p)
        for n in seen:
            live_in[n].add(x)
    return items, [set().union(*(live_in[s] for s in nxt[n])) for n in range(len(items))]


def position_after(item, pos, start):
    lab, kind, j = item[0], item[1], item[2]
    return start[lab] + 1 if kind == "phi" else pos[(lab, j)] + 1


# ------------------------------------------------------------------- tests


def check(orig, ssa, k, rng):
    work = prepare(ssa)
    out, reg, spilled = allocate(ssa, k)
    items, live_out = brute_live_out(work)
    for it, o in zip(items, live_out):
        here = [x for x in it[3] | o if x not in spilled and not x.startswith("mem.")]
        assert all(0 <= reg[x] < k for x in here)
        assert len({reg[x] for x in here}) == len(here), (it, here)
    for b in out.blocks.values():
        assert all(ins[0] != "phi" for ins in b.instrs)
    for _ in range(4):
        args = [rng.randint(-6, 6), rng.randint(-6, 6)]
        assert toyir.run(out, args, fuel=200000) == toyir.run(orig, args, fuel=200000)
    return reg, spilled


def test_random_programs_keep_their_outputs():
    rng = random.Random(11)
    spills = 0
    for trial in range(120):
        orig, ssa = random_ssa(rng, acyclic=trial % 2 == 0)
        for k in (1, 2, 3, 4):
            spills += len(check(orig, ssa, k, rng)[1])
    assert spills > 0


def test_intervals_are_exact_liveness():
    rng = random.Random(5)
    for trial in range(150):
        _, ssa = random_ssa(rng, acyclic=trial % 3 == 0)
        work = prepare(ssa)
        order = block_order(work)
        ranges, pos, start, _ = build_intervals(work, order)
        items, live_out = brute_live_out(work)
        for it, o in zip(items, live_out):
            p = position_after(it, pos, start)
            expect = set(o)
            if it[1] == "term":
                # The phi operands stay live to the end of the block, where
                # the parallel copy reads them.
                for s in toyir.succs(work, it[0]):
                    for ins in work.blocks[s].instrs:
                        if ins[0] == "phi" and isinstance(ins[2][it[0]], str):
                            expect.add(ins[2][it[0]])
            assert {x for x in ranges if covers(ranges[x], p)} == expect, (it, expect)
        # Every definition is inside the interval of its name.
        for it in items:
            for y in it[3]:
                q = start[it[0]] if it[1] == "phi" else pos[(it[0], it[2])]
                assert covers(ranges[y], q)


def test_block_order_respects_dominance_and_loops():
    rng = random.Random(9)
    for trial in range(150):
        _, ssa = random_ssa(rng, acyclic=False)
        work = prepare(ssa)
        order = block_order(work)
        assert sorted(order) == sorted(work.blocks)
        at = {v: i for i, v in enumerate(order)}
        dom = dominator_sets(work)
        for v in order:
            assert all(at[d] <= at[v] for d in dom[v])
        # The loop of a header is the union of the natural loops of its back edges.
        pred = toyir.preds(work)
        loops = {}
        for u in work.blocks:
            for h in toyir.succs(work, u):
                if h in dom[u]:
                    loop, stack = loops.setdefault(h, {h}), [u]
                    while stack:
                        v = stack.pop()
                        if v not in loop:
                            loop.add(v)
                            stack.extend(pred[v])
        for h, loop in loops.items():
            spots = sorted(at[v] for v in loop)
            assert spots == list(range(spots[0], spots[0] + len(spots)))
            assert order[spots[0]] == h


def test_no_spill_and_max_live_registers_when_pressure_fits():
    rng = random.Random(3)
    for trial in range(150):
        orig, ssa = random_ssa(rng, acyclic=trial % 2 == 1)
        items, live_out = brute_live_out(prepare(ssa))
        m = max(len(it[3] | o) for it, o in zip(items, live_out))
        for k in (m, m + 1):
            reg, spilled = check(orig, ssa, k, rng)
            assert not spilled
            assert len(set(reg.values())) == m


def test_irreducible_graph_is_rejected():
    text = """# params: p
A:
  br p B C
B:
  x = p + 1
  jump C
C:
  y = p + 2
  br y B D
D:
  ret p
"""
    prog = toyir.parse(text)
    assert not is_reducible(prog)
    with pytest.raises(ValueError):
        allocate(prog, 2)


def test_diamond_hole_saves_a_register():
    prog = toyir.parse(DIAMOND)
    work = prepare(prog)
    order = block_order(work)
    assert order == ["start", "entry", "R", "L", "J"]
    ranges, pos, start, end = build_intervals(work, order)
    assert ranges["a"] == [[8, 12], [20, 22]]
    assert ranges["p"] == [[2, 16], [20, 22]]
    # The interval of a has a hole over R, where b and c live.
    hull = {x: (r[0][0], r[-1][1]) for x, r in ranges.items()}
    overlap = max(sum(1 for a, e in hull.values() if a <= q < e) for q in range(end["J"]))
    assert overlap == 3
    out, reg, spilled = allocate(prog, 2)
    assert not spilled
    assert reg == {"p": 0, "a": 1, "b": 1, "c": 0, "d": 0, "e": 0}
    for p in range(-3, 4):
        assert toyir.run(out, [p]) == toyir.run(prog, [p])


def test_scan_spills_furthest_end():
    ranges = {"x": [[0, 20]], "y": [[1, 5]], "z": [[2, 4]]}
    reg, spilled = linear_scan(ranges, 2)
    assert spilled == {"x"}
    assert reg == {"y": 1, "z": 0}


def test_inactive_interval_never_meets_current():
    # In strict SSA with a dominance order, an earlier interval in a hole at
    # the start of cur never meets cur, so the inactive test is never needed.
    rng = random.Random(5)
    pairs = 0
    for trial in range(150):
        _, ssa = random_ssa(rng, acyclic=trial % 2 == 0)
        work = prepare(ssa)
        ranges = build_intervals(work, block_order(work))[0]
        cells = {x: {q for a, e in r for q in range(a, e)} for x, r in ranges.items()}
        names = sorted(ranges, key=lambda x: (ranges[x][0][0], x))
        for i, cur in enumerate(names):
            p = ranges[cur][0][0]
            for x in names[:i]:
                if max(cells[x]) >= p and p not in cells[x]:
                    pairs += 1
                    assert not cells[x] & cells[cur]
    assert pairs > 100
