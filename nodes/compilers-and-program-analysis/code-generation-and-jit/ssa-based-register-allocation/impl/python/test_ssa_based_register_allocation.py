# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ssa-based-register-allocation/. The authors are listed in prov/C6A8K4.jsonl.

import random

import toyir
from ssa_based_register_allocation import allocate, is_mem, max_live, prepare, sequentialize

LOOP = """# params: n
entry:
  i0 = 0
  a0 = 0
  jump head
head:
  i1 = phi [entry: i0, body: i2]
  a1 = phi [entry: a0, body: a2]
  t = i1 < n
  br t body done
body:
  u = i1 * i1
  a2 = a1 + u
  i2 = i1 + 1
  jump head
done:
  ret a1
"""


# ------------------------------------------------- SSA construction (Cytron)


def dominators(prog):
    """Dominator sets by the plain fixed point: Dom(v) = {v} + meet of Dom(p)."""
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
    idom = {}
    for v in labels:
        strict = dom[v] - {v}
        for d in strict:
            if strict <= dom[d]:
                idom[v] = d
    return dom, idom


def block_live_in(prog):
    """Live-in names of each block of a program without phis."""
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
    """Pruned SSA form (phis at the iterated dominance frontier where the
    name is live, then renaming along the dominator tree). The parameters
    keep their names."""
    dom, idom = dominators(prog)
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
    count = {}
    stacks = {p: [p] for p in prog.params}
    blocks = {}
    phi_args = {lab: {x: {} for x in phis[lab]} for lab in prog.blocks}
    phi_name = {}

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


def random_ssa(rng, nvars, nblocks, acyclic):
    prog = toyir.random_program(rng, nvars, nblocks, acyclic)
    return prog, to_ssa(prog)


# --------------------------------------------- independent checks on output


def item_graph(prog):
    """Nodes: one phi group per block with phis, each instruction, each
    terminator. A phi operand is read by the terminator of its predecessor."""
    items, first = [], {}
    for lab, b in prog.blocks.items():
        first[lab] = len(items)
        ph = [ins for ins in b.instrs if ins[0] == "phi"]
        if ph:
            items.append((lab, "phi", set(i[1] for i in ph), set()))
        for ins in b.instrs:
            if ins[0] != "phi":
                items.append((lab, "ins", {ins[1]}, set(toyir.uses(ins))))
        reads = set(toyir.term_uses(b.term))
        for s in toyir.succs(prog, lab):
            for ins in prog.blocks[s].instrs:
                if ins[0] == "phi" and isinstance(ins[2][lab], str):
                    reads.add(ins[2][lab])
        items.append((lab, "term", set(), reads))
    nxt = []
    for n, (lab, kind, _, _) in enumerate(items):
        nxt.append([first[s] for s in toyir.succs(prog, lab)] if kind == "term" else [n + 1])
    return items, nxt


def brute_live_out(prog):
    items, nxt = item_graph(prog)
    prv = [[] for _ in items]
    for n, ss in enumerate(nxt):
        for s in ss:
            prv[s].append(n)
    names = set().union(*(u for _, _, _, u in items))
    live_in = [set() for _ in items]
    for x in names:
        work = [n for n, it in enumerate(items) if x in it[3]]
        seen = set(work)
        while work:
            v = work.pop()
            for p in prv[v]:
                if p not in seen and x not in items[p][2]:
                    seen.add(p)
                    work.append(p)
        for n in seen:
            live_in[n].add(x)
    out = [set().union(*(live_in[s] for s in nxt[n])) for n in range(len(items))]
    return items, out


def interference(prog):
    items, out = brute_live_out(prog)
    adj = {}
    for _, _, d, _ in items:
        for x in d:
            adj.setdefault(x, set())
    points = []
    for n, (_, _, d, _) in enumerate(items):
        here = {x for x in d | out[n] if not is_mem(x)}
        points.append(here)
        for x in d:
            for y in here:
                if x != y and not is_mem(x):
                    adj.setdefault(x, set()).add(y)
                    adj.setdefault(y, set()).add(x)
    return {x: v for x, v in adj.items() if not is_mem(x)}, points


def is_chordal(adj):
    """Maximum cardinality search, then a check that its reverse order is a
    perfect elimination ordering."""
    weight = {v: 0 for v in adj}
    order, done = [], set()
    while len(order) < len(adj):
        v = max((u for u in adj if u not in done), key=lambda u: (weight[u], u))
        order.append(v)
        done.add(v)
        for w in adj[v]:
            if w not in done:
                weight[w] += 1
    pos = {v: i for i, v in enumerate(order)}
    for v in adj:
        earlier = [w for w in adj[v] if pos[w] < pos[v]]
        if earlier:
            parent = max(earlier, key=pos.__getitem__)
            if any(w != parent and w not in adj[parent] for w in earlier):
                return False
    return True


def chromatic(adj):
    nodes = sorted(adj, key=lambda v: -len(adj[v]))
    for k in range(len(nodes) + 1):
        col = {}

        def go(i):
            if i == len(nodes):
                return True
            v = nodes[i]
            used = {col[w] for w in adj[v] if w in col}
            for c in range(k):
                if c not in used:
                    col[v] = c
                    if go(i + 1):
                        return True
                    del col[v]
            return False

        if go(0):
            return k
    return len(nodes)


