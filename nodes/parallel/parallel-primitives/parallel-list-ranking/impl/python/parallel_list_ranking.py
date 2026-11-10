# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-list-ranking/. The authors are listed in prov/PJYJ60.jsonl.

"""Randomized work-efficient list ranking by random mate contraction.

The code follows the rounds of the algorithm. Each list comprehension is one parallel
loop over independent items. The costs are counted in the work-span model with binary
forking: a parallel loop over m items with a constant body has span ceil(log2 m) + 1,
and a pack of m items (a work-efficient prefix sum and a scatter) is charged work 2m
and span 2 ceil(log2 m) + 1, the cost proved on the prefix sum pages.
"""

import random
from dataclasses import dataclass


def ceil_log2(m: int) -> int:
    return 0 if m <= 1 else (m - 1).bit_length()


@dataclass
class Cost:
    work: int = 0
    span: int = 0
    rounds: int = 0

    def loop(self, m: int, body: int = 1) -> None:
        """Charge a parallel loop over m items with a constant body."""
        if m > 0:
            self.work += m * body
            self.span += ceil_log2(m) + body

    def pack(self, m: int) -> None:
        """Charge a pack (prefix sum plus scatter) over m items."""
        if m > 0:
            self.work += 2 * m
            self.span += 2 * ceil_log2(m) + 1


def random_mate_rank(nxt: list[int | None], rng: random.Random, cost: Cost | None = None) -> list[int]:
    """Return rank[i], the number of links from node i to the tail of its list.

    nxt[i] is the successor of i or None; the lists must be disjoint and acyclic.
    Expected work O(n); O(log n) rounds with high probability; span O(log^2 n) w.h.p.
    """
    c = cost if cost is not None else Cost()
    n = len(nxt)
    nxt = list(nxt)
    prv: list[int | None] = [None] * n
    w = [0 if nxt[i] is None else 1 for i in range(n)]  # @line L1
    c.loop(n)
    for i in [i for i in range(n) if nxt[i] is not None]:  # @line L2: exclusive writes
        prv[nxt[i]] = i  # type: ignore[index]
    c.loop(n)
    live = list(range(n))  # @line L3
    removed_by_round: list[list[int]] = []
    while live:  # @line L4
        coin = {i: rng.random() < 0.5 for i in live}  # @line L5
        c.loop(len(live))
        out = [i for i in live if coin[i] and (nxt[i] is None or not coin[nxt[i]])]  # @line L6
        c.loop(len(live))
        c.pack(len(live))
        for i in out:  # @line L7: the splices touch disjoint cells, so they run in parallel
            p, q = prv[i], nxt[i]
            if p is not None:
                w[p] += w[i]
                nxt[p] = q
            if q is not None:
                prv[q] = p
        c.loop(len(out))
        gone = set(out)
        live = [i for i in live if i not in gone]  # @line L8
        c.pack(len(live) + len(out))
        removed_by_round.append(out)
        c.rounds += 1
    rank = [0] * n
    for out in reversed(removed_by_round):  # @line L9
        for i in out:  # @line L10: the nodes of one round are independent
            q = nxt[i]
            rank[i] = w[i] + (rank[q] if q is not None else 0)
        c.loop(len(out))
    return rank  # @line L11
