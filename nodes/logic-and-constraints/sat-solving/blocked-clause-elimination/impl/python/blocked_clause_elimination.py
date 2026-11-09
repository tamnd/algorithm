# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blocked-clause-elimination/. The authors are listed in prov/GQDPDA.jsonl.

"""Blocked clause elimination (BCE) with model reconstruction.

A clause C is blocked on a literal l in C (with respect to F) if every
resolvent of C on l with a clause of F that contains -l is a tautology.
Removing a blocked clause keeps satisfiability. Each removed clause is
saved with its blocking literal; reconstruct() turns a model of the
reduced formula into a model of the original. Clauses are DIMACS ints.
"""

from collections import deque


def is_blocked(c: set[int], lit: int, others: list[set[int]]) -> bool:
    """True if c is blocked on lit with respect to the clauses in others."""
    return all(any(-m in d for m in c if m != lit) for d in others if -lit in d)


def bce(clauses: list[list[int]]) -> tuple[list[list[int]], list[tuple[list[int], int]]]:
    """Remove blocked clauses until none is left.

    Returns (remaining clauses, stack of (clause, blocking literal)).
    Tautologies are blocked on any of their literals and are removed too.
    """
    cls: list[set[int] | None] = [set(c) for c in clauses]
    occ: dict[int, set[int]] = {}
    for i, c in enumerate(cls):
        for a in c:
            occ.setdefault(a, set()).add(i)
    stack: list[tuple[list[int], int]] = []  # @line L1
    queue = deque(range(len(cls)))
    queued = set(queue)
    while queue:  # @line L2
        i = queue.popleft()  # @line L3
        queued.discard(i)
        c = cls[i]
        if c is None:
            continue
        for lit in sorted(c, key=lambda a: (abs(a), a)):  # @line L4
            partners = [cls[j] for j in occ.get(-lit, ()) if j != i]
            if is_blocked(c, lit, partners):  # @line L5
                cls[i] = None  # @line L6
                stack.append((sorted(c, key=lambda a: (abs(a), a)), lit))
                for a in c:
                    occ[a].discard(i)
                for a in c:  # @line L7
                    for j in occ.get(-a, ()):
                        if j not in queued:
                            queue.append(j)
                            queued.add(j)
                break
    rest = [sorted(c, key=lambda a: (abs(a), a)) for c in cls if c is not None]
    return rest, stack  # @line L8


def reconstruct(model: dict[int, bool], stack: list[tuple[list[int], int]]) -> dict[int, bool]:
    """Extend a model of the reduced formula to a model of the original.

    model must give a value to every variable of the original formula.
    """
    alpha = dict(model)
    for c, lit in reversed(stack):  # @line L9
        if not any(alpha[abs(a)] == (a > 0) for a in c):  # @line L10
            alpha[abs(lit)] = lit > 0
    return alpha  # @line L11
