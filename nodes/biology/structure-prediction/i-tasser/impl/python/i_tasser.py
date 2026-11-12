# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/i-tasser/. The authors are listed in prov/KNTH85.jsonl.

"""The search core of I-TASSER: replica-exchange Monte Carlo and SPICKER clustering.

The real I-TASSER (Roy, Kucukural and Zhang 2010) threads the sequence with
LOMETS, cuts the aligned parts of the templates into fragments, reassembles
them on a reduced chain model by replica-exchange Monte Carlo, clusters the
decoys with SPICKER, and runs a second round of simulation from the cluster
centroids with extra restraints. Threading and the protein force field are
far too large for this file, so the pipeline below takes them as inputs:

- the starting states (built from templates in the real program),
- an energy function on states and a proposal function for local moves,
- a distance between states (RMSD of the C-alpha atoms in the real program).

Everything random takes an explicit random.Random.
"""

import math
import random
from typing import Callable, Dict, Hashable, List, Sequence, Tuple

State = Hashable
Energy = Callable[[State], float]
Propose = Callable[[State, random.Random], State]
Distance = Callable[[State, State], float]


def replica_exchange_mc(
    energy: Energy, propose: Propose, starts: Sequence[State], temps: Sequence[float],
    sweeps: int, rng: random.Random, sample_every: int = 1,
) -> List[List[State]]:
    """Replica-exchange (parallel tempering) Metropolis Monte Carlo.

    Replica r runs at temperature temps[r]; temps should increase. The proposal
    must be symmetric (q(x -> y) = q(y -> x)) for the stationary distribution of
    replica r to be the Boltzmann distribution exp(-E / T_r) / Z. After each sweep,
    one random neighbouring pair (r, r + 1) tries to swap states.
    Returns, for each replica, the states it visited every sample_every sweeps.
    """
    x = [starts[r % len(starts)] for r in range(len(temps))]
    e = [energy(s) for s in x]
    samples: List[List[State]] = [[] for _ in temps]
    for sweep in range(sweeps):  # @line L8
        for r, t in enumerate(temps):  # @line L9
            y = propose(x[r], rng)
            ey = energy(y)
            if ey <= e[r] or rng.random() < math.exp(-(ey - e[r]) / t):
                x[r], e[r] = y, ey
        if len(temps) > 1:  # @line L10
            r = rng.randrange(len(temps) - 1)
            delta = (1.0 / temps[r] - 1.0 / temps[r + 1]) * (e[r] - e[r + 1])
            if delta >= 0 or rng.random() < math.exp(delta):
                x[r], x[r + 1] = x[r + 1], x[r]
                e[r], e[r + 1] = e[r + 1], e[r]
        if sweep % sample_every == 0:
            for r in range(len(temps)):
                samples[r].append(x[r])
    return samples  # @line L11


def spicker(decoys: Sequence[State], dist: Distance, cutoff: float) -> List[Tuple[int, List[int]]]:
    """SPICKER-style clustering by neighbour count.

    Repeatedly take the decoy with the most neighbours (decoys within cutoff,
    itself included) among those not yet clustered, ties broken by the lower
    index, and remove it with its neighbours. Returns (center, members) pairs,
    largest first. O(d^2) distance evaluations for d decoys.
    """
    d = len(decoys)
    near = [[j for j in range(d) if dist(decoys[i], decoys[j]) <= cutoff] for i in range(d)]
    left = set(range(d))
    clusters: List[Tuple[int, List[int]]] = []
    while left:  # @line L12
        counts = {i: sum(1 for j in near[i] if j in left) for i in left}
        c = min(left, key=lambda i: (-counts[i], i))  # @line L13
        members = sorted(j for j in near[c] if j in left)
        clusters.append((c, members))  # @line L14
        left -= set(members)
    return clusters


def i_tasser(
    energy: Energy, propose: Propose, starts: Sequence[State], dist: Distance, cutoff: float,
    temps: Sequence[float], sweeps: int, rng: random.Random, restraint_weight: float = 1.0,
    decoy_every: int = 20,
) -> Tuple[State, List[Tuple[int, List[int]]]]:
    """Two rounds of replica-exchange MC with SPICKER clustering in between.

    Round 2 adds a restraint toward the nearest centroid of round 1, the role
    the centroid and template restraints play in the second I-TASSER
    iteration. Returns the lowest-energy decoy of the largest round-2 cluster,
    and the round-2 clusters.
    """
    first = list(starts)  # @line L1
    n_low = max(1, len(temps) // 2)  # decoys come from the low-temperature replicas
    run1 = replica_exchange_mc(energy, propose, first, temps, sweeps, rng, decoy_every)  # @line L2
    decoys1 = [s for r in range(n_low) for s in run1[r]]
    clusters1 = spicker(decoys1, dist, cutoff)  # @line L3
    centroids = [decoys1[c] for c, _ in clusters1[:3]]

    def restrained(s: State) -> float:  # @line L4
        return energy(s) + restraint_weight * min(dist(s, c) for c in centroids) ** 2

    run2 = replica_exchange_mc(restrained, propose, centroids, temps, sweeps, rng, decoy_every)  # @line L5
    decoys2 = [s for r in range(n_low) for s in run2[r]]
    clusters2 = spicker(decoys2, dist, cutoff)
    _, members = clusters2[0]
    best = min((decoys2[j] for j in members), key=lambda s: (energy(s), repr(s)))  # @line L6
    return best, clusters2  # @line L7


def boltzmann(energy: Energy, states: Sequence[State], t: float) -> Dict[State, float]:
    """The exact Boltzmann distribution at temperature t over a finite state list."""
    w = {s: math.exp(-energy(s) / t) for s in states}
    z = sum(w.values())
    return {s: v / z for s, v in w.items()}
