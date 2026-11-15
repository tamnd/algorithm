# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterated-register-coalescing/. The authors are listed in prov/ZBH45M.jsonl.
"""Iterated register coalescing (George and Appel).

irc_color(adj, moves, k, cost, test) works on a graph: adj maps each node to
the set of its neighbors and moves is a list of pairs (x, y), one for each
copy. It returns (color, spilled, coalesced). color maps each node that got
a color to a color in 0 .. k-1, spilled is the set of nodes left without a
color, and coalesced is the list of the indices of the moves whose two ends
got one node. test is the coalescing rule: "briggs", "george", "either"
(the move passes one of the two) or "aggressive" (any move whose ends do
not interfere). There are no precolored nodes.

briggs_ok, george_ok and merge apply the two tests and the merge to a
fixed graph. allocate(prog, k, test) is the full allocator for toy IR
programs with const, copy and op instructions; it returns
(out, rounds, spilled) as the allocators of the Chaitin and Briggs pages do.
"""

import math

import toyir

MEM = "mem."


def is_mem(name):
    return isinstance(name, str) and name.startswith(MEM)


# ------------------------------------------------------- tests on one graph


def merge(adj, a, b):
    """The graph with b merged into a. a and b must not be adjacent."""
    if b in adj[a]:
        raise ValueError("cannot merge two adjacent nodes")
    out = {v: set(ws) for v, ws in adj.items() if v != b}
    for w in adj[b]:
        out[w].discard(b)
        out[w].add(a)
        out[a].add(w)
    return out


def briggs_ok(adj, a, b, k):
    """Briggs: the merged node has fewer than k neighbors of degree >= k,
    with the degrees taken in the merged graph."""
    m = merge(adj, a, b)
    return sum(1 for w in m[a] if len(m[w]) >= k) < k


def george_ok(adj, a, b, k):
    """George, for merging a into b: each neighbor of a is a neighbor of b
    or has degree < k."""
    return all(w in adj[b] or len(adj[w]) < k for w in adj[a])


# -------------------------------------------------------------- the worklists


def _merged_cost(a, b):
    # A spill temporary has an infinite cost; a node that holds any other
    # name keeps the finite part, so it stays a possible spill choice.
    if a == math.inf:
        return b
    if b == math.inf:
        return a
    return a + b


