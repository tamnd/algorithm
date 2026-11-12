# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/codel/. The authors are listed in prov/74M4VC.jsonl.

"""CoDel, controlled delay (Nichols and Jacobson 2012, RFC 8289).

The queue stamps each packet when it arrives. At each dequeue, CoDel looks at
the sojourn time of the head packet. When the sojourn time has stayed at or
above TARGET for INTERVAL, CoDel enters the dropping state and drops packets
at times set by the control law next = t + INTERVAL / sqrt(count).

Time is a float in milliseconds, given by the caller. Sizes are in bytes.
"""

import math
from collections import deque


class CoDel:
    def __init__(
        self, target: float = 5.0, interval: float = 100.0, maxpacket: int = 1500
    ) -> None:
        self.target = target
        self.interval = interval
        self.maxpacket = maxpacket
        self.queue: deque[tuple[float, int, int]] = deque()  # (stamp, size, id)
        self.bytes = 0
        self.first_above_time: float | None = None
        self.drop_next = 0.0
        self.count = 0
        self.lastcount = 0
        self.dropping = False
        self.drops: list[tuple[float, int]] = []  # (time, packet id)
        self.entries: list[tuple[float, int]] = []  # (time, count) at each entry

    def control_law(self, t: float, count: int) -> float:
        return t + self.interval / math.sqrt(count)

    def enqueue(self, now: float, size: int, pid: int) -> None:
        self.queue.append((now, size, pid))
        self.bytes += size

    def _dodequeue(self, now: float) -> tuple[tuple[float, int, int] | None, bool]:
        if not self.queue:  # @line L1
            self.first_above_time = None
            return None, False
        p = self.queue.popleft()  # @line L2
        self.bytes -= p[1]
        sojourn = now - p[0]
        if sojourn < self.target or self.bytes <= self.maxpacket:  # @line L3
            self.first_above_time = None
            return p, False
        if self.first_above_time is None:  # @line L4
            self.first_above_time = now + self.interval
            return p, False
        return p, now >= self.first_above_time  # @line L5

    def _drop(self, now: float, p: tuple[float, int, int]) -> None:
        self.drops.append((now, p[2]))

    def dequeue(self, now: float) -> tuple[float, int, int] | None:
        """Return the packet to send now, or None if the queue is empty."""
        p, ok = self._dodequeue(now)  # @line L6
        if p is None:  # @line L7
            self.dropping = False
            return None
        if self.dropping:  # @line L8
            if not ok:  # @line L9
                self.dropping = False
            while self.dropping and now >= self.drop_next:  # @line L10
                self._drop(now, p)  # @line L11
                self.count += 1
                p, ok = self._dodequeue(now)
                if not ok:  # @line L12
                    self.dropping = False
                else:
                    self.drop_next = self.control_law(self.drop_next, self.count)
        elif ok:  # @line L13
            self._drop(now, p)  # @line L14
            p, ok = self._dodequeue(now)
            self.dropping = True
            delta = self.count - self.lastcount  # @line L15
            self.count = 1
            if delta > 1 and now - self.drop_next < 16 * self.interval:  # @line L16
                self.count = delta
            self.drop_next = self.control_law(now, self.count)  # @line L17
            self.lastcount = self.count
            self.entries.append((now, self.count))
        return p  # @line L18


def simulate(
    codel: CoDel, arrivals: list[float], tx: float, size: int = 1500
) -> list[tuple[int, float]]:
    """Run a link that needs tx ms per packet. Return (id, sojourn) per sent packet.

    arrivals is a sorted list of arrival times in ms. Packet i arrives at
    arrivals[i]. The link calls dequeue whenever it is free.
    """
    sent: list[tuple[int, float]] = []
    i = 0
    n = len(arrivals)
    t = 0.0
    while i < n or codel.queue:
        if not codel.queue and t < arrivals[i]:
            t = arrivals[i]
        while i < n and arrivals[i] <= t:
            codel.enqueue(arrivals[i], size, i)
            i += 1
        p = codel.dequeue(t)
        if p is None:
            continue
        sent.append((p[2], t - p[0]))
        t += tx
    return sent
