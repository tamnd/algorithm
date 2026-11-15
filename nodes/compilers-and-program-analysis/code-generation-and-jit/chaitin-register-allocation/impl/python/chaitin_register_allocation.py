# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chaitin-register-allocation/. The authors are listed in prov/D7BWHP.jsonl.
"""Chaitin's graph coloring register allocator.

chaitin_color(adj, k, cost) works on a graph: adj maps each node to the set
of its neighbors. It returns (color, spilled). When spilled is empty, color
maps every node to a color in 0 .. k-1 and no edge has two equal colors.
Otherwise color is empty and spilled is the set of nodes that the simplify
phase chose to spill.

allocate(prog, k) works on a toy IR program with const, copy and op
instructions only (no phi). It builds the interference graph, colors it,
spills the chosen names everywhere and repeats. It returns
(out, rounds, spilled): out runs like prog, its register names are
r0 .. r(k-1), and its memory slots have names that start with "mem.".
The parameters of out are the memory slots of the parameters of prog.
"""

from collections import deque
import math

import toyir

MEM = "mem."


def is_mem(name):
    return isinstance(name, str) and name.startswith(MEM)


# ------------------------------------------------------------- graph level


def simplify(adj, k, cost):
    """The simplify phase. Returns the stack as a list of (node, chosen),
    in the order of removal; chosen is True for a spill choice."""
    order = list(adj)
    index = {v: i for i, v in enumerate(order)}
    deg = {v: len(adj[v]) for v in order}
    removed = set()
    low = deque(v for v in order if deg[v] < k)
    queued = set(low)
    stack = []  # @line L6
    while len(stack) < len(order):  # @line L7
        if low:  # @line L8
            v, chosen = low.popleft(), False  # @line L9
        else:  # @line L10
            # Every node left has degree >= k: choose the cheapest per edge.
            v = min((u for u in order if u not in removed), key=lambda u: (cost[u] / deg[u], index[u]))  # @line L11
            chosen = True  # @line L12
        removed.add(v)
        stack.append((v, chosen))
        for w in sorted(adj[v], key=index.__getitem__):
            if w not in removed:
                deg[w] -= 1
                if deg[w] < k and w not in queued:
                    queued.add(w)
                    low.append(w)
    return stack


def chaitin_color(adj, k, cost=None):
    if k < 1:
        raise ValueError("k must be at least 1")
    if cost is None:
        cost = {v: 1 for v in adj}
    stack = simplify(adj, k, cost)
    spilled = {v for v, chosen in stack if chosen}
    if spilled:  # @line L13
        return {}, spilled
    color = {}
    for v, _ in reversed(stack):  # @line L14
        used = {color[w] for w in adj[v] if w in color}
        c = 0
        while c in used:
            c += 1
        color[v] = c  # @line L15 (c < k: v had fewer than k neighbors left when it was removed)
    return color, set()


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


def interference(prog):
    """The interference graph of the names that are not memory slots, and
    the list of copies (x, y) for x = y between two such names. At each
    definition of x, x interferes with each name live after it, except the
    source of a copy x = y."""
    _check(prog)
    _, live_out = liveness(prog)
    adj = {}
    moves = []
    for b in prog.blocks.values():
        for ins in b.instrs:
            for a in [ins[1]] + toyir.uses(ins):
                if not is_mem(a):
                    adj.setdefault(a, set())
        for a in toyir.term_uses(b.term):
            if not is_mem(a):
                adj.setdefault(a, set())
    for label, b in prog.blocks.items():
        live = set(live_out[label]) | set(toyir.term_uses(b.term))
        for ins in reversed(b.instrs):
            x = ins[1]
            src = ins[2] if ins[0] == "copy" and isinstance(ins[2], str) else None
            if not is_mem(x):
                for y in live:
                    if y != x and y != src and not is_mem(y):
                        adj[x].add(y)
                        adj[y].add(x)
                if src is not None and src != x and not is_mem(src):
                    moves.append((x, src))
            live.discard(x)
            live.update(toyir.uses(ins))
    return adj, moves


