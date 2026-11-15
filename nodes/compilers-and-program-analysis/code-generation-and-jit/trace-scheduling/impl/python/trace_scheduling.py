# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trace-scheduling/. The authors are listed in prov/5GWXK6.jsonl.
"""Trace scheduling after Fisher, on the toy IR.

trace_schedule(prog, freq) takes a toy IR program with an acyclic control
flow graph and only const, copy and op instructions, and an edge profile
freq (a dict from an edge (a, b) to a count). While some block is not
scheduled, it

1. picks a trace: the unscheduled block of highest count, grown forward and
   backward along edges that are the most likely way out of one end and the
   most likely way into the other end;
2. builds the dependence DAG of the items of the trace (its operations, its
   side exits and its side entrances) and list schedules it as one block;
3. puts copies of the operations that moved below a side exit on the
   off-trace edge of that exit, and copies of the operations that moved
   above a side entrance on the edges that enter there;
4. cuts the scheduled trace into blocks and marks them scheduled.

The compensation blocks are new unscheduled blocks, so later traces
schedule them too.

The machine: each cycle issues at most `width` items, at most cap[u] of
unit u. The unit of a multiply, divide or remainder is "mul" (latency 3),
of a branch or of the last terminator "br" (latency 1), and of the other
operations "alu" (latency 1). An entrance is a mark that takes no slot.
The scheduled trace runs its items in the order (cycle, original
position), so a dependence with delay 0 lets two items share a cycle.

Code motion rules. An operation may move below a side exit; it is copied
onto the off-trace edge. An operation may move above a side exit only if it
cannot trap and its result is dead on the off-trace edge. No operation moves
below a side entrance: entrances and branches keep their order. An
operation may move above a side entrance; it is copied onto the side edges.
"""

import toyir

MACHINE = {"width": 2, "cap": {"mul": 1, "br": 1}}
LATENCY = {"alu": 1, "mul": 3, "br": 1, "join": 0}


class Item:
    """One item of a trace: an operation ("op"), a side exit ("br"), a
    side entrance ("join") or the terminator of the last block ("end")."""

    def __init__(self, kind, blk, ins=None, term=None, label=None, off=None):
        self.kind = kind
        self.blk = blk
        self.ins = ins
        self.term = term
        self.label = label
        self.off = off
        if kind == "op":
            self.uses = toyir.uses(ins)
            self.defs = toyir.defs(ins)
        elif kind in ("br", "end"):
            self.uses = toyir.term_uses(term)
            self.defs = None
        else:
            self.uses = []
            self.defs = None

    def unit(self):
        if self.kind in ("br", "end"):
            return "br"
        if self.kind == "join":
            return "join"
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
        raise ValueError("trace scheduling here needs an acyclic CFG")
    for b in prog.blocks.values():
        for ins in b.instrs:
            if ins[0] not in ("const", "copy", "op"):
                raise ValueError("only const, copy and op instructions: %r" % (ins,))


def liveness(prog):
    """live_in[label]: the names read before any write on some path."""
    live_in = {lab: set() for lab in prog.blocks}
    changed = True
    while changed:
        changed = False
        for lab in reversed(list(prog.blocks)):
            b = prog.blocks[lab]
            live = set()
            for s in toyir.succs(prog, lab):
                live |= live_in[s]
            live |= set(toyir.term_uses(b.term))
            for ins in reversed(b.instrs):
                live.discard(toyir.defs(ins))
                live |= set(toyir.uses(ins))
            if live != live_in[lab]:
                live_in[lab] = live
                changed = True
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
    order = []
    seen = set()

    def visit(lab):
        seen.add(lab)
        for s in toyir.succs(prog, lab):
            if s not in seen:
                visit(s)
        order.append(lab)

    visit(prog.entry)
    order.reverse()
    bf = {lab: 0.0 for lab in prog.blocks}
    bf[prog.entry] = 1.0
    freq = {}
    for lab in order:
        ss = toyir.succs(prog, lab)
        for s in ss:
            freq[(lab, s)] = bf[lab] / len(ss)
            bf[s] += freq[(lab, s)]
    return freq


# ---------------------------------------------------------- trace selection


def pick_trace(prog, freq, done):
    """The seed is the unscheduled block with the highest count. The trace
    grows from its last block a to the most likely successor b, and from its
    first block b to the most likely predecessor a, only while a is also the
    most likely predecessor of b (or b the most likely successor of a) and
    the new block is not scheduled. The entry block is always the head of
    its trace, so the entry label stays the entry."""
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
        if b is None or b in done or b in trace or best_pred(b) != trace[-1]:
            break
        trace.append(b)
    while trace[0] != prog.entry:
        a = best_pred(trace[0])
        if a is None or a in done or a in trace or best_succ(a) != trace[0]:
            break
        trace.insert(0, a)
    return trace


# ------------------------------------------------------------ the DAG


