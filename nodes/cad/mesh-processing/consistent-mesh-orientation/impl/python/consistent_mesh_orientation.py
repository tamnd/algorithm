# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consistent-mesh-orientation/. The authors are listed in prov/A5KM8D.jsonl.

"""Orient the faces of a mesh consistently, then make closed parts face outward.

A breadth-first search over the faces flips a neighbour when the shared edge
runs the same way in both faces. A conflict shows that the component is not
orientable, as for a Moebius strip. For a closed component, the exact signed
volume decides the outward side. Coordinates must be int or Fraction, so the
sign is exact.
"""

from collections import deque
from fractions import Fraction
from typing import NamedTuple, Optional, Sequence, Union

Num = Union[int, Fraction]


class Orientation(NamedTuple):
    faces: list[tuple[int, ...]]  # the faces, reversed where needed
    flipped: list[bool]  # whether each face was reversed
    component: list[int]  # the component number of each face
    orientable: list[bool]  # per component
    closed: list[bool]  # per component: no border edge
    volume6: list[Optional[Num]]  # per component: six times the signed volume after the fix


def det3(a: Sequence[Num], b: Sequence[Num], c: Sequence[Num]) -> Num:
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def signed_volume6(points: Sequence[Sequence[Num]], faces: Sequence[Sequence[int]]) -> Num:
    """Six times the signed volume bounded by oriented faces (fan triangulation of each face)."""
    total: Num = 0
    for f in faces:
        for i in range(1, len(f) - 1):
            total += det3(points[f[0]], points[f[i]], points[f[i + 1]])
    return total


def orient(faces: Sequence[Sequence[int]], points: Optional[Sequence[Sequence[Num]]] = None) -> Orientation:
    """Orient each edge-connected component; flip closed components to positive volume.

    Raise ValueError if an edge has three or more faces.
    """
    faces = [tuple(f) for f in faces]
    m = len(faces)
    uses: dict[tuple[int, int], list[tuple[int, int]]] = {}  # @line L1
    for f, face in enumerate(faces):
        k = len(face)
        if k < 3 or len(set(face)) != k:
            raise ValueError(f"face {f} is not a valid polygon: {face}")
        for i in range(k):
            u, v = face[i], face[(i + 1) % k]
            key, d = ((u, v), 1) if u < v else ((v, u), -1)
            uses.setdefault(key, []).append((f, d))
    for key, lst in uses.items():
        if len(lst) > 2:
            raise ValueError(f"edge {key} has {len(lst)} faces")
    face_edges: list[list[tuple[tuple[int, int], int]]] = [[] for _ in range(m)]
    for key, lst in uses.items():
        for f, d in lst:
            face_edges[f].append((key, d))

    s: list[int] = [-1] * m  # @line L2
    comp = [-1] * m
    orientable: list[bool] = []
    closed: list[bool] = []
    volume6: list[Optional[Num]] = []
    for r in range(m):  # @line L3
        if s[r] != -1:
            continue
        cid = len(orientable)
        s[r], comp[r] = 0, cid  # @line L4
        queue, members, ok, is_closed = deque([r]), [r], True, True
        while queue:  # @line L5
            f = queue.popleft()  # @line L6
            for key, df in face_edges[f]:  # @line L7
                lst = uses[key]
                if len(lst) == 1:
                    is_closed = False
                    continue
                g, dg = lst[1] if lst[0][0] == f else lst[0]
                want = s[f] ^ (1 if df == dg else 0)  # @line L8
                if s[g] == -1:  # @line L9
                    s[g], comp[g] = want, cid
                    queue.append(g)
                    members.append(g)
                elif s[g] != want:  # @line L10
                    ok = False
        vol: Optional[Num] = None
        if ok and is_closed and points is not None:  # @line L11
            oriented = [faces[f][::-1] if s[f] else faces[f] for f in members]
            vol = signed_volume6(points, oriented)  # @line L12
            if vol < 0:  # @line L13
                for f in members:
                    s[f] ^= 1
                vol = -vol
        orientable.append(ok)
        closed.append(is_closed)
        volume6.append(vol)
    out = [faces[f][::-1] if s[f] else faces[f] for f in range(m)]  # @line L14
    return Orientation(out, [x == 1 for x in s], comp, orientable, closed, volume6)


def is_consistent(faces: Sequence[Sequence[int]]) -> bool:
    """True if no directed edge is used twice."""
    seen: set[tuple[int, int]] = set()
    for face in faces:
        k = len(face)
        for i in range(k):
            e = (face[i], face[(i + 1) % k])
            if e in seen:
                return False
            seen.add(e)
    return True