def spill_costs(prog, infinite=()):
    """The number of definitions and uses of each name; a name in infinite
    (a spill temporary) gets an infinite cost, so it is never chosen."""
    cost = {}
    for b in prog.blocks.values():
        for ins in b.instrs:
            for a in [ins[1]] + toyir.uses(ins):
                cost[a] = cost.get(a, 0) + 1
        for a in toyir.term_uses(b.term):
            cost[a] = cost.get(a, 0) + 1
    for a in infinite:
        cost[a] = math.inf
    return cost


def _names(prog):
    out = set(prog.params)
    for b in prog.blocks.values():
        for ins in b.instrs:
            out.add(ins[1])
            out.update(toyir.uses(ins))
        out.update(toyir.term_uses(b.term))
    return out


def _sub(a, m):
    return m.get(a, a) if isinstance(a, str) else a


def spill_everywhere(prog, spilled):
    """Keep each name x of spilled in the memory slot mem.x. Each use reads a
    new temporary loaded just before it; each definition writes a new
    temporary stored just after it. Returns (program, temporaries)."""
    taken = _names(prog)
    temps = set()
    count = [0]

    def temp(x):
        while True:
            count[0] += 1
            t = "%s.%d" % (x, count[0])
            if t not in taken:
                taken.add(t)
                temps.add(t)
                return t

    blocks = {}
    for label, b in prog.blocks.items():
        out = []
        for ins in b.instrs:
            loads = {}
            for a in toyir.uses(ins):
                if a in spilled and a not in loads:
                    loads[a] = temp(a)
                    out.append(("copy", loads[a], MEM + a))
            if ins[0] == "copy":
                ins = ("copy", ins[1], _sub(ins[2], loads))
            elif ins[0] == "op":
                ins = ("op", ins[1], ins[2], _sub(ins[3], loads), _sub(ins[4], loads))
            x = ins[1]
            if x in spilled:
                t = temp(x)
                out.append((ins[0], t) + ins[2:])
                out.append(("copy", MEM + x, t))
            else:
                out.append(ins)
        term = b.term
        if term[0] in ("br", "ret") and term[1] in spilled:
            t = temp(term[1])
            out.append(("copy", t, MEM + term[1]))
            term = (term[0], t) + term[2:]
        blocks[label] = toyir.Block(out, term)
    return toyir.Program(list(prog.params), blocks), temps


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


def assign(prog, color):
    """Rename each name to its register; drop copies that become r = r."""

    def reg(a):
        if not isinstance(a, str) or is_mem(a):
            return a
        return "r%d" % color[a]

    blocks = {}
    for label, b in prog.blocks.items():
        out = []
        for ins in b.instrs:
            if ins[0] == "const":
                out.append(("const", reg(ins[1]), ins[2]))
            elif ins[0] == "copy":
                x, a = reg(ins[1]), reg(ins[2])
                if x != a:
                    out.append(("copy", x, a))
            else:
                out.append(("op", reg(ins[1]), ins[2], reg(ins[3]), reg(ins[4])))
        term = b.term
        if term[0] in ("br", "ret"):
            term = (term[0], reg(term[1])) + term[2:]
        blocks[label] = toyir.Block(out, term)
    return toyir.Program(list(prog.params), blocks)


def allocate(prog, k):
    """Build, simplify, spill and repeat until the graph is k-colorable by
    simplify alone. Each round spills at least one name that is not a spill
    temporary, so the number of rounds is at most the number of names + 1."""
    if k < 2:
        raise ValueError("k must be at least 2: one instruction can read two spilled names")
    work = prepare(prog)  # @line L1
    infinite = set()  # @line L2
    spilled_all = []
    rounds = 0
    while True:  # @line L3
        rounds += 1
        adj, _ = interference(work)  # @line L4
        cost = spill_costs(work, infinite)  # @line L5
        color, spilled = chaitin_color(adj, k, cost)
        if not spilled:
            return assign(work, color), rounds, spilled_all  # @line L16
        work, temps = spill_everywhere(work, spilled)  # @line L17
        infinite |= temps  # @line L18
        spilled_all.extend(sorted(spilled))
