# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/list-contraction/. The authors are listed in prov/QF7GHN.jsonl.

"""List contraction by random mate, used for suffix sums on linked lists.

One round chooses an independent set of nodes with coin flips, splices them out and
folds their values into their predecessors. The rounds repeat until no node is left,
then the removed nodes get their results back in the reverse order of the rounds.
Every list comprehension below is one parallel step over independent nodes.
"""

import random
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TypeVar

T = TypeVar("T")


@dataclass
class Stats:
    """The number of live nodes at the start of each round, and the number removed in it."""

    live: list[int] = field(default_factory=list)
    removed: list[int] = field(default_factory=list)


def choose(live: list[int], nxt: list[int | None], rng: random.Random) -> list[int]:
    """Return the nodes that flip heads and whose successor is nil or flips tails."""
    coin = {i: rng.random() < 0.5 for i in live}  # @line L2
    return [i for i in live if coin[i] and (nxt[i] is None or not coin[nxt[i]])]  # @line L3


def suffix_sums(
    nxt: list[int | None], x: list[T], op: Callable[[T, T], T], rng: random.Random, stats: Stats | None = None
) -> list[T]:
    """Return y[i] = x[i] op x[next(i)] op ... op x[tail] for each node of a set of disjoint lists.

    op must be associative; it need not be commutative. Expected work O(n); the number of
    rounds is at most log_{4/3} n + 5 in expectation and O(log n) with high probability.
    """
    n = len(nxt)
    nxt = list(nxt)
    prv: list[int | None] = [None] * n
    for i in range(n):
        if nxt[i] is not None:
            prv[nxt[i]] = i
    val = list(x)
    y: list[T | None] = [None] * n
    live = list(range(n))
    history: list[list[int]] = []
    while live:  # @line L1: the base case is the empty list
        removed = choose(live, nxt, rng)
        if stats is not None:
            stats.live.append(len(live))
            stats.removed.append(len(removed))
        # @line L4: splice out all removed nodes at once; they are independent, so no
        # two of them touch the same cell
        gone = set(removed)
        for i in removed:
            p, q = prv[i], nxt[i]
            assert p not in gone and q not in gone
            if p is not None:
                val[p] = op(val[p], val[i])
                nxt[p] = q
            if q is not None:
                prv[q] = p
        history.append(removed)
        live = [i for i in live if i not in gone]  # @line L5 (a pack by prefix sums)
    # @line L6: the recursion on the smaller list is the next turn of the loop above
    for removed in reversed(history):  # @line L7: put the nodes back, last round first
        for i in removed:
            q = nxt[i]
            y[i] = val[i] if q is None else op(val[i], y[q])  # type: ignore[arg-type]
    return y  # type: ignore[return-value]
