# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karma-contention-manager/. The authors are listed in prov/GCR25F.jsonl.
"""The Karma contention manager of Scherer and Scott (2004, 2005).

The priority of a transaction is the number of objects it has opened,
summed over all its attempts: it grows by one at each open, is kept when the
transaction is aborted, and is reset to zero when it commits. When A meets
an active enemy B, A aborts B if its number of tries on this object exceeds
prio(B) - prio(A); otherwise A backs off for a fixed interval and tries
again.

Use it with the model in cmsim.py: `Karma(interval)` is a manager object;
the fixed backoff interval is counted in steps.

Precondition: interval >= 0. Cost: O(1) per decision; a transaction with
priority p below its enemy waits at most p + 1 intervals.
"""

from __future__ import annotations

from cmsim import Tx


class Karma:
    """Priority by work done, kept across aborts."""

    name = "karma"

    def __init__(self, interval: int = 1) -> None:
        self.interval = interval

    def begin(self, ts: int) -> Tx:
        return Tx(ts=ts)

    def opened(self, me: Tx) -> Tx:
        me = me._replace(prio=me.prio + 1)  # @line L1
        return me._replace(tries=0)  # @line L2

    def resolve(self, me: Tx, enemy: Tx) -> tuple[bool, Tx]:
        """Return (abort the enemy?, new state of me)."""
        if me.prio + me.tries > enemy.prio:  # @line L3
            return True, me  # @line L4
        me = me._replace(tries=me.tries + 1)  # @line L5
        me = me._replace(left=self.interval)  # @line L6
        return False, me  # @line L7

    def restarted(self, me: Tx) -> Tx:
        return me  # @line L8

    def committed(self, me: Tx) -> Tx:
        return me._replace(prio=0)  # @line L9
