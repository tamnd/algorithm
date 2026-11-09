# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lookahead-sat/. The authors are listed in prov/AM6WAY.jsonl.

"""A small lookahead DPLL solver.

At each node, every free variable x is tried both ways with unit propagation.
A side that fails gives a failed literal, a side that shortens no clause
gives an autarky, and otherwise the reduction counts d(x) and d(-x) score
the variable. The solver branches on the best score. Clauses are lists of
DIMACS ints; an assignment is a dict from variable to bool.
"""

from dataclasses import dataclass


@dataclass
class Stats:
    nodes: int = 0
    failed_literals: int = 0
    autarkies: int = 0
    lookaheads: int = 0


def propagate(clauses: list[list[int]], assign: dict[int, bool]) -> dict[int, bool] | None:
    """Unit propagation to a fixpoint; None on a conflict."""
    assign = dict(assign)
    changed = True
    while changed:
        changed = False
        for c in clauses:
            free = None
            count = 0
            for a in c:
                v = assign.get(abs(a))
                if v is None:
                    free = a
                    count += 1
                elif v == (a > 0):
                    break
            else:
                if count == 0:
                    return None
                if count == 1:
                    assign[abs(free)] = free > 0
                    changed = True
    return assign


def satisfied(clause: list[int], assign: dict[int, bool]) -> bool:
    return any(assign.get(abs(a)) == (a > 0) for a in clause)


def reduction(clauses: list[list[int]], before: dict[int, bool], after: dict[int, bool]) -> int:
    """d(l): the clauses that the step from before to after shortens but does not satisfy."""
    count = 0
    for c in clauses:
        if satisfied(c, after):
            continue
        if any(abs(a) in after and abs(a) not in before for a in c):
            count += 1
    return count


def score(d_pos: int, d_neg: int) -> int:
    """The product rule with the sum as a tie-breaker."""
    return 1024 * d_pos * d_neg + d_pos + d_neg


def lookahead(clauses: list[list[int]], assign: dict[int, bool], stats: Stats):
    """One lookahead phase. Returns ("unsat", None), ("sat", model) or ("branch", (x, d, assign))."""
    while True:
        open_clauses = [c for c in clauses if not satisfied(c, assign)]
        if not open_clauses:  # @line L2
            return "sat", assign
        free = sorted({abs(a) for c in open_clauses for a in c if abs(a) not in assign})
        best = None
        restart = False
        for x in free:  # @line L3
            stats.lookaheads += 1
            side = {lit: propagate(clauses, {**assign, x: lit > 0}) for lit in (x, -x)}  # @line L4
            if side[x] is None and side[-x] is None:  # @line L5
                return "unsat", None
            failed = [lit for lit in (x, -x) if side[lit] is None]
            if failed:  # @line L6
                stats.failed_literals += 1
                assign = side[-failed[0]]
                restart = True
                break
            d = {lit: reduction(clauses, assign, side[lit]) for lit in (x, -x)}  # @line L7
            zero = [lit for lit in (x, -x) if d[lit] == 0]
            if zero:  # @line L8
                stats.autarkies += 1
                assign = side[zero[0]]
                restart = True
                break
            s = score(d[x], d[-x])
            if best is None or s > best[0]:  # @line L9
                best = (s, x, d)
        if not restart:
            return "branch", (best[1], best[2], assign)


def solve(clauses: list[list[int]], n: int, stats: Stats | None = None) -> dict[int, bool] | None:
    """A model over 1..n, or None if the formula is unsatisfiable."""
    stats = stats if stats is not None else Stats()

    def rec(assign: dict[int, bool]) -> dict[int, bool] | None:
        stats.nodes += 1
        assign = propagate(clauses, assign)  # @line L1
        if assign is None:
            return None
        kind, info = lookahead(clauses, assign, stats)
        if kind == "unsat":
            return None
        if kind == "sat":
            return {v: info.get(v, False) for v in range(1, n + 1)}
        x, d, assign = info
        first = x if d[x] <= d[-x] else -x  # the side that reduces less first
        for lit in (first, -first):  # @line L10
            model = rec({**assign, abs(lit): lit > 0})
            if model is not None:
                return model
        return None  # @line L11

    return rec({})
