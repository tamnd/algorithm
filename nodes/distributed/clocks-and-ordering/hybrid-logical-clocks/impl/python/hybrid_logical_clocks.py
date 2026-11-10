# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-logical-clocks/. The authors are listed in prov/F6ZVRW.jsonl.

"""Hybrid logical clocks (Kulkarni, Demirbas, Madappa, Avva and Leone 2014).

A timestamp is a pair (l, c). The part l is the largest physical clock value
that the process has heard of, and c counts events that share that l. Pairs
are compared lexicographically. If e happened before f, then (l, c) of e is
smaller than (l, c) of f. If physical clocks differ by at most eps, then
0 <= l - pt <= eps at every event. Each operation costs O(1) time and space.
"""

import random


class HybridLogicalClock:
    """The clock of one process. Each method takes the current physical clock reading pt."""

    def __init__(self) -> None:
        self.l = 0  # @line L1
        self.c = 0

    def send_or_local(self, pt: int) -> tuple[int, int]:
        """A local or send event. Return the timestamp of the event, to be put on a sent message."""
        old = self.l  # @line L2
        self.l = max(old, pt)  # @line L3
        self.c = self.c + 1 if self.l == old else 0  # @line L4
        return (self.l, self.c)

    def receive(self, lm: int, cm: int, pt: int) -> tuple[int, int]:
        """A receive event of a message with timestamp (lm, cm). Return the timestamp of the event."""
        old = self.l  # @line L5
        self.l = max(old, lm, pt)
        if self.l == old and self.l == lm:  # @line L6
            self.c = max(self.c, cm) + 1
        elif self.l == old:  # @line L7
            self.c = self.c + 1
        elif self.l == lm:  # @line L8
            self.c = cm + 1
        else:  # @line L9
            self.c = 0
        return (self.l, self.c)


def timestamp_execution(n: int, execution: list[tuple], pts: list[int]) -> list[tuple[int, int]]:
    """Run the clocks over an execution; pts[e] is the physical clock reading of the process at event e."""
    clocks = [HybridLogicalClock() for _ in range(n)]
    stamp_of_msg: dict[int, tuple[int, int]] = {}
    out: list[tuple[int, int]] = []
    for e, (p, kind, x) in enumerate(execution):
        if kind == "recv":
            lm, cm = stamp_of_msg[x]
            out.append(clocks[p].receive(lm, cm, pts[e]))
        else:
            t = clocks[p].send_or_local(pts[e])
            if kind == "send":
                stamp_of_msg[x[1]] = t
            out.append(t)
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


def skewed_readings(n: int, execution: list[tuple], eps: int, rng: random.Random, strict: bool) -> tuple[list[int], list[int]]:
    """Seeded physical clock readings with skew at most eps.

    Real time t is non-decreasing along the execution. Process p reads
    t + offset[p] with offset[p] in [0, eps], so any two readings taken at the
    same real time differ by at most eps. With strict=True, real time grows by
    at least 1 at each event, so each process reads strictly increasing values.
    Return (real times, readings).
    """
    offset = [rng.randint(0, eps) for _ in range(n)]
    t = 1  # readings are positive, so no event shares l = 0 with the initial state
    times: list[int] = []
    pts: list[int] = []
    for p, _, _ in execution:
        t += rng.randint(1, 3) if strict else rng.choice([0, 0, 1, 2])
        times.append(t)
        pts.append(t + offset[p])
    return times, pts
