# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alpern-wegman-zadeck-value-numbering/. The authors are listed in prov/1FT49Y.jsonl.
"""Alpern-Wegman-Zadeck value numbering on the toy IR.

awz(prog) takes a program without phis and without memory operations, puts it
in SSA form, finds the coarsest congruence of its value graph by Hopcroft
partition refinement, and replaces each definition that has a congruent
definition above it in the dominator tree by a copy. It returns the new
program and the partition.

The parts can be used alone: to_ssa builds SSA form with copies and constants
folded into the operands, value_graph builds the labeled graph, congruence
refines a partition, and eliminate does the replacement.
"""

import toyir


# ------------------------------------------------------------------ graphs


def normalize(prog):
    """A copy of prog without unreachable blocks and with an entry block that
    has no predecessor (a new block "start" is added if needed)."""
    seen = []
    stack = [prog.entry]
    reach = {prog.entry}
    while stack:
        b = stack.pop()
        seen.append(b)
        for s in toyir.succs(prog, b):
            if s not in reach:
                reach.add(s)
                stack.append(s)
    blocks = {}
    if any(prog.entry in toyir.succs(prog, b) for b in reach):
        name = "start"
        while name in prog.blocks:
            name += "_"
        blocks[name] = toyir.Block([], ("jump", prog.entry))
    for label, blk in prog.blocks.items():
        if label in reach:
            blocks[label] = toyir.Block(list(blk.instrs), blk.term)
    return toyir.Program(list(prog.params), blocks)


def reverse_postorder(prog):
    order = []
    seen = {prog.entry}
    stack = [(prog.entry, iter(toyir.succs(prog, prog.entry)))]
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


def dominators(prog):
    """Immediate dominators by the iterative method of Cooper, Harvey and
    Kennedy. The entry maps to itself. Every block must be reachable."""
    rpo = reverse_postorder(prog)
    index = {b: i for i, b in enumerate(rpo)}
    preds = toyir.preds(prog)
    idom = {rpo[0]: rpo[0]}

    def meet(a, b):
        while a != b:
            while index[a] > index[b]:
                a = idom[a]
            while index[b] > index[a]:
                b = idom[b]
        return a

    changed = True
    while changed:
        changed = False
        for b in rpo[1:]:
            new = None
            for p in preds[b]:
                if p in idom:
                    new = p if new is None else meet(p, new)
            if idom.get(b) != new:
                idom[b] = new
                changed = True
    return idom


def dom_children(prog, idom):
    kids = {b: [] for b in prog.blocks}
    for b in prog.blocks:
        if b != prog.entry:
            kids[idom[b]].append(b)
    return kids


def dominates(idom, a, b):
    """True if block a dominates block b."""
    while True:
        if a == b:
            return True
        if idom[b] == b:
            return False
        b = idom[b]


def frontiers(prog, idom):
    preds = toyir.preds(prog)
    df = {b: set() for b in prog.blocks}
    for b in prog.blocks:
        if len(preds[b]) >= 2:
            for p in preds[b]:
                r = p
                while r != idom[b]:
                    df[r].add(b)
                    r = idom[r]
    return df


# --------------------------------------------------------------------- SSA


def live_in(prog):
    """The names that are live on entry to each block of a program without
    phis."""
    gen, kill = {}, {}
    for b, blk in prog.blocks.items():
        g, k = set(), set()
        for ins in blk.instrs:
            g |= set(toyir.uses(ins)) - k
            k.add(toyir.defs(ins))
        g |= set(toyir.term_uses(blk.term)) - k
        gen[b], kill[b] = g, k
    live = {b: set() for b in prog.blocks}
    changed = True
    while changed:
        changed = False
        for b in reversed(list(prog.blocks)):
            out = set()
            for s in toyir.succs(prog, b):
                out |= live[s]
            new = gen[b] | (out - kill[b])
            if new != live[b]:
                live[b] = new
                changed = True
    return live


