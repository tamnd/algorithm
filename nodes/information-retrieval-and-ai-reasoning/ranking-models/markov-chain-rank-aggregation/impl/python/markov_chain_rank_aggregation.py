# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-chain-rank-aggregation/. The authors are listed in prov/DF298Z.jsonl.

from fractions import Fraction
from typing import Any, Hashable, Sequence

Ranking = Sequence[Hashable]


def _union(rankings: Sequence[Ranking]) -> list[Any]:
    items = set()
    for r in rankings:
        items.update(r)
    return sorted(items)


def transition_matrix(rankings: Sequence[Ranking], chain: str = "MC4", exact: bool = False) -> tuple[list[Any], list[list[Any]]]:
    """Return (items, M), where M[i][j] is the probability that the chain moves from items[i] to items[j].

    Each ranking lists distinct items, best first, and may be partial. The chains are
    MC1 to MC4 of Dwork, Kumar, Naor and Sivakumar (2001), with no teleport. With
    exact=True the entries are Fractions, else floats.
    """
    one = Fraction(1) if exact else 1.0
    items = _union(rankings)  # @line L1
    n = len(items)
    idx = {x: i for i, x in enumerate(items)}
    pos = [{x: i + 1 for i, x in enumerate(r)} for r in rankings]
    m = [[0 * one for _ in range(n)] for _ in range(n)]
    for p in items:  # @line L2
        i = idx[p]
        lists_p = [t for t in pos if p in t]
        if chain == "MC1":
            pool = [q for t in lists_p for q in t if t[q] <= t[p]]
            for q in pool:
                m[i][idx[q]] += one / len(pool)
        elif chain == "MC2":
            for t in lists_p:
                above = [q for q in t if t[q] <= t[p]]
                for q in above:
                    m[i][idx[q]] += one / len(lists_p) / len(above)
        elif chain == "MC3":
            for t in lists_p:
                for q in t:
                    target = q if t[q] < t[p] else p
                    m[i][idx[target]] += one / len(lists_p) / len(t)
        elif chain == "MC4":
            for q in items:
                both = [t for t in pos if p in t and q in t]
                wins = sum(1 for t in both if t[q] < t[p])
                target = q if q != p and 2 * wins > len(both) else p
                m[i][idx[target]] += one / n
        else:
            raise ValueError("chain must be MC1, MC2, MC3 or MC4")
    return items, m


def teleport(m: list[list[Any]], eps: Any) -> list[list[Any]]:
    """Return (1 - eps) M + eps J / n, the chain that jumps to a uniform state with probability eps."""
    n = len(m)
    return [[(1 - eps) * m[i][j] + eps / n for j in range(n)] for i in range(n)]  # @line L3


def stationary(m: list[list[float]], tol: float = 1e-12, max_iter: int = 100000) -> list[float]:
    """Power iteration from the uniform distribution, until the L1 change is below tol."""
    n = len(m)
    pi = [1.0 / n] * n  # @line L4
    for _ in range(max_iter):
        new = [sum(pi[i] * m[i][j] for i in range(n)) for j in range(n)]  # @line L5
        if sum(abs(a - b) for a, b in zip(new, pi)) < tol:
            return new
        pi = new
    return pi


def aggregate(rankings: Sequence[Ranking], chain: str = "MC4", eps: float = 0.15) -> list[Any]:
    """Rank the items of the union by the stationary probability of the chain, high first, ties by item.

    The probabilities are rounded to 10 decimals before the sort, so that two states with
    the same exact probability are not split by rounding noise of the power iteration.
    """
    items, m = transition_matrix(rankings, chain)
    pi = stationary(teleport(m, eps) if eps > 0 else m)
    order = sorted(range(len(items)), key=lambda i: (-round(pi[i], 10), items[i]))  # @line L6
    return [items[i] for i in order]


def _prefers(pos: Sequence[dict], x: Hashable, y: Hashable) -> bool:
    over = sum(1 for t in pos if x in t and y in t and t[x] < t[y])
    under = sum(1 for t in pos if x in t and y in t and t[y] < t[x])
    return over > under


def prefers(rankings: Sequence[Ranking], x: Hashable, y: Hashable) -> bool:
    """True when strictly more of the rankings that hold both x and y put x above y than y above x."""
    return _prefers([{z: i for i, z in enumerate(r)} for r in rankings], x, y)


def local_kemenize(order: Sequence[Hashable], rankings: Sequence[Ranking]) -> list[Any]:
    """Insertion sort of order where an item moves up past its upper neighbour only when a strict majority prefers it."""
    pos = [{z: i for i, z in enumerate(r)} for r in rankings]
    out: list[Any] = []
    for x in order:  # @line L7
        out.append(x)
        j = len(out) - 1
        while j > 0 and _prefers(pos, out[j], out[j - 1]):  # @line L8
            out[j - 1], out[j] = out[j], out[j - 1]  # @line L9
            j -= 1
    return out
