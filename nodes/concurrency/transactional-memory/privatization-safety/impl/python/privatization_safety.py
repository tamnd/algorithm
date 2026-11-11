# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/privatization-safety/. The authors are listed in prov/9NJC6P.jsonl.
"""The privatization idiom on three STMs, with and without a quiescence fence.

Word PRIV is a flag and word X is the data it guards. Process 0, the
privatizer, runs atomic { PRIV = 1 } and then, outside any transaction,
reads X and writes X + 1. Process 1, the worker, runs
atomic { if PRIV == 0 then X = 100 }. Process 2 (optional) is a second
worker. Serial runs give X = 1 (the worker sees the flag set) or X = 101
(the worker runs first), so ALLOWED holds the correct final values.

Precondition: the stm class is one of the classes of stm.py.
Cost: one run takes O(1) steps for each process, plus retries.
"""

from __future__ import annotations

from typing import Any, Callable

from stm import Memory

PRIV, X = 0, 1
ALLOWED = {1, 101}


def privatization(stm_cls: type, fence: bool = False, workers: int = 1) -> Callable[[], tuple[Any, list]]:
    """Return a factory for the scheduler: (memory, [privatizer, worker, ...])."""

    def make() -> tuple[Any, list]:
        mem = Memory(2)
        stm = stm_cls(mem)

        def privatize(tx):
            yield from tx.write(PRIV, 1)

        def work(tx):
            p = yield from tx.read(PRIV)
            if p == 0:
                yield from tx.write(X, 100)

        def privatizer():
            yield from stm.atomic(0, privatize)
            if fence:
                yield from stm.fence(0)
            v = yield from stm.nt_read(X)
            yield from stm.nt_write(X, v + 1)
            return v

        def worker(pid):
            yield from stm.atomic(pid, work)

        return mem, [privatizer()] + [worker(1 + i) for i in range(workers)]

    return make


def allowed(workers: int) -> set[int]:
    """Final values of X that some serial order gives."""
    return {1, 101} if workers else {1}
