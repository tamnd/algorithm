# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-vpack/. The authors are listed in prov/R2R827.jsonl.

"""T-VPack: greedy timing-driven packing of BLEs into clusters.

A BLE is a K-input LUT, an optional flip-flop and an output multiplexer. A netlist of BLEs is a list of Ble records. Nets are
strings. A cluster holds at most N BLEs and at most I distinct nets that
come from outside it. All arithmetic is in Fraction, so a run is exact.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional


@dataclass(frozen=True)
class Ble:
    inputs: tuple[str, ...]
    output: str
    registered: bool = False


def form_bles(luts: list[tuple[tuple[str, ...], str]], ffs: list[tuple[str, str]]) -> list[Ble]:
    """Step 1: put each LUT together with the flip-flop that it alone feeds.

    luts: (input nets, output net). ffs: (D net, Q net). A flip-flop whose D net
    is not the output of a LUT with that flip-flop as its only reader gets a
    BLE of its own, whose LUT passes D through.
    """
    readers: dict[str, int] = {}
    for ins, _ in luts:
        for n in ins:
            readers[n] = readers.get(n, 0) + 1
    for d, _ in ffs:
        readers[d] = readers.get(d, 0) + 1
    by_out = {out: (ins, out) for ins, out in luts}
    merged: set[str] = set()
    bles = []
    for d, q in ffs:
        if d in by_out and readers[d] == 1 and d not in merged:
            merged.add(d)
            bles.append(Ble(by_out[d][0], q, True))
        else:
            bles.append(Ble((d,), q, True))
    for ins, out in luts:
        if out not in merged:
            bles.append(Ble(ins, out, False))
    return bles


def external_inputs(bles: list[Ble], members: set[int]) -> set[str]:
    """Nets used by some member and driven by no member."""
    driven = {bles[i].output for i in members}
    return {n for i in members for n in bles[i].inputs if n not in driven}


def criticalities(bles: list[Ble]) -> dict[tuple[int, int], Fraction]:
    """Criticality 1 - slack / Dmax of each connection (driver BLE, reader BLE).

    Unit delay model: each BLE has delay 1, connections have delay 0, and a
    registered BLE starts a new path at its output. The netlist must have no
    combinational cycle.
    """
    driver = {b.output: i for i, b in enumerate(bles)}
    n = len(bles)
    fanin = [[driver[x] for x in b.inputs if x in driver] for b in bles]
    order: list[int] = []
    state = [0] * n

    def visit(v: int) -> None:
        state[v] = 1
        for u in fanin[v]:
            if not bles[u].registered and state[u] == 0:
                visit(u)
        state[v] = 2
        order.append(v)

    for v in range(n):
        if state[v] == 0:
            visit(v)
    # arrival[v]: time at the output of v's LUT (before its flip-flop).
    arrival = [0] * n
    for v in order:
        a = 0
        for u in fanin[v]:
            if not bles[u].registered:
                a = max(a, arrival[u])
        arrival[v] = a + 1
    dmax = max(arrival) if arrival else 1
    required = [dmax] * n
    for v in reversed(order):
        for u in fanin[v]:
            if not bles[u].registered:
                required[u] = min(required[u], required[v] - 1)
    crit = {}
    for v in range(n):
        for u in fanin[v]:
            start = 0 if bles[u].registered else arrival[u]  # a flip-flop output starts a path
            slack = required[v] - 1 - start
            crit[(u, v)] = 1 - Fraction(slack, dmax)
    return crit


def t_vpack(
    bles: list[Ble],
    n_max: int,
    i_max: int,
    lam: Fraction = Fraction(3, 4),
    k: Optional[int] = None,
) -> list[list[int]]:
    """Pack the BLEs into clusters of at most n_max BLEs and i_max inputs.

    Returns the clusters as lists of BLE indices, in the order filled.
    """
    if k is None:
        k = max((len(b.inputs) for b in bles), default=1)
    if k > i_max:
        raise ValueError("a BLE with more inputs than the cluster cannot be packed")
    g = k + 1  # the most nets a BLE can touch: K inputs and one output
    crit = criticalities(bles)
    nets_of = [set(b.inputs) | {b.output} for b in bles]
    ble_crit = [Fraction(0)] * len(bles)
    pair_crit: list[dict[int, Fraction]] = [{} for _ in bles]  # pair_crit[a][b]: most critical connection between a and b
    for (u, v), c in crit.items():
        ble_crit[u] = max(ble_crit[u], c)
        ble_crit[v] = max(ble_crit[v], c)
        pair_crit[u][v] = max(pair_crit[u].get(v, Fraction(0)), c)
        pair_crit[v][u] = max(pair_crit[v].get(u, Fraction(0)), c)
    unclustered = set(range(len(bles)))
    clusters = []
    while unclustered:  # @line L1
        seed = max(unclustered, key=lambda i: (ble_crit[i], len(bles[i].inputs), -i))  # @line L2
        members = {seed}
        unclustered.discard(seed)
        while len(members) < n_max:  # @line L3
            cluster_nets = set().union(*(nets_of[i] for i in members))
            best = None
            best_key = None
            for b in sorted(unclustered):  # @line L4
                if len(external_inputs(bles, members | {b})) > i_max:  # @line L5
                    continue
                shared = len(nets_of[b] & cluster_nets)
                c = max((pair_crit[b].get(m, Fraction(0)) for m in members), default=Fraction(0))
                attraction = lam * c + (1 - lam) * Fraction(shared, g)  # @line L6
                key = (attraction, len(bles[b].inputs), -b)
                if best_key is None or key > best_key:
                    best, best_key = b, key
            if best is None:  # @line L7
                break
            members.add(best)  # @line L8
            unclustered.discard(best)
        clusters.append(sorted(members))  # @line L9
    return clusters


def is_legal(bles: list[Ble], clusters: list[list[int]], n_max: int, i_max: int) -> bool:
    """Every BLE in exactly one cluster, and every cluster within N and I."""
    seen = sorted(i for c in clusters for i in c)
    if seen != list(range(len(bles))):
        return False
    return all(1 <= len(c) <= n_max and len(external_inputs(bles, set(c))) <= i_max for c in clusters)


def min_clusters(bles: list[Ble], n_max: int, i_max: int) -> int:
    """Exact least number of legal clusters, by dynamic programming over subsets."""
    n = len(bles)
    full = (1 << n) - 1
    legal = [False] * (1 << n)
    for mask in range(1, 1 << n):
        members = {i for i in range(n) if mask >> i & 1}
        legal[mask] = len(members) <= n_max and len(external_inputs(bles, members)) <= i_max
    best = [0] + [n + 1] * full
    for mask in range(1, full + 1):
        low = mask & -mask
        sub = mask
        while sub:
            if sub & low and legal[sub]:
                best[mask] = min(best[mask], best[mask ^ sub] + 1)
            sub = (sub - 1) & mask
    return best[full]
