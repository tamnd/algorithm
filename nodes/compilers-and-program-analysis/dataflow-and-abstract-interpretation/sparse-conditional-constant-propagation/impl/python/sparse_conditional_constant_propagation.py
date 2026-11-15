# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-conditional-constant-propagation/. The authors are listed in prov/WNK50T.jsonl.
"""Sparse conditional constant propagation (Wegman and Zadeck) on the toy IR.

The analysis runs on SSA form. to_ssa builds pruned SSA form by the method
of Cytron et al.: phi-functions at the iterated dominance frontier of the
blocks that assign a variable, kept only where the variable is live, then
renaming by a walk of the dominator tree. The k-th definition of v is named
v.k, and a parameter keeps its own name for its value on entry.

The lattice is flat, in the meet convention: TOP (no value seen yet) is the
start value, an int is a constant, BOT means "not a constant". sccp keeps
two worklists, one of CFG edges and one of SSA edges, and evaluates an
instruction only when its block is reachable through executable edges.
rewrite applies the result: it folds constants, turns a branch on a known
condition into a jump, and drops the blocks that no executable edge reaches.
"""

from collections import Counter, deque

import toyir
from toyir import Block, Program

TOP = "top"  # no value seen yet
BOT = "bot"  # not a constant


def is_const(v):
    return isinstance(v, int)


def meet(a, b):
    if a == TOP:
        return b
    if b == TOP or a == b:
        return a
    return BOT


def fold(op, a, b):
    """The abstract value of a op b. Any TOP operand gives TOP, else any BOT
    operand gives BOT, else the operation runs; an operation that traps
    gives BOT, because the instruction must stay in the program."""
    if a == TOP or b == TOP:
        return TOP
    if a == BOT or b == BOT:
        return BOT
    try:
        return toyir._binop(op, a, b)
    except toyir._Trap:
        return BOT


# ------------------------------------------------------------ SSA construction


def _reachable_order(succ, root):
    """Postorder of the blocks that root reaches."""
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
    """Cooper, Harvey and Kennedy. Only the blocks that root reaches are keys."""
    order = _reachable_order(succ, root)
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


def dominance_frontiers(succ, idom):
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


def live_in(prog, labels, succ):
    """The variables that are live on entry to each block (backward round robin)."""
    gen, kill = {}, {}
    for b in labels:
        g, k = set(), set()
        for ins in prog.blocks[b].instrs:
            g |= {a for a in toyir.uses(ins) if a not in k}
            k.add(ins[1])
        g |= {a for a in toyir.term_uses(prog.blocks[b].term) if a not in k}
        gen[b], kill[b] = g, k
    live = {b: set() for b in labels}
    changed = True
    while changed:
        changed = False
        for b in reversed(labels):
            out = set()
            for s in succ[b]:
                out |= live[s]
            new = gen[b] | (out - kill[b])
            if new != live[b]:
                live[b] = new
                changed = True
    return live


