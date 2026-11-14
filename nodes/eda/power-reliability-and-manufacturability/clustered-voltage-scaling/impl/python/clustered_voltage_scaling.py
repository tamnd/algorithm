# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clustered-voltage-scaling/. The authors are listed in prov/STT7KY.jsonl.
"""Clustered voltage scaling (Usami and Horowitz 1995).

The logic between registers is a DAG of gates. Each gate has a delay at the
high supply and a larger delay at the low supply, and a switched capacitance.
The primary inputs come from registers at time 0. The outputs go to
level-converting registers, which add the delay lc when their driver is low.
The clock period is T.

Legal: no low gate drives a high gate. The pass visits the gates in reverse
topological order. A gate whose gate fanouts are all low already is tried at
the low supply, and stays low when every output still meets T.
"""

from __future__ import annotations

import random
from typing import Dict, Iterable, List, Sequence, Set, Tuple


class Net:
    """inputs: names; gates: (name, fanins, d_high, d_low, cap) in topological order; outputs: gate names."""

    def __init__(self, inputs: Sequence[str], gates: Sequence[Tuple[str, Sequence[str], float, float, float]], outputs: Sequence[str]):
        self.inputs = list(inputs)
        self.gates = [g[0] for g in gates]
        self.fanin = {g[0]: list(g[1]) for g in gates}
        self.d_high = {g[0]: g[2] for g in gates}
        self.d_low = {g[0]: g[3] for g in gates}
        self.cap = {g[0]: g[4] for g in gates}
        self.outputs = list(outputs)
        self.fanout: Dict[str, List[str]] = {g: [] for g in self.gates}
        for g in self.gates:
            for f in self.fanin[g]:
                if f in self.fanout:
                    self.fanout[f].append(g)


def arrival(net: Net, low: Set[str]) -> Dict[str, float]:
    a: Dict[str, float] = {x: 0 for x in net.inputs}
    for g in net.gates:
        d = net.d_low[g] if g in low else net.d_high[g]
        a[g] = max((a[f] for f in net.fanin[g]), default=0) + d
    return a


def worst_output_time(net: Net, low: Set[str], lc: float) -> float:
    a = arrival(net, low)
    return max(a[o] + (lc if o in low else 0) for o in net.outputs)


def meets_timing(net: Net, low: Set[str], period: float, lc: float) -> bool:
    return worst_output_time(net, low, lc) <= period


def is_legal(net: Net, low: Set[str]) -> bool:
    """No low gate drives a high gate."""
    return all(f in low for g in low for f in net.fanout[g])


def saving(net: Net, low: Iterable[str]) -> float:
    """Switched capacitance moved to the low supply (the power saving is this times alpha f (VH^2 - VL^2))."""
    return sum(net.cap[g] for g in low)


def cvs(net: Net, period: float, lc: float) -> Set[str]:
    """The set of low gates chosen by clustered voltage scaling."""
    low: Set[str] = set()  # @line L1
    if not meets_timing(net, low, period, lc):
        raise ValueError("the circuit misses the period with every gate high")
    for g in reversed(net.gates):  # @line L2: reverse topological order
        if all(f in low for f in net.fanout[g]):  # @line L3
            low.add(g)  # @line L4
            if not meets_timing(net, low, period, lc):  # @line L5
                low.discard(g)  # @line L6
    return low  # @line L7


def random_net(rng: random.Random, n_in: int, n_gates: int) -> Net:
    inputs = [f"i{k}" for k in range(n_in)]
    names = list(inputs)
    gates = []
    for k in range(n_gates):
        fanins = rng.sample(names, min(len(names), rng.randint(1, 2)))
        dh = rng.randint(1, 3)
        gates.append((f"g{k}", fanins, dh, dh + rng.randint(1, 2), rng.randint(1, 5)))
        names.append(f"g{k}")
    used = {f for g in gates for f in g[1]}
    outputs = [g[0] for g in gates if g[0] not in used]
    outputs += [g[0] for g in gates if g[0] in used and rng.random() < 0.2]
    return Net(inputs, gates, outputs)
