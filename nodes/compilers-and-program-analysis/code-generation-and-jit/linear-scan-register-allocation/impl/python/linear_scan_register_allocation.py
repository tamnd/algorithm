# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-scan-register-allocation/. The authors are listed in prov/5E24WB.jsonl.
"""Linear scan register allocation (Poletto and Sarkar, 1999).

linear_scan(iv, k) works on intervals: iv maps each name to (start, end),
with start <= end, both ends included. It returns (reg, spilled): reg maps
each kept name to a register number in 0 .. k-1, and spilled is the set of
names that get no register.

allocate(prog, k) works on a toy IR program with const, copy and op
instructions only (no phi). It numbers the instructions in block order,
builds one interval per name, runs linear_scan and rewrites the program.
It returns (out, reg, spilled). The names in out are the registers
r0 .. r(k-1), the two scratch registers s0 and s1 that hold spilled values
for one instruction, and memory slots whose names start with "mem.". The
parameters of out are the memory slots of the parameters of prog.
"""

import toyir

MEM = "mem."
SCRATCH = ("s0", "s1")


def is_mem(name):
    return isinstance(name, str) and name.startswith(MEM)


# ---------------------------------------------------------- interval level


def linear_scan(iv, k):
    if k < 0:
        raise ValueError("k must be at least 0")
    reg = {}
    spilled = set()
    active = []  # @line L4 (kept sorted by end)
    free = list(range(k))  # @line L5
    order = sorted(iv, key=lambda x: (iv[x][0], iv[x][1], x))

    def end_key(x):
        return (iv[x][1], iv[x][0], x)

    def expire_old(start):
        for j in list(active):  # @line L10
            if iv[j][1] >= start:  # @line L11
                return
            active.remove(j)  # @line L12
            free.append(reg[j])
            free.sort()

    for i in order:  # @line L6
        start, end = iv[i]
        expire_old(start)  # @line L7
        if len(active) == k:  # @line L8
            # SPILL-AT: of the k + 1 intervals that contain start, drop the
            # one that ends last.
            if k > 0:
                s = active[-1]  # @line L13
            if k > 0 and end_key(s) > end_key(i):  # @line L14
                reg[i] = reg.pop(s)
                spilled.add(s)
                active.pop()
                active.append(i)
                active.sort(key=end_key)
            else:
                spilled.add(i)  # @line L15
        else:
            reg[i] = free.pop(0)  # @line L9
            active.append(i)
            active.sort(key=end_key)
    return reg, spilled


def max_overlap(iv):
    """The largest number of intervals that contain one point."""
    events = []
    for s, e in iv.values():
        events.append((s, 0))
        events.append((e, 1))
    best = cur = 0
    for _, kind in sorted(events):
        if kind == 0:
            cur += 1
            best = max(best, cur)
        else:
            cur -= 1
    return best


# ----------------------------------------------------------- program level


def _check(prog):
    for b in prog.blocks.values():
        for ins in b.instrs:
            if ins[0] not in ("const", "copy", "op"):
                raise ValueError("only const, copy and op instructions: %r" % (ins,))


def liveness(prog):
    """live_in and live_out of each block, by the backward fixed point."""
    use, kill = {}, {}
    for label, b in prog.blocks.items():
        u, d = set(), set()
        for ins in b.instrs:
            u.update(a for a in toyir.uses(ins) if a not in d)
            d.add(ins[1])
        u.update(a for a in toyir.term_uses(b.term) if a not in d)
        use[label], kill[label] = u, d
    live_in = {label: set() for label in prog.blocks}
    live_out = {label: set() for label in prog.blocks}
    changed = True
    while changed:
        changed = False
        for label in reversed(list(prog.blocks)):
            out = set()
            for s in toyir.succs(prog, label):
                out |= live_in[s]
            new_in = use[label] | (out - kill[label])
            if out != live_out[label] or new_in != live_in[label]:
                live_out[label], live_in[label] = out, new_in
                changed = True
    return live_in, live_out


def linear_order(prog):
    """The instructions and terminators in block order, as a list of
    (label, item, is_term). Item n reads at 2n and writes at 2n + 1."""
    out = []
    for label, b in prog.blocks.items():
        for ins in b.instrs:
            out.append((label, ins, False))
        out.append((label, b.term, True))
    return out


