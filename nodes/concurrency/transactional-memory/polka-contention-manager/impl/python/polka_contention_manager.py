# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polka-contention-manager/. The authors are listed in prov/D8YGK7.jsonl.
"""The Polka contention manager of Scherer and Scott (PODC 2005).

Polka joins Polite and Karma. The priority of a transaction is the number
of objects it has opened, over all its attempts (as in Karma): it grows at
each open, is kept on abort and is reset on commit. When A meets an active
enemy B, A backs off for prio(B) - prio(A) intervals whose length grows
exponentially (as in Polite), and then aborts B. The paper uses randomized
intervals; in this model interval i is 2^i steps of the waiting thread.

Use it with the model in cmsim.py: `Polka()` is a manager object.

Precondition: none. Cost: O(1) per decision; with a priority gap d that
does not change, a conflict ends after d waits and 2^d - 1 backoff steps.
"""

from __future__ import annotations

from cmsim import Tx


class Polka:
    """Karma's priorities with Polite's exponential backoff."""

    name = "polka"

    def begin(self, ts: int) -> Tx:
        return Tx(ts=ts)

    def opened(self, me: Tx) -> Tx:
        me = me._replace(prio=me.prio + 1)  # @line L1
        return me._replace(tries=0)  # @line L2

    def resolve(self, me: Tx, enemy: Tx) -> tuple[bool, Tx]:
        """Return (abort the enemy?, new state of me)."""
        if me.tries >= enemy.prio - me.prio:  # @line L3
            return True, me  # @line L4
        me = me._replace(left=2 ** me.tries)  # @line L5
        me = me._replace(tries=me.tries + 1)  # @line L6
        return False, me  # @line L7

    def restarted(self, me: Tx) -> Tx:
        return me  # @line L8

    def committed(self, me: Tx) -> Tx:
        return me._replace(prio=0)  # @line L9
