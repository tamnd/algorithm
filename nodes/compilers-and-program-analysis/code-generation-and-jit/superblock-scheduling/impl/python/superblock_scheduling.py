# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/superblock-scheduling/. The authors are listed in prov/WWP2JP.jsonl.
"""Superblock formation by tail duplication and superblock scheduling, on
the toy IR.

superblock_schedule(prog, freq) takes a toy IR program with an acyclic
control flow graph and only const, copy and op instructions, and an edge
profile freq (a dict from an edge (a, b) to a count).

Formation. While some block is in no superblock, pick a trace among those
blocks (the block of highest count, grown along edges that are the most
likely way out of one end and the most likely way into the other end). If
some block b_j, j >= 2, of the trace has a predecessor other than b_(j-1),
copy the tail b_j .. b_k and send every such side edge to the copy. Then
the trace has one entry, at its head: it is a superblock. The copies are new
blocks and later get superblocks of their own.

Scheduling. Each superblock is list scheduled as one block. Its only side
paths are side exits, so no compensation code is needed if an operation
moves above a side exit only when it cannot trap and its result is dead on
the exit, and moves below a side exit only under the same two conditions.

The machine: each cycle issues at most `width` items, at most cap[u] of
unit u. A multiply, divide or remainder uses "mul" (latency 3), a branch or
the last terminator "br" (latency 1), and the other operations "alu"
(latency 1). The scheduled superblock runs its items in the order (cycle,
original position), so a dependence with delay 0 lets two items share a
cycle.

Cost: with s instructions and terminators, N names, n items in a
superblock and m superblocks, O(m (s N + n^2)) time besides the Python
list scheduler, which is O(n^3) per superblock. Tail duplication can make s
grow exponentially in the number of blocks in the worst case.
"""

import toyir

MACHINE = {"width": 2, "cap": {"mul": 1, "br": 1}}
LATENCY = {"alu": 1, "mul": 3, "br": 1}


class Item:
    """One item of a superblock: an operation ("op"), a side exit ("br")
    or the terminator of the last block ("end")."""

    def __init__(self, kind, blk, ins=None, term=None, off=None):
        self.kind = kind
        self.blk = blk
        self.ins = ins
        self.term = term
        self.off = off
        if kind == "op":
            self.uses = toyir.uses(ins)
            self.defs = toyir.defs(ins)
        else:
            self.uses = toyir.term_uses(term)
            self.defs = None

    def unit(self):
        if self.kind != "op":
            return "br"
        if self.ins[0] == "op" and self.ins[2] in ("*", "/", "%"):
            return "mul"
        return "alu"

    def latency(self):
        return LATENCY[self.unit()]


def can_trap(ins):
    if ins[0] in ("const", "copy"):
        return False
    if ins[0] != "op":
        return True
    op, b = ins[2], ins[4]
    if op in ("/", "%"):
        return not (isinstance(b, int) and b != 0)
    if op in ("<<", ">>"):
        return not (isinstance(b, int) and 0 <= b <= 63)
    return False


def check_input(prog):
    if not toyir.is_acyclic(prog):
        raise ValueError("superblock scheduling here needs an acyclic CFG")
    for b in prog.blocks.values():
        for ins in b.instrs:
            if ins[0] not in ("const", "copy", "op"):
                raise ValueError("only const, copy and op instructions: %r" % (ins,))


