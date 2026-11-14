# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sea-of-nodes/. The authors are listed in prov/Q4NRFR.jsonl.
"""A small sea-of-nodes graph for the toy IR, after Click and Paleczny (1995).

build(prog) turns a toy IR procedure with const, copy and op instructions
into a graph. Control is a chain of nodes: Start, one Region per block, If
with IfTrue and IfFalse projections, and Return. Data nodes are Param,
Const, Undef, Phi and Op. A Phi has its Region as input 0 and one value per
input of the Region. An Op that cannot trap floats: it has no control input,
and equal floating Ops are made once (hash-consing, which is global value
numbering at creation). An Op that can trap (/, %, <<, >>) is pinned to the
Region of its block and kept alive, because the trap is an effect.

schedule(graph) places every live floating node in a block by global code
motion (Click 1995): as early as its inputs allow, as late as its uses
allow, and then in the block of least loop depth between the two. It gives
back a toy IR program in SSA form with phi instructions.
"""

import toyir

TRAPPING = ("/", "%", "<<", ">>")


class Node:
    __slots__ = ("id", "kind", "inputs", "val")

    def __init__(self, nid, kind, inputs, val=None):
        self.id = nid
        self.kind = kind
        self.inputs = inputs
        self.val = val

    def __repr__(self):
        return "%s%d" % (self.kind, self.id)


class Graph:
    """The nodes, the region of each block and the roots."""

    def __init__(self):
        self.nodes = []
        self.table = {}  # hash-cons table for Const and floating Op
        self.region = {}  # block label -> Region node
        self.term = {}  # block label -> ("jump", L) / ("br", If, L1, L2) / ("ret", Return)
        self.label_of = {}  # Region id -> block label
        self.params = []
        self.entry = None
        self.roots = []

    def new(self, kind, inputs, val=None):
        n = Node(len(self.nodes), kind, inputs, val)
        self.nodes.append(n)
        return n

    def hashcons(self, kind, inputs, val):
        key = (kind, val, tuple(i.id for i in inputs))
        n = self.table.get(key)
        if n is None:
            n = self.new(kind, inputs, val)
            self.table[key] = n
        return n

    def pinned(self, n):
        return n.kind not in ("Const", "Undef", "Op") or (n.kind == "Op" and n.val in TRAPPING)


def _rpo(prog):
    order, seen = [], {prog.entry}
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
    return order[::-1]


def build(prog):
    """The sea-of-nodes graph of prog. The entry block must have no
    predecessor, every block must be reachable, and the instructions must be
    const, copy and op."""
    preds = toyir.preds(prog)
    if preds[prog.entry]:
        raise ValueError("the entry block must have no predecessor")
    names = set(prog.params)
    for b in prog.blocks.values():
        for ins in b.instrs:
            if ins[0] not in ("const", "copy", "op"):
                raise ValueError("unsupported instruction: %r" % (ins,))
            names.add(ins[1])
    names = sorted(names)
    g = Graph()
    g.params, g.entry = list(prog.params), prog.entry
    start = g.new("Start", [])
    for label in prog.blocks:  # @line L1
        g.region[label] = g.new("Region", [])
        g.label_of[g.region[label].id] = label
    order = _rpo(prog)
    if len(order) != len(prog.blocks):
        raise ValueError("every block must be reachable from the entry")
    out, phis, proj = {}, {}, {}
    for label in order:  # @line L2
        reg = g.region[label]
        if label == prog.entry:  # @line L3
            reg.inputs = [start]
            env = {v: g.hashcons("Undef", [], None) for v in names}
            for i, p in enumerate(prog.params):
                env[p] = g.new("Param", [start], p)
        elif len(preds[label]) == 1:  # @line L4
            env = dict(out[preds[label][0]])
        else:
            env = {v: g.new("Phi", [reg]) for v in names}  # @line L5
            phis[label] = dict(env)

        def value(a):
            return g.hashcons("Const", [], a) if isinstance(a, int) else env[a]

        for ins in prog.blocks[label].instrs:  # @line L6
            if ins[0] == "const":
                env[ins[1]] = value(ins[2])
            elif ins[0] == "copy":
                env[ins[1]] = value(ins[2])
            elif ins[2] in TRAPPING:
                n = g.new("Op", [reg, value(ins[3]), value(ins[4])], ins[2])  # @line L7
                g.roots.append(n)
                env[ins[1]] = n
            else:
                n = g.hashcons("Op", [value(ins[3]), value(ins[4])], ins[2])  # @line L8
                env[ins[1]] = n  # @line L9
        t = prog.blocks[label].term  # @line L10
        if t[0] == "ret":
            r = g.new("Return", [reg, value(t[1])])
            g.roots.append(r)
            g.term[label] = ("ret", r)
        elif t[0] == "br" and t[2] != t[3]:
            iff = g.new("If", [reg, value(t[1])])
            g.roots.append(iff)
            proj[(label, t[2])] = g.new("IfTrue", [iff])
            proj[(label, t[3])] = g.new("IfFalse", [iff])
            g.term[label] = ("br", iff, t[2], t[3])
        else:
            target = t[1] if t[0] == "jump" else t[2]
            proj[(label, target)] = reg
            g.term[label] = ("jump", target)
        out[label] = env  # @line L11
    for label in prog.blocks:  # @line L12
        if label == prog.entry:
            continue
        ps = preds[label]
        g.region[label].inputs = [proj[(p, label)] for p in ps]  # @line L13
        if label in phis:
            for v, phi in phis[label].items():
                phi.inputs = [g.region[label]] + [out[p][v] for p in ps]  # @line L14
    _remove_trivial_phis(g)
    return g


