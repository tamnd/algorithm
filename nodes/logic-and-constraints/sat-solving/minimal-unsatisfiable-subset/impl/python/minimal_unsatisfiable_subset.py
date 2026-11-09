# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimal-unsatisfiable-subset/. The authors are listed in prov/V0RSZE.jsonl.

"""Minimal unsatisfiable subsets with a SAT oracle.

Clauses are lists of DIMACS ints. hard is a list of clauses that every
subset keeps; it must be satisfiable. The functions return the indices of
the chosen clauses of soft, in increasing order. The Oracle counts its calls,
so the bounds of the page can be checked.
"""


class Oracle:
    """A small DPLL solver that counts how often it is called."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, clauses: list[list[int]]) -> dict[int, bool] | None:
        self.calls += 1
        return _dpll([list(c) for c in clauses], {})


def _dpll(clauses: list[list[int]], assign: dict[int, bool]) -> dict[int, bool] | None:
    while True:
        unit = None
        rest: list[list[int]] = []
        for c in clauses:
            if any(assign.get(abs(a)) == (a > 0) for a in c):
                continue
            free = [a for a in c if abs(a) not in assign]
            if not free:
                return None
            if len(free) == 1:
                unit = free[0]
            rest.append(free)
        if unit is None:
            break
        assign = {**assign, abs(unit): unit > 0}
        clauses = rest
    if not rest:
        return assign
    v = abs(rest[0][0])
    for value in (rest[0][0] > 0, rest[0][0] < 0):
        model = _dpll(rest, {**assign, v: value})
        if model is not None:
            return model
    return None


def deletion_mus(soft: list[list[int]], hard: list[list[int]] = (),
                 oracle: Oracle | None = None) -> list[int] | None:
    """Deletion-based MUS. Exactly len(soft) + 1 oracle calls; None if satisfiable."""
    sat = oracle or Oracle()
    hard = list(hard)
    if sat(hard + soft) is not None:  # @line L1
        return None
    keep = set(range(len(soft)))  # @line L2
    for i in range(len(soft)):  # @line L3
        trial = keep - {i}
        if sat(hard + [soft[j] for j in sorted(trial)]) is None:  # @line L4
            keep = trial  # @line L5
    return sorted(keep)  # @line L6


def quickxplain(soft: list[list[int]], hard: list[list[int]] = (),
                oracle: Oracle | None = None) -> list[int] | None:
    """Junker's QuickXplain. At most 2 + sum over d of min(2^d, 2k) oracle calls."""
    sat = oracle or Oracle()
    hard = list(hard)
    if sat(hard + soft) is not None:
        return None
    if sat(hard) is None:
        return []  # the hard clauses alone are unsatisfiable

    def qx(background: list[int], delta: list[int], cands: list[int]) -> list[int]:
        if delta and sat(hard + [soft[j] for j in background]) is None:
            return []
        if len(cands) == 1:
            return cands
        half = len(cands) // 2
        c1, c2 = cands[:half], cands[half:]
        d2 = qx(background + c1, c1, c2)
        d1 = qx(background + d2, d2, c1)
        return d1 + d2

    return sorted(qx([], [], list(range(len(soft)))))
