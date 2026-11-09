# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gsat/. The authors are listed in prov/BW0R7G.jsonl.

"""GSAT: greedy local search for SAT (Selman, Levesque and Mitchell 1992).

Clauses are DIMACS-style lists of nonzero ints over the variables 1 .. n.
GSAT is incomplete: it returns a model or None, and None does not prove that
the formula is unsatisfiable.
"""

import random


def normalize(clauses: list[list[int]]) -> list[list[int]] | None:
    """Drop repeated literals and tautologies. None when an empty clause occurs."""
    out = []
    for cl in clauses:
        c = sorted(set(cl))
        if not c:
            return None
        if any(-l in c for l in c):
            continue  # always true
        out.append(c)
    return out


def scores(n: int, clauses: list[list[int]], x: list[bool]) -> tuple[list[int], list[int]]:
    """make[v] and break[v] for v = 1 .. n under x (x[v] for v = 1 .. n, x[0] unused).

    make[v]: false clauses that flipping v makes true.
    break[v]: true clauses that flipping v makes false.
    """
    make = [0] * (n + 1)
    brk = [0] * (n + 1)
    for cl in clauses:
        true_lits = [l for l in cl if x[abs(l)] == (l > 0)]
        if not true_lits:
            for l in cl:
                make[abs(l)] += 1
        elif len(true_lits) == 1:
            brk[abs(true_lits[0])] += 1
    return make, brk


def gsat(n: int, clauses: list[list[int]], max_tries: int = 10, max_flips: int | None = None, rng: random.Random | None = None) -> list[bool] | None:
    """Return a model as a list of n booleans (x[v - 1] is the value of v), or None.

    max_flips defaults to 5 n. Each flip takes O(m k) time here, since the
    scores are recomputed from scratch.
    """
    rng = rng or random.Random()
    cls = normalize(clauses)
    if cls is None:
        return None
    if max_flips is None:
        max_flips = 5 * n
    for _ in range(max_tries):  # @line L1
        x = [False] + [rng.random() < 0.5 for _ in range(n)]  # @line L2
        for f in range(max_flips + 1):  # @line L3
            if all(any(x[abs(l)] == (l > 0) for l in cl) for cl in cls):  # @line L4
                return x[1:]
            if f == max_flips or n == 0:
                break
            make, brk = scores(n, cls, x)
            best = max(make[v] - brk[v] for v in range(1, n + 1))  # @line L5
            ties = [v for v in range(1, n + 1) if make[v] - brk[v] == best]
            v = rng.choice(ties)  # @line L6
            x[v] = not x[v]  # @line L7
    return None  # @line L8
