# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sat-based-atpg/. The authors are listed in prov/PFQN6B.jsonl.
"""SAT-based ATPG (Larrabee 1992) for one single stuck-at fault.

The good circuit and the faulty copy of the fault cone are written as one CNF
formula with the Tseitin transformation. Extra clauses say that the fault site
has the stuck value in the faulty copy, the other value in the good circuit,
and that some primary output differs. The formula is satisfiable if and only
if the fault is detectable, and the primary input values of a model are a test.

Optional active clauses (Larrabee) add a variable A_l for each line of the
cone. A_l means that the line is on a path of differences to an output. These
clauses do not change satisfiability but give the solver more implications.

A small DPLL solver with two watched literals and chronological backtracking
is included so that the module needs only the standard library.
"""

from __future__ import annotations

from typing import Optional, Sequence

from gatenet import Circuit, Fault

Clause = list[int]


def gate_clauses(op: str, z: int, ins: Sequence[int], new_var) -> list[Clause]:
    """Tseitin clauses for the literal z = op(ins). new_var() returns a fresh variable."""
    if op in ("NAND", "NOR", "NOT", "XNOR"):
        op, z = {"NAND": "AND", "NOR": "OR", "NOT": "BUF", "XNOR": "XOR"}[op], -z
    if op == "BUF":
        a = ins[0]
        return [[-z, a], [z, -a]]
    if op == "AND":
        return [[-z, a] for a in ins] + [[z] + [-a for a in ins]]
    if op == "OR":
        return [[z, -a] for a in ins] + [[-z] + list(ins)]
    if op == "XOR":
        out: list[Clause] = []
        acc = ins[0]
        for k, b in enumerate(ins[1:], start=1):
            t = z if k == len(ins) - 1 else new_var()
            out += [[-t, acc, b], [-t, -acc, -b], [t, -acc, b], [t, acc, -b]]
            acc = t
        return out
    raise ValueError(f"unknown gate type {op}")


def encode(c: Circuit, fault: Fault, active: bool = False) -> tuple[int, list[Clause], list[int]]:
    """The CNF of the fault. Returns (number of variables, clauses, variables G of the inputs)."""
    site, s = fault
    n = 0

    def new_var() -> int:
        nonlocal n
        n += 1
        return n

    clauses: list[Clause] = []
    good = [new_var() for _ in range(c.n_lines)]  # @line L1
    for k in range(c.n_lines):
        if c.kind[k] != "pi":
            clauses += gate_clauses(c.op[k], good[k], [good[j] for j in c.fanin[k]], new_var)
    cone = c.cone(site)  # @line L2
    bad = good[:]
    for k in sorted(cone):  # @line L3
        bad[k] = new_var()
    for k in sorted(cone):
        if k != site:
            clauses += gate_clauses(c.op[k], bad[k], [bad[j] for j in c.fanin[k]], new_var)
    clauses.append([bad[site] if s else -bad[site]])  # @line L4
    clauses.append([-good[site] if s else good[site]])
    diff = []
    for o in c.po:  # @line L5
        if o in cone:
            d = new_var()
            g, b = good[o], bad[o]
            clauses += [[-d, g, b], [-d, -g, -b], [d, -g, b], [d, g, -b]]
            diff.append(d)
    clauses.append(diff)  # @line L6: an empty clause if no output is in the cone
    if active:  # @line L7
        po = set(c.po)
        act = {k: new_var() for k in cone}
        clauses.append([act[site]])
        for k in cone:
            a = act[k]
            clauses += [[-a, good[k], bad[k]], [-a, -good[k], -bad[k]]]
            if k not in po:
                clauses.append([-a] + [act[w] for w in c.fanout[k]])
    return n, clauses, [good[p] for p in c.pi]


