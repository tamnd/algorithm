# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/program-dependence-graph/. The authors are listed in prov/AK2XM4.jsonl.
"""The program dependence graph of a toy IR procedure.

Control dependence follows Ferrante, Ottenstein and Warren (1987): the CFG
gets a node START with edges to the entry block and to a node EXIT, and an
edge from every ret block to EXIT. For each edge (a, b) where b is not the
immediate post-dominator of a, the walk from b up the post-dominator tree to
ipdom(a), not included, gives the nodes that are control dependent on a
through the edge (a, b). Data dependence is flow dependence: an edge from a
definition to each use that it reaches, found by reaching definitions.

A PDG node is ("ENTRY",) for START and the parameters, or (label, i): the
instruction i of the block, where i = len(instrs) is the terminator.
"""

import toyir

START = "START"
EXIT = "EXIT"
ENTRY = ("ENTRY",)


def idoms(nodes, succ, root):
    """Immediate dominators by the Cooper-Harvey-Kennedy iteration.

    nodes: all nodes; succ: dict node -> list of nodes; root: the start.
    Returns a dict from each node that root reaches to its immediate
    dominator; root maps to itself.
    """
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
    pred = {v: [] for v in nodes}
    for v in nodes:
        for w in succ[v]:
            pred[w].append(v)
    order = sorted(po, key=lambda v: -po[v])
    dom = {root: root}

    def intersect(a, b):
        while a != b:
            while po[a] < po[b]:
                a = dom[a]
            while po[b] < po[a]:
                b = dom[b]
        return a

    changed = True
    while changed:
        changed = False
        for b in order[1:]:
            ps = [p for p in pred[b] if p in dom]
            new = ps[0]
            for p in ps[1:]:
                new = intersect(p, new)
            if dom.get(b) != new:
                dom[b] = new
                changed = True
    return dom


def augmented_cfg(prog):
    """The CFG with START and EXIT, as (nodes, succ). The edge START -> EXIT
    makes the blocks that run on every run control dependent on START."""
    nodes = [START] + list(prog.blocks) + [EXIT]
    succ = {START: [prog.entry, EXIT], EXIT: []}
    for label in prog.blocks:
        s = toyir.succs(prog, label)
        succ[label] = s if s else [EXIT]
    return nodes, succ


def post_dominator_tree(nodes, succ, exit_node):
    """ipdom as a dict: dominators of the reversed graph, rooted at the exit."""
    rsucc = {v: [] for v in nodes}
    for v in nodes:
        for w in succ[v]:
            rsucc[w].append(v)
    return idoms(nodes, rsucc, exit_node)


def control_dependences(nodes, succ, exit_node):
    """The set of triples (x, y, s): y is control dependent on x through the
    edge x -> s. Every node must reach exit_node."""
    ipdom = post_dominator_tree(nodes, succ, exit_node)
    out = set()
    for a in nodes:
        for b in succ[a]:
            if b == ipdom.get(a):
                continue
            runner = b
            while runner != ipdom[a]:
                out.add((a, runner, b))
                runner = ipdom[runner]
    return out


def block_control_dependences(prog):
    nodes, succ = augmented_cfg(prog)
    return control_dependences(nodes, succ, EXIT)


def reaching_definitions(prog):
    """IN sets per block: sets of (node, var). The parameters are defined at
    ENTRY."""
    gen, kill_vars = {}, {}
    for label, b in prog.blocks.items():
        last = {}
        for i, ins in enumerate(b.instrs):
            d = toyir.defs(ins)
            if d is not None:
                last[d] = (label, i)
        gen[label] = {(n, v) for v, n in last.items()}
        kill_vars[label] = set(last)
    preds = toyir.preds(prog)
    inn = {label: set() for label in prog.blocks}
    out = {label: set(gen[label]) for label in prog.blocks}
    boundary = {(ENTRY, p) for p in prog.params}
    changed = True
    while changed:
        changed = False
        for label in prog.blocks:
            s = set(boundary) if label == prog.entry else set()
            for p in preds[label]:
                s |= out[p]
            inn[label] = s
            o = gen[label] | {(n, v) for (n, v) in s if v not in kill_vars[label]}
            if o != out[label]:
                out[label] = o
                changed = True
    return inn


def data_dependences(prog):
    """The set of triples (d, u, v): the definition of v at node d reaches the
    node u, which reads v."""
    inn = reaching_definitions(prog)  # @line L9
    out = set()
    for label, b in prog.blocks.items():  # @line L10
        cur = {}
        for n, v in inn[label]:  # @line L11
            cur.setdefault(v, set()).add(n)
        items = list(b.instrs) + [b.term]
        for i, ins in enumerate(items):  # @line L12
            used = toyir.term_uses(ins) if i == len(b.instrs) else toyir.uses(ins)
            for v in used:
                for d in cur.get(v, ()):
                    out.add((d, (label, i), v))  # @line L13
            if i < len(b.instrs):
                d = toyir.defs(ins)
                if d is not None:
                    cur[d] = {(label, i)}  # @line L14
    return out


class PDG:
    """The nodes and the two kinds of edges.

    block_cd: set of (x, y, s): block y is control dependent on x through the
    CFG edge x -> s; x may be START.
    control: set of (x, y, s): node y is control dependent on the branch
    node x, through the CFG edge to block s; x is ENTRY for START.
    data: set of (d, u, v), flow dependences.
    """

    def __init__(self, prog):
        self.prog = prog
        self.nodes = [ENTRY]
        for label, b in prog.blocks.items():
            self.nodes += [(label, i) for i in range(len(b.instrs) + 1)]
        nodes, succ = augmented_cfg(prog)  # @line L1
        ipdom = post_dominator_tree(nodes, succ, EXIT)  # @line L2
        self.block_cd, self.control = set(), set()
        for a in nodes:
            for b in succ[a]:  # @line L3
                if b == ipdom.get(a):
                    continue
                y = b  # @line L4
                while y != ipdom[a]:  # @line L5
                    src = ENTRY if a == START else (a, len(prog.blocks[a].instrs))  # @line L6
                    self.block_cd.add((a, y, b))
                    for i in range(len(prog.blocks[y].instrs) + 1):
                        self.control.add((src, (y, i), b))  # @line L7
                    y = ipdom[y]  # @line L8
        self.data = data_dependences(prog)

    def control_parents(self, node):
        return {(x, s) for x, y, s in self.control if y == node}

    def data_parents(self, node):
        return {(d, v) for d, u, v in self.data if u == node}

    def slice(self, node):
        """The backward slice: every node from which node is reachable."""
        into = {}
        for x, y, _ in self.control:
            into.setdefault(y, []).append(x)
        for d, u, _ in self.data:
            into.setdefault(u, []).append(d)
        seen, stack = {node}, [node]  # @line L15
        while stack:  # @line L16
            z = stack.pop()  # @line L17
            for x in into.get(z, ()):  # @line L18
                if x not in seen:
                    seen.add(x)
                    stack.append(x)
        return seen  # @line L19
