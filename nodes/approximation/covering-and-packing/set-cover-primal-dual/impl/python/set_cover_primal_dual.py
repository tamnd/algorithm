# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-cover-primal-dual/. The authors are listed in prov/24X7Z1.jsonl.

from fractions import Fraction
from typing import Hashable, Sequence


def set_cover_primal_dual(
    elements: Sequence[Hashable],
    sets: Sequence[set[Hashable]],
    costs: Sequence[int | Fraction],
) -> tuple[list[int], dict[Hashable, Fraction]]:
    """Return (chosen, y).

    elements lists the universe in the order in which the loop visits it.
    chosen holds the indices of the tight sets, in the order in which they became tight.
    y is a feasible solution of the dual LP, and each chosen set is tight for it.
    Raises ValueError if an element is in no set.
    """
    holders: dict[Hashable, list[int]] = {e: [] for e in elements}
    for j, s in enumerate(sets):
        for e in s:
            if e in holders:
                holders[e].append(j)
    y = {e: Fraction(0) for e in elements}  # @line L1
    residual = [Fraction(c) for c in costs]  # residual[j] = c_j - sum of y_e over e in S_j
    in_cover = [False] * len(sets)
    chosen: list[int] = []
    covered: set[Hashable] = set()
    for e in elements:  # @line L2
        if e in covered:  # @line L3
            continue
        if not holders[e]:
            raise ValueError(f"element {e!r} is in no set")
        delta = min(residual[j] for j in holders[e])  # @line L4
        y[e] = delta  # @line L5
        for j in holders[e]:
            residual[j] -= delta
        for j in holders[e]:  # @line L6: add each set that became tight
            if residual[j] == 0 and not in_cover[j]:
                in_cover[j] = True
                chosen.append(j)
                covered |= sets[j]
    return chosen, y  # @line L7
