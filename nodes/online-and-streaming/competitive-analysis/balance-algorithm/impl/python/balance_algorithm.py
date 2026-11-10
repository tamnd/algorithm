# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balance-algorithm/. The authors are listed in prov/QHSMWD.jsonl.

import math
from collections.abc import Hashable, Iterable, Mapping, Sequence


def balance_ratio(b: int) -> float:
    """The competitive ratio 1 - (1 + 1/b)^(-b) of Balance for capacity b."""
    return 1 - (1 + 1 / b) ** (-b)


class Balance:
    """Balance (Kalyanasundaram and Pruhs) for online b-matching.

    Each offline vertex can take b online vertices. An arrival goes to a
    neighbour with load below b and the smallest load; ties go to the
    neighbour listed first. The dual of the proof is kept alongside:
    alpha[u] = A(load[u]) and beta[t] = 1 - A(load before the assignment).
    """

    def __init__(self, offline: Iterable[Hashable], b: int) -> None:
        if b < 1:
            raise ValueError("b must be at least 1")
        self.b = b
        self.load = {u: 0 for u in offline}  # @line L1
        self.match: list[Hashable | None] = []
        self.beta: list[float] = []
        r = 1 + 1 / b
        self._den = r**b - 1
        self._r = r

    def A(self, ell: int) -> float:
        """The dual price (r^ell - 1)/(r^b - 1) of an offline vertex with load ell."""
        return (self._r**ell - 1) / self._den

    def arrive(self, neighbours: Iterable[Hashable]) -> Hashable | None:  # @line L3
        """Assign one online vertex; return its partner or None. Cost O(degree)."""
        best = None
        for u in neighbours:  # @line L4
            if self.load[u] < self.b and (best is None or self.load[u] < self.load[best]):
                best = u
        if best is None:  # @line L5
            self.match.append(None)
            self.beta.append(0.0)
            return None
        self.beta.append(1 - self.A(self.load[best]))
        self.load[best] += 1  # @line L6
        self.match.append(best)  # @line L7
        return best

    def alpha(self) -> dict[Hashable, float]:
        return {u: self.A(ell) for u, ell in self.load.items()}


def balance(offline: Iterable[Hashable], b: int, arrivals: Sequence[Iterable[Hashable]]) -> Balance:
    """Run Balance on a whole arrival sequence and return the final state."""
    alg = Balance(offline, b)
    for nb in arrivals:  # @line L2
        alg.arrive(nb)
    return alg  # @line L8


def size(match: Sequence[Hashable | None]) -> int:
    return sum(1 for u in match if u is not None)


# Adwords: bids[t] maps each advertiser to its bid for query t.


def psi(f: float) -> float:
    """The MSVV tradeoff function 1 - e^(f - 1) of the spent fraction f."""
    return 1 - math.exp(f - 1)


def msvv(budgets: Mapping[Hashable, float], bids: Sequence[Mapping[Hashable, float]]):
    """MSVV for adwords: give query t to the advertiser that maximizes bid * psi(spent/budget).

    Only advertisers with budget left take part; an advertiser pays
    min(bid, budget left). Returns (assignment, revenue).
    """
    spent = {i: 0.0 for i in budgets}
    out: list[Hashable | None] = []
    for q in bids:
        best, key = None, 0.0
        for i, bid in q.items():
            if bid > 0 and spent[i] < budgets[i]:
                k = bid * psi(spent[i] / budgets[i])
                if best is None or k > key:
                    best, key = i, k
        out.append(best)
        if best is not None:
            spent[best] = min(budgets[best], spent[best] + q[best])
    return out, sum(spent.values())


def bjn_adwords(budgets: Mapping[Hashable, float], bids: Sequence[Mapping[Hashable, float]]):
    """The primal-dual adwords algorithm of Buchbinder, Jain and Naor.

    With R = max bid/budget and c = (1 + R)^(1/R), query t goes to the
    advertiser i that maximizes bid * (1 - x_i), if that is positive. Then
    z_t = bid * (1 - x_i) and x_i <- x_i (1 + bid/B_i) + bid / ((c - 1) B_i).
    Returns (assignment, revenue, x, z, c).
    """
    R = max((bid / budgets[i] for q in bids for i, bid in q.items() if bid > 0), default=1.0)
    c = (1 + R) ** (1 / R)
    x = {i: 0.0 for i in budgets}
    z: list[float] = []
    spent = {i: 0.0 for i in budgets}
    out: list[Hashable | None] = []
    for q in bids:
        best, key = None, 0.0
        for i, bid in q.items():
            k = bid * (1 - x[i])
            if k > key:
                best, key = i, k
        out.append(best)
        if best is None:
            z.append(0.0)
            continue
        bid, B = q[best], budgets[best]
        z.append(key)
        x[best] = x[best] * (1 + bid / B) + bid / ((c - 1) * B)
        spent[best] = min(B, spent[best] + bid)
    return out, sum(spent.values()), x, z, c
