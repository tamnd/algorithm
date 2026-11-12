# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-response-time/. The authors are listed in prov/4ZQE1H.jsonl.

"""Least response time load balancing.

Each backend j keeps a smoothed response time L[j] (an exponential moving
average with factor alpha) and its number of requests in flight a[j]. pick()
returns the up backend with the smallest estimated time to finish,
e[j] = L[j] * (a[j] + 1), divided by the weight w[j]. done(j, x) records a
response time x. Cost: Theta(n) per pick, Theta(1) per done.

mode="latency" ranks by L[j] alone. It is here to show herding: with no
completions, it sends a whole burst to one backend.

nginx_eta() is the score of the nginx least_time balancer: the average is
rounded up to a 20 ms cluster, capped at 5000 ms, and multiplied by 1 + conns.
"""

from fractions import Fraction
from typing import List, Optional, Sequence, Union

Num = Union[int, float, Fraction]


class LeastResponseTime:
    def __init__(self, n: int, alpha: Num = Fraction(1, 20), initial: Optional[Num] = None,
                 weights: Optional[Sequence[int]] = None, mode: str = "product") -> None:
        if not 0 < alpha <= 1:
            raise ValueError("alpha must be in (0, 1]")
        if mode not in ("product", "latency"):
            raise ValueError("mode is product or latency")
        self.alpha = alpha
        self.L: List[Optional[Num]] = [initial] * n
        self.a = [0] * n
        self.w = list(weights) if weights is not None else [1] * n
        self.up = [True] * n
        self.mode = mode

    def score(self, j: int) -> Num:
        lat = self.L[j] if self.L[j] is not None else 0  # no sample yet: probe it first
        return lat * (self.a[j] + 1) if self.mode == "product" else lat

    def pick(self) -> Optional[int]:
        best = None  # @line L1
        for j in range(len(self.a)):  # @line L2
            if not self.up[j] or self.w[j] <= 0:  # @line L3
                continue
            e = self.score(j)  # @line L4
            if best is None or e * self.w[best] < self.score(best) * self.w[j]:  # @line L5
                best = j  # @line L6
        if best is not None:  # @line L7
            self.a[best] += 1
        return best  # @line L8

    def done(self, j: int, x: Num) -> None:
        if self.a[j] <= 0:
            raise ValueError("no request in flight on this backend")
        self.a[j] -= 1  # @line L9
        if self.L[j] is None:  # @line L10
            self.L[j] = x
        else:
            self.L[j] = self.L[j] + self.alpha * (x - self.L[j])  # @line L11


def ewma_closed_form(l0: Num, xs: Sequence[Num], alpha: Num) -> Num:
    """(1 - alpha)^k l0 + sum of alpha (1 - alpha)^(k - i) x_i for i = 1..k."""
    k = len(xs)
    out = (1 - alpha) ** k * l0
    for i, x in enumerate(xs, start=1):
        out += alpha * (1 - alpha) ** (k - i) * x
    return out


def nginx_avg(avg: int, v: int) -> int:
    """nginx ngx_http_upstream_response_time_avg: EWMA with weight 0.05 and rounding, in ms."""
    return int(0.5 + v * 0.05 + avg * 0.95) if avg else v


def nginx_eta(rt: int, conns: int) -> int:
    """The nginx least_time score of a peer with average rt (ms) and conns active connections."""
    if rt > 5000:
        rt = 5000
    else:
        rt += 20 - rt % 20
    return rt * (1 + conns)


def burst(latencies: Sequence[Num], k: int, mode: str = "product",
          weights: Optional[Sequence[int]] = None) -> List[int]:
    """Picks for a burst of k requests that arrive before any response."""
    lb = LeastResponseTime(len(latencies), mode=mode, weights=weights)
    lb.L = list(latencies)
    return [lb.pick() for _ in range(k)]
