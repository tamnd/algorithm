# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spatial-cloaking/. The authors are listed in prov/JKVDFZ.jsonl.

from collections.abc import Sequence

Point = tuple[int, int]
Cell = tuple[int, int, int]  # (x, y, side): the half-open square [x, x + side) x [y, y + side)


def cloak(p: Point, users: Sequence[Point], k: int, h: int) -> Cell | None:
    """Return the smallest quadtree cell that holds p and at least k users, or None.

    users lists every known position, the requester included, with integer
    coordinates in [0, 2^h). Precondition: k >= 1, h >= 0 and p is in users.
    Cost: O(n h) time and O(n) extra space for n users.
    """
    q: Cell = (0, 0, 1 << h)  # @line L1
    q_prev = q
    d = 0
    v = list(users)  # @line L2
    if len(v) < k:  # @line L3
        return None
    while True:  # @line L4
        if len(v) < k:  # @line L5
            return q_prev
        if d == h:  # @line L6
            return q
        q_prev = q  # @line L7
        x, y, side = q
        half = side // 2
        q = (x + half if p[0] >= x + half else x, y + half if p[1] >= y + half else y, half)  # @line L8
        v = [u for u in v if q[0] <= u[0] < q[0] + half and q[1] <= u[1] < q[1] + half]  # @line L9
        d += 1  # @line L10


def reciprocity_holds(users: Sequence[Point], k: int, h: int) -> bool:
    """Return True if every region that CLOAK returns for some user is returned for at least k users.

    Precondition: as for cloak, and at least k users. Cost: O(n^2 h).
    """
    senders: dict[Cell | None, int] = {}
    for u in users:
        r = cloak(u, users, k, h)
        senders[r] = senders.get(r, 0) + 1
    return all(c >= k for c in senders.values())
