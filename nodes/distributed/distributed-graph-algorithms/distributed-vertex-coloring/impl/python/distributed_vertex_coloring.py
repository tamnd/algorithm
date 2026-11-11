# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-vertex-coloring/. The authors are listed in prov/5JYM67.jsonl.

"""Randomized (Delta + 1)-colouring by random colour trials, simulated phase by phase in the LOCAL model.

In each phase every uncoloured node, with probability 1/2, tries a colour
drawn uniformly from its palette: the colours in {0, ..., Delta} that no
coloured neighbour holds. It keeps the colour if no neighbour tried the same
colour in this phase. A phase is two rounds: one to send the trial and one to
announce a kept colour.

Precondition: adj is an undirected simple graph; delta >= the maximum degree.
Cost: each node succeeds in a phase with probability at least 1/4, whatever
the other nodes do, so all nodes are coloured after O(log n) phases with high
probability. A message holds one colour of O(log Delta) bits.
"""

import random


def random_trial_coloring(
    adj: list[list[int]], delta: int, rng: random.Random, stats: list[tuple[int, int]] | None = None
) -> tuple[list[int], int]:
    """Return (colours in [0, delta], rounds). stats, if given, gets (uncoloured, newly coloured) per phase."""
    n = len(adj)
    col = [-1] * n
    rounds = 0
    while any(c < 0 for c in col):
        live = [v for v in range(n) if col[v] < 0]
        trial: dict[int, int] = {}
        for v in live:
            if rng.random() < 0.5:
                palette = sorted(set(range(delta + 1)) - {col[u] for u in adj[v] if col[u] >= 0})
                trial[v] = rng.choice(palette)
        rounds += 1  # round 1 of the phase: send the trial colour
        kept = [v for v, x in trial.items() if all(trial.get(u) != x for u in adj[v])]
        for v in kept:
            col[v] = trial[v]
        rounds += 1  # round 2 of the phase: announce a kept colour
        if stats is not None:
            stats.append((len(live), len(kept)))
    return col, rounds
