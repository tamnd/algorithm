# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-max-coverage/. The authors are listed in prov/CJWJGV.jsonl.

from typing import Hashable, Sequence


def greedy_max_coverage(sets: Sequence[set[Hashable]], k: int) -> tuple[list[int], set[Hashable]]:
    """Pick at most k sets, each time the one that covers the most new elements.

    Returns (chosen, covered). Ties go to the smallest index. The loop stops early
    when no set covers a new element.
    """
    covered: set[Hashable] = set()  # @line L1
    chosen: list[int] = []
    for _ in range(k):  # @line L2
        best, gain = -1, 0
        for j, s in enumerate(sets):  # @line L3: the largest marginal gain
            g = len(s - covered)
            if g > gain:
                best, gain = j, g
        if gain == 0:  # @line L4
            break
        chosen.append(best)  # @line L5
        covered |= sets[best]
    return chosen, covered  # @line L6
