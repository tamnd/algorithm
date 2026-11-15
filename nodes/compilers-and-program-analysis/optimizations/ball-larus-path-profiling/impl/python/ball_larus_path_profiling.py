# SPDX-License-Identifier: MIT
"""Ball-Larus path profiling.

A DAG is given as a list of nodes and a list of edges (u, v). Edges are
named by their index in the list, so two edges may join the same pair of
nodes. ENTRY reaches every node and every node reaches EXIT.

number_paths gives each edge a value Val so that the sums of Val along the
N paths from ENTRY to EXIT are exactly 0, 1, ..., N - 1. place_increments
moves the values off the edges of a maximum spanning tree, so that only the
chords carry code, and the sum along every path stays the same.
regenerate turns a path number back into its path.

cfg_to_dag and instrument apply the method to a program of the toy IR
(toyir.py): back edges are cut and replaced by dummy edges, and the
instrumented program keeps the path register in bl.r and records each
finished path in bl.h.
"""

import toyir

ENTRY = "bl.entry"
EXIT = "bl.exit"


def out_edges(nodes, edges):
    """Dict from node to the indices of its outgoing edges, in list order."""
    out = {v: [] for v in nodes}
    for i, (u, _) in enumerate(edges):
        out[u].append(i)
    return out


def topological_order(nodes, edges):
    """Kahn's algorithm. Raises ValueError if the graph has a cycle."""
    indeg = {v: 0 for v in nodes}
    for _, v in edges:
        indeg[v] += 1
    out = out_edges(nodes, edges)
    ready = [v for v in nodes if indeg[v] == 0]
    order = []
    while ready:
        u = ready.pop()
        order.append(u)
        for i in out[u]:
            v = edges[i][1]
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    if len(order) != len(nodes):
        raise ValueError("the graph has a cycle")
    return order


def number_paths(nodes, edges, entry, exit_):
    """The Ball-Larus numbering.

    Returns (num, val): num[v] is the number of paths from v to exit_, and
    val[i] is the value of edge i. The sum of val along a path from entry to
    exit_ is its path number, in 0 .. num[entry] - 1.
    """
    out = out_edges(nodes, edges)
    num = {}
    val = [0] * len(edges)
    for v in reversed(topological_order(nodes, edges)):  # @line L1
        if v == exit_:
            num[v] = 1  # @line L2
            continue
        num[v] = 0  # @line L3 L4
        for i in out[v]:  # @line L5
            val[i] = num[v]  # @line L6
            num[v] += num[edges[i][1]]  # @line L7
        if num[v] == 0:
            raise ValueError("node %r does not reach the exit" % (v,))
    return num, val


def regenerate(nodes, edges, num, val, entry, exit_, r):
    """The list of edge indices of the path with number r."""
    if not 0 <= r < num[entry]:
        raise ValueError("no path has number %r" % (r,))
    out = out_edges(nodes, edges)
    path, v = [], entry  # @line L16
    while v != exit_:  # @line L17
        for i in out[v]:
            w = edges[i][1]
            if val[i] <= r < val[i] + num[w]:  # @line L18
                path.append(i)  # @line L19
                r -= val[i]
                v = w
                break
    return path  # @line L20


def all_paths(nodes, edges, entry, exit_):
    """Every path from entry to exit_, as lists of edge indices (brute force)."""
    out = out_edges(nodes, edges)
    result, stack = [], [(entry, [])]
    while stack:
        v, path = stack.pop()
        if v == exit_:
            result.append(path)
            continue
        for i in out[v]:
            stack.append((edges[i][1], path + [i]))
    return result


