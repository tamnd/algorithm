# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aggressive-dead-code-elimination/. The authors are listed in prov/VFFWX5.jsonl.
"""Aggressive dead code elimination on the toy IR, for programs without
phi-functions.

adce(prog) starts from the critical statements (returns, stores, calls,
allocations, operations that may trap, and definitions of address-taken
names), marks
every definition that reaches a use in a marked statement, and marks every
branch on which a block with a marked statement is control dependent. Then
it deletes the unmarked instructions, replaces each unmarked branch by a jump
to the nearest post-dominator that holds a marked statement, and drops the
blocks that the entry no longer reaches. It returns a new program.

A statement is named by (label, i). For i < len(instrs) it is instruction
i of the block; i == len(instrs) is the terminator.

The result has the same outcome as the input on every run that ends. A run
that loops forever in code with no marked statement may end after the
transform: ADCE assumes that such loops end.
"""

import toyir

EXIT = "<exit>"  # the virtual exit node; no label of the toy IR looks like this


def may_trap(ins):
    """True if the operation can trap in the toy IR: a division or remainder
    by a divisor that may be zero, or a shift by a count that may be outside
    0 to 63."""
    if ins[0] != "op":
        return False
    op, b = ins[2], ins[4]
    if op in ("/", "%"):
        return not (isinstance(b, int) and b != 0)
    if op in ("<<", ">>"):
        return not (isinstance(b, int) and 0 <= b <= 63)
    return False


def address_taken(prog):
    return {ins[2] for blk in prog.blocks.values() for ins in blk.instrs if ins[0] == "addr"}


def critical(ins, taken):
    """A statement that must stay whatever the rest of the program does."""
    if ins[0] in ("store", "call"):
        return True
    if ins[0] == "alloc":
        # The toy IR numbers heap cells in the order of the allocations, so
        # deleting one would rename the cells that later allocations get.
        return True
    if may_trap(ins):
        return True
    # A load or a call can read an address-taken name through a pointer,
    # which no reaching definition shows.
    return ins[1] in taken


def reachable(prog):
    seen = {prog.entry}
    stack = [prog.entry]
    while stack:
        v = stack.pop()
        for w in toyir.succs(prog, v):
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def postdominators(prog, labels):
    """The immediate post-dominator of each block of labels, with a virtual
    exit EXIT after every ret block. Uses the iterative algorithm of Cooper,
    Harvey and Kennedy on the reverse graph."""
    # Successors in the reverse graph: the predecessors, and for EXIT the
    # ret blocks.
    rsucc = {b: [] for b in labels}
    rsucc[EXIT] = []
    for b in labels:
        ss = toyir.succs(prog, b)
        if not ss:
            rsucc[EXIT].append(b)
        for s in ss:
            rsucc[s].append(b)
    order = []
    seen = {EXIT}
    stack = [(EXIT, iter(rsucc[EXIT]))]
    while stack:
        v, it = stack[-1]
        w = next(it, None)
        if w is None:
            order.append(v)
            stack.pop()
        elif w not in seen:
            seen.add(w)
            stack.append((w, iter(rsucc[w])))
    missing = [b for b in labels if b not in seen]
    if missing:
        raise ValueError("block %r reaches no ret; ADCE needs every block to reach an exit" % missing[0])
    num = {v: i for i, v in enumerate(order)}  # postorder numbers
    rpo = order[::-1]
    ipdom = {EXIT: EXIT}

    def intersect(a, b):
        while a != b:
            while num[a] < num[b]:
                a = ipdom[a]
            while num[b] < num[a]:
                b = ipdom[b]
        return a

    changed = True
    while changed:
        changed = False
        for v in rpo:
            if v is EXIT:
                continue
            new = None
            # The reverse-graph predecessors of v are its CFG successors.
            for p in toyir.succs(prog, v) or [EXIT]:
                if p in ipdom:
                    new = p if new is None else intersect(p, new)
            if ipdom.get(v) != new:
                ipdom[v] = new
                changed = True
    return ipdom


def control_dependence(prog, labels, ipdom):
    """cd[y] is the set of blocks c whose branch y is control dependent on:
    y post-dominates a successor of c and does not strictly post-dominate c.
    This is the reverse dominance frontier of y."""
    cd = {b: set() for b in labels}
    for c in labels:
        ss = toyir.succs(prog, c)
        if len(ss) < 2:
            continue
        for s in ss:
            runner = s
            while runner != ipdom[c]:
                cd[runner].add(c)
                runner = ipdom[runner]
    return cd


