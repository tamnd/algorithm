# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/max-product/. The authors are listed in prov/SMKERH.jsonl.

"""The max-product algorithm on a factor tree, with backtracking for a MAP assignment.

A model is a list of factors over the variables 0 .. n-1, where variable v takes
the values 0 .. card[v]-1. A factor is a scope (a nonempty tuple of distinct
variables) and a table from assignments of the scope to nonnegative numbers.
The factor graph must be a forest. max_product returns an assignment that
maximizes the product of the factors among the assignments that agree with the
evidence, the maximum, and the max-marginals. max_sum does the same with
log-tables, where the product becomes a sum (Pearl 1988, Chapter 5).
Ties are broken toward the smaller value, and backtracking keeps the choices
consistent.
"""

import math
from operator import add, mul
from typing import Callable, Dict, List, NamedTuple, Sequence, Tuple

Assignment = Tuple[int, ...]
Node = Tuple[str, int]  # ("v", i) for variable i, ("f", j) for factor j


class Factor(NamedTuple):
    scope: Tuple[int, ...]
    table: Dict[Assignment, object]


class Result(NamedTuple):
    assignment: Tuple[int, ...]           # a MAP assignment of all the variables
    value: object                         # its value: the maximum of the product (or of the sum of logs)
    max_marginals: List[List[object]]     # max over the other variables, for each variable and value
    messages: int


def _run(factors: Sequence[Factor], card: Sequence[int], evidence: Dict[int, int],
         times: Callable, unit: object, bottom: object) -> Result:
    n = len(card)
    nb: Dict[Node, List[Node]] = {("v", v): [] for v in range(n)}
    for j, f in enumerate(factors):
        if not f.scope or len(set(f.scope)) != len(f.scope):
            raise ValueError("a scope must be nonempty and hold each variable once")
        nb[("f", j)] = [("v", v) for v in f.scope]
        for v in f.scope:
            nb[("v", v)].append(("f", j))
    lam = [[unit if v not in evidence or x == evidence[v] else bottom for x in range(card[v])]
           for v in range(n)]
    msg: Dict[Tuple[Node, Node], List[object]] = {}

    def into_var(x: Node, skip: Node) -> List[object]:
        m = list(lam[x[1]])
        for g in nb[x]:
            if g != skip:
                m = [times(a, b) for a, b in zip(m, msg[g, x])]
        return m

    def factor_score(j: int, a: Assignment, skip: int) -> object:
        """f_j(a) times the messages into f_j from its variables, except skip."""
        val = factors[j].table[a]
        for t, y in enumerate(factors[j].scope):
            if y != skip:
                val = times(val, msg[("v", y), ("f", j)][a[t]])
        return val

    def send(u: Node, w: Node) -> None:
        if u[0] == "v":
            msg[u, w] = into_var(u, w)
            return
        k = factors[u[1]].scope.index(w[1])
        m = [bottom] * card[w[1]]
        for a in factors[u[1]].table:  # @line L3
            s = factor_score(u[1], a, w[1])
            if s > m[a[k]]:
                m[a[k]] = s
        msg[u, w] = m

    order: List[Node] = []
    parent: Dict[Node, Node] = {}
    roots = []
    for v in range(n):  # @line L1
        if ("v", v) in parent:
            continue
        parent[("v", v)] = ("v", v)
        roots.append(("v", v))
        i = len(order)
        order.append(("v", v))
        while i < len(order):
            u = order[i]
            i += 1
            for w in nb[u]:
                if w == parent[u]:
                    continue
                if w in parent:
                    raise ValueError("the factor graph has a cycle")
                parent[w] = u
                order.append(w)
    for u in reversed(order):  # @line L2
        if parent[u] != u:
            send(u, parent[u])
    x: Dict[int, int] = {}
    value = unit
    for r in roots:  # @line L4
        b = into_var(r, ("none", -1))
        best = max(range(card[r[1]]), key=lambda t: (b[t], -t))  # ties: the smaller value
        x[r[1]] = best
        value = times(value, b[best])
    for u in order:  # @line L5
        if u[0] != "f":
            continue
        j, p = u[1], parent[u][1]
        f = factors[j]
        k = f.scope.index(p)
        best_a, best_s = None, None
        for a in sorted(f.table):  # @line L6
            if a[k] == x[p]:
                s = factor_score(j, a, p)
                if best_s is None or s > best_s:
                    best_a, best_s = a, s
        for t, y in enumerate(f.scope):  # @line L7
            if y != p:
                x[y] = best_a[t]
    if value == bottom:
        raise ValueError("every assignment that agrees with the evidence has value zero")
    # The distribute pass gives the max-marginals; it is not needed for the assignment.
    for u in order:
        if parent[u] != u:
            send(parent[u], u)
    max_marginals = [into_var(("v", v), ("none", -1)) for v in range(n)]
    return Result(tuple(x[v] for v in range(n)), value, max_marginals, len(msg))  # @line L8


def max_product(factors: Sequence[Factor], card: Sequence[int], evidence: Dict[int, int]) -> Result:
    """A MAP assignment of a factor forest by max-product messages and backtracking."""
    unit = next((val ** 0 for f in factors for val in f.table.values()), 1)
    return _run(factors, card, evidence, mul, unit, 0 * unit)


def max_sum(log_factors: Sequence[Factor], card: Sequence[int], evidence: Dict[int, int]) -> Result:
    """The same in log space: the tables hold log values (-inf for zero), the product is +."""
    return _run(log_factors, card, evidence, add, 0.0, -math.inf)


def to_log(factors: Sequence[Factor]) -> List[Factor]:
    return [Factor(f.scope, {a: (math.log(v) if v > 0 else -math.inf) for a, v in f.table.items()})
            for f in factors]
