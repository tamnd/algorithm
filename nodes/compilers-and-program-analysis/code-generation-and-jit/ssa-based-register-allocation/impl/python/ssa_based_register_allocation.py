# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ssa-based-register-allocation/. The authors are listed in prov/C6A8K4.jsonl.
"""SSA-based register allocation in the style of Hack, Grund and Goos.

allocate(prog, k) takes a toy IR program in strict SSA form, with const,
copy, op and phi instructions, and k >= 1 registers. It works in three
phases:

1. spill: keep whole names in memory slots until at most k names that are
   not spilled hold a value at each node;
2. color: walk the blocks in a preorder of the dominator tree and give each
   definition the lowest register that no live name holds (or the register
   of its copy or phi partner, when that one is free);
3. leave SSA: replace the phis of each block by a parallel copy at the end
   of each predecessor, made sequential with the scratch register s0 for
   cycles and s1 for moves from memory to memory.

It returns (out, color, spilled). out has no phis, and its names are the
registers r0 .. r(k-1), the scratch registers s0 and s1, and memory slots
whose names start with "mem.". Its parameters are the slots of the
parameters of prog.

A node is a group of phis of one block, an ordinary instruction or a
terminator. nodes(prog) lists, for each block, its nodes as (defs, out),
where out is the set of names live just after the node. The names of a phi
operand count as read at the end of the predecessor.
"""

import toyir

MEM = "mem."


def is_mem(name):
    return isinstance(name, str) and name.startswith(MEM)


# ------------------------------------------------------------ preparation


def _fresh(prog, base):
    label = base
    while label in prog.blocks:
        label += "_"
    return label


def prepare(prog):
    """Add a start block that loads each live parameter from its slot, and
    split each edge into a block with phis whose source ends in a branch,
    so that every parallel copy can go just before a jump."""
    for b in prog.blocks.values():
        for ins in b.instrs:
            if ins[0] not in ("const", "copy", "op", "phi"):
                raise ValueError("only const, copy, op and phi: %r" % (ins,))
            for a in [ins[1]] + toyir.uses(ins):
                if is_mem(a):
                    raise ValueError("names that start with %r are reserved" % MEM)
    if any(ins[0] == "phi" for ins in prog.blocks[prog.entry].instrs):
        raise ValueError("the entry block must not have phis")
    blocks = {lab: toyir.Block(list(b.instrs), b.term) for lab, b in prog.blocks.items()}
    work = toyir.Program(list(prog.params), blocks)
    for lab in list(blocks):
        term = blocks[lab].term
        if term[0] != "br":
            continue
        for target in toyir.succs(work, lab):
            if not any(ins[0] == "phi" for ins in blocks[target].instrs):
                continue
            mid = _fresh(work, "%s_%s" % (lab, target))
            blocks[mid] = toyir.Block([], ("jump", target))
            term = (term[0], term[1]) + tuple(mid if t == target else t for t in term[2:])
            blocks[target].instrs = [
                ("phi", ins[1], {(mid if p == lab else p): a for p, a in ins[2].items()}) if ins[0] == "phi" else ins
                for ins in blocks[target].instrs
            ]
        blocks[lab].term = term
    live_in, _ = liveness(work)
    start = _fresh(work, "start")
    pro = [("copy", p, MEM + p) for p in prog.params if p in live_in[work.entry]]
    out = {start: toyir.Block(pro, ("jump", work.entry))}
    out.update(blocks)
    return toyir.Program([MEM + p for p in prog.params], out)


# --------------------------------------------------------------- liveness


def _phis(b):
    return [ins for ins in b.instrs if ins[0] == "phi"]


def _body(b):
    return [ins for ins in b.instrs if ins[0] != "phi"]


