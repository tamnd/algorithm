# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/march-test/. The authors are listed in prov/G5W6E7.jsonl.
"""March tests for bit-oriented random access memories.

A march test is a list of march elements. Each element has an address order
(up, down or any) and a short list of operations, each a write w0 or w1 or a
read r0 or r1 that expects the given value. The element applies all its
operations to one address before it moves to the next. A test with operations
per address m_1, ..., m_e on N cells performs N (m_1 + ... + m_e) operations
and runs in that much time with O(1) extra space.

The memory is any object with read(address) and write(address, value).
"""

from __future__ import annotations

import re
from typing import Optional, Protocol, Sequence

UP, DOWN, ANY = "up", "down", "any"
Op = tuple[str, int]
Element = tuple[str, tuple[Op, ...]]
Failure = tuple[int, int, int, int]


class Memory(Protocol):
    def read(self, address: int) -> int: ...

    def write(self, address: int, value: int) -> None: ...


def parse(text: str) -> list[Element]:
    """Parse a test such as "any(w0); up(r0,w1); down(r1,w0)"."""
    test: list[Element] = []
    for part in text.split(";"):
        m = re.fullmatch(r"\s*(up|down|any)\s*\(([^)]*)\)\s*", part)
        if not m:
            raise ValueError(f"bad march element {part!r}")
        ops = []
        for tok in m.group(2).split(","):
            tok = tok.strip()
            if not re.fullmatch(r"[rw][01]", tok):
                raise ValueError(f"bad operation {tok!r}")
            ops.append((tok[0], int(tok[1])))
        test.append((m.group(1), tuple(ops)))
    return test


def show(test: Sequence[Element]) -> str:
    return "; ".join(f"{order}({','.join(f'{k}{v}' for k, v in ops)})" for order, ops in test)


MATS = parse("any(w0); any(r0,w1); any(r1)")
MATS_PLUS = parse("any(w0); up(r0,w1); down(r1,w0)")
MATS_PLUS_PLUS = parse("any(w0); up(r0,w1); down(r1,w0,r0)")
MARCH_C_MINUS = parse("any(w0); up(r0,w1); up(r1,w0); down(r0,w1); down(r1,w0); any(r0)")


def operation_count(test: Sequence[Element], n: int) -> int:
    """The number of read and write operations of the test on n cells."""
    return n * sum(len(ops) for _, ops in test)


def addresses(order: str, n: int) -> range:
    """The address order of an element. "any" is run upward here."""
    return range(n - 1, -1, -1) if order == DOWN else range(n)


def consistent(test: Sequence[Element]) -> bool:
    """True if every read expects the value a fault-free memory holds at that point.

    All cells get the same operations in each element, so one value per element
    boundary describes the whole memory. A read before any write is not allowed.
    """
    value: Optional[int] = None
    for _, ops in test:
        for kind, v in ops:
            if kind == "w":
                value = v
            elif value != v:
                return False
    return True


def run_march(memory: Memory, test: Sequence[Element], n: int) -> Optional[Failure]:
    """Apply the test to a memory of n cells.

    Returns None if every read gave the expected value, else the first failure as
    (element index, address, operation index, value read).
    """
    for e, (order, ops) in enumerate(test):  # @line L1
        for a in addresses(order, n):  # @line L2
            for t, (kind, v) in enumerate(ops):  # @line L3
                if kind == "w":  # @line L4
                    memory.write(a, v)
                else:
                    got = memory.read(a)  # @line L5
                    if got != v:
                        return (e, a, t, got)  # @line L6
    return None  # @line L7


class GoodMemory:
    """A fault-free memory of n one-bit cells."""

    def __init__(self, n: int, init: Sequence[int] | None = None) -> None:
        self.cells = list(init) if init is not None else [0] * n

    def read(self, address: int) -> int:
        return self.cells[address]

    def write(self, address: int, value: int) -> None:
        self.cells[address] = value
