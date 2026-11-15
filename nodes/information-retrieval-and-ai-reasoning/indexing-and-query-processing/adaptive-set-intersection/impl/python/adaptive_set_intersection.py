# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-set-intersection/. The authors are listed in prov/340HGS.jsonl.

from typing import Any, Sequence


def adaptive_intersect(lists: Sequence[Sequence[Any]], stats: dict[str, Any] | None = None) -> list[Any]:
    """Return the ids that are in each list, in increasing order.

    The one-sided form of the adaptive algorithm of Demaine, Lopez-Ortiz and Munro:
    one eliminator e, and one doubling step at a time in each list that is not yet
    known to hold e, in round robin. Precondition: at least one list, each strictly
    increasing. Only the tests < and == are used. A list s with r_s galloping runs
    makes at most 2 r_s log2(1 + n_s / r_s) + 2 r_s tests.

    If stats is a dict, it receives "runs" (the number of runs in each list, in the
    sorted order), "lengths" (the sorted lengths) and "eliminators" (how many times e
    was set).
    """
    order = sorted(lists, key=len)  # @line L1
    k = len(order)
    runs = [0] * k
    elims = 0
    out: list[Any] = []
    if all(len(lst) > 0 for lst in order):
        pos = [0] * k
        jump = [1] * k
        e = order[0][0]  # @line L2
        elims = 1
        pos[0] = 1
        held = {0}
        last = 0
        s = 0
        while True:  # @line L3
            if len(held) == k:  # @line L4
                out.append(e)  # @line L5
                if pos[last] == len(order[last]):  # @line L6
                    break
                e = order[last][pos[last]]  # @line L7
                elims += 1
                pos[last] += 1
                held = {last}
                continue
            s = (s + 1) % k  # @line L8
            while s in held:
                s = (s + 1) % k
            lst = order[s]
            n = len(lst)
            if pos[s] == n:  # @line L9
                break
            if jump[s] == 1:
                runs[s] += 1
            p = min(pos[s] + jump[s] - 1, n - 1)  # @line L10
            if lst[p] < e:  # @line L11
                if p == n - 1:  # @line L12
                    break
                pos[s] = p + 1  # @line L13
                jump[s] *= 2
            else:
                a, c = pos[s], p  # @line L14
                while a < c:  # @line L15
                    q = (a + c) // 2
                    if lst[q] < e:
                        a = q + 1
                    else:
                        c = q
                pos[s] = a + 1  # @line L16
                jump[s] = 1
                last = s
                if lst[a] == e:  # @line L17
                    held.add(s)
                else:
                    e = lst[a]  # @line L18
                    elims += 1
                    held = {s}
    if stats is not None:
        stats["runs"] = runs
        stats["lengths"] = [len(lst) for lst in order]
        stats["eliminators"] = elims
    return out
