# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/israeli-itai/. The authors are listed in prov/NSTYXT.jsonl.

"""Israeli-Itai maximal matching, simulated round by round.

In each round every vertex with an edge proposes to a random neighbour, every
vertex keeps one of the proposals it got, and the kept edges form a graph of
largest degree 2. Each vertex then picks one of its kept edges at random, and
an edge picked by both its ends joins the matching. Matched vertices leave
with their edges.

Precondition: edges is a list of pairs (u, v) with 0 <= u, v < n. Self-loops
are ignored and parallel edges count once.
Cost: a round with n_t vertices of positive degree and m_t edges costs
O(n_t + m_t) work and O(log n) span. A constant fraction of the edges leaves
in each round in expectation, so the expected work is O(n + m) and the number
of rounds is O(log n) with high probability.
"""

import math
import random

Script = list[tuple[dict[int, int], dict[int, int], dict[int, int]]]


class Cost:
    """Counters for work, span, rounds, and the number of edges at the start of each round."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.rounds = 0
        self.edges: list[int] = []


def israeli_itai(
    n: int,
    edges: list[tuple[int, int]],
    rng: random.Random | None = None,
    cost: Cost | None = None,
    script: Script | None = None,
) -> list[tuple[int, int]]:
    """Return a maximal matching as a sorted list of pairs (u, v) with u < v.

    If script is given, round t uses script[t] = (propose, accept, pick) instead of
    random choices: propose[v] is the neighbour v proposes to, accept[v] the proposer
    v keeps, and pick[v] the other end of the kept edge v picks.
    """
    rng = rng if rng is not None else random.Random(0)
    c = cost if cost is not None else Cost()
    lg = max(1, math.ceil(math.log2(n + 1)))
    nb: list[set[int]] = [set() for _ in range(n)]
    for u, v in edges:
        if u != v:
            nb[u].add(v)
            nb[v].add(u)
    adj = [sorted(s) for s in nb]
    matching: list[tuple[int, int]] = []  # @line L1
    live = [v for v in range(n) if adj[v]]
    c.work += n + 2 * len(edges)
    c.span += lg
    while live:  # @line L2 (while some edge remains)
        n_t = len(live)
        m_t = sum(len(adj[v]) for v in live) // 2
        c.edges.append(m_t)
        if script is not None:
            propose, accept, pick = script[c.rounds]
        else:
            propose = {v: rng.choice(adj[v]) for v in live}  # @line L3
            got: dict[int, list[int]] = {}
            for v in live:
                got.setdefault(propose[v], []).append(v)
            accept = {u: rng.choice(ps) for u, ps in got.items()}  # @line L4 (any one will do)
        h: dict[int, set[int]] = {}
        for u, v in accept.items():  # @line L5 (the kept edges, largest degree 2)
            h.setdefault(u, set()).add(v)
            h.setdefault(v, set()).add(u)
        if script is None:
            pick = {v: rng.choice(sorted(h[v])) for v in h}  # @line L6
        new = [(min(v, w), max(v, w)) for v, w in pick.items() if v < w and pick.get(w) == v]  # @line L7
        matching.extend(new)
        gone = {x for e in new for x in e}
        for v in live:  # @line L8 (remove the matched vertices and their edges, then pack)
            adj[v] = [] if v in gone else [u for u in adj[v] if u not in gone]
        live = [v for v in live if adj[v]]
        c.rounds += 1
        c.work += 4 * n_t + 6 * m_t + len(h)
        c.span += 4 * lg
    return sorted(matching)  # @line L9
