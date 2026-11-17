# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gyo-reduction/. The authors are listed in prov/AMABKP.jsonl.
"""The GYO reduction (Graham 1979; Yu and Ozsoyoglu 1979).

A hypergraph is a list of edges. Each edge is an iterable of vertices; vertices must be
hashable and sortable (str or int). Edges are named by their index in the list, and two
edges may be equal. The reduction applies two rules while one applies:

  ear rule:         delete a vertex that occurs in exactly one remaining edge;
  containment rule: delete an edge that is a subset of another remaining edge.

The hypergraph is alpha-acyclic if and only if at most one edge remains. Each edge that the
containment rule deletes gets the edge that contains it as its parent, and these parent links
form a join tree of the original edges.
"""


def gyo_reduction(edges, rng=None):
    """Run the GYO reduction.

    Return (acyclic, parent, steps). parent maps the index of each deleted edge to the index
    of the edge that contained it. steps lists the rule applications in order, as
    ("vertex", v, i) for the ear rule on vertex v in edge i, and ("edge", i, j) for the
    containment rule that deletes edge i into edge j. If rng (a random.Random) is given, the
    next rule is chosen at random among all that apply; otherwise the first one in a fixed
    order is taken (vertex rules first, smallest vertex, then smallest pair of indices)."""
    cur = {i: set(e) for i, e in enumerate(edges)}                       # @line L1
    parent = {}                                                          # @line L1
    steps = []
    while True:                                                          # @line L2
        count = {}
        for i in cur:
            for v in cur[i]:
                count.setdefault(v, []).append(i)
        ears = sorted((v, occ[0]) for v, occ in count.items() if len(occ) == 1)  # @line L3
        pairs = []
        if rng is not None or not ears:
            keys = sorted(cur)
            for i in keys:                                               # @line L5
                for j in keys:
                    if i != j and cur[i] <= cur[j]:
                        pairs.append((i, j))
        moves = [("vertex", v, i) for v, i in ears] + [("edge", i, j) for i, j in pairs]
        if not moves:                                                    # @line L7
            break
        move = moves[0] if rng is None else moves[rng.randrange(len(moves))]
        if move[0] == "vertex":
            _, v, i = move
            cur[i].discard(v)                                            # @line L4
        else:
            _, i, j = move
            del cur[i]                                                   # @line L6
            parent[i] = j                                                # @line L6
        steps.append(move)
    return len(cur) <= 1, parent, steps                                  # @line L8


def is_alpha_acyclic(edges) -> bool:
    return gyo_reduction(edges)[0]


def is_join_tree(edges, tree_edges) -> bool:
    """Check that tree_edges (pairs of edge indices) form a tree on all the edges of the
    hypergraph and that, for each vertex, the edges that contain it induce a connected
    subtree (the running intersection property)."""
    m = len(edges)
    if m == 0:
        return not tree_edges
    if len(tree_edges) != m - 1:
        return False
    adj = {i: set() for i in range(m)}
    for a, b in tree_edges:
        if a == b or not (0 <= a < m and 0 <= b < m):
            return False
        adj[a].add(b)
        adj[b].add(a)
    if len(_component(adj, 0, set(range(m)))) != m:
        return False
    vertices = sorted(set().union(*[set(e) for e in edges]))
    for v in vertices:
        holders = {i for i in range(m) if v in set(edges[i])}
        start = min(holders)
        if _component(adj, start, holders) != holders:
            return False
    return True


def _component(adj, start, allowed) -> set:
    seen = {start}
    stack = [start]
    while stack:
        a = stack.pop()
        for b in adj[a]:
            if b in allowed and b not in seen:
                seen.add(b)
                stack.append(b)
    return seen


def join_tree(edges):
    """Return the tree edges of a join tree built from the GYO parent links, or None if the
    hypergraph is not alpha-acyclic."""
    acyclic, parent, _ = gyo_reduction(edges)
    if not acyclic:
        return None
    return sorted((i, j) for i, j in parent.items())
