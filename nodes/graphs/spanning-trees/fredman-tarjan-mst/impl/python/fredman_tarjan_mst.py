# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fredman-tarjan-mst/. The authors are listed in prov/37AZFW.jsonl.


def fredman_tarjan_mst(
    n: int,
    edges: list[tuple[int, int, float]],
    heap_limit: int | None = None,
    log: list[tuple[int, int, float, int]] | None = None,
) -> list[int]:
    """Return the indices of a minimum spanning forest, by Fredman and Tarjan.

    The vertices are 0 .. n - 1 and edges[i] = (u, v, w) is an undirected
    edge. Weights may tie (ties are broken by the edge index); the graph may
    be disconnected, and parallel edges and self-loops are allowed.

    Each phase grows trees one after another, Prim style, with a Fibonacci
    heap of the vertices next to the tree. A tree adds at least one edge,
    and stops when its heap holds more than k vertices, when it reaches a
    tree of the same phase, or when its heap runs empty. Then every tree is
    contracted to one vertex. The limit is k = 2^(2m/t), where t is the number of vertices of the phase
    and m the number of edges of the input after loops and parallel edges
    are removed, unless heap_limit fixes it. If log is a list, each phase
    appends (t, edges of the phase, k, number of trees).

    Cost: O(m) per phase and at most beta(m, n) + 1 phases, so
    O(m beta(m, n)) time; O(n + m) space.
    """
    forest: list[int] = []
    cur, t = _clean(edges, list(range(n)))
    m0 = len(cur)
    while cur:  # @line L1
        m = len(cur)
        k = heap_limit if heap_limit is not None else 2.0 ** min(2.0 * m0 / t, 60.0)  # @line L2
        adj: list[list[tuple[int, tuple[float, int]]]] = [[] for _ in range(t)]
        for a, b, w, i in cur:
            adj[a].append((b, (w, i)))
            adj[b].append((a, (w, i)))
        tree_of = [-1] * t
        trees = 0
        for v0 in range(t):  # @line L3
            if tree_of[v0] >= 0 or not adj[v0]:
                continue
            in_tree = {v0}  # @line L4
            heap = _FibHeap()
            node: dict[int, _Node] = {}
            _scan(v0, adj, in_tree, heap, node)
            join = -1
            while heap.size > 0:  # @line L5
                (_, i), u = heap.extract_min()  # @line L6
                del node[u]
                forest.append(i)
                if tree_of[u] >= 0:  # @line L7
                    join = tree_of[u]
                    break
                in_tree.add(u)  # @line L8
                _scan(u, adj, in_tree, heap, node)
                if heap.size > k:
                    break
            if join < 0:  # @line L9
                join = trees
                trees += 1
            for v in in_tree:
                tree_of[v] = join
        if log is not None:
            log.append((t, m, k, trees))
        cur, t = _clean([(a, b, w) for a, b, w, _ in cur], tree_of, [i for *_, i in cur])  # @line L10
    return sorted(forest)  # @line L11


def _scan(u, adj, in_tree, heap, node):
    """Offer each edge at u to the heap of the vertices next to the tree."""
    for x, key in adj[u]:
        if x in in_tree:
            continue
        if x not in node:
            node[x] = heap.insert(key, x)
        elif key < node[x].key:
            heap.decrease_key(node[x], key)


def _clean(edges, label, index=None):
    """Relabel the ends, drop loops, keep the lightest of parallel edges.

    The vertices that keep an edge are numbered 0 .. t - 1; return (edges, t).
    """
    best: dict[tuple[int, int], tuple[float, int]] = {}
    for j, (u, v, w) in enumerate(edges):
        i = j if index is None else index[j]
        a, b = label[u], label[v]
        if a == b:
            continue
        pair = (a, b) if a < b else (b, a)
        if pair not in best or (w, i) < best[pair]:
            best[pair] = (w, i)
    new: dict[int, int] = {}
    for a, b in best:
        new.setdefault(a, len(new))
        new.setdefault(b, len(new))
    return [(new[a], new[b], w, i) for (a, b), (w, i) in best.items()], len(new)


class _Node:
    __slots__ = ("key", "item", "parent", "child", "left", "right", "degree", "mark")

    def __init__(self, key, item):
        self.key = key
        self.item = item
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.degree = 0
        self.mark = False


class _FibHeap:
    """A Fibonacci heap with insert, decrease-key and extract-min."""

    def __init__(self):
        self.min = None
        self.size = 0

    def insert(self, key, item):
        x = _Node(key, item)
        self._add_root(x)
        self.size += 1
        return x

    def _add_root(self, x):
        x.parent = None
        x.mark = False
        if self.min is None:
            x.left = x.right = x
            self.min = x
        else:
            x.left = self.min
            x.right = self.min.right
            self.min.right.left = x
            self.min.right = x
            if x.key < self.min.key:
                self.min = x

    def extract_min(self):
        z = self.min
        children = []
        c = z.child
        if c is not None:
            children.append(c)
            c = c.right
            while c is not z.child:
                children.append(c)
                c = c.right
        roots = [z.right]
        r = z.right.right
        while r is not z:
            roots.append(r)
            r = r.right
        if z.right is z:
            roots = []
        self.size -= 1
        table: dict[int, _Node] = {}
        for x in roots + children:
            x.parent = None
            while x.degree in table:
                y = table.pop(x.degree)
                if y.key < x.key:
                    x, y = y, x
                self._link(y, x)
            table[x.degree] = x
        self.min = None
        for x in table.values():
            self._add_root(x)
        return z.key, z.item

    def _link(self, y, x):
        """Make the root y a child of the root x."""
        y.parent = x
        y.mark = False
        if x.child is None:
            x.child = y
            y.left = y.right = y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right.left = y
            x.child.right = y
        x.degree += 1

    def decrease_key(self, x, key):
        x.key = key
        p = x.parent
        if p is not None and key < p.key:
            self._cut(x, p)
            while p.parent is not None and p.mark:
                q = p.parent
                self._cut(p, q)
                p = q
            if p.parent is not None:
                p.mark = True
        if key < self.min.key:
            self.min = x

    def _cut(self, x, p):
        if x.right is x:
            p.child = None
        else:
            x.left.right = x.right
            x.right.left = x.left
            if p.child is x:
                p.child = x.right
        p.degree -= 1
        self._add_root(x)
