# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-order-alignment/. The authors are listed in prov/K4CMRB.jsonl.

"""Partial order alignment (Lee, Grasso and Sharlow 2002), global version.

The alignment is kept as a directed acyclic graph with one letter per node.
Each new sequence is aligned to the graph by dynamic programming, where a node
looks back at all of its predecessors, and the alignment is then fused into the
graph: a matched letter reuses a node, a mismatch makes a new node in the same
column, and an inserted letter makes a new node in a new column.

Nodes that occupy the same alignment position form a column (the "aligned-to"
ring of the paper). The columns are kept in a list whose order every edge
follows, so flattening the list gives a topological order of the nodes.
"""

GAP = "-"
MATCH, MISMATCH, INDEL = 1, -1, -2
NEG = float("-inf")


def pair_score(x: str, y: str) -> int:
    """Linear scores: match +1, mismatch -1, letter against gap -2, gap against gap 0."""
    if x == GAP and y == GAP:
        return 0
    if x == GAP or y == GAP:
        return INDEL
    return MATCH if x == y else MISMATCH


def sp_score(rows: list[str]) -> int:
    return sum(pair_score(a, b) for i in range(len(rows)) for j in range(i + 1, len(rows))
               for a, b in zip(rows[i], rows[j]))


class POGraph:
    def __init__(self):
        self.base = []      # letter of each node
        self.preds = []     # set of predecessor nodes
        self.succs = []     # set of successor nodes
        self.labels = {}    # (u, v) -> set of sequence ids that use the edge
        self.col_of = []    # column id of each node
        self.columns = []   # list of column ids, in an order that every edge follows
        self.members = {}   # column id -> list of nodes
        self.paths = []     # for each sequence, its list of nodes

    def new_node(self, letter: str, column: int) -> int:
        v = len(self.base)
        self.base.append(letter)
        self.preds.append(set())
        self.succs.append(set())
        self.col_of.append(column)
        self.members.setdefault(column, []).append(v)
        return v

    def new_column(self, after) -> int:
        """A new column placed right after column `after` (or first if None)."""
        c = len(self.members)
        self.members[c] = []
        pos = 0 if after is None else self.columns.index(after) + 1
        self.columns.insert(pos, c)
        return c

    def order(self) -> list[int]:
        """A topological order of the nodes: the nodes column by column."""
        return [v for c in self.columns for v in self.members[c]]


def align_to_graph(g: POGraph, y: str):
    """Global alignment of y to the best path from a node without predecessors to a
    node without successors. Returns (score, pairs) where pairs is a list of
    (node or None, index in y or None) in path order."""
    n = len(y)
    order = g.order()
    if not order:
        return INDEL * n, [(None, j) for j in range(n)]
    start = [INDEL * j for j in range(n + 1)]   # the virtual start row
    h, back = {}, {}
    for v in order:  # @line L3
        row, ptr = [NEG] * (n + 1), [None] * (n + 1)
        for u in (sorted(g.preds[v]) or [None]):
            prev = start if u is None else h[u]
            for j in range(n + 1):
                if j and prev[j - 1] + pair_score(g.base[v], y[j - 1]) > row[j]:
                    row[j], ptr[j] = prev[j - 1] + pair_score(g.base[v], y[j - 1]), ("M", u)
                if prev[j] + INDEL > row[j]:
                    row[j], ptr[j] = prev[j] + INDEL, ("D", u)
        for j in range(1, n + 1):
            if row[j - 1] + INDEL > row[j]:
                row[j], ptr[j] = row[j - 1] + INDEL, ("I", v)
        h[v], back[v] = row, ptr
    best, end = max((h[v][n], -i) for i, v in enumerate(order) if not g.succs[v])
    v, j, pairs = order[-end], n, []
    while v is not None:  # @line L4
        move, u = back[v][j]
        if move == "M":
            pairs.append((v, j - 1)); j -= 1; v = u
        elif move == "D":
            pairs.append((v, None)); v = u
        else:
            pairs.append((None, j - 1)); j -= 1
    while j:
        pairs.append((None, j - 1)); j -= 1
    pairs.reverse()
    return best, pairs


def fuse(g: POGraph, y: str, pairs) -> None:
    """Add sequence y to the graph along its alignment."""
    sid = len(g.paths)
    path, last_col = [], None
    for v, j in pairs:
        if j is None:
            last_col = g.col_of[v]
            continue
        if v is not None:
            same = [w for w in g.members[g.col_of[v]] if g.base[w] == y[j]]
            w = same[0] if same else g.new_node(y[j], g.col_of[v])  # @line L5
            last_col = g.col_of[v]
        else:
            w = g.new_node(y[j], g.new_column(last_col))  # @line L6
            last_col = g.col_of[w]
        path.append(w)
    for a, b in zip(path, path[1:]):  # @line L7
        g.succs[a].add(b)
        g.preds[b].add(a)
        g.labels.setdefault((a, b), set()).add(sid)
    g.paths.append(path)


def rows_of(g: POGraph) -> list[str]:
    """One row per sequence; column c holds the letter of the sequence's node in c."""
    used = [c for c in g.columns if any(g.col_of[v] == c for p in g.paths for v in p)]
    rows = []
    for p in g.paths:
        at = {g.col_of[v]: g.base[v] for v in p}
        rows.append("".join(at.get(c, GAP) for c in used))
    return rows


def partial_order_alignment(seqs: list[str]) -> tuple[list[str], POGraph]:
    """Align the sequences in the given order. Returns the rows and the graph."""
    g = POGraph()
    for y in seqs:  # @line L1
        _, pairs = align_to_graph(g, y)  # @line L2
        fuse(g, y, pairs)
    return rows_of(g), g  # @line L8
