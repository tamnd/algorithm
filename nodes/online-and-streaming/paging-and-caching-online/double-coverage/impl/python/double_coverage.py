# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-coverage/. The authors are listed in prov/M90XJV.jsonl.

from fractions import Fraction
from typing import List, Sequence, Tuple, Union

Number = Union[int, Fraction]


def double_coverage(servers: Sequence[Number], requests: Sequence[Number]) -> Tuple[Number, List[Number]]:
    """Serve requests on the real line with the double coverage rule.

    servers: the start positions of the k servers (k >= 1), in any order.
    requests: the points of the request sequence.
    Returns (cost, positions): the total distance moved and the final sorted positions.
    Integer input gives integer positions. Each request takes O(log k) time to find
    its neighbours and O(1) time to move them.
    """
    s = sorted(servers)
    if not s:
        raise ValueError("at least one server is needed")
    cost: Number = 0  # @line L1
    for r in requests:  # @line L2
        if r <= s[0]:  # @line L3
            cost += s[0] - r
            s[0] = r
        elif r >= s[-1]:  # @line L4
            cost += r - s[-1]
            s[-1] = r
        else:
            i = _left_neighbour(s, r)  # @line L5
            if s[i] == r or s[i + 1] == r:
                continue
            delta = min(r - s[i], s[i + 1] - r)  # @line L6
            s[i] += delta  # @line L7
            s[i + 1] -= delta
            cost += 2 * delta  # @line L8
    return cost, s  # @line L9


def _left_neighbour(s: List[Number], r: Number) -> int:
    """Largest index i with s[i] <= r, for s[0] < r < s[-1]."""
    lo, hi = 0, len(s) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if s[mid] <= r:
            lo = mid
        else:
            hi = mid
    return lo
