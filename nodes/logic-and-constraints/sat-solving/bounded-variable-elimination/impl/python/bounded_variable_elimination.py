# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounded-variable-elimination/. The authors are listed in prov/CFQP37.jsonl.

"""Bounded variable elimination (BVE) by clause distribution, as in SatELite.

A variable v is eliminated when the number of non-tautological resolvents
on v is at most the number of clauses that contain v or -v (plus an
optional slack). The removed clauses are saved with their witness literal
on a stack, and reconstruct() rebuilds a model of the original formula.
Clauses are lists of DIMACS ints.
"""


def resolve(c: frozenset[int], d: frozenset[int], v: int) -> frozenset[int] | None:
    """Resolvent of c (with v) and d (with -v) on v, or None if it is a tautology."""
    r = (c - {v}) | (d - {-v})
    if any(-a in r for a in r):
        return None
    return r


def bve(clauses: list[list[int]], frozen: frozenset[int] = frozenset(),
        slack: int = 0) -> tuple[list[list[int]], list[tuple[list[int], int]]]:
    """Eliminate variables while the clause count does not grow by more than slack.

    Returns (remaining clauses, stack of (clause, witness literal)).
    Variables in frozen are kept. If the empty clause appears, the remaining
    clauses are [[]].
    """
    cnf: set[frozenset[int]] = set()
    for c in clauses:
        s = frozenset(c)
        if not any(-a in s for a in s):
            cnf.add(s)
    stack: list[tuple[list[int], int]] = []
    changed = True
    while changed:  # @line L1
        changed = False
        if frozenset() in cnf:
            return [[]], stack
        variables = {abs(a) for c in cnf for a in c} - set(frozen)
        occ = {v: (sum(v in c for c in cnf), sum(-v in c for c in cnf)) for v in variables}
        for v in sorted(variables, key=lambda u: (occ[u][0] * occ[u][1], u)):  # @line L2
            pos = [c for c in cnf if v in c]  # @line L3
            neg = [c for c in cnf if -v in c]
            if not pos and not neg:
                continue
            res = set()  # @line L4
            for c in pos:
                for d in neg:
                    r = resolve(c, d, v)
                    if r is not None:
                        res.add(r)
            if len(res) <= len(pos) + len(neg) + slack:  # @line L5
                cnf.difference_update(pos)  # @line L6
                cnf.difference_update(neg)
                cnf |= res  # @line L7
                for c in pos:
                    stack.append((sorted(c, key=lambda a: (abs(a), a)), v))  # @line L8
                for d in neg:
                    stack.append((sorted(d, key=lambda a: (abs(a), a)), -v))
                changed = True
                break
    rest = sorted(sorted(c, key=lambda a: (abs(a), a)) for c in cnf)
    return rest, stack


def reconstruct(model: dict[int, bool], stack: list[tuple[list[int], int]]) -> dict[int, bool]:
    """Extend a model of the reduced formula to one of the original formula."""
    alpha = dict(model)
    for c, lit in reversed(stack):  # @line L9
        if not any(alpha[abs(a)] == (a > 0) for a in c):  # @line L10
            alpha[abs(lit)] = lit > 0
    return alpha  # @line L11
