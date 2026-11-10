# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/max-sat-lp-rounding/. The authors are listed in prov/TE21R0.jsonl.

import random
from fractions import Fraction
from typing import Sequence

Clause = Sequence[int]  # DIMACS literals: +i is x_i, -i is not x_i, variables 1 .. n


def _simplex_max(
    c: Sequence[Fraction], a: Sequence[Sequence[Fraction]], b: Sequence[Fraction]
) -> tuple[Fraction, list[Fraction]]:
    """Maximize c.x subject to a x <= b and x >= 0, exactly, for b >= 0.

    A dense tableau simplex with Bland's rule, in exact rational arithmetic,
    started at the slack basis. It is meant for small instances only.
    """
    m, n = len(a), len(c)
    t = [[Fraction(v) for v in a[i]] + [Fraction(int(k == i)) for k in range(m)] + [Fraction(b[i])] for i in range(m)]
    basis = [n + i for i in range(m)]
    cost = [Fraction(v) for v in c] + [Fraction(0)] * m
    while True:
        enter = None
        for j in range(n + m):
            if j not in basis and cost[j] - sum(cost[basis[i]] * t[i][j] for i in range(m)) > 0:
                enter = j
                break
        if enter is None:
            break
        best = None
        for i in range(m):
            if t[i][enter] > 0:
                q = t[i][-1] / t[i][enter]
                if best is None or q < best[0] or (q == best[0] and basis[i] < basis[best[1]]):
                    best = (q, i)
        if best is None:
            raise ValueError("the LP is unbounded")
        r = best[1]
        p = t[r][enter]
        t[r] = [v / p for v in t[r]]
        for k in range(m):
            if k != r and t[k][enter] != 0:
                f = t[k][enter]
                t[k] = [u - f * v for u, v in zip(t[k], t[r])]
        basis[r] = enter
    x = [Fraction(0)] * n
    for i, j in enumerate(basis):
        if j < n:
            x[j] = t[i][-1]
    return sum((ci * xi for ci, xi in zip(cost, x)), Fraction(0)), x


def _check(n: int, clauses: Sequence[Clause], weights: Sequence[int | Fraction]) -> None:
    if len(clauses) != len(weights) or any(w < 0 for w in weights):
        raise ValueError("one non-negative weight per clause is needed")
    for cl in clauses:
        if not cl or any(l == 0 or abs(l) > n for l in cl) or len({abs(l) for l in cl}) != len(cl):
            raise ValueError("each clause needs literals on different variables among 1 .. n")


def solve_max_sat_lp(
    n: int, clauses: Sequence[Clause], weights: Sequence[int | Fraction]
) -> tuple[Fraction, list[Fraction], list[Fraction]]:
    """Return (LP*, y, z) for: max sum w_j z_j, z_j <= sum_{P_j} y_i + sum_{N_j} (1 - y_i), 0 <= y, z <= 1."""
    m = len(clauses)
    rows: list[list[Fraction]] = []
    rhs: list[Fraction] = []
    for j, cl in enumerate(clauses):
        row = [Fraction(0)] * (n + m)
        row[n + j] = Fraction(1)
        for l in cl:
            row[abs(l) - 1] = Fraction(-1 if l > 0 else 1)
        rows.append(row)
        rhs.append(Fraction(sum(1 for l in cl if l < 0)))
    for k in range(n + m):
        rows.append([Fraction(int(i == k)) for i in range(n + m)])
        rhs.append(Fraction(1))
    val, v = _simplex_max([Fraction(0)] * n + [Fraction(w) for w in weights], rows, rhs)
    return val, v[:n], v[n:]


def satisfied_weight(clauses: Sequence[Clause], weights: Sequence[int | Fraction], a: Sequence[bool]) -> Fraction:
    """The total weight of the clauses satisfied by a, where a[i - 1] is the value of x_i."""
    return sum((Fraction(w) for cl, w in zip(clauses, weights) if any(a[abs(l) - 1] == (l > 0) for l in cl)), Fraction(0))


def expected_weight(clauses: Sequence[Clause], weights: Sequence[int | Fraction], p: Sequence[Fraction]) -> Fraction:
    """E[satisfied weight] when x_i is true with probability p[i - 1], independently."""
    total = Fraction(0)
    for cl, w in zip(clauses, weights):
        false = Fraction(1)
        for l in cl:
            false *= (1 - p[abs(l) - 1]) if l > 0 else p[abs(l) - 1]
        total += Fraction(w) * (1 - false)
    return total


def derandomize(
    n: int, clauses: Sequence[Clause], weights: Sequence[int | Fraction], p: Sequence[Fraction]
) -> list[bool]:
    """Method of conditional expectations: fix x_1 .. x_n so the satisfied weight is >= expected_weight(p)."""
    q = [Fraction(v) for v in p]
    for i in range(n):
        q[i] = Fraction(1)
        e_true = expected_weight(clauses, weights, q)
        q[i] = Fraction(0)
        e_false = expected_weight(clauses, weights, q)
        q[i] = Fraction(1) if e_true >= e_false else Fraction(0)
    return [v == 1 for v in q]


def max_sat_lp_rounding(
    n: int, clauses: Sequence[Clause], weights: Sequence[int | Fraction], rng: random.Random
) -> tuple[list[bool], Fraction, Fraction]:
    """Return (a, W(a), LP*): the better of LP rounding and a fair random assignment.

    Precondition: weights are non-negative and each clause has literals on
    different variables (else ValueError). E[W(a)] >= (3/4) LP* >= (3/4) OPT.
    Cost: one LP solve (an exact simplex here, for small instances only) and
    O(n + total clause length) more.
    """
    _check(n, clauses, weights)
    lp_value, y, z = solve_max_sat_lp(n, clauses, weights)  # @line L1
    a = [rng.random() < y[i] for i in range(n)]  # @line L2
    b = [rng.random() < 0.5 for _ in range(n)]  # @line L3
    wa, wb = satisfied_weight(clauses, weights, a), satisfied_weight(clauses, weights, b)
    if wa >= wb:  # @line L4
        return a, wa, lp_value
    return b, wb, lp_value


def deterministic_max_sat(
    n: int, clauses: Sequence[Clause], weights: Sequence[int | Fraction]
) -> tuple[list[bool], Fraction, Fraction]:
    """Return (a, W(a), LP*): the better of the two derandomized roundings, so W(a) >= (3/4) LP*."""
    _check(n, clauses, weights)
    lp_value, y, z = solve_max_sat_lp(n, clauses, weights)
    a = derandomize(n, clauses, weights, y)
    b = derandomize(n, clauses, weights, [Fraction(1, 2)] * n)
    wa, wb = satisfied_weight(clauses, weights, a), satisfied_weight(clauses, weights, b)
    return (a, wa, lp_value) if wa >= wb else (b, wb, lp_value)
