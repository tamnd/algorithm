# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reed-frost-model/. The authors are listed in prov/PA1DQR.jsonl.
"""The Reed-Frost chain binomial epidemic and the Greenwood variant.

The state after generation t is (S_t, I_t): the number of susceptibles and
the number of new cases of generation t. A case is infectious for exactly
one generation and is then removed. Each susceptible escapes each case of
the generation independently with probability q = 1 - p, so it is infected
with probability 1 - q^I_t (Reed-Frost) or p whenever I_t > 0 (Greenwood).

The exact functions take p as a float or a fractions.Fraction. With Fraction
input they are exact.
"""

from __future__ import annotations

from itertools import combinations
from math import comb
from typing import Dict, List, Tuple

from biostoch import binomial


def infection_probability(p, i: int, greenwood: bool = False):
    """The chance that one susceptible is infected by a generation of i cases."""
    if i == 0:
        return 0 * p
    if greenwood:
        return p
    return 1 - (1 - p) ** i


def simulate(rng, s0: int, i0: int, p: float,
             greenwood: bool = False) -> List[Tuple[int, int]]:
    """One epidemic as the list of states (S_t, I_t), t = 0, 1, ...

    The list ends at the first generation with no new cases. Draw order: one
    biostoch.binomial draw per generation.
    """
    s, i = s0, i0  # @line L1
    path = [(s, i)]  # @line L2
    while i > 0:  # @line L3
        pi = infection_probability(float(p), i, greenwood)  # @line L4
        c = binomial(rng, s, pi)  # @line L5
        s, i = s - c, c  # @line L6
        path.append((s, i))  # @line L7
    return path  # @line L8


def final_size(path: List[Tuple[int, int]]) -> int:
    """The number of people infected after generation 0: S_0 - S_end."""
    return path[0][0] - path[-1][0]


def chain_probability(chain: List[int], s0: int, p, greenwood: bool = False):
    """P(I_0, I_1, ..., I_T = chain), the last entry being 0, given S_0 = s0.

    This is the product of the binomial terms C(S_t, I_(t+1)) pi^I_(t+1)
    (1 - pi)^S_(t+1), with pi = infection_probability(p, I_t).
    """
    if chain[-1] != 0:
        raise ValueError("a complete chain ends with 0")
    prob = 1 + 0 * p
    s = s0
    for t in range(len(chain) - 1):
        i, c = chain[t], chain[t + 1]
        if c > s:
            return 0 * p
        pi = infection_probability(p, i, greenwood)
        prob *= comb(s, c) * pi ** c * (1 - pi) ** (s - c)
        s -= c
    return prob


def final_size_distribution(s0: int, i0: int, p, greenwood: bool = False) -> Dict[int, object]:
    """The exact law of the final size, by a pass over the states (S, I).

    Each generation either ends the epidemic (no new cases) or lowers S, so
    the loop runs at most s0 + 1 times.
    """
    one = 1 + 0 * p
    live = {(s0, i0): one}
    out: Dict[int, object] = {}
    while live:
        nxt: Dict[Tuple[int, int], object] = {}
        for (s, i), w in live.items():
            if i == 0:
                out[s0 - s] = out.get(s0 - s, 0 * p) + w
                continue
            pi = infection_probability(p, i, greenwood)
            for c in range(s + 1):
                term = w * comb(s, c) * pi ** c * (1 - pi) ** (s - c)
                key = (s - c, c)
                nxt[key] = nxt.get(key, 0 * p) + term
        live = nxt
    return dict(sorted(out.items()))


def chains_by_graphs(s0: int, i0: int, p) -> Dict[Tuple[int, ...], object]:
    """The law of the chain (I_0, I_1, ...) by summing over all random graphs.

    Each of the C(n, 2) pairs of the n = s0 + i0 people is an edge with
    probability p. The cases of generation t are the people at graph
    distance t from the i0 initial cases, so the chain is the list of the
    sizes of the breadth-first layers. Use only for n <= 6.
    """
    n = s0 + i0
    pairs = list(combinations(range(n), 2))
    out: Dict[Tuple[int, ...], object] = {}
    for mask in range(1 << len(pairs)):
        adj = [[] for _ in range(n)]
        k = 0
        for b, (u, v) in enumerate(pairs):
            if mask >> b & 1:
                adj[u].append(v)
                adj[v].append(u)
                k += 1
        w = p ** k * (1 - p) ** (len(pairs) - k)
        seen = set(range(i0))
        layer = list(range(i0))
        chain = [i0]
        while layer:
            new = []
            for u in layer:
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v)
                        new.append(v)
            chain.append(len(new))
            layer = new
        key = tuple(chain)
        out[key] = out.get(key, 0 * p) + w
    return out
