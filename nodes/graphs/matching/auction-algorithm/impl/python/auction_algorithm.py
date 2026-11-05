# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/auction-algorithm/. The authors are listed in prov/YB4A74.jsonl.

from collections import deque
from typing import Callable, NamedTuple, Optional


class Auction(NamedTuple):
    assignment: Optional[list[int]]  # assignment[i] = object of person i, None if infeasible
    value: Optional[int]  # total benefit, None if infeasible
    prices: list[int]  # final prices, in units of benefit / (n + 1)
    bids: int  # number of bids made


def auction(
    benefit: list[list[Optional[int]]],
    on_bid: Optional[Callable[[int, int, int, Optional[int]], None]] = None,
) -> Auction:
    """Maximum-benefit assignment by Bertsekas' auction algorithm.

    benefit is an n by n matrix: person i values object j at benefit[i][j], an
    integer, or None if person i may not take object j. The graph is bipartite
    and weighted: persons on one side, objects on the other. Benefits are
    multiplied by n + 1 and the bid increment is epsilon = 1, so the result is
    optimal, not only within n * epsilon. Forbidden pairs get a benefit so low
    that an optimal assignment uses one only if no feasible assignment exists;
    then assignment and value are None. For minimum cost, negate the costs.

    on_bid(person, object, new price, outbid person or None) is called per bid.
    With C the largest difference between two finite benefits: O(n^2 C + n^2)
    bids without forbidden pairs, O(n) time each; O(n^2) space.
    """
    n = len(benefit)
    if any(len(row) != n for row in benefit):
        raise ValueError("benefit must be a square matrix")
    finite = [a for row in benefit for a in row if a is not None]
    low = min(finite, default=0)
    high = max(finite, default=0)
    forbidden = low - n * (high - low) - 1  # worse than any feasible assignment
    price = [0] * n  # @line L1
    owner = [-1] * n
    assigned = [-1] * n
    scaled = [  # @line L2
        [(n + 1) * (forbidden if a is None else a) for a in row] for row in benefit
    ]
    queue = deque(range(n))  # @line L3
    bids = 0
    while queue:  # @line L4
        i = queue.popleft()
        row = scaled[i]
        best_j = 0  # @line L5
        best = row[0] - price[0]
        for j in range(1, n):
            if row[j] - price[j] > best:
                best_j, best = j, row[j] - price[j]
        second = best  # @line L6
        if n > 1:
            second = max(row[j] - price[j] for j in range(n) if j != best_j)
        price[best_j] += best - second + 1  # @line L7
        loser = owner[best_j]
        if loser >= 0:  # @line L8
            assigned[loser] = -1
            queue.append(loser)
        owner[best_j] = i  # @line L9
        assigned[i] = best_j
        bids += 1
        if on_bid is not None:
            on_bid(i, best_j, price[best_j], loser if loser >= 0 else None)
    if any(benefit[i][assigned[i]] is None for i in range(n)):  # @line L10
        return Auction(None, None, price, bids)
    value = sum(benefit[i][assigned[i]] for i in range(n))  # type: ignore[misc]
    return Auction(assigned, value, price, bids)
