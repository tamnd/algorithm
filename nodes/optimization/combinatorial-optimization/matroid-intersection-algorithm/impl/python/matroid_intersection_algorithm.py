# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matroid-intersection-algorithm/. The authors are listed in prov/1YKCWY.jsonl.

from collections import deque
from typing import Callable, Optional

Oracle = Callable[[frozenset[int]], bool]


def matroid_intersection(
    n: int,
    indep1: Oracle,
    indep2: Oracle,
    on_augment: Optional[Callable[[list[int], frozenset[int]], None]] = None,
) -> tuple[list[int], list[int]]:
    """Largest common independent set of two matroids on the ground set 0 .. n-1.

    indep1 and indep2 are independence oracles: they take a frozenset of
    elements and return True if it is independent in the first or second
    matroid. Returns (I, U), where I is a maximum common independent set and
    U is a set with |I| = r1(U) + r2(E - U), which proves that I is maximum.
    Both are sorted lists.

    If on_augment is given, it is called with (path, new I) after each
    augmentation. It exists for tests.

    Cost: O(n r^2) oracle calls and O(n r^2) further time, where r is the
    answer, because there are r + 1 rounds and each builds the exchange graph
    with O(n r) oracle calls.
    """
    cur: set[int] = set()  # @line L1
    while True:  # @line L2
        base = frozenset(cur)
        outside = [x for x in range(n) if x not in cur]
        x1 = {x for x in outside if indep1(base | {x})}  # @line L3
        x2 = {x for x in outside if indep2(base | {x})}
        out: dict[int, list[int]] = {v: [] for v in range(n)}  # @line L4
        inn: dict[int, list[int]] = {v: [] for v in range(n)}
        for y in sorted(cur):
            without = base - {y}
            for x in outside:
                if indep1(without | {x}):
                    out[y].append(x)
                    inn[x].append(y)
                if indep2(without | {x}):
                    out[x].append(y)
                    inn[y].append(x)
        parent: dict[int, int] = {}  # @line L5
        queue = deque(sorted(x1))
        seen = set(x1)
        end = None
        while queue:
            v = queue.popleft()
            if v in x2:
                end = v
                break
            for u in out[v]:
                if u not in seen:
                    seen.add(u)
                    parent[u] = v
                    queue.append(u)
        if end is None:  # @line L6
            reach = set(x2)  # @line L7
            todo = list(x2)
            while todo:
                v = todo.pop()
                for u in inn[v]:
                    if u not in reach:
                        reach.add(u)
                        todo.append(u)
            return sorted(cur), sorted(reach)  # @line L8
        path = [end]
        while path[-1] in parent:
            path.append(parent[path[-1]])
        path.reverse()
        cur.symmetric_difference_update(path)  # @line L9
        if on_augment is not None:
            on_augment(path, frozenset(cur))
