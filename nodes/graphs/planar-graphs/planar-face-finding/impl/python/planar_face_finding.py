# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/planar-face-finding/. The authors are listed in prov/X3Q68V.jsonl.

from functools import cmp_to_key

Rotation = dict[int, list[int]]


def planar_face_finding(rot: Rotation) -> list[list[int]]:
    """Return the faces of the embedding given by the rotation system rot.

    rot[v] lists the neighbours of v in counterclockwise order. The graph is
    simple and undirected: w in rot[v] if and only if v in rot[w]. Each face is
    returned as the list of the tails of its darts, in walk order, so that the
    face lies on the left of each dart. An isolated vertex v gives the face [v]
    of length 0. Time O(n + m), extra space O(n + m).
    """
    pos: dict[tuple[int, int], int] = {}
    for v, around in rot.items():  # @line L1
        for i, w in enumerate(around):
            pos[(v, w)] = i
    visited: set[tuple[int, int]] = set()  # @line L2
    faces: list[list[int]] = []
    for u, around in rot.items():  # @line L3
        if not around:
            faces.append([u])  # an isolated vertex is a face of length 0
            continue
        for v in around:
            if (u, v) in visited:  # @line L4
                continue
            walk: list[int] = []  # @line L5
            d = (u, v)
            while d not in visited:  # @line L6
                visited.add(d)  # @line L7
                walk.append(d[0])
                a, b = d
                i = pos[(b, a)]  # @line L8
                ring = rot[b]
                d = (b, ring[i - 1])  # @line L9: the neighbour just before a
            faces.append(walk)  # @line L10
    return faces  # @line L11


def _half(dx: int, dy: int) -> int:
    return 0 if dy > 0 or (dy == 0 and dx > 0) else 1


def rotation_from_points(points: dict[int, tuple[int, int]], edges: list[tuple[int, int]]) -> Rotation:
    """Rotation system of a straight-line drawing with integer coordinates.

    The neighbours of each vertex are sorted counterclockwise by the exact
    angle of the edge, starting from the positive x direction, using only
    integer cross products. Time O(m log n).
    """
    rot: Rotation = {v: [] for v in points}
    for u, v in edges:
        rot[u].append(v)
        rot[v].append(u)
    for v, around in rot.items():
        x0, y0 = points[v]

        def cmp(a: int, b: int, x0: int = x0, y0: int = y0) -> int:
            ax, ay = points[a][0] - x0, points[a][1] - y0
            bx, by = points[b][0] - x0, points[b][1] - y0
            ha, hb = _half(ax, ay), _half(bx, by)
            if ha != hb:
                return ha - hb
            cross = ax * by - ay * bx
            return -1 if cross > 0 else (1 if cross < 0 else 0)

        around.sort(key=cmp_to_key(cmp))
    return rot
