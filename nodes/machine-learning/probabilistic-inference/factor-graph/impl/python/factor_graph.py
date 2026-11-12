# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/factor-graph/. The authors are listed in prov/XJS0S3.jsonl.

"""Factor graphs over discrete variables.

A factor graph is a bipartite graph with one node per variable and one
node per factor; a factor is joined to the variables it depends on. It
represents g(x) = prod_a f_a(x_{N(a)}). The module stores the graph,
computes g, Z and marginals by brute force, converts a Bayesian network
or a Markov random field into a factor graph, and runs the sum-product
algorithm, which is exact when the factor graph is a tree.
"""

from fractions import Fraction
from itertools import product
from typing import Dict, List, Sequence, Tuple

Table = Dict[Tuple[int, ...], Fraction]


class FactorGraph:
    def __init__(self) -> None:
        self.card: Dict[str, int] = {}
        self.factors: Dict[str, Tuple[Tuple[str, ...], Table]] = {}

    def add_variable(self, name: str, card: int) -> None:
        if name in self.card or name in self.factors:
            raise ValueError(f"duplicate node {name}")
        self.card[name] = card

    def add_factor(self, name: str, scope: Sequence[str], table: Table) -> None:
        if name in self.card or name in self.factors:
            raise ValueError(f"duplicate node {name}")
        scope = tuple(scope)
        for v in scope:
            if v not in self.card:
                raise ValueError(f"unknown variable {v}")
        for vals in product(*(range(self.card[v]) for v in scope)):
            if table[vals] < 0:
                raise ValueError("factor values must be nonnegative")
        self.factors[name] = (scope, dict(table))

    # the bipartite graph
    def neighbors(self, node: str) -> List[str]:
        if node in self.factors:
            return list(self.factors[node][0])
        return [a for a, (scope, _) in self.factors.items() if node in scope]

    def edges(self) -> List[Tuple[str, str]]:
        return [(a, v) for a, (scope, _) in self.factors.items() for v in scope]

    def is_tree(self) -> bool:
        nodes = list(self.card) + list(self.factors)
        if len(self.edges()) != len(nodes) - 1:
            return False
        seen, stack = {nodes[0]}, [nodes[0]]
        while stack:
            for w in self.neighbors(stack.pop()):
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        return len(seen) == len(nodes)

    # brute force
    def variables(self) -> List[str]:
        return sorted(self.card)

    def assignments(self):
        names = self.variables()
        for vals in product(*(range(self.card[v]) for v in names)):
            yield dict(zip(names, vals))

    def value(self, x: Dict[str, int]) -> Fraction:
        g = Fraction(1)
        for scope, table in self.factors.values():
            g *= table[tuple(x[v] for v in scope)]
        return g

    def partition_function(self) -> Fraction:
        return sum((self.value(x) for x in self.assignments()), Fraction(0))

    def joint(self) -> Dict[Tuple[int, ...], Fraction]:
        z = self.partition_function()
        names = self.variables()
        return {tuple(x[v] for v in names): self.value(x) / z for x in self.assignments()}

    def brute_force_marginal(self, var: str) -> List[Fraction]:
        m = [Fraction(0)] * self.card[var]
        for x in self.assignments():
            m[x[var]] += self.value(x)
        z = sum(m)
        return [v / z for v in m]

    # sum-product
    def sum_product_marginals(self) -> Dict[str, List[Fraction]]:
        """Exact marginals on a tree factor graph by message passing.

        Variable to factor: product of the messages from the other factors.
        Factor to variable: sum over the other variables of the factor times
        the messages from those variables. Each message is computed once.
        """
        if not self.is_tree():
            raise ValueError("sum-product is exact only on a tree; this graph has a cycle or is disconnected")
        memo: Dict[Tuple[str, str], List[Fraction]] = {}

        def message(src: str, dst: str) -> List[Fraction]:
            key = (src, dst)
            if key in memo:
                return memo[key]
            if src in self.card:  # variable -> factor
                out = [Fraction(1)] * self.card[src]
                for a in self.neighbors(src):
                    if a != dst:
                        m = message(a, src)
                        out = [p * q for p, q in zip(out, m)]
            else:  # factor -> variable
                scope, table = self.factors[src]
                others = [(i, v) for i, v in enumerate(scope) if v != dst]
                incoming = {v: message(v, src) for _, v in others}
                out = [Fraction(0)] * self.card[dst]
                for vals in product(*(range(self.card[v]) for v in scope)):
                    w = table[vals]
                    if w:
                        for i, v in others:
                            w *= incoming[v][vals[i]]
                        out[vals[scope.index(dst)]] += w
            memo[key] = out
            return out

        result = {}
        for v in self.card:
            b = [Fraction(1)] * self.card[v]
            for a in self.neighbors(v):
                b = [p * q for p, q in zip(b, message(a, v))]
            z = sum(b)
            result[v] = [p / z for p in b]
        return result


def from_bayesian_network(card: Dict[str, int], parents: Dict[str, Sequence[str]], cpt: Dict[str, Dict[Tuple[int, ...], Sequence[Fraction]]]) -> FactorGraph:
    """One factor per node: f_i(x_i, x_pa(i)) = p(x_i | x_pa(i))."""
    fg = FactorGraph()
    for v, r in card.items():
        fg.add_variable(v, r)
    for v in card:
        pa = list(parents.get(v, []))
        table = {}
        for u in product(*(range(card[p]) for p in pa)):
            for xv in range(card[v]):
                table[(xv,) + u] = Fraction(cpt[v][u][xv])
        fg.add_factor("p(" + v + ")", [v] + pa, table)
    return fg


def from_markov_random_field(card: Dict[str, int], potentials: Sequence[Tuple[Sequence[str], Table]]) -> FactorGraph:
    """One factor per clique potential."""
    fg = FactorGraph()
    for v, r in card.items():
        fg.add_variable(v, r)
    for k, (scope, table) in enumerate(potentials):
        fg.add_factor(f"psi{k}", scope, table)
    return fg
