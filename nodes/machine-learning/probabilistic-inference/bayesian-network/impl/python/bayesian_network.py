# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-network/. The authors are listed in prov/BFMEF2.jsonl.

"""A discrete Bayesian network: a DAG with one CPT per node.

The joint probability of a full assignment is the product of one CPT
entry per node. Queries P(X = x | evidence) are answered exactly by
enumerating all assignments, which costs O(n * prod of cardinalities)
and is meant for small networks and for checking faster methods.
"""

from fractions import Fraction
from itertools import product
from typing import Dict, Iterable, List, Sequence, Tuple

Assignment = Dict[str, int]


class BayesianNetwork:
    def __init__(self, card: Dict[str, int], parents: Dict[str, Sequence[str]], cpt: Dict[str, Dict[Tuple[int, ...], Sequence[Fraction]]]):
        """card[v]: number of values of v; parents[v]: ordered parent list;
        cpt[v][u]: the distribution of v given parent values u (a row)."""
        self.card = dict(card)
        self.parents = {v: list(parents.get(v, [])) for v in card}
        self.cpt = cpt
        self.order = self._topological_order()
        for v in self.order:
            for u in product(*(range(self.card[p]) for p in self.parents[v])):
                row = cpt[v][u]
                if len(row) != self.card[v] or min(row) < 0 or sum(row) != 1:
                    raise ValueError(f"bad CPT row for {v} at {u}")

    def _topological_order(self) -> List[str]:
        order, state = [], {}

        def visit(v: str) -> None:
            if state.get(v) == 1:
                raise ValueError("the graph has a directed cycle")
            if state.get(v) == 2:
                return
            state[v] = 1
            for p in self.parents[v]:
                visit(p)
            state[v] = 2
            order.append(v)

        for v in sorted(self.card):
            visit(v)
        return order

    def free_parameters(self) -> int:
        """sum over nodes of (r_i - 1) * product of parent cardinalities."""
        total = 0
        for v in self.card:
            q = 1
            for p in self.parents[v]:
                q *= self.card[p]
            total += (self.card[v] - 1) * q
        return total

    def joint(self, x: Assignment) -> Fraction:
        p = Fraction(1)
        for v in self.order:
            u = tuple(x[q] for q in self.parents[v])
            p *= self.cpt[v][u][x[v]]
        return p

    def assignments(self) -> Iterable[Assignment]:
        names = self.order
        for vals in product(*(range(self.card[v]) for v in names)):
            yield dict(zip(names, vals))

    def probability(self, event: Assignment) -> Fraction:
        """P(event) for a partial assignment, by summing the joint."""
        return sum((self.joint(x) for x in self.assignments() if all(x[k] == v for k, v in event.items())), Fraction(0))

    def query(self, var: str, evidence: Assignment) -> List[Fraction]:
        """Posterior distribution of var given evidence, by enumeration."""
        weights = [Fraction(0)] * self.card[var]
        for x in self.assignments():
            if all(x[k] == v for k, v in evidence.items()):
                weights[x[var]] += self.joint(x)
        z = sum(weights)
        if z == 0:
            raise ValueError("the evidence has probability 0")
        return [w / z for w in weights]

    def descendants(self, v: str) -> set:
        children = {u: [w for w in self.card if u in self.parents[w]] for u in self.card}
        out, stack = set(), [v]
        while stack:
            for c in children[stack.pop()]:
                if c not in out:
                    out.add(c)
                    stack.append(c)
        return out
