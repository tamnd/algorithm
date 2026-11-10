# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-cover-2-approximation/. The authors are listed in prov/MQCR0W.jsonl.

from typing import Hashable, Iterable


def vertex_cover_2_approximation(
    edges: Iterable[tuple[Hashable, Hashable]],
) -> tuple[set[Hashable], list[tuple[Hashable, Hashable]]]:
    """Return (cover, matching).

    The scan builds a maximal matching greedily. The cover is the set of the
    endpoints of the matching, so |cover| = 2 |matching|. Self-loops are not allowed.
    """
    cover: set[Hashable] = set()  # @line L1
    matching: list[tuple[Hashable, Hashable]] = []
    for u, v in edges:  # @line L2
        if u == v:
            raise ValueError("self-loop")
        if u not in cover and v not in cover:  # @line L3: the edge is not yet covered
            matching.append((u, v))  # @line L4
            cover.add(u)  # @line L5
            cover.add(v)
    return cover, matching  # @line L6
