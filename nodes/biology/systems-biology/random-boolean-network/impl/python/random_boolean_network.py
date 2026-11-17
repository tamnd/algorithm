# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-boolean-network/. The authors are listed in prov/JT779F.jsonl.
"""Random Boolean networks (Kauffman's NK model) and their attractors.

A network on n genes is a list of (inputs, table) pairs, one per gene. inputs
is a tuple of K distinct genes, and table is a list of 2^K bits: the next
value of the gene is table[sum(x[inputs[r]] << r)]. A state is an integer
whose bit i is the value of gene i, so there are 2^n states.

Random draws. random_network(rng, n, k, p) draws, gene by gene in index
order, first rng.sample(range(n), k) for the inputs, then 2^k calls of
rng.random(), one per table entry in index order; an entry is 1 when the
draw is below p.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

Network = List[Tuple[Tuple[int, ...], List[int]]]


def random_network(rng, n: int, k: int, p: float = 0.5) -> Network:
    """Kauffman's random network: K distinct random inputs and a random table with bias p per gene."""
    if not 0 <= k <= n:
        raise ValueError("need 0 <= k <= n")
    net: Network = []
    for _ in range(n):
        inputs = tuple(rng.sample(range(n), k))
        table = [1 if rng.random() < p else 0 for _ in range(1 << k)]
        net.append((inputs, table))
    return net


def step(net: Network, state: int) -> int:
    """Synchronous update: every gene reads its inputs in the old state."""
    out = 0
    for i, (inputs, table) in enumerate(net):
        idx = 0
        for r, g in enumerate(inputs):
            idx |= ((state >> g) & 1) << r
        out |= table[idx] << i
    return out


def successor_table(net: Network) -> List[int]:
    """The map F on all 2^n states, as a list."""
    return [step(net, s) for s in range(1 << len(net))]


def attractors(succ: Sequence[int]) -> Tuple[List[List[int]], List[int], List[int]]:
    """Cycles of the functional graph s -> succ[s], with basin sizes.

    Returns (cycles, basin, label): cycles[a] lists the states of attractor a
    in the order of the dynamics, starting from its smallest state; basin[a]
    is the number of states that reach it (the cycle included); label[s] is
    the attractor that state s reaches. Attractors are numbered in the order
    in which the scan over s = 0, 1, ... finds them. Time O(2^n).
    """
    size = len(succ)
    label = [-1] * size  # @line L1
    mark = [-1] * size  # the scan start that put a state on the current path
    cycles: List[List[int]] = []
    for s in range(size):  # @line L2
        if label[s] != -1:
            continue
        path = []  # @line L3
        t = s
        while label[t] == -1 and mark[t] != s:  # @line L4
            mark[t] = s
            path.append(t)
            t = succ[t]
        # if t has no label, it is on the current path, and the path closes a new cycle
        if label[t] == -1:  # @line L5
            start = path.index(t)
            cyc = path[start:]
            r = cyc.index(min(cyc))
            cycles.append(cyc[r:] + cyc[:r])
            a = len(cycles) - 1
        else:
            a = label[t]
        for u in path:  # @line L6
            label[u] = a
    basin = [0] * len(cycles)
    for s in range(size):
        basin[label[s]] += 1
    return cycles, basin, label  # @line L7


def attractors_by_image(succ: Sequence[int]) -> Tuple[List[List[int]], Dict[int, int]]:
    """A second method: the cyclic states are the limit of X, F(X), F(F(X)), ... from X = all states.

    Returns the cycles (each from its smallest state, sorted by that state) and
    a map from the smallest state of each cycle to its basin size, where the
    basin is found by iterating each state until it reaches a cyclic state.
    """
    x = set(range(len(succ)))
    while True:
        y = {succ[s] for s in x}
        if y == x:
            break
        x = y
    cycles = []
    seen = set()
    for s in sorted(x):
        if s in seen:
            continue
        cyc = [s]
        t = succ[s]
        while t != s:
            cyc.append(t)
            t = succ[t]
        seen.update(cyc)
        cycles.append(cyc)
    rep = {}
    for cyc in cycles:
        for u in cyc:
            rep[u] = cyc[0]
    basin: Dict[int, int] = {}
    for s in range(len(succ)):
        t = s
        while t not in rep:
            t = succ[t]
        basin[rep[t]] = basin.get(rep[t], 0) + 1
    return cycles, basin


def hamming_spread(net: Network, state: int, gene: int) -> int:
    """Number of genes whose next value changes when one gene of the state is flipped."""
    return bin(step(net, state) ^ step(net, state ^ (1 << gene))).count("1")
