# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/switch-level-simulation/. The authors are listed in prov/Z1Y4FS.jsonl.
"""Switch-level simulation of MOS transistor networks with Bryant's strength model.

A transistor is a switch: an n-type one conducts when its gate is 1, a
p-type one when its gate is 0, and its state is X when its gate is X.
Input nodes (vdd, gnd and the primary inputs) are sources of strength OMEGA.
A storage node keeps its charge, a signal whose strength is the node size.
Each transistor has a strength. All sizes are below all transistor strengths,
and OMEGA is above them. A signal on a path has the least strength on the
path. A path is dominant when the signal on it, at every node it passes, is
as strong as the strongest signal at that node. The value of a node is the
least upper bound of the source values of its dominant paths.

With X transistors the steady state uses definite strengths (transistors in
state 1 only) and potential paths (transistors in state 1 or X). The result
is sound: each 0 or 1 holds for every binary choice of the X values.

The storage nodes are split into channel-connected components. A round solves
every component whose transistor gates or own nodes changed, from the values
of the round before. This is a unit-delay model with one delay per component.
"""

from __future__ import annotations

import heapq
from typing import Dict, List, Optional, Sequence, Tuple

X = 2
OMEGA = 10 ** 9
NONE = -1  # no signal


class Oscillation(RuntimeError):
    """The rounds did not reach a steady state within the limit."""


class Network:
    """Storage nodes with sizes, input nodes, and transistors (kind, gate, a, b, strength)."""

    def __init__(self) -> None:
        self.inputs: List[str] = ["vdd", "gnd"]
        self.size: Dict[str, int] = {}
        self.trans: List[Tuple[str, str, str, str, int]] = []

    def add_input(self, name: str) -> None:
        self.inputs.append(name)

    def add_node(self, name: str, size: int = 1) -> None:
        self.size[name] = size

    def add_transistor(self, kind: str, gate: str, a: str, b: str, strength: int = 10) -> None:
        if kind not in ("n", "p"):
            raise ValueError("a transistor is of type n or p")
        self.trans.append((kind, gate, a, b, strength))

    def is_input(self, n: str) -> bool:
        return n in self.inputs

    def check(self) -> None:
        """Every terminal is a node, and every size is below every transistor strength."""
        known = set(self.inputs) | set(self.size)
        for kind, g, a, b, s in self.trans:
            if not {g, a, b} <= known:
                raise ValueError("a transistor terminal is not a node")
            if self.size and s <= max(self.size.values()):
                raise ValueError("every transistor strength must be above every node size")


def channel_connected_components(net: Network) -> List[Tuple[List[str], List[int]]]:
    """Storage nodes joined by source-drain connections, input nodes left out.

    Returns a list of (storage nodes, indices of the transistors with a storage terminal in it).
    """
    parent = {n: n for n in net.size}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for kind, g, a, b, s in net.trans:
        if a in parent and b in parent:
            parent[find(a)] = find(b)
    groups: Dict[str, Tuple[List[str], List[int]]] = {}
    for n in net.size:
        groups.setdefault(find(n), ([], []))[0].append(n)
    for i, (kind, g, a, b, s) in enumerate(net.trans):
        end = a if a in parent else (b if b in parent else None)
        if end is not None:
            groups[find(end)][1].append(i)
    return list(groups.values())


def switch_state(kind: str, gate_value: int) -> int:
    """1 = conducting, 0 = open, X = unknown."""
    if gate_value == X:
        return X
    return gate_value if kind == "n" else 1 - gate_value


