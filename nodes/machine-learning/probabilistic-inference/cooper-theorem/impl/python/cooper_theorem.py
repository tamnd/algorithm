# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cooper-theorem/. The authors are listed in prov/RAWF2P.jsonl.

"""The reduction of Cooper's theorem: a Bayesian network for a 3-CNF formula.

A formula has variables 0 .. n-1 and clauses; a clause is a list of at most
three literals (v, positive). The network has binary nodes in this order:

  Q_0 .. Q_{n-1}   roots, P(Q_i = 1) = 1/2
  C_1 .. C_m       C_j = 1 exactly when clause j is true (parents: its variables)
  A_1 .. A_m       A_1 = C_1, A_j = A_{j-1} and C_j (parents: A_{j-1}, C_j)

The output is A_m. Every node has at most three parents and every table has
entries 0, 1/2 or 1, so the network has size O(n + m). Then
P(A_m = 1) = (number of satisfying assignments) / 2^n, which is positive
exactly when the formula is satisfiable.
"""

from fractions import Fraction
from itertools import product
from typing import Dict, List, NamedTuple, Sequence, Tuple

Clause = Sequence[Tuple[int, bool]]


class Node(NamedTuple):
    parents: Tuple[int, ...]
    cpt: Dict[Tuple[int, ...], Fraction]  # P(node = 1 | parent values)


def cooper_network(n: int, clauses: Sequence[Clause]) -> Tuple[List[Node], int]:
    """The network of the reduction and the index of its output node."""
    if not clauses:
        raise ValueError("the formula needs at least one clause")
    nodes = [Node((), {(): Fraction(1, 2)}) for _ in range(n)]
    for cl in clauses:
        if not 1 <= len(cl) <= 3 or len({v for v, _ in cl}) != len(cl):
            raise ValueError("a clause has one to three literals on distinct variables")
        pa = tuple(v for v, _ in cl)
        signs = [pos for _, pos in cl]
        cpt = {a: Fraction(int(any(bool(x) == s for x, s in zip(a, signs)))) for a in product((0, 1), repeat=len(pa))}
        nodes.append(Node(pa, cpt))
    m = len(clauses)
    nodes.append(Node((n,), {(0,): Fraction(0), (1,): Fraction(1)}))  # A_1 = C_1
    for j in range(1, m):
        a_prev, c_j = n + m + j - 1, n + j
        nodes.append(Node((a_prev, c_j), {(x, y): Fraction(x & y) for x in (0, 1) for y in (0, 1)}))
    return nodes, len(nodes) - 1


def probability(nodes: Sequence[Node], var: int, val: int) -> Fraction:
    """P(var = val) as the sum of P(x) over all joint assignments x, done depth first
    in the topological order of the nodes; a prefix of probability 0 is skipped,
    because all its extensions have probability 0."""
    total = Fraction(0)
    k = len(nodes)
    stack: List[Tuple[Tuple[int, ...], Fraction]] = [((), Fraction(1))]  # (prefix, its probability)
    while stack:
        x, p = stack.pop()
        if len(x) == k:
            if x[var] == val:
                total += p
            continue
        node = nodes[len(x)]
        q = node.cpt[tuple(x[u] for u in node.parents)]
        for b, pb in ((1, q), (0, 1 - q)):
            if pb != 0:
                stack.append((x + (b,), p * pb))
    return total


def count_models(n: int, clauses: Sequence[Clause]) -> int:
    """The number of satisfying assignments, by trying all 2^n."""
    return sum(all(any(bool(q[v]) == pos for v, pos in cl) for cl in clauses) for q in product((0, 1), repeat=n))
