# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/march-test/. The authors are listed in prov/G5W6E7.jsonl.
"""A small memory with one injected functional fault, for checking march tests.

The faults follow van de Goor's functional model (see the memory coupling
fault page). A fault is a tuple:

- ("SAF", i, v): cell i is stuck at v.
- ("TF", i, t): cell i cannot make the transition t ("up" is 0 to 1, "down" is 1 to 0).
- ("CFin", i, j, t): a transition t of the aggressor i inverts the victim j.
- ("CFid", i, j, t, v): a transition t of i sets j to v.
- ("CFst", i, j, x, v): while i holds x, j holds v.
- ("AFnone", a, v): address a reaches no cell, and a read of it returns v.
  Cell a is never accessed.
- ("AFother", a, b): address a reaches cell b instead of cell a.
- ("AFmulti", a, b, w): address a reaches cells a and b. A write goes to both,
  and a read returns their AND (w = 0) or their OR (w = 1).
"""

from __future__ import annotations

from itertools import product
from typing import Sequence

Fault = tuple


class FaultyMemory:
    """A memory of n one-bit cells with one fault."""

    def __init__(self, n: int, fault: Fault, init: Sequence[int]) -> None:
        self.n = n
        self.fault = fault
        self.cells = list(init)
        f = fault
        if f[0] == "SAF":
            self.cells[f[1]] = f[2]
        self._state_coupling()

    def _targets(self, a: int) -> list[int]:
        f = self.fault
        if f[0] == "AFnone" and a == f[1]:
            return []
        if f[0] == "AFother" and a == f[1]:
            return [f[2]]
        if f[0] == "AFmulti" and a == f[1]:
            return [a, f[2]]
        return [a]

    def _state_coupling(self) -> None:
        f = self.fault
        if f[0] == "CFst" and self.cells[f[1]] == f[3]:
            self.cells[f[2]] = f[4]

    def _write_cell(self, c: int, v: int) -> None:
        f = self.fault
        old = self.cells[c]
        new = v
        if f[0] == "SAF" and c == f[1]:
            new = f[2]
        if f[0] == "TF" and c == f[1] and old != new:
            if (f[2] == "up") == (new == 1):
                new = old
        self.cells[c] = new
        if old != new and f[0] in ("CFin", "CFid") and c == f[1]:
            t = "up" if new == 1 else "down"
            if t == f[3]:
                j = f[2]
                self.cells[j] = 1 - self.cells[j] if f[0] == "CFin" else f[4]
        self._state_coupling()

    def write(self, address: int, value: int) -> None:
        for c in self._targets(address):
            self._write_cell(c, value)

    def read(self, address: int) -> int:
        f = self.fault
        cells = self._targets(address)
        if not cells:
            return f[2]
        if len(cells) == 1:
            return self.cells[cells[0]]
        vals = [self.cells[c] for c in cells]
        return max(vals) if f[3] == 1 else min(vals)


def all_faults(n: int) -> dict[str, list[Fault]]:
    """Every fault of each class in a memory of n cells."""
    cells = range(n)
    pairs = [(i, j) for i in cells for j in cells if i != j]
    return {
        "SAF": [("SAF", i, v) for i in cells for v in (0, 1)],
        "TF": [("TF", i, t) for i in cells for t in ("up", "down")],
        "CFin": [("CFin", i, j, t) for i, j in pairs for t in ("up", "down")],
        "CFid": [("CFid", i, j, t, v) for i, j in pairs for t in ("up", "down") for v in (0, 1)],
        "CFst": [("CFst", i, j, x, v) for i, j in pairs for x in (0, 1) for v in (0, 1)],
        "AF": [("AFnone", a, v) for a in cells for v in (0, 1)]
        + [("AFother", a, b) for a, b in pairs]
        + [("AFmulti", a, b, w) for a, b in pairs for w in (0, 1)],
    }


def initial_states(n: int) -> list[tuple[int, ...]]:
    return list(product((0, 1), repeat=n))
