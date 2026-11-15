# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ssa-linear-scan/. The authors are listed in prov/SBG2CF.jsonl.
"""Linear scan register allocation on SSA form, after Wimmer and Franz.

allocate(prog, k) takes a toy IR program in strict SSA form with a
reducible control flow graph, with const, copy, op and phi instructions,
and k >= 1 registers. It

1. orders the blocks so that each block comes after its dominators and the
   blocks of each loop are contiguous;
2. builds a lifetime interval with holes (a list of ranges) for each name in
   one backward pass over the blocks, with no liveness fixed point: a name
   live at a loop header gets a range over the whole loop;
3. scans the intervals by start with the sets active and inactive (an
   inactive interval is in a hole), and gives each interval a register that
   no interval it intersects holds, or spills the interval that ends last;
4. replaces the phis by parallel copies at the ends of the predecessors.

This version never splits an interval: a name is in one register for its
whole life, or in its slot mem.x. It returns (out, reg, spilled), where reg
maps each kept name to its register number. The output uses r0 .. r(k-1),
the scratch registers s0 and s1, and slots, and its parameters are the slots
of the parameters of prog.

Positions: the blocks get the positions in order. A block b starts at an
even position b.start where its phis write, its items (instructions and the
terminator) get the next even positions, and b.end is two after the last
item, which is also the start of the next block. A range [a, e) is half
open. An item at position p reads its operands at the end of a range that
stops at p and writes its result at the start of a range that starts at p.
"""

import toyir

MEM = "mem."


def is_mem(name):
    return isinstance(name, str) and name.startswith(MEM)


def _phis(b):
    return [ins for ins in b.instrs if ins[0] == "phi"]


def _body(b):
    return [ins for ins in b.instrs if ins[0] != "phi"]


# ------------------------------------------------------------ preparation


def _fresh(blocks, base):
    label = base
    while label in blocks:
        label += "_"
    return label


def prepare(prog):
    """Add a start block that loads each parameter from its slot, and split
    each edge into a block with phis whose source ends in a branch."""
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
    for lab in list(blocks):
        term = blocks[lab].term
        if term[0] != "br" or term[2] == term[3]:
            continue
        for target in (term[2], term[3]):
            if not _phis(blocks[target]):
                continue
            mid = _fresh(blocks, "%s_%s" % (lab, target))
            blocks[mid] = toyir.Block([], ("jump", target))
            term = (term[0], term[1]) + tuple(mid if t == target else t for t in term[2:])
            blocks[target].instrs = [
                ("phi", ins[1], {(mid if p == lab else p): a for p, a in ins[2].items()}) if ins[0] == "phi" else ins
                for ins in blocks[target].instrs
            ]
        blocks[lab].term = term
    start = _fresh(blocks, "start")
    pro = [("copy", p, MEM + p) for p in prog.params]
    out = {start: toyir.Block(pro, ("jump", prog.entry))}
    out.update(blocks)
    return toyir.Program([MEM + p for p in prog.params], out)


# ------------------------------------------------------------- block order


def dominators(prog):
    """Immediate dominators by the iterative method of Cooper, Harvey and
    Kennedy. Unreachable blocks are left out."""
    entry = prog.entry
    post, seen = [], {entry}
    stack = [(entry, iter(toyir.succs(prog, entry)))]
    while stack:
        v, it = stack[-1]
        w = next(it, None)
        if w is None:
            post.append(v)
            stack.pop()
        elif w not in seen:
            seen.add(w)
            stack.append((w, iter(toyir.succs(prog, w))))
    rpo = post[::-1]
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
    return idom, rpo


def dominates(idom, a, b):
    while b != a and idom[b] != b:
        b = idom[b]
    return a == b


