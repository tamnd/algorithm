# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/small-versus-small-intersection/. The authors are listed in prov/39S9T4.jsonl.

from typing import Any, Sequence


def gallop(lst: Sequence[Any], x: Any, lo: int) -> int:
    """Return the least index p >= lo with lst[p] >= x, or len(lst) if there is none.

    Precondition: lst is sorted. Only the test < is used. If g = p - lo, the call makes
    one test when g = 0 and at most 2 floor(log2 g) + 2 tests when g >= 1, and no test
    when lo >= len(lst).
    """
    n = len(lst)
    if lo >= n or not (lst[lo] < x):
        return lo
    b = 1
    while lo + 2 * b - 1 < n and lst[lo + 2 * b - 1] < x:
        b *= 2
    a, c = lo + b, min(lo + 2 * b - 1, n)
    while a < c:
        q = (a + c) // 2
        if lst[q] < x:
            a = q + 1
        else:
            c = q
    return a


def svs(lists: Sequence[Sequence[Any]]) -> list[Any]:
    """Return the ids that are in each list, in increasing order (small-versus-small).

    Precondition: at least one list, each strictly increasing. The lists are taken by
    increasing length. Each candidate of the current result is searched in the next list
    by galloping from the place where the last search ended. Intersecting a candidate list
    of size r with a list of size n makes at most 2 r log2(1 + n/r) + 3 r tests.
    """
    order = sorted(lists, key=len)  # @line L1
    cand = list(order[0])  # @line L2
    for t in range(1, len(order)):  # @line L3
        if not cand:
            break
        lst = order[t]
        out: list[Any] = []
        p = 0  # @line L4
        for x in cand:  # @line L5
            p = gallop(lst, x, p)  # @line L6
            if p == len(lst):  # @line L7
                break
            if lst[p] == x:  # @line L8
                out.append(x)
                p += 1
        cand = out  # @line L9
    return cand  # @line L10
