# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/red-random-early-detection/. The authors are listed in prov/A9935B.jsonl.

"""Random early detection (Floyd and Jacobson 1993).

The gateway keeps an exponentially weighted average of the queue length.
Between the two thresholds it marks an arriving packet with a probability
that grows with the average and with the number of unmarked packets since
the last mark, so that marks are spaced almost evenly.
"""

import random


class RED:
    """The marking decision of a RED gateway, one call per arriving packet."""

    def __init__(
        self,
        min_th: float,
        max_th: float,
        max_p: float,
        w_q: float,
        rng: random.Random,
        s: float = 1.0,
    ) -> None:
        if not 0 <= min_th < max_th:
            raise ValueError("need 0 <= min_th < max_th")
        if not 0 < max_p <= 1 or not 0 <= w_q <= 1:
            raise ValueError("need 0 < max_p <= 1 and 0 <= w_q <= 1")
        self.min_th = min_th
        self.max_th = max_th
        self.max_p = max_p
        self.w_q = w_q
        self.rng = rng
        self.s = s  # typical transmission time of a small packet
        self.avg = 0.0
        self.count = 0  # unmarked packets since the last mark
        self.idle_since: float | None = None

    def queue_empty(self, now: float) -> None:
        """Record the moment when the queue became empty."""
        self.idle_since = now

    def update_average(self, q: int, now: float = 0.0) -> float:
        if q == 0 and self.idle_since is not None:  # @line L2
            m = (now - self.idle_since) / self.s
            self.avg *= (1.0 - self.w_q) ** m
            self.idle_since = None
        else:
            self.avg = (1.0 - self.w_q) * self.avg + self.w_q * q  # @line L1
        return self.avg

    def marking_probability(self) -> float:
        """The probability p_a for the next packet, from avg and count."""
        avg = self.avg
        if avg < self.min_th:
            return 0.0
        if avg >= self.max_th:
            return 1.0
        p_b = self.max_p * (avg - self.min_th) / (self.max_th - self.min_th)  # @line L5
        if self.count * p_b >= 1.0 - p_b:  # then p_a >= 1
            return 1.0
        return p_b / (1.0 - self.count * p_b)  # @line L6

    def arrival(self, q: int, now: float = 0.0) -> bool:
        """Return True when the arriving packet is marked (or dropped).

        q is the queue length in packets when the packet arrives.
        """
        self.update_average(q, now)
        if self.avg < self.min_th:  # @line L3
            self.count = 0
            return False
        if self.avg >= self.max_th:  # @line L4
            self.count = 0
            return True
        p_a = self.marking_probability()
        if self.rng.random() < p_a:  # @line L7
            self.count = 0
            return True
        self.count += 1  # @line L8
        return False


def simulate_red_queue(
    red: RED, arrivals_per_slot: list[int], buffer: int
) -> tuple[list[int], list[float], int, int]:
    """A discrete-time queue that serves one packet per slot.

    Each slot, the arrivals of the slot come in one by one and RED decides on
    each; a marked packet is dropped. A packet is also dropped when the buffer
    is full. Then the link sends one packet. Returns the queue length and the
    average after each slot, the number of RED drops and of overflow drops.
    """
    q = 0
    qs: list[int] = []
    avgs: list[float] = []
    early = 0
    overflow = 0
    for slot, k in enumerate(arrivals_per_slot):
        for _ in range(k):
            if red.arrival(q, float(slot)):
                early += 1
            elif q >= buffer:
                overflow += 1
            else:
                q += 1
        if q > 0:
            q -= 1
            if q == 0:
                red.queue_empty(slot + 1.0)
        qs.append(q)
        avgs.append(red.avg)
    return qs, avgs, early, overflow
