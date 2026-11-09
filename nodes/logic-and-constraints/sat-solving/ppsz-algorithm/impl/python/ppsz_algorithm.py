# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ppsz-algorithm/. The authors are listed in prov/ECTVB1.jsonl.

"""The PPSZ algorithm for k-SAT (Paturi, Pudlak, Saks and Zane).

Clauses are DIMACS-style lists of nonzero ints over the variables 1 .. n.
The algorithm has one-sided error: it returns an assignment only when the
assignment satisfies every clause, and None when no try found one, which does
not prove that the formula is unsatisfiable.
"""

import random
from collections.abc import Callable


def bounded_resolution(clauses: list[list[int]], s: int) -> list[frozenset[int]]:
    """Close the formula under resolution, keeping resolvents of at most s literals.

    Tautologies and repeated literals are removed. Every clause of the result
    is implied by the input, so the result has the same models.
    """
    known: set[frozenset[int]] = set()
    order: list[frozenset[int]] = []
    for cl in clauses:
        c = frozenset(cl)
        if any(-l in c for l in c) or c in known:
            continue
        known.add(c)
        order.append(c)
    by_lit: dict[int, list[frozenset[int]]] = {}
    for c in order:
        for l in c:
            by_lit.setdefault(l, []).append(c)
    i = 0
    while i < len(order):  # each clause is resolved once with each earlier and later partner
        c = order[i]
        i += 1
        for l in c:
            for d in list(by_lit.get(-l, [])):
                r = (c - {l}) | (d - {-l})
                if len(r) > s or r in known or any(-x in r for x in r):
                    continue
                known.add(r)
                order.append(r)
                for x in r:
                    by_lit.setdefault(x, []).append(r)
    return order


def ppsz_try(n: int, occ: list[list[frozenset[int]]], rng: random.Random) -> list[bool]:
    """One try of PPSZ: a random order, forced values from unit clauses, else random values."""
    order = list(range(1, n + 1))
    rng.shuffle(order)  # @line L3
    return ppsz_pass(n, occ, order, lambda v: rng.randrange(2))[0]


def ppsz_pass(n: int, occ: list[list[frozenset[int]]], order: list[int], guess: Callable[[int], int]) -> tuple[list[bool], list[bool]]:
    """Set the variables in the given order. Returns (values, forced) as lists of n booleans."""
    val: list[int] = [-1] * (n + 1)  # -1 unset, 0 false, 1 true
    was_forced = [False] * (n + 1)
    for v in order:  # @line L4
        forced = -1
        for c in occ[v]:
            # c is a unit clause on v when no literal is true and every other literal is false
            ok = True
            lit_v = 0
            for l in c:
                a = abs(l)
                if a == v:
                    lit_v = l
                    continue
                if val[a] == -1 or (val[a] == 1) == (l > 0):
                    ok = False
                    break
            if ok:  # @line L5
                forced = 1 if lit_v > 0 else 0  # @line L6
                break
        was_forced[v] = forced != -1
        val[v] = forced if forced != -1 else guess(v)  # @line L7
    return [val[v] == 1 for v in range(1, n + 1)], was_forced[1:]


def satisfies(clauses: list[list[int]], x: list[bool]) -> bool:
    return all(any(x[abs(l) - 1] == (l > 0) for l in cl) for cl in clauses)


def ppsz_algorithm(n: int, clauses: list[list[int]], tries: int = 1000, s: int | None = None, rng: random.Random | None = None) -> list[bool] | None:
    """PPSZ: bounded resolution, then random tries.

    s is the bound on the size of resolvents; the default is the longest
    clause. The closure can have about (2n)^s clauses, so keep s small. Returns a model as a list of n booleans (x[v - 1] is the
    value of v), or None when no try found one.
    """
    rng = rng or random.Random()
    if any(len(cl) == 0 for cl in clauses):
        return None
    k = max((len(set(cl)) for cl in clauses), default=1)
    g = bounded_resolution(clauses, s if s is not None else k)  # @line L1
    if frozenset() in g:
        return None  # resolution derived the empty clause: no model
    occ: list[list[frozenset[int]]] = [[] for _ in range(n + 1)]
    for c in g:
        for l in c:
            occ[abs(l)].append(c)
    for _ in range(tries):  # @line L2
        x = ppsz_try(n, occ, rng)
        if satisfies(clauses, x):  # @line L8
            return x
    return None  # @line L9