def clique_number(adj):
    best = 0

    def grow(clique, cand):
        nonlocal best
        best = max(best, len(clique))
        for v in sorted(cand):
            grow(clique | {v}, {w for w in cand if w > v and w in adj[v]})

    grow(set(), set(adj))
    return best


# ------------------------------------------------------------------- tests


def check(orig, ssa, k, rng):
    work = prepare(ssa)
    out, col, spilled = allocate(ssa, k)
    adj, points = interference(work)
    for x in adj:
        assert (x in col) != (x in spilled), x
    for x in col:
        assert 0 <= col[x] < k
        for y in adj[x]:
            if y in col:
                assert col[x] != col[y], (x, y)
    for here in points:
        assert len(here - spilled) <= k
    for b in out.blocks.values():
        assert all(ins[0] != "phi" for ins in b.instrs)
    for _ in range(4):
        args = [rng.randint(-6, 6), rng.randint(-6, 6)]
        assert toyir.run(out, args, fuel=200000) == toyir.run(orig, args, fuel=200000)
    return adj, points, col, spilled


def test_random_programs_keep_their_outputs():
    rng = random.Random(7)
    spills = 0
    for trial in range(150):
        orig, ssa = random_ssa(rng, rng.randint(2, 6), rng.randint(1, 7), acyclic=trial % 2 == 0)
        for k in (1, 2, 3, 4):
            _, _, _, spilled = check(orig, ssa, k, rng)
            spills += len(spilled)
    assert spills > 0


def test_max_live_colors_when_pressure_fits():
    rng = random.Random(21)
    tested = 0
    for trial in range(150):
        orig, ssa = random_ssa(rng, rng.randint(2, 5), rng.randint(1, 6), acyclic=trial % 2 == 1)
        work = prepare(ssa)
        adj, points = interference(work)
        m = max(len(p) for p in points)
        assert m == max_live(work)
        assert is_chordal(adj)
        for k in range(m, m + 2):
            _, _, col, spilled = check(orig, ssa, k, rng)
            assert not spilled
            assert len(set(col.values())) == m
        if len(adj) <= 14:
            assert clique_number(adj) == chromatic(adj) == m
            tested += 1
    assert tested > 50


def test_not_chordal_after_leaving_ssa():
    # The loop of the interference graph page: several definitions of d.
    text = """# params: n
L0:
  d = n
  jump L1
L1:
  a = d + 1
  b = a + d
  c = a + 1
  d = b - c
  d = d % c
  br d L1 L2
L2:
  ret d
"""
    prog = toyir.parse(text)
    items, out = brute_live_out(prog)
    adj = {}
    for n, (_, _, d, _) in enumerate(items):
        for x in d:
            for y in out[n]:
                src = None
                if items[n][1] == "ins":
                    ins = [i for i in prog.blocks[items[n][0]].instrs if i[1] == x]
                    src = ins[0][2] if ins and ins[0][0] == "copy" else None
                if x != y and y != src:
                    adj.setdefault(x, set()).add(y)
                    adj.setdefault(y, set()).add(x)
    assert {x: adj[x] for x in "abcd"} == {"a": {"b", "d"}, "b": {"a", "c"}, "c": {"b", "d"}, "d": {"a", "c"}}
    assert not is_chordal({x: adj[x] for x in "abcd"})


def test_loop_example():
    prog = toyir.parse(LOOP)
    work = prepare(prog)
    assert max_live(work) == 4
    out, col, spilled = allocate(prog, 4)
    assert not spilled
    assert col == {"n": 0, "i0": 1, "a0": 2, "i1": 1, "a1": 2, "t": 3, "u": 3, "a2": 2, "i2": 1}
    # The bias puts each phi and its operands in one register, so no copy is left.
    assert [ins for b in out.blocks.values() for ins in b.instrs if ins[0] == "copy"] == [("copy", "r0", "mem.n")]
    out3, _, spilled3 = allocate(prog, 3)
    assert spilled3 == {"n"}
    out2, _, spilled2 = allocate(prog, 2)
    assert spilled2 == {"n", "t", "u"}
    for n in range(-2, 8):
        expect = toyir.run(prog, [n])
        assert toyir.run(out, [n]) == toyir.run(out3, [n]) == toyir.run(out2, [n]) == expect
        assert expect == ("ret", sum(i * i for i in range(max(n, 0))))


def test_sequentialize_parallel_copies():
    rng = random.Random(4)
    locs = ["r0", "r1", "r2", "r3", "mem.a", "mem.b"]
    for _ in range(3000):
        dsts = rng.sample(locs, rng.randint(1, len(locs)))
        moves = [(d, rng.choice(locs + [rng.randint(0, 9)])) for d in dsts]
        state = {x: i + 100 for i, x in enumerate(locs)}
        expect = dict(state)
        for d, s in moves:
            expect[d] = s if isinstance(s, int) else state[s]
        for ins in sequentialize(moves):
            state[ins[1]] = ins[2] if ins[0] == "const" else state[ins[2]]
        assert all(state[x] == expect[x] for x in locs)


def test_swap_needs_s0():
    seq = sequentialize([("r0", "r1"), ("r1", "r0")])
    assert seq == [("copy", "s0", "r0"), ("copy", "r0", "r1"), ("copy", "r1", "s0")]
    # A chain needs no scratch register: r2 is read before it is written.
    assert sequentialize([("r1", "r2"), ("r2", "r3")]) == [("copy", "r1", "r2"), ("copy", "r2", "r3")]
