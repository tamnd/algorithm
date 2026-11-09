# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monotone-polygon-triangulation/. The authors are listed in prov/WF7BGF.jsonl.

from functools import cmp_to_key

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of pqr: positive for a left turn. Exact for int and Fraction."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def above(p: Point, q: Point) -> bool:
    """The sweep order: higher y first, and for equal y the smaller x first."""
    return p[1] > q[1] or (p[1] == q[1] and p[0] < q[0])


def triangulate_monotone(pts: list[Point], piece: list[int]) -> list[tuple[int, int, int]]:
    """Triangulate a y-monotone polygon. piece lists vertex indices in counterclockwise order."""
    m = len(piece)
    if m < 3:
        return []
    top = max(range(m), key=cmp_to_key(lambda a, b: 1 if above(pts[piece[a]], pts[piece[b]]) else -1))
    bot = min(range(m), key=cmp_to_key(lambda a, b: 1 if above(pts[piece[a]], pts[piece[b]]) else -1))
    left = set()  # counterclockwise from the top vertex down to the bottom is the left chain
    k = top
    while k != bot:
        left.add(piece[k])
        k = (k + 1) % m
    left_chain = []
    k = top
    while True:
        left_chain.append(piece[k])
        if k == bot:
            break
        k = (k + 1) % m
    right_chain = []
    k = top
    while True:
        right_chain.append(piece[k])
        if k == bot:
            break
        k = (k - 1) % m
    u = [left_chain[0]]  # @line L1
    a, b = 1, 1
    while a < len(left_chain) - 1 or b < len(right_chain) - 1:
        if b >= len(right_chain) - 1 or (a < len(left_chain) - 1 and above(pts[left_chain[a]], pts[right_chain[b]])):
            u.append(left_chain[a])
            a += 1
        else:
            u.append(right_chain[b])
            b += 1
    u.append(left_chain[-1])
    tris: list[tuple[int, int, int]] = []

    def emit(x: int, y: int, z: int) -> None:
        tris.append((x, y, z) if orient(pts[x], pts[y], pts[z]) > 0 else (x, z, y))

    stack = [u[0], u[1]]  # @line L2
    for j in range(2, m - 1):  # @line L3
        uj = u[j]
        if (uj in left) != (stack[-1] in left):  # @line L4
            while len(stack) > 1:  # @line L5
                s = stack.pop()
                emit(uj, s, stack[-1])
            stack = [u[j - 1], uj]  # @line L6
        else:
            last = stack.pop()  # @line L7
            sign = 1 if uj in left else -1
            while stack and sign * orient(pts[uj], pts[stack[-1]], pts[last]) > 0:  # @line L8
                emit(uj, last, stack[-1])
                last = stack.pop()
            stack.append(last)  # @line L9
            stack.append(uj)
    un = u[m - 1]
    while len(stack) > 1:  # @line L10
        s = stack.pop()
        emit(un, s, stack[-1])
    return tris


