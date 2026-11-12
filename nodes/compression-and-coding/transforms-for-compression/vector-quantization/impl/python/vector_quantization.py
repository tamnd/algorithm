# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vector-quantization/. The authors are listed in prov/ERP96S.jsonl.

"""Vector quantization: full-search encoding, the generalized Lloyd
iteration, the LBG design with codebook splitting (Linde, Buzo and Gray,
1980), a binary tree-structured VQ, and the hexagonal lattice quantizer.

A vector is a tuple of floats; the distortion is the squared Euclidean
distance. Full-search encoding costs O(N k) per vector for N codewords
of dimension k. One Lloyd iteration over M training vectors costs O(M N k).
"""

import math
from typing import List, Optional, Sequence, Tuple

Vector = Tuple[float, ...]


def dist2(a: Sequence[float], b: Sequence[float]) -> float:
    """Squared Euclidean distance."""
    return sum((x - y) ** 2 for x, y in zip(a, b))


def nearest(x: Sequence[float], codebook: Sequence[Sequence[float]]) -> int:
    """Index of the nearest codeword (full search; ties go to the lowest index)."""
    best, best_d = 0, math.inf
    for i, c in enumerate(codebook):
        d = dist2(x, c)
        if d < best_d:
            best, best_d = i, d
    return best


def mean(vectors: Sequence[Sequence[float]]) -> Vector:
    k = len(vectors[0])
    return tuple(sum(v[j] for v in vectors) / len(vectors) for j in range(k))


def distortion(data: Sequence[Sequence[float]], codebook: Sequence[Sequence[float]]) -> float:
    """Mean squared error per vector of full-search encoding."""
    return sum(dist2(x, codebook[nearest(x, codebook)]) for x in data) / len(data)


def lloyd(data: Sequence[Sequence[float]], codebook: Sequence[Sequence[float]], tol: float = 1e-4, max_iter: int = 100) -> Tuple[List[Vector], List[float]]:
    """Generalized Lloyd iteration from a start codebook.

    Returns the codebook and the distortion of each partition step; the
    list never increases. An empty cell keeps its old codeword.
    """
    cb = [tuple(c) for c in codebook]
    history: List[float] = []
    for _ in range(max_iter):  # @line L4
        cells: List[List[Sequence[float]]] = [[] for _ in cb]
        total = 0.0
        for x in data:  # @line L5
            i = nearest(x, cb)
            cells[i].append(x)
            total += dist2(x, cb[i])
        history.append(total / len(data))  # @line L7
        cb = [mean(cell) if cell else c for cell, c in zip(cells, cb)]  # @line L6
        if len(history) > 1 and history[-2] - history[-1] <= tol * history[-1]:  # @line L8
            break
    return cb, history


def lbg(data: Sequence[Sequence[float]], size: int, eps: float = 0.01, tol: float = 1e-4) -> Tuple[List[Vector], List[float]]:
    """LBG design with splitting; size must be a power of 2.

    Returns the codebook and the distortion after each Lloyd run (one per
    codebook size 1, 2, 4, ..., size).
    """
    if size < 1 or size & (size - 1):
        raise ValueError("size must be a power of 2")
    cb = [mean(data)]  # @line L1
    per_size = [distortion(data, cb)]
    # The split moves each codeword by +-eps times the spread of each coordinate.
    spread = [math.sqrt(sum((x[j] - cb[0][j]) ** 2 for x in data) / len(data)) or 1.0 for j in range(len(cb[0]))]
    while len(cb) < size:  # @line L2
        cb = [tuple(v + s * eps * d for v, d in zip(c, spread)) for c in cb for s in (1, -1)]  # @line L3
        cb, hist = lloyd(data, cb, tol)
        per_size.append(hist[-1] if hist else distortion(data, cb))
    final = distortion(data, cb)
    per_size[-1] = final
    return cb, per_size  # @line L9


class TreeVQ:
    """Binary tree-structured VQ: each node splits its training cell in two
    with a 2-codeword LBG design. Encoding costs O(k log N), with two
    distance computations per level."""

    def __init__(self, data: Sequence[Sequence[float]], depth: int, eps: float = 0.01) -> None:
        self.centre = mean(data)
        self.children: Optional[Tuple["TreeVQ", "TreeVQ"]] = None
        if depth > 0 and len(data) > 1:
            pair, _ = lbg(data, 2, eps)
            parts: List[List[Sequence[float]]] = [[], []]
            for x in data:
                parts[nearest(x, pair)].append(x)
            if parts[0] and parts[1]:
                self.children = (TreeVQ(parts[0], depth - 1, eps), TreeVQ(parts[1], depth - 1, eps))

    def encode(self, x: Sequence[float]) -> Vector:
        node = self
        while node.children is not None:
            a, b = node.children
            node = a if dist2(x, a.centre) <= dist2(x, b.centre) else b
        return node.centre

    def leaves(self) -> List[Vector]:
        if self.children is None:
            return [self.centre]
        return self.children[0].leaves() + self.children[1].leaves()


SQRT3 = math.sqrt(3.0)


def hexagonal_nearest(x: float, y: float) -> Tuple[float, float]:
    """Nearest point of the hexagonal lattice with minimum distance 1.

    The lattice is the union of the rectangular lattices Z x sqrt(3) Z and
    (Z + 1/2) x (sqrt(3) Z + sqrt(3)/2); the answer is the nearer of the
    nearest points of the two (Conway and Sloane's method for A2).
    """
    a = (round(x), round(y / SQRT3) * SQRT3)
    b = (math.floor(x) + 0.5, (math.floor(y / SQRT3) + 0.5) * SQRT3)
    return a if dist2((x, y), a) <= dist2((x, y), b) else b


HEXAGON_CELL_AREA = SQRT3 / 2  # area of a Voronoi cell, for minimum distance 1
HEXAGON_G = 5 / (36 * SQRT3)  # normalized second moment, about 0.0801875
