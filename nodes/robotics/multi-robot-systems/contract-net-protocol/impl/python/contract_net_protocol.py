# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contract-net-protocol/. The authors are listed in prov/JAEWRV.jsonl.

"""Contract net protocol (Smith 1980) for single-task robots, in synchronous rounds.

Robots are 0..r-1 and tasks are 0..t-1. cost[i][j] is the bid of robot i for
task j, a number, or None when robot i is not eligible for task j. Each task has
a manager that announces it, collects bids and awards it. Each robot does at most
one task (single-task robots), and in each round an idle robot bids only on the
announced task it likes best, so it can never win two tasks at once.

The function counts the messages: an announcement goes to every robot (r
messages per announced task), a bid is one message, and an award is one message.
"""

from typing import Optional, Sequence


def contract_net(
    cost: Sequence[Sequence[Optional[float]]],
    batch: Optional[int] = None,
    order: Optional[Sequence[int]] = None,
) -> dict:
    """Run the protocol until every task is awarded or cannot be awarded.

    batch is the number of open tasks announced in each round (None means all
    of them). order is the order in which the managers announce their tasks
    (default 0..t-1). With batch=1 the protocol is a sequence of single-item
    auctions in the given order.

    Returns a dict with award (task -> robot), the total cost, the number of
    rounds and the message counts.
    """
    r = len(cost)
    t = len(cost[0]) if r else 0
    order = list(range(t)) if order is None else list(order)
    if sorted(order) != list(range(t)):
        raise ValueError("order must be a permutation of the tasks")
    open_tasks = list(order)  # @line L1
    idle = set(range(r))
    award = {}
    msgs = {"announce": 0, "bid": 0, "award": 0}
    rounds = 0
    while open_tasks:  # @line L2
        rounds += 1
        window = list(open_tasks if batch is None else open_tasks[:batch])
        msgs["announce"] += r * len(window)  # @line L3
        bids = {}
        for i in sorted(idle):  # @line L4
            best = None
            for j in window:
                c = cost[i][j]
                if c is not None and (best is None or (c, j) < best):
                    best = (c, j)
            if best is not None:
                bids.setdefault(best[1], []).append((best[0], i))
                msgs["bid"] += 1
        if not bids:  # @line L5
            # No idle robot is eligible for any task in the window. Robots
            # never become idle again, so these tasks can never be awarded.
            open_tasks = [j for j in open_tasks if j not in window]
            continue
        for j in window:  # @line L6
            if j in bids:
                c, i = min(bids[j])  # @line L7
                award[j] = i
                msgs["award"] += 1
                idle.discard(i)
                open_tasks.remove(j)
    total = sum(cost[i][j] for j, i in award.items())
    return {"award": award, "cost": total, "rounds": rounds, "messages": msgs}  # @line L8
