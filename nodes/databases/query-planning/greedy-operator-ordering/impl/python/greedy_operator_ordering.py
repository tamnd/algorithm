# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-operator-ordering/. The authors are listed in prov/X0F4M8.jsonl.
"""Greedy operator ordering (GOO), a join ordering heuristic after Fegaras (1998).

The input is a query graph: the size of each relation and a selectivity on
each edge {i, j}. GOO keeps a set of join trees, one per relation at the
start. In each step it joins the two trees whose join has the smallest
estimated size. By default it only joins trees that an edge links, and it
uses a cross product only when no two trees are linked, which happens when
the query graph is not connected.

The size of a join of trees T1 and T2 is |T1| * |T2| * f, where f is the
product of the selectivities of the edges between them. The cost of the
result is C_out, the sum of the sizes of all joins. GOO is a heuristic: it
builds a bushy tree in O(n^3) time, and the tree may cost more than the
optimum.
"""

from fractions import Fraction
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union

Plan = Union[int, tuple]
Edges = Dict[Tuple[int, int], Fraction]


def _norm(sel: Edges, n: int) -> Edges:
    out: Edges = {}
    for (i, j), f in sel.items():
        if i == j or not (0 <= i < n and 0 <= j < n):
            raise ValueError("an edge needs two different relations")
        key = (min(i, j), max(i, j))
        out[key] = out.get(key, Fraction(1)) * Fraction(f)
    return out


def goo(card: Sequence, sel: Edges, cross_products: bool = False,
        on_step: Optional[Callable[[Plan, Plan, Fraction], None]] = None) -> Tuple[Fraction, Plan]:
    """Return (C_out cost, plan). A plan is a relation number or a pair (left, right).

    Ties are broken by the smallest pair of tree numbers. If cross_products is
    True, every pair of trees is a candidate in every step. on_step(T1, T2,
    size) is called for each join, with the larger input as T1.
    """
    n = len(card)
    if n == 0:
        raise ValueError("no relations")
    sel = _norm(sel, n)
    plan: Dict[int, Plan] = {}
    size: Dict[int, Fraction] = {}
    for i in range(n):  # @line L1
        plan[i], size[i] = i, Fraction(card[i])
    # between[a][b]: the product of the selectivities between trees a and b, or None if no edge.
    between: Dict[int, Dict[int, Optional[Fraction]]] = {a: {b: None for b in range(n) if b != a} for a in range(n)}
    for (i, j), f in sel.items():
        between[i][j] = between[j][i] = f
    cost = Fraction(0)
    nxt = n
    while len(plan) > 1:  # @line L2
        best = None
        ids = sorted(plan)
        linked = any(between[a][b] is not None for a in ids for b in ids if a < b)
        for x, a in enumerate(ids):  # @line L3
            for b in ids[x + 1:]:
                f = between[a][b]
                if f is None and linked and not cross_products:
                    continue
                s = size[a] * size[b] * (Fraction(1) if f is None else f)
                if best is None or s < best[0]:
                    best = (s, a, b)
        s, a, b = best
        left, right = (a, b) if size[a] >= size[b] else (b, a)
        if on_step is not None:
            on_step(plan[left], plan[right], s)
        new = nxt  # @line L4
        nxt += 1
        plan[new], size[new] = (plan[left], plan[right]), s  # @line L5
        cost += s
        between[new] = {}
        for c in plan:
            if c in (a, b, new):
                continue
            fa, fb = between[a][c], between[b][c]
            f = None
            if fa is not None or fb is not None:
                f = (Fraction(1) if fa is None else fa) * (Fraction(1) if fb is None else fb)
            between[new][c] = between[c][new] = f
            del between[c][a], between[c][b]
        for t in (a, b):
            del plan[t], size[t], between[t]
    (root,) = plan.values()
    return cost, root  # @line L6


def leaves(p: Plan) -> List[int]:
    return [p] if isinstance(p, int) else leaves(p[0]) + leaves(p[1])


def plan_size(card: Sequence, sel: Edges, rels: Sequence[int]) -> Fraction:
    s = Fraction(1)
    rs = set(rels)
    for i in rs:
        s *= Fraction(card[i])
    for (i, j), f in _norm(sel, len(card)).items():
        if i in rs and j in rs:
            s *= f
    return s


def plan_cost(card: Sequence, sel: Edges, p: Plan) -> Fraction:
    """The C_out cost of a plan: the sum of the sizes of its joins."""
    if isinstance(p, int):
        return Fraction(0)
    return plan_cost(card, sel, p[0]) + plan_cost(card, sel, p[1]) + plan_size(card, sel, leaves(p))