def irc_color(adj, moves, k, cost=None, test="briggs"):
    if k < 1:
        raise ValueError("k must be at least 1")
    if test not in ("briggs", "george", "either", "aggressive"):
        raise ValueError("unknown test %r" % test)
    order = list(adj)
    index = {v: i for i, v in enumerate(order)}
    cost = dict(cost) if cost is not None else {v: 1 for v in order}
    graph = {v: set(adj[v]) for v in order}
    degree = {v: len(adj[v]) for v in order}
    move_list = {v: set() for v in order}
    for i, (x, y) in enumerate(moves):
        if x != y:
            move_list[x].add(i)
            move_list[y].add(i)
    worklist_moves = {i: None for i, (x, y) in enumerate(moves) if x != y}
    active = set()
    alias = {}
    gone = set()  # nodes on the stack or coalesced
    stack = []  # @line L6
    chosen = set()
    simplify_wl, freeze_wl, spill_wl = {}, {}, {}
    coalesced_moves = []

    def get_alias(n):
        while n in alias:
            n = alias[n]
        return n

    def adjacent(n):
        return sorted((w for w in graph[n] if w not in gone), key=index.__getitem__)

    def node_moves(n):
        return [i for i in sorted(move_list[n]) if i in active or i in worklist_moves]

    def place(n):
        """Put n in the one worklist that its degree and its moves call for."""
        if n in gone or n in chosen:
            return
        for wl in (simplify_wl, freeze_wl, spill_wl):
            wl.pop(n, None)
        if degree[n] >= k:
            spill_wl[n] = None
        elif node_moves(n):
            freeze_wl[n] = None
        else:
            simplify_wl[n] = None

    def enable_moves(nodes):
        for n in nodes:
            for i in node_moves(n):
                if i in active:
                    active.discard(i)
                    worklist_moves[i] = None

    def decrement_degree(m):
        degree[m] -= 1
        if degree[m] == k - 1:
            enable_moves([m] + adjacent(m))
        place(m)

    def add_edge(u, v):
        if v not in graph[u]:
            graph[u].add(v)
            graph[v].add(u)
            degree[u] += 1
            degree[v] += 1

    def ok(u, v):
        if test == "aggressive":
            return True
        nu, nv = set(adjacent(u)), set(adjacent(v))
        if test in ("briggs", "either"):
            high = sum(1 for t in nu | nv if degree[t] - (t in nu and t in nv) >= k)
            if high < k:
                return True
        if test in ("george", "either"):
            if all(t in nv or degree[t] < k for t in nu):
                return True
            if all(t in nu or degree[t] < k for t in nv):
                return True
        return False

    def combine(u, v):
        for wl in (simplify_wl, freeze_wl, spill_wl):
            wl.pop(v, None)
        gone.add(v)
        alias[v] = u
        move_list[u] |= move_list[v]
        cost[u] = _merged_cost(cost[u], cost[v])
        enable_moves([v])
        for t in adjacent(v):
            add_edge(t, u)
            decrement_degree(t)
        place(u)

    def freeze_moves(u):
        for i in node_moves(u):
            x, y = get_alias(moves[i][0]), get_alias(moves[i][1])
            v = x if y == get_alias(u) else y
            active.discard(i)
            worklist_moves.pop(i, None)
            place(v)

    for v in order:
        place(v)
    while simplify_wl or worklist_moves or freeze_wl or spill_wl:  # @line L7
        if simplify_wl:  # @line L8
            n = next(iter(simplify_wl))
            del simplify_wl[n]
            stack.append(n)  # @line L9
            gone.add(n)
            for m in adjacent(n):
                decrement_degree(m)
        elif worklist_moves:  # @line L10
            i = next(iter(worklist_moves))
            del worklist_moves[i]
            u, v = get_alias(moves[i][0]), get_alias(moves[i][1])  # @line L11
            if u == v:  # @line L12
                coalesced_moves.append(i)
                place(u)
            elif v in graph[u]:  # @line L13
                place(u)
                place(v)
            elif ok(u, v):  # @line L14
                coalesced_moves.append(i)
                combine(u, v)
            else:
                active.add(i)  # @line L15
        elif freeze_wl:  # @line L16
            u = next(iter(freeze_wl))
            del freeze_wl[u]
            simplify_wl[u] = None
            freeze_moves(u)  # @line L17
            place(u)
        else:  # @line L18
            m = min(spill_wl, key=lambda u: (cost[u] / degree[u], index[u]))  # @line L19
            del spill_wl[m]
            chosen.add(m)
            simplify_wl[m] = None
            freeze_moves(m)

    color = {}
    actual = set()  # @line L20
    while stack:  # @line L21
        n = stack.pop()
        used = {color[get_alias(w)] for w in graph[n] if get_alias(w) in color}
        c = 0
        while c in used:
            c += 1
        if c < k:  # @line L22
            color[n] = c  # @line L23
        else:
            assert n in chosen  # a node that simplify removed always finds a color
            actual.add(n)  # @line L24
    for n in order:
        if n in alias and get_alias(n) in color:
            color[n] = color[get_alias(n)]
    spilled = {n for n in order if get_alias(n) in actual}
    return color, spilled, sorted(coalesced_moves)


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
    the list of copies (x, y) for x = y between two such names. A copy does
    not make its two names interfere."""
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
            src = ins[2] if ins[0] == "copy" else None
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
    """Keep each name x of spilled in the memory slot mem.x: load a new
    temporary before each use, store a new temporary after each definition.
    Returns (program, temporaries)."""
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
    """A copy of prog whose arguments arrive in memory slots: a new entry
    block loads each parameter that is live on entry."""
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
    """Rename each name to its register; drop copies that become r = r,
    which removes every coalesced copy."""

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


def allocate(prog, k, test="briggs"):
    """Build, run the worklists, spill and repeat. Each spilled node holds
    a name that is not a spill temporary, so the rounds end."""
    if k < 2:
        raise ValueError("k must be at least 2: one instruction can read two spilled names")
    work = prepare(prog)  # @line L1
    infinite = set()  # @line L2
    spilled_all = []
    rounds = 0
    while True:  # @line L3
        rounds += 1
        adj, moves = interference(work)  # @line L4
        cost = spill_costs(work, infinite)  # @line L5
        color, spilled, _ = irc_color(adj, moves, k, cost, test)
        if not spilled:  # @line L25
            return assign(work, color), rounds, spilled_all  # @line L26
        work, temps = spill_everywhere(work, spilled)  # @line L27
        infinite |= temps  # @line L28
        spilled_all.extend(sorted(spilled))
