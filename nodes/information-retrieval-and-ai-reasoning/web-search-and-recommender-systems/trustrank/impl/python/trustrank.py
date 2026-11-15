# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trustrank/. The authors are listed in prov/Y8VX0X.jsonl.
"""TrustRank of Gyongyi, Garcia-Molina and Pedersen (VLDB 2004).

Pages are the integers 0 to n - 1. An edge (q, p) is a link from q to p.
Self links are removed and repeated links count once, as in the paper.
The transition matrix is T[p][q] = 1 / out(q) for each link (q, p), so a
page with no out-link passes no trust on and its trust leaks away.
"""

from fractions import Fraction
from typing import Callable, Iterable, Sequence

Number = float | Fraction


def clean_links(n: int, edges: Iterable[tuple[int, int]]) -> list[tuple[int, int]]:
    """Distinct links (q, p) with q != p, sorted."""
    arcs = set()
    for q, p in edges:
        if not (0 <= q < n and 0 <= p < n):
            raise ValueError("page out of range")
        if q != p:
            arcs.add((q, p))
    return sorted(arcs)


def biased_pagerank(n: int, edges: Iterable[tuple[int, int]], d: Sequence[Number], alpha: Number = 0.85, rounds: int = 20) -> list[Number]:
    """Start from t = d and apply t <- alpha T t + (1 - alpha) d for the given number of rounds.

    Works with floats, or exactly with Fraction values of alpha and d.
    """
    arcs = clean_links(n, edges)
    out = [0] * n
    for q, _ in arcs:
        out[q] += 1
    t = list(d)  # @line L5
    for _ in range(rounds):  # @line L6
        new = [(1 - alpha) * d[p] for p in range(n)]
        for q, p in arcs:
            new[p] += alpha * t[q] / out[q]
        t = new
    return t


def inverse_pagerank(n: int, edges: Iterable[tuple[int, int]], alpha: Number = 0.85, rounds: int = 20) -> list[Number]:
    """PageRank on the graph with every link reversed, with the uniform jump vector."""
    rev = [(p, q) for q, p in clean_links(n, edges)]
    one = Fraction(1, n) if isinstance(alpha, Fraction) else 1.0 / n
    return biased_pagerank(n, rev, [one] * n, alpha, rounds)


def select_seeds(scores: Sequence[Number], oracle: Callable[[int], bool], limit: int) -> list[int]:
    """The pages among the top `limit` by score (ties: smaller page first) that the oracle calls good."""
    order = sorted(range(len(scores)), key=lambda p: (-scores[p], p))  # @line L2
    return [p for p in order[:limit] if oracle(p)]  # @line L3


def seed_vector(n: int, seeds: Sequence[int], exact: bool = False) -> list[Number]:
    """The vector d with d(p) = 1 / |seeds| on each seed and 0 elsewhere."""
    if not seeds:
        raise ValueError("no good seed page")
    w: Number = Fraction(1, len(seeds)) if exact else 1.0 / len(seeds)  # @line L4
    zero: Number = Fraction(0) if exact else 0.0
    d = [zero] * n
    for s in seeds:
        d[s] = w
    return d


def trustrank(n: int, edges: Sequence[tuple[int, int]], oracle: Callable[[int], bool], limit: int, alpha: float = 0.85, rounds: int = 20, seed_alpha: float = 0.85, seed_rounds: int = 20) -> tuple[list[float], list[int]]:
    """Return (trust scores, good seeds) as in Figure 5 of the paper."""
    s = inverse_pagerank(n, edges, seed_alpha, seed_rounds)  # @line L1
    seeds = select_seeds(s, oracle, limit)
    d = seed_vector(n, seeds)
    return biased_pagerank(n, edges, d, alpha, rounds), seeds  # @line L7


def _solve(a: list[list[Fraction]], b: list[Fraction]) -> list[Fraction]:
    """Solve a x = b exactly by Gaussian elimination with Fraction entries."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        piv = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def trustrank_exact(n: int, edges: Iterable[tuple[int, int]], seeds: Sequence[int], alpha: Fraction = Fraction(17, 20)) -> list[Fraction]:
    """The fixed point t = alpha T t + (1 - alpha) d, from (I - alpha T) t = (1 - alpha) d."""
    arcs = clean_links(n, edges)
    out = [0] * n
    for q, _ in arcs:
        out[q] += 1
    a = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for q, p in arcs:
        a[p][q] -= alpha / out[q]
    d = seed_vector(n, seeds, exact=True)
    return _solve(a, [(1 - alpha) * x for x in d])
