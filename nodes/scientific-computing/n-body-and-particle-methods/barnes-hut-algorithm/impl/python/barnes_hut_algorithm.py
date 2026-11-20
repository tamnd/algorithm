# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barnes-hut-algorithm/. The authors are listed in prov/RQH8DT.jsonl.
"""Barnes-Hut tree code for gravitational accelerations.

The bodies have masses m[i] and positions x[i] in dimension 2 (quadtree) or
3 (octree); any dimension works. Each cell is a cube with 2^dim children and
stores its total mass and center of mass (the monopole). A cell of side s
whose center of mass is at distance d from the target is accepted when
s / d < theta and the target is not inside the cell; otherwise it is opened.
theta = 0 opens every cell and gives direct summation.

Pair potential: -G m_i m_j / sqrt(r^2 + eps^2) (Plummer softening); G = 1
unless given.
"""

import math
from typing import Optional, Sequence

Vec = Sequence[float]
MAX_DEPTH = 48  # bodies closer than side / 2^48 share one leaf


class Cell:
    __slots__ = ("lo", "side", "bodies", "children", "mass", "com")

    def __init__(self, lo: list[float], side: float) -> None:
        self.lo = lo
        self.side = side
        self.bodies: list[int] = []
        self.children: Optional[list[Optional["Cell"]]] = None
        self.mass = 0.0
        self.com = [0.0] * len(lo)

    def contains(self, p: Vec) -> bool:
        return all(self.lo[k] <= p[k] <= self.lo[k] + self.side for k in range(len(p)))


def _child_index(cell: Cell, p: Vec) -> int:
    half = cell.side / 2
    idx = 0
    for k in range(len(p)):
        if p[k] >= cell.lo[k] + half:
            idx |= 1 << k
    return idx


def _insert(cell: Cell, i: int, x: Sequence[Vec], depth: int) -> None:
    if cell.children is None:
        if not cell.bodies or depth >= MAX_DEPTH:  # @line L3
            cell.bodies.append(i)
            return
        dim = len(x[i])
        cell.children = [None] * (1 << dim)  # @line L4
        old = cell.bodies
        cell.bodies = []
        for k in old:
            _insert_child(cell, k, x, depth)
    _insert_child(cell, i, x, depth)  # @line L5


def _insert_child(cell: Cell, i: int, x: Sequence[Vec], depth: int) -> None:
    c = _child_index(cell, x[i])
    assert cell.children is not None
    if cell.children[c] is None:
        half = cell.side / 2
        lo = [cell.lo[k] + (half if (c >> k) & 1 else 0.0) for k in range(len(cell.lo))]
        cell.children[c] = Cell(lo, half)
    _insert(cell.children[c], i, x, depth + 1)


def _summarize(cell: Cell, m: Sequence[float], x: Sequence[Vec]) -> None:
    dim = len(cell.lo)
    parts: list[tuple[float, Vec]] = [(m[i], x[i]) for i in cell.bodies]
    if cell.children is not None:
        for ch in cell.children:
            if ch is not None:
                _summarize(ch, m, x)
                parts.append((ch.mass, ch.com))
    cell.mass = sum(w for w, _ in parts)  # @line L6
    cell.com = [sum(w * p[k] for w, p in parts) / cell.mass for k in range(dim)]


def build_tree(m: Sequence[float], x: Sequence[Vec]) -> Cell:
    """Build the 2^dim-ary tree and fill in the mass and center of mass of every cell."""
    dim = len(x[0])
    lo = [min(p[k] for p in x) for k in range(dim)]
    side = max(max(p[k] for p in x) - lo[k] for k in range(dim)) or 1.0
    root = Cell(lo, side * (1 + 1e-12))  # @line L1
    for i in range(len(m)):  # @line L2
        _insert(root, i, x, 0)
    _summarize(root, m, x)
    return root


def _pull(a: list[float], g: float, src: Vec, p: Vec, e2: float) -> None:
    d = [src[k] - p[k] for k in range(len(p))]
    s = sum(c * c for c in d) + e2
    if s == 0.0:
        raise ValueError("two bodies at the same point with eps = 0")
    w = g / (s * math.sqrt(s))
    for k in range(len(p)):
        a[k] += w * d[k]


def tree_force(root: Cell, i: int, m: Sequence[float], x: Sequence[Vec], theta: float,
               eps: float = 0.0, G: float = 1.0) -> tuple[list[float], int]:
    """Acceleration of body i from the tree, and the number of interactions used."""
    p = x[i]
    e2 = eps * eps
    a = [0.0] * len(p)
    count = 0
    stack = [root]
    while stack:
        c = stack.pop()
        if c.children is None:  # @line L7
            for j in c.bodies:
                if j != i:
                    _pull(a, G * m[j], x[j], p, e2)
                    count += 1
            continue
        d = math.dist(c.com, p)
        if d > 0 and c.side < theta * d and not c.contains(p):  # @line L8
            _pull(a, G * c.mass, c.com, p, e2)
            count += 1
            continue
        stack.extend(ch for ch in c.children if ch is not None)  # @line L9
    return a, count  # @line L10


def barnes_hut(m: Sequence[float], x: Sequence[Vec], theta: float = 0.5, eps: float = 0.0,
               G: float = 1.0) -> tuple[list[list[float]], int]:
    """Accelerations of all bodies and the total number of interactions."""
    root = build_tree(m, x)
    acc, total = [], 0
    for i in range(len(m)):
        a, c = tree_force(root, i, m, x, theta, eps, G)
        acc.append(a)
        total += c
    return acc, total


def leaves(cell: Cell) -> list[Cell]:
    if cell.children is None:
        return [cell]
    out = []
    for ch in cell.children:
        if ch is not None:
            out.extend(leaves(ch))
    return out
