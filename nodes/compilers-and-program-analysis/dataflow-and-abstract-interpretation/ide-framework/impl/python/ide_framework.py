# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ide-framework/. The authors are listed in prov/60PTYF.jsonl.
"""The IDE algorithm of Sagiv, Reps and Horwitz, with linear constant
propagation on the toy IR as the instance.

A module is a dict from procedure name to toyir.Program, as for IFDS. The
supergraph has a node (proc, label, i) for instruction i of a block, a node
for each terminator (i = len(instrs)) and an exit node (proc, EXIT, 0) per
procedure. The facts of a procedure are its variables and RET; ZERO is the
extra fact. Every exploded edge carries a micro-function on values.

Values: TOP (no value seen), an int, or BOT (not a constant).
Micro-functions, in a form that is unique for each function:

    ("top",)          l -> TOP for every l, the function of no path
    ("bot",)          l -> BOT
    ("const", k)      l -> k
    ("line", a, b)    l -> a*l + b for an int l, BOT -> BOT   (a != 0)
    ("point", l0, v)  l0 -> v, any other l -> BOT

Every function maps TOP to TOP. A value that some path reaches is never
TOP, so only the behaviour on ints and BOT matters, and there the forms
above are closed under meet and composition, with no loss.
"""

from collections import Counter, deque

import toyir

ZERO = "0"
RET = "RET"
EXIT = "$exit"
TOP = "top"
BOT = "bot"

TOPF = ("top",)
BOTF = ("bot",)
ID = ("line", 1, 0)


# ------------------------------------------------------------------ values


def meet_val(a, b):
    if a == TOP:
        return b
    if b == TOP or a == b:
        return a
    return BOT


def apply(f, l):
    """The value of the micro-function f at l."""
    if l == TOP or f[0] == "top":
        return TOP
    k = f[0]
    if k == "bot":
        return BOT
    if k == "const":
        return f[1]
    if l == BOT:
        return BOT
    if k == "line":
        return f[1] * l + f[2]
    return f[2] if l == f[1] else BOT