def to_ssa(prog):
    """Pruned SSA form with the same runs. The unreachable blocks are dropped.
    A name that some path reads before any definition gets v.0 = 0 at the top
    of the entry, so the result is strict."""
    succ = {b: toyir.succs(prog, b) for b in prog.blocks}
    root = prog.entry
    for b in prog.blocks.values():
        for ins in b.instrs:
            if ins[0] not in ("const", "copy", "op", "call"):
                raise ValueError("unsupported instruction: %r" % (ins,))
            if "." in ins[1]:
                raise ValueError("names must not contain a dot: %r" % ins[1])
    idom = immediate_dominators(succ, root)
    labels = [b for b in prog.blocks if b in idom]
    if any(root in succ[b] for b in labels):
        raise ValueError("the entry must have no predecessor")
    df = dominance_frontiers(succ, idom)
    live = live_in(prog, labels, succ)

    sites = {}
    for p in prog.params:
        sites.setdefault(p, {root})
    for b in labels:
        for ins in prog.blocks[b].instrs:
            sites.setdefault(ins[1], set()).add(b)
    phis = {b: [] for b in labels}
    for v, s in sites.items():
        has_phi, work = set(), list(s)
        while work:
            x = work.pop()
            for y in df[x]:
                if y not in has_phi and v in live[y]:
                    has_phi.add(y)
                    phis[y].append(v)
                    work.append(y)

    children = {b: [] for b in labels}
    for b in labels:
        if idom[b] is not None:
            children[idom[b]].append(b)
    counter = Counter()
    stacks = {v: [] for v in sites}
    for p in prog.params:
        stacks[p].append(p)
    undefined = []

    def top(v):
        if stacks.get(v):
            return stacks[v][-1]
        name = v + ".0"
        if name not in undefined:
            undefined.append(name)
        return name

    def operand(a):
        return top(a) if isinstance(a, str) else a

    def fresh(v):
        counter[v] += 1
        name = "%s.%d" % (v, counter[v])
        stacks[v].append(name)
        return name

    phi_args = {b: [{} for _ in phis[b]] for b in labels}
    phi_names = {b: [] for b in labels}
    out = {}

    def rename(b):
        pushed = []
        for v in phis[b]:
            phi_names[b].append(fresh(v))
            pushed.append(v)
        instrs = []
        for ins in prog.blocks[b].instrs:
            if ins[0] == "const":
                new = ("const", None, ins[2])
            elif ins[0] == "copy":
                new = ("copy", None, operand(ins[2]))
            elif ins[0] == "op":
                new = ("op", None, ins[2], operand(ins[3]), operand(ins[4]))
            else:
                new = ("call", None, ins[2], [operand(a) for a in ins[3]])
            instrs.append(new[:1] + (fresh(ins[1]),) + new[2:])
            pushed.append(ins[1])
        t = prog.blocks[b].term
        if t[0] == "br":
            t = ("br", operand(t[1]), t[2], t[3])
        elif t[0] == "ret":
            t = ("ret", operand(t[1]))
        for s in succ[b]:
            for v, args in zip(phis[s], phi_args[s]):
                args[b] = top(v)
        out[b] = (instrs, t)
        for c in children[b]:
            rename(c)
        for v in pushed:
            stacks[v].pop()

    rename(root)
    preds = {b: [p for p in labels if b in succ[p]] for b in labels}
    blocks = {}
    for b in labels:
        instrs, t = out[b]
        head = [("phi", x, {p: args[p] for p in preds[b]}) for x, args in zip(phi_names[b], phi_args[b])]
        if b == root:
            head = [("const", name, 0) for name in undefined] + head
        blocks[b] = Block(head + instrs, t)
    return Program(list(prog.params), blocks)


# ------------------------------------------------------------------- SCCP


