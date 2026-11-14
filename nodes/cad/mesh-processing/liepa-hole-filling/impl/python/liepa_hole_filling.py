# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/liepa-hole-filling/. The authors are listed in prov/4HZ1HE.jsonl.

"""Fill a hole of a triangle mesh in the way of Liepa (SGP 2003).

1. A dynamic program over the border loop finds the triangulation of the loop
   of least weight. The weight of a triangle is a pair: the largest dihedral
   angle with its neighbours, then its area. Pairs add by (max, +) and are
   compared in lexicographic order.
2. Refinement splits large patch triangles at their centroids and flips patch
   edges that are not locally Delaunay, so that the patch gets the density of
   the mesh around it.
3. Fairing moves the new vertices to the solution of the uniform Laplace
   equation, with the loop fixed (a membrane patch).

The dynamic program is generic: `triangulate_loop` takes any weight and any
monotone way to add weights, so it can be tested against exhaustive search.
"""

from math import acos, sqrt
from typing import Callable, NamedTuple, Optional, Sequence, TypeVar

Vec = tuple[float, ...]
W = TypeVar("W")


# ---- vector helpers ----


def sub(a: Sequence[float], b: Sequence[float]) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a: Sequence[float], b: Sequence[float]) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def normal(p: Sequence[Sequence[float]], a: int, b: int, c: int) -> Vec:
    """The normal of the oriented triangle (a, b, c), twice its area long."""
    return cross(sub(p[b], p[a]), sub(p[c], p[a]))


def area(p: Sequence[Sequence[float]], a: int, b: int, c: int) -> float:
    n = normal(p, a, b, c)
    return sqrt(dot(n, n)) / 2


def dihedral(p: Sequence[Sequence[float]], t: tuple[int, int, int], u: tuple[int, int, int]) -> float:
    """The angle between the normals of two oriented triangles; 0 when they are flat."""
    n1, n2 = normal(p, *t), normal(p, *u)
    l1, l2 = dot(n1, n1), dot(n2, n2)
    if l1 == 0 or l2 == 0:
        return acos(-1.0)  # a degenerate triangle counts as the worst fold
    c = dot(n1, n2) / sqrt(l1 * l2)
    return acos(max(-1.0, min(1.0, c)))


# ---- the dynamic program ----


class LoopTriangulation(NamedTuple):
    weight: object  # the weight of the whole triangulation
    triangles: list[tuple[int, int, int]]  # positions in the loop, (i, m, k) with i < m < k


def triangulate_loop(
    n: int,
    omega: Callable[[int, int, int, Optional[int], Optional[int]], W],
    plus: Callable[[W, W], W],
    zero: W,
) -> LoopTriangulation:
    """Least weight triangulation of the loop 0, 1, ..., n - 1 by dynamic programming.

    omega(i, m, k, a, b) is the weight of the triangle (i, m, k). The values a and b
    are the apex of the triangle already chosen on the edge (i, m) and on the edge
    (m, k), or None when that edge is a loop edge. The weight of a triangulation is
    the plus of its triangle weights; the result is optimal when plus is monotone.
    """
    if n < 3:
        raise ValueError("a loop needs at least 3 vertices")
    cost: list[list[Optional[W]]] = [[None] * n for _ in range(n)]
    apex = [[-1] * n for _ in range(n)]
    for i in range(n - 1):  # @line L1
        cost[i][i + 1] = zero
    for j in range(2, n):  # @line L2
        for i in range(n - j):  # @line L3
            k = i + j  # @line L4
            for m in range(i + 1, k):  # @line L5
                a = apex[i][m] if m > i + 1 else None
                b = apex[m][k] if k > m + 1 else None
                cand = plus(plus(cost[i][m], cost[m][k]), omega(i, m, k, a, b))  # @line L6
                if cost[i][k] is None or cand < cost[i][k]:  # @line L7
                    cost[i][k], apex[i][k] = cand, m
    tris: list[tuple[int, int, int]] = []
    stack = [(0, n - 1)]
    while stack:  # @line L8
        i, k = stack.pop()
        if k - i >= 2:
            m = apex[i][k]
            tris.append((i, m, k))
            stack.append((i, m))
            stack.append((m, k))
    return LoopTriangulation(cost[0][n - 1], sorted(tris))


# ---- holes of a mesh ----


