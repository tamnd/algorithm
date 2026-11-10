# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boyer-moore-majority/. The authors are listed in prov/FE4TJK.jsonl.

from collections.abc import Hashable, Iterable
from typing import TypeVar

T = TypeVar("T", bound=Hashable)


def majority_candidate(stream: Iterable[T]) -> tuple[T | None, int]:
    """Return (candidate, count) after one pass of the Boyer-Moore vote.

    If the stream has a majority item (one that occurs more than half of the
    time), the candidate is that item. Otherwise the candidate can be any item,
    and it is None only for an empty stream. Items need only an equality test.
    Cost: one pass, O(1) time for each item, and two words of memory.
    """
    candidate: T | None = None  # @line L1
    count = 0  # @line L1
    for x in stream:  # @line L2
        if count == 0:  # @line L3
            candidate, count = x, 1  # @line L4
        elif x == candidate:  # @line L5
            count += 1  # @line L6
        else:  # @line L7
            count -= 1  # @line L8
    return candidate, count  # @line L9


def merge_candidates(a: tuple[T | None, int], b: tuple[T | None, int]) -> tuple[T | None, int]:
    """Merge the first-pass states of two streams into the state of their concatenation.

    Equal candidates add their counts. Different candidates cancel: the one
    with the larger count stays, with the difference of the counts. The
    pairing invariant holds for the result, so a majority of the concatenated
    stream is the merged candidate. Cost: O(1).
    """
    (c1, n1), (c2, n2) = a, b
    if n1 == 0:
        return (c2, n2) if n2 > 0 else (c1 if c1 is not None else c2, 0)
    if n2 == 0:
        return c1, n1
    if c1 == c2:
        return c1, n1 + n2
    return (c1, n1 - n2) if n1 >= n2 else (c2, n2 - n1)


def majority(items: list[T]) -> T | None:
    """Return the majority item of a list, or None if there is none.

    Two passes: the first finds the candidate, the second counts it.
    Cost: O(m) time for m items and O(1) extra memory.
    """
    candidate, _ = majority_candidate(items)
    if candidate is None:
        return None
    occurrences = sum(1 for x in items if x == candidate)  # @line L10
    return candidate if 2 * occurrences > len(items) else None  # @line L11
