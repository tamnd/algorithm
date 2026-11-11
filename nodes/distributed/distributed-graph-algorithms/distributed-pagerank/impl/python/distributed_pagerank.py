# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-pagerank/. The authors are listed in prov/S5R1H6.jsonl.

"""PageRank by short random walks in CONGEST (Das Sarma, Molla, Pandurangan
and Upfal).

Each node starts K walk tokens. In each round each token stops with
probability eps, or moves to an out-neighbour chosen uniformly. The tokens
are all alike, so a node sends one number on each out-link: how many tokens
go that way. Each node counts the tokens that visit it, and outputs
eps * visits / (n K). The run has a fixed length R = ceil(ln(n^2 K) / eps),
so that with probability at least 1 - 1/n no token is still alive at the end.

PageRank here is the vector pi with pi(v) = eps / n + (1 - eps) * sum over
arcs u -> v of pi(u) / outdeg(u). Every node must have an out-arc.
"""

import math
import random


def rounds_needed(n: int, k: int, eps: float) -> int:
    return math.ceil(math.log(n * n * k) / eps)


def walk_pagerank(n: int, out: list[list[int]], eps: float, k: int, rng: random.Random) -> dict:
    """Return the estimates, the rounds, the messages, the largest message in
    bits and the number of tokens still alive at the end."""
    count = [k] * n  # @line L1
    visits = [k] * n  # the start is the first visit
    r_max = rounds_needed(n, k, eps)
    messages = max_bits = 0
    for _ in range(r_max):  # @line L2
        incoming = [0] * n
        for v in range(n):
            if count[v] == 0:
                continue
            per_arc: dict[int, int] = {}
            for _ in range(count[v]):  # @line L3
                if rng.random() >= eps:  # the token goes on
                    u = out[v][rng.randrange(len(out[v]))]
                    per_arc[u] = per_arc.get(u, 0) + 1
            for u, c in per_arc.items():  # @line L4
                incoming[u] += c
                messages += 1
                max_bits = max(max_bits, c.bit_length())
        for v in range(n):  # @line L5
            count[v] = incoming[v]
            visits[v] += incoming[v]
    est = [eps * visits[v] / (n * k) for v in range(n)]  # @line L6
    return {"est": est, "visits": visits, "rounds": r_max, "messages": messages, "max_bits": max_bits, "alive": sum(count)}


def median_estimate(n: int, out: list[list[int]], eps: float, k: int, groups: int, rng: random.Random) -> list[float]:
    """Run groups independent copies side by side (one number per copy on each
    arc) and take the median at each node."""
    runs = [walk_pagerank(n, out, eps, k, rng)["est"] for _ in range(groups)]
    return [sorted(r[v] for r in runs)[groups // 2] for v in range(n)]


def power_iteration(n: int, out: list[list[int]], eps: float, tol: float = 1e-13) -> list[float]:
    """The oracle: iterate the PageRank equation until it stops moving."""
    pi = [1.0 / n] * n
    while True:
        nxt = [eps / n] * n
        for u in range(n):
            share = (1 - eps) * pi[u] / len(out[u])
            for v in out[u]:
                nxt[v] += share
        if max(abs(a - b) for a, b in zip(pi, nxt)) < tol:
            return nxt
        pi = nxt


def return_probability(n: int, out: list[list[int]], eps: float, v: int) -> float:
    """The chance r(v) that a walk at v comes back to v before it stops."""
    # h(u) = chance to reach v before stopping, from u != v: h = (1 - eps) * mean h(next)
    h = [0.0] * n
    for _ in range(10000):
        nxt = [0.0] * n
        for u in range(n):
            nxt[u] = (1 - eps) * sum(1.0 if w == v else h[w] for w in out[u]) / len(out[u])
        if max(abs(a - b) for a, b in zip(h, nxt)) < 1e-14:
            break
        h = nxt
    return h[v]