def topological_order(prog):
    order, seen = [], set()
    for root in prog.blocks:
        if root in seen:
            continue
        seen.add(root)
        stack = [(root, iter(toyir.succs(prog, root)))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                order.append(v)
                stack.pop()
            elif w not in seen:
                seen.add(w)
                stack.append((w, iter(toyir.succs(prog, w))))
    order.reverse()
    return order


def liveness(prog):
    """live_in[label]: the names that some path from the start of the block
    reads before it writes them. One backward pass in reverse topological
    order, which is exact on an acyclic graph."""
    live_in = {}
    for lab in reversed(topological_order(prog)):
        b = prog.blocks[lab]
        live = set()
        for s in toyir.succs(prog, lab):
            live |= live_in[s]
        live |= set(toyir.term_uses(b.term))
        for ins in reversed(b.instrs):
            live.discard(toyir.defs(ins))
            live |= set(toyir.uses(ins))
        live_in[lab] = live
    return live_in


# ---------------------------------------------------------------- profiles


def profile(prog, inputs):
    """Edge counts from runs of prog on the inputs (a run that traps
    counts the edges it took before the trap)."""
    freq = {e: 0 for e in toyir.edges(prog)}
    for args in inputs:
        env = dict(zip(prog.params, args))
        lab = prog.entry
        try:
            while True:
                b = prog.blocks[lab]
                for ins in b.instrs:
                    env[ins[1]] = _value(ins, env)
                t = b.term
                if t[0] == "ret":
                    break
                if t[0] == "jump":
                    nxt = t[1]
                else:
                    nxt = t[2] if _operand(t[1], env) != 0 else t[3]
                freq[(lab, nxt)] += 1
                lab = nxt
        except toyir._Trap:
            pass
    return freq


def _operand(a, env):
    return a if isinstance(a, int) else env[a]


def _value(ins, env):
    if ins[0] == "const":
        return ins[2]
    if ins[0] == "copy":
        return _operand(ins[2], env)
    return toyir._binop(ins[2], _operand(ins[3], env), _operand(ins[4], env))


def static_profile(prog):
    """A guess without runs: the entry runs once and each br splits evenly."""
    bf = {lab: 0.0 for lab in prog.blocks}
    bf[prog.entry] = 1.0
    freq = {}
    for lab in topological_order(prog):
        ss = toyir.succs(prog, lab)
        for s in ss:
            freq[(lab, s)] = bf[lab] / len(ss)
            bf[s] += freq[(lab, s)]
    return freq


# ---------------------------------------------------------------- formation


def pick_trace(prog, freq, done):
    """The seed is the block outside every superblock with the highest
    count. The trace grows from its last block a to the most likely
    successor b, and from its first block b to the most likely predecessor
    a, only while a is also the most likely predecessor of b (or b the most
    likely successor of a) and the new block is in no superblock. The entry
    block is always the head of its trace."""
    pr = toyir.preds(prog)
    rank = {lab: i for i, lab in enumerate(prog.blocks)}
    inn = {lab: 0 for lab in prog.blocks}
    out = {lab: 0 for lab in prog.blocks}
    for a, b in toyir.edges(prog):
        out[a] += freq.get((a, b), 0)
        inn[b] += freq.get((a, b), 0)

    def count(lab):
        return max(inn[lab], out[lab])

    def best_succ(a):
        return max(toyir.succs(prog, a), key=lambda b: (freq.get((a, b), 0), -rank[b]), default=None)

    def best_pred(b):
        return max(pr[b], key=lambda a: (freq.get((a, b), 0), -rank[a]), default=None)

    seed = max((lab for lab in prog.blocks if lab not in done), key=lambda lab: (count(lab), -rank[lab]))
    trace = [seed]
    while True:
        b = best_succ(trace[-1])
        if b is None or b in done or b in trace or b == prog.entry or best_pred(b) != trace[-1]:
            break
        trace.append(b)
    while trace[0] != prog.entry:
        a = best_pred(trace[0])
        if a is None or a in done or a in trace or best_succ(a) != trace[0]:
            break
        trace.insert(0, a)
    return trace


def _fresh(taken, base):
    k = 1
    while "%s.%d" % (base, k) in taken:
        k += 1
    lab = "%s.%d" % (base, k)
    taken.add(lab)
    return lab


def _retarget(term, old, new):
    if term[0] == "jump":
        return ("jump", new) if term[1] == old else term
    if term[0] == "br":
        return ("br", term[1], new if term[2] == old else term[2], new if term[3] == old else term[3])
    return term


def tail_duplicate(prog, trace, freq):
    """Copy the trace from its first side entrance to its end and send the
    side entrances to the copy. Returns (new program, new edge counts)."""
    pr = toyir.preds(prog)
    k = len(trace)
    side = [i for i in range(1, k) if any(p != trace[i - 1] for p in pr[trace[i]])]  # @line L4
    if not side:
        return prog, dict(freq)
    j = side[0]
    taken = set(prog.blocks)
    copy_of = {trace[i]: _fresh(taken, trace[i]) for i in range(j, k)}
    blocks = {lab: toyir.Block(list(b.instrs), b.term) for lab, b in prog.blocks.items()}
    for i in range(j, k):  # @line L5
        lab = trace[i]
        term = prog.blocks[lab].term
        # A copy is never the trace predecessor of a tail block, so every
        # edge from a copy into the tail goes to the copy of the target.
        for s in toyir.succs(prog, lab):
            if s in copy_of:
                term = _retarget(term, s, copy_of[s])
        blocks[copy_of[lab]] = toyir.Block(list(prog.blocks[lab].instrs), term)
    for i in range(j, k):
        lab = trace[i]
        for p in pr[lab]:
            if p != trace[i - 1]:
                blocks[p].term = _retarget(blocks[p].term, lab, copy_of[lab])  # @line L6
    new = toyir.Program(list(prog.params), blocks)
    return new, _split_counts(prog, new, trace, j, copy_of, freq)


def _split_counts(prog, new, trace, j, copy_of, freq):
    """Edge counts for the program after tail duplication. The out-counts
    of a tail block are split between it and its copy in the ratio of the
    flow that now enters the copy to the flow that entered the block."""
    orig = {c: lab for lab, c in copy_of.items()}
    pr_old = toyir.preds(prog)
    pr_new = toyir.preds(new)
    ratio = {}

    def weight(a, b):
        a0, b0 = orig.get(a, a), orig.get(b, b)
        w = freq.get((a0, b0), 0)
        if a0 in ratio:
            w = w * ratio[a0] if a in orig else w * (1 - ratio[a0])
        return w

    for i in range(j, len(trace)):
        lab = trace[i]
        total = sum(freq.get((p, lab), 0) for p in pr_old[lab])
        inflow = sum(weight(p, copy_of[lab]) for p in pr_new[copy_of[lab]])
        ratio[lab] = min(1, inflow / total) if total else 0
    return {(a, b): weight(a, b) for a, b in toyir.edges(new)}


def form_superblocks(prog, freq):
    """Returns (program, list of superblocks, edge counts). Each
    superblock is a path of blocks whose only entry is its head."""
    done = set()  # @line L1
    superblocks = []
    while any(lab not in done for lab in prog.blocks):  # @line L2
        trace = pick_trace(prog, freq, done)  # @line L3
        prog, freq = tail_duplicate(prog, trace, freq)
        superblocks.append(trace)  # @line L7
        done |= set(trace)
    return prog, superblocks, freq


# ---------------------------------------------------------------- scheduling


def superblock_items(prog, sb):
    """The items of the superblock in their original order."""
    items = []
    for i, lab in enumerate(sb):
        b = prog.blocks[lab]
        for ins in b.instrs:
            items.append(Item("op", i, ins=ins))
        t = b.term
        if i == len(sb) - 1:
            items.append(Item("end", i, term=t))
        elif t[0] == "br" and t[2] != t[3]:
            off = t[3] if t[2] == sb[i + 1] else t[2]
            items.append(Item("br", i, term=t, off=off))
    return items


def _stays(it, live):
    """An operation must stay on its side of a side exit if it can trap or
    if it writes a name that is live on the exit."""
    return can_trap(it.ins) or it.defs in live


def build_dag(items, live_in):
    """Edges (u, v) -> delay, all with u < v."""
    edges = {}

    def add(u, v, d):
        edges[(u, v)] = max(edges.get((u, v), d), d)

    last_def = {}
    readers = {}
    for v, it in enumerate(items):
        for x in it.uses:
            if x in last_def:
                add(last_def[x], v, items[last_def[x]].latency())
        x = it.defs
        if x is not None:
            if x in last_def:
                add(last_def[x], v, 1)
            for r in readers.get(x, []):
                add(r, v, 0)
        for y in it.uses:
            readers.setdefault(y, []).append(v)
        if x is not None:
            last_def[x] = v
            readers[x] = []
    for b, it in enumerate(items):
        if it.kind != "br":
            continue
        live = live_in[it.off]
        for v in range(b + 1, len(items)):  # @line L11
            w = items[v]
            if w.kind != "op" or _stays(w, live):
                add(b, v, 0)
        for u in range(b):  # @line L12
            w = items[u]
            if w.kind == "op" and _stays(w, live):
                add(u, b, 0)
    end = len(items) - 1
    for u in range(end):
        add(u, end, 0)
    return edges


def heights(items, edges):
    h = [it.latency() for it in items]
    succ = {}
    for (u, v), d in edges.items():
        succ.setdefault(u, []).append((v, d))
    for u in range(len(items) - 1, -1, -1):
        for v, d in succ.get(u, []):
            h[u] = max(h[u], d + h[v])
    return h


def fits(it, used, machine):
    u = it.unit()
    return len(used) < machine["width"] and used.count(u) < machine["cap"].get(u, machine["width"])


def list_schedule(items, edges, machine=MACHINE):
    """Cycle by cycle, start the ready item of greatest height that fits,
    until no ready item fits; then go to the next cycle."""
    n = len(items)
    preds = [[] for _ in range(n)]
    for (u, v), d in edges.items():
        preds[v].append((u, d))
    h = heights(items, edges)
    t = {}
    cyc = 0
    while len(t) < n:
        used = []
        while True:
            ready = [v for v in range(n) if v not in t and all(u in t and t[u] + d <= cyc for u, d in preds[v])]
            ok = [v for v in ready if fits(items[v], used, machine)]
            if not ok:
                break
            v = max(ok, key=lambda v: (h[v], -v))
            t[v] = cyc
            used.append(items[v].unit())
        cyc += 1
    return t


def length(items, t):
    return max(t[v] + items[v].latency() for v in range(len(items)))


def schedule_superblock(prog, sb, machine=MACHINE):
    """Schedule one superblock. Returns (new program, labels of its
    pieces, (items, t))."""
    live_in = liveness(prog)  # @line L9
    items = superblock_items(prog, sb)
    edges = build_dag(items, live_in)  # @line L10
    t = list_schedule(items, edges, machine)  # @line L13
    order = sorted(range(len(items)), key=lambda v: (t[v], v))
    taken = set(prog.blocks)
    head = sb[0]
    pieces = {}
    cur, body = head, []
    for v in order:  # @line L14
        it = items[v]
        if it.kind == "op":
            body.append(it.ins)
        elif it.kind == "br":
            nxt = _fresh(taken, head)
            c = it.term
            term = ("br", c[1], it.off, nxt) if c[2] == it.off else ("br", c[1], nxt, it.off)
            pieces[cur] = toyir.Block(body, term)
            cur, body = nxt, []
        else:
            pieces[cur] = toyir.Block(body, it.term)
    blocks = {}
    for lab, b in prog.blocks.items():
        if lab == head:
            blocks.update(pieces)
        elif lab not in sb:
            blocks[lab] = b
    return toyir.Program(list(prog.params), blocks), list(pieces), (items, t)


def superblock_schedule(prog, freq=None, machine=MACHINE):
    """Form superblocks, then schedule each one. Returns (new program,
    list of superblocks, list of (items, t) for each superblock)."""
    check_input(prog)
    if freq is None:
        freq = static_profile(prog)
    prog, superblocks, _ = form_superblocks(prog, freq)
    log = []
    for sb in superblocks:  # @line L8
        prog, _, sched = schedule_superblock(prog, sb, machine)
        log.append(sched)
    return prog, superblocks, log  # @line L15
