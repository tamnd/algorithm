# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pie-aqm/. The authors are listed in prov/97E1GT.jsonl.

"""PIE, Proportional Integral controller Enhanced (Pan et al. 2013, RFC 8033).

Every T_UPDATE seconds PIE estimates the queueing delay and changes the drop
probability by alpha (qdelay - QDELAY_REF) + beta (qdelay - qdelay_old),
scaled down while the probability is small. At enqueue it drops each packet
with that probability, except during a burst allowance and when the queue is
short.

Time is a float in seconds, given by the caller. Sizes are in bytes. The
delay estimate uses Little's law with a known departure rate in bytes/s.
"""

import random


# Auto-tuning of RFC 8033, Section 4.2: (upper limit on drop_prob, divisor).
AUTO_TUNE = [(1e-6, 2048), (1e-5, 512), (1e-4, 128), (1e-3, 32), (1e-2, 8), (1e-1, 2)]


def auto_tune(p: float, drop_prob: float) -> float:
    for limit, divisor in AUTO_TUNE:
        if drop_prob < limit:
            return p / divisor
    return p


class PIE:
    def __init__(
        self,
        rate: float,
        rng: random.Random,
        qdelay_ref: float = 0.015,
        t_update: float = 0.015,
        alpha: float = 0.125,
        beta: float = 1.25,
        max_burst: float = 0.150,
        mean_pktsize: int = 1500,
    ) -> None:
        self.rate = rate  # departure rate in bytes per second
        self.rng = rng
        self.ref = qdelay_ref
        self.t_update = t_update
        self.alpha = alpha
        self.beta = beta
        self.max_burst = max_burst
        self.mean_pktsize = mean_pktsize
        self.drop_prob = 0.0
        self.qdelay_old = 0.0
        self.burst_allowance = max_burst
        self.bytes = 0  # bytes in the queue

    def qdelay(self) -> float:
        return self.bytes / self.rate  # Little's law

    def enqueue(self, size: int) -> bool:
        """Return True to accept the packet, False to drop it."""
        half = self.ref / 2
        if self.drop_prob == 0 and self.qdelay() < half and self.qdelay_old < half:
            self.burst_allowance = self.max_burst  # @line L1
        if self.burst_allowance > 0:  # @line L2
            return self._accept(size)
        if (self.qdelay_old < half and self.drop_prob < 0.2) or (
            self.bytes <= 2 * self.mean_pktsize
        ):  # @line L3
            return self._accept(size)
        if self.rng.random() < self.drop_prob:  # @line L4
            return False
        return self._accept(size)

    def _accept(self, size: int) -> bool:
        self.bytes += size
        return True

    def dequeue(self, size: int) -> None:
        self.bytes -= size

    def update(self) -> None:
        """Run once every T_UPDATE seconds."""
        qdelay = self.qdelay()  # @line L5
        p = self.alpha * (qdelay - self.ref) + self.beta * (qdelay - self.qdelay_old)  # @line L6
        p = auto_tune(p, self.drop_prob)  # @line L7
        self.drop_prob += p  # @line L8
        if qdelay == 0 and self.qdelay_old == 0:  # @line L9
            self.drop_prob *= 0.98
        self.drop_prob = min(1.0, max(0.0, self.drop_prob))  # @line L10
        self.qdelay_old = qdelay  # @line L11
        self.burst_allowance = max(0.0, self.burst_allowance - self.t_update)


def simulate(
    pie: PIE, arrivals: list[float], size: int = 1500, until: float | None = None
) -> dict:
    """Run a FIFO link of rate pie.rate behind PIE.

    arrivals is a sorted list of arrival times in seconds. Return the drop
    times, the queueing delay of each sent packet as (arrival time, delay),
    and the state after each update as (time, drop_prob, qdelay sample).
    """
    tx = size / pie.rate
    if until is None:
        until = arrivals[-1] if arrivals else 0.0
    fifo: list[float] = []  # arrival times of queued packets
    head = 0
    busy_until = 0.0  # time when the packet in service leaves
    in_service = False
    next_update = pie.t_update
    drops: list[float] = []  # drop times
    delays: list[tuple[float, float]] = []
    probs: list[tuple[float, float, float]] = []
    i = 0
    n = len(arrivals)
    inf = float("inf")
    while True:
        ta = arrivals[i] if i < n else inf
        td = busy_until if in_service else inf
        tu = next_update if next_update <= until else inf
        t = min(ta, td, tu)
        if t == inf:
            break
        if td == t:  # a departure; start the next packet
            in_service = False
            pie.dequeue(size)
            if head < len(fifo):
                delays.append((fifo[head], t - fifo[head]))
                head += 1
                in_service = True
                busy_until = t + tx
        elif tu == t:
            pie.update()
            probs.append((t, pie.drop_prob, pie.qdelay_old))
            next_update += pie.t_update
        else:
            i += 1
            if pie.enqueue(size):
                if not in_service:
                    delays.append((t, 0.0))
                    in_service = True
                    busy_until = t + tx
                else:
                    fifo.append(t)
            else:
                drops.append(t)
    return {"drops": drops, "delays": delays, "probs": probs}
