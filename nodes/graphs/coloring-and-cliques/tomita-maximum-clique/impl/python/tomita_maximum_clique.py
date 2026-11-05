# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tomita-maximum-clique/. The authors are listed in prov/B53EJC.jsonl.

from collections.abc import Sequence


def number_sort(r: list[int], nbr: list[set[int]]) -> tuple[list[int], list[int]]:
    """Greedy-color r in its order and return (r sorted by color, colors)."""
    classes: list[list[int]] = []
    for p in r:
        for cls in classes:
            if not any(q in nbr[p] for q in cls):
                cls.append(p)
                break
        else:
            classes.append([p])
    order: list[int] = []
    col: list[int] = []
    for k, cls in enumerate(classes, start=1):
        order.extend(cls)
        col.extend([k] * len(cls))
    return order, col


def tomita_maximum_clique(adj: Sequence[Sequence[int]]) -> list[int]:
    """Return a maximum clique of a simple undirected graph on vertices 0 .. n-1.

    adj[v] lists the neighbours of v. This is Tomita and Seki's MCQ: depth-first
    branch and bound in which the candidate set R is greedily colored, the vertex
    of largest color is expanded first, and a branch is cut as soon as
    |Q| + color <= |best|, since a clique uses each color at most once.
    The clique is returned sorted. Worst-case time O(2^n n^2), space O(n^2).
    """
    n = len(adj)
    nbr = [set(a) for a in adj]
    best: list[int] = []  # @line L1

    def expand(q: list[int], r: list[int]) -> None:
        nonlocal best
        r, col = number_sort(r, nbr)  # @line L4
        while r:  # @line L5
            p = r[-1]  # @line L6
            if len(q) + col[-1] <= len(best):  # @line L7
                return
            rp = [x for x in r if x in nbr[p]]  # @line L8
            if not rp:  # @line L9
                if len(q) + 1 > len(best):
                    best = q + [p]
            else:
                expand(q + [p], rp)  # @line L10
            r.pop()  # @line L11
            col.pop()

    order = sorted(range(n), key=lambda v: (-len(nbr[v]), v))
    expand([], order)  # @line L2
    return sorted(best)  # @line L3
