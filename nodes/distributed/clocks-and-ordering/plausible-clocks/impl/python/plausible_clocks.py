# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plausible-clocks/. The authors are listed in prov/DY2814.jsonl.

"""Plausible clocks of constant size (Torres-Rojas and Ahamad 1999).

A plausible clock never orders a causal pair the wrong way and never calls a
causal pair concurrent. It may order two concurrent events. Three clocks:

- REV, R-entries vector: site i uses entry i mod R of a vector of R entries.
- KLA, K-Lamport: entry 0 is a Lamport clock, entry k is the largest entry
  k - 1 received in a message.
- Comb: the product of a REV and a KLA clock; it orders a pair only if both do.

A stamp is (site, tuple). Executions use the format
(p, "local", None), (p, "send", (q, mid)), (p, "recv", mid).
Each event costs O(R) or O(K) time; each stamp has R or K integers.
"""

import random

Stamp = tuple[int, tuple[int, ...]]


class REVClock:
    """R-entries vector clock of one site."""

    def __init__(self, site: int, r: int) -> None:
        """Precondition: r >= 1."""
        self.site = site
        self.r = r
        self.v = [0] * r  # @line L1

    def tick(self) -> Stamp:
        """A local event. O(R)."""
        self.v[self.site % self.r] += 1  # @line L2
        return (self.site, tuple(self.v))  # @line L3

    def send(self) -> Stamp:
        """A send event: the stamp to attach."""
        return self.tick()  # @line L4

    def receive(self, w: Stamp) -> Stamp:
        """A receive event of a message with stamp w. O(R)."""
        for k in range(self.r):  # @line L5
            self.v[k] = max(self.v[k], w[1][k])  # @line L6
        return self.tick()  # @line L7


def rev_before(a: Stamp, b: Stamp, r: int) -> bool:
    """The REV relation a ->_P b. O(R)."""
    (sa, va), (sb, vb) = a, b
    if sa == sb:  # @line L8
        return va[sa % r] < vb[sb % r]
    return all(x <= y for x, y in zip(va, vb)) and va[sb % r] < vb[sb % r]  # @line L9


class KLAClock:
    """K-Lamport clock of one site."""

    def __init__(self, site: int, k: int) -> None:
        """Precondition: k >= 2."""
        self.site = site
        self.v = [0] * k

    def tick(self) -> Stamp:
        """A local event: Lamport tick of entry 0."""
        self.v[0] += 1
        return (self.site, tuple(self.v))

    def send(self) -> Stamp:
        """A send event: the stamp to attach."""
        return self.tick()

    def receive(self, w: Stamp) -> Stamp:
        """A receive event. Entry k takes the largest received entry k - 1. O(K)."""
        old = self.v[:]
        self.v[0] = max(old[0], w[1][0]) + 1
        for k in range(1, len(self.v)):
            self.v[k] = max(old[k], w[1][k - 1])
        return (self.site, tuple(self.v))


def kla_before(a: Stamp, b: Stamp) -> bool:
    """The KLA relation a ->_P b. O(K)."""
    (sa, va), (sb, vb) = a, b
    if sa == sb:
        return va[0] < vb[0]
    return all(va[k] <= vb[k + 1] for k in range(len(va) - 1))


class CombClock:
    """The product of an REV clock with R entries and a KLA clock with K entries."""

    def __init__(self, site: int, r: int, k: int) -> None:
        self.rev = REVClock(site, r)
        self.kla = KLAClock(site, k)

    def tick(self) -> tuple[Stamp, Stamp]:
        return (self.rev.tick(), self.kla.tick())

    def send(self) -> tuple[Stamp, Stamp]:
        return self.tick()

    def receive(self, w: tuple[Stamp, Stamp]) -> tuple[Stamp, Stamp]:
        return (self.rev.receive(w[0]), self.kla.receive(w[1]))


def comb_before(a: tuple[Stamp, Stamp], b: tuple[Stamp, Stamp], r: int) -> bool:
    """Comb orders a before b only if both component clocks do."""
    return rev_before(a[0], b[0], r) and kla_before(a[1], b[1])


def timestamp_execution(clocks: list, execution: list[tuple]) -> list:
    """Run the given per-site clocks over the execution. Return the stamp of each event."""
    msg: dict[int, object] = {}
    out = []
    for p, kind, x in execution:
        if kind == "local":
            out.append(clocks[p].tick())
        elif kind == "send":
            t = clocks[p].send()
            msg[x[1]] = t
            out.append(t)
        elif kind == "recv":
            out.append(clocks[p].receive(msg[x]))
        else:
            raise ValueError(f"unknown step kind {kind!r}")
    return out


def random_execution(n: int, steps: int, rng: random.Random, p_send: float = 0.4, p_recv: float = 0.4) -> list[tuple]:
    """A seeded random execution. In-transit messages are received in a random order."""
    in_transit: list[tuple[int, int]] = []
    out: list[tuple] = []
    mid = 0
    for _ in range(steps):
        r = rng.random()
        if r < p_recv and in_transit:
            m, q = in_transit.pop(rng.randrange(len(in_transit)))
            out.append((q, "recv", m))
        elif r < p_recv + p_send and n > 1:
            p = rng.randrange(n)
            q = rng.randrange(n - 1)
            q += q >= p
            out.append((p, "send", (q, mid)))
            in_transit.append((mid, q))
            mid += 1
        else:
            out.append((rng.randrange(n), "local", None))
    return out
