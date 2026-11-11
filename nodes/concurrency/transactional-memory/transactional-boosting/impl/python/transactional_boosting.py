# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transactional-boosting/. The authors are listed in prov/BFAFX0.jsonl.
"""Transactional boosting (Herlihy and Koskinen, 2008) of a set of keys.

The base object is a linearizable set: each call (add, remove, contains)
is one atomic step of the scheduler in sched.py. A transaction is a list of
calls. Before a call on key k, the transaction takes the abstract lock of k
(calls on different keys commute, so one lock per key is enough). After a
call that changed the set, it logs the inverse call. On commit it releases
its locks. On abort it runs the inverses, newest first, and then releases
its locks. A transaction that finds a lock held by another transaction
aborts itself and waits until that lock is free, then starts again; this
stands for the timeout of the paper.

Two wrong variants are given for the tests: use_locks=False drops the
abstract locks, and inverse="none" or inverse="blind" drops the undo log or
logs an inverse that ignores the result of the call.

Precondition: transactions are lists of (method, key) pairs with method in
{"add", "remove", "contains"}. Cost: O(1) steps per call; an abort costs
one step per logged inverse.
"""

from __future__ import annotations

from itertools import permutations
from typing import Any, Generator

Gen = Generator[Any, None, Any]
Call = tuple[str, int]


def apply(items: set[int], call: Call) -> bool:
    """Run one call on a plain set; return its result."""
    m, k = call
    if m == "add":
        if k in items:
            return False
        items.add(k)
        return True
    if m == "remove":
        if k not in items:
            return False
        items.remove(k)
        return True
    if m == "contains":
        return k in items
    raise ValueError(m)


def inverse(call: Call, result: bool) -> Call | None:
    """The inverse of a call that returned result, or None if it changed nothing."""
    m, k = call
    if m == "add" and result:
        return ("remove", k)
    if m == "remove" and result:
        return ("add", k)
    return None


class BoostedSet:
    """A linearizable set used inside transactions through boosting."""

    def __init__(self, initial: set[int] | None = None, use_locks: bool = True,
                 inverse_mode: str = "correct") -> None:
        self.items: set[int] = set(initial or ())
        self.initial = frozenset(self.items)
        self.use_locks = use_locks
        self.inverse_mode = inverse_mode
        self.locks: dict[int, int] = {}
        self.committed: list[tuple[int, list[Call], list[bool]]] = []

    def _undo_entry(self, call: Call, r: bool) -> Call | None:
        if self.inverse_mode == "none":
            return None
        if self.inverse_mode == "blind":
            m, k = call
            return {"add": ("remove", k), "remove": ("add", k)}.get(m)
        return inverse(call, r)

    def transaction(self, pid: int, calls: list[Call], cancel_first: bool = False,
                    max_attempts: int = 1_000) -> Gen:
        """Run calls as one boosted transaction; return their results.

        With cancel_first, the first attempt aborts itself after its last
        call, which tests the undo log.
        """
        for attempt in range(1, max_attempts + 1):
            held: list[int] = []
            undo: list[Call] = []
            results: list[bool] = []
            blocker = None
            for call in calls:
                k = call[1]  # @line L1
                if self.use_locks and k not in held:  # @line L2
                    owner = self.locks.get(k)
                    if owner is not None:  # @line L3
                        blocker = k
                        break
                    self.locks[k] = pid
                    held.append(k)  # @line L4
                    yield
                r = apply(self.items, call)  # @line L5
                entry = self._undo_entry(call, r)
                if entry is not None:  # @line L6
                    undo.append(entry)  # @line L7
                results.append(r)  # @line L8
                yield
            if blocker is None and not (cancel_first and attempt == 1):
                for k in held:  # @line L9
                    del self.locks[k]
                self.committed.append((pid, list(calls), results))
                yield
                return results
            for c in reversed(undo):  # @line L10
                apply(self.items, c)  # @line L11
                yield
            for k in held:  # @line L12
                del self.locks[k]
            yield
            if blocker is not None:
                b = blocker
                yield lambda: self.locks.get(b) is None
        raise RuntimeError("too many attempts")


def serializable(initial: frozenset, final: set[int],
                 committed: list[tuple[int, list[Call], list[bool]]]) -> bool:
    """Brute force: is there a serial order of the committed transactions
    that gives every recorded result and the final set?"""
    for order in permutations(committed):
        items = set(initial)
        ok = True
        for _, calls, results in order:
            for call, r in zip(calls, results):
                if apply(items, call) != r:
                    ok = False
                    break
            if not ok:
                break
        if ok and items == final:
            return True
    return False