def border_loops(faces: Sequence[Sequence[int]]) -> list[list[int]]:
    """The border loops of an oriented manifold mesh, each in the order a patch must walk it.

    A face that uses the border edge a -> b leaves the patch to use b -> a, so each loop
    is listed along the reversed border edges. Each border vertex must have one
    border edge in and one out.
    """
    directed = set()
    for f in faces:
        for i in range(len(f)):
            directed.add((f[i], f[(i + 1) % len(f)]))
    nxt: dict[int, int] = {}
    for a, b in directed:
        if (b, a) not in directed:
            if b in nxt:
                raise ValueError("a vertex with two border loops")
            nxt[b] = a  # the patch walks b -> a
    loops, seen = [], set()
    for s in sorted(nxt):
        if s in seen:
            continue
        loop, v = [], s
        while v not in seen:
            seen.add(v)
            loop.append(v)
            v = nxt[v]
        loops.append(loop)
    return loops


def outside_apex(faces: Sequence[Sequence[int]], loop: Sequence[int]) -> list[Optional[int]]:
    """For each loop edge (loop[i], loop[i + 1]), the third vertex of the mesh triangle on it."""
    third: dict[tuple[int, int], int] = {}
    for f in faces:
        if len(f) == 3:
            for i in range(3):
                third[(f[i], f[(i + 1) % 3])] = f[(i + 2) % 3]
    n = len(loop)
    return [third.get((loop[(i + 1) % n], loop[i])) for i in range(n)]


def liepa_triangulation(points: Sequence[Sequence[float]], faces: Sequence[Sequence[int]],
                        loop: Sequence[int]) -> list[tuple[int, int, int]]:
    """Triangles over the mesh vertices that close the loop, with Liepa's weight."""
    n = len(loop)
    out = outside_apex(faces, loop)

    def omega(i: int, m: int, k: int, a: Optional[int], b: Optional[int]) -> tuple[float, float]:
        t = (loop[i], loop[m], loop[k])
        worst = 0.0
        # the neighbour across (i, m), then across (m, k), and across (k, i) at the top
        if a is not None:
            worst = max(worst, dihedral(points, t, (loop[i], loop[a], loop[m])))
        elif out[i] is not None:
            worst = max(worst, dihedral(points, t, (loop[m], loop[i], out[i])))
        if b is not None:
            worst = max(worst, dihedral(points, t, (loop[m], loop[b], loop[k])))
        elif out[m] is not None:
            worst = max(worst, dihedral(points, t, (loop[k], loop[m], out[m])))
        if i == 0 and k == n - 1 and out[n - 1] is not None:
            worst = max(worst, dihedral(points, t, (loop[i], loop[k], out[n - 1])))
        return (worst, area(points, *t))

    def plus(x: tuple[float, float], y: tuple[float, float]) -> tuple[float, float]:
        return (max(x[0], y[0]), x[1] + y[1])

    r = triangulate_loop(n, omega, plus, (0.0, 0.0))
    return [(loop[i], loop[m], loop[k]) for i, m, k in r.triangles]


# ---- refinement and fairing ----


def edge_scale(points: Sequence[Sequence[float]], faces: Sequence[Sequence[int]]) -> dict[int, float]:
    """The mean length of the mesh edges at each vertex (Liepa's sigma)."""
    total: dict[int, float] = {}
    count: dict[int, int] = {}
    seen = set()
    for f in faces:
        for i in range(len(f)):
            u, v = f[i], f[(i + 1) % len(f)]
            e = (min(u, v), max(u, v))
            if e in seen:
                continue
            seen.add(e)
            d = sub(points[u], points[v])
            ln = sqrt(dot(d, d))
            for x in e:
                total[x] = total.get(x, 0.0) + ln
                count[x] = count.get(x, 0) + 1
    return {x: total[x] / count[x] for x in total}


def _angle_at(p: Sequence[Sequence[float]], o: int, a: int, b: int) -> float:
    u, v = sub(p[a], p[o]), sub(p[b], p[o])
    lu, lv = dot(u, u), dot(v, v)
    if lu == 0 or lv == 0:
        return 0.0
    return acos(max(-1.0, min(1.0, dot(u, v) / sqrt(lu * lv))))


