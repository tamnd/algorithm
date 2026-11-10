# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/planar-steiner-tree-ptas/. The authors are listed in prov/H3DF34.jsonl.

"""The parts of the Borradaile-Klein-Mathieu scheme that can be checked on small weighted grid graphs.

A graph is a dict {vertex: {neighbour: weight}}. The code finds a 2-approximate Steiner tree, uses the lines of a
coarse grid as the mortar graph (the scheme builds it from the approximate tree and short paths), puts portals on the
brick boundaries, builds the portal-connected graph B+, solves Steiner tree on B+ exactly in place of the dynamic
program, and maps the solution back to the input graph."""

import heapq
from typing import Optional, Sequence

Graph = dict


def grid_graph(rows: int, cols: int, weight) -> Graph:
    """The rows x cols grid; weight(u, v) gives the weight of each edge."""
    g: Graph = {(r, c): {} for r in range(rows) for c in range(cols)}
    for r in range(rows):
        for c in range(cols):
            for v in ((r + 1, c), (r, c + 1)):
                if v in g:
                    g[(r, c)][v] = g[v][(r, c)] = weight((r, c), v)
    return g


def dijkstra(g: Graph, source) -> tuple[dict, dict]:
    d, parent = {source: 0}, {source: None}
    heap = [(0, 0, source)]
    count = 1
    while heap:
        du, _, u = heapq.heappop(heap)
        if du > d[u]:
            continue
        for v, w in g[u].items():
            if v not in d or du + w < d[v]:
                d[v], parent[v] = du + w, u
                heapq.heappush(heap, (du + w, count, v))
                count += 1
    return d, parent


def tree_weight(g: Graph, edges) -> int:
    return sum(g[u][v] for u, v in edges)


def edge(u, v) -> tuple:
    return (u, v) if u <= v else (v, u)


def two_approx(g: Graph, terminals: Sequence) -> set:
    """Prim on the shortest-path distances between terminals, each tree edge replaced by its path, then a
    minimum spanning tree of the union. Its weight is at most 2(1 - 1/k) OPT."""
    paths = {t: dijkstra(g, t) for t in terminals}
    inside, rest, used = [terminals[0]], list(terminals[1:]), set()
    while rest:
        _, s, t = min((paths[s][0][t], s, t) for s in inside for t in rest)
        parent = paths[s][1]
        v = t
        while parent[v] is not None:
            used.add(edge(v, parent[v]))
            v = parent[v]
        inside.append(t)
        rest.remove(t)
    return spanning_tree(g, used)


def spanning_tree(g: Graph, edges: set) -> set:
    """A minimum spanning forest of the subgraph with these edges (Kruskal)."""
    root: dict = {}

    def find(x):
        root.setdefault(x, x)
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x

    out = set()
    for u, v in sorted(edges, key=lambda e: (g[e[0]][e[1]], e)):
        a, b = find(u), find(v)
        if a != b:
            root[a] = b
            out.add((u, v))
    return out


def steiner_exact(g: Graph, terminals: Sequence) -> tuple[int, set]:
    """Dreyfus-Wagner over subsets of terminals, with a Dijkstra pass per subset; returns (weight, edges)."""
    k = len(terminals)
    if k == 1:
        return 0, set()
    verts = list(g)
    full = (1 << k) - 1
    cost: dict = {}
    how: dict = {}
    for i, t in enumerate(terminals):
        d, parent = dijkstra(g, t)
        for v in verts:
            cost[(1 << i, v)] = d[v]
            how[(1 << i, v)] = ("path", t, parent)
    for mask in range(1, full + 1):
        if mask & (mask - 1) == 0:
            continue
        for v in verts:  # join two parts at v
            best, arg = None, None
            sub = (mask - 1) & mask
            while sub:
                if sub < mask ^ sub:
                    val = cost[(sub, v)] + cost[(mask ^ sub, v)]
                    if best is None or val < best:
                        best, arg = val, sub
                sub = (sub - 1) & mask
            cost[(mask, v)], how[(mask, v)] = best, ("join", arg)
        heap = [(cost[(mask, v)], n, v) for n, v in enumerate(verts)]
        heapq.heapify(heap)
        done = set()
        count = len(verts)
        while heap:  # then move the joining point along shortest paths
            du, _, u = heapq.heappop(heap)
            if u in done:
                continue
            done.add(u)
            for v, w in g[u].items():
                if du + w < cost[(mask, v)]:
                    cost[(mask, v)], how[(mask, v)] = du + w, ("step", u)
                    heapq.heappush(heap, (du + w, count, v))
                    count += 1
    root = terminals[0]
    rest_mask = full ^ 1
    edges: set = set()
    todo = [(rest_mask, root)]
    while todo:
        mask, v = todo.pop()
        kind = how[(mask, v)]
        if kind[0] == "path":
            parent = kind[2]
            while parent[v] is not None:
                edges.add(edge(v, parent[v]))
                v = parent[v]
        elif kind[0] == "join":
            todo += [(kind[1], v), (mask ^ kind[1], v)]
        else:
            edges.add(edge(v, kind[1]))
            todo.append((mask, kind[1]))
    return cost[(rest_mask, root)], edges


