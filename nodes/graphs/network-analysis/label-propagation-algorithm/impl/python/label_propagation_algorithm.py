# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/label-propagation-algorithm/. The authors are listed in prov/GKHM2A.jsonl.

import random


def label_propagation_algorithm(
    n: int,
    edges: list[tuple[int, int]],
    rng: random.Random | None = None,
) -> tuple[list[int], list[list[int]], int]:
    """Return (labels, communities, rounds) for an undirected graph on 0 .. n-1.

    Asynchronous label propagation: each round visits the vertices in a new
    random order, and a vertex whose label is not among the most frequent
    labels of its neighbours takes one of those, chosen at random. The run
    stops after a round with no change, at most m + 1 rounds. communities is
    the sorted list of the sorted classes of equal labels. Self-loops and
    repeated edges are ignored.
    Expected time O(n + m) per round, extra space O(n).
    """
    if rng is None:
        rng = random.Random(0)
    adj = [set() for _ in range(n)]
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            adj[v].add(u)
    neighbours = [sorted(a) for a in adj]
    label = list(range(n))  # @line L1
    order = list(range(n))
    rounds = 0
    while True:  # @line L2
        rounds += 1
        changed = False  # @line L3
        rng.shuffle(order)  # @line L4
        for v in order:
            count: dict[int, int] = {}  # @line L5
            for w in neighbours[v]:
                count[label[w]] = count.get(label[w], 0) + 1
            if not count:  # @line L6
                continue
            top = max(count.values())
            if count.get(label[v], 0) < top:
                best = sorted(x for x, c in count.items() if c == top)  # @line L7
                label[v] = rng.choice(best)
                changed = True  # @line L8
        if not changed:  # @line L9
            break
    classes: dict[int, list[int]] = {}  # @line L10
    for v in range(n):
        classes.setdefault(label[v], []).append(v)
    return label, sorted(classes.values()), rounds