def to_ssa(prog):
    """SSA form of a program with only const, copy and op instructions.
    Copies and constants are folded into the operands that read them, so
    the result has only phis and ops. Version 0 of a parameter is the
    parameter itself, and the other versions are named base.k. A read of a
    name with no reaching definition reads 0; the programs we transform never
    do such a read. Phis are placed at the iterated dominance frontier of the
    definitions (minimal SSA, not pruned)."""
    prog = normalize(prog)
    for blk in prog.blocks.values():
        for ins in blk.instrs:
            if ins[0] not in ("const", "copy", "op"):
                raise ValueError("awz handles const, copy and op only: %r" % (ins,))
    idom = dominators(prog)
    df = frontiers(prog, idom)
    kids = dom_children(prog, idom)
    preds = toyir.preds(prog)

    sites = {}
    for p in prog.params:
        sites.setdefault(p, set()).add(prog.entry)
    for label, blk in prog.blocks.items():
        for ins in blk.instrs:
            sites.setdefault(ins[1], set()).add(label)
    live = live_in(prog)
    phis = {b: [] for b in prog.blocks}
    for v in sites:
        work = list(sites[v])
        placed = set()
        while work:
            b = work.pop()
            for f in df[b]:
                if f not in placed:
                    placed.add(f)
                    if v in live[f]:
                        phis[f].append(v)
                    if f not in sites[v]:
                        work.append(f)
    for b in phis:
        phis[b].sort()

    taken = set(sites) | set(prog.params)
    counter = {}

    def fresh(v):
        while True:
            counter[v] = counter.get(v, 0) + 1
            name = "%s.%d" % (v, counter[v])
            if name not in taken:
                taken.add(name)
                return name

    stack = {v: [] for v in sites}
    for p in prog.params:
        stack[p].append(p)

    def cur(a):
        if isinstance(a, int):
            return a
        s = stack.get(a)
        return s[-1] if s else 0

    phi_name = {}
    phi_args = {}
    body = {}
    terms = {}

    def rename(b):
        pushed = []
        for v in phis[b]:
            name = fresh(v)
            phi_name[(b, v)] = name
            stack[v].append(name)
            pushed.append(v)
        out = []
        for ins in prog.blocks[b].instrs:
            x = ins[1]
            if ins[0] == "const":
                val = ins[2]
            elif ins[0] == "copy":
                val = cur(ins[2])
            else:
                val = fresh(x)
                out.append(("op", val, ins[2], cur(ins[3]), cur(ins[4])))
            stack[x].append(val)
            pushed.append(x)
        body[b] = out
        t = prog.blocks[b].term
        if t[0] == "br":
            terms[b] = ("br", cur(t[1]), t[2], t[3])
        elif t[0] == "ret":
            terms[b] = ("ret", cur(t[1]))
        else:
            terms[b] = t
        for s in toyir.succs(prog, b):
            for v in phis[s]:
                phi_args.setdefault((s, v), {})[b] = cur(v)
        for c in kids[b]:
            rename(c)
        for v in pushed:
            stack[v].pop()

    rename(prog.entry)
    blocks = {}
    for b in prog.blocks:
        instrs = []
        for v in phis[b]:
            args = phi_args[(b, v)]
            instrs.append(("phi", phi_name[(b, v)], {p: args[p] for p in preds[b]}))
        blocks[b] = toyir.Block(instrs + body[b], terms[b])
    return toyir.Program(list(prog.params), blocks)


# ------------------------------------------------------------ value graph