def widest(nodes: Sequence[str], seeds: Dict[str, int], adj: Dict[str, List[Tuple[str, int]]],
           floor: Optional[Dict[str, int]] = None) -> Dict[str, int]:
    """Strongest signal at each node: max over paths of the least strength on the path.

    seeds gives the strength that enters each node directly. With floor, a signal
    enters node w only when its strength is at least floor[w].
    """
    best = {n: NONE for n in nodes}
    for n, s in seeds.items():
        if floor is None or s >= floor[n]:
            best[n] = max(best[n], s)
    heap = [(-s, n) for n, s in best.items() if s != NONE]
    heapq.heapify(heap)
    done = set()
    while heap:
        s, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for w, gamma in adj[u]:
            c = min(best[u], gamma)
            if c > best[w] and (floor is None or c >= floor[w]):
                best[w] = c
                heapq.heappush(heap, (-c, w))
    return best


def steady_state(net: Network, nodes: Sequence[str], trans: Sequence[int],
                 val: Dict[str, int]) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Steady state of one component for the transistor states and charges in val.

    Returns (new values, definite strengths) of the storage nodes of the component.
    """
    on: Dict[str, List[Tuple[str, int]]] = {n: [] for n in nodes}
    maybe: Dict[str, List[Tuple[str, int]]] = {n: [] for n in nodes}
    feed_on: List[Tuple[str, str, int]] = []  # (storage node, input node, strength)
    feed_maybe: List[Tuple[str, str, int]] = []
    for i in trans:  # @line L9
        kind, g, a, b, gamma = net.trans[i]
        state = switch_state(kind, val[g])
        if state == 0:
            continue
        for u, w in ((a, b), (b, a)):
            if w not in on:
                continue
            if net.is_input(u):
                feed_maybe.append((w, u, gamma))
                if state == 1:
                    feed_on.append((w, u, gamma))
            else:
                maybe[w].append((u, gamma))
                if state == 1:
                    on[w].append((u, gamma))
    seeds = {n: net.size[n] for n in nodes}  # @line L10
    for w, u, gamma in feed_on:
        seeds[w] = max(seeds[w], gamma)
    strength = widest(nodes, seeds, on)
    reach: Dict[int, Dict[str, int]] = {}
    for b in (0, 1):  # @line L11
        seeds_b: Dict[str, int] = {n: net.size[n] for n in nodes if val[n] in (b, X)}  # @line L12
        for w, u, gamma in feed_maybe:
            if val[u] in (b, X):
                seeds_b[w] = max(seeds_b.get(w, NONE), gamma)
        reach[b] = widest(nodes, seeds_b, maybe, floor=strength)
    new: Dict[str, int] = {}
    for n in nodes:  # @line L13
        r0, r1 = reach[0][n] != NONE, reach[1][n] != NONE
        new[n] = X if (r0 and r1) else (1 if r1 else 0)
    return new, strength  # @line L14


def simulate(net: Network, inputs: Dict[str, int], init: Dict[str, int],
             max_rounds: int = 200) -> Tuple[Dict[str, int], int]:
    """Settle the network for fixed input values from the stored values init.

    Returns (values of all nodes, number of component solves).
    """
    net.check()
    val = {n: init.get(n, X) for n in net.size}  # @line L1
    val.update(inputs)
    val["vdd"], val["gnd"] = 1, 0
    comps = channel_connected_components(net)  # @line L2
    readers: Dict[str, List[int]] = {}  # components whose solve reads the node
    for ci, (nodes, trans) in enumerate(comps):
        for n in nodes:
            readers.setdefault(n, []).append(ci)
        for i in trans:
            readers.setdefault(net.trans[i][1], []).append(ci)
    queue = list(range(len(comps)))  # @line L3
    rounds = solves = 0
    while queue:  # @line L4
        rounds += 1
        if rounds > max_rounds:
            raise Oscillation(f"no steady state after {max_rounds} rounds")
        new: Dict[str, int] = {}
        for ci in queue:  # @line L5
            new.update(steady_state(net, comps[ci][0], comps[ci][1], val)[0])
            solves += 1
        changed = [n for n, v in new.items() if v != val[n]]  # @line L6
        val.update(new)
        queue = sorted({ci for n in changed for ci in readers.get(n, [])})  # @line L7
    return val, solves  # @line L8
