# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cytron-ssa-construction/. The authors are listed in prov/BVFDF2.jsonl.
"""Minimal SSA form by the method of Cytron, Ferrante, Rosen, Wegman and
Zadeck: phi-functions at the iterated dominance frontier of the blocks that
assign each variable, then renaming by a walk of the dominator tree.

The input is a toy IR program without phi-functions, whose names contain no
dot. The output names the k-th definition of v as v.k. A parameter keeps its
own name for its value on entry. A variable that some path reads before any
assignment gets the name v.0, defined by v.0 = 0 at the top of the entry, so
the result is strict: every definition dominates its uses.
"""

import toyir
from toyir import Block, Program


# ------------------------------------------------- dominators and frontiers


def _postorder(succ, root):
    seen = {root}
    out = []
    stack = [(root, iter(succ[root]))]
    while stack:
        v, it = stack[-1]
        w = next(it, None)
        if w is None:
            stack.pop()
            out.append(v)
        elif w not in seen:
            seen.add(w)
            stack.append((w, iter(succ[w])))
    return out


def immediate_dominators(succ, root):
    """The Cooper-Harvey-Kennedy iteration. idom[root] is None, and only the
    nodes that root reaches are keys."""
    order = _postorder(succ, root)
    po = {v: i for i, v in enumerate(order)}
    pred = {v: [] for v in order}
    for v in order:
        for w in succ[v]:
            pred[w].append(v)
    doms = {root: root}

    def intersect(a, b):
        while a != b:
            while po[a] < po[b]:
                a = doms[a]
            while po[b] < po[a]:
                b = doms[b]
        return a

    changed = True
    while changed:
        changed = False
        for b in reversed(order):
            if b == root:
                continue
            new = None
            for p in pred[b]:
                if p in doms:
                    new = p if new is None else intersect(p, new)
            if doms.get(b) != new:
                doms[b] = new
                changed = True
    idom = dict(doms)
    idom[root] = None
    return idom


def dominance_frontiers(succ, root, idom):
    """The walk of Cooper, Harvey and Kennedy from each predecessor."""
    pred = {v: [] for v in idom}
    for v in idom:
        for w in succ[v]:
            pred[w].append(v)
    df = {v: set() for v in idom}
    for y in idom:
        for p in pred[y]:
            runner = p
            while runner != idom[y] and y not in df[runner]:
                df[runner].add(y)
                runner = idom[runner]
    return df


# ------------------------------------------------------------- construction


def variables(prog):
    """The parameters, then the assigned names, in order of first appearance."""
    out = list(prog.params)
    for b in prog.blocks.values():
        for ins in b.instrs:
            x = toyir.defs(ins)
            if x is not None and x not in out:
                out.append(x)
    return out


def place_phis(prog, idom=None, df=None):
    """Dict from block to the variables that get a phi-function there."""
    succ = {label: toyir.succs(prog, label) for label in prog.blocks}
    root = prog.entry
    if idom is None:
        idom = immediate_dominators(succ, root)
    if df is None:
        df = dominance_frontiers(succ, root, idom)
    sites = {v: {root} for v in variables(prog)}  # @line L1
    for label in idom:
        for ins in prog.blocks[label].instrs:
            x = toyir.defs(ins)
            if x is not None:
                sites[x].add(label)  # @line L2
    phis = {label: [] for label in idom}
    for v, s in sites.items():  # @line L3
        has_phi = set()
        work = list(s)  # @line L4
        queued = set(s)
        while work:  # @line L5
            x = work.pop()
            for y in df[x]:  # @line L6
                if y not in has_phi:
                    has_phi.add(y)
                    phis[y].append(v)  # @line L7
                    if y not in queued:
                        queued.add(y)
                        work.append(y)  # @line L8
    return phis


