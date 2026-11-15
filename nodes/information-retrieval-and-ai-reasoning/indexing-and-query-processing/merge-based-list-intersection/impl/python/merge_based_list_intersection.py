# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merge-based-list-intersection/. The authors are listed in prov/06R0D3.jsonl.

from typing import Any, Sequence


def intersect(a: Sequence[Any], b: Sequence[Any]) -> list[Any]:
    """Return the ids that are in both a and b, in increasing order.

    Precondition: a and b are strictly increasing. Each step of the loop makes one
    three-way comparison (a test == and, when it fails, a test <), and the loop runs
    at most len(a) + len(b) - 1 times, so the time is O(len(a) + len(b)).
    """
    r: list[Any] = []
    i, j = 0, 0  # @line L1
    while i < len(a) and j < len(b):  # @line L2
        if a[i] == b[j]:  # @line L3
            r.append(a[i])  # @line L4
            i += 1
            j += 1
        elif a[i] < b[j]:  # @line L5
            i += 1
        else:
            j += 1  # @line L6
    return r  # @line L7


def intersect_all(lists: Sequence[Sequence[Any]]) -> list[Any]:
    """Return the ids that are in each list, in increasing order.

    Precondition: at least one list, each strictly increasing. The lists are taken in
    order of increasing length, two at a time, and the work stops when the result is empty.
    """
    order = sorted(lists, key=len)  # @line L8
    r = list(order[0])  # @line L9
    for t in range(1, len(order)):  # @line L10
        if not r:
            break
        r = intersect(r, order[t])  # @line L11
    return r  # @line L12
