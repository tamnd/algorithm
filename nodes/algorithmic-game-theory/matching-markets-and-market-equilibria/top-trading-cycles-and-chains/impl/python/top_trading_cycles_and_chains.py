# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/top-trading-cycles-and-chains/. The authors are listed in prov/4BQP88.jsonl.

from typing import Optional, Sequence

W = -1  # the waiting list option: priority on the deceased-donor waiting list

ACTIVE, TAIL, DONE = 0, 1, 2


def top_trading_cycles_and_chains(
    prefs: Sequence[Sequence[int]],
    priority: Optional[Sequence[int]] = None,
    keep: bool = True,
) -> tuple[list[int], list[int]]:
    """Top trading cycles and chains (Roth, Sonmez and Unver 2004).

    Pair i has patient i and donor kidney i. prefs[i] is the strict ranking of patient i,
    best first, over kidneys 0, ..., n - 1 and the option W = -1. It must contain i (keep
    the own kidney, that is, no exchange); entries after i are never used. priority is the
    order of the pairs for the chain selection rule (default 0, 1, ..., n - 1).
    keep=True is chain rule e: the selected w-chain stays, and the kidney at its tail stays
    available. keep=False is chain rule d: the chain is removed and its tail kidney goes to
    the waiting list at once.
    Returns (x, waitlist): x[i] is the kidney that patient i gets, or W, and waitlist is
    the sorted list of the kidneys that go to the deceased-donor waiting list.
    There are at most n rounds and each costs O(n) besides the pointer moves, which only go
    forward, so the time is O(n^2 + total list length) and the extra space is O(n).
    """
    n = len(prefs)
    for i, lst in enumerate(prefs):
        if len(set(lst)) != len(lst) or any(not -1 <= h < n for h in lst) or i not in lst:
            raise ValueError("each list must rank kidneys and W without repeats and contain the own kidney")
    order = list(range(n)) if priority is None else list(priority)
    if sorted(order) != list(range(n)):
        raise ValueError("priority must be an order of the pairs")
    ptr = [0] * n  # @line L1
    state = [ACTIVE] * n
    x: list[int] = [W] * n  # @line L2
    waitlist: list[int] = []
    active = n
    while active > 0:  # @line L3
        target = [W] * n
        for i in range(n):  # @line L4
            if state[i] == ACTIVE:
                while prefs[i][ptr[i]] != W and state[prefs[i][ptr[i]]] == DONE:
                    ptr[i] += 1
                target[i] = prefs[i][ptr[i]]
        cycles = []
        color = [0] * n  # 0 not seen, 1 on the current walk, 2 finished
        for s in range(n):
            if state[s] != ACTIVE or color[s] != 0:
                continue
            walk = []
            v = s
            while v != W and state[v] == ACTIVE and color[v] == 0:
                color[v] = 1
                walk.append(v)
                v = target[v]
            if v != W and state[v] == ACTIVE and color[v] == 1:
                cycles.append(walk[walk.index(v):])
            for u in walk:
                color[u] = 2
        if cycles:  # @line L5
            for cyc in cycles:  # @line L6
                for i in cyc:
                    x[i] = target[i]
                    state[i] = DONE
                active -= len(cyc)
        else:  # @line L7
            a = next(i for i in order if state[i] == ACTIVE)  # @line L8
            path = [a]  # @line L9
            while target[path[-1]] != W and state[target[path[-1]]] == ACTIVE:
                path.append(target[path[-1]])
            end = target[path[-1]]  # W, or the kidney of a TAIL pair
            for q in path:  # @line L10
                x[q] = target[q]
            for q in path[1:]:
                state[q] = DONE
            if end != W:
                state[end] = DONE
            active -= len(path)
            if keep:  # @line L11
                state[a] = TAIL
            else:
                state[a] = DONE
                waitlist.append(a)
    waitlist.extend(i for i in range(n) if state[i] == TAIL)  # @line L12
    return x, sorted(waitlist)
