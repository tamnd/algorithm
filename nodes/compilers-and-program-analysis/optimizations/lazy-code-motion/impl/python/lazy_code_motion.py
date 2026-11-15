# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazy-code-motion/. The authors are listed in prov/AQQH48.jsonl.
"""Lazy code motion (Knoop, Ruthing and Steffen) on the toy IR.

lcm(prog) takes a program with const, copy and op instructions only. It
removes unreachable blocks, gives the entry no predecessor, and splits every
critical edge with a new block that only jumps. Then it works on a graph with
one node for each instruction and one node for each terminator. An
expression is the lexical triple (op, a, b) of an op instruction. Each
expression e gets a new temporary t_e. The program computes t_e = e at the
latest safe points, and an original x = e becomes x = t_e unless it is the
only use of a value computed at that point.

Sets of expressions are Python ints used as bit vectors. analyses(prog)
returns all the sets, so the tests and the page can look at them.
"""

import toyir


# ------------------------------------------------------------------- graph


def normalize(prog):
    """A copy of prog without unreachable blocks, with an entry that has no
    predecessor, and with every critical edge split. An edge A -> B is
    critical if A has two successors and B has two predecessors. The new
    block on the edge only jumps to B."""
    for blk in prog.blocks.values():
        for ins in blk.instrs:
            if ins[0] not in ("const", "copy", "op"):
                raise ValueError("lcm handles const, copy and op only: %r" % (ins,))
    reach = {prog.entry}
    stack = [prog.entry]
    while stack:
        b = stack.pop()
        for s in toyir.succs(prog, b):
            if s not in reach:
                reach.add(s)
                stack.append(s)
    taken = set(prog.blocks)

    def fresh(base):
        name = base
        while name in taken:
            name += "_"
        taken.add(name)
        return name

    blocks = {}
    if any(prog.entry in toyir.succs(prog, b) for b in reach):
        blocks[fresh("start")] = toyir.Block([], ("jump", prog.entry))
    for label, blk in prog.blocks.items():
        if label in reach:
            blocks[label] = toyir.Block(list(blk.instrs), blk.term)
    p = toyir.Program(list(prog.params), blocks)
    npred = {b: len(ps) for b, ps in toyir.preds(p).items()}
    out = {}
    for label, blk in p.blocks.items():
        out[label] = blk
        t = blk.term
        if t[0] == "br" and t[2] != t[3]:
            targets = []
            for s in (t[2], t[3]):
                if npred[s] > 1:
                    mid = fresh(label + "_" + s)
                    out[mid] = toyir.Block([], ("jump", s))
                    targets.append(mid)
                else:
                    targets.append(s)
            blk.term = ("br", t[1], targets[0], targets[1])
    return toyir.Program(list(prog.params), out)


class Graph:
    """The node graph of a program. Node (b, i) is instruction i of block b,
    and node (b, len(instrs)) is the terminator of b."""

    def __init__(self, prog):
        self.prog = prog
        self.nodes = []
        self.succ = {}
        for b, blk in prog.blocks.items():
            k = len(blk.instrs)
            for i in range(k + 1):
                self.nodes.append((b, i))
                self.succ[(b, i)] = [(b, i + 1)] if i < k else [(s, 0) for s in toyir.succs(prog, b)]
        self.pred = {n: [] for n in self.nodes}
        for n in self.nodes:
            for s in self.succ[n]:
                self.pred[s].append(n)

    def instr(self, n):
        blk = self.prog.blocks[n[0]]
        return blk.instrs[n[1]] if n[1] < len(blk.instrs) else None


def expression(ins):
    """The expression (op, a, b) that an instruction computes, or None."""
    if ins is not None and ins[0] == "op":
        return (ins[2], ins[3], ins[4])
    return None


# --------------------------------------------------------------- analyses


