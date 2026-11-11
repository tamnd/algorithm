# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phi-accrual-failure-detector/. The authors are listed in prov/TY0JW4.jsonl.

"""The phi accrual failure detector (Hayashibara, Defago, Yared and
Katayama 2004).

The detector keeps a sliding window of the last w heartbeat inter-arrival
times and models the next one as normal with the window's mean and standard
deviation. At time t_now, with the last heartbeat at T_last,

    phi(t_now) = -log10(P_later(t_now - T_last)),  P_later(x) = 1 - F(x),

where F is the normal CDF. The application suspects the process when phi
reaches its threshold Phi; if the model is right, the next heartbeat comes
after that moment with probability 10^(-Phi).

Two variants used in practice are included for comparison:

* exponential_phi: P_later(x) = exp(-x / mean), so phi = x / (mean ln 10),
  the model of Apache Cassandra's failure detector;
* logistic_phi: the logistic approximation of the normal tail used by Akka,
  with the mean shifted by an acceptable pause and the standard deviation
  floored at a minimum.
"""

import math
from collections import deque
from statistics import NormalDist


class PhiAccrualDetector:
    def __init__(self, window: int = 1000, min_std: float = 0.0):
        self.window = window
        self.min_std = min_std
        self.samples: deque[float] = deque()
        self.total = 0.0
        self.total_sq = 0.0
        self.last: float | None = None

    def heartbeat(self, t: float) -> None:
        if self.last is not None:
            x = t - self.last                                            # @line L1
            self.samples.append(x)
            self.total += x
            self.total_sq += x * x
            if len(self.samples) > self.window:
                y = self.samples.popleft()
                self.total -= y
                self.total_sq -= y * y
        self.last = t                                                    # @line L2

    def mean_std(self) -> tuple[float, float]:
        m = len(self.samples)
        mean = self.total / m                                            # @line L3
        var = max(0.0, self.total_sq / m - mean * mean)
        return mean, max(math.sqrt(var), self.min_std)

    def phi(self, now: float) -> float:
        mean, std = self.mean_std()
        delta = now - self.last                                          # @line L4
        # 1 - F(delta) through erfc, which keeps precision in the far tail
        p_later = 0.5 * math.erfc((delta - mean) / (std * math.sqrt(2)))  # @line L5
        if p_later <= 0:
            return math.inf
        return -math.log10(p_later)                                      # @line L6

    def suspect(self, now: float, threshold: float) -> bool:
        return self.phi(now) >= threshold                                # @line L7

    def suspicion_time(self, threshold: float) -> float:
        """The time after the last heartbeat at which phi reaches threshold."""
        mean, std = self.mean_std()
        return mean - std * NormalDist().inv_cdf(10 ** (-threshold))


def exponential_phi(delta: float, mean: float) -> float:
    """Phi under an exponential model of inter-arrival times, as in
    Cassandra: -log10(exp(-delta / mean)) = delta / (mean ln 10)."""
    return delta / (mean * math.log(10))


def logistic_phi(delta: float, mean: float, std: float,
                 pause: float = 0.0, min_std: float = 0.0) -> float:
    """Phi with the logistic approximation of the normal tail, as in Akka.
    The mean is shifted by the acceptable heartbeat pause and the standard
    deviation is at least min_std."""
    mean = mean + pause
    std = max(std, min_std)
    y = (delta - mean) / std
    a = y * (1.5976 + 0.070566 * y * y)
    if delta > mean:
        # -log10(e / (1 + e)) with e = exp(-a), written so that it does not
        # underflow when e is tiny
        return a / math.log(10) + math.log10(1 + math.exp(-a))
    e = math.exp(-a)
    return -math.log10(1 - 1 / (1 + e))


def mistake_rate(intervals, threshold: float, window: int = 1000, warmup: int = 100) -> float:
    """Feed heartbeats with the given inter-arrival times. For each interval
    after the warm-up, check whether phi reached the threshold before the
    next heartbeat came, a wrong suspicion of a live process. Returns the
    fraction of such intervals."""
    d = PhiAccrualDetector(window)
    t = 0.0
    d.heartbeat(t)
    wrong = counted = 0
    for k, x in enumerate(intervals):
        if k >= warmup:
            counted += 1
            if x >= d.suspicion_time(threshold):
                wrong += 1
        t += x
        d.heartbeat(t)
    return wrong / counted
