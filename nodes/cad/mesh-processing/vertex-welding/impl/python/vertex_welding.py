# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-welding/. The authors are listed in prov/09QVC4.jsonl.

"""Weld the vertices of a mesh that lie within a distance eps of each other.

A uniform grid with cells of side eps finds the close pairs, and a disjoint-set
forest joins them. Two points are joined when their distance is at most eps,
and joining is transitive, so a chain of close points becomes one vertex.
Coordinates and eps must be int or Fraction, so the tests are exact.
"""

from fractions import Fraction
from itertools import product
from math import floor
from typing import NamedTuple, Sequence, Union

Num = Union[int, Fraction]


class Weld(NamedTuple):
    points: list[tuple[Num, ...]]  # one position per new vertex
    faces: list[tuple[int, ...]]  # remapped faces, degenerate ones removed
    new_index: list[int]  # new vertex of each old vertex
    dropped: list[int]  # indices of the input faces that became degenerate
    non_manifold_edges: list[tuple[int, int]]  # edges of the output with three or more faces


class DisjointSet:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            if ra < rb:
                self.parent[rb] = ra
            else:
                self.parent[ra] = rb


def close(p: Sequence[Num], q: Sequence[Num], eps: Num) -> bool:
    return sum((a - b) * (a - b) for a, b in zip(p, q)) <= eps * eps


def weld_classes(points: Sequence[Sequence[Num]], eps: Num) -> list[int]:
    """The representative (smallest index) of the class of each point."""
    if eps <= 0:
        raise ValueError("eps must be positive")
    n = len(points)
    cells: dict[tuple[int, ...], list[int]] = {}
    key = []
    for i, p in enumerate(points):  # @line L1
        c = tuple(floor(Fraction(x) / eps) for x in p)
        key.append(c)
        cells.setdefault(c, []).append(i)
    ds = DisjointSet(n)  # @line L2
    offsets = list(product((-1, 0, 1), repeat=len(points[0]) if n else 3))
    for i in range(n):  # @line L3
        for off in offsets:
            c = tuple(a + b for a, b in zip(key[i], off))
            for j in cells.get(c, ()):
                if j > i and close(points[i], points[j], eps):  # @line L4
                    ds.union(i, j)
    return [ds.find(i) for i in range(n)]  # @line L5


def clean_face(face: Sequence[int]) -> tuple[int, ...]:
    """Remove repeats of consecutive vertices, cyclically."""
    out: list[int] = []
    for v in face:
        if not out or out[-1] != v:
            out.append(v)
    while len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return tuple(out)


def weld(points: Sequence[Sequence[Num]], faces: Sequence[Sequence[int]], eps: Num) -> Weld:
    """Weld close vertices, remap the faces and remove the faces that collapse."""
    rep = weld_classes(points, eps)
    order = sorted(set(rep))
    new_of_rep = {r: k for k, r in enumerate(order)}
    new_index = [new_of_rep[r] for r in rep]
    new_points = [tuple(points[r]) for r in order]
    out_faces: list[tuple[int, ...]] = []
    dropped: list[int] = []
    for f, face in enumerate(faces):
        g = clean_face([new_index[v] for v in face])  # @line L6
        if len(g) < 3 or len(set(g)) != len(g):  # @line L7
            dropped.append(f)
        else:
            out_faces.append(g)
    count: dict[tuple[int, int], int] = {}
    for g in out_faces:
        for i in range(len(g)):
            u, v = g[i], g[(i + 1) % len(g)]
            e = (min(u, v), max(u, v))
            count[e] = count.get(e, 0) + 1
    bad = sorted(e for e, k in count.items() if k >= 3)
    return Weld(new_points, out_faces, new_index, dropped, bad)  # @line L8
