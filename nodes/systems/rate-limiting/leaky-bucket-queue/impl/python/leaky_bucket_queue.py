# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leaky-bucket-queue/. The authors are listed in prov/QSRTMA.jsonl.

from collections import deque
from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]


class LeakyBucketQueue:
    """A leaky bucket used as a queue: a FIFO of at most K packets, sent at rate r.

    The capacity K counts the packets in the system, with the one that is
    being sent. A packet of size L takes L / r seconds to send, and the next
    packet starts when it ends. A packet that finds K packets in the system
    is dropped. Time is an explicit number; it must not go back.
    """

    def __init__(self, rate: Number, capacity: int, start: Number = 0) -> None:
        if rate <= 0 or capacity < 1:
            raise ValueError("need rate > 0 and capacity >= 1")
        self.rate = rate
        self.capacity = capacity
        self.fifo: deque = deque()  # (packet id, size); the head is being sent
        self.next: Number = start  # departure time of the head, when fifo is not empty
        self.now: Number = start
        self.sent: list[tuple[object, Number]] = []  # (packet id, departure time)

    def drain(self, t: Number) -> None:
        """Send every packet whose departure time is at most t."""
        if t < self.now:
            raise ValueError("time went back")
        self.now = t
        while self.fifo and self.next <= t:  # @line L6
            pid, _ = self.fifo.popleft()  # @line L7
            self.sent.append((pid, self.next))
            if self.fifo:  # @line L8
                self.next = self.next + Fraction(self.fifo[0][1]) / self.rate

    def arrive(self, t: Number, pid: object, size: Number = 1) -> bool:
        """A packet arrives at time t. Return True if it is queued, False if it is dropped."""
        self.drain(t)  # @line L1
        if len(self.fifo) >= self.capacity:  # @line L2
            return False
        if not self.fifo:  # @line L3
            self.next = t + Fraction(size) / self.rate
        self.fifo.append((pid, size))  # @line L4
        return True  # @line L5


def shape(arrivals: list[tuple[Number, Number]], rate: Number, capacity: int) -> list[Optional[Number]]:
    """Run the queue over (time, size) pairs; return each departure time, or None for a drop."""
    if not arrivals:
        return []
    q = LeakyBucketQueue(rate, capacity, arrivals[0][0])
    accepted = [q.arrive(t, i, size) for i, (t, size) in enumerate(arrivals)]
    q.drain(max(t for t, _ in arrivals) + sum(Fraction(s) for _, s in arrivals) / rate)
    out: list[Optional[Number]] = [None] * len(arrivals)
    for pid, d in q.sent:
        out[pid] = d
    assert all((d is not None) == a for d, a in zip(out, accepted))
    return out


def departures_by_recursion(arrivals: list[tuple[Number, Number]], rate: Number, capacity: int) -> list[Optional[Number]]:
    """The same queue for unit packets, from d_k = max(t_k, d_prev) + 1/r and the count of packets in the system."""
    out: list[Optional[Number]] = []
    last: Optional[Number] = None
    for t, _ in arrivals:
        in_system = 0
        if last is not None and last > t:
            q = rate * (last - t)
            in_system = int(q) if q == int(q) else int(q) + 1  # ceil
        if in_system >= capacity:
            out.append(None)
            continue
        last = (t if last is None else max(t, last)) + Fraction(1) / rate
        out.append(last)
    return out
