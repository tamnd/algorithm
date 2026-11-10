# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vector-clocks/. The authors are listed in prov/GQ5H12.jsonl.

"""Vector clocks (Fidge 1988, Mattern 1989).

The model is the asynchronous message-passing model with n processes
0 .. n - 1 and reliable channels that need not be FIFO. An execution is a
list of steps in the order they occur:

    (p, "local", None)      process p does a local event
    (p, "send", (q, mid))   process p sends message mid to process q
    (p, "recv", mid)        process p receives message mid

Each step is one event. Each operation costs O(n) time; each process stores
n integers and each message carries n integers.
"""

import random

Stamp = tuple[int, ...]


class VectorClock:
    """The vector clock V_i of process i among n processes."""

    def __init__(self, n: int, i: int) -> None:
        """Precondition: 0 <= i < n."""
        self.i = i
        self.v = [0] * n  # @line L1

    def tick(self) -> Stamp:
        """A local event. Return its timestamp. O(n) for the copy."""
        self.v[self.i] += 1  # @line L2
        return tuple(self.v)  # @line L3

    def send(self) -> Stamp:
        """A send event. Return the timestamp to attach to the message."""
        return self.tick()  # @line L4

    def receive(self, w: Stamp) -> Stamp:
        """A receive event of a message with timestamp w. O(n)."""
        for k in range(len(self.v)):  # @line L5
            self.v[k] = max(self.v[k], w[k])  # @line L6
        return self.tick()  # @line L7


def leq(v: Stamp, w: Stamp) -> bool:
    """V <= W in every entry. O(n)."""
    return all(a <= b for a, b in zip(v, w))  # @line L8


def less(v: Stamp, w: Stamp) -> bool:
    """V < W: V <= W and V != W. For event stamps this is happened-before."""
    return leq(v, w) and v != w  # @line L9


def concurrent(v: Stamp, w: Stamp) -> bool:
    """Neither stamp is <= the other. For event stamps this is concurrency."""
    return not leq(v, w) and not leq(w, v)  # @line L10


def less_fast(v: Stamp, i: int, w: Stamp) -> bool:
    """The O(1) test: for an event e of process i and an event f != e, e -> f iff V(e)[i] <= V(f)[i]."""
    return v[i] <= w[i]


def timestamp_execution(n: int, execution: list[tuple]) -> list[Stamp]:
    """Run one vector clock per process. Return V(e) for each event, in order. Time O(n) per event."""
    clocks = [VectorClock(n, p) for p in range(n)]
    stamp_of_msg: dict[int, Stamp] = {}
    out: list[Stamp] = []
    for p, kind, x in execution:
        if kind == "local":
            out.append(clocks[p].tick())
        elif kind == "send":
            t = clocks[p].send()
            stamp_of_msg[x[1]] = t
            out.append(t)
        elif kind == "recv":
            out.append(clocks[p].receive(stamp_of_msg[x]))
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
