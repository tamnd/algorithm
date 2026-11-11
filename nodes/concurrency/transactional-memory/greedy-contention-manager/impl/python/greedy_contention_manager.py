# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-contention-manager/. The authors are listed in prov/Z33CZD.jsonl.
"""The Greedy contention manager of Guerraoui, Herlihy and Pochon (PODC 2005).

A transaction gets a timestamp when it begins and keeps it when it restarts
after an abort; an older timestamp means a higher priority. When A finds
that active transaction B holds an object it needs:
  rule 1: if B is younger than A, or B is waiting, A aborts B;
  rule 2: otherwise A waits (sets its waiting flag) and asks again later.

Use it with the model in cmsim.py: `Greedy()` is a manager object.

Precondition: timestamps are distinct. Cost: O(1) per decision.
"""

from __future__ import annotations

from cmsim import Tx


class Greedy:
    """Rules 1 and 2 of the Greedy manager."""

    name = "greedy"

    def begin(self, ts: int) -> Tx:
        """A new transaction; ts comes from a shared counter (fetch-and-add)."""
        stamp = ts  # @line L1
        return Tx(ts=stamp, waiting=False)  # @line L2

    def resolve(self, me: Tx, enemy: Tx) -> tuple[bool, Tx]:
        """Return (abort the enemy?, new state of me)."""
        if enemy.ts > me.ts or enemy.waiting:  # @line L3
            return True, me  # @line L4
        me = me._replace(waiting=True)  # @line L5
        return False, me  # @line L6

    def opened(self, me: Tx) -> Tx:
        return me._replace(waiting=False, tries=0)  # @line L7

    def restarted(self, me: Tx) -> Tx:
        return me._replace(waiting=False)  # @line L8

    def committed(self, me: Tx) -> Tx:
        return me
