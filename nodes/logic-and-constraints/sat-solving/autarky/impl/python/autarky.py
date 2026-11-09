# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/autarky/. The authors are listed in prov/FSZY2A.jsonl.

"""Autarkies of a CNF formula.

A partial assignment alpha is an autarky for F if every clause of F that
contains a variable set by alpha is satisfied by alpha. Removing those
clauses keeps satisfiability. find_autarky() reduces the search for a
non-trivial autarky to SAT (two variables per original variable, as in
Liffiton and Sakallah 2008) and solves it with a small DPLL. lean_kernel()
applies autarkies until none is left. Clauses are lists of DIMACS ints.
"""


def is_autarky(clauses: list[list[int]], alpha: dict[int, bool]) -> bool:
    for c in clauses:
        if any(abs(a) in alpha for a in c):  # the clause is touched
            if not any(alpha.get(abs(a)) == (a > 0) for a in c):
                return False
    return True


def apply_autarky(clauses: list[list[int]], alpha: dict[int, bool]) -> list[list[int]]:
    """The clauses that alpha does not touch."""
    return [c for c in clauses if not any(abs(a) in alpha for a in c)]


def _dpll(clauses: list[list[int]], assign: dict[int, bool]) -> dict[int, bool] | None:
    a = dict(assign)
    while True:  # unit propagation
        unit = None
        for c in clauses:
            free = [x for x in c if abs(x) not in a]
            if any(a.get(abs(x)) == (x > 0) for x in c):
                continue
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
                r = _dpll(clauses, {**a, abs(x): value})
                if r is not None:
                    return r
            return None
    return a


def find_autarky(clauses: list[list[int]]) -> dict[int, bool] | None:
    """A non-trivial autarky (one that satisfies some clause), or None if F is lean."""
    variables = sorted({abs(a) for c in clauses for a in c})
    if not variables:
        return None
    t = {x: 2 * i + 1 for i, x in enumerate(variables)}  # "x is set true"
    f = {x: 2 * i + 2 for i, x in enumerate(variables)}  # "x is set false"

    def is_true(lit: int) -> int:
        return t[lit] if lit > 0 else f[-lit]

    def is_false(lit: int) -> int:
        return f[lit] if lit > 0 else t[-lit]

    enc = [[-t[x], -f[x]] for x in variables]  # @line L1
    for c in clauses:  # @line L2
        for lit in c:
            enc.append([-is_false(lit)] + [is_true(b) for b in c])  # @line L3
    enc.append(sorted({is_true(a) for c in clauses for a in c}))  # @line L4
    model = _dpll(enc, {})  # @line L5
    if model is None:
        return None
    alpha = {}
    for x in variables:  # @line L6
        if model.get(t[x]):
            alpha[x] = True
        elif model.get(f[x]):
            alpha[x] = False
    return alpha


def lean_kernel(clauses: list[list[int]]) -> tuple[list[list[int]], dict[int, bool]]:
    """Apply autarkies until the rest is lean.

    Returns (lean kernel, the composed autarky). The autarky satisfies
    exactly the clauses outside the kernel.
    """
    rest = [list(c) for c in clauses]
    total: dict[int, bool] = {}
    while True:  # @line L7
        alpha = find_autarky(rest)
        if alpha is None:
            return rest, total  # @line L9
        rest = apply_autarky(rest, alpha)  # @line L8
        total = {**alpha, **total}  # earlier autarkies keep their values