def _remove_trivial_phis(g):
    """A phi whose inputs, other than itself, are all one node v is replaced
    by v everywhere. Repeat until no such phi is left."""
    changed = True
    while changed:
        changed = False
        for n in g.nodes:
            if n.kind != "Phi":
                continue
            vals = {i.id: i for i in n.inputs[1:] if i is not n}
            if len(vals) == 1:  # @line L15
                v = next(iter(vals.values()))
                n.kind, n.inputs = "Dead", []
                for m in g.nodes:
                    m.inputs = [v if i is n else i for i in m.inputs]
                g.roots = [v if r is n else r for r in g.roots]
                changed = True


# ------------------------------------------------------------ scheduling


def _control_block(g, n):
    """The block of a control node or of a node pinned by a control input."""
    while n.kind != "Region":
        if n.kind == "Start":
            return g.entry
        n = n.inputs[0]
    return g.label_of[n.id]


def _dominators(labels, succ, root):
    """idom and depth in the dominator tree, by the Cooper-Harvey-Kennedy
    iteration."""
    po, seen, stack = {}, {root}, [(root, iter(succ[root]))]
    while stack:
        v, it = stack[-1]
        w = next(it, None)
        if w is None:
            po[v] = len(po)
            stack.pop()
        elif w not in seen:
            seen.add(w)
            stack.append((w, iter(succ[w])))
    pred = {v: [] for v in labels}
    for v in labels:
        for w in succ[v]:
            pred[w].append(v)
    order = sorted(po, key=lambda v: -po[v])
    idom = {root: root}

    def intersect(a, b):
        while a != b:
            while po[a] < po[b]:
                a = idom[a]
            while po[b] < po[a]:
                b = idom[b]
        return a

    changed = True
    while changed:
        changed = False
        for b in order[1:]:
            ps = [p for p in pred[b] if p in idom]
            new = ps[0]
            for p in ps[1:]:
                new = intersect(p, new)
            if idom.get(b) != new:
                idom[b] = new
                changed = True
    depth = {root: 0}
    for b in order[1:]:
        depth[b] = depth[idom[b]] + 1
    return idom, depth


def _loop_depth(labels, succ, idom, depth):
    """The number of natural loops that hold each block. A loop is the set of
    blocks that reach the tail t of a back edge t -> h, where h dominates t,
    without passing through h."""
    pred = {v: [] for v in labels}
    for v in labels:
        for w in succ[v]:
            pred[w].append(v)

    def dominates(a, b):
        while depth[b] > depth[a]:
            b = idom[b]
        return a == b

    loops = {}
    for t in labels:
        for h in succ[t]:
            if dominates(h, t):
                body = loops.setdefault(h, {h})
                stack = [t]
                while stack:
                    v = stack.pop()
                    if v not in body:
                        body.add(v)
                        stack.extend(pred[v])
    ld = {v: 0 for v in labels}
    for body in loops.values():
        for v in body:
            ld[v] += 1
    return ld