class _Sets:
    """Disjoint sets with path halving and union by size."""

    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.size = {x: 1 for x in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True


def place_increments(nodes, edges, val, entry, exit_, weight=None):
    """Ball and Larus's placement on the chords of a maximum spanning tree.

    The tree is taken in the undirected graph of the DAG plus one edge
    exit_ -> entry, which is always in the tree. weight[i] is the expected
    frequency of edge i (1 for every edge if omitted). Returns (inc, tree):
    inc[i] is the increment of edge i, and tree is the set of the indices
    of the DAG edges in the tree, where inc is 0.
    """
    if weight is None:
        weight = [1] * len(edges)
    sets = _Sets(nodes)  # @line L8
    sets.union(exit_, entry)
    adj = {v: [] for v in nodes}
    adj[exit_].append((entry, 0))
    adj[entry].append((exit_, 0))
    tree = set()
    for i in sorted(range(len(edges)), key=lambda i: (-weight[i], i)):  # @line L9
        u, v = edges[i]
        if sets.union(u, v):
            tree.add(i)
            adj[u].append((v, val[i]))
            adj[v].append((u, -val[i]))
    # A potential phi with phi[v] = phi[u] + val[i] along every tree edge u -> v.
    phi = {entry: 0}  # @line L10
    stack = [entry]
    while stack:  # @line L11
        u = stack.pop()
        for v, d in adj[u]:
            if v not in phi:
                phi[v] = phi[u] + d  # @line L12
                stack.append(v)
    inc = [val[i] + phi[u] - phi[v] for i, (u, v) in enumerate(edges)]  # @line L13 L14
    return inc, tree  # @line L15


def cfg_to_dag(prog):
    """The DAG of a toy IR program, with back edges cut.

    Returns (nodes, edges, kind, back). kind[i] is "real" for an edge of
    the CFG or the edge ENTRY -> entry block, "ret" for b -> EXIT where b
    ends in ret, "start" for the dummy ENTRY -> h of a loop header h, and
    "stop" for the dummy b -> EXIT of the source b of a back edge. back maps
    each back edge (b, h) to the indices of its stop and start edges.
    """
    labels = list(prog.blocks)
    # Back edges: the edges to a block on the DFS stack.
    back_edges = []
    state = {lab: 0 for lab in labels}
    state[prog.entry] = 1
    stack = [(prog.entry, iter(toyir.succs(prog, prog.entry)))]
    while stack:
        v, it = stack[-1]
        w = next(it, None)
        if w is None:
            state[v] = 2
            stack.pop()
        elif state[w] == 1:
            back_edges.append((v, w))
        elif state[w] == 0:
            state[w] = 1
            stack.append((w, iter(toyir.succs(prog, w))))
    cut = set(back_edges)
    nodes = [ENTRY] + labels + [EXIT]
    edges, kind = [(ENTRY, prog.entry)], ["real"]
    for a in labels:
        for b in toyir.succs(prog, a):
            if (a, b) not in cut:
                edges.append((a, b))
                kind.append("real")
        if prog.blocks[a].term[0] == "ret":
            edges.append((a, EXIT))
            kind.append("ret")
    start, stop, back = {}, {}, {}
    for b, h in back_edges:
        if h not in start:
            start[h] = len(edges)
            edges.append((ENTRY, h))
            kind.append("start")
        if b not in stop:
            stop[b] = len(edges)
            edges.append((b, EXIT))
            kind.append("stop")
        back[(b, h)] = (stop[b], start[h])
    return nodes, edges, kind, back


def instrument(prog, nodes, edges, kind, back, inc, radix):
    """The profiling version of prog.

    bl.r is the path register. When a path ends (at a ret or a back edge),
    its number t is recorded as bl.h = bl.h * radix + t + 1, and every ret
    returns bl.h in place of the program's value. radix must exceed the
    number of paths. Code on an edge goes into a new block on that edge.
    """
    index = {e: i for i, e in enumerate(edges) if kind[i] == "real"}
    ret_edge = {edges[i][0]: i for i in range(len(edges)) if kind[i] == "ret"}

    def add(k):
        return [("op", "bl.r", "+", "bl.r", k)] if k else []

    def record(k):
        return [("op", "bl.t", "+", "bl.r", k + 1),
                ("op", "bl.h", "*", "bl.h", radix),
                ("op", "bl.h", "+", "bl.h", "bl.t")]

    blocks = {ENTRY: toyir.Block([("const", "bl.r", 0), ("const", "bl.h", 0)]
                                 + add(inc[index[(ENTRY, prog.entry)]]),
                                 ("jump", prog.entry))}
    extra = {}
    for a, blk in prog.blocks.items():
        instrs = list(blk.instrs)
        term = blk.term
        if term[0] == "ret":
            instrs += record(inc[ret_edge[a]])
            term = ("ret", "bl.h")
        else:
            targets = [term[1]] if term[0] == "jump" else [term[2], term[3]]
            new = []
            for b in targets:
                if (a, b) in back:
                    s_stop, s_start = back[(a, b)]
                    code = record(inc[s_stop]) + [("const", "bl.r", inc[s_start])]
                else:
                    code = add(inc[index[(a, b)]])
                if code:
                    lab = "bl.%s.%s" % (a, b)
                    extra[lab] = toyir.Block(code, ("jump", b))
                    b = lab
                new.append(b)
            term = ("jump", new[0]) if term[0] == "jump" else ("br", term[1], new[0], new[1])
        blocks[a] = toyir.Block(instrs, term)
    blocks.update(extra)
    return toyir.Program(list(prog.params), blocks)


def decode_history(h, radix):
    """The path numbers recorded in bl.h, in order."""
    out = []
    while h:
        h, t = divmod(h, radix)
        out.append(t - 1)
    return out[::-1]


def path_blocks(edges, kind, path):
    """The blocks of the program on a DAG path, without ENTRY and EXIT."""
    blocks = [edges[i][1] for i in path]
    return [b for b in blocks if b not in (ENTRY, EXIT)]
