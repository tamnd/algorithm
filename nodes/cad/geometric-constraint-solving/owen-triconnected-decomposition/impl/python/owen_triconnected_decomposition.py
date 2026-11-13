# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/owen-triconnected-decomposition/. The authors are listed in prov/AM42WY.jsonl.

"""Owen's top-down decomposition, for points and distances in the plane.

The constraint graph is split at a separation pair {a, b}. One side is rigid; the other
side gets a virtual edge ab and is rigid with it. Both sides are split again, until
every part is a triangle. The solver places the rigid side first, measures |ab| there,
places the other side with that length, and glues the two by a proper rigid motion.
"""

from math import sqrt

Edge = tuple[int, int]
# A node is ("tri", u, v, w) or ("split", a, b, rigid child, flexible child).
Node = tuple


def _key(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def _articulation_points(verts: list[int], adj: dict[int, list[int]], skip: int) -> list[int]:
    """Articulation points of the graph on verts minus skip, by an iterative low-point DFS.
    Raises ValueError if that graph is not connected. Cost O(n + m)."""
    rest = [v for v in verts if v != skip]
    root = rest[0]
    disc = {root: 0}
    low = {root: 0}
    parent = {root: -1}
    cut: set[int] = set()
    root_children = 0
    stack = [(root, iter(adj[root]))]
    t = 1
    while stack:
        v, it = stack[-1]
        advanced = False
        for w in it:
            if w == skip:
                continue
            if w not in disc:
                disc[w] = low[w] = t
                t += 1
                parent[w] = v
                if v == root:
                    root_children += 1
                stack.append((w, iter(adj[w])))
                advanced = True
                break
            if w != parent[v]:
                low[v] = min(low[v], disc[w])
        if advanced:
            continue
        stack.pop()
        if stack:
            u = stack[-1][0]
            low[u] = min(low[u], low[v])
            if u != root and low[v] >= disc[u]:
                cut.add(u)
    if len(disc) != len(rest):
        raise ValueError("the constraint graph is not 2-connected, so it is not rigid")
    if root_children >= 2:
        cut.add(root)
    return sorted(cut)


def separation_pair(verts: list[int], edges: set[Edge]) -> tuple[int, int] | None:
    """A pair {a, b} whose removal disconnects the graph, or None if there is none.
    Precondition: the graph is 2-connected with at least 4 vertices. Cost O(n (n + m))."""
    adj: dict[int, list[int]] = {v: [] for v in verts}
    for u, v in sorted(edges):
        adj[u].append(v)
        adj[v].append(u)
    for a in verts:
        cut = _articulation_points(verts, adj, a)
        if cut:
            return (a, cut[0])
    return None


def decompose(n: int, edges: list[Edge]) -> list[Node] | None:
    """Split the constraint graph (range(n), edges) at separation pairs, down to triangles.

    Precondition: the graph is a Laman graph (2n - 3 edges, and every k >= 2 vertices
    span at most 2k - 3 edges), n >= 3. Returns the list of nodes, root first, or None
    if a part with four or more vertices has no separation pair (the method fails).
    Raises ValueError if a count shows that the graph is not Laman.
    Cost: O(n^3) here; O(n^2) with a linear-time triconnectivity algorithm.
    """
    es = {_key(u, v) for u, v in edges}
    if len(es) != len(edges) or any(u == v for u, v in edges):
        raise ValueError("bad edges")
    nodes: list[Node] = [()]
    stack: list[tuple[int, list[int], set[Edge]]] = [(0, list(range(n)), es)]
    while stack:
        nid, verts, part = stack.pop()
        k = len(verts)
        if len(part) != 2 * k - 3:  # @line L1
            raise ValueError("a part has the wrong number of edges, so the graph is not Laman")
        if k == 3:  # @line L2
            nodes[nid] = ("tri", *verts)
            continue
        pair = separation_pair(verts, part)  # @line L3
        if pair is None:  # @line L4
            return None
        a, b = pair
        inside = set(verts) - {a, b}
        first = min(inside)
        comp = {first}
        todo = [first]
        nbr: dict[int, list[int]] = {v: [] for v in verts}
        for u, v in part:
            nbr[u].append(v)
            nbr[v].append(u)
        while todo:  # @line L5
            v = todo.pop()
            for w in nbr[v]:
                if w in inside and w not in comp:
                    comp.add(w)
                    todo.append(w)
        side1 = sorted(comp | {a, b})
        side2 = sorted((inside - comp) | {a, b})
        s1 = set(side1)
        ab = _key(a, b)
        e1 = {e for e in part if e[0] in s1 and e[1] in s1 and e != ab}
        e2 = {e for e in part if e not in e1 and e != ab}
        if ab in part:  # @line L6
            e1.add(ab)
        elif len(e2) == 2 * len(side2) - 3:
            side1, side2, e1, e2 = side2, side1, e2, e1
        e2.add(ab)  # @line L7
        i1, i2 = len(nodes), len(nodes) + 1
        nodes.extend(((), ()))
        nodes[nid] = ("split", a, b, i1, i2)
        stack.append((i2, side2, e2))
        stack.append((i1, side1, e1))
    return nodes


def is_decomposable(n: int, edges: list[Edge]) -> bool:
    """True if Owen's method splits the Laman graph down to triangles."""
    if n == 2 and len(edges) == 1:
        return True
    return decompose(n, edges) is not None


def orient(p: tuple[int, int], q: tuple[int, int], r: tuple[int, int]) -> int:
    """Sign of the orientation determinant of three integer points, computed exactly."""
    d = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (d > 0) - (d < 0)


def _triangle(l_uv: float, l_uw: float, l_vw: float, side: int) -> tuple[complex, complex, complex]:
    """Place u at 0, v on the positive x axis, and w on the side given by the sign."""
    if not (l_uv > 0.0 and l_uw > 0.0 and l_vw > 0.0):
        raise ValueError("lengths must be positive")
    x = (l_uv * l_uv + l_uw * l_uw - l_vw * l_vw) / (2.0 * l_uv)
    h2 = l_uw * l_uw - x * x
    if h2 < -1e-9 * max(l_uv, l_uw, l_vw) ** 2:
        raise ValueError("no real solution: the triangle inequality fails")
    h = sqrt(h2) if h2 > 0.0 else 0.0
    return 0j, complex(l_uv, 0.0), complex(x, h if side > 0 else -h)


def solve(
    n: int,
    lengths: dict[Edge, float],
    draft: list[tuple[int, int]] | None = None,
    signs: list[int] | None = None,
) -> list[tuple[float, float]]:
    """Place n points so that |p_u - p_v| = lengths[(u, v)] for every constraint.

    Precondition: the graph is a Laman graph that Owen's method splits into triangles,
    and the lengths are positive. Triangle i, in the order the solver meets them, takes
    signs[i] if given, else the exact orientation sign of its points in the integer
    draft (0 counts as +1). Raises ValueError if the method fails or a triangle has no
    real solution. Cost: the decomposition plus O(n^2) for the moves.
    """
    if n == 2 and len(lengths) == 1:
        ((u, v), d), = lengths.items()
        return [(0.0, 0.0), (d, 0.0)] if u == 0 else [(d, 0.0), (0.0, 0.0)]
    length = {_key(u, v): d for (u, v), d in lengths.items()}
    nodes = decompose(n, list(lengths))
    if nodes is None:
        raise ValueError("Owen's method fails: a part is 3-connected")
    leaves = sum(1 for nd in nodes if nd[0] == "tri")
    if signs is not None and len(signs) != leaves:
        raise ValueError("one sign per triangle is needed")
    placed: dict[int, dict[int, complex]] = {}
    leaf = 0
    stack: list[tuple[str, int]] = [("go", 0)]
    while stack:
        step, nid = stack.pop()
        nd = nodes[nid]
        if nd[0] == "tri":  # @line L8
            _, u, v, w = nd
            if signs is not None:
                side = signs[leaf]
            elif draft is not None:
                side = orient(draft[u], draft[v], draft[w]) or 1
            else:
                side = 1
            leaf += 1
            pu, pv, pw = _triangle(length[_key(u, v)], length[_key(u, w)], length[_key(v, w)], side)
            placed[nid] = {u: pu, v: pv, w: pw}
            continue
        _, a, b, i1, i2 = nd
        if step == "go":  # @line L9
            stack.append(("mid", nid))
            stack.append(("go", i1))
        elif step == "mid":  # @line L10
            r = placed[i1]
            length.setdefault(_key(a, b), abs(r[a] - r[b]))
            stack.append(("end", nid))
            stack.append(("go", i2))
        else:  # @line L11
            r, f = placed.pop(i1), placed.pop(i2)
            z = (r[b] - r[a]) / (f[b] - f[a])
            z /= abs(z)
            glued = dict(r)
            for v, x in f.items():
                glued.setdefault(v, r[a] + z * (x - f[a]))
            placed[nid] = glued
    final = placed[0]
    return [(final[v].real, final[v].imag) for v in range(n)]