def relax(points: Sequence[Sequence[float]], patch: list[tuple[int, int, int]], fixed: set[tuple[int, int]]) -> int:
    """Flip patch edges whose two opposite angles sum to more than pi. Returns the number of flips."""
    flips = 0
    changed = True
    while changed and flips < 100 * len(patch) + 100:
        changed = False
        where: dict[tuple[int, int], int] = {}
        for idx, t in enumerate(patch):
            for i in range(3):
                where[(t[i], t[(i + 1) % 3])] = idx
        undirected = {(min(a, b), max(a, b)) for a, b in where}
        for (a, b), f in list(where.items()):
            g = where.get((b, a))
            if g is None or a > b or (a, b) in fixed or (b, a) in fixed:
                continue
            c = next(x for x in patch[f] if x not in (a, b))
            d = next(x for x in patch[g] if x not in (a, b))
            if c == d or (min(c, d), max(c, d)) in undirected:
                continue
            if _angle_at(points, c, a, b) + _angle_at(points, d, a, b) > acos(-1.0) + 1e-12:
                patch[f], patch[g] = (c, a, d), (d, b, c)  # a -> b is replaced by d -> c
                flips += 1
                changed = True
                break
    return flips


class Fill(NamedTuple):
    points: list[Vec]  # the old points, then the new ones
    patch: list[tuple[int, int, int]]  # the new triangles
    coarse: list[tuple[int, int, int]]  # the triangles of the dynamic program


def fill_hole(points: Sequence[Sequence[float]], faces: Sequence[Sequence[int]], loop: Sequence[int],
              alpha: float = sqrt(2.0), fair: bool = True, max_rounds: int = 50) -> Fill:
    """Triangulate, refine and fair the patch that closes one border loop."""
    pts: list[Vec] = [tuple(float(x) for x in p) for p in points]
    coarse = liepa_triangulation(pts, faces, loop)
    patch = list(coarse)
    sigma = edge_scale(pts, faces)
    n = len(loop)
    fixed = {(loop[i], loop[(i + 1) % n]) for i in range(n)}
    for v in loop:
        sigma.setdefault(v, 0.0)
    for _ in range(max_rounds):  # @line L9
        split = False
        new_patch = []
        for a, b, c in patch:
            ctr = tuple((pts[a][j] + pts[b][j] + pts[c][j]) / 3 for j in range(3))
            sc = (sigma[a] + sigma[b] + sigma[c]) / 3
            ok = True
            for v in (a, b, c):
                d = sub(ctr, pts[v])
                ln = alpha * sqrt(dot(d, d))
                if ln <= sc or ln <= sigma[v]:
                    ok = False
            if ok:
                k = len(pts)
                pts.append(ctr)
                sigma[k] = sc
                new_patch += [(a, b, k), (b, c, k), (c, a, k)]
                split = True
            else:
                new_patch.append((a, b, c))
        patch = new_patch
        relax(pts, patch, fixed)  # @line L10
        if not split:
            break
    if fair:
        fair_patch(pts, patch, set(range(len(points))))  # @line L11
    return Fill(pts, patch, coarse)


def fair_patch(pts: list[Vec], patch: Sequence[tuple[int, int, int]], fixed: set[int],
               tol: float = 1e-13, max_sweeps: int = 100000) -> None:
    """Move each free vertex of the patch to the mean of its neighbours (Gauss-Seidel)."""
    nb: dict[int, set[int]] = {}
    for t in patch:
        for i in range(3):
            for j in range(3):
                if i != j:
                    nb.setdefault(t[i], set()).add(t[j])
    free = sorted(v for v in nb if v not in fixed)
    for _ in range(max_sweeps):
        delta = 0.0
        for v in free:
            ns = nb[v]
            new = tuple(sum(pts[u][j] for u in ns) / len(ns) for j in range(3))
            d = sub(new, pts[v])
            delta = max(delta, abs(d[0]), abs(d[1]), abs(d[2]))
            pts[v] = new
        if delta < tol:
            break


def fill_all_holes(points: Sequence[Sequence[float]], faces: Sequence[Sequence[int]],
                   keep: Callable[[list[int]], bool] = lambda loop: True) -> tuple[list[Vec], list[tuple[int, ...]]]:
    """Fill every border loop for which keep(loop) is true, one after another."""
    pts: list[Vec] = [tuple(float(x) for x in p) for p in points]
    out: list[tuple[int, ...]] = [tuple(f) for f in faces]
    for loop in border_loops(faces):
        if keep(loop):
            r = fill_hole(pts, out, loop)
            pts = r.points
            out += r.patch
    return pts, out
