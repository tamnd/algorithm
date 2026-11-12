# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mattson-stack-algorithm/. The authors are listed in prov/CPEY4J.jsonl.

"""Mattson's one-pass stack algorithm: stack distances, and so hit counts for every cache size."""

from typing import Callable, Hashable, List, Optional, Sequence


def _next_uses(seq: Sequence[Hashable]) -> List[int]:
    n = len(seq)
    nxt, last = [n] * n, {}
    for t in range(n - 1, -1, -1):
        nxt[t] = last.get(seq[t], n)
        last[seq[t]] = t
    return nxt


def stack_distances(seq: Sequence[Hashable], policy: str = "lru") -> List[Optional[int]]:
    """Return the stack distance (1-based depth before the request, None if not in the stack) of each request.

    policy "lru" orders the stack by recency. policy "opt" orders it by the time of the next use,
    as Mattson et al. do for the optimal algorithm. A request with distance d is a hit in every
    cache of size k >= d.
    """
    if policy not in ("lru", "opt"):
        raise ValueError("policy must be 'lru' or 'opt'")
    nxt = _next_uses(seq)
    stamp = {}  # lru: time of the last use; opt: time of the next use after the current request
    stack: List[Hashable] = []  # @line L1: stack[0] is the top
    out: List[Optional[int]] = []  # the distances; hit_curve turns them into the histogram

    def keeps(a: Hashable, b: Hashable) -> bool:
        """True if a, already at this depth, has priority over the carried item b and stays."""
        if policy == "lru":
            return stamp[a] > stamp[b]
        return stamp[a] <= stamp[b]  # sooner next use stays; on a tie the item in place stays

    for t, y in enumerate(seq):  # @line L2, L3
        pos = None
        for i, z in enumerate(stack):  # @line L4: linear search, as in the original list version
            if z == y:
                pos = i
                break
        out.append(None if pos is None else pos + 1)  # @line L5
        stamp[y] = t if policy == "lru" else nxt[t]  # @line L6
        if pos == 0:  # @line L7
            continue
        if not stack:  # @line L8
            stack.append(y)
            continue
        carry = stack[0]  # @line L9
        stack[0] = y
        end = len(stack) if pos is None else pos
        for i in range(1, end):  # @line L10
            if not keeps(stack[i], carry):  # @line L11
                stack[i], carry = carry, stack[i]
        if pos is None:  # @line L12
            stack.append(carry)
        else:
            stack[pos] = carry
    return out


def hit_curve(distances: Sequence[Optional[int]], kmax: int) -> List[int]:
    """hits[k] for k = 0 .. kmax: the number of requests with distance at most k."""
    hist = [0] * (kmax + 2)
    for d in distances:
        if d is not None and d <= kmax:
            hist[d] += 1
    hits = [0] * (kmax + 1)
    for k in range(1, kmax + 1):  # @line L13
        hits[k] = hits[k - 1] + hist[k]
    return hits


def miss_ratio_curve(seq: Sequence[Hashable], kmax: int, policy: str = "lru") -> List[float]:
    """Miss ratio for k = 1 .. kmax from one pass."""
    n = len(seq)
    hits = hit_curve(stack_distances(seq, policy), kmax)
    return [1.0 - hits[k] / n if n else 0.0 for k in range(1, kmax + 1)]
