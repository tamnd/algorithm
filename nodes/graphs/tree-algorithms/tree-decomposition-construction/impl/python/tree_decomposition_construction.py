# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-decomposition-construction/. The authors are listed in prov/EC5HWV.jsonl.
"""Tree decomposition of width at most 4k+4, or a proof that treewidth > k.

The graph is simple and undirected, with the vertices 0..n-1, given as an
edge list. It is not weighted. The result is None when the treewidth is
larger than k, and otherwise a pair (bags, tree_edges): bags[i] is a sorted
list of vertices, and tree_edges lists pairs (parent, child) of bag indices.
The method is the separator recursion of Robertson and Seymour, done with
an explicit stack and a unit-capacity flow for the separators.
"""

from collections import deque
from itertools import combinations


def _components(adj, allowed):
    """Connected components of the subgraph induced by the set `allowed`."""
    seen = set()
    comps = []
    for s in sorted(allowed):
        if s in seen:
            continue
        seen.add(s)
        comp = [s]
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for w in adj[u]:
                if w in allowed and w not in seen:
                    seen.add(w)
                    comp.append(w)
                    queue.append(w)
        comps.append(comp)
    return comps


def _separator(adj, inner, side_a, side_b, limit):
    """A set Y of at most `limit` vertices of `inner` that meets every path
    from side_a to side_b inside inner + side_a + side_b, or None.

    Vertex capacities are 1 on `inner` and unbounded on the two sides; the
    flow is found by at most limit + 1 augmenting paths."""
    space = inner | side_a | side_b
    # node (v, 0) is the entry of v, (v, 1) its exit; cap holds residual capacities
    cap = {}
    graph = {}

    def arc(x, y, c):
        graph.setdefault(x, []).append(y)
        graph.setdefault(y, []).append(x)
        cap[(x, y)] = cap.get((x, y), 0) + c
        cap.setdefault((y, x), 0)

    big = len(space) + 1
    for v in space:
        arc((v, 0), (v, 1), 1 if v in inner else big)
        for w in adj[v]:
            if w in space:
                arc((v, 1), (w, 0), big)
    src, snk = ("s", 0), ("t", 0)
    for v in side_a:
        arc(src, (v, 0), big)
    for v in side_b:
        arc((v, 1), snk, big)
    flow = 0
    while True:
        prev = {src: None}
        queue = deque([src])
        while queue and snk not in prev:
            x = queue.popleft()
            for y in graph.get(x, ()):
                if y not in prev and cap[(x, y)] > 0:
                    prev[y] = x
                    queue.append(y)
        if snk not in prev:
            break
        flow += 1
        if flow > limit:
            return None
        y = snk
        while prev[y] is not None:
            x = prev[y]
            cap[(x, y)] -= 1
            cap[(y, x)] += 1
            y = x
    # the cut: inner vertices whose entry is reachable and exit is not
    return {v for v in inner if (v, 0) in prev and (v, 1) not in prev}


def _balanced_split(adj, comp, s, k):
    """Try every split of s into (A, X, B) with |X| <= k+1 and |A|, |B| <= 2k+2,
    and return X together with a separator inside comp, or None."""
    s = sorted(s)
    inner = set(comp)
    for size in range(k + 2):
        for sx in combinations(s, size):
            rest = [v for v in s if v not in sx]
            r = len(rest)
            for mask in range(1 << r):
                a = {rest[i] for i in range(r) if mask >> i & 1}
                if not a or len(a) > 2 * k + 2 or r - len(a) > 2 * k + 2:
                    continue
                if rest[0] not in a:  # (A, B) and (B, A) are the same split
                    continue
                b = set(rest) - a
                y = _separator(adj, inner, a, b, k + 1 - size)
                if y is not None:
                    return set(sx) | y
    return None


def tree_decomposition(n, edges, k):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    if len(edges) > k * n:  # @line L1
        return None
    bags = []
    tree_edges = []
    stack = [(comp, set(), -1) for comp in _components(adj, set(range(n)))]  # @line L2
    while stack:  # @line L3
        comp, s, parent = stack.pop()  # @line L4
        if len(s) < 3 * k + 4:  # @line L5
            bag = s | {comp[0]}
        else:
            x = _balanced_split(adj, comp, s, k)  # @line L6
            if x is None:  # @line L7
                return None
            bag = s | x  # @line L8
        node = len(bags)  # @line L9
        bags.append(sorted(bag))
        if parent >= 0:
            tree_edges.append((parent, node))
        rest = set(comp) - bag
        for d in _components(adj, rest):  # @line L10
            nd = {w for u in d for w in adj[u] if w not in rest}
            stack.append((d, nd, node))  # @line L11
    return bags, tree_edges  # @line L12


def is_tree_decomposition(n, edges, bags, tree_edges):
    """Check the three conditions and that the bags form a forest."""
    m = len(bags)
    if n > 0 and m == 0:
        return False
    tadj = [[] for _ in range(m)]
    for a, b in tree_edges:
        tadj[a].append(b)
        tadj[b].append(a)
    if len(tree_edges) != m - len(_components(tadj, set(range(m)))):
        return False  # a cycle among the bags
    where = [set() for _ in range(n)]
    for i, bag in enumerate(bags):
        for v in bag:
            where[v].add(i)
    if any(not w for w in where):
        return False
    for u, v in edges:
        if not (where[u] & where[v]):
            return False
    return all(len(_components(tadj, w)) == 1 for w in where)