def _point_or_bot(num, den, value):
    """The point function at l0 = num / den with the given value, or BOT
    when l0 is not an int (or the value is BOT)."""
    if value == BOT or num % den != 0:
        return BOTF
    return ("point", num // den, value)


def meet_fn(f, g):
    """The pointwise meet of two micro-functions."""
    if f[0] == "top":
        return g
    if g[0] == "top" or f == g:
        return f
    if f[0] == "bot" or g[0] == "bot":
        return BOTF
    if f[0] > g[0]:
        f, g = g, f
    # Now f[0] <= g[0] in the order const < line < point.
    if f[0] == "const" and g[0] == "const":
        return BOTF
    if f[0] == "const" and g[0] == "line":
        k, a, b = f[1], g[1], g[2]
        return _point_or_bot(k - b, a, k)
    if f[0] == "const":  # g is a point
        return g if g[2] == f[1] else BOTF
    if f[0] == "line" and g[0] == "line":
        a1, b1, a2, b2 = f[1], f[2], g[1], g[2]
        if a1 == a2:
            return BOTF
        num, den = b2 - b1, a1 - a2
        if num % den != 0:
            return BOTF
        l0 = num // den
        return ("point", l0, a1 * l0 + b1)
    if f[0] == "line":  # g is a point
        return g if f[1] * g[1] + f[2] == g[2] else BOTF
    return BOTF  # two different points


def compose(g, f):
    """The micro-function g after f."""
    if f[0] == "top" or g[0] == "top":
        return TOPF
    if g[0] == "bot" or g[0] == "const":
        return g
    if f[0] == "bot":
        return BOTF
    if f[0] == "const":
        v = apply(g, f[1])
        return BOTF if v == BOT else ("const", v)
    if f[0] == "point":
        v = apply(g, f[2])
        return BOTF if v == BOT else ("point", f[1], v)
    a1, b1 = f[1], f[2]  # f is a line
    if g[0] == "line":
        return ("line", g[1] * a1, g[1] * b1 + g[2])
    return _point_or_bot(g[1] - b1, a1, g[2])  # g is a point


# ------------------------------------------------------------- supergraph


def _linear(op, a, b):
    """The micro-function of x = a op b, as (source, function): source is a
    variable, or ZERO for a function that ignores its input."""
    if isinstance(a, int) and isinstance(b, int):
        try:
            return ZERO, ("const", toyir._binop(op, a, b))
        except toyir._Trap:
            return ZERO, BOTF
    if isinstance(a, str) and isinstance(b, str):
        return ZERO, BOTF
    if op == "+":
        return (a, ("line", 1, b)) if isinstance(a, str) else (b, ("line", 1, a))
    if op == "-":
        return (a, ("line", 1, -b)) if isinstance(a, str) else (b, ("line", -1, a))
    if op == "*":
        var, k = (a, b) if isinstance(a, str) else (b, a)
        return (ZERO, ("const", 0)) if k == 0 else (var, ("line", k, 0))
    return ZERO, BOTF


class Supergraph:
    """The supergraph of a module and the exploded edges of linear constant
    propagation. Each flow method returns a list of (fact, micro-function)."""

    def __init__(self, module, main=None):
        self.module = module
        self.main = main if main is not None else next(iter(module))
        self.facts = {}
        self.start = {}
        self.exit = {}
        self.succ = {}
        self.callee = {}
        self.ret_site = {}
        self.callers = {p: [] for p in module}
        self.calls_in = {p: [] for p in module}
        self.nodes = []
        self.proc = {}
        for p, prog in module.items():
            names = set(prog.params)
            for label, blk in prog.blocks.items():
                for i, ins in enumerate(blk.instrs):
                    if ins[0] not in ("const", "copy", "op", "call"):
                        raise ValueError("unsupported instruction: %r" % (ins,))
                    names.add(ins[1])
                    names.update(toyir.uses(ins))
                    node = (p, label, i)
                    self.nodes.append(node)
                    if ins[0] == "call":
                        q = ins[2]
                        if q not in module:
                            raise ValueError("unknown procedure %r" % q)
                        if len(ins[3]) != len(module[q].params):
                            raise ValueError("wrong number of arguments for %r" % q)
                        self.callee[node] = q
                        self.ret_site[node] = (p, label, i + 1)
                        self.callers[q].append(node)
                        self.calls_in[p].append(node)
                    else:
                        self.succ[node] = [(p, label, i + 1)]
                names.update(toyir.term_uses(blk.term))
                tnode = (p, label, len(blk.instrs))
                self.nodes.append(tnode)
                if blk.term[0] == "ret":
                    self.succ[tnode] = [(p, EXIT, 0)]
                else:
                    self.succ[tnode] = [(p, s, 0) for s in toyir.succs(prog, label)]
            if RET in names or ZERO in names:
                raise ValueError("reserved name used as a variable")
            self.facts[p] = sorted(names) + [RET]
            self.start[p] = (p, prog.entry, 0)
            self.exit[p] = (p, EXIT, 0)
            self.nodes.append(self.exit[p])
            self.succ[self.exit[p]] = []
        for n in self.nodes:
            self.proc[n] = n[0]

    def num_edges(self):
        return sum(len(v) for v in self.succ.values()) + 3 * len(self.callee)

    def instr(self, n):
        p, label, i = n
        blk = self.module[p].blocks[label]
        return blk.instrs[i] if i < len(blk.instrs) else blk.term

    def normal_flow(self, n, m, d):
        ins = self.instr(n)
        k = ins[0]
        if k == "jump" or k == "br":
            return [(d, ID)]
        if k == "ret":
            a = ins[1]
            out = [(d, ID)]
            if d == ZERO and isinstance(a, int):
                out.append((RET, ("const", a)))
            elif d == a:
                out.append((RET, ID))
            return out
        x = ins[1]
        if k == "const":
            src, fn = ZERO, ("const", ins[2])
        elif k == "copy":
            src, fn = ins[2], ID
        else:
            src, fn = _linear(ins[2], ins[3], ins[4])
        out = []
        if d != x:
            out.append((d, ID))
        if d == src:
            out.append((x, fn))
        return out

    def call_flow(self, c, d):
        ins = self.instr(c)
        params = self.module[ins[2]].params
        if d == ZERO:
            out = [(ZERO, ID)]
            out += [(params[j], ("const", a)) for j, a in enumerate(ins[3]) if isinstance(a, int)]
            return out
        return [(params[j], ID) for j, a in enumerate(ins[3]) if a == d]

    def c2r_flow(self, c, d):
        return [] if d == self.instr(c)[1] else [(d, ID)]

    def ret_flow(self, c, d):
        if d == ZERO:
            return [(ZERO, ID)]
        return [(self.instr(c)[1], ID)] if d == RET else []


# -------------------------------------------------------------- the solver


def ide(sg, seeds=None):
    """Run IDE. seeds maps each parameter of main to its value at the start
    (an int or BOT); a missing parameter is BOT. Returns (V, stats), where
    V[n] maps each variable with a value other than TOP to that value."""
    seeds = dict(seeds or {})
    main = sg.main
    stats = Counter()
    jump = {}  # (n, d1, d2) -> the jump function from <s_p, d1> to <n, d2>
    sources = {}  # (n, d2) -> the d1 with a jump function to <n, d2>
    targets = {}  # (n, d1) -> the d2 with a jump function from <s_p, d1> to <n, d2>
    summary = {}  # (c, d4) -> {d5: the summary function from <c, d4> to <r, d5>}
    through = {}  # (c, d1, d5) -> meet of ret o jump(e_q, d1, d2) over d2
    inv_call = {}  # c -> d1 -> [(d4, h)] for the call edges <c, d4> -> <s_q, d1>
    for c in sg.callee:
        inv = {}
        for d4 in sg.facts[sg.proc[c]] + [ZERO]:
            for d1, h in sg.call_flow(c, d4):
                inv.setdefault(d1, []).append((d4, h))
        inv_call[c] = inv
    work = deque()
    queued = set()

    def propagate(n, d1, d2, f):
        key = (n, d1, d2)
        old = jump.get(key, TOPF)
        new = meet_fn(old, f)
        stats["meets"] += 1
        if new != old:  # @line L22
            if old == TOPF:
                stats["path_edges"] += 1
                sources.setdefault((n, d2), set()).add(d1)
                targets.setdefault((n, d1), set()).add(d2)
            jump[key] = new
            stats["jump_changes"] += 1
            if key not in queued:
                queued.add(key)
                work.append(key)

    # Phase I: jump functions and summary functions.
    s_main = sg.start[main]  # @line L1
    for d in [ZERO] + list(sg.module[main].params):  # @line L2
        propagate(s_main, d, d, ID)
    while work:  # @line L3
        key = work.popleft()  # @line L4
        queued.discard(key)
        n, d1, d2 = key
        f = jump[key]
        stats["pops"] += 1
        p = sg.proc[n]
        if n in sg.callee:  # @line L5
            c, q, r = n, sg.callee[n], sg.ret_site[n]
            for d3, _h in sg.call_flow(c, d2):  # @line L6
                propagate(sg.start[q], d3, d3, ID)
            for d3, g in sg.c2r_flow(c, d2):  # @line L7
                propagate(r, d1, d3, compose(g, f))
            for d3, s in list(summary.get((c, d2), {}).items()):
                propagate(r, d1, d3, compose(s, f))
        elif n == sg.exit[p]:  # @line L8
            for c in sg.callers[p]:  # @line L9
                r = sg.ret_site[c]
                for d5, g in sg.ret_flow(c, d2):
                    tkey = (c, d1, d5)
                    told = through.get(tkey, TOPF)
                    t = meet_fn(told, compose(g, f))  # @line L10
                    if t == told:
                        continue
                    through[tkey] = t
                    for d4, h in inv_call[c].get(d1, ()):  # @line L11
                        sums = summary.setdefault((c, d4), {})
                        sold = sums.get(d5, TOPF)
                        s = meet_fn(sold, compose(t, h))  # @line L12
                        if s == sold:
                            continue
                        sums[d5] = s
                        stats["summary_changes"] += 1
                        for d3 in list(sources.get((c, d4), ())):  # @line L13
                            propagate(r, d3, d5, compose(s, jump[(c, d3, d4)]))
        else:
            for m in sg.succ[n]:  # @line L14
                for d3, g in sg.normal_flow(n, m, d2):
                    propagate(m, d1, d3, compose(g, f))

    # Phase II: values.
    val = {}
    work2 = deque()
    in_work2 = set()

    def lower(n, d, v):
        old = val.get((n, d), TOP)
        new = meet_val(old, v)
        if new != old:  # @line L23
            val[(n, d)] = new
            stats["value_changes"] += 1
            if (n, d) not in in_work2:
                in_work2.add((n, d))
                work2.append((n, d))

    lower(s_main, ZERO, BOT)  # @line L15
    for x in sg.module[main].params:
        lower(s_main, x, seeds.get(x, BOT))
    while work2:  # @line L16
        n, d = work2.popleft()  # @line L17
        in_work2.discard((n, d))
        v = val[(n, d)]
        p = sg.proc[n]
        if n == sg.start[p]:  # @line L18
            for m in [n] + sg.calls_in[p]:
                for d2 in list(targets.get((m, d), ())):
                    lower(m, d2, apply(jump[(m, d, d2)], v))
        if n in sg.callee:  # @line L19
            q = sg.callee[n]
            for d3, h in sg.call_flow(n, d):
                lower(sg.start[q], d3, apply(h, v))
    for (n, d1, d2), f in jump.items():  # @line L20
        p = sg.proc[n]
        if n == sg.start[p] or n in sg.callee:
            continue
        v = val.get((sg.start[p], d1), TOP)
        if v != TOP:
            new = meet_val(val.get((n, d2), TOP), apply(f, v))
            if new != TOP:
                val[(n, d2)] = new
    V = {n: {} for n in sg.nodes}  # @line L21
    for (n, d), v in val.items():
        if d != ZERO and v != TOP:
            V[n][d] = v
    return V, stats


def ide_framework(module, main=None, seeds=None):
    """Convenience wrapper: the constants at every node of the module."""
    sg = Supergraph(module, main)
    V, _ = ide(sg, seeds)
    return V
