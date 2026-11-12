# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conditional-probability-table/. The authors are listed in prov/FEM89D.jsonl.

"""Conditional probability tables for discrete Bayesian networks.

A CPT for a child with `card` values and parents with cardinalities
`parent_cards` stores one distribution over the child values for each
parent configuration (a row). Values are 0..card-1.
"""

from fractions import Fraction
from itertools import product
from typing import Dict, List, Sequence, Tuple


class CPT:
    def __init__(self, card: int, parent_cards: Sequence[int], rows: Dict[Tuple[int, ...], Sequence]):
        self.card = card
        self.parent_cards = tuple(parent_cards)
        self.rows = {tuple(u): list(r) for u, r in rows.items()}
        self.check()

    def configurations(self) -> List[Tuple[int, ...]]:
        return list(product(*(range(c) for c in self.parent_cards)))

    def check(self) -> None:
        for u in self.configurations():
            if u not in self.rows:
                raise ValueError(f"missing row for parent values {u}")
            row = self.rows[u]
            if len(row) != self.card or any(p < 0 for p in row):
                raise ValueError(f"bad row {u}")
            if sum(row) != 1:
                raise ValueError(f"row {u} does not sum to 1")

    def prob(self, x: int, u: Tuple[int, ...]) -> object:
        return self.rows[tuple(u)][x]

    def free_parameters(self) -> int:
        """(r - 1) times the number of parent configurations."""
        q = 1
        for c in self.parent_cards:
            q *= c
        return (self.card - 1) * q


def noisy_or(strengths: Sequence[Fraction], leak: Fraction = Fraction(0)) -> CPT:
    """Noisy-OR CPT for a binary child with k binary parents.

    strengths[j] is the probability that parent j, when on, turns the
    child on by itself; leak is the probability that the child is on with
    all parents off. P(X = 0 | u) = (1 - leak) * prod over on parents of (1 - strengths[j]).
    """
    k = len(strengths)
    rows = {}
    for u in product((0, 1), repeat=k):
        off = 1 - leak
        for j in range(k):
            if u[j]:
                off *= 1 - strengths[j]
        rows[u] = [off, 1 - off]
    return CPT(2, [2] * k, rows)


def noisy_or_by_mechanism(strengths: Sequence[Fraction], leak: Fraction, u: Tuple[int, ...]) -> Fraction:
    """P(X = 1 | u) from the causal story, by enumeration.

    Each on parent j fires an independent hidden cause with probability
    strengths[j], a leak cause fires with probability leak, and X is the OR
    of the hidden causes.
    """
    causes = [leak] + [s for s, on in zip(strengths, u) if on]
    total = Fraction(0)
    for fired in product((0, 1), repeat=len(causes)):
        p = Fraction(1)
        for f, c in zip(fired, causes):
            p *= c if f else 1 - c
        if any(fired):
            total += p
    return total


def mle_from_counts(card: int, parent_cards: Sequence[int], data: Sequence[Tuple[int, Tuple[int, ...]]], pseudo: Fraction = Fraction(0)) -> CPT:
    """Estimate a CPT from (x, u) pairs: (N(x, u) + pseudo) / (N(u) + card * pseudo).

    pseudo = 0 gives the maximum likelihood estimate; a row with no data
    and pseudo = 0 is set to uniform. pseudo > 0 is the posterior mean
    under a symmetric Dirichlet prior.
    """
    counts: Dict[Tuple[int, ...], List[int]] = {}
    for x, u in data:
        counts.setdefault(tuple(u), [0] * card)[x] += 1
    rows = {}
    for u in product(*(range(c) for c in parent_cards)):
        c = counts.get(u, [0] * card)
        n = sum(c)
        if n == 0 and pseudo == 0:
            rows[u] = [Fraction(1, card)] * card
        else:
            rows[u] = [Fraction(ci) + pseudo for ci in c]
            rows[u] = [v / (n + card * pseudo) for v in rows[u]]
    return CPT(card, parent_cards, rows)
