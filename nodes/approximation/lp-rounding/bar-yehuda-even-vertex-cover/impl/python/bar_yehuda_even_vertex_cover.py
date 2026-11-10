# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bar-yehuda-even-vertex-cover/. The authors are listed in prov/V1VWVP.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]


def bar_yehuda_even_vertex_cover(
    weights: Sequence[Number], edges: Sequence[tuple[int, int]]
) -> tuple[set[int], list[Number], list[Number]]:
    """Return (C, eps, r): a vertex cover, the amount taken off at each edge, and the residual weights.

    The vertices are 0 .. n - 1 with n = len(weights). Precondition: the
    weights are non-negative and no edge is a self-loop (else ValueError).
    The edges are scanned once in the given order. At edge uv the amount
    eps = min(r[u], r[v]) is taken off both ends, so one end drops to 0. The
    vertices with residual weight 0 form a cover C, and
    w(C) <= 2 * sum(eps) <= 2 * OPT. Time O(n + m), space O(n + m).
    """
    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative")
    r = list(weights)  # @line L1
    eps: list[Number] = []
    for u, v in edges:  # @line L2
        if u == v:
            raise ValueError("self-loops have no vertex cover of this form")
        e = min(r[u], r[v])  # @line L3
        r[u] -= e  # @line L4
        r[v] -= e
        eps.append(e)
    cover = {v for v in range(len(r)) if r[v] == 0}  # @line L5
    return cover, eps, r  # @line L6
