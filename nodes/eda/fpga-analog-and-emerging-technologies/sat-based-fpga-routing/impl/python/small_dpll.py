# SPDX-License-Identifier: MIT
# Shared helper of the fa1 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""A small complete SAT solver: DPLL with unit propagation, for the tests and the examples.

A clause is a list of nonzero ints in DIMACS style. solve(n, clauses) returns
a list model with model[v] True or False for v = 1..n (model[0] is unused),
or None when the formula has no model.
"""


def solve(n: int, clauses):
    clauses = [list(dict.fromkeys(c)) for c in clauses]
    value: list = [None] * (n + 1)
    trail: list[int] = []

    def lit_value(lit: int):
        v = value[abs(lit)]
        return None if v is None else (v if lit > 0 else not v)

    def propagate() -> bool:
        changed = True
        while changed:
            changed = False
            for c in clauses:
                free = None
                n_free = 0
                sat = False
                for lit in c:
                    val = lit_value(lit)
                    if val is True:
                        sat = True
                        break
                    if val is None:
                        n_free += 1
                        free = lit
                if sat:
                    continue
                if n_free == 0:
                    return False
                if n_free == 1:
                    value[abs(free)] = free > 0
                    trail.append(abs(free))
                    changed = True
        return True

    def undo(mark: int) -> None:
        while len(trail) > mark:
            value[trail.pop()] = None

    def search() -> bool:
        if not propagate():
            return False
        var = next((v for v in range(1, n + 1) if value[v] is None), None)
        if var is None:
            return True
        for choice in (True, False):
            mark = len(trail)
            value[var] = choice
            trail.append(var)
            if search():
                return True
            undo(mark)
        return False

    if not search():
        return None
    return [False] + [bool(value[v]) for v in range(1, n + 1)]
