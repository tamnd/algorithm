# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coalescent-simulation/. The authors are listed in prov/V8W27B.jsonl.
"""Hudson's algorithm: a neutral sample under the Kingman coalescent and the
infinite-sites model, without recombination.

Time runs backward from the sample at time 0 and is in units of 2N
generations, so k lineages merge at rate k (k - 1) / 2, and theta = 4 N mu is
the mutation rate of the whole locus. (The program ms uses units of 4N
generations; its times are half of these.)

Nodes 0 .. n-1 are the sampled copies. Each merge makes a new node, so the
internal nodes are n .. 2n-2, in the order in which they were made, and node
2n-2 is the root. parent[v] is the parent of node v (-1 for the root) and
time[v] is its age.

Random numbers are drawn in this order: first, for each merge, one
expovariate and one sample of two positions; then, for each branch in the
order of the node numbers, one Poisson count and one random() per mutation.
"""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from biostoch import categorical, poisson


def simulate_genealogy(rng, n: int) -> Tuple[List[int], List[float]]:
    """A Kingman coalescent tree of n sampled copies as (parent, time)."""
    if n < 1:
        raise ValueError("need n >= 1")
    parent = [-1] * n
    time = [0.0] * n
    active = list(range(n))  # @line L1
    t = 0.0
    while len(active) > 1:  # @line L2
        k = len(active)
        t += rng.expovariate(k * (k - 1) / 2.0)  # @line L3
        i, j = rng.sample(range(k), 2)  # @line L4
        u = len(parent)
        parent.append(-1)
        time.append(t)
        parent[active[i]] = u
        parent[active[j]] = u
        # Replace lineage i by u and remove lineage j.
        active[i] = u  # @line L5
        active[j] = active[-1]
        active.pop()
    return parent, time


def leaves_below(parent: Sequence[int], n: int) -> List[int]:
    """For each node, the bit mask of the sampled copies below it."""
    below = [1 << v if v < n else 0 for v in range(len(parent))]
    # A parent is made after its children, so it has a larger number.
    for v in range(len(parent)):
        if parent[v] >= 0:
            below[parent[v]] |= below[v]
    return below


def place_mutations(rng, parent: Sequence[int], time: Sequence[float], n: int,
                    theta: float, segsites: Optional[int] = None
                    ) -> Tuple[List[float], List[str]]:
    """Mutations on the tree under the infinite-sites model.

    With segsites None, each branch of length l gets Poisson(theta l / 2)
    mutations. With segsites = s, exactly s mutations are placed, each on a
    branch chosen with probability proportional to its length (as ms -s
    does); theta is then not used.

    Returns (positions, haplotypes): the positions in [0, 1) in increasing
    order, and one 0/1 string per sampled copy, with 1 for the derived allele.
    """
    if theta < 0:
        raise ValueError("need theta >= 0")
    below = leaves_below(parent, n)
    branches = [v for v in range(len(parent)) if parent[v] >= 0]
    lengths = [time[parent[v]] - time[v] for v in branches]
    sites = []
    if segsites is None:
        for v, length in zip(branches, lengths):  # @line L6
            count = poisson(rng, theta * length / 2.0)  # @line L7
            for _ in range(count):
                sites.append((rng.random(), below[v]))  # @line L8
    else:
        if segsites < 0:
            raise ValueError("need segsites >= 0")
        if segsites > 0 and not branches:
            raise ValueError("a sample of one copy has no branches")
        for _ in range(segsites):
            v = branches[categorical(rng, lengths)]
            sites.append((rng.random(), below[v]))
    sites.sort()  # @line L9
    positions = [x for x, _ in sites]
    haplotypes = ["".join("1" if (mask >> r) & 1 else "0" for _, mask in sites)
                  for r in range(n)]
    return positions, haplotypes


def simulate(rng, n: int, theta: float, segsites: Optional[int] = None):
    """One sample: (parent, time, positions, haplotypes)."""
    parent, time = simulate_genealogy(rng, n)
    positions, haplotypes = place_mutations(rng, parent, time, n, theta, segsites)
    return parent, time, positions, haplotypes


def tmrca(time: Sequence[float]) -> float:
    """The age of the root."""
    return max(time)


def total_branch_length(parent: Sequence[int], time: Sequence[float]) -> float:
    """The sum of the lengths of all branches."""
    return sum(time[p] - time[v] for v, p in enumerate(parent) if p >= 0)
