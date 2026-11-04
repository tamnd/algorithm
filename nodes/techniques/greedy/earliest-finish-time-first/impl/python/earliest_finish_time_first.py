# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/earliest-finish-time-first/. The authors are listed in prov/4XRAFH.jsonl.

from typing import Protocol, Sequence, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...
    def __le__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def earliest_finish_time_first(activities: Sequence[tuple[T, T]]) -> list[int]:
    """Return a maximum set of pairwise compatible activities.

    Each activity is a pair (start, finish) with start < finish and stands for
    the half-open interval [start, finish). Two activities are compatible when
    one finishes at or before the other starts. The result is the list of the
    0-based indices of the chosen activities, in order of finish time.

    Cost: O(n log n) time for the sort and O(n) for the scan; O(n) extra space.
    """
    order = sorted(range(len(activities)), key=lambda i: activities[i][1])  # @line L1
    chosen: list[int] = []  # @line L2
    last: T | None = None  # @line L3
    for i in order:  # @line L4
        start, finish = activities[i]
        if last is None or last <= start:  # @line L5
            chosen.append(i)  # @line L6
            last = finish  # @line L7
    return chosen  # @line L8
