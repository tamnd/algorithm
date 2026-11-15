# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ifds-framework/. The authors are listed in prov/K1QASX.jsonl.
"""The IFDS tabulation algorithm of Reps, Horwitz and Sagiv on the toy IR.

A module is a dict from procedure name to toyir.Program. Calls are
("call", x, f, args) instructions. The supergraph has one node per
instruction and one per terminator, as (proc, label, i), where i is the
index of the instruction in its block and i = len(instrs) is the
terminator. Each procedure also has an exit node (proc, EXIT, 0). A call
node c has three edges: to the start of the callee, from the exit of the
callee to the return site (the next node), and the call-to-return edge.

The problem solved here is "which variables may depend on the secret
inputs" (a taint analysis that follows data flow, not branches). It is a
distributive subset problem. The facts of a procedure are its variables
and the slot RET for its return value. ZERO is the extra fact that is
always present; it is the Lambda of the exploded supergraph.

ifds() returns, for every node, the set of facts that hold there on some
valid path from the start of main, and a Counter of the work done.
"""

from collections import Counter, deque

import toyir

ZERO = "0"
RET = "RET"
EXIT = "$exit"


class Supergraph:
    """The supergraph of a module and the flow functions of the problem."""

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
        """Edges of the supergraph: three per call site, the rest one each."""
        return sum(len(v) for v in self.succ.values()) + 3 * len(self.callee)

    def instr(self, n):
        p, label, i = n
        blk = self.module[p].blocks[label]
        return blk.instrs[i] if i < len(blk.instrs) else blk.term

    def normal_flow(self, n, m, d):
        """The facts at m that the fact d at n gives, for an edge n -> m that
        is not a call edge (the successor m does not change the result)."""
        if d == ZERO:
            return (ZERO,)
        ins = self.instr(n)
        k = ins[0]
        if k == "jump" or k == "br":
            return (d,)
        if k == "ret":
            return (d, RET) if d == ins[1] else (d,)
        x = ins[1]
        if k == "const":
            srcs = ()
        elif k == "copy":
            srcs = (ins[2],)
        else:
            srcs = (ins[3], ins[4])
        out = []
        if d != x:
            out.append(d)
        if d in srcs:
            out.append(x)
        return tuple(out)

    def call_flow(self, c, d):
        """From the fact d before the call c to the facts at the callee start."""
        if d == ZERO:
            return (ZERO,)
        ins = self.instr(c)
        params = self.module[ins[2]].params
        return tuple(params[j] for j, a in enumerate(ins[3]) if a == d)

    def c2r_flow(self, c, d):
        """The call-to-return edge: the caller's facts, minus the target."""
        if d == ZERO:
            return (ZERO,)
        return () if d == self.instr(c)[1] else (d,)

    def ret_flow(self, c, d):
        """From the fact d at the callee exit to the facts at the return site."""
        if d == ZERO:
            return (ZERO,)
        return (self.instr(c)[1],) if d == RET else ()


def ifds(sg, seeds=None):
    """Run the tabulation algorithm. seeds are the facts at the start of
    main; the default is the first parameter of main. Returns (X, stats)."""
    main = sg.main
    if seeds is None:
        seeds = [sg.module[main].params[0]]
    stats = Counter()
    path = set()  # @line L1
    sources = {}  # (n, d2) -> the set of d1 with a path edge <s_p,d1> -> <n,d2>
    summary = {}  # (c, d4) -> the set of d5 with a summary edge <c,d4> -> <r,d5>
    through = set()  # (c, d1, d5): <s_q,d1> reaches <e_q,d2> and d5 is in ret_c(d2)
    inv_call = {}  # c -> d1 -> the d4 with d1 in call_c(d4)
    for c in sg.callee:
        inv = {}
        for d4 in sg.facts[sg.proc[c]] + [ZERO]:
            for d1 in sg.call_flow(c, d4):
                inv.setdefault(d1, []).append(d4)
        inv_call[c] = inv
    work = deque()

    def propagate(d1, n, d2):
        key = (n, d1, d2)
        if key not in path:  # @line L16
            path.add(key)
            sources.setdefault((n, d2), set()).add(d1)
            work.append(key)
            stats["path_edges"] += 1

    s_main = sg.start[main]
    for d in list(seeds) + [ZERO]:  # @line L2
        propagate(d, s_main, d)
    while work:  # @line L3
        n, d1, d2 = work.popleft()  # @line L4
        stats["pops"] += 1
        p = sg.proc[n]
        if n in sg.callee:  # @line L5
            c, q, r = n, sg.callee[n], sg.ret_site[n]
            for d3 in sg.call_flow(c, d2):  # @line L6
                stats["flow"] += 1
                propagate(d3, sg.start[q], d3)
            for d3 in sg.c2r_flow(c, d2):  # @line L7
                stats["flow"] += 1
                propagate(d1, r, d3)
            for d3 in list(summary.get((c, d2), ())):
                stats["flow"] += 1
                propagate(d1, r, d3)
        elif n == sg.exit[p]:  # @line L8
            for c in sg.callers[p]:  # @line L9
                r = sg.ret_site[c]
                for d5 in sg.ret_flow(c, d2):
                    stats["flow"] += 1
                    if (c, d1, d5) in through:  # @line L10
                        continue
                    through.add((c, d1, d5))
                    for d4 in inv_call[c].get(d1, ()):  # @line L11
                        stats["flow"] += 1
                        sset = summary.setdefault((c, d4), set())
                        if d5 in sset:
                            continue
                        sset.add(d5)  # @line L12
                        stats["summary_edges"] += 1
                        for d3 in list(sources.get((c, d4), ())):  # @line L13
                            stats["flow"] += 1
                            propagate(d3, r, d5)
        else:
            for m in sg.succ[n]:  # @line L14
                for d3 in sg.normal_flow(n, m, d2):
                    stats["flow"] += 1
                    propagate(d1, m, d3)
    X = {n: set() for n in sg.nodes}  # @line L15
    for n, _d1, d2 in path:
        if d2 != ZERO:
            X[n].add(d2)
    return X, stats


def ifds_framework(module, main=None, seeds=None):
    """Convenience wrapper: the facts at every node of the module."""
    sg = Supergraph(module, main)
    X, _ = ifds(sg, seeds)
    return X
