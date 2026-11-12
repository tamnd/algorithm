# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-elimination/. The authors are listed in prov/ZJC1JG.jsonl.

"""Variable elimination (Zhang and Poole 1994; Dechter 1996) for discrete models.

A model is a list of factors over variables 0 .. n-1, where variable v takes the
values 0 .. card[v]-1. A factor is a scope (a tuple of distinct variables) and a
table that maps each assignment of the scope (a tuple of values) to a number
(a Fraction, an int or a float). A Bayesian network is the special case with one
factor P(X | parents) for each variable; a Markov random field gives its
potentials. The cost is O(m d^(w+1)) for m factors, domain size at most d and
induced width w of the order.
"""

from itertools import product
from typing import Dict, Iterable, List, NamedTuple, Sequence, Tuple

Assignment = Tuple[int, ...]


class Factor(NamedTuple):
    scope: Tuple[int, ...]
    table: Dict[Assignment, object]


def factor_product(f: Factor, g: Factor, card: Sequence[int]) -> Factor:
    """The product f * g over the union of the two scopes."""
    scope = tuple(f.scope) + tuple(v for v in g.scope if v not in f.scope)
    pos = {v: i for i, v in enumerate(scope)}
    fi = [pos[v] for v in f.scope]
    gi = [pos[v] for v in g.scope]
    table = {}
    for a in product(*(range(card[v]) for v in scope)):
        table[a] = f.table[tuple(a[i] for i in fi)] * g.table[tuple(a[i] for i in gi)]
    return Factor(scope, table)


def sum_out(f: Factor, z: int) -> Factor:
    """Sum the variable z out of f."""
    k = f.scope.index(z)
    scope = f.scope[:k] + f.scope[k + 1:]
    table: Dict[Assignment, object] = {}
    for a, val in f.table.items():
        b = a[:k] + a[k + 1:]
        table[b] = table[b] + val if b in table else val
    return Factor(scope, table)


def reduce_factor(f: Factor, evidence: Dict[int, int]) -> Factor:
    """Keep the rows of f that agree with the evidence, and drop the evidence variables."""
    keep = [i for i, v in enumerate(f.scope) if v not in evidence]
    scope = tuple(f.scope[i] for i in keep)
    table = {}
    for a, val in f.table.items():
        if all(a[i] == evidence[v] for i, v in enumerate(f.scope) if v in evidence):
            table[tuple(a[i] for i in keep)] = val
    return Factor(scope, table)


def multiply_all(factors: Iterable[Factor], card: Sequence[int]) -> Factor:
    result = Factor((), {(): 1})
    for f in factors:
        result = factor_product(result, f, card)
    return result


def variable_elimination(factors: Sequence[Factor], card: Sequence[int], query: Sequence[int],
                         evidence: Dict[int, int], order: Sequence[int]) -> Dict[Assignment, object]:
    """Return P(query | evidence) as a dict from query assignments to probabilities.

    Precondition: query, the evidence variables and order are disjoint, and they
    cover all the variables of the factors; P(evidence) > 0. The keys of the
    result are tuples of values of the query variables, in the order given.
    """
    seen = list(query) + list(evidence) + list(order)
    if len(set(seen)) != len(seen):
        raise ValueError("query, evidence and order must be disjoint")
    phi = [reduce_factor(f, evidence) for f in factors]  # @line L1
    # A unit factor per query variable keeps a query variable that no factor mentions.
    phi += [Factor((q,), {(x,): 1 for x in range(card[q])}) for q in query]
    for z in order:  # @line L2
        psi = [f for f in phi if z in f.scope]  # @line L3
        prod = multiply_all(psi, card)  # @line L4
        tau = sum_out(prod, z) if z in prod.scope else prod  # @line L5
        phi = [f for f in phi if z not in f.scope] + [tau]  # @line L6
    final = multiply_all(phi, card)  # @line L7
    if set(final.scope) != set(query):
        raise ValueError("the order must eliminate every variable that is not a query or evidence variable")
    total = sum(final.table.values())
    if total == 0:
        raise ValueError("the evidence has probability zero")
    idx = [final.scope.index(q) for q in query]
    return {tuple(a[i] for i in idx): val / total for a, val in final.table.items()}  # @line L8


def induced_width(scopes: Iterable[Sequence[int]], order: Sequence[int]) -> int:
    """The induced width of the interaction graph of the scopes along the order.

    The width is the largest number of neighbors that a variable has, among the
    variables not yet eliminated, at the time it is eliminated.
    """
    adj: Dict[int, set] = {v: set() for v in order}
    for s in scopes:
        for u in s:
            adj.setdefault(u, set())
            for v in s:
                if u != v:
                    adj[u].add(v)
    width = 0
    gone: set = set()
    for z in order:
        nb = adj[z] - gone
        width = max(width, len(nb))
        for u in nb:
            adj[u] |= nb - {u}
        gone.add(z)
    return width


def sprinkler_network() -> Tuple[List[Factor], List[int]]:
    """The cloudy, sprinkler, rain, wet grass network: C=0, S=1, R=2, W=3."""
    from fractions import Fraction as F
    card = [2, 2, 2, 2]
    pc = Factor((0,), {(0,): F(1, 2), (1,): F(1, 2)})
    ps1 = {0: F(1, 2), 1: F(1, 10)}
    pr1 = {0: F(1, 5), 1: F(4, 5)}
    pw1 = {(0, 0): F(0), (0, 1): F(9, 10), (1, 0): F(9, 10), (1, 1): F(99, 100)}
    ps = Factor((1, 0), {(s, c): ps1[c] if s else 1 - ps1[c] for s in (0, 1) for c in (0, 1)})
    pr = Factor((2, 0), {(r, c): pr1[c] if r else 1 - pr1[c] for r in (0, 1) for c in (0, 1)})
    pw = Factor((3, 1, 2), {(w, s, r): pw1[s, r] if w else 1 - pw1[s, r]
                            for w in (0, 1) for s in (0, 1) for r in (0, 1)})
    return [pc, ps, pr, pw], card
