# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marking-algorithm/. The authors are listed in prov/5WP5GD.jsonl.

from collections import OrderedDict
from collections.abc import Callable, Hashable, Iterable

Choose = Callable[[list[Hashable]], Hashable]


def oldest(unmarked: list[Hashable]) -> Hashable:
    """The rule of LRU: the unmarked page whose last request is oldest."""
    return unmarked[0]


class MarkingCache:
    """An online marking cache of size k, with a rule that picks the victim.

    The rule gets the unmarked cached pages, ordered from the oldest last
    request to the newest, and must return one of them.
    Cost per request: O(1) expected on a hit, and O(k) plus the cost of the
    rule on a fault with a full cache.
    """

    def __init__(self, k: int, choose: Choose = oldest) -> None:
        if k < 1:
            raise ValueError("k must be at least 1")
        self.k = k
        self.choose = choose
        # Cached pages in two maps, each ordered by last request.
        self.marked: OrderedDict[Hashable, None] = OrderedDict()  # @line L1
        self.unmarked: OrderedDict[Hashable, None] = OrderedDict()
        self.faults = 0
        self.phases = 0

    def cache(self) -> set[Hashable]:
        return set(self.marked) | set(self.unmarked)

    def request(self, p: Hashable) -> Hashable | None:
        """Serve a request for p. Return the evicted page, or None."""
        victim = None
        if p not in self.marked and p not in self.unmarked:  # @line L4
            self.faults += 1  # @line L5
            if len(self.marked) + len(self.unmarked) == self.k:  # @line L6
                if not self.unmarked:  # @line L7
                    self.unmarked, self.marked = self.marked, OrderedDict()
                    self.phases += 1
                victim = self.choose(list(self.unmarked))  # @line L8
                if victim not in self.unmarked:
                    raise ValueError("the rule must return an unmarked cached page")
                del self.unmarked[victim]  # @line L9
            self.marked[p] = None  # @line L10
        elif p in self.unmarked:
            del self.unmarked[p]  # @line L11
            self.marked[p] = None
        else:
            self.marked.move_to_end(p)
        if self.phases == 0:
            self.phases = 1
        return victim


def marking(sigma: Iterable[Hashable], k: int, choose: Choose = oldest) -> tuple[int, int]:
    """Serve sigma from an empty cache of size k with a marking algorithm.

    Precondition: k >= 1, pages are hashable, and choose returns an element
    of the list that it gets.
    Returns (faults, phases). Cost: O(n k) time in the worst case plus the cost
    of the rule, and O(k) space, with n requests.
    """
    m = MarkingCache(k, choose)
    for p in sigma:  # @line L2
        m.request(p)  # @line L3
    return m.faults, m.phases  # @line L12
