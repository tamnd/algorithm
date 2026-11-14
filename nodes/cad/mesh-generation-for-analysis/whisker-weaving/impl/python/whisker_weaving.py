# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whisker-weaving/. The authors are listed in prov/4SHZ6G.jsonl.

"""The dual sheets of a hex mesh: the spatial twist continuum that whisker weaving builds.

Whisker weaving builds the sheets first and the hexes last. This module does
the opposite step, which is exact and always works: from a given conforming
hex mesh it finds the sheets, the three sheet crossings of every hex, the
boundary quads, and the loops (chords) of the boundary quad mesh. A hex is a
list of 8 vertex ids in the standard order of mg4geom. An edge is the sorted
pair of its vertex ids, and a face is identified by its set of 4 vertex ids.
"""

from typing import Dict, Hashable, List, Sequence, Tuple

from mg4geom import EDGE_CLASSES, FACES

Edge = Tuple[int, int]


class DisjointSets:
    """Union-find with path halving and union by size."""

    def __init__(self) -> None:
        self.parent: Dict[Hashable, Hashable] = {}
        self.size: Dict[Hashable, int] = {}

    def add(self, x: Hashable) -> None:
        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1

    def find(self, x: Hashable) -> Hashable:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: Hashable, y: Hashable) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]

    def classes(self) -> List[List[Hashable]]:
        groups: Dict[Hashable, List[Hashable]] = {}
        for x in self.parent:
            groups.setdefault(self.find(x), []).append(x)
        return sorted(sorted(g) for g in groups.values())


def edge(a: int, b: int) -> Edge:
    return (a, b) if a < b else (b, a)


def hex_faces(h: Sequence[int]) -> List[Tuple[int, int, int, int]]:
    """The six faces of a hex as vertex tuples, counterclockwise seen from outside."""
    return [tuple(h[i] for i in f) for f in FACES]


def dual_sheets(hexes: Sequence[Sequence[int]]):
    """The sheets, crossings, boundary quads and loops of a conforming hex mesh.

    Returns a dict with
      sheets:   list of sheets, each a sorted list of edges (the dual vertices of the sheet),
      sheet_of: edge -> index of its sheet,
      crossing: for each hex, the sheet indices of its classes u, v and w,
      boundary: the faces that belong to exactly one hex,
      interior: the number of faces shared by two hexes,
      loops:    the chords of the boundary quad mesh, each a sorted list of edges,
      loop_sheet: for each loop, the sheet that contains it.
    Cost: O(H alpha(H)) for H hexes, plus sorting for a canonical output.
    """
    edges = DisjointSets()  # @line L1
    for h in hexes:  # @line L2
        for cls in EDGE_CLASSES:  # @line L3
            es = [edge(h[i], h[j]) for i, j in cls]
            for e in es:
                edges.add(e)
            for e in es[1:]:
                edges.union(es[0], e)  # @line L4
    sheets = edges.classes()  # @line L5
    sheet_of = {e: s for s, members in enumerate(sheets) for e in members}
    crossing = [tuple(sheet_of[edge(h[cls[0][0]], h[cls[0][1]])] for cls in EDGE_CLASSES) for h in hexes]  # @line L6
    count: Dict[frozenset, int] = {}
    first: Dict[frozenset, Tuple[int, int, int, int]] = {}
    for h in hexes:
        for f in hex_faces(h):
            key = frozenset(f)
            count[key] = count.get(key, 0) + 1
            first.setdefault(key, f)
    boundary = sorted(first[k] for k, c in count.items() if c == 1)  # @line L7
    interior = sum(1 for c in count.values() if c == 2)
    if any(c > 2 for c in count.values()):
        raise ValueError("a face belongs to more than two hexes")
    chords = DisjointSets()  # @line L8
    for a, b, c, d in boundary:  # @line L9
        e0, e1, e2, e3 = edge(a, b), edge(b, c), edge(c, d), edge(d, a)
        for e in (e0, e1, e2, e3):
            chords.add(e)
        chords.union(e0, e2)  # @line L10
        chords.union(e1, e3)
    loops = chords.classes()  # @line L11
    loop_sheet = [sheet_of[lp[0]] for lp in loops]
    return {  # @line L12
        "sheets": sheets,
        "sheet_of": sheet_of,
        "crossing": crossing,
        "boundary": boundary,
        "interior": interior,
        "loops": loops,
        "loop_sheet": loop_sheet,
    }


def sheet_euler(hexes: Sequence[Sequence[int]], result, s: int) -> int:
    """The Euler characteristic V - E + F of sheet s as a cell complex.

    V: the edges of the sheet. E: the pairs of opposite sheet edges on a hex face
    (one dual edge per such face and pair). F: one dual face per hex class in sheet s.
    """
    sheet_of = result["sheet_of"]
    v = len(result["sheets"][s])
    seen = set()
    f = 0
    for h in hexes:
        for cls in EDGE_CLASSES:
            if sheet_of[edge(h[cls[0][0]], h[cls[0][1]])] == s:
                f += 1
        for a, b, c, d in hex_faces(h):
            for p, q in ((edge(a, b), edge(c, d)), (edge(b, c), edge(d, a))):
                if sheet_of[p] == s and sheet_of[q] == s:
                    seen.add((frozenset((a, b, c, d)), frozenset((p, q))))
    return v - len(seen) + f


def voxel_mesh(voxels):
    """The hex mesh of a set of unit voxels (i, j, k), with the lattice point (x, y, z) as vertex id."""
    ids: Dict[Tuple[int, int, int], int] = {}
    hexes = []
    for i, j, k in sorted(voxels):
        h = []
        for a, b, c in ((0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)):
            p = (i + a, j + b, k + c)
            h.append(ids.setdefault(p, len(ids)))
        hexes.append(h)
    points = sorted(ids, key=ids.get)
    return points, hexes


def pillowed_cube():
    """The cube [0, 3]^3 meshed by the inner cube [1, 2]^3 and six hexes that join it to the outer faces."""
    outer = [(0, 0, 0), (3, 0, 0), (3, 3, 0), (0, 3, 0), (0, 0, 3), (3, 0, 3), (3, 3, 3), (0, 3, 3)]
    inner = [(1, 1, 1), (2, 1, 1), (2, 2, 1), (1, 2, 1), (1, 1, 2), (2, 1, 2), (2, 2, 2), (1, 2, 2)]
    points = outer + inner
    hexes = [[8, 9, 10, 11, 12, 13, 14, 15]]
    for f in FACES:
        # the inner face, then the outer face, both counterclockwise seen from outside
        hexes.append([8 + f[0], 8 + f[1], 8 + f[2], 8 + f[3], f[0], f[1], f[2], f[3]])
    return points, hexes
