# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sat-based-design-debugging/. The authors are listed in prov/1D5R8Y.jsonl.
"""A small DPLL solver with two watched literals and chronological backtracking.

Literals are nonzero integers, -v is the negation of v. Clauses can be added
between calls of solve, which is enough for enumeration with blocking clauses.
"""

from __future__ import annotations

from typing import Iterable, Optional, Sequence


class Solver:
    def __init__(self) -> None:
        self.nvars = 0
        self.clauses: list[list[int]] = []
        self.units: list[int] = []
        self.empty = False
        self.order: list[int] = []          # decision order; others follow by index

    def new_var(self) -> int:
        self.nvars += 1
        return self.nvars

    def add_clause(self, lits: Iterable[int]) -> None:
        c = list(dict.fromkeys(lits))
        if any(-l in c for l in c):
            return                          # a tautology
        if not c:
            self.empty = True
        elif len(c) == 1:
            self.units.append(c[0])
        else:
            self.clauses.append(c)

    def solve(self, assumptions: Sequence[int] = ()) -> Optional[dict[int, bool]]:
        if self.empty:
            return None
        n = self.nvars
        val: list[Optional[bool]] = [None] * (n + 1)
        watches: dict[int, list[int]] = {}
        for ci, c in enumerate(self.clauses):
            watches.setdefault(c[0], []).append(ci)
            watches.setdefault(c[1], []).append(ci)
        trail: list[int] = []

        def value(lit: int) -> Optional[bool]:
            v = val[abs(lit)]
            return None if v is None else (v if lit > 0 else not v)

        def enqueue(lit: int) -> bool:
            v = value(lit)
            if v is not None:
                return v
            val[abs(lit)] = lit > 0
            trail.append(lit)
            return True

        def propagate(qhead: int) -> bool:
            """Unit propagation from trail[qhead:]; False on a conflict."""
            while qhead < len(trail):
                false_lit = -trail[qhead]
                qhead += 1
                ws = watches.get(false_lit, [])
                keep: list[int] = []
                ok = True
                for i, ci in enumerate(ws):
                    if not ok:
                        keep.append(ci)
                        continue
                    c = self.clauses[ci]
                    if c[0] == false_lit:
                        c[0], c[1] = c[1], c[0]
                    if value(c[0]) is True:
                        keep.append(ci)
                        continue
                    for k in range(2, len(c)):
                        if value(c[k]) is not False:
                            c[1], c[k] = c[k], c[1]
                            watches.setdefault(c[1], []).append(ci)
                            break
                    else:
                        keep.append(ci)
                        if not enqueue(c[0]):
                            ok = False
                watches[false_lit] = keep
                if not ok:
                    return False
            return True

        for lit in list(self.units) + list(assumptions):
            if not enqueue(lit):
                return None
        if not propagate(0):
            return None
        root = len(trail)
        order = list(dict.fromkeys(self.order + list(range(1, n + 1))))
        decisions: list[tuple[int, int, bool]] = []    # (trail length, literal, flipped)
        qhead = root
        while True:
            if propagate(qhead):
                qhead = len(trail)
                var = next((v for v in order if val[v] is None), None)
                if var is None:
                    return {v: bool(val[v]) for v in range(1, n + 1)}
                decisions.append((len(trail), -var, False))
                enqueue(-var)
                continue
            while decisions and decisions[-1][2]:
                start, _, _ = decisions.pop()
                for lit in trail[start:]:
                    val[abs(lit)] = None
                del trail[start:]
            if not decisions:
                return None
            start, lit, _ = decisions.pop()
            for l in trail[start:]:
                val[abs(l)] = None
            del trail[start:]
            decisions.append((start, -lit, True))
            enqueue(-lit)
            qhead = start
