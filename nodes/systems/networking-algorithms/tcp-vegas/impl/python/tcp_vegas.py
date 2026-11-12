# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tcp-vegas/. The authors are listed in prov/NPTDBB.jsonl.

"""TCP Vegas congestion avoidance in a fluid model of one bottleneck link.

The link serves c packets per time unit. Flow i has propagation round-trip
time d[i] and window w[i] packets. When the windows overfill the pipe, a
queue builds and adds the same queueing delay q to every round trip; q is
the value with sum(w[i] / (d[i] + q)) = c. Each round, every active flow
measures its RTT d[i] + q and runs the Vegas rule once.
"""

from dataclasses import dataclass, field


def queueing_delay(w: list[float], d: list[float], c: float) -> float:
    """The queueing delay q >= 0 of the fluid model, by bisection.

    Precondition: c > 0 and every d[i] > 0. Cost O(n log(1/eps)).
    """
    if sum(wi / di for wi, di in zip(w, d)) <= c:
        return 0.0
    lo, hi = 0.0, sum(w) / c
    for _ in range(80):
        mid = (lo + hi) / 2
        if sum(wi / (di + mid) for wi, di in zip(w, d)) > c:
            lo = mid
        else:
            hi = mid
    return hi


class VegasFlow:
    """The Vegas window rule for one flow; windows are whole packets."""

    def __init__(self, w: int, alpha: float = 1.0, beta: float = 3.0) -> None:
        if not 0 < alpha <= beta:
            raise ValueError("need 0 < alpha <= beta")
        self.cwnd = w
        self.alpha = alpha
        self.beta = beta
        self.base_rtt = float("inf")
        self.diff = 0.0

    def on_round(self, rtt: float) -> None:
        """Run once per round trip with the RTT measured in that round."""
        self.base_rtt = min(self.base_rtt, rtt)  # @line L2
        expected = self.cwnd / self.base_rtt  # @line L3
        actual = self.cwnd / rtt  # @line L4
        self.diff = (expected - actual) * self.base_rtt  # @line L5
        if self.diff < self.alpha:  # @line L6
            self.cwnd += 1
        elif self.diff > self.beta:  # @line L7
            self.cwnd = max(self.cwnd - 1, 2)
        # @line L8: otherwise the window stays


@dataclass
class Trace:
    windows: list[list[int]] = field(default_factory=list)
    rates: list[list[float]] = field(default_factory=list)
    delay: list[float] = field(default_factory=list)


def simulate(d: list[float], c: float, rounds: int, start: list[int] | None = None, w0: int = 2, alpha: float = 1.0, beta: float = 3.0) -> tuple[list[VegasFlow], Trace]:
    """Run Vegas flows on one link for a number of synchronous rounds.

    Flow i joins at round start[i]. Before a flow joins, its window is 0.
    The trace keeps the windows, the rates w/(d + q) and q of each round.
    """
    n = len(d)
    start = start or [0] * n
    flows = [VegasFlow(w0, alpha, beta) for _ in range(n)]
    tr = Trace()
    for r in range(rounds):
        act = [i for i in range(n) if start[i] <= r]
        w = [flows[i].cwnd if i in act else 0 for i in range(n)]
        q = queueing_delay(w, d, c)
        tr.windows.append(w)
        tr.rates.append([w[i] / (d[i] + q) for i in range(n)])
        tr.delay.append(q)
        for i in act:
            flows[i].on_round(d[i] + q)  # @line L1
    return flows, tr
