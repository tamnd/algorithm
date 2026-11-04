# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smoothsort/. The authors are listed in prov/WX5SGY.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def leonardo(limit: int) -> list[int]:
    """Return the Leonardo numbers 1, 1, 3, 5, 9, 15, ... up to the first one above limit."""
    nums = [1, 1]
    while nums[-1] <= limit:
        nums.append(nums[-1] + nums[-2] + 1)
    return nums


def sift_down(a: list[T], root: int, order: int, lp: list[int]) -> None:
    """Restore the max-heap order of the Leonardo tree of the given order whose root is at index root."""
    while order >= 2:
        right = root - 1  # the root of the subtree of order - 2
        left = right - lp[order - 2]  # the root of the subtree of order - 1
        if a[left] < a[right]:
            child, child_order = right, order - 2
        else:
            child, child_order = left, order - 1
        if not a[root] < a[child]:
            return
        a[root], a[child] = a[child], a[root]
        root, order = child, child_order


def rectify(a: list[T], trees: list[tuple[int, int]], j: int, lp: list[int]) -> None:
    """Make the roots of trees[0..j] ascending and tree j a max-heap, assuming the others are."""
    root, order = trees[j]
    while j > 0:
        prev = trees[j - 1][0]
        big = root
        if order >= 2:
            right = root - 1
            left = right - lp[order - 2]
            if a[big] < a[left]:
                big = left
            if a[big] < a[right]:
                big = right
        if not a[big] < a[prev]:
            break
        a[root], a[prev] = a[prev], a[root]
        j -= 1
        root, order = trees[j]
    sift_down(a, root, order, lp)


def smoothsort(a: list[T]) -> None:
    """Sort the list a in place, in non-decreasing order."""
    n = len(a)
    lp = leonardo(n)
    trees: list[tuple[int, int]] = []  # @line L1: (root index, order), from left to right
    for i in range(n):  # @line L2
        if len(trees) >= 2 and trees[-2][1] == trees[-1][1] + 1:  # @line L3
            order = trees[-2][1] + 1
            del trees[-2:]
            trees.append((i, order))
        elif trees and trees[-1][1] == 1:  # @line L4
            trees.append((i, 0))
        else:
            trees.append((i, 1))
        rectify(a, trees, len(trees) - 1, lp)  # @line L5
    for i in range(n - 1, 0, -1):  # @line L6
        root, order = trees.pop()  # @line L7: a[i] is the largest item left
        if order >= 2:  # @line L8
            right = root - 1
            left = right - lp[order - 2]
            trees.append((left, order - 1))
            rectify(a, trees, len(trees) - 1, lp)  # @line L9
            trees.append((right, order - 2))
            rectify(a, trees, len(trees) - 1, lp)
