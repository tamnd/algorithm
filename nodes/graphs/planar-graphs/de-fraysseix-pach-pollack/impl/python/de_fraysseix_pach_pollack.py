# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-fraysseix-pach-pollack/. The authors are listed in prov/FQHSKN.jsonl.
"""Straight-line grid drawing of a maximal planar graph by the shift method.

The embedding is given as a rotation system: rot[v] lists the neighbours of v
in counterclockwise order. The outer face is the triangle (v1, v2, vn), listed
counterclockwise. The result puts v1 at (0, 0), v2 at (2n - 4, 0) and vn at
(n - 2, n - 2), with integer coordinates and no crossings.
"""


def canonical_ordering(rot, v1, v2, vn):
    """Return (order, left, right) for a maximal planar graph.

    order is a canonical ordering v1, v2, ..., vn. For k >= 4, left[v] and
    right[v] are the first and last neighbours of v on the contour of the
    graph induced by the vertices before v.
    """
    n = len(rot)
    prev = [-1] * n
    nxt = [-1] * n
    on = [False] * n
    chords = [0] * n
    left = [-1] * n
    right = [-1] * n
    nxt[v1], prev[vn], nxt[vn], prev[v2] = vn, v1, v2, vn
    on[v1] = on[v2] = on[vn] = True
    removed_order = []
    stack = []
    v = vn
    for k in range(n, 3, -1):
        if k < n:
            while True:
                v = stack.pop()
                if on[v] and chords[v] == 0 and v != v1 and v != v2:
                    break
        a, b = prev[v], nxt[v]
        left[v], right[v] = a, b
        removed_order.append(v)
        on[v] = False
        r = rot[v]
        d = len(r)
        i = r.index(a)
        new = []
        while True:
            i = (i + 1) % d
            w = r[i]
            if w == b:
                break
            new.append(w)
        if not new:
            # the edge ab was a chord and is now a contour edge
            chords[a] -= 1
            chords[b] -= 1
            nxt[a], prev[b] = b, a
            for x in (a, b):
                if chords[x] == 0:
                    stack.append(x)
            continue
        chain = [a] + new + [b]
        for j in range(1, len(chain)):
            nxt[chain[j - 1]] = chain[j]
            prev[chain[j]] = chain[j - 1]
        for w in new:
            # mark the new vertices one at a time, so that a chord
            # between two new vertices is counted once
            on[w] = True
            for y in rot[w]:
                if on[y] and y != w and y != prev[w] and y != nxt[w]:
                    chords[w] += 1
                    chords[y] += 1
        for x in [a] + new + [b]:
            if chords[x] == 0:
                stack.append(x)
    third = nxt[v1]
    order = [v1, v2, third] + removed_order[::-1]
    return order, left, right


def check_triangulation(rot, v1, v2, vn):
    """Raise ValueError unless rot is a plane triangulation with outer face
    v1, v2, vn in counterclockwise order."""
    n = len(rot)
    if n < 3:
        raise ValueError("need at least 3 vertices")
    where = []
    m2 = 0
    for v, r in enumerate(rot):
        if len(set(r)) != len(r) or v in r:
            raise ValueError("not a simple graph")
        where.append({w: i for i, w in enumerate(r)})
        m2 += len(r)
    for v, r in enumerate(rot):
        for w in r:
            if not 0 <= w < n or v not in where[w]:
                raise ValueError("adjacency is not symmetric")
    seen = set()
    faces = 0
    for v in range(n):
        for w in rot[v]:
            if (v, w) in seen:
                continue
            faces += 1
            length = 0
            a, b = v, w
            while (a, b) not in seen:
                seen.add((a, b))
                length += 1
                r = rot[b]
                a, b = b, r[(where[b][a] - 1) % len(r)]
            if length != 3:
                raise ValueError("a face is not a triangle")
    if n - m2 // 2 + faces != 2:
        raise ValueError("the rotation system is not planar")
    for a, b in ((v1, v2), (v2, vn), (vn, v1)):
        if a not in where[b]:
            raise ValueError("outer face is not a triangle")
    for a, b, c in ((v1, vn, v2), (v2, v1, vn), (vn, v2, v1)):
        r = rot[a]
        if r[(where[a][b] + 1) % len(r)] != c:
            raise ValueError("outer face is not v1, v2, vn counterclockwise")


def draw(rot, v1, v2, vn):
    """Return integer coordinates [(x, y)] of a crossing-free drawing."""
    check_triangulation(rot, v1, v2, vn)
    n = len(rot)
    if n == 3:
        pos = [None] * 3
        pos[v1], pos[v2], pos[vn] = (0, 0), (2, 0), (1, 1)
        return pos
    order, lft, rgt = canonical_ordering(rot, v1, v2, vn)  # @line L1
    dx = [0] * n   # x offset relative to the parent in the shift tree
    y = [0] * n
    nxt = [-1] * n  # next vertex on the contour, or in a covered chain
    under = [-1] * n  # first vertex covered by v
    v3 = order[2]
    dx[v1], dx[v3], dx[v2] = 0, 1, 1
    y[v3] = 1
    nxt[v1], nxt[v3] = v3, v2  # @line L2
    for v in order[3:]:  # @line L3
        wp, wq = lft[v], rgt[v]  # @line L4
        first = nxt[wp]
        dx[first] += 1  # @line L5
        dx[wq] += 1  # @line L6
        delta = 0
        w = first
        while True:
            delta += dx[w]
            if w == wq:
                break
            w = nxt[w]
        dx[v] = (delta - y[wp] + y[wq]) // 2  # @line L7
        y[v] = (delta + y[wp] + y[wq]) // 2
        dx[wq] = delta - dx[v]  # @line L8
        if first != wq:
            dx[first] -= dx[v]  # @line L9
            w = first
            while nxt[w] != wq:
                w = nxt[w]
            nxt[w] = -1
            under[v] = first
        nxt[wp], nxt[v] = v, wq  # @line L10
    x = [0] * n  # @line L11
    stack = [(v1, 0)]
    while stack:
        v, base = stack.pop()
        x[v] = base + dx[v]
        if nxt[v] != -1:
            stack.append((nxt[v], x[v]))
        if under[v] != -1:
            stack.append((under[v], x[v]))
    return [(x[v], y[v]) for v in range(n)]  # @line L12
