# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-assignment-max-3-sat/. The authors are listed in prov/G3HNQ1.jsonl.

import random
from fractions import Fraction
from typing import Sequence

Clause = Sequence[int]  # DIMACS literals: +i is x_i, -i is not x_i, variables 1 .. n


def _check(n: int, clauses: Sequence[Clause]) -> None:
    for cl in clauses:
        if not cl or any(lit == 0 or abs(lit) > n for lit in cl):
            raise ValueError("each clause needs literals on variables 1 .. n")


def count_satisfied(clauses: Sequence[Clause], a: Sequence[bool]) -> int:
    """The number of clauses satisfied by a, where a[i - 1] is the value of x_i."""
    return sum(1 for cl in clauses if any(a[abs(l) - 1] == (l > 0) for l in cl))


def random_assignment_max_3_sat(
    n: int, clauses: Sequence[Clause], rng: random.Random
) -> tuple[list[bool], int]:
    """Return (a, s): a uniformly random assignment of x_1 .. x_n and the number of clauses it satisfies.

    For clauses with exactly 3 literals on 3 different variables,
    E[s] = 7m/8 >= (7/8) OPT. Time O(n + total clause length).
    """
    _check(n, clauses)
    a = []
    for _ in range(n):  # @line L1
        a.append(rng.random() < 0.5)  # @line L2
    s = count_satisfied(clauses, a)  # @line L3
    return a, s  # @line L4


def expected_satisfied(clauses: Sequence[Clause], fixed: dict[int, bool]) -> Fraction:
    """E[number of satisfied clauses] when the variables in fixed are set and the rest are fair coins."""
    total = Fraction(0)
    for cl in clauses:
        free: set[int] = set()
        sat = False
        signs: dict[int, set[bool]] = {}
        for l in cl:
            v = abs(l)
            if v in fixed:
                if fixed[v] == (l > 0):
                    sat = True
            else:
                signs.setdefault(v, set()).add(l > 0)
                free.add(v)
        if sat or any(len(s) == 2 for s in signs.values()):
            total += 1
        else:
            total += 1 - Fraction(1, 2 ** len(free))
    return total


def derandomized_max_3_sat(n: int, clauses: Sequence[Clause]) -> tuple[list[bool], int]:
    """Fix x_1, ..., x_n in turn to the value with the larger conditional expectation.

    The result satisfies at least E[s] clauses of the random assignment, so at
    least 7m/8 for exact 3-CNF. Time O(n * total clause length).
    """
    _check(n, clauses)
    fixed: dict[int, bool] = {}
    for v in range(1, n + 1):
        fixed[v] = True
        e_true = expected_satisfied(clauses, fixed)
        fixed[v] = False
        e_false = expected_satisfied(clauses, fixed)
        fixed[v] = e_true >= e_false
    a = [fixed[v] for v in range(1, n + 1)]
    return a, count_satisfied(clauses, a)
