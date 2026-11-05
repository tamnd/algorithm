# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-covering-greedy/. The authors are listed in prov/EYK6H0.jsonl.
"""Greedy farthest-reach cover of a target interval.

The intervals and the target have one type: "closed" ([l, r] covering [s, t]),
"half-open" ([l, r) covering [s, t)) or "open" ((l, r) covering (s, t)).
"""

from typing import Optional, Sequence, Tuple

Interval = Tuple[float, float]


def interval_covering_greedy(
    intervals: Sequence[Interval], s: float, t: float, kind: str = "closed"
) -> Optional[list[int]]:
    """Return the indices of a fewest intervals whose union covers the target, or None.

    The target is [s, t], [s, t) or (s, t) by kind, with s < t.
    """
    if kind not in ("closed", "half-open", "open"):
        raise ValueError("kind must be closed, half-open or open")
    if not s < t:
        raise ValueError("the target needs s < t")
    order = sorted(range(len(intervals)), key=lambda k: intervals[k][0])  # @line L1
    reach, chosen, i = s, [], 0  # @line L2
    while reach < t:  # @line L3
        best, best_r = None, reach  # @line L4
        # Open intervals leave the point reach uncovered once something is
        # chosen, so the next interval must start strictly before it.
        strict = kind == "open" and chosen
        while i < len(order) and (  # @line L5
            intervals[order[i]][0] < reach or (not strict and intervals[order[i]][0] == reach)
        ):
            if intervals[order[i]][1] > best_r:  # @line L6
                best, best_r = order[i], intervals[order[i]][1]
            i += 1
        if best is None:  # @line L7
            return None
        chosen.append(best)  # @line L8
        reach = best_r
    return chosen  # @line L9
