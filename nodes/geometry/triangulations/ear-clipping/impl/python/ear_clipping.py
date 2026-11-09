# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ear-clipping/. The authors are listed in prov/7DYMFT.jsonl.

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of pqr: positive for a left turn, zero when collinear. Exact for int and Fraction."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def in_closed_triangle(p: Point, a: Point, b: Point, c: Point) -> bool:
    """True when p lies in the closed counterclockwise triangle abc."""
    return orient(a, b, p) >= 0 and orient(b, c, p) >= 0 and orient(c, a, p) >= 0


def ear_clipping(poly: list[Point]) -> list[tuple[int, int, int]]:
    """Triangulate a simple polygon by clipping ears.

    poly lists the vertices in order, clockwise or counterclockwise, with no repeated vertex.
    Consecutive collinear vertices are allowed. The result is a list of n - 2 index triples,
    each a counterclockwise triangle. A polygon with fewer than 3 vertices gives [].
    """
    n = len(poly)
    if n < 3:
        return []
    area2 = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    if area2 == 0:
        raise ValueError("the polygon has zero area, so it is not simple")
    order = list(range(n)) if area2 > 0 else list(range(n - 1, -1, -1))  # @line L1
    nxt = {order[k]: order[(k + 1) % n] for k in range(n)}  # @line L2
    prv = {order[k]: order[k - 1] for k in range(n)}
    alive = set(order)

    def is_ear(v: int) -> bool:
        a, b, c = poly[prv[v]], poly[v], poly[nxt[v]]
        if orient(a, b, c) <= 0:  # @line L11
            return False
        for w in alive:  # @line L12
            if w not in (prv[v], v, nxt[v]) and in_closed_triangle(poly[w], a, b, c):
                return False
        return True

    ear = {v: is_ear(v) for v in order}  # @line L3
    work = [v for v in order if ear[v]]  # @line L4
    tris: list[tuple[int, int, int]] = []
    while len(alive) > 3:  # @line L5
        v = work.pop()  # @line L6
        if v not in alive or not ear[v]:
            continue
        u, w = prv[v], nxt[v]
        tris.append((u, v, w))  # @line L7
        alive.remove(v)  # @line L8
        nxt[u], prv[w] = w, u
        for x in (u, w):  # @line L9
            ear[x] = is_ear(x)
            if ear[x]:
                work.append(x)
    u = next(iter(alive))
    tris.append((prv[u], u, nxt[u]))  # @line L10
    return tris