def liveness(prog):
    """live_in and live_out of each block for SSA form: live_in excludes the
    phis of the block, and live_out includes the phi operands that the block
    sends to its successors."""
    use, kill, phiuse, phidef = {}, {}, {}, {}
    for label, b in prog.blocks.items():
        u, d = set(), set()
        for ins in _body(b):
            u.update(a for a in toyir.uses(ins) if a not in d)
            d.add(ins[1])
        u.update(a for a in toyir.term_uses(b.term) if a not in d)
        use[label], kill[label] = u, d
        phidef[label] = {ins[1] for ins in _phis(b)}
        phiuse[label] = set()
    for label, b in prog.blocks.items():
        for ins in _phis(b):
            for p, a in ins[2].items():
                if isinstance(a, str):
                    phiuse[p].add(a)
    live_in = {label: set() for label in prog.blocks}
    live_out = {label: set() for label in prog.blocks}
    changed = True
    while changed:
        changed = False
        for label in reversed(list(prog.blocks)):
            out = set(phiuse[label])
            for s in toyir.succs(prog, label):
                out |= live_in[s]
            new_in = (use[label] | (out - kill[label])) - phidef[label]
            if out != live_out[label] or new_in != live_in[label]:
                live_out[label], live_in[label] = out, new_in
                changed = True
    return live_in, live_out


def nodes(prog):
    """For each block, its nodes in order as (defs, out). The phi group comes
    first (when the block has phis), then the instructions, then the
    terminator."""
    _, live_out = liveness(prog)
    result = {}
    for label, b in prog.blocks.items():
        live = set(live_out[label])
        rev = [((), frozenset(live))]
        live |= set(toyir.term_uses(b.term))
        for ins in reversed(_body(b)):
            rev.append(((ins[1],), frozenset(live)))
            live.discard(ins[1])
            live.update(toyir.uses(ins))
        phis = _phis(b)
        if phis:
            rev.append((tuple(ins[1] for ins in phis), frozenset(live)))
        result[label] = list(reversed(rev))
    return result


def max_live(prog, spilled=()):
    """The largest number of names that are not spilled in defs | out of one
    node."""
    best = 0
    for ns in nodes(prog).values():
        for defs, out in ns:
            best = max(best, len((set(defs) | out) - set(spilled)))
    return best


# ------------------------------------------------------------- dominators


def dominator_preorder(prog):
    """The blocks in a preorder of the dominator tree (iterative dominators
    of Cooper, Harvey and Kennedy on the reverse postorder)."""
    entry = prog.entry
    order, seen = [], {entry}
    stack = [(entry, iter(toyir.succs(prog, entry)))]
    while stack:
        v, it = stack[-1]
        w = next(it, None)
        if w is None:
            order.append(v)
            stack.pop()
        elif w not in seen:
            seen.add(w)
            stack.append((w, iter(toyir.succs(prog, w))))
    rpo = list(reversed(order))
    index = {v: i for i, v in enumerate(rpo)}
    pred = toyir.preds(prog)
    idom = {entry: entry}

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
        for v in rpo[1:]:
            ps = [p for p in pred[v] if p in idom]
            new = ps[0]
            for p in ps[1:]:
                new = meet(p, new)
            if idom.get(v) != new:
                idom[v] = new
                changed = True
    children = {v: [] for v in rpo}
    for v in rpo[1:]:
        children[idom[v]].append(v)
    out, stack = [], [entry]
    while stack:
        v = stack.pop()
        out.append(v)
        stack.extend(reversed(children[v]))
    return out


# ----------------------------------------------------------------- phases


def spill_costs(prog):
    """The number of definitions and uses of each name, phi operands included."""
    cost = {}
    for b in prog.blocks.values():
        for ins in b.instrs:
            for a in [ins[1]] + toyir.uses(ins):
                cost[a] = cost.get(a, 0) + 1
        for a in toyir.term_uses(b.term):
            cost[a] = cost.get(a, 0) + 1
    return cost


def spill(prog, k):
    """Spill whole names until each node has at most k names that are not
    spilled in defs | out. The name chosen at an overfull node is the one
    with the least cost; ties go to the one that is overfull at the most
    nodes, then to the name order."""
    ns = [(set(d) | out) - {a for a in set(d) | out if is_mem(a)} for v in nodes(prog).values() for d, out in v]  # @line L2
    cost = spill_costs(prog)
    spilled = set()  # @line L3
    while True:
        over = [s - spilled for s in ns if len(s - spilled) > k]  # @line L4
        if not over:
            return spilled
        count = {}
        for s in over:
            for x in s:
                count[x] = count.get(x, 0) + 1
        x = min(over[0], key=lambda a: (cost[a], -count[a], a))  # @line L5
        spilled.add(x)  # @line L6