def cytron_ssa(prog):
    """Return a new program in minimal, strict SSA form with the same behaviour."""
    for b in prog.blocks.values():
        for ins in b.instrs:
            if ins[0] == "phi":
                raise ValueError("the input already has phi-functions")
            x = toyir.defs(ins)
            if x is not None and "." in x:
                raise ValueError("names must not contain a dot: %r" % x)
    succ = {label: toyir.succs(prog, label) for label in prog.blocks}
    root = prog.entry
    idom = immediate_dominators(succ, root)
    df = dominance_frontiers(succ, root, idom)
    phis = place_phis(prog, idom, df)

    children = {v: [] for v in idom}
    for v in idom:
        if idom[v] is not None:
            children[idom[v]].append(v)
    params = set(prog.params)
    counter = {v: 0 for v in variables(prog)}
    stacks = {v: [] for v in counter}
    undefined = []  # the variables that need v.0 = 0 at the entry

    def top(v):
        if stacks[v]:
            return stacks[v][-1]
        name = v + ".0"
        if name not in undefined:
            undefined.append(name)
        return name

    def fresh(v):
        counter[v] += 1
        name = "%s.%d" % (v, counter[v])
        stacks[v].append(name)
        return name

    def operand(a):
        return top(a) if isinstance(a, str) else a

    for p in prog.params:
        stacks[p].append(p)  # @line L9

    # The blocks of the result, filled in during the walk. The phi-functions
    # are created first, with no operands, and get one operand per edge.
    new_phis = {label: [("phi", None, {}) for _ in phis[label]] for label in idom}
    out = {label: None for label in prog.blocks if label in idom}

    def rename(b):  # @line L10
        pushed = []
        block_phis = []
        for v, (_, _, args) in zip(phis[b], new_phis[b]):
            block_phis.append(("phi", fresh(v), args))  # @line L11
            pushed.append(v)
        new_phis[b] = block_phis
        instrs = []
        for ins in prog.blocks[b].instrs:
            k = ins[0]
            if k == "const":
                ins2 = ("const", None, ins[2])
            elif k == "copy":
                ins2 = ("copy", None, operand(ins[2]))  # @line L12
            elif k == "op":
                ins2 = ("op", None, ins[2], operand(ins[3]), operand(ins[4]))
            else:
                raise ValueError("unsupported instruction: %r" % (ins,))
            name = fresh(ins[1])  # @line L13
            pushed.append(ins[1])
            instrs.append(ins2[:1] + (name,) + ins2[2:])
        t = prog.blocks[b].term
        if t[0] == "br":
            t = ("br", operand(t[1]), t[2], t[3])
        elif t[0] == "ret":
            t = ("ret", operand(t[1]))
        for s in succ[b]:  # @line L14
            for v, (_, _, args) in zip(phis[s], new_phis[s]):
                args[b] = top(v)  # @line L15
        out[b] = (instrs, t)
        for c in children[b]:  # @line L16
            rename(c)
        for v in pushed:  # @line L17
            stacks[v].pop()

    rename(root)

    preds = {label: [] for label in out}
    for a in out:
        for s in succ[a]:
            preds[s].append(a)
    blocks = {}
    for label, (instrs, t) in out.items():
        # Write the operands of each phi-function in predecessor order.
        head = [("phi", x, {p: args[p] for p in preds[label]}) for _, x, args in new_phis[label]]
        if label == root:
            head = [("const", name, 0) for name in undefined] + head
        blocks[label] = Block(head + instrs, t)
    return Program(list(prog.params), blocks)


def strip_versions(prog):
    """Out of SSA for the output of cytron_ssa: drop the phi-functions and
    map each name v.k back to v. This is correct because the construction
    keeps the program conventional: no two versions of one variable are live
    at the same point."""
    def base(a):
        return a.split(".")[0] if isinstance(a, str) else a

    blocks = {}
    for label, b in prog.blocks.items():
        instrs = []
        for ins in b.instrs:
            if ins[0] == "phi":
                continue
            if ins[0] == "const":
                instrs.append(("const", base(ins[1]), ins[2]))
            elif ins[0] == "copy":
                instrs.append(("copy", base(ins[1]), base(ins[2])))
            else:
                instrs.append(("op", base(ins[1]), ins[2], base(ins[3]), base(ins[4])))
        t = b.term
        if t[0] == "br":
            t = ("br", base(t[1]), t[2], t[3])
        elif t[0] == "ret":
            t = ("ret", base(t[1]))
        blocks[label] = Block(instrs, t)
    return Program(list(prog.params), blocks)