def make_monotone(pts: list[Point]) -> list[tuple[int, int]]:
    """Diagonals that split a counterclockwise simple polygon into y-monotone pieces (sweep).

    The status is a plain list searched linearly, which keeps the code short; a balanced
    search tree gives the O(n log n) bound.
    """
    n = len(pts)
    prv = lambda i: (i - 1) % n
    nxt = lambda i: (i + 1) % n
    kind = {}
    for i in range(n):
        p, q, r = pts[prv(i)], pts[i], pts[nxt(i)]
        if above(q, p) and above(q, r):
            kind[i] = "start" if orient(p, q, r) > 0 else "split"
        elif above(p, q) and above(r, q):
            kind[i] = "end" if orient(p, q, r) > 0 else "merge"
        else:
            kind[i] = "regular"
    status: list[int] = []  # edge e_i = (v_i, v_{i+1}), with the interior to its right
    helper: dict[int, int] = {}
    diags: list[tuple[int, int]] = []

    def right_of(e: int, f: int) -> bool:
        """For two edges crossing the sweep line, True if e lies to the right of f (larger x)."""
        a1, b1 = (e, nxt(e)) if above(pts[e], pts[nxt(e)]) else (nxt(e), e)
        a2, b2 = (f, nxt(f)) if above(pts[f], pts[nxt(f)]) else (nxt(f), f)
        if above(pts[a2], pts[a1]):
            return orient(pts[a2], pts[b2], pts[a1]) > 0
        return orient(pts[a1], pts[b1], pts[a2]) < 0

    def left_edge(i: int) -> int:
        best = -1
        for e in status:
            a, b = (e, nxt(e)) if above(pts[e], pts[nxt(e)]) else (nxt(e), e)
            if orient(pts[a], pts[b], pts[i]) > 0 and (best < 0 or right_of(e, best)):
                best = e
        return best

    order = sorted(range(n), key=cmp_to_key(lambda a, b: -1 if above(pts[a], pts[b]) else 1))
    for i in order:
        k = kind[i]
        if k == "start":
            status.append(i)
            helper[i] = i
        elif k == "end":
            if kind[helper[prv(i)]] == "merge":
                diags.append((i, helper[prv(i)]))
            status.remove(prv(i))
        elif k == "split":
            j = left_edge(i)
            diags.append((i, helper[j]))
            helper[j] = i
            status.append(i)
            helper[i] = i
        elif k == "merge":
            if kind[helper[prv(i)]] == "merge":
                diags.append((i, helper[prv(i)]))
            status.remove(prv(i))
            j = left_edge(i)
            if kind[helper[j]] == "merge":
                diags.append((i, helper[j]))
            helper[j] = i
        elif above(pts[prv(i)], pts[i]):  # regular vertex, interior to the right
            if kind[helper[prv(i)]] == "merge":
                diags.append((i, helper[prv(i)]))
            status.remove(prv(i))
            status.append(i)
            helper[i] = i
        else:
            j = left_edge(i)
            if kind[helper[j]] == "merge":
                diags.append((i, helper[j]))
            helper[j] = i
    return diags


def _faces(pts: list[Point], edges: list[tuple[int, int]]) -> list[list[int]]:
    """Bounded faces of a plane graph, each as a counterclockwise vertex list."""
    adj: dict[int, list[int]] = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)

    def angle_cmp(c: Point):
        def half(d):
            return 0 if d[1] > 0 or (d[1] == 0 and d[0] > 0) else 1

        def cmp(x: int, y: int) -> int:
            dx = (pts[x][0] - c[0], pts[x][1] - c[1])
            dy = (pts[y][0] - c[0], pts[y][1] - c[1])
            if half(dx) != half(dy):
                return half(dx) - half(dy)
            cr = dx[0] * dy[1] - dx[1] * dy[0]
            return -1 if cr > 0 else (1 if cr < 0 else 0)
        return cmp

    pos: dict[tuple[int, int], int] = {}
    for v, nb in adj.items():
        nb.sort(key=cmp_to_key(angle_cmp(pts[v])))
        for t, w in enumerate(nb):
            pos[(v, w)] = t
    seen = set()
    faces = []
    for a, b in edges:
        for start in ((a, b), (b, a)):
            if start in seen:
                continue
            face = []
            u, v = start
            while (u, v) not in seen:
                seen.add((u, v))
                face.append(u)
                nb = adj[v]
                w = nb[(pos[(v, u)] - 1) % len(nb)]  # the neighbor just before u, counterclockwise around v
                u, v = v, w
            area2 = sum(orient(pts[face[0]], pts[face[t]], pts[face[t + 1]]) for t in range(1, len(face) - 1))
            if area2 > 0:
                faces.append(face)
    return faces


def triangulate_polygon(poly: list[Point]) -> list[tuple[int, int, int]]:
    """Triangulate a simple polygon: split it into monotone pieces, then triangulate each piece."""
    n = len(poly)
    if n < 3:
        return []
    area2 = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    if area2 == 0:
        raise ValueError("the polygon has zero area, so it is not simple")
    order = list(range(n)) if area2 > 0 else list(range(n - 1, -1, -1))
    pts = [poly[v] for v in order]
    diags = make_monotone(pts)
    edges = [(i, (i + 1) % n) for i in range(n)] + diags
    tris = []
    for piece in _faces(pts, edges):
        tris.extend(triangulate_monotone(pts, piece))
    return [(order[a], order[b], order[c]) for a, b, c in tris]
