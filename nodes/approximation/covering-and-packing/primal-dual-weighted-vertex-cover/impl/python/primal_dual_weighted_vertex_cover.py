# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/primal-dual-weighted-vertex-cover/. The authors are listed in prov/7D7Y44.jsonl.

from fractions import Fraction
from typing import Hashable, Mapping, Sequence


def primal_dual_weighted_vertex_cover(
    weights: Mapping[Hashable, int | Fraction],
    edges: Sequence[tuple[Hashable, Hashable]],
) -> tuple[set[Hashable], dict[tuple[Hashable, Hashable], Fraction]]:
    """Return (cover, y).

    Scan the edges once. For an edge with no tight endpoint, raise its dual y_e
    until one endpoint becomes tight. The cover is the set of tight vertices.
    y is a feasible solution of the dual LP (a fractional packing of edges).
    """
    residual = {v: Fraction(w) for v, w in weights.items()}  # @line L1: w(v) - sum of y over edges at v
    if any(r < 0 for r in residual.values()):
        raise ValueError("weights must be non-negative")
    cover: set[Hashable] = set()
    y: dict[tuple[Hashable, Hashable], Fraction] = {}
    for u, v in edges:  # @line L2
        if u == v:
            raise ValueError("self-loop")
        if u in cover or v in cover:  # @line L3: the edge is covered
            y[(u, v)] = Fraction(0)
            continue
        delta = min(residual[u], residual[v])  # @line L4
        y[(u, v)] = delta  # @line L5
        residual[u] -= delta
        residual[v] -= delta
        for x in (u, v):  # @line L6: add each endpoint that became tight
            if residual[x] == 0:
                cover.add(x)
    return cover, y  # @line L7
