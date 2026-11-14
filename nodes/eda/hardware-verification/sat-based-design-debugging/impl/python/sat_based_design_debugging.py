# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sat-based-design-debugging/. The authors are listed in prov/1D5R8Y.jsonl.
"""SAT-based design debugging with correction multiplexers.

A circuit is a list of gates in topological order. Each gate is
(name, op, fanins), with op in AND, OR, XOR, NAND, NOR, XNOR, NOT, BUF, and the
fanins are names of inputs or of earlier gates. A test is (inputs, expected),
two dicts from names to 0 or 1.

debug() returns every set of at most k_max suspect gates, of the least size
that works, such that new values at those gates make every test give its
expected outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from dpll import Solver

Gate = tuple[str, str, tuple[str, ...]]
Test = tuple[dict[str, int], dict[str, int]]

OPS = {
    "AND": lambda xs: int(all(xs)),
    "OR": lambda xs: int(any(xs)),
    "XOR": lambda xs: sum(xs) & 1,
    "NAND": lambda xs: 1 - int(all(xs)),
    "NOR": lambda xs: 1 - int(any(xs)),
    "XNOR": lambda xs: 1 - (sum(xs) & 1),
    "NOT": lambda xs: 1 - xs[0],
    "BUF": lambda xs: xs[0],
}


@dataclass
class Circuit:
    inputs: list[str]
    gates: list[Gate]
    outputs: list[str]


def simulate(c: Circuit, inputs: dict[str, int], override: Optional[dict[str, int]] = None) -> dict[str, int]:
    """Values of all signals; override replaces the values of some gates."""
    v = dict(inputs)
    for name, op, fanins in c.gates:
        if override and name in override:
            v[name] = override[name]
        else:
            v[name] = OPS[op]([v[f] for f in fanins])
    return v


def gate_clauses(s: Solver, op: str, out: int, ins: list[int]) -> None:
    """Tseitin clauses of out = op(ins)."""
    if op in ("NOT", "BUF"):
        a = ins[0] if op == "BUF" else -ins[0]
        s.add_clause([-out, a])
        s.add_clause([out, -a])
        return
    if op in ("XOR", "XNOR"):
        acc = ins[0]
        for x in ins[1:]:
            t = s.new_var()
            for a, b, r in ((1, 1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1)):
                s.add_clause([-a * acc, -b * x, r * t])
            acc = t
        sign = 1 if op == "XOR" else -1
        s.add_clause([-out, sign * acc])
        s.add_clause([out, -sign * acc])
        return
    neg = op in ("NAND", "NOR")
    o = -out if neg else out
    if op in ("AND", "NAND"):
        for x in ins:
            s.add_clause([-o, x])
        s.add_clause([o] + [-x for x in ins])
    else:
        for x in ins:
            s.add_clause([o, -x])
        s.add_clause([-o] + list(ins))


def at_most(s: Solver, xs: list[int], k: int) -> None:
    """Sinz's sequential counter for sum(xs) <= k."""
    n = len(xs)
    if k >= n:
        return
    if k == 0:
        for x in xs:
            s.add_clause([-x])
        return
    r = [[s.new_var() for _ in range(k)] for _ in range(n - 1)]
    s.add_clause([-xs[0], r[0][0]])
    for j in range(1, k):
        s.add_clause([-r[0][j]])
    for i in range(1, n - 1):
        s.add_clause([-xs[i], r[i][0]])
        s.add_clause([-r[i - 1][0], r[i][0]])
        for j in range(1, k):
            s.add_clause([-xs[i], -r[i - 1][j - 1], r[i][j]])
            s.add_clause([-r[i - 1][j], r[i][j]])
        s.add_clause([-xs[i], -r[i - 1][k - 1]])
    s.add_clause([-xs[n - 1], -r[n - 2][k - 1]])


def debug_instance(c: Circuit, tests: Sequence[Test], suspects: Sequence[str]):
    """The CNF of lines L1 to L3. Returns the solver, the select variables, and
    for each test the map from signal names to variables."""
    s = Solver()
    select = {g: s.new_var() for g in suspects}
    s.order = list(select.values())
    copies = []
    for inputs, expected in tests:                                      # @line L1
        var = {x: s.new_var() for x in c.inputs}
        for x in c.inputs:
            s.add_clause([var[x] if inputs[x] else -var[x]])
        for name, op, fanins in c.gates:
            out = s.new_var()
            if name in select:                                          # @line L2
                orig, w, sel = s.new_var(), s.new_var(), select[name]
                gate_clauses(s, op, orig, [var[f] for f in fanins])
                s.add_clause([-sel, -w, out])
                s.add_clause([-sel, w, -out])
                s.add_clause([sel, -orig, out])
                s.add_clause([sel, orig, -out])
            else:
                gate_clauses(s, op, out, [var[f] for f in fanins])     # @line L3
            var[name] = out
        for y in c.outputs:
            s.add_clause([var[y] if expected[y] else -var[y]])
        copies.append(var)
    return s, select, copies


def debug(c: Circuit, tests: Sequence[Test], k_max: int,
          suspects: Optional[Sequence[str]] = None) -> tuple[int, list[frozenset[str]]]:
    """(k, all correction sets of size k) for the least k <= k_max that has one,
    or (-1, []) if there is none."""
    suspects = list(suspects) if suspects is not None else [g[0] for g in c.gates]
    base, select, _ = debug_instance(c, tests, suspects)
    for k in range(k_max + 1):                                          # @line L4
        s = Solver()
        s.nvars, s.clauses, s.units, s.order = base.nvars, [list(x) for x in base.clauses], list(base.units), base.order
        at_most(s, list(select.values()), k)                            # @line L5
        found = []
        while (model := s.solve()) is not None:                         # @line L6
            sol = frozenset(g for g, v in select.items() if model[v])   # @line L7
            found.append(sol)
            s.add_clause([-select[g] for g in sol])                     # @line L8
        if found:                                                       # @line L9
            return k, found
    return -1, []                                                       # @line L10


def correction_values(c: Circuit, tests: Sequence[Test], fix: frozenset[str]) -> Optional[list[dict[str, int]]]:
    """Values at the gates of fix, one dict per test, that make all tests pass."""
    s, select, copies = debug_instance(c, tests, sorted(fix))
    model = s.solve([select[g] for g in fix])
    if model is None:
        return None
    return [{g: int(model[var[g]]) for g in fix} for var in copies]
