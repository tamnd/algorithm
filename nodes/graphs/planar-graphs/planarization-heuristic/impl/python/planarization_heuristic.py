# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/planarization-heuristic/. The authors are listed in prov/8EHK3E.jsonl.

"""Planarization heuristic: a maximal planar subgraph, then edge insertion.

A graph is given by n (vertices 0..n-1) and a list of edges. The result is a
planar graph in which every crossing is a new dummy vertex of degree 4,
together with a rotation system: rot[v] lists the neighbours of v in
counterclockwise order. Faces are traced with the rule that the dart after
(a, b) is (b, c), where c is the neighbour just before a in rot[b].
"""

from collections import deque

Edge = tuple[int, int]


def _key(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def _blocks(n: int, adj: list[list[int]]) -> list[list[Edge]]:
    """Edges of each biconnected component, by iterative DFS."""
    disc = [-1] * n
    low = [0] * n
    blocks: list[list[Edge]] = []
    time = 0
    for s in range(n):
        if disc[s] != -1:
            continue
        disc[s] = low[s] = time
        time += 1
        stack = [(s, -1, iter(adj[s]))]
        edges: list[Edge] = []
        while stack:
            v, p, it = stack[-1]
            descended = False
            for w in it:
                if w == p:
                    continue
                if disc[w] == -1:
                    edges.append((v, w))
                    disc[w] = low[w] = time
                    time += 1
                    stack.append((w, v, iter(adj[w])))
                    descended = True
                    break
                if disc[w] < disc[v]:
                    edges.append((v, w))
                    low[v] = min(low[v], disc[w])
            if descended:
                continue
            stack.pop()
            if stack:
                u = stack[-1][0]
                low[u] = min(low[u], low[v])
                if low[v] >= disc[u]:
                    block: list[Edge] = []
                    while True:
                        e = edges.pop()
                        block.append(e)
                        if e == (u, v):
                            break
                    blocks.append(block)
    return blocks


def _embed_block(block: list[Edge]) -> dict[int, list[int]] | None:
    """Demoucron-Malgrange-Pertuiset path addition on one biconnected block.

    Returns the rotation at each vertex of the block, or None if the block is
    not planar.
    """
    adj: dict[int, set[int]] = {}
    for u, v in block:
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    if len(block) == 1:
        u, v = block[0]
        return {u: [v], v: [u]}
    # A first cycle: the edge (a, b) plus a shortest a-b path avoiding it.
    a, b = block[0]
    parent = {a: a}
    queue = deque([a])
    while queue:
        x = queue.popleft()
        for y in adj[x]:
            if y not in parent and not (x == a and y == b):
                parent[y] = x
                queue.append(y)
    cycle = [b]
    while cycle[-1] != a:
        cycle.append(parent[cycle[-1]])
    in_h = set(cycle)
    h_edges = {_key(cycle[i], cycle[i - 1]) for i in range(len(cycle))}
    faces = [cycle, cycle[::-1]]
    while len(h_edges) < len(block):
        # Fragments: chords, and components of the vertices not yet in H.
        fragments: list[tuple[set[int], list[int]]] = []  # (attachments, path)
        for u, v in block:
            if u in in_h and v in in_h and _key(u, v) not in h_edges:
                fragments.append(({u, v}, [u, v]))
        seen: set[int] = set()
        for s in adj:
            if s in in_h or s in seen:
                continue
            comp = [s]
            seen.add(s)
            att: set[int] = set()
            for x in comp:
                for y in adj[x]:
                    if y in in_h:
                        att.add(y)
                    elif y not in seen:
                        seen.add(y)
                        comp.append(y)
            seed = next(x for x in comp if any(y in in_h for y in adj[x]))
            fragments.append((att, [seed]))  # seed: a vertex next to H
        best = None
        for att, path in fragments:
            ok = [f for f in faces if att <= set(f)]
            if not ok:
                return None
            if best is None or len(ok) < len(best[2]):
                best = (att, path, ok)
            if len(ok) == 1:
                break
        att, path, ok = best
        face = ok[0]
        if len(path) == 1:  # a component: find a path between two attachments
            s = path[0]
            start = next(y for y in adj[s] if y in in_h)
            prev = {s: s}
            queue = deque([s])
            end = None
            while queue and end is None:
                x = queue.popleft()
                for y in adj[x]:
                    if y in in_h:
                        if y != start:
                            end = (x, y)
                            break
                    elif y not in prev:
                        prev[y] = x
                        queue.append(y)
            x, stop = end
            inner = [x]
            while inner[-1] != s:
                inner.append(prev[inner[-1]])
            path = [start] + inner[::-1] + [stop]
        u, v = path[0], path[-1]
        i, j = face.index(u), face.index(v)
        k = len(face)
        seg1 = [face[(i + t) % k] for t in range((j - i) % k + 1)]  # u .. v
        seg2 = [face[(j + t) % k] for t in range((i - j) % k + 1)]  # v .. u
        mid = path[1:-1]
        faces.remove(face)
        faces.append(seg1 + mid[::-1])
        faces.append(seg2 + mid)
        for t in range(len(path) - 1):
            h_edges.add(_key(path[t], path[t + 1]))
        in_h.update(mid)
    # Rotation from faces: for consecutive a, b, c on a face, a follows c at b.
    nxt: dict[int, dict[int, int]] = {v: {} for v in adj}
    for f in faces:
        k = len(f)
        for t in range(k):
            x, y, z = f[t - 1], f[t], f[(t + 1) % k]
            nxt[y][z] = x
    rot: dict[int, list[int]] = {}
    for v in adj:
        first = next(iter(adj[v]))
        order = [first]
        while nxt[v][order[-1]] != first:
            order.append(nxt[v][order[-1]])
        rot[v] = order
    return rot


def planar_embedding(n: int, edges: list[Edge]) -> list[list[int]] | None:
    """A planar rotation system of a simple graph, or None if it is not planar."""
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    rot: list[list[int]] = [[] for _ in range(n)]
    for block in _blocks(n, adj):
        brot = _embed_block(block)
        if brot is None:
            return None
        for v, around in brot.items():  # blocks at a cut vertex are concatenated
            rot[v].extend(around)
    return rot


def faces(rot: list[list[int]]) -> list[list[Edge]]:
    """All faces of a rotation system, each as its cycle of darts."""
    pos = [{w: i for i, w in enumerate(around)} for around in rot]
    seen: set[Edge] = set()
    result = []
    for u in range(len(rot)):
        for v in rot[u]:
            if (u, v) in seen:
                continue
            walk = []
            d = (u, v)
            while d not in seen:
                seen.add(d)
                walk.append(d)
                a, b = d
                d = (b, rot[b][pos[b][a] - 1])
            result.append(walk)
    return result


def planarize(n: int, edges: list[Edge]) -> dict:
    """Planarize a simple graph.

    Returns a dict with
      rot       rotation system of the planarized graph on n + crossings vertices
      chains    for each input edge, its path of vertices in the planarized graph
      kept      indices of the edges of the maximal planar subgraph
      crossings number of dummy vertices, n, n + 1, ...
    """
    seen: set[Edge] = set()
    for u, v in edges:
        if u == v or not (0 <= u < n and 0 <= v < n) or _key(u, v) in seen:
            raise ValueError("the graph must be simple, with vertices 0..n-1")
        seen.add(_key(u, v))
    kept: list[int] = []  # @line L1
    removed: list[int] = []
    sub: list[Edge] = []
    for idx, (u, v) in enumerate(edges):  # @line L2
        if planar_embedding(n, sub + [(u, v)]) is not None:  # @line L3
            sub.append((u, v))
            kept.append(idx)
        else:
            removed.append(idx)
    rot = planar_embedding(n, sub)  # @line L4
    # Every graph edge (x, y) of the planarized graph maps to its input edge.
    owner: dict[Edge, int] = {_key(*edges[i]): i for i in kept}
    chains: dict[int, list[int]] = {i: list(edges[i]) for i in kept}
    for idx in removed:  # @line L5
        u, v = edges[idx]
        fs = faces(rot)  # @line L6
        face_of: dict[Edge, int] = {}
        for f, walk in enumerate(fs):
            for d in walk:
                face_of[d] = f
        at_v = {f for f, walk in enumerate(fs) if any(d[0] == v for d in walk)}
        # Breadth-first search in the dual, from all faces at u.
        back: dict[int, tuple[int, Edge] | None] = {}
        queue: deque[int] = deque()  # @line L7
        for f, walk in enumerate(fs):
            if any(d[0] == u for d in walk):
                back[f] = None
                queue.append(f)
        goal = None
        while queue:
            f = queue.popleft()
            if f in at_v:
                goal = f
                break
            for d in fs[f]:
                g = face_of[(d[1], d[0])]
                if g not in back:
                    back[g] = (f, d)
                    queue.append(g)
        crossed: list[Edge] = []  # darts crossed, each seen from the earlier face
        path_faces = [goal]
        while back[path_faces[-1]] is not None:
            f, d = back[path_faces[-1]]
            crossed.append(d)
            path_faces.append(f)
        crossed.reverse()
        path_faces.reverse()
        # Subdivide each crossed edge by a dummy vertex.
        dummies = []
        for x, y in crossed:  # @line L8
            d = len(rot)
            rot.append([x, y])
            rot[x][rot[x].index(y)] = d
            rot[y][rot[y].index(x)] = d
            j = owner.pop(_key(x, y))
            chain = chains[j]
            for t in range(len(chain) - 1):
                if _key(chain[t], chain[t + 1]) == _key(x, y):
                    chain.insert(t + 1, d)
                    break
            owner[_key(x, d)] = j
            owner[_key(d, y)] = j
            dummies.append((d, x, y))
        # Connect u, d_1, ..., d_k, v through the faces of the path.
        seq = [u] + [d for d, _, _ in dummies] + [v]  # @line L9
        # A corner of z on a face is a pair of darts (a, z), (z, c) of its
        # walk; c is just before a in rot[z], and a new neighbour put between
        # them lies in that face. The search never crosses an edge at u or v
        # (both sides of such an edge are already start or goal faces), so the
        # vertices a found here are still neighbours of u and v.
        cu = _corner(fs[path_faces[0]], u)
        cv = _corner(fs[path_faces[-1]], v)
        _insert_after_pred(rot, u, cu, seq[1])
        _insert_after_pred(rot, v, cv, seq[-2])
        for t, (d, x, y) in enumerate(dummies):
            # rot[d] = [x, y]; the earlier face holds (x, d), (d, y), so its
            # corner at d is after y; the later face's corner is after x.
            rot[d] = [x, seq[t + 2], y, seq[t]]
        for t in range(len(seq) - 1):
            owner[_key(seq[t], seq[t + 1])] = idx
        chains[idx] = seq
    return {  # @line L10
        "rot": rot,
        "chains": [chains[i] for i in range(len(edges))],
        "kept": kept,
        "crossings": len(rot) - n,
    }


def _corner(walk: list[Edge], z: int) -> int:
    """The vertex a of some dart (a, z) on the walk, the start of a corner at z."""
    for t, d in enumerate(walk):
        if d[0] == z:
            return walk[t - 1][0]
    raise AssertionError("vertex not on face")


def _insert_after_pred(rot: list[list[int]], b: int, a: int, w: int) -> None:
    """Insert w into the corner at b entered from a: just before a in rot[b]."""
    around = rot[b]
    around.insert(around.index(a), w)