def analyses(prog):
    """All the sets of lazy code motion for a normalized program. Returns a
    dict with the graph, the list of expressions, and a dict node -> bit set
    for each of use, kill, ant_in, ant_out, av_in, av_out, earliest,
    post_in, post_out, latest, used_in and used_out."""
    g = Graph(prog)
    nodes, succ, pred = g.nodes, g.succ, g.pred
    exprs = []
    index = {}
    for n in nodes:
        e = expression(g.instr(n))
        if e is not None and e not in index:
            index[e] = len(exprs)
            exprs.append(e)
    full = (1 << len(exprs)) - 1
    reads = {}
    for e, i in index.items():
        for a in e[1:]:
            if isinstance(a, str):
                reads[a] = reads.get(a, 0) | (1 << i)

    use, kill = {}, {}
    for n in nodes:  # @line L2
        ins = g.instr(n)
        e = expression(ins)
        use[n] = 0 if e is None else 1 << index[e]
        kill[n] = 0 if ins is None else reads.get(ins[1], 0)

    # Anticipated (down-safe): on every path to the exit, e is computed
    # before an operand changes.
    ant_in = {n: full for n in nodes}
    ant_out = {}
    changed = True
    while changed:  # @line L3
        changed = False
        for n in reversed(nodes):
            out = full if succ[n] else 0
            for s in succ[n]:
                out &= ant_in[s]
            ant_out[n] = out
            new = use[n] | (out & ~kill[n])
            if new != ant_in[n]:
                ant_in[n] = new
                changed = True

    # Available if e were computed at every earliest point.
    av_out = {n: full for n in nodes}
    av_in = {}
    changed = True
    while changed:  # @line L4
        changed = False
        for n in nodes:
            inn = full if pred[n] else 0
            for p in pred[n]:
                inn &= av_out[p]
            av_in[n] = inn
            new = (ant_in[n] | inn) & ~kill[n]
            if new != av_out[n]:
                av_out[n] = new
                changed = True

    earliest = {n: ant_in[n] & ~av_in[n] for n in nodes}  # @line L5

    post_out = {n: full for n in nodes}
    post_in = {}
    changed = True
    while changed:  # @line L6
        changed = False
        for n in nodes:
            inn = full if pred[n] else 0
            for p in pred[n]:
                inn &= post_out[p]
            post_in[n] = inn
            new = (earliest[n] | inn) & ~use[n]
            if new != post_out[n]:
                post_out[n] = new
                changed = True

    latest = {}
    for n in nodes:  # @line L7
        nxt = full
        for s in succ[n]:
            nxt &= earliest[s] | post_in[s]
        latest[n] = (earliest[n] | post_in[n]) & (use[n] | (full & ~nxt))

    used_in = {n: 0 for n in nodes}
    used_out = {}
    changed = True
    while changed:  # @line L8
        changed = False
        for n in reversed(nodes):
            out = 0
            for s in succ[n]:
                out |= used_in[s]
            used_out[n] = out
            new = (use[n] | out) & ~latest[n]
            if new != used_in[n]:
                used_in[n] = new
                changed = True

    return {
        "graph": g, "exprs": exprs, "use": use, "kill": kill,
        "ant_in": ant_in, "ant_out": ant_out, "av_in": av_in, "av_out": av_out,
        "earliest": earliest, "post_in": post_in, "post_out": post_out,
        "latest": latest, "used_in": used_in, "used_out": used_out,
    }


# -------------------------------------------------------------- transform


def names_of(prog):
    out = set(prog.params)
    for blk in prog.blocks.values():
        for ins in blk.instrs:
            out.add(ins[1])
            out.update(toyir.uses(ins))
        out.update(toyir.term_uses(blk.term))
    return out


def rewrite(prog, exprs, insert, replace):
    """Build the new program. insert[n] and replace[n] are bit sets: insert
    t_e = e before node n for each e in insert[n], and turn the instruction
    x = e at n into x = t_e if e is in replace[n]."""
    taken = names_of(prog)
    temp = []
    for i in range(len(exprs)):
        name = "pre.%d" % i
        while name in taken:
            name += "_"
        taken.add(name)
        temp.append(name)
    blocks = {}
    for b, blk in prog.blocks.items():
        instrs = []
        for i in range(len(blk.instrs) + 1):
            n = (b, i)
            for k, e in enumerate(exprs):
                if insert[n] >> k & 1:
                    instrs.append(("op", temp[k], e[0], e[1], e[2]))
            if i < len(blk.instrs):
                ins = blk.instrs[i]
                e = expression(ins)
                if e is not None and replace[n] >> exprs.index(e) & 1:
                    instrs.append(("copy", ins[1], temp[exprs.index(e)]))
                else:
                    instrs.append(ins)
        blocks[b] = toyir.Block(instrs, blk.term)
    return toyir.Program(list(prog.params), blocks)


def lcm(prog):
    """Lazy code motion. Returns the new program. Its blocks are the blocks
    of normalize(prog), with the same terminators."""
    p = normalize(prog)  # @line L1
    a = analyses(p)
    nodes = a["graph"].nodes
    insert = {n: a["latest"][n] & a["used_out"][n] for n in nodes}  # @line L9
    replace = {}
    for n in nodes:  # @line L10
        u = a["use"][n]
        replace[n] = u & (~a["latest"][n] | a["used_out"][n])  # @line L11
    return rewrite(p, a["exprs"], insert, replace)  # @line L12