def color(prog, spilled):
    """Color the names that are not spilled, in a preorder of the dominator
    tree. Returns the color of each such name."""
    color = {}
    ns = nodes(prog)
    partner = {}
    for b in prog.blocks.values():
        for ins in b.instrs:
            if ins[0] == "copy" and isinstance(ins[2], str):
                partner[ins[1]] = [ins[2]]
            elif ins[0] == "phi":
                partner[ins[1]] = [a for a in ins[2].values() if isinstance(a, str)]
    for label in dominator_preorder(prog):  # @line L7
        for defs, out in ns[label]:  # @line L8
            busy = {color[z] for z in out if z not in defs and z not in spilled and not is_mem(z)}  # @line L9
            for y in defs:  # @line L10
                if y in spilled or is_mem(y):
                    continue
                pref = [color[a] for a in partner.get(y, []) if a in color and color[a] not in busy]
                c = pref[0] if pref else min(set(range(len(busy) + 1)) - busy)  # @line L11
                color[y] = c
                busy.add(c)  # @line L12
    return color


def sequentialize(moves):
    """Turn a parallel copy, a list of (dst, src) with distinct dst, into a
    list of instructions. A cycle is broken by saving one destination in s0;
    a move from memory to memory goes through s1."""
    moves = [(d, s) for d, s in moves if d != s]
    out = []

    def emit(d, s):
        if isinstance(s, int):
            out.append(("const", d, s))
        elif is_mem(d) and is_mem(s):
            out.extend([("copy", "s1", s), ("copy", d, "s1")])
        else:
            out.append(("copy", d, s))

    while moves:
        srcs = {s for _, s in moves if isinstance(s, str)}
        for i, (d, s) in enumerate(moves):
            if d not in srcs:
                emit(d, s)
                moves.pop(i)
                break
        else:
            # Every destination is still read, so only cycles are left.
            d = moves[0][0]  # @line L15
            out.append(("copy", "s0", d))
            moves = [(dd, "s0" if ss == d else ss) for dd, ss in moves]
    return out


def _rewrite_body(instrs, loc):
    out = []
    for ins in instrs:
        x = loc(ins[1])
        if ins[0] == "const":
            out.append(("const", x, ins[2]))
            continue
        locs = [loc(a) for a in ([ins[2]] if ins[0] == "copy" else [ins[3], ins[4]])]
        if ins[0] == "copy":
            if locs[0] != x:
                if is_mem(locs[0]) and is_mem(x):
                    out += [("copy", "s0", locs[0]), ("copy", x, "s0")]
                else:
                    out.append(("copy", x, locs[0]))
            continue
        loaded = {}
        for a in locs:
            if is_mem(a) and a not in loaded:
                loaded[a] = ("s0", "s1")[len(loaded)]
                out.append(("copy", loaded[a], a))
        a, c = (loaded.get(v, v) for v in locs)
        if is_mem(x):
            out += [("op", "s0", ins[2], a, c), ("copy", x, "s0")]
        else:
            out.append(("op", x, ins[2], a, c))
    return out


def allocate(prog, k):
    if k < 1:
        raise ValueError("k must be at least 1")
    work = prepare(prog)  # @line L1
    spilled = spill(work, k)
    col = color(work, spilled)

    def loc(a):
        if not isinstance(a, str) or is_mem(a):
            return a
        return MEM + a if a in spilled else "r%d" % col[a]

    copies = {label: [] for label in work.blocks}
    for label, b in work.blocks.items():  # @line L13
        for ins in _phis(b):
            for p, a in ins[2].items():
                copies[p].append((loc(ins[1]), loc(a)))  # @line L14
    blocks = {}
    for label, b in work.blocks.items():
        body = _rewrite_body(_body(b), loc)
        term = b.term
        if copies[label]:
            if term[0] != "jump":
                raise AssertionError("prepare split this edge")
            body += sequentialize(copies[label])
        if term[0] in ("br", "ret"):
            a = loc(term[1])
            if is_mem(a):
                body.append(("copy", "s0", a))
                a = "s0"
            term = (term[0], a) + term[2:]
        blocks[label] = toyir.Block(body, term)
    return toyir.Program(list(work.params), blocks), col, spilled  # @line L16
