# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structural-causal-model/. The authors are listed in prov/ZC6AXX.jsonl.

"""A finite structural causal model, with the three rungs of Pearl's ladder
computed by exact enumeration: observation, intervention (do) and
counterfactuals by abduction, action and prediction.

Exogenous variable k takes values 0 .. len(prior[k]) - 1 with the
probabilities prior[k] (Fractions), independently. Endogenous variable v is
given by an equation (parents, noises, f): its value is
f(tuple of parent values, tuple of noise values). The equations are listed
in a causal order, so every parent of v has a smaller index.
"""

import itertools
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable


@dataclass
class Equation:
    parents: list[int]
    noises: list[int]
    f: Callable[[tuple, tuple], int]


@dataclass
class SCM:
    prior: list[list[Fraction]]
    eqs: list[Equation]

    def __post_init__(self):
        for v, e in enumerate(self.eqs):
            if any(p >= v for p in e.parents):
                raise ValueError("equations must be listed in a causal order")

    def solve(self, u: tuple, do: dict[int, int] | None = None) -> tuple:
        """The unique solution for the noise values u, with the equations of `do` replaced by constants."""
        do = do or {}
        x: list[int] = []
        for v, e in enumerate(self.eqs):
            if v in do:
                x.append(do[v])
            else:
                x.append(e.f(tuple(x[p] for p in e.parents), tuple(u[k] for k in e.noises)))
        return tuple(x)

    def noise_values(self):
        for u in itertools.product(*(range(len(p)) for p in self.prior)):
            pu = Fraction(1)
            for k, val in enumerate(u):
                pu *= self.prior[k][val]
            if pu:
                yield u, pu

    def distribution(self, do: dict[int, int] | None = None) -> dict[tuple, Fraction]:
        """P(V) under the model, or P(V | do(...)) under the submodel."""
        out: dict[tuple, Fraction] = {}
        for u, pu in self.noise_values():
            x = self.solve(u, do)
            out[x] = out.get(x, Fraction(0)) + pu
        return out

    def counterfactual(self, evidence: dict[int, int], do: dict[int, int]) -> dict[tuple, Fraction]:
        """P(V_do | evidence): abduction, action, prediction."""
        post: dict[tuple, Fraction] = {}
        for u, pu in self.noise_values():          # abduction: P(u | evidence)
            x = self.solve(u)
            if all(x[v] == val for v, val in evidence.items()):
                post[u] = pu
        z = sum(post.values())
        if z == 0:
            raise ValueError("the evidence has probability zero")
        out: dict[tuple, Fraction] = {}
        for u, pu in post.items():
            x = self.solve(u, do)                  # action, then prediction
            out[x] = out.get(x, Fraction(0)) + pu / z
        return out

    def graph(self) -> tuple[set[tuple[int, int]], set[frozenset[int]]]:
        """The induced graph: directed edges parent -> child, and a bidirected edge for each shared noise."""
        directed = {(p, v) for v, e in enumerate(self.eqs) for p in e.parents}
        bidirected = {frozenset((a, b)) for a, b in itertools.combinations(range(len(self.eqs)), 2)
                      if set(self.eqs[a].noises) & set(self.eqs[b].noises)}
        return directed, bidirected


def prob(pj: dict[tuple, Fraction], event: dict[int, int], given: dict[int, int] | None = None) -> Fraction:
    """P(event | given) from a joint over value tuples."""
    given = given or {}
    num = sum((p for x, p in pj.items() if all(x[v] == a for v, a in {**given, **event}.items())), Fraction(0))
    den = sum((p for x, p in pj.items() if all(x[v] == a for v, a in given.items())), Fraction(0))
    return num / den
