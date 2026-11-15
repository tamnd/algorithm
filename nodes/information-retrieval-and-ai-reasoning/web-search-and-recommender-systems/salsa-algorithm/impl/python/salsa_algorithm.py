# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/salsa-algorithm/. The authors are listed in prov/XD0VVF.jsonl.
"""SALSA of Lempel and Moran (WWW9 2000, ACM TOIS 2001), unweighted.

Pages are the integers 0 to n - 1 and an edge (q, p) is a link from q to p.
Self links are removed and repeated links count once. A page with an
out-link is a hub, a page with an in-link is an authority, and a page can
be both. The scores are the stationary distributions of two Markov chains
on the bipartite graph of hubs and authorities, started from the uniform
distribution on each side.
"""

from fractions import Fraction
from typing import Iterable

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


def degrees(n: int, arcs: list[tuple[int, int]]) -> tuple[list[int], list[int]]:
    out, inn = [0] * n, [0] * n
    for q, p in arcs:
        out[q] += 1
        inn[p] += 1
    return out, inn


def salsa(n: int, edges: Iterable[tuple[int, int]], exact: bool = False) -> tuple[list[Number], list[Number]]:
    """Return (hub scores, authority scores) by the closed form of Lempel and Moran.

    A page that is not a hub has hub score 0, and one that is not an authority
    has authority score 0. With exact=True the scores are Fractions.
    """
    arcs = clean_links(n, edges)  # @line L1
    out, inn = degrees(n, arcs)
    hubs = [q for q in range(n) if out[q] > 0]  # @line L2
    auths = [p for p in range(n) if inn[p] > 0]
    # The bipartite graph has 2n sides: hub q is node q and authority p is node n + p.
    adj: list[list[int]] = [[] for _ in range(2 * n)]
    for q, p in arcs:
        adj[q].append(n + p)
        adj[n + p].append(q)
    label = [-1] * (2 * n)  # @line L3
    for start in range(2 * n):
        if label[start] >= 0 or not adj[start]:
            continue
        label[start] = start
        stack = [start]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if label[w] < 0:
                    label[w] = start
                    stack.append(w)
    nh: dict[int, int] = {}  # @line L4
    na: dict[int, int] = {}
    ne: dict[int, int] = {}
    for q in hubs:
        nh[label[q]] = nh.get(label[q], 0) + 1
    for p in auths:
        na[label[n + p]] = na.get(label[n + p], 0) + 1
    for q, _ in arcs:
        ne[label[q]] = ne.get(label[q], 0) + 1

    def find(x: int) -> int:
        return label[x]

    def frac(a: int, b: int) -> Number:
        return Fraction(a, b) if exact else a / b

    zero: Number = Fraction(0) if exact else 0.0
    a: list[Number] = [zero] * n
    h: list[Number] = [zero] * n
    for p in auths:  # @line L5
        c = find(n + p)
        a[p] = frac(na[c] * inn[p], len(auths) * ne[c])
    for q in hubs:  # @line L6
        c = find(q)
        h[q] = frac(nh[c] * out[q], len(hubs) * ne[c])
    return h, a  # @line L7


def authority_step(n: int, arcs: list[tuple[int, int]], x: list[Number]) -> list[Number]:
    """One step of the authority chain: back to a random hub that links to the page, then forward on a random link of that hub."""
    out, inn = degrees(n, arcs)
    y = [x[0] * 0 for _ in range(n)]
    for q, p in arcs:
        y[q] += x[p] / inn[p]
    z = [x[0] * 0 for _ in range(n)]
    for q, p in arcs:
        z[p] += y[q] / out[q]
    return z


def hub_step(n: int, arcs: list[tuple[int, int]], x: list[Number]) -> list[Number]:
    """One step of the hub chain: forward on a random link, then back to a random hub that links to that authority."""
    out, inn = degrees(n, arcs)
    y = [x[0] * 0 for _ in range(n)]
    for q, p in arcs:
        y[p] += x[q] / out[q]
    z = [x[0] * 0 for _ in range(n)]
    for q, p in arcs:
        z[q] += y[p] / inn[p]
    return z


def salsa_power(n: int, edges: Iterable[tuple[int, int]], tol: float = 1e-13, max_rounds: int = 100000) -> tuple[list[float], list[float], int]:
    """The definition: run both chains from the uniform start until no score moves by more than tol.

    Returns (hub scores, authority scores, rounds used).
    """
    arcs = clean_links(n, edges)
    out, inn = degrees(n, arcs)
    hubs = [q for q in range(n) if out[q] > 0]
    auths = [p for p in range(n) if inn[p] > 0]
    a = [1.0 / len(auths) if inn[p] else 0.0 for p in range(n)] if auths else [0.0] * n
    h = [1.0 / len(hubs) if out[q] else 0.0 for q in range(n)] if hubs else [0.0] * n
    for r in range(1, max_rounds + 1):
        a2, h2 = authority_step(n, arcs, a), hub_step(n, arcs, h)
        moved = max([abs(u - v) for u, v in zip(a, a2)] + [abs(u - v) for u, v in zip(h, h2)])
        a, h = a2, h2
        if moved <= tol:
            return h, a, r
    raise RuntimeError("no convergence")


def authority_matrix(n: int, edges: Iterable[tuple[int, int]]) -> dict[tuple[int, int], Fraction]:
    """The exact transition probabilities P_A(i, j) of the authority chain, for authorities i and j."""
    arcs = clean_links(n, edges)
    out, inn = degrees(n, arcs)
    by_hub: dict[int, list[int]] = {}
    for q, p in arcs:
        by_hub.setdefault(q, []).append(p)
    pa: dict[tuple[int, int], Fraction] = {}
    for q, ps in by_hub.items():
        for i in ps:
            for j in ps:
                pa[(i, j)] = pa.get((i, j), Fraction(0)) + Fraction(1, inn[i] * out[q])
    return pa