def schedule(g, prog_labels):
    """Place the live nodes and give back a toy IR program. prog_labels is the
    list of block labels in the order to print them, the entry first."""
    succ = {}
    for label in prog_labels:
        t = g.term[label]
        succ[label] = [] if t[0] == "ret" else ([t[1]] if t[0] == "jump" else [t[2], t[3]])
    idom, depth = _dominators(prog_labels, succ, g.entry)  # @line L16
    loop = _loop_depth(prog_labels, succ, idom, depth)

    def lca(a, b):
        if a is None:
            return b
        while depth[a] > depth[b]:
            a = idom[a]
        while depth[b] > depth[a]:
            b = idom[b]
        while a != b:
            a, b = idom[a], idom[b]
        return a

    live, stack = set(), list(g.roots)
    for n in stack:
        live.add(n.id)
    while stack:
        n = stack.pop()
        for i in n.inputs:
            if i.id not in live:
                live.add(i.id)
                stack.append(i)
    nodes = [n for n in g.nodes if n.id in live]
    uses = {n.id: [] for n in nodes}
    for n in nodes:
        for k, i in enumerate(n.inputs):
            uses[i.id].append((n, k))

    block = {}
    for n in nodes:  # @line L17
        if g.pinned(n):
            block[n.id] = _control_block(g, n.inputs[0] if n.kind in ("Phi", "Op", "If", "Return", "Param") else n)

    early = {}

    def schedule_early(n):  # @line L18
        if n.id in early:
            return early[n.id]
        if n.id in block:
            early[n.id] = block[n.id]
        else:
            best = g.entry
            for i in n.inputs:
                b = schedule_early(i)
                if depth[b] > depth[best]:
                    best = b
            early[n.id] = best
        return early[n.id]

    for n in nodes:
        schedule_early(n)

    def use_block(u, k):
        if u.kind == "Phi" and k > 0:
            region = u.inputs[0]
            return _control_block(g, region.inputs[k - 1])
        return schedule_late(u)

    def schedule_late(n):  # @line L19
        if n.id in block:
            return block[n.id]
        here = None  # @line L20
        for u, k in uses[n.id]:
            here = lca(here, use_block(u, k))  # @line L21
        best, x = here, here
        while True:  # @line L22
            if loop[x] < loop[best]:
                best = x
            if x == early[n.id]:
                break
            x = idom[x]
        block[n.id] = best  # @line L23
        return best

    for n in nodes:
        schedule_late(n)

    def name(n):
        if n.kind == "Param":
            return n.val
        if n.kind == "Const":
            return n.val
        if n.kind == "Undef":
            return 0
        return "v%d" % n.id

    for p in g.params:
        if p.startswith("v") and p[1:].isdigit():
            raise ValueError("parameter name %r clashes with node names" % p)
    placed = {label: [] for label in prog_labels}
    for n in nodes:
        if n.kind in ("Phi", "Op"):
            placed[block[n.id]].append(n)
    blocks = {}
    for label in prog_labels:  # @line L24
        instrs = []
        region = g.region[label]
        for n in placed[label]:
            if n.kind == "Phi":
                ops = {}
                for k, c in enumerate(region.inputs):
                    ops[_control_block(g, c)] = name(n.inputs[k + 1])
                instrs.append(("phi", name(n), ops))
        done = set()

        def emit(n):
            if n.id in done or n.kind != "Op" or block[n.id] != label:
                return
            done.add(n.id)
            ins = n.inputs[1:] if n.val in TRAPPING else n.inputs
            for i in ins:
                emit(i)
            instrs.append(("op", name(n), n.val, name(ins[0]), name(ins[1])))

        for n in placed[label]:
            emit(n)
        t = g.term[label]
        if t[0] == "ret":
            term = ("ret", name(t[1].inputs[1]))
        elif t[0] == "br":
            term = ("br", name(t[1].inputs[1]), t[2], t[3])
        else:
            term = ("jump", t[1])
        blocks[label] = toyir.Block(instrs, term)
    return toyir.Program(list(g.params), blocks), block


def roundtrip(prog):
    """Build the graph of prog and schedule it back."""
    g = build(prog)
    out, _ = schedule(g, list(prog.blocks))
    return out
