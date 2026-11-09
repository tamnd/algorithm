# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/failed-literal-probing/. The authors are listed in prov/SWRBBT.jsonl.

"""Failed-literal probing with lifting.

For each free variable x, run unit propagation on F with x and on F with
-x. If one side gives a conflict, the other literal is a unit of F. If
both give a conflict, F is unsatisfiable. A literal implied on both sides
is also a unit (lifting). Clauses are lists of DIMACS ints.
"""


def unit_propagate(clauses: list[list[int]], assign: dict[int, bool]) -> dict[int, bool] | None:
    """Closure of assign under unit propagation, or None on a conflict."""
    a = dict(assign)
    changed = True
    while changed:
        changed = False
        for c in clauses:
            free = None
            nfree = 0
            done = False
            for lit in c:
                v = a.get(abs(lit))
                if v is None:
                    free = lit
                    nfree += 1
                elif v == (lit > 0):
                    done = True
                    break
            if done:
                continue
            if nfree == 0:
                return None
            if nfree == 1:
                a[abs(free)] = free > 0
                changed = True
    return a


def probe(clauses: list[list[int]], n: int) -> dict[int, bool] | None:
    """Return the fixed literals found by probing (as an assignment), or None if UNSAT."""
    fixed = unit_propagate(clauses, {})
    if fixed is None:
        return None
    again = True
    while again:  # @line L1
        again = False
        for x in range(1, n + 1):  # @line L2
            if x in fixed:
                continue
            pos = unit_propagate(clauses, {**fixed, x: True})  # @line L3
            neg = unit_propagate(clauses, {**fixed, x: False})
            if pos is None and neg is None:  # @line L4
                return None
            if pos is None:  # @line L5
                new = {x: False}
            elif neg is None:  # @line L6
                new = {x: True}
            else:  # @line L7
                new = {v: b for v, b in pos.items() if v not in fixed and neg.get(v) == b}
            if new:
                fixed = unit_propagate(clauses, {**fixed, **new})
                if fixed is None:
                    return None
                again = True  # @line L8
    return fixed  # @line L9


def simplify(clauses: list[list[int]], fixed: dict[int, bool]) -> list[list[int]]:
    """Remove satisfied clauses and false literals; keep the units of fixed."""
    out = [[v if b else -v] for v, b in sorted(fixed.items())]
    for c in clauses:
        if any(fixed.get(abs(a)) == (a > 0) for a in c):
            continue
        out.append([a for a in c if abs(a) not in fixed])
    return out