def mortar_grid(rows: int, cols: int, kappa: int) -> tuple[set, list[tuple]]:
    """The vertices on every kappa-th row and column, and the bricks (r0, c0, r1, c1) between them."""
    on = {(r, c) for r in range(rows) for c in range(cols) if r % kappa == 0 or c % kappa == 0}
    bricks = [(r, c, r + kappa, c + kappa) for r in range(0, rows - 1, kappa) for c in range(0, cols - 1, kappa)]
    return on, bricks


def in_brick(v, b) -> bool:
    return b[0] <= v[0] <= b[2] and b[1] <= v[1] <= b[3]


def boundary_cycle(b) -> list[tuple]:
    """The boundary of a brick in cyclic order, starting at its top left corner."""
    r0, c0, r1, c1 = b
    return ([(r0, c) for c in range(c0, c1)] + [(r, c1) for r in range(r0, r1)]
            + [(r1, c) for c in range(c1, c0, -1)] + [(r, c0) for r in range(r1, r0, -1)])


def portals(b, spacing: int) -> list[tuple]:
    """Boundary vertices whose position along their side is a multiple of the spacing; nested as spacing halves."""
    return [v for v in boundary_cycle(b) if (v[0] % spacing == 0 if v[1] in (b[1], b[3]) else v[1] % spacing == 0)]


def portal_graph(g: Graph, mortar: set, bricks: Sequence[tuple], spacing: int) -> Graph:
    """B+: the mortar graph, a copy of each brick, and edges of weight 0 from each portal of a copy to the mortar."""
    plus: Graph = {}

    def add(u, v, w):
        plus.setdefault(u, {})[v] = w
        plus.setdefault(v, {})[u] = w

    for u in g:
        for v, w in g[u].items():
            if u < v and u in mortar and v in mortar:  # with kappa >= 2 such an edge lies on a mortar line
                add(("m", u), ("m", v), w)
    for i, b in enumerate(bricks):
        for u in g:
            for v, w in g[u].items():
                if u < v and in_brick(u, b) and in_brick(v, b):
                    add(("b", i, u), ("b", i, v), w)
        for p in portals(b, spacing):  # @line L3
            add(("b", i, p), ("m", p), 0)
    return plus


def lift(terminal, mortar: set, bricks: Sequence[tuple]):
    if terminal in mortar:
        return ("m", terminal)
    return ("b", next(i for i, b in enumerate(bricks) if in_brick(terminal, b)), terminal)


def project(plus_edges) -> set:
    """Map edges of B+ back to the input graph; the edges of weight 0 to the mortar disappear."""
    out = set()
    for a, b in plus_edges:
        u, v = a[-1], b[-1]
        if u != v:
            out.add(edge(u, v))
    return out


def connects(edges: set, terminals: Sequence) -> bool:
    adj: dict = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    seen, stack = {terminals[0]}, [terminals[0]]
    while stack:
        for v in adj.get(stack.pop(), []):
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return all(t in seen for t in terminals)


def portal_partitions(g: Graph, b, ports: Sequence[tuple]) -> set:
    """The partitions of the portals of one brick into groups joined by a subgraph of the brick, over all edge
    subsets of the brick. These are the connection states of the brick in the dynamic program."""
    inner = sorted({edge(u, v) for u in g for v in g[u] if in_brick(u, b) and in_brick(v, b)})
    out = set()
    for mask in range(1 << len(inner)):
        root = {p: p for p in g if in_brick(p, b)}

        def find(x):
            while root[x] != x:
                root[x] = root[root[x]]
                x = root[x]
            return x

        for j, (u, v) in enumerate(inner):
            if mask >> j & 1:
                root[find(u)] = find(v)
        groups: dict = {}
        for p in ports:
            groups.setdefault(find(p), []).append(ports.index(p))
        out.add(tuple(sorted(tuple(x) for x in groups.values())))
    return out


def non_crossing(partition: Sequence[tuple]) -> bool:
    """No a < b < c < d with a, c in one group and b, d in another (positions along the boundary cycle)."""
    where = {p: i for i, grp in enumerate(partition) for p in grp}
    pts = sorted(where)
    for a in pts:
        for b in pts:
            for c in pts:
                for d in pts:
                    if a < b < c < d and where[a] == where[c] != where[b] == where[d]:
                        return False
    return True


def scheme(g: Graph, rows: int, cols: int, terminals: Sequence, kappa: int, spacing: int,
           stats: Optional[dict] = None) -> tuple[int, set]:
    """One run of the outline: returns the weight and the edges of a Steiner tree of g."""
    approx = two_approx(g, terminals)  # @line L1
    mortar, bricks = mortar_grid(rows, cols, kappa)  # @line L2
    plus = portal_graph(g, mortar, bricks, spacing)  # @line L4
    lifted = [lift(t, mortar, bricks) for t in terminals]
    value, plus_edges = steiner_exact(plus, lifted)  # @line L5
    edges = spanning_tree(g, project(plus_edges))  # @line L6
    if stats is not None:
        stats.update(approx=tree_weight(g, approx), plus=value, mortar=len(mortar), bricks=len(bricks),
                     portals=len(portals(bricks[0], spacing)), plus_vertices=len(plus))
    return tree_weight(g, edges), edges