def live_before(prog):
    """For each item n of linear_order, the names live just before it."""
    _, live_out = liveness(prog)
    order = linear_order(prog)
    result = [None] * len(order)
    n = len(order) - 1
    for label in reversed(list(prog.blocks)):
        b = prog.blocks[label]
        live = set(live_out[label]) | set(toyir.term_uses(b.term))
        result[n] = set(live)
        n -= 1
        for ins in reversed(b.instrs):
            live.discard(ins[1])
            live.update(toyir.uses(ins))
            result[n] = set(live)
            n -= 1
    return result


def intervals(prog):
    """One interval per name that is not a memory slot: from the first to
    the last position where the name is defined (2n + 1) or live before an
    item (2n)."""
    order = linear_order(prog)  # @line L1
    live = live_before(prog)  # @line L2
    pos = {}
    for n, (_, item, is_term) in enumerate(order):  # @line L3
        for x in live[n]:
            if not is_mem(x):
                pos.setdefault(x, []).append(2 * n)
        if not is_term and not is_mem(item[1]):
            pos.setdefault(item[1], []).append(2 * n + 1)
    return {x: (min(p), max(p)) for x, p in pos.items()}


def _names(prog):
    out = set(prog.params)
    for b in prog.blocks.values():
        for ins in b.instrs:
            out.add(ins[1])
            out.update(toyir.uses(ins))
        out.update(toyir.term_uses(b.term))
    return out


def prepare(prog):
    """A copy of prog whose arguments arrive in memory slots. A new entry
    block loads each parameter that is live on entry, then jumps to the old
    entry."""
    _check(prog)
    if any(is_mem(a) for a in _names(prog)):
        raise ValueError("names that start with %r are reserved" % MEM)
    live_in, _ = liveness(prog)
    label = "start"
    while label in prog.blocks:
        label += "_"
    pro = [("copy", p, MEM + p) for p in prog.params if p in live_in[prog.entry]]
    blocks = {label: toyir.Block(pro, ("jump", prog.entry))}
    for lab, b in prog.blocks.items():
        blocks[lab] = toyir.Block(list(b.instrs), b.term)
    return toyir.Program([MEM + p for p in prog.params], blocks)


def rewrite(prog, reg, spilled):
    """Replace each name by its location. A spilled name x lives in mem.x:
    each use loads it into a scratch register first, and each definition
    computes into s0 and then stores s0 into mem.x."""

    def loc(a):
        if not isinstance(a, str) or is_mem(a):
            return a
        if a in spilled:
            return MEM + a
        return "r%d" % reg[a]

    blocks = {}
    for label, b in prog.blocks.items():
        out = []
        for ins in b.instrs:
            x = loc(ins[1])
            if ins[0] == "const":
                out.append(("const", x, ins[2]))
                continue
            srcs = [ins[2]] if ins[0] == "copy" else [ins[3], ins[4]]
            locs = [loc(a) for a in srcs]
            if ins[0] == "copy":
                a = locs[0]
                if a == x:
                    continue
                if is_mem(a) and is_mem(x):
                    out += [("copy", "s0", a), ("copy", x, "s0")]
                else:
                    out.append(("copy", x, a))
                continue
            loaded = {}
            for a in locs:
                if is_mem(a) and a not in loaded:
                    loaded[a] = SCRATCH[len(loaded)]
                    out.append(("copy", loaded[a], a))
            a, c = (loaded.get(v, v) for v in locs)
            if is_mem(x):
                out += [("op", "s0", ins[2], a, c), ("copy", x, "s0")]
            else:
                out.append(("op", x, ins[2], a, c))
        term = b.term
        if term[0] in ("br", "ret") and is_mem(loc(term[1])):
            out.append(("copy", "s0", loc(term[1])))
            term = (term[0], "s0") + term[2:]
        elif term[0] in ("br", "ret"):
            term = (term[0], loc(term[1])) + term[2:]
        blocks[label] = toyir.Block(out, term)
    return toyir.Program(list(prog.params), blocks)


def allocate(prog, k):
    work = prepare(prog)
    iv = intervals(work)
    reg, spilled = linear_scan(iv, k)
    return rewrite(work, reg, spilled), reg, spilled  # @line L16
