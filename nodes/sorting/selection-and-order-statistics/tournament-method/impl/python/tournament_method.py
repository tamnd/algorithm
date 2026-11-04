# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tournament-method/. The authors are listed in prov/RB2RMG.jsonl.

from typing import Protocol, Sequence, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def tournament_second(a: Sequence[T]) -> tuple[T, T]:
    """Return (largest, second largest) of a, with n + ceil(lg n) - 2 comparisons at most.

    The second largest is the item of rank n - 1 in sorted order, so it equals
    the largest when the largest occurs twice. Uses only the operator <.
    """
    n = len(a)
    if n < 2:
        raise ValueError("need at least two items")
    players = list(range(n))  # @line L1
    beaten: list[list[int]] = [[] for _ in range(n)]  # @line L1
    while len(players) > 1:  # @line L2
        nxt: list[int] = []  # @line L3
        for j in range(0, len(players) - 1, 2):  # @line L4
            u, v = players[j], players[j + 1]  # @line L5
            if not a[u] < a[v]:  # @line L6
                w, l = u, v  # @line L6
            else:
                w, l = v, u  # @line L6
            beaten[w].append(l)  # @line L7
            nxt.append(w)  # @line L7
        if len(players) % 2 == 1:  # @line L8
            nxt.append(players[-1])  # @line L8
        players = nxt  # @line L9
    m = players[0]  # @line L10
    s = beaten[m][0]  # @line L11
    for i in beaten[m][1:]:  # @line L12
        if a[s] < a[i]:  # @line L12
            s = i  # @line L12
    return a[m], a[s]  # @line L13
