# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitonic-counting-network/. The authors are listed in prov/0S8S0R.jsonl.

"""The bitonic counting network (Aspnes, Herlihy and Shavit, JACM 1994).

Bitonic[1] is a wire. Bitonic[2k] is two Bitonic[k] side by side, the first
on the first k input wires and the second on the last k, followed by
Merger[2k] on their outputs x (from the first) and x' (from the second).

Merger[2] is one balancer. Merger[2k] for k >= 2 is two Merger[k] side by
side: the first gets the even outputs of x and the odd outputs of x', the
second gets the odd outputs of x and the even outputs of x'. Call their
outputs z and z'. A last layer of k balancers joins z_i with z'_i, and its
outputs, in the order z_0, z'_0, z_1, z'_1, ..., are the outputs of the
merger.

A balancer joins two wires in place: the tokens that reach it leave on the
first wire, then the second, then the first, and so on. So a network is a
list of balancers on wire pairs and an output order: out[j] is the wire of
output j. In Bitonic[w] the output order is a permutation of the wires.

Every token enters on an input wire, toggles one balancer per layer, and
then takes a value from the counter of its output: the k-th token to leave
on output j gets j + k w. The toggle is one atomic step; the explorer has no
fetch-and-complement step, so the toggle is a fetch-and-add on the balancer
word, and only its low bit is used.

Flag that models a bug, for the tests:

- wiring="even-even": the first half merger gets the even outputs of both x
  and x' (and the second half merger the odd outputs of both). The network
  still balances, but it does not count.
"""

from __future__ import annotations

from typing import Any

from explorer import Memory, Proc


class Network:
    """A balancing network: balancers (layer, a, b) on wires 0..w-1 and an output order."""

    def __init__(self, w: int) -> None:
        self.w = w
        self.bals: list[tuple[int, int, int]] = []
        self.wire_depth = [0] * w
        self.out: list[int] = list(range(w))
        self.on: list[list[tuple[int, int]]] = []
        self.pos: dict[int, int] = {}

    def add(self, a: int, b: int) -> None:
        """Add a balancer after the last balancer on wire a and on wire b."""
        layer = max(self.wire_depth[a], self.wire_depth[b]) + 1
        self.wire_depth[a] = self.wire_depth[b] = layer
        self.bals.append((layer, a, b))

    def close(self, out: list[int]) -> "Network":
        self.out = list(out)
        self.pos = {x: j for j, x in enumerate(self.out)}
        self.on = [[] for _ in range(self.w)]
        for i, (layer, a, b) in enumerate(self.bals):
            self.on[a].append((layer, i))
            self.on[b].append((layer, i))
        for lst in self.on:
            lst.sort()
        return self

    @property
    def depth(self) -> int:
        return max(self.wire_depth, default=0)

    def next_balancer(self, x: int, layer: int) -> int | None:
        for lv, i in self.on[x]:
            if lv > layer:
                return i
        return None

    def quiescent_outputs(self, inputs: list[int]) -> list[int]:
        """The output counts after inputs[i] tokens entered on wire i and all left.
        A balancer that has seen t tokens has sent ceil(t/2) to its first
        wire and floor(t/2) to its second."""
        c = list(inputs)
        for _, a, b in sorted(self.bals):
            t = c[a] + c[b]
            c[a], c[b] = (t + 1) // 2, t // 2
        return [c[x] for x in self.out]

    def comparator_outputs(self, inputs: list[int]) -> list[int]:
        """The same network with a comparator in place of each balancer:
        the larger value goes to the first wire."""
        c = list(inputs)
        for _, a, b in sorted(self.bals):
            c[a], c[b] = max(c[a], c[b]), min(c[a], c[b])
        return [c[x] for x in self.out]


def has_step_property(y: list[int]) -> bool:
    return all(0 <= y[i] - y[j] <= 1 for i in range(len(y)) for j in range(i + 1, len(y)))


def step_sequence(total: int, k: int) -> list[int]:
    """The only sequence of length k with the step property and the given sum."""
    return [(total - i + k - 1) // k for i in range(k)]


def merger(net: Network, x: list[int], y: list[int], wiring: str = "even-odd") -> list[int]:
    k = len(x)
    if k == 1:  # @line L4
        net.add(x[0], y[0])
        return [x[0], y[0]]
    if wiring == "even-odd":
        z = merger(net, x[0::2], y[1::2], wiring)  # @line L5
        z2 = merger(net, x[1::2], y[0::2], wiring)  # @line L6
    else:
        z = merger(net, x[0::2], y[0::2], wiring)
        z2 = merger(net, x[1::2], y[1::2], wiring)
    out = []
    for a, b in zip(z, z2):  # @line L7
        net.add(a, b)
        out += [a, b]
    return out  # @line L8


def bitonic_wires(net: Network, v: list[int], wiring: str = "even-odd") -> list[int]:
    if len(v) == 1:  # @line L1
        return v
    h = len(v) // 2
    a, b = bitonic_wires(net, v[:h], wiring), bitonic_wires(net, v[h:], wiring)  # @line L2
    return merger(net, a, b, wiring)  # @line L3


def bitonic(w: int, wiring: str = "even-odd") -> Network:
    net = Network(w)
    return net.close(bitonic_wires(net, list(range(w)), wiring))


def merger_network(k: int) -> tuple[Network, list[int], list[int]]:
    """Merger[2k] alone, on wires 0..k-1 (input x) and k..2k-1 (input x')."""
    net = Network(2 * k)
    x, y = list(range(k)), list(range(k, 2 * k))
    return net.close(merger(net, x, y)), x, y


class Token:
    def __init__(self, cn: "BitonicCounter", wire: int) -> None:
        self.cn, self.wire = cn, wire

    def inc(self) -> Proc:
        return self.cn.inc(self.wire)


class BitonicCounter:
    def __init__(self, mem: Memory, net: Network) -> None:
        self.mem, self.net = mem, net
        for i in range(len(net.bals)):
            mem.init(("bal", i), 0)
        for j in range(net.w):
            mem.init(("out", j), 0)

    def token(self, wire: int) -> Token:
        return Token(self, wire)

    def inc(self, wire: int) -> Proc:
        net = self.net
        x, layer = wire, 0  # @line L9
        while True:
            i = net.next_balancer(x, layer)  # @line L10
            if i is None:
                break
            t = (yield ("faa", ("bal", i), 1)) % 2  # @line L11
            layer, a, b = net.bals[i]
            x = a if t == 0 else b  # @line L12
        j = net.pos[x]  # @line L13
        k = yield ("faa", ("out", j), 1)
        return j + net.w * k  # @line L14

    # Not a step: for the tests, the tokens that left on each output so far.
    def outputs(self) -> list[int]:
        return [self.mem.peek(("out", j)) for j in range(self.net.w)]


def quiescent_check(run: Any, truncated: bool = False) -> str | None:
    """A check for explorer.explore: in every quiescent point of the history
    (no operation pending), the values given out so far are exactly 0..n-1."""
    open_ops, values = 0, []
    for ev in run.history:
        if ev[1] == "inv":
            open_ops += 1
        else:
            open_ops -= 1
            values.append(ev[2])
        if open_ops == 0 and sorted(values) != list(range(len(values))):
            return f"not quiescently consistent: {sorted(values)}"
    return None
