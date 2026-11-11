# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-atomicity/. The authors are listed in prov/NZDH5H.jsonl.
"""Weak atomicity anomalies, and how strong atomicity removes them.

Each program has process 0, which runs one transaction, and process 1,
which makes one access outside any transaction. With strong=False the
access touches memory directly (weak atomicity). With strong=True it runs
as a transaction of one access: it waits while the block is locked, and a
write gives the block a new version, so the transaction can detect it.

The programs follow the anomaly names of Shpeisman et al. (PLDI 2007):
- NR, non-repeatable read: the transaction reads X twice; process 1
  writes X = 1. Anomaly: the committed transaction saw two values.
- ILU, intermediate lost update: the transaction runs X = X + 1; process 1
  writes X = 10. Serial outcomes are 10 and 11. Anomaly: any other value.
- GLU, granular lost update: words 0 and 1 share one block (a cache line
  or an object). The transaction writes word 0 = 1; process 1 writes
  word 1 = 5. Anomaly: word 1 is not 5 at the end.
- IDR, intermediate dirty read: the transaction writes X = 1 and then
  X = 2; process 1 reads X. Anomaly: process 1 reads 1.

Precondition: the stm class is one of the classes of stm.py.
Cost: one run takes O(1) steps for each process, plus retries.
"""

from __future__ import annotations

from typing import Any, Callable

from stm import Memory

X = 0
Make = Callable[[], tuple[Any, list]]


def nr(stm_cls: type, strong: bool) -> Make:
    """Non-repeatable read."""

    def make() -> tuple[Any, list]:
        mem = Memory(1)
        stm = stm_cls(mem, strong=strong)

        def body(tx):
            a = yield from tx.read(X)
            b = yield from tx.read(X)
            return (a, b)

        def p0():
            return (yield from stm.atomic(0, body))

        def p1():
            yield from stm.nt_write(X, 1)

        return mem, [p0(), p1()]

    return make


def ilu(stm_cls: type, strong: bool) -> Make:
    """Intermediate lost update."""

    def make() -> tuple[Any, list]:
        mem = Memory(1)
        stm = stm_cls(mem, strong=strong)

        def body(tx):
            a = yield from tx.read(X)
            yield from tx.write(X, a + 1)

        def p0():
            yield from stm.atomic(0, body)

        def p1():
            yield from stm.nt_write(X, 10)

        return mem, [p0(), p1()]

    return make


def glu(stm_cls: type, strong: bool) -> Make:
    """Granular lost update: two words in one block."""

    def make() -> tuple[Any, list]:
        mem = Memory(2, block=2)
        stm = stm_cls(mem, strong=strong)

        def body(tx):
            yield from tx.write(0, 1)

        def p0():
            yield from stm.atomic(0, body)

        def p1():
            yield from stm.nt_write(1, 5)

        return mem, [p0(), p1()]

    return make


def idr(stm_cls: type, strong: bool) -> Make:
    """Intermediate dirty read."""

    def make() -> tuple[Any, list]:
        mem = Memory(1)
        stm = stm_cls(mem, strong=strong)

        def body(tx):
            yield from tx.write(X, 1)
            yield from tx.write(X, 2)

        def p0():
            yield from stm.atomic(0, body)

        def p1():
            return (yield from stm.nt_read(X))

        return mem, [p0(), p1()]

    return make


def anomaly(name: str, mem: Any, result: list) -> bool:
    """Return True if the final state of a run of program `name` is not serial."""
    if name == "NR":
        a, b = result[0]
        return a != b
    if name == "ILU":
        return mem.val[X] not in (10, 11)
    if name == "GLU":
        return mem.val[1] != 5 or mem.val[0] != 1
    if name == "IDR":
        return result[1] == 1
    raise ValueError(name)


PROGRAMS = {"NR": nr, "ILU": ilu, "GLU": glu, "IDR": idr}
