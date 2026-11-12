# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/map-inference/. The authors are listed in prov/VQER59.jsonl.

"""Reference solvers for the two MAP problems, by enumeration.

A model is a list of factors over the variables 0 .. n-1, where variable v takes
the values 0 .. card[v]-1. A factor is a scope (a tuple of variables) and a
table from assignments of the scope to nonnegative numbers.

  mpe          most probable explanation: maximize the product over all the
               variables that are not observed (NP-hard, Shimony 1994)
  marginal_map maximize over a set M of variables the sum of the product over
               the other unobserved variables (NP^PP-complete, Park and
               Darwiche 2004)

Both take time O(d^n) times the number of factors. They are exact and are meant
for small models and as a test oracle for the fast methods on trees.
"""

from itertools import product
from typing import Dict, NamedTuple, Optional, Sequence, Tuple

Assignment = Tuple[int, ...]


class Factor(NamedTuple):
    scope: Tuple[int, ...]
    table: Dict[Assignment, object]


def value(factors: Sequence[Factor], x: Sequence[int]) -> object:
    """The product of the factors at the full assignment x."""
    w = 1
    for f in factors:
        w = w * f.table[tuple(x[v] for v in f.scope)]
    return w


def _agree(x: Sequence[int], evidence: Dict[int, int]) -> bool:
    return all(x[v] == val for v, val in evidence.items())


def mpe(factors: Sequence[Factor], card: Sequence[int],
        evidence: Dict[int, int]) -> Tuple[Assignment, object]:
    """An assignment of all the variables that agrees with the evidence and has the
    largest product, and that product. Ties go to the smallest assignment in
    lexicographic order. Raises ValueError if every such assignment has value 0."""
    best: Optional[Assignment] = None
    best_w = None
    for x in product(*(range(c) for c in card)):
        if _agree(x, evidence):
            w = value(factors, x)
            if best_w is None or w > best_w:
                best, best_w = x, w
    if best is None or best_w == 0:
        raise ValueError("the evidence has probability zero")
    return best, best_w


def marginal_map(factors: Sequence[Factor], card: Sequence[int], query: Sequence[int],
                 evidence: Dict[int, int]) -> Tuple[Assignment, object]:
    """Values for the query variables that maximize the sum of the product over all
    the other unobserved variables, and that sum. Keys follow the order of query."""
    sums: Dict[Assignment, object] = {}
    for x in product(*(range(c) for c in card)):
        if _agree(x, evidence):
            key = tuple(x[q] for q in query)
            sums[key] = sums.get(key, 0) + value(factors, x)
    best = min(sums, key=lambda k: (-sums[k], k))
    if sums[best] == 0:
        raise ValueError("the evidence has probability zero")
    return best, sums[best]


def posterior_marginal_decoding(factors: Sequence[Factor], card: Sequence[int],
                                evidence: Dict[int, int]) -> Assignment:
    """For contrast: each variable alone takes its most probable value given e."""
    return tuple(marginal_map(factors, card, [v], evidence)[0][0] for v in range(len(card)))
