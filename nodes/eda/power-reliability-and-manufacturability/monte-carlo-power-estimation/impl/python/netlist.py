# SPDX-License-Identifier: MIT
# Shared helper of the pr1 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Gate-level combinational netlists for the power estimation pages.

A circuit has named primary inputs and gates in topological order. Each gate
has a kind (BUF, NOT, AND, OR, NAND, NOR, XOR, XNOR), a list of fanin names
and an integer delay (1 by default). A node is a primary input or a gate.

This module holds the circuit model, plain evaluation of one input vector,
structural queries (fanout, support, reconvergence) and a step simulation of
the transport delay model. It holds no estimation algorithm.
"""

from __future__ import annotations

import random
from typing import Iterable, Optional, Sequence

KINDS = ("BUF", "NOT", "AND", "OR", "NAND", "NOR", "XOR", "XNOR")


def gate_value(kind: str, bits: Sequence[int]) -> int:
    """Value of one gate on 0-1 inputs."""
    if kind == "BUF":
        return bits[0]
    if kind == "NOT":
        return 1 - bits[0]
    if kind in ("AND", "NAND"):
        v = int(all(bits))
    elif kind in ("OR", "NOR"):
        v = int(any(bits))
    elif kind in ("XOR", "XNOR"):
        v = sum(bits) % 2
    else:
        raise ValueError(f"unknown gate kind {kind}")
    return 1 - v if kind in ("NAND", "NOR", "XNOR") else v


class Circuit:
    """Inputs, then gates (name, kind, fanins) in topological order."""

    def __init__(
        self,
        inputs: Sequence[str],
        gates: Sequence[tuple[str, str, Sequence[str]]],
        delay: Optional[dict[str, int]] = None,
    ) -> None:
        self.inputs = list(inputs)
        self.gates = [(g, k, list(f)) for g, k, f in gates]
        seen = set(self.inputs)
        if len(seen) != len(self.inputs):
            raise ValueError("repeated input name")
        for g, k, fins in self.gates:
            if k not in KINDS:
                raise ValueError(f"unknown gate kind {k}")
            if g in seen:
                raise ValueError(f"repeated node name {g}")
            if not fins or (k in ("BUF", "NOT") and len(fins) != 1):
                raise ValueError(f"bad fanin count at {g}")
            for f in fins:
                if f not in seen:
                    raise ValueError(f"{g} reads {f} before it is defined")
            seen.add(g)
        self.nodes = self.inputs + [g for g, _, _ in self.gates]
        self.delay = {g: 1 for g, _, _ in self.gates}
        if delay:
            self.delay.update(delay)

    def evaluate(self, x: Sequence[int]) -> dict[str, int]:
        """Values of all nodes for the input vector x (in the order of self.inputs)."""
        val = dict(zip(self.inputs, x))
        for g, k, fins in self.gates:
            val[g] = gate_value(k, [val[f] for f in fins])
        return val

    def fanout(self) -> dict[str, int]:
        """Number of gate input pins that each node drives."""
        cnt = {v: 0 for v in self.nodes}
        for _, _, fins in self.gates:
            for f in fins:
                cnt[f] += 1
        return cnt

    def is_fanout_free(self) -> bool:
        return all(c <= 1 for c in self.fanout().values())

    def support(self) -> dict[str, frozenset[str]]:
        """The primary inputs in the transitive fanin of each node."""
        sup: dict[str, frozenset[str]] = {x: frozenset([x]) for x in self.inputs}
        for g, _, fins in self.gates:
            sup[g] = frozenset().union(*(sup[f] for f in fins))
        return sup

    def has_reconvergence(self) -> bool:
        """True when some gate has two fanin pins whose supports meet."""
        sup = self.support()
        for _, _, fins in self.gates:
            for i in range(len(fins)):
                for j in range(i + 1, len(fins)):
                    if sup[fins[i]] & sup[fins[j]]:
                        return True
        return False

    def arrival(self) -> dict[str, int]:
        """Latest time at which each node can change after the inputs change at time 0."""
        t = {x: 0 for x in self.inputs}
        for g, _, fins in self.gates:
            t[g] = self.delay[g] + max(t[f] for f in fins)
        return t


def waveforms(c: Circuit, x: Sequence[int], y: Sequence[int]) -> dict[str, list[int]]:
    """Transport delay simulation: the inputs change from x to y at time 0.

    Returns, for each node, its values at times -1, 0, 1, ..., T, where T is the
    largest arrival time. A gate with delay d has at time t the value of its
    function on the values of its fanins at time t - d. Before time 0 every
    node holds its value under x.
    """
    old = c.evaluate(x)
    horizon = max(c.arrival().values())
    wave = {v: [old[v]] for v in c.nodes}  # index 0 is time -1
    for xi, a, b in zip(c.inputs, x, y):
        wave[xi] = [a] + [b] * (horizon + 1)
    for g, k, fins in c.gates:
        d = c.delay[g]
        w = [old[g]]
        for t in range(horizon + 1):
            s = t - d
            w.append(gate_value(k, [wave[f][s + 1] if s >= -1 else old[f] for f in fins]))
        wave[g] = w
    return wave


def transitions(c: Circuit, x: Sequence[int], y: Sequence[int], delay_model: str = "zero") -> dict[str, int]:
    """Number of value changes of each node when the inputs change from x to y.

    delay_model "zero": a node changes at most once, when its value under x and y differ.
    delay_model "transport": the step simulation of waveforms(), which counts glitches.
    """
    if delay_model == "zero":
        a, b = c.evaluate(x), c.evaluate(y)
        return {v: int(a[v] != b[v]) for v in c.nodes}
    if delay_model == "transport":
        w = waveforms(c, x, y)
        return {v: sum(1 for t in range(1, len(s)) if s[t] != s[t - 1]) for v, s in w.items()}
    raise ValueError(delay_model)


def random_circuit(
    rng: random.Random,
    n_inputs: int,
    n_gates: int,
    kinds: Iterable[str] = KINDS,
    max_fanin: int = 3,
    fanout_free: bool = False,
    max_delay: int = 1,
) -> Circuit:
    """A random circuit. With fanout_free, every node drives at most one gate pin."""
    kinds = list(kinds)
    inputs = [f"x{i}" for i in range(n_inputs)]
    free = list(inputs)
    names = list(inputs)
    gates = []
    delay = {}
    for j in range(n_gates):
        pool = free if fanout_free else names
        if not pool:
            break
        k = rng.choice(kinds)
        if k in ("BUF", "NOT"):
            m = 1
        else:
            m = min(len(pool), rng.randint(2, max_fanin))
            if m < 2:
                k = rng.choice(["BUF", "NOT"])
                m = 1
        fins = rng.sample(pool, m)
        g = f"g{j}"
        gates.append((g, k, fins))
        delay[g] = rng.randint(1, max_delay)
        if fanout_free:
            for f in fins:
                free.remove(f)
            free.append(g)
        names.append(g)
    return Circuit(inputs, gates, delay)
