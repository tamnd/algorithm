# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backbone/. The authors are listed in prov/3CT6YF.jsonl.

"""The backbone of a CNF formula: the literals true in every model.

backbone() uses the iterative algorithm with model filtering: each SAT
call either proves a candidate literal (UNSAT) or returns a model that
removes every candidate it falsifies. It makes at most n + 1 SAT calls.
The SAT oracle is a small DPLL. Clauses are lists of DIMACS ints.
"""


class Oracle:
    """A plain DPLL that counts its calls."""

    def __init__(self, clauses: list[list[int]]) -> None:
        self.clauses = [list(c) for c in clauses]
        self.calls = 0

    def solve(self, units: list[int]) -> dict[int, bool] | None:
        self.calls += 1
        return self._dpll(self.clauses + [[u] for u in units], {})

    def _dpll(self, clauses: list[list[int]], assign: dict[int, bool]) -> dict[int, bool] | None:
        a = dict(assign)
        while True:
            unit = None
            for c in clauses:
                if any(a.get(abs(x)) == (x > 0) for x in c):
                    continue
                free = [x for x in c if abs(x) not in a]
                if not free:
                    return None
                if len(free) == 1:
                    unit = free[0]
                    break
            if unit is None:
                break
            a[abs(unit)] = unit > 0
        for c in clauses:
            if not any(a.get(abs(x)) == (x > 0) for x in c):
                x = next(x for x in c if abs(x) not in a)
                for value in (x > 0, x < 0):
                    r = self._dpll(clauses, {**a, abs(x): value})
                    if r is not None:
                        return r
                return None
        return a


def backbone(clauses: list[list[int]], n: int) -> tuple[set[int] | None, int]:
    """Return (backbone literals, number of SAT calls); None if F is UNSAT."""
    oracle = Oracle(clauses)
    mu = oracle.solve([])  # @line L1
    if mu is None:
        return None, oracle.calls
    cand = [v if mu.get(v, False) else -v for v in range(1, n + 1)]  # @line L2
    bb: set[int] = set()
    while cand:  # @line L3
        lit = cand.pop()  # @line L4
        model = oracle.solve(sorted(bb) + [-lit])  # @line L5
        if model is not None:
            cand = [c for c in cand if model.get(abs(c), False) == (c > 0)]  # @line L6
        else:
            bb.add(lit)  # @line L7
    return bb, oracle.calls  # @line L8