def reaching_uses(prog, labels):
    """For each statement (label, i), the set of statements (label, j) that
    define a name it reads and reach it along some path with no other
    definition of that name. Parameters have no defining statement."""
    sites = {}
    for b in labels:
        for i, ins in enumerate(prog.blocks[b].instrs):
            x = toyir.defs(ins)
            if x is not None:
                sites.setdefault(x, set()).add((b, i))
    gen, kill = {}, {}
    for b in labels:
        last = {}
        for i, ins in enumerate(prog.blocks[b].instrs):
            x = toyir.defs(ins)
            if x is not None:
                last[x] = (b, i)
        gen[b] = set(last.values())
        kill[b] = set().union(*(sites[x] for x in last)) if last else set()
    allpred = toyir.preds(prog)
    pred = {b: [p for p in allpred[b] if p in labels] for b in labels}
    inn = {b: set() for b in labels}
    out = {b: set(gen[b]) for b in labels}
    changed = True
    while changed:
        changed = False
        for b in labels:
            i = set().union(*(out[p] for p in pred[b])) if pred[b] else set()
            o = gen[b] | (i - kill[b])
            inn[b] = i
            if o != out[b]:
                out[b] = o
                changed = True
    result = {}
    for b in labels:
        blk = prog.blocks[b]
        cur = {}
        for d in inn[b]:
            x = toyir.defs(prog.blocks[d[0]].instrs[d[1]])
            cur.setdefault(x, set()).add(d)
        for i, ins in enumerate(blk.instrs):
            r = set()
            for u in toyir.uses(ins):
                r |= cur.get(u, set())
            result[(b, i)] = r
            x = toyir.defs(ins)
            if x is not None:
                cur[x] = {(b, i)}
        r = set()
        for u in toyir.term_uses(blk.term):
            r |= cur.get(u, set())
        result[(b, len(blk.instrs))] = r
    return result


def mark(prog):
    """The marked statements, and the analysis results the sweep needs."""
    for blk in prog.blocks.values():
        for ins in blk.instrs:
            if ins[0] == "phi":
                raise ValueError("this ADCE works on programs without phi-functions")
    labels = [b for b in prog.blocks if b in reachable(prog)]
    ipdom = postdominators(prog, labels)  # @line L1
    cd = control_dependence(prog, labels, ipdom)
    reach = reaching_uses(prog, labels)
    taken = address_taken(prog)
    marked = set()  # @line L2
    work = []
    for b in labels:  # @line L3
        blk = prog.blocks[b]
        for i, ins in enumerate(blk.instrs):
            if critical(ins, taken):  # @line L4
                marked.add((b, i))
                work.append((b, i))
        if blk.term[0] == "ret":
            marked.add((b, len(blk.instrs)))
            work.append((b, len(blk.instrs)))
    while work:  # @line L5
        s = work.pop()  # @line L6
        for d in reach[s]:  # @line L7
            if d not in marked:  # @line L8
                marked.add(d)
                work.append(d)
        for c in cd[s[0]]:  # @line L9
            t = (c, len(prog.blocks[c].instrs))
            if t not in marked:  # @line L10
                marked.add(t)
                work.append(t)
    return marked, labels, ipdom


def adce(prog):
    marked, labels, ipdom = mark(prog)
    useful = {b for (b, _) in marked}
    blocks = {}
    for b in labels:  # @line L11
        blk = prog.blocks[b]
        instrs = [ins for i, ins in enumerate(blk.instrs) if (b, i) in marked]  # @line L12
        term = blk.term
        if term[0] == "br" and (b, len(blk.instrs)) not in marked:  # @line L13
            n = ipdom[b]  # @line L14
            while n not in useful:
                if n is EXIT:
                    raise AssertionError("an unmarked branch has no useful post-dominator")
                n = ipdom[n]
            term = ("jump", n)  # @line L15
        blocks[b] = toyir.Block(instrs, term)
    out = toyir.Program(list(prog.params), blocks)
    live = reachable(out)  # @line L16
    out.blocks = {b: blk for b, blk in out.blocks.items() if b in live}
    return out  # @line L17
