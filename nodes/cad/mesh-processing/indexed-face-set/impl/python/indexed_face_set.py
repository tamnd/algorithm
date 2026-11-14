# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/indexed-face-set/. The authors are listed in prov/A865QN.jsonl.

"""An indexed face set: vertex positions and faces given as lists of vertex indices.

The class adds an edge table (a hash map from each undirected edge to the
faces that use it) and a vertex-to-face table, so that the adjacency queries
take time proportional to the size of their answer. It also reads and writes
the OFF file format.
"""

from typing import Iterator, Sequence

Edge = tuple[int, int]


def edge_key(u: int, v: int) -> Edge:
    """The key of the undirected edge {u, v}."""
    return (u, v) if u < v else (v, u)


class IndexedFaceSet:
    """Vertices and polygonal faces, with edge and vertex incidence tables."""

    def __init__(self, vertices: Sequence[Sequence[float]], faces: Sequence[Sequence[int]]) -> None:
        """Build the tables. Each face needs at least 3 distinct vertex indices in range."""
        n = len(vertices)
        self.vertices: list[tuple] = [tuple(p) for p in vertices]
        self.faces: list[tuple[int, ...]] = []
        self.edges: dict[Edge, list[tuple[int, int]]] = {}  # @line L1
        self.vertex_face: list[list[int]] = [[] for _ in range(n)]
        for f, face in enumerate(faces):  # @line L2
            face = tuple(face)
            if len(face) < 3 or len(set(face)) != len(face) or min(face) < 0 or max(face) >= n:
                raise ValueError(f"face {f} is not a valid polygon: {face}")
            self.faces.append(face)
            k = len(face)
            for i in range(k):
                u, v = face[i], face[(i + 1) % k]  # @line L3
                self.edges.setdefault(edge_key(u, v), []).append((f, i))  # @line L4
                self.vertex_face[u].append(f)  # @line L5

    def edge_faces(self, u: int, v: int) -> list[int]:
        """The faces that use the edge {u, v}, with repeats if a face uses it twice."""
        return [f for f, _ in self.edges.get(edge_key(u, v), [])]  # @line L6

    def face_edges(self, f: int) -> Iterator[Edge]:
        face = self.faces[f]
        k = len(face)
        for i in range(k):
            yield edge_key(face[i], face[(i + 1) % k])

    def face_neighbors(self, f: int) -> list[int]:
        """The faces other than f that share an edge with f, each listed once."""
        out: list[int] = []
        seen = {f}
        for e in self.face_edges(f):  # @line L7
            for g, _ in self.edges[e]:
                if g not in seen:
                    seen.add(g)
                    out.append(g)
        return out

    def vertex_faces(self, v: int) -> list[int]:
        """The faces that have v as a vertex."""
        return list(self.vertex_face[v])

    def boundary_edges(self) -> list[Edge]:
        """The edges that exactly one face uses."""
        return [e for e, uses in self.edges.items() if len(uses) == 1]  # @line L8

    def non_manifold_edges(self) -> list[Edge]:
        """The edges that three or more faces use."""
        return [e for e, uses in self.edges.items() if len(uses) >= 3]

    def euler_characteristic(self) -> int:
        """V - E + F of the cell complex. An unused vertex counts as a point."""
        return len(self.vertices) - len(self.edges) + len(self.faces)  # @line L9

    def to_off(self) -> str:
        """The mesh in the OFF text format."""
        lines = ["OFF", f"{len(self.vertices)} {len(self.faces)} {len(self.edges)}"]
        lines += [" ".join(repr(c) for c in p) for p in self.vertices]
        lines += [" ".join(str(x) for x in (len(face),) + face) for face in self.faces]
        return "\n".join(lines) + "\n"


def _number(token: str) -> float:
    try:
        return int(token)
    except ValueError:
        return float(token)


def read_off(text: str) -> IndexedFaceSet:
    """Parse an OFF file. Comments start with #. The edge count of the header is ignored."""
    tokens: list[str] = []
    for line in text.splitlines():
        tokens += line.split("#", 1)[0].split()
    if not tokens or tokens[0] != "OFF":
        raise ValueError("not an OFF file")
    nv, nf = int(tokens[1]), int(tokens[2])
    pos = 4
    vertices = []
    for _ in range(nv):
        vertices.append(tuple(_number(t) for t in tokens[pos:pos + 3]))
        pos += 3
    faces = []
    for _ in range(nf):
        k = int(tokens[pos])
        faces.append(tuple(int(t) for t in tokens[pos + 1:pos + 1 + k]))
        pos += 1 + k
    return IndexedFaceSet(vertices, faces)