class Solver:
    """DPLL with two watched literals, unit propagation and chronological backtracking."""

    def __init__(self, n_vars: int, clauses: Sequence[Clause], order: Optional[Sequence[int]] = None) -> None:
        self.n = n_vars
        self.value = [0] * (n_vars + 1)  # 0 unassigned, 1 true, -1 false
        self.trail: list[int] = []
        self.qhead = 0
        self.levels: list[int] = []  # trail position of each decision
        self.flipped: list[bool] = []
        self.watches: dict[int, list[int]] = {}
        self.clauses: list[Clause] = []
        self.units: list[int] = []
        self.empty = False
        self.decisions = self.conflicts = 0
        for cl in clauses:
            cl = list(dict.fromkeys(cl))
            if any(-a in cl for a in cl):
                continue  # always true
            if not cl:
                self.empty = True
            elif len(cl) == 1:
                self.units.append(cl[0])
            else:
                ci = len(self.clauses)
                self.clauses.append(cl)
                self.watches.setdefault(cl[0], []).append(ci)
                self.watches.setdefault(cl[1], []).append(ci)
        first = list(order or [])
        seen = set(first)
        self.order = first + [v for v in range(1, n_vars + 1) if v not in seen]

    def val(self, lit: int) -> int:
        v = self.value[abs(lit)]
        return v if lit > 0 else -v

    def assign(self, lit: int) -> None:
        self.value[abs(lit)] = 1 if lit > 0 else -1
        self.trail.append(lit)

    def propagate(self) -> bool:
        """Unit propagation over the watched literals. False on a conflict."""
        while self.qhead < len(self.trail):
            false_lit = -self.trail[self.qhead]
            self.qhead += 1
            ws = self.watches.get(false_lit, [])
            keep: list[int] = []
            conflict = False
            for ci in ws:
                if conflict:
                    keep.append(ci)
                    continue
                cl = self.clauses[ci]
                if cl[0] == false_lit:
                    cl[0], cl[1] = cl[1], cl[0]
                if self.val(cl[0]) == 1:
                    keep.append(ci)
                    continue
                for k in range(2, len(cl)):
                    if self.val(cl[k]) != -1:
                        cl[1], cl[k] = cl[k], cl[1]
                        self.watches.setdefault(cl[1], []).append(ci)
                        break
                else:
                    keep.append(ci)
                    if self.val(cl[0]) == -1:
                        conflict = True
                    else:
                        self.assign(cl[0])
            self.watches[false_lit] = keep
            if conflict:
                return False
        return True

    def undo_to(self, pos: int) -> None:
        while len(self.trail) > pos:
            self.value[abs(self.trail.pop())] = 0
        self.qhead = min(self.qhead, pos)

    def solve(self) -> Optional[list[int]]:
        """A model as a list of values (index = variable), or None if unsatisfiable."""
        if self.empty:
            return None
        for lit in self.units:
            if self.val(lit) == -1:
                return None
            if self.val(lit) == 0:
                self.assign(lit)
        ok = self.propagate()
        while True:
            if ok:
                var = next((v for v in self.order if self.value[v] == 0), None)
                if var is None:
                    return [0] + [1 if self.value[v] == 1 else 0 for v in range(1, self.n + 1)]
                self.decisions += 1
                self.levels.append(len(self.trail))
                self.flipped.append(False)
                self.assign(-var)  # try the value 0 first
            else:
                self.conflicts += 1
                while self.flipped and self.flipped[-1]:
                    self.undo_to(self.levels.pop())
                    self.flipped.pop()
                if not self.levels:
                    return None
                lit = self.trail[self.levels[-1]]
                self.undo_to(self.levels[-1])
                self.flipped[-1] = True
                self.assign(-lit)
            ok = self.propagate()


def sat_based_atpg(
    c: Circuit, fault: Fault, active: bool = False, stats: Optional[dict[str, int]] = None
) -> Optional[tuple[int, ...]]:
    """Return a test vector for the fault, or None if the fault is undetectable."""
    n, clauses, inputs = encode(c, fault, active)
    solver = Solver(n, clauses, order=inputs)
    model = solver.solve()  # @line L8
    if stats is not None:
        stats.update(variables=n, clauses=len(clauses), decisions=solver.decisions, conflicts=solver.conflicts)
    if model is None:  # @line L9
        return None
    return tuple(model[v] for v in inputs)  # @line L10
