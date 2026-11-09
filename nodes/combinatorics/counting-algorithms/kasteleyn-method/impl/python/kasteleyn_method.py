# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kasteleyn-method/. The authors are listed in prov/GT7NZ8.jsonl.

from functools import cmp_to_key
from math import isqrt


def _half(dx, dy):
    """0 for directions in the upper half plane (with the positive x axis), else 1."""
    return 0 if dy > 0 or (dy == 0 and dx > 0) else 1


def _rotation(pos, adj, v):
    """The neighbours of v, sorted counterclockwise by direction, with exact integer tests."""
    x0, y0 = pos[v]

    def cmp(a, b):
        ax, ay = pos[a][0] - x0, pos[a][1] - y0
        bx, by = pos[b][0] - x0, pos[b][1] - y0
        ha, hb = _half(ax, ay), _half(bx, by)
        if ha != hb:
            return ha - hb
        cross = ax * by - ay * bx
        return -1 if cross > 0 else (1 if cross < 0 else 0)

    return sorted(adj[v], key=cmp_to_key(cmp))


def faces_of(pos, adj):
    """The faces of a plane straight-line graph, each as a list of darts (a, b).

    Each face is traced with the face on the left of every dart, so bounded
    faces are traced counterclockwise and the outer face clockwise.
    """
    rot = {v: _rotation(pos, adj, v) for v in adj}
    where = {v: {w: k for k, w in enumerate(r)} for v, r in rot.items()}
    seen = set()
    faces = []
    for u in adj:
        for v in rot[u]:
            if (u, v) in seen:
                continue
            face = []
            a, b = u, v
            while (a, b) not in seen:
                seen.add((a, b))
                face.append((a, b))
                r = rot[b]
                a, b = b, r[(where[b][a] - 1) % len(r)]  # clockwise successor of a around b
            faces.append(face)
    return faces


def twice_area(pos, face):
    """Twice the signed area enclosed by the boundary walk of a face."""
    return sum(pos[a][0] * pos[b][1] - pos[b][0] * pos[a][1] for a, b in face)


def pfaffian_orientation(pos, adj, root):
    """Orient the edges of the connected component of root (a dict edge -> (tail, head))."""
    # @line L2: a depth-first spanning tree T; tree edges point from the smaller to the larger label
    parent = {root: None}
    stack = [(root, iter(adj[root]))]
    orient = {}
    while stack:
        v, it = stack[-1]
        for w in it:
            if w not in parent:
                parent[w] = v
                orient[frozenset((v, w))] = (min(v, w), max(v, w))
                stack.append((w, iter(adj[w])))
                break
        else:
            stack.pop()
    comp = {v: adj[v] for v in parent}
    faces = faces_of(pos, comp)  # @line L3
    if not faces:  # a single vertex: no edges to orient
        return orient
    outer = min(range(len(faces)), key=lambda i: twice_area(pos, faces[i]))
    side = {d: i for i, face in enumerate(faces) for d in face}
    dual = {i: [] for i in range(len(faces))}  # @line L4
    for u in comp:
        for v in comp[u]:
            e = frozenset((u, v))
            if u < v and e not in orient:
                f, g = side[(u, v)], side[(v, u)]
                dual[f].append((g, e))
                dual[g].append((f, e))
    up = {outer: None}
    order = [outer]
    for f in order:
        for g, e in dual[f]:
            if g not in up:
                up[g] = e
                order.append(g)
    for f in reversed(order[1:]):  # @line L5: children before parents
        e = up[f]  # @line L6
        clockwise = 0
        for a, b in faces[f]:
            k = frozenset((a, b))
            if k != e and orient[k] == (b, a):
                clockwise += 1
        a, b = next(d for d in faces[f] if frozenset(d) == e)
        orient[e] = (b, a) if clockwise % 2 == 0 else (a, b)  # @line L7
    return orient


def _det(m):
    """Exact determinant of an integer matrix by fraction-free (Bareiss) elimination."""
    a = [row[:] for row in m]
    n = len(a)
    if n == 0:
        return 1
    sign = 1
    prev = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            for i in range(k + 1, n):
                if a[i][k] != 0:
                    a[k], a[i] = a[i], a[k]
                    sign = -sign
                    break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // prev
        prev = a[k][k]
    return sign * a[n - 1][n - 1]


def kasteleyn_count(pos, edges):
    """Count the perfect matchings of a plane graph.

    pos[v] is the integer point of vertex v, for v = 0, ..., n - 1, and edges is
    a list of pairs. The straight segments of the edges must form a plane
    drawing: no two segments cross, and no segment passes through a vertex.
    Each connected component is handled on its own and the counts multiply.
    """
    n = len(pos)
    adj = {v: [] for v in range(n)}
    seen = set()
    for u, v in edges:
        e = frozenset((u, v))
        if u == v or e in seen or not (0 <= u < n and 0 <= v < n):
            raise ValueError("edges must join two distinct vertices, once")
        seen.add(e)
        adj[u].append(v)
        adj[v].append(u)
    if len(set(map(tuple, pos))) != n:
        raise ValueError("vertices must have distinct positions")
    total = 1
    done = set()
    for root in range(n):
        if root in done:
            continue
        comp = [root]
        done.add(root)
        for v in comp:
            for w in adj[v]:
                if w not in done:
                    done.add(w)
                    comp.append(w)
        if len(comp) % 2 == 1:  # @line L1
            return 0
        orient = pfaffian_orientation(pos, adj, root)
        index = {v: i for i, v in enumerate(comp)}
        k = [[0] * len(comp) for _ in comp]  # @line L8
        for u, v in orient.values():
            k[index[u]][index[v]] = 1
            k[index[v]][index[u]] = -1
        d = _det(k)  # @line L9
        r = isqrt(d)
        if r * r != d:
            raise ArithmeticError("det(K) is not a square; the drawing is not plane")
        total *= r
    return total
