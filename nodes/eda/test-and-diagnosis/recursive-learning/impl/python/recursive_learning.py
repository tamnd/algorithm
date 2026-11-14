# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-learning/. The authors are listed in prov/HZB5S0.jsonl.
"""Recursive learning (Kunz and Pradhan) on a gate-level circuit.

A situation is a partial assignment of 0 and 1 to the lines of a circuit (the
other lines are X). Direct implications follow one gate at a time, forward and
backward. A gate is unjustified when its output has a value that its input
values do not yet force. Recursive learning tries every justification of each
unjustified gate, makes all implications of each case up to a depth r_max, and
keeps the values common to all the cases that do not end in a conflict.

The values are lists indexed by line, with X = 2. The time is exponential in
r_max in the worst case: each level multiplies the work by the number of
justifications of each unjustified gate.
"""

from __future__ import annotations

from typing import Optional, Sequence

from td2net import X, Circuit, controlling, eval_gate, inversion

Values = list[int]


def _set(vals: Values, k: int, v: int, changed: list[int]) -> bool:
    if vals[k] == X:
        vals[k] = v
        changed.append(k)
        return True
    return vals[k] == v


def direct_implications(c: Circuit, vals: Values) -> Optional[Values]:
    """All direct implications of a situation, or None on a conflict."""
    vals = list(vals)
    changed = [0]
    while changed:
        changed = []
        for k in range(c.n_lines):
            if c.kind[k] == "pi":
                continue
            ins = c.fanin[k]
            op = c.op[k]
            e = eval_gate(op, [vals[j] for j in ins])
            if e != X and not _set(vals, k, e, changed):  # forward
                return None
            v = vals[k]
            if v == X:
                continue
            if op in ("BUF", "NOT"):  # also fanout branches
                if not _set(vals, ins[0], v ^ inversion(op), changed):
                    return None
                continue
            open_ins = [j for j in ins if vals[j] == X]
            cv = controlling(op)
            if cv is None:  # XOR, XNOR
                if len(open_ins) == 1:
                    parity = v ^ inversion(op)
                    for j in ins:
                        if j != open_ins[0]:
                            parity ^= vals[j]
                    if not _set(vals, open_ins[0], parity, changed):
                        return None
                continue
            core = v ^ inversion(op)
            if core == 1 - cv:  # every input is non-controlling
                for j in open_ins:
                    if not _set(vals, j, 1 - cv, changed):
                        return None
            elif len(open_ins) == 1 and all(vals[j] == 1 - cv for j in ins if j != open_ins[0]):
                if not _set(vals, open_ins[0], cv, changed):
                    return None
    return vals


def unjustified_gates(c: Circuit, vals: Values) -> list[int]:
    """Gates whose output value is not forced by the values of their inputs."""
    return [
        k
        for k in range(c.n_lines)
        if c.kind[k] == "gate" and vals[k] != X and eval_gate(c.op[k], [vals[j] for j in c.fanin[k]]) == X
    ]


def justifications(c: Circuit, vals: Values, g: int) -> list[tuple[int, int]]:
    """A complete set of justifications: every consistent extension satisfies one."""
    op = c.op[g]
    open_ins = [j for j in c.fanin[g] if vals[j] == X]
    cv = controlling(op)
    if cv is None:
        return [(open_ins[0], 0), (open_ins[0], 1)]
    return [(j, cv) for j in open_ins]


def make_all_implications(c: Circuit, vals: Values, r: int, r_max: int) -> Optional[Values]:
    """Kunz and Pradhan's make_all_implications(r, r_max). None means a conflict."""
    s = direct_implications(c, vals)  # @line L1
    if s is None:
        return None
    if r >= r_max:  # @line L2
        return s
    progress = True
    while progress:  # @line L3
        progress = False
        for g in unjustified_gates(c, s):  # @line L4
            if not (s[g] != X and eval_gate(c.op[g], [s[j] for j in c.fanin[g]]) == X):
                continue  # justified by a value learned in this pass
            common: Optional[Values] = None
            for j, v in justifications(c, s, g):  # @line L5
                t = list(s)
                t[j] = v
                sj = make_all_implications(c, t, r + 1, r_max)  # @line L6
                if sj is None:
                    continue
                if common is None:
                    common = sj
                else:  # @line L8
                    common = [a if a == b else X for a, b in zip(common, sj)]
            if common is None:  # @line L7
                return None
            learned = [k for k in range(c.n_lines) if s[k] == X and common[k] != X]
            if learned:
                t = list(s)
                for k in learned:
                    t[k] = common[k]
                s = direct_implications(c, t)  # @line L9
                if s is None:
                    return None
                progress = True  # @line L10
    return s  # @line L11


def from_assignment(c: Circuit, assignment: dict[int, int]) -> Values:
    vals = [X] * c.n_lines
    for k, v in assignment.items():
        vals[k] = v
    return vals


def learn(c: Circuit, assignment: dict[int, int], r_max: int) -> Optional[dict[int, int]]:
    """The values that recursive learning to depth r_max finds for a situation, or None."""
    s = make_all_implications(c, from_assignment(c, assignment), 0, r_max)
    if s is None:
        return None
    return {k: s[k] for k in range(c.n_lines) if s[k] != X}


def necessary_assignments(c: Circuit, assignment: dict[int, int], r_max: Optional[int] = None) -> Optional[dict[int, int]]:
    """Every necessary assignment, by one conflict test per line and value.

    (k, v) is necessary when the situation with k set to the other value has a
    conflict. With r_max at least the number of lines, the test is exact.
    """
    if r_max is None:
        r_max = c.n_lines
    base = make_all_implications(c, from_assignment(c, assignment), 0, r_max)
    if base is None:
        return None
    out = {}
    for k in range(c.n_lines):
        if base[k] != X:
            out[k] = base[k]
            continue
        for v in (0, 1):
            trial = dict(assignment)
            trial[k] = 1 - v
            if make_all_implications(c, from_assignment(c, trial), 0, r_max) is None:
                out[k] = v
    return out


def consistent_vectors(c: Circuit, assignment: dict[int, int]) -> list[Sequence[int]]:
    """Brute force: the input vectors whose simulation agrees with the situation."""
    out = []
    for vec in c.all_vectors():
        vals = c.simulate(vec)
        if all(vals[k] == v for k, v in assignment.items()):
            out.append(vec)
    return out
