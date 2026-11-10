# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ranking-algorithm/. The authors are listed in prov/NV7H45.jsonl.

import itertools
import math
import random
from collections.abc import Hashable, Iterable, Sequence
from fractions import Fraction

Match = list[Hashable | None]


class Ranking:
    """The Ranking algorithm of Karp, Vazirani and Vazirani for online bipartite matching.

    `rank` maps each offline vertex to its rank (a smaller value comes first).
    It is fixed before the first arrival. Call `arrive` once per online vertex.
    """

    def __init__(self, rank: dict[Hashable, float]) -> None:
        self.rank = dict(rank)
        self.free = set(self.rank)  # @line L2
        self.match: Match = []

    def arrive(self, neighbours: Iterable[Hashable]) -> Hashable | None:  # @line L4
        """Match one online vertex to its free neighbour of smallest rank."""
        cand = [u for u in neighbours if u in self.free]  # @line L5
        partner = None
        if cand:  # @line L6
            partner = min(cand, key=self.rank.__getitem__)  # @line L7
            self.free.remove(partner)  # @line L8
        self.match.append(partner)
        return partner


def ranking_with_order(order: Sequence[Hashable], arrivals: Sequence[Iterable[Hashable]]) -> Match:
    """Run Ranking with the offline vertices ranked in the given order."""
    r = Ranking({u: i for i, u in enumerate(order)})
    for nb in arrivals:  # @line L3
        r.arrive(nb)
    return r.match  # @line L9


def ranking(offline: Iterable[Hashable], arrivals: Sequence[Iterable[Hashable]], rng: random.Random) -> Match:
    """Run Ranking with a uniform random order drawn from rng."""
    order = list(offline)
    rng.shuffle(order)  # @line L1
    return ranking_with_order(order, arrivals)


def size(match: Match) -> int:
    return sum(1 for u in match if u is not None)


def expected_size(offline: Sequence[Hashable], arrivals: Sequence[Sequence[Hashable]]) -> Fraction:
    """Exact expected size of Ranking, by enumeration of all orders (small inputs)."""
    total = 0
    count = 0
    for order in itertools.permutations(offline):
        total += size(ranking_with_order(order, arrivals))
        count += 1
    return Fraction(total, count)


F = 1 - 1 / math.e


def g(y: float) -> float:
    """The split function of the primal-dual proof: the offline side gets g(y)/F."""
    return math.exp(y - 1)


def ranking_dual(y: dict[Hashable, float], arrivals: Sequence[Iterable[Hashable]]):
    """Run Ranking ranked by y and return (match, alpha, beta) of the proof.

    For each matched pair (u, v_t): alpha[u] = g(y_u)/F and beta[t] = (1 - g(y_u))/F.
    All other entries are 0, so sum(alpha) + sum(beta) = size(match)/F.
    """
    r = Ranking(y)
    alpha = {u: 0.0 for u in y}
    beta = []
    for nb in arrivals:
        u = r.arrive(nb)
        if u is None:
            beta.append(0.0)
        else:
            alpha[u] = g(y[u]) / F
            beta.append((1 - g(y[u])) / F)
    return r.match, alpha, beta