def value_graph(ssa):
    """The value graph of an SSA program: (nodes, label, children). A node
    is an SSA name or an integer constant. The label of an op is ("op", op),
    of a phi ("phi", block), of a parameter ("param", name) and of a
    constant ("const", k). The children of a phi follow the order of the
    predecessors of its block."""
    label = {}
    children = {}

    def leaf(a):
        if isinstance(a, int) and a not in label:
            label[a] = ("const", a)
            children[a] = ()
        return a

    for p in ssa.params:
        label[p] = ("param", p)
        children[p] = ()
    for b, blk in ssa.blocks.items():
        for ins in blk.instrs:
            if ins[0] == "phi":
                label[ins[1]] = ("phi", b)
                children[ins[1]] = tuple(leaf(a) for a in ins[2].values())
            else:
                label[ins[1]] = ("op", ins[2])
                children[ins[1]] = (leaf(ins[3]), leaf(ins[4]))
        t = blk.term
        if t[0] in ("br", "ret"):
            leaf(t[1])
    nodes = list(label)
    return nodes, label, children


# --------------------------------------------------- partition refinement


def congruence(nodes, label, children):
    """The coarsest partition of the nodes that refines the partition by
    label and in which nodes of one class have children in the same
    classes, position by position. Returns a dict node -> class number.
    Hopcroft's rule: after a split, only the smaller part goes into the
    worklist. The time is O((N + E) log N) for N nodes and E edges."""
    users = {}
    for n in nodes:
        for j, c in enumerate(children[n]):
            users.setdefault(c, []).append((j, n))
    members = []
    cls = {}
    first = {}
    for n in nodes:  # @line L3
        key = (label[n], len(children[n]))
        if key not in first:
            first[key] = len(members)
            members.append(set())
        cls[n] = first[key]
        members[first[key]].add(n)
    work = list(range(len(members)))  # @line L4
    while work:  # @line L5
        c = work.pop()  # @line L6
        pre = {}
        for m in list(members[c]):
            for j, u in users.get(m, ()):
                pre.setdefault(j, []).append(u)
        for j in sorted(pre):  # @line L7
            hit = {}
            for u in pre[j]:
                hit.setdefault(cls[u], set()).add(u)
            for d, part in hit.items():  # @line L8
                if len(part) == len(members[d]):
                    continue
                # Split in time O(|part|): move out the smaller side.
                if 2 * len(part) <= len(members[d]):  # @line L9
                    small = part
                    members[d] -= part
                else:
                    small = members[d] - part
                    members[d] = part
                new = len(members)
                members.append(small)
                for u in small:
                    cls[u] = new
                work.append(new)  # @line L10
    return cls


# -------------------------------------------------------------- elimination


def eliminate(ssa, cls):
    """Replace each phi or op whose class has a definition higher in the
    dominator tree, or earlier in the same block, by a copy of that
    definition. A replaced phi becomes a copy placed after the phis of its
    block. Returns a new program."""
    idom = dominators(ssa)
    kids = dom_children(ssa, idom)
    rep = {}
    for p in ssa.params:
        rep.setdefault(cls[p], p)
    blocks = {}

    def walk(b):  # @line L11
        added = []
        blk = ssa.blocks[b]
        phis, copies, rest = [], [], []
        for ins in blk.instrs:  # @line L12
            x = ins[1]
            c = cls[x]
            if c in rep:  # @line L13
                (copies if ins[0] == "phi" else rest).append(("copy", x, rep[c]))
            else:
                rep[c] = x  # @line L14
                added.append(c)
                (phis if ins[0] == "phi" else rest).append(ins)
        blocks[b] = toyir.Block(phis + copies + rest, blk.term)
        for k in kids[b]:
            walk(k)
        for c in added:
            del rep[c]

    walk(ssa.entry)
    return toyir.Program(list(ssa.params), {b: blocks[b] for b in ssa.blocks})  # @line L15


def awz(prog):
    """Returns (new program, partition) for a program with const, copy and
    op instructions only. The partition maps each node of the value graph
    of to_ssa(prog) to its class number."""
    ssa = to_ssa(prog)  # @line L1
    nodes, label, children = value_graph(ssa)  # @line L2
    cls = congruence(nodes, label, children)
    return eliminate(ssa, cls), cls