def loops(prog, idom, reach):
    """The natural loops, as a dict from header to the set of its blocks.
    Raises ValueError if the graph is not reducible."""
    pred = toyir.preds(prog)
    body = {}
    for u in reach:
        for h in toyir.succs(prog, u):
            if dominates(idom, h, u):
                blocks = body.setdefault(h, {h})
                work = [u]
                while work:
                    v = work.pop()
                    if v not in blocks:
                        blocks.add(v)
                        work.extend(p for p in pred[v] if p in reach)
    # Reducible if and only if the graph without the back edges is acyclic.
    state = {}
    for root in reach:
        if root in state:
            continue
        state[root] = 1
        stack = [(root, iter(toyir.succs(prog, root)))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                state[v] = 2
                stack.pop()
            elif w in body and v in body[w]:
                continue
            elif state.get(w) == 1:
                raise ValueError("the control flow graph is not reducible")
            elif w not in state:
                state[w] = 1
                stack.append((w, iter(toyir.succs(prog, w))))
    return body


def loop_bodies(prog):
    idom, rpo = dominators(prog)
    return loops(prog, idom, set(rpo)), rpo


def block_order(prog):
    """A linear order of the reachable blocks in which every block comes
    after its dominators and the blocks of each loop are contiguous. Each
    loop is first shrunk to its header; the resulting acyclic graph is put
    in reverse postorder; then each header is replaced by the order of its
    own loop, built the same way."""
    body, rpo = loop_bodies(prog)
    rank = {v: i for i, v in enumerate(rpo)}

    def region(blocks, head):
        # top[v] is v, or the header of the largest loop inside this region
        # that holds v.
        top = {}
        for v in blocks:
            around = [h for h, hb in body.items() if h != head and h in blocks and v in hb]
            top[v] = max(around, key=lambda h: len(body[h])) if around else v
        succ = {x: [] for x in set(top.values())}
        for v in sorted(blocks, key=rank.get):
            for w in toyir.succs(prog, v):
                if w in blocks and w != head and top[w] != top[v] and top[w] not in succ[top[v]]:
                    succ[top[v]].append(top[w])
        first = head if head is not None else prog.entry
        post, seen = [], {first}
        stack = [(first, iter(succ[first]))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                post.append(v)
                stack.pop()
            elif w not in seen:
                seen.add(w)
                stack.append((w, iter(succ[w])))
        out = []
        for x in reversed(post):
            out += [x] if x == head or x not in body else region(body[x], x)
        return out

    return region(set(rpo), None)


# --------------------------------------------------------------- intervals


def _add_range(ranges, a, e):
    """Add [a, e) to a sorted list of disjoint ranges, merging touching ones."""
    if a >= e:
        return
    out = []
    for r in ranges:
        if r[1] < a or r[0] > e:
            out.append(r)
        else:
            a, e = min(a, r[0]), max(e, r[1])
    out.append([a, e])
    out.sort()
    ranges[:] = out


def build_intervals(prog, order):
    """Number the positions, then build the ranges of each name in one
    backward pass over the blocks. Returns (ranges, pos, start, end), where
    pos maps (label, j) to the position of item j of the block."""
    pos, start, end = {}, {}, {}
    p = 0
    for lab in order:
        start[lab] = p
        n = len(_body(prog.blocks[lab])) + 1
        for j in range(n):
            pos[(lab, j)] = p + 2 + 2 * j
        p += 2 * n + 2
        end[lab] = p
    body, _ = loop_bodies(prog)
    last = {}
    for h, blocks in body.items():
        last[h] = max(blocks, key=order.index)
    ranges = {}
    live_in = {}
    for lab in reversed(order):  # @line L3
        b = prog.blocks[lab]
        live = set()
        for s in toyir.succs(prog, lab):  # @line L4
            live |= live_in.get(s, set())
            for ins in _phis(prog.blocks[s]):
                a = ins[2][lab]
                if isinstance(a, str):
                    live.add(a)
        for x in live:  # @line L5
            _add_range(ranges.setdefault(x, []), start[lab], end[lab])
        items = _body(b)
        t = b.term
        reads = toyir.term_uses(t)
        for x in reads:
            _add_range(ranges.setdefault(x, []), start[lab], pos[(lab, len(items))])
            live.add(x)
        for j in range(len(items) - 1, -1, -1):  # @line L6
            ins = items[j]
            q = pos[(lab, j)]
            y = ins[1]
            if y in live:  # @line L7
                r = ranges[y][0]
                r[0] = q
                live.discard(y)
            else:
                _add_range(ranges.setdefault(y, []), q, q + 1)
            for x in toyir.uses(ins):  # @line L8
                if not is_mem(x):
                    _add_range(ranges.setdefault(x, []), start[lab], q)
                    live.add(x)
        for ins in _phis(b):  # @line L9
            y = ins[1]
            if y in live:
                live.discard(y)
            else:
                _add_range(ranges.setdefault(y, []), start[lab], start[lab] + 1)
        live_in[lab] = live
        # A name live at a loop header is live in the whole loop, which is
        # contiguous in the order.
        if lab in body:  # @line L10
            for x in live:
                _add_range(ranges[x], start[lab], end[last[lab]])  # @line L11
    return ranges, pos, start, end


def covers(ranges, p):
    return any(a <= p < e for a, e in ranges)


def intersects(r1, r2):
    i = j = 0
    while i < len(r1) and j < len(r2):
        if r1[i][0] < r2[j][1] and r2[j][0] < r1[i][1]:
            return True
        if r1[i][1] <= r2[j][1]:
            i += 1
        else:
            j += 1
    return False


# ------------------------------------------------------------------- scan


def linear_scan(ranges, k):
    """Scan the intervals by start. Returns (reg, spilled)."""
    names = sorted(ranges, key=lambda x: (ranges[x][0][0], x))  # @line L12
    reg, spilled = {}, set()
    active, inactive = [], []
    for cur in names:  # @line L13
        p = ranges[cur][0][0]
        for it in list(active):  # @line L14
            if ranges[it][-1][1] <= p:
                active.remove(it)
            elif not covers(ranges[it], p):
                active.remove(it)
                inactive.append(it)
        for it in list(inactive):  # @line L15
            if ranges[it][-1][1] <= p:
                inactive.remove(it)
            elif covers(ranges[it], p):
                inactive.remove(it)
                active.append(it)
        blocked = {reg[it] for it in inactive if intersects(ranges[it], ranges[cur])}
        busy = {reg[it] for it in active} | blocked  # @line L16
        free = [r for r in range(k) if r not in busy]
        if free:
            reg[cur] = free[0]  # @line L17
            active.append(cur)
            continue
        cands = [it for it in active if reg[it] not in blocked]
        s = max(cands, key=lambda it: (ranges[it][-1][1], ranges[it][0][0], it), default=None)  # @line L18
        if s is not None and ranges[s][-1][1] > ranges[cur][-1][1]:
            reg[cur] = reg.pop(s)  # @line L19
            spilled.add(s)
            active.remove(s)
            active.append(cur)
        else:
            spilled.add(cur)  # @line L20
    return reg, spilled


# ------------------------------------------------------------ phi removal


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
            d = moves[0][0]
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
    order = block_order(work)  # @line L2
    ranges, _, _, _ = build_intervals(work, order)
    reg, spilled = linear_scan(ranges, k)

    def loc(a):
        if not isinstance(a, str) or is_mem(a):
            return a
        return MEM + a if a in spilled else "r%d" % reg[a]

    reached = set(order)
    copies = {lab: [] for lab in work.blocks}
    for lab in order:  # @line L21
        for ins in _phis(work.blocks[lab]):
            for p, a in ins[2].items():
                if p in reached:
                    copies[p].append((loc(ins[1]), loc(a)))
    blocks = {}
    for lab in order:
        b = work.blocks[lab]
        body = _rewrite_body(_body(b), loc)
        term = b.term
        if copies[lab]:
            body += sequentialize(copies[lab])  # @line L22
        if term[0] in ("br", "ret"):
            a = loc(term[1])
            if is_mem(a):
                body.append(("copy", "s0", a))
                a = "s0"
            term = (term[0], a) + term[2:]
        blocks[lab] = toyir.Block(body, term)
    return toyir.Program(list(work.params), blocks), reg, spilled  # @line L23
