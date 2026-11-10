# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/landlord-algorithm/. The authors are listed in prov/ESNB1H.jsonl.

from fractions import Fraction
from typing import Dict, Hashable, List, Sequence, Tuple

File = Hashable


def landlord(
    requests: Sequence[File],
    size: Dict[File, int],
    cost: Dict[File, int],
    k: int,
    reset: str = "full",
) -> Tuple[Fraction, List[Tuple[File, List[File]]]]:
    """Serve file requests with Young's Landlord rule on a cache of total size k.

    size and cost give a positive integer size and a non-negative cost for each file.
    reset is "full" (a hit raises the credit back to the cost) or "keep" (a hit
    leaves the credit). Of several files with zero credit, the one used least
    recently is evicted first.
    Returns (total fetch cost, a log of (file, evicted files) for each miss).
    Time: O(c) for each decrease of credits, with c <= k files in the cache.
    """
    if reset not in ("full", "keep"):
        raise ValueError("reset must be 'full' or 'keep'")
    credit: Dict[File, Fraction] = {}
    last: Dict[File, int] = {}
    used = 0
    total = Fraction(0)  # @line L1
    log: List[Tuple[File, List[File]]] = []
    for t, f in enumerate(requests):  # @line L2
        if size[f] > k:
            raise ValueError("a file is larger than the cache")
        if f in credit:  # @line L3
            if reset == "full":
                credit[f] = Fraction(cost[f])
            last[f] = t
            continue
        evicted: List[File] = []
        while used + size[f] > k:  # @line L4
            zero = [g for g in credit if credit[g] == 0]
            if zero:  # @line L5
                g = min(zero, key=lambda x: last[x])
                del credit[g]
                used -= size[g]
                evicted.append(g)
            else:
                delta = min(credit[g] / size[g] for g in credit)  # @line L6
                for g in credit:
                    credit[g] -= delta * size[g]
        credit[f] = Fraction(cost[f])  # @line L7
        last[f] = t
        used += size[f]
        total += cost[f]
        log.append((f, evicted))
    return total, log  # @line L8