def trace_items(prog, trace):
    """The items of the trace in their original order."""
    pr = toyir.preds(prog)
    items = []
    for i, lab in enumerate(trace):
        b = prog.blocks[lab]
        if i > 0 and any(p != trace[i - 1] for p in pr[lab]):
            items.append(Item("join", i, label=lab))
        for ins in b.instrs:
            items.append(Item("op", i, ins=ins))
        t = b.term
        if i == len(trace) - 1:
            items.append(Item("end", i, term=t))
        elif t[0] == "br" and t[2] != t[3]:
            off = t[3] if t[2] == trace[i + 1] else t[2]
            items.append(Item("br", i, term=t, off=off))
    return items


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
        if it.kind == "br":  # @line L5
            for v in range(b + 1, len(items)):
                w = items[v]
                if w.kind in ("br", "end"):
                    add(b, v, 0)
                elif w.kind == "op" and (can_trap(w.ins) or w.defs in live_in[it.off]):
                    add(b, v, 0)
        elif it.kind == "join":  # @line L6
            for u in range(b):
                add(u, b, 0)
            for v in range(b + 1, len(items)):
                if items[v].kind in ("br", "end"):
                    add(b, v, 0)
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
    if u == "join":
        return True
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
            if items[v].unit() != "join":
                used.append(items[v].unit())
        cyc += 1
    return t


def length(items, t):
    return max(t[v] + items[v].latency() for v in range(len(items)))


# ------------------------------------------------------------ one trace


def _fresh(taken, base):
    k = 1
    while "%s.%d" % (base, k) in taken:
        k += 1
    lab = "%s.%d" % (base, k)
    taken.add(lab)
    return lab


def schedule_trace(prog, trace, freq, machine=MACHINE):
    """Schedule one trace. Returns (new program, labels of the scheduled
    pieces, new edge counts, (items, t))."""
    live_in = liveness(prog)  # @line L3
    items = trace_items(prog, trace)
    edges = build_dag(items, live_in)  # @line L4
    t = list_schedule(items, edges, machine)  # @line L7
    order = sorted(range(len(items)), key=lambda v: (t[v], v))
    where = {v: k for k, v in enumerate(order)}
    taken = set(prog.blocks)
    head = trace[0]
    pieces = {}
    extra = {}
    newfreq = {}
    cur, body = head, []
    for v in order:
        it = items[v]
        if it.kind == "op":
            body.append(it.ins)
        elif it.kind == "br":  # @line L8
            comp = [items[u].ins for u in order[where[v] + 1 :] if items[u].kind == "op" and u < v]  # @line L9
            nxt = _fresh(taken, head)
            w = freq.get((trace[it.blk], it.off), 0)
            target = it.off
            if comp:
                target = _fresh(taken, head)  # @line L10
                extra[target] = toyir.Block(list(comp), ("jump", it.off))
                newfreq[(target, it.off)] = w
            c = it.term
            term = ("br", c[1], target, nxt) if c[2] == it.off else ("br", c[1], nxt, target)
            pieces[cur] = toyir.Block(body, term)
            newfreq[(cur, target)] = w
            newfreq[(cur, nxt)] = freq.get((trace[it.blk], trace[it.blk + 1]), 0)
            cur, body = nxt, []
        elif it.kind == "join":  # @line L11
            comp = [items[u].ins for u in order[: where[v]] if items[u].kind == "op" and u > v]  # @line L12
            side = sum(freq.get((p, it.label), 0) for p in toyir.preds(prog)[it.label] if p != trace[it.blk - 1])
            if comp:
                nxt = _fresh(taken, head)
                extra[it.label] = toyir.Block(list(comp), ("jump", nxt))  # @line L13
                newfreq[(it.label, nxt)] = side
            else:
                nxt = it.label
            pieces[cur] = toyir.Block(body, ("jump", nxt))
            newfreq[(cur, nxt)] = freq.get((trace[it.blk - 1], it.label), 0)
            cur, body = nxt, []
        else:
            pieces[cur] = toyir.Block(body, it.term)
            last = trace[-1]
            for s in toyir.succs(prog, last):
                newfreq[(cur, s)] = freq.get((last, s), 0)
    blocks = {}
    for lab, b in prog.blocks.items():  # @line L14
        if lab == head:
            blocks.update(pieces)
        elif lab in trace:
            if lab in extra:
                blocks[lab] = extra.pop(lab)
        else:
            blocks[lab] = b
            for s in toyir.succs(prog, lab):
                newfreq[(lab, s)] = freq.get((lab, s), 0)
    blocks.update(extra)
    return toyir.Program(list(prog.params), blocks), set(pieces), newfreq, (items, t)


def trace_schedule(prog, freq=None, machine=MACHINE):
    """Schedule the whole program trace by trace. Returns (new program,
    list of (trace, items, t) for each trace)."""
    check_input(prog)
    if freq is None:
        freq = static_profile(prog)
    done = set()
    log = []
    while any(lab not in done for lab in prog.blocks):  # @line L1
        trace = pick_trace(prog, freq, done)  # @line L2
        prog, pieces, freq, (items, t) = schedule_trace(prog, trace, freq, machine)
        done |= pieces
        log.append((trace, items, t))
    return prog, log  # @line L15
