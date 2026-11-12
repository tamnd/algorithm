# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gang-scheduling/. The authors are listed in prov/YGJAGZ.jsonl.

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Gang:
    """A parallel job of `size` threads that needs `work` slots, in which
    all of its threads run together."""

    name: str
    arrival: int
    size: int
    work: int


class Matrix:
    """The Ousterhout matrix: one row per time slot, one column per
    processor. Cell (r, p) holds (gang, thread) or None."""

    def __init__(self, processors: int) -> None:
        if processors < 1:
            raise ValueError("need at least one processor")
        self.p = processors
        self.rows: list[list[Optional[tuple[str, int]]]] = []
        self.where: dict[str, tuple[int, list[int]]] = {}  # gang -> (row, columns)

    def place(self, g: Gang) -> int:
        """First fit: the first row with size free columns, else a new row.
        The threads take the lowest free columns. Return the row."""
        if not 1 <= g.size <= self.p:
            raise ValueError(f"gang {g.name} does not fit on {self.p} processors")
        for r, row in enumerate(self.rows):
            free = [c for c in range(self.p) if row[c] is None]
            if len(free) >= g.size:
                break
        else:
            self.rows.append([None] * self.p)
            r, free = len(self.rows) - 1, list(range(self.p))
        cols = free[: g.size]
        for i, c in enumerate(cols):
            self.rows[r][c] = (g.name, i)
        self.where[g.name] = (r, cols)
        return r

    def remove(self, name: str) -> None:
        """Remove a gang, and drop its row if the row becomes empty."""
        r, cols = self.where.pop(name)
        for c in cols:
            self.rows[r][c] = None
        if all(x is None for x in self.rows[r]):
            del self.rows[r]
            self.where = {g: (rr - (rr > r), cs) for g, (rr, cs) in self.where.items()}

    def gangs_in_row(self, r: int) -> list[str]:
        seen: list[str] = []
        for x in self.rows[r]:
            if x is not None and x[0] not in seen:
                seen.append(x[0])
        return seen


@dataclass
class Trace:
    slots: list = field(default_factory=list)  # per slot: list of P cells (gang, thread) or None
    done: dict = field(default_factory=dict)


def gang_schedule(processors: int, gangs: list[Gang], alternate: bool = False) -> Trace:
    """Gang scheduling with an Ousterhout matrix. Slot t runs one row, and
    the rows take turns. With alternate=True, the idle processors of the
    row also run whole gangs from other rows whose columns are all idle."""
    left = {g.name: g.work for g in gangs}
    arrivals = sorted(gangs, key=lambda g: (g.arrival, g.name))
    m = Matrix(processors)
    tr = Trace()
    nxt, r, t = 0, 0, 0  # @line L1
    while len(tr.done) < len(gangs):  # @line L2
        while nxt < len(arrivals) and arrivals[nxt].arrival <= t:  # @line L3
            m.place(arrivals[nxt])
            nxt += 1
        if not m.rows:  # @line L4
            tr.slots.append([None] * processors)
            t += 1
            continue
        r %= len(m.rows)  # @line L5
        cells = list(m.rows[r])  # @line L6
        ran = m.gangs_in_row(r)
        if alternate:  # @line L7
            for rr in range(len(m.rows)):
                if rr == r:
                    continue
                for g in m.gangs_in_row(rr):
                    cols = m.where[g][1]
                    if all(cells[c] is None for c in cols):
                        for c in cols:
                            cells[c] = m.rows[rr][c]
                        ran.append(g)
        tr.slots.append(cells)
        t += 1
        before = list(m.rows)
        for g in ran:  # @line L8
            left[g] -= 1
            if left[g] == 0:
                m.remove(g)
                tr.done[g] = t
        # the next turn goes to the first surviving row after row r
        alive = [any(x is row for x in m.rows) for row in before]
        r = sum(alive[: r + 1])  # @line L9
    return tr
