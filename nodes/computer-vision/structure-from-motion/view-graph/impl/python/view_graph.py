# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/view-graph/. The authors are listed in prov/P4TY5D.jsonl.

"""A view graph: images as nodes, verified image pairs as edges.

The edge (i, j) stores the relative pose of camera j with respect to
camera i, in the convention X_j = R_ij X_i + t_ij (so R_ij = R_j R_i^T for
absolute rotations with X_c = R X_w + t), and a weight, usually the number
of inlier matches. The translation t_ij is known only up to a positive
scale. Each edge is stored in both directions: the reverse of (R, t) is
(R^T, -R^T t).
"""

import math
from collections import deque
from typing import Dict, List, Optional, Sequence, Tuple

Matrix = List[List[float]]
Vector = List[float]
EdgeData = Tuple[Matrix, Vector, float]


def _mul(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> Matrix:
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def _tr(a: Sequence[Sequence[float]]) -> Matrix:
    return [[a[j][i] for j in range(3)] for i in range(3)]


def rotation_angle(r: Sequence[Sequence[float]]) -> float:
    """The angle of a rotation matrix, arccos((tr R - 1) / 2)."""
    c = (r[0][0] + r[1][1] + r[2][2] - 1.0) / 2.0
    return math.acos(max(-1.0, min(1.0, c)))


class ViewGraph:
    def __init__(self) -> None:
        self.adj: Dict[int, Dict[int, EdgeData]] = {}

    def add_view(self, i: int) -> None:
        self.adj.setdefault(i, {})

    def add_edge(self, i: int, j: int, r: Matrix, t: Vector, w: float = 1.0) -> None:
        """Store the pair (i, j) in both directions."""
        if i == j:
            raise ValueError("add_edge: a view graph has no loops")
        self.add_view(i)
        self.add_view(j)
        self.adj[i][j] = ([list(row) for row in r], list(t), w)  # @line L1
        rt = _tr(r)
        self.adj[j][i] = (rt, [-sum(rt[a][b] * t[b] for b in range(3)) for a in range(3)], w)  # @line L2

    def remove_edge(self, i: int, j: int) -> None:
        del self.adj[i][j]
        del self.adj[j][i]

    def relative(self, i: int, j: int) -> Optional[EdgeData]:
        return self.adj.get(i, {}).get(j)

    def neighbors(self, i: int) -> List[int]:
        return sorted(self.adj.get(i, {}))

    def edges(self) -> List[Tuple[int, int, float]]:
        """Each edge once, as (i, j, w) with i < j."""
        return sorted((i, j, d[2]) for i in self.adj for j, d in self.adj[i].items() if i < j)

    def components(self) -> List[List[int]]:
        """The connected components, each sorted, by breadth-first search."""
        seen, out = set(), []
        for s in sorted(self.adj):
            if s in seen:
                continue
            seen.add(s)
            comp, queue = [], deque([s])
            while queue:
                i = queue.popleft()
                comp.append(i)
                for j in self.adj[i]:
                    if j not in seen:
                        seen.add(j)
                        queue.append(j)
            out.append(sorted(comp))
        return out

    def maximum_spanning_tree(self) -> List[Tuple[int, int]]:
        """Kruskal's method on the weights, largest first. On a graph that is
        not connected, the result is a spanning forest."""
        parent = {i: i for i in self.adj}  # @line L3
        tree = []

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for i, j, _ in sorted(self.edges(), key=lambda e: (-e[2], e[0], e[1])):  # @line L4
            ri, rj = find(i), find(j)
            if ri != rj:  # @line L5
                parent[ri] = rj  # @line L6
                tree.append((i, j))
        return tree  # @line L7

    def chain_rotations(self, tree: Sequence[Tuple[int, int]], root: int) -> Dict[int, Matrix]:
        """Absolute rotations of the views reached from root along the tree,
        with R_root = I and R_j = R_ij R_i."""
        tadj: Dict[int, List[int]] = {}
        for i, j in tree:
            tadj.setdefault(i, []).append(j)
            tadj.setdefault(j, []).append(i)
        rots = {root: [[1.0 if a == b else 0.0 for b in range(3)] for a in range(3)]}  # @line L8
        queue = deque([root])
        while queue:  # @line L9
            i = queue.popleft()  # @line L10
            for j in tadj.get(i, []):  # @line L11
                if j not in rots:
                    rots[j] = _mul(self.adj[i][j][0], rots[i])  # @line L12
                    queue.append(j)
        return rots  # @line L13

    def cycle_error(self, i: int, j: int, k: int) -> float:
        """The angle of R_ki R_jk R_ij, zero for consistent rotations."""
        r = _mul(self.adj[k][i][0], _mul(self.adj[j][k][0], self.adj[i][j][0]))
        return rotation_angle(r)  # @line L14
