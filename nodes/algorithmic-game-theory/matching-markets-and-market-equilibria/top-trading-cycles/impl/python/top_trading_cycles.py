# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/top-trading-cycles/. The authors are listed in prov/YD7XQN.jsonl.

from typing import Optional, Sequence


def top_trading_cycles(
    prefs: Sequence[Sequence[int]], start_order: Optional[Sequence[int]] = None
) -> list[int]:
    """Gale's top trading cycles for a Shapley-Scarf housing market.

    Agent i owns house i, for i = 0, ..., n - 1. prefs[i] is the strict ranking of agent i,
    best first. It must contain i; houses after i in the list are never used, so a list may
    stop at i (the agent would rather keep its house than take those). Returns x with x[i]
    the house that agent i gets.
    The walk keeps a path of agents, each pointing to the owner of its best remaining
    house; when the path closes a cycle, the cycle trades and leaves. start_order only
    changes the order in which walks start (the result does not depend on it).
    O(n + total list length) time, so O(n^2) for complete lists, and O(n) extra space:
    each agent enters the path once, and each list pointer only moves forward.
    """
    n = len(prefs)
    for i, lst in enumerate(prefs):
        if len(set(lst)) != len(lst) or any(not 0 <= h < n for h in lst) or i not in lst:
            raise ValueError("each list must be a ranking of houses that contains the own house")
    ptr = [0] * n  # @line L1
    left = [True] * n  # agent i and its house i are still in the market
    x = [-1] * n  # @line L2
    on_path = [False] * n
    order = range(n) if start_order is None else start_order
    for s in order:  # @line L3
        if not left[s]:
            continue
        path = [s]  # @line L4
        on_path[s] = True
        while path:  # @line L5
            i = path[-1]  # @line L6
            while not left[prefs[i][ptr[i]]]:  # @line L7
                ptr[i] += 1
            j = prefs[i][ptr[i]]  # @line L8
            if on_path[j]:  # @line L9
                cycle = []  # the agents j, ..., i at the end of the path
                while True:
                    k = path.pop()
                    x[k] = prefs[k][ptr[k]]  # k gets the house it points to
                    on_path[k] = False
                    cycle.append(k)
                    if k == j:
                        break
                for k in cycle:  # the houses of the cycle are the houses of its agents
                    left[k] = False
            else:  # @line L10
                path.append(j)
                on_path[j] = True
    return x  # @line L11
