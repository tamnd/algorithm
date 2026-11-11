# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/counting-network/. The authors are listed in prov/BHV1FX.jsonl.

"""Counting networks (Aspnes, Herlihy and Shavit, JACM 1994).

A balancing network of width w is a set of balancers on w wires. A balancer
joins two wires a < b. It is a toggle: the tokens that reach it leave on
wire a, then b, then a, and so on, whichever wire they came in on. A token
enters on an input wire, passes the balancers on its path in layer order,
and leaves on an output wire. The network is a counting network if, in every
quiescent state, the numbers y_0, ..., y_{w-1} of tokens that left on the
outputs have the step property: 0 <= y_i - y_j <= 1 for all i < j.

A shared counter: output j has a local counter c_j. The token that is the
k-th to leave on output j (k = 0, 1, ...) gets the value j + k w. In a
quiescent state after n tokens, the values given out are exactly 0..n-1.

This file builds two counting networks:

- periodic(w): the periodic network, log w copies of Block[w] in series. A
  Block[n] is one layer of balancers that join wire i with wire n-1-i,
  followed by a Block[n/2] on each half. This is the balanced periodic
  sorting network of Dowd, Perl, Rudolph and Saks with each comparator
  replaced by a balancer.
- bitonic(w): the bitonic network, Bitonic[2k] = two Bitonic[k] followed by
  Merger[2k]. It has its own page, bitonic-counting-network.

The toggle of a balancer is one atomic step. The explorer has no
fetch-and-complement step, so the toggle is a fetch-and-add on the balancer
word, and only its low bit is used.

Flag that models a bug, for the tests:

- atomic=False: the toggle is a read followed by a write. Two tokens can
  read the same state and leave on the same wire.
"""

from __future__ import annotations

from typing import Any, Callable

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

    def close(self, out: list[int] | None = None) -> "Network":
        """Fix the output order (out[j] is the wire of output j) and index the balancers."""
        if out is not None:
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
        """The first balancer on wire x after the given layer, or None."""
        for lv, i in self.on[x]:
            if lv > layer:
                return i
        return None

    def quiescent_outputs(self, inputs: list[int]) -> list[int]:
        """The output counts after inputs[i] tokens entered on wire i and all left.

        In a quiescent state a balancer that has seen t tokens has sent
        ceil(t/2) to its first wire and floor(t/2) to its second, whatever
        the order in which they came.
        """
        c = list(inputs)
        for _, a, b in sorted(self.bals):
            t = c[a] + c[b]
            c[a], c[b] = (t + 1) // 2, t // 2
        return [c[x] for x in self.out]


def has_step_property(y: list[int]) -> bool:
    return all(0 <= y[i] - y[j] <= 1 for i in range(len(y)) for j in range(i + 1, len(y)))


def block(net: Network, v: list[int]) -> None:
    n = len(v)
    if n == 2:  # @line L8
        net.add(v[0], v[1])
        return
    for i in range(n // 2):  # @line L9
        net.add(v[i], v[n - 1 - i])
    block(net, v[: n // 2])  # @line L10
    block(net, v[n // 2:])


def periodic(w: int) -> Network:
    net = Network(w)
    if w >= 2:
        for _ in range(w.bit_length() - 1):  # @line L11
            block(net, list(range(w)))
    return net.close()


def bitonic(w: int) -> Network:
    net = Network(w)

    def merger(x: list[int], y: list[int]) -> list[int]:
        if len(x) == 1:
            net.add(x[0], y[0])
            return [x[0], y[0]]
        z = merger(x[0::2], y[1::2])
        z2 = merger(x[1::2], y[0::2])
        out = []
        for a, b in zip(z, z2):
            net.add(a, b)
            out += [a, b]
        return out

    def bit(v: list[int]) -> list[int]:
        if len(v) == 1:
            return v
        h = len(v) // 2
        return merger(bit(v[:h]), bit(v[h:]))

    return net.close(bit(list(range(w))))


class Token:
    """The view of the counter for one process: every token enters on one input wire."""

    def __init__(self, cn: "CountingNetwork", wire: int) -> None:
        self.cn, self.wire = cn, wire

    def inc(self) -> Proc:
        return self.cn.inc(self.wire)


class CountingNetwork:
    def __init__(self, mem: Memory, net: Network, atomic: bool = True) -> None:
        self.mem, self.net, self.atomic = mem, net, atomic
        for i in range(len(net.bals)):
            mem.init(("bal", i), 0)
        for j in range(net.w):
            mem.init(("out", j), 0)

    def token(self, wire: int) -> Token:
        return Token(self, wire)

    def inc(self, wire: int) -> Proc:
        net = self.net
        x, layer = wire, 0  # @line L1
        while True:
            i = net.next_balancer(x, layer)  # @line L2
            if i is None:
                break
            if self.atomic:
                t = (yield ("faa", ("bal", i), 1)) % 2  # @line L3
            else:
                v = yield ("read", ("bal", i))
                yield ("write", ("bal", i), v + 1)
                t = v % 2
            layer, a, b = net.bals[i]
            x = a if t == 0 else b  # @line L4
        j = net.pos[x]  # @line L5
        k = yield ("faa", ("out", j), 1)  # @line L6
        return j + net.w * k  # @line L7

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


def make_check(*checks: Callable[..., str | None]) -> Callable[..., str | None]:
    def check(run: Any, truncated: bool = False) -> str | None:
        for c in checks:
            msg = c(run, truncated)
            if msg:
                return msg
        return None

    return check
