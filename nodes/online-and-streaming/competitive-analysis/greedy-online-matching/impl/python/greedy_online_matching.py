# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-online-matching/. The authors are listed in prov/39VNTT.jsonl.

from collections.abc import Callable, Hashable, Iterable, Sequence

Choose = Callable[[list[Hashable]], Hashable]


def first(free: list[Hashable]) -> Hashable:
    """Pick the first free neighbour in the order the arrival lists them."""
    return free[0]


class GreedyOnlineMatching:
    """Online greedy matching: each arrival takes a free neighbour if it has one.

    The offline side is the set `offline`. Call `arrive` once per online
    vertex, in order. The rule `choose` gets the free neighbours, in the order
    of the arrival's neighbour list, and must return one of them.
    """

    def __init__(self, offline: Iterable[Hashable], choose: Choose = first) -> None:
        self.free = set(offline)  # @line L1
        self.choose = choose
        self.match: list[Hashable | None] = []

    def arrive(self, neighbours: Iterable[Hashable]) -> Hashable | None:  # @line L3
        """Process one online vertex; return its partner or None. Cost O(degree)."""
        cand = [u for u in dict.fromkeys(neighbours) if u in self.free]  # @line L4
        partner = None
        if cand:  # @line L5
            partner = self.choose(cand)  # @line L6
            if partner not in self.free:
                raise ValueError("choose must return a free neighbour")
            self.free.remove(partner)  # @line L8
        self.match.append(partner)  # @line L7
        return partner


def greedy_online_matching(
    offline: Iterable[Hashable],
    arrivals: Sequence[Iterable[Hashable]],
    choose: Choose = first,
) -> list[Hashable | None]:
    """Run greedy on a whole arrival sequence; entry t is the partner of v_t."""
    g = GreedyOnlineMatching(offline, choose)
    for nb in arrivals:  # @line L2
        g.arrive(nb)
    return g.match  # @line L9


def matching_size(match: Sequence[Hashable | None]) -> int:
    return sum(1 for u in match if u is not None)


def adversary_half(choose: Choose, k: int) -> tuple[list[list[int]], list[Hashable | None]]:
    """Build the k-gadget sequence that holds a deterministic greedy rule to 1/2.

    Gadget i uses offline vertices 2i and 2i + 1. Its first arrival sees both;
    its second arrival sees only the vertex the rule took. The optimum is 2k.
    Returns the arrival lists and the run of the rule on them.
    """
    g = GreedyOnlineMatching(range(2 * k), choose)
    arrivals: list[list[int]] = []
    for i in range(k):
        a, b = 2 * i, 2 * i + 1
        arrivals.append([a, b])
        took = g.arrive([a, b])
        nxt = [a if took is None else took]
        arrivals.append(nxt)
        g.arrive(nxt)
    return arrivals, g.match
