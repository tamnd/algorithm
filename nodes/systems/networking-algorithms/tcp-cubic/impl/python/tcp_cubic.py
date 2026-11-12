# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tcp-cubic/. The authors are listed in prov/NC11TV.jsonl.

"""CUBIC congestion avoidance (RFC 9438), with the window in segments and
time in seconds. A round model drives it: in each round trip the sender gets
one ACK per segment of the window, and a loss happens when the window is
above the pipe size (the bandwidth-delay product plus the buffer).
"""

import math

C = 0.4
BETA = 0.7


def w_cubic(t: float, w_max: float, k: float, c: float = C) -> float:
    """The cubic window function C (t - K)^3 + W_max."""
    return c * (t - k) ** 3 + w_max


def k_of(w_max: float, cwnd_epoch: float, c: float = C) -> float:
    """The time K at which the cubic function returns to W_max."""
    return math.copysign(abs((w_max - cwnd_epoch) / c) ** (1 / 3), w_max - cwnd_epoch)


class Cubic:
    """CUBIC state for one sender in congestion avoidance."""

    def __init__(self, cwnd: float, rtt: float, fast_convergence: bool = False) -> None:
        self.cwnd = float(cwnd)
        self.rtt = rtt
        self.fast_convergence = fast_convergence
        self.w_max = float(cwnd)
        self.cwnd_prior = float(cwnd)
        self.ssthresh = float(cwnd)
        self.t_epoch = 0.0
        self.k = 0.0
        self.w_est = float(cwnd)
        self.region = "cubic"

    def on_ack(self, now: float, acked: int = 1) -> None:
        """A new ACK for acked segments arrives at time now (seconds)."""
        t = now - self.t_epoch  # @line L1
        w_next = w_cubic(t + self.rtt, self.w_max, self.k)  # @line L2
        target = min(max(w_next, self.cwnd), 1.5 * self.cwnd)  # @line L3
        alpha = 1.0 if self.w_est >= self.cwnd_prior else 3 * (1 - BETA) / (1 + BETA)
        self.w_est += alpha * acked / self.cwnd  # @line L4
        if w_cubic(t, self.w_max, self.k) < self.w_est:  # @line L5
            self.cwnd = self.w_est
            self.region = "reno-friendly"
        else:  # @line L6
            self.cwnd += (target - self.cwnd) / self.cwnd
            self.region = "concave" if self.cwnd < self.w_max else "convex"

    def on_loss(self, now: float) -> None:
        """A congestion event at time now: multiplicative decrease by BETA."""
        if self.fast_convergence and self.cwnd < self.w_max:  # @line L7
            self.w_max = self.cwnd * (1 + BETA) / 2
        else:
            self.w_max = self.cwnd
        self.cwnd_prior = self.cwnd
        self.ssthresh = self.cwnd * BETA  # @line L8
        self.cwnd = max(self.ssthresh, 2.0)
        self.t_epoch = now  # @line L9
        self.w_est = self.cwnd
        self.k = k_of(self.w_max, self.cwnd)


def run_rounds(cc: Cubic, rounds: int, pipe: float) -> list[tuple[float, float, bool]]:
    """Drive cc for a number of round trips. A round whose window is above
    pipe ends with a loss. Returns (time, cwnd at the start, loss) per round.
    Cost: O(total segments acknowledged).
    """
    out = []
    now = 0.0
    for _ in range(rounds):
        w = cc.cwnd
        lost = w > pipe
        out.append((now, w, lost))
        acks = max(int(w), 1)
        for j in range(acks):
            cc.on_ack(now + cc.rtt * (j + 1) / acks)
        now += cc.rtt
        if lost:
            cc.on_loss(now)
    return out
