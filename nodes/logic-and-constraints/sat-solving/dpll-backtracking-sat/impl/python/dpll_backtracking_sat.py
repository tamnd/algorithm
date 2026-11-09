# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dpll-backtracking-sat/. The authors are listed in prov/EPST33.jsonl.

"""Plain backtracking search for CNF satisfiability.

A clause is a list of nonzero ints in DIMACS style: v is the variable v and
-v is its negation. The search assigns x1, x2, ..., xn in this order, tries
false before true, and backtracks as soon as a clause whose largest variable
was just assigned is false. It uses no unit propagation and no pure literal
rule; that is the job of DPLL.
"""

from __future__ import annotations

from collections.abc import Sequence


def dpll_backtracking_sat(
    n: int,
    clauses: Sequence[Sequence[int]],
    log: list[tuple[int, bool, bool]] | None = None,
) -> list[int] | None:
    """Return a model as a list of n literals (entry i is i + 1 or -(i + 1)),
    or None when the formula has no model.

    Precondition: n >= 0 and each literal l of each clause has 1 <= |l| <= n.
    If log is a list, each test of line L5 appends (i, value of x_i, passed).
    Cost: at most 2^(n+1) - 2 tests of line L5. The tests at depth i read only
    the clauses whose largest variable is x_i, so the time is O(2^n (n + |F|))
    in the worst case, where |F| is the number of literal occurrences. The
    extra space is O(n + m) for m clauses.
    """
    if any(len(c) == 0 for c in clauses):  # @line L1
        return None
    by_max: list[list[Sequence[int]]] = [[] for _ in range(n + 1)]
    for c in clauses:
        by_max[max(abs(lit) for lit in c)].append(c)
    if n == 0:  # @line L2
        return []
    alpha = [0] * (n + 1)  # 1 is true, -1 is false, 0 is unassigned
    i = 1  # @line L3
    alpha[1] = -1
    while True:  # @line L4
        ok = all(
            any(alpha[abs(lit)] == (1 if lit > 0 else -1) for lit in c) for c in by_max[i]
        )  # @line L5
        if log is not None:
            log.append((i, alpha[i] == 1, ok))
        if ok:
            if i == n:  # @line L6
                return [v if alpha[v] == 1 else -v for v in range(1, n + 1)]
            i += 1  # @line L7
            alpha[i] = -1
        else:  # @line L8
            while i >= 1 and alpha[i] == 1:  # @line L9
                alpha[i] = 0
                i -= 1
            if i == 0:  # @line L10
                return None
            alpha[i] = 1  # @line L11