def sccp(prog):
    """Analyse a program in SSA form. Returns (value, executable, visited,
    stats): the lattice value of every name, the executable CFG edges (the
    pseudo edge (None, entry) included), the reachable blocks, and counters.
    stats["ssa_pushes"] counts how often each SSA edge (name, use site) was
    put on the SSA worklist; stats["changes"] counts how often each value
    went down."""
    blocks = prog.blocks
    uses_of = {}
    value = {p: BOT for p in prog.params}  # @line L1
    for b, blk in blocks.items():
        for i, ins in enumerate(blk.instrs):
            if ins[1] in value:
                raise ValueError("not in SSA form: %r has two definitions" % ins[1])
            value[ins[1]] = TOP  # @line L1
            for a in set(toyir.uses(ins)):  # one SSA edge per (name, use site)
                uses_of.setdefault(a, []).append((b, i))
        for a in toyir.term_uses(blk.term):
            uses_of.setdefault(a, []).append((b, None))
    executable, visited, pushed = set(), set(), set()  # @line L2
    flow = deque([(None, prog.entry)])  # @line L3
    pushed.add((None, prog.entry))
    ssa = deque()
    stats = {"ssa_pushes": Counter(), "changes": Counter(), "flow_pops": 0, "ssa_pops": 0, "evals": 0}

    def val(a):
        return a if isinstance(a, int) else value[a]

    def add_edge(e):
        if e not in pushed:
            pushed.add(e)
            flow.append(e)

    def evaluate(b, i):
        stats["evals"] += 1
        if i is None:
            t = blocks[b].term
            if t[0] == "jump":
                add_edge((b, t[1]))  # @line L15
            elif t[0] == "br":
                c = val(t[1])
                if c == BOT:
                    add_edge((b, t[2]))  # @line L14
                    add_edge((b, t[3]))
                elif c != TOP:
                    add_edge((b, t[2] if c != 0 else t[3]))  # @line L14
            return
        ins = blocks[b].instrs[i]
        k, x = ins[0], ins[1]
        if k == "phi":
            new = TOP
            for p, a in ins[2].items():
                if (p, b) in executable:
                    new = meet(new, val(a))  # @line L11
        elif k == "const":
            new = ins[2]
        elif k == "copy":
            new = val(ins[2])
        elif k == "op":
            new = fold(ins[2], val(ins[3]), val(ins[4]))  # @line L12
        else:
            new = BOT  # a call: nothing is known about its result
        if new != value[x]:  # @line L13
            value[x] = new
            stats["changes"][x] += 1
            for s in uses_of.get(x, ()):
                stats["ssa_pushes"][(x, s)] += 1
                ssa.append((x, s))

    while flow or ssa:  # @line L4
        if flow:  # @line L5
            e = flow.popleft()  # @line L6
            stats["flow_pops"] += 1
            p, b = e
            executable.add(e)  # @line L7
            first = b not in visited
            visited.add(b)
            for i, ins in enumerate(blocks[b].instrs):
                if ins[0] == "phi" or first:  # @line L7
                    evaluate(b, i)  # @line L8
            if first:
                evaluate(b, None)  # @line L8
        else:
            x, (b, i) = ssa.popleft()  # @line L9
            stats["ssa_pops"] += 1
            if b in visited:
                evaluate(b, i)  # @line L10
    return value, executable, visited, stats


def rewrite(prog, value, executable, visited):
    """Apply an SCCP result: names with a constant value become constants, a
    branch on a constant becomes a jump, unreachable blocks and the phi
    operands of non-executable edges go away."""

    def opnd(a):
        if isinstance(a, str) and is_const(value[a]):
            return value[a]
        return a

    blocks = {}
    for b, blk in prog.blocks.items():
        if b not in visited:
            continue
        phis, folded, rest = [], [], []
        for ins in blk.instrs:
            k, x = ins[0], ins[1]
            if k != "call" and is_const(value[x]):
                (folded if k == "phi" else rest).append(("const", x, value[x]))
            elif k == "phi":
                phis.append(("phi", x, {p: opnd(a) for p, a in ins[2].items() if (p, b) in executable}))
            elif k == "copy":
                rest.append(("copy", x, opnd(ins[2])))
            elif k == "op":
                rest.append(("op", x, ins[2], opnd(ins[3]), opnd(ins[4])))
            else:
                rest.append(("call", x, ins[2], [opnd(a) for a in ins[3]]))
        t = blk.term
        if t[0] == "br":
            c = opnd(t[1])
            if is_const(c):
                t = ("jump", t[2] if c != 0 else t[3])
            else:
                t = ("br", c, t[2], t[3])
        elif t[0] == "ret":
            t = ("ret", opnd(t[1]))
        blocks[b] = Block(phis + folded + rest, t)
    return Program(list(prog.params), blocks)


def sparse_conditional_constant_propagation(prog):
    """SSA construction, analysis and rewrite in one call. Returns the
    optimised SSA program and the lattice value of every SSA name."""
    ssa = to_ssa(prog)
    value, executable, visited, _ = sccp(ssa)
    return rewrite(ssa, value, executable, visited), value
