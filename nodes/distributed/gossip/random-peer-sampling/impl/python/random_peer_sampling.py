# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-peer-sampling/. The authors are listed in prov/F8JAYE.jsonl.

"""Random walk samplers of a peer on a connected graph.

A simple random walk moves to a uniform neighbour, so its stationary law is
proportional to the degree: high degree nodes are sampled too often. The
Metropolis-Hastings walk proposes a uniform neighbour j of i and moves there
with probability min(1, d_i / d_j), and stays at i otherwise. Its transition
matrix is symmetric, so its stationary law is uniform. Both walks are made
lazy (stay with probability 1/2) so that they are aperiodic on every graph.

walk_law computes the exact law after t steps, without sampling.
"""

import random


def preferential_graph(n: int, k: int, seed: int) -> list[list[int]]:
    """A connected graph with uneven degrees: node v joins and links to k
    earlier nodes chosen with probability proportional to degree."""
    rng = random.Random(seed)
    nb = [set() for _ in range(n)]
    ends = []
    for v in range(1, n):
        targets = {0} if v == 1 else set()
        while len(targets) < min(k, v):
            targets.add(rng.choice(ends) if ends and rng.random() < 0.9 else rng.randrange(v))
        for u in targets:
            nb[v].add(u)
            nb[u].add(v)
            ends += [u, v]
    return [sorted(s) for s in nb]


def step_probabilities(adj: list[list[int]], i: int, kind: str) -> dict[int, float]:
    """The law of the next position of a lazy walk at node i."""
    out = {i: 0.5}
    d = len(adj[i])
    for j in adj[i]:
        if kind == "srw":
            p = 0.5 / d
        else:
            p = 0.5 / d * min(1.0, d / len(adj[j]))
        out[j] = out.get(j, 0.0) + p
        if kind != "srw":
            out[i] += 0.5 / d - p
    return out


def walk_law(adj: list[list[int]], start: int, steps: int, kind: str) -> list[float]:
    n = len(adj)
    rows = [step_probabilities(adj, i, kind) for i in range(n)]
    law = [0.0] * n
    law[start] = 1.0
    for _ in range(steps):
        new = [0.0] * n
        for i, p in enumerate(law):
            if p:
                for j, q in rows[i].items():
                    new[j] += p * q
        law = new
    return law


def sample(adj: list[list[int]], start: int, steps: int, kind: str, rng: random.Random) -> int:
    v = start
    for _ in range(steps):
        if rng.random() < 0.5:
            continue
        j = rng.choice(adj[v])
        if kind == "srw" or rng.random() < len(adj[v]) / len(adj[j]):
            v = j
    return v


def total_variation(p: list[float], q: list[float]) -> float:
    return sum(abs(a - b) for a, b in zip(p, q)) / 2
