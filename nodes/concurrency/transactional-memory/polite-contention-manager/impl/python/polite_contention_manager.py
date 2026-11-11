# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polite-contention-manager/. The authors are listed in prov/6YVCN1.jsonl.
"""The Polite contention manager of Scherer and Scott (2004, 2005).

When A meets an active enemy B, A backs off for an interval that grows
exponentially with the number of tries on this object; after m rounds of
backoff it aborts B. The paper spins for a random time with mean
2^(tries + k) ns, with k = 4 and m = 22 on their machine. In this model the
interval is 2^tries steps of the waiting thread, so the backoff is fixed and
the scheduler decides what the other threads do meanwhile.

Use it with the model in cmsim.py: `Polite(m)` is a manager object.

Precondition: m >= 0. Cost: O(1) per decision; a conflict ends after m
waits and 2^m - 1 backoff steps if the enemy keeps the object.
"""

from __future__ import annotations

from cmsim import Tx


class Polite:
    """Exponential backoff, then abort the enemy."""

    name = "polite"

    def __init__(self, m: int = 3) -> None:
        self.m = m

    def begin(self, ts: int) -> Tx:
        return Tx(ts=ts)

    def resolve(self, me: Tx, enemy: Tx) -> tuple[bool, Tx]:
        """Return (abort the enemy?, new state of me)."""
        if me.tries >= self.m:  # @line L1
            return True, me  # @line L2
        me = me._replace(left=2 ** me.tries)  # @line L3
        me = me._replace(tries=me.tries + 1)  # @line L4
        return False, me  # @line L5

    def opened(self, me: Tx) -> Tx:
        return me._replace(tries=0)  # @line L6

    def restarted(self, me: Tx) -> Tx:
        return me

    def committed(self, me: Tx) -> Tx:
        return me
