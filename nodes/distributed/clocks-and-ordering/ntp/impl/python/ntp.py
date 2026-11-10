# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ntp/. The authors are listed in prov/PXEY9N.jsonl.

"""The NTP on-wire computation and a small version of its mitigation chain.

The names follow RFC 5905. A client A polls a server B:

  t1  client clock when the request leaves A
  t2  server clock when the request reaches B
  t3  server clock when the reply leaves B
  t4  client clock when the reply reaches A

  offset theta = ((t2 - t1) + (t3 - t4)) / 2       (an estimate of clock B - clock A)
  delay  delta = (t4 - t1) - (t3 - t2)

If the true offset is theta0 and the one-way delays are a (out) and b (back),
then theta = theta0 + (a - b) / 2 and delta = a + b, so |theta - theta0| <= delta / 2.

The chain after that is a reduced form of RFC 5905:
  clock_filter   keep the last 8 samples of a peer and use the one with the least delay (Section 10)
  ntp_select     the intersection steps of Section 11.2.1
  cluster        drop the candidate with the largest selection jitter until NMIN = 3 remain
                 or the largest selection jitter is below the smallest peer jitter (Section 11.2.2)
  combine        average the offsets with weights 1 / root distance (Section 11.2.3)
"""

import math
import random
from dataclasses import dataclass, field
from typing import Optional

NSTAGE = 8
NMIN = 3


def on_wire(t1: float, t2: float, t3: float, t4: float) -> tuple[float, float]:
    """Return (theta, delta) from the four timestamps."""
    theta = ((t2 - t1) + (t3 - t4)) / 2  # @line L1
    delta = (t4 - t1) - (t3 - t2)  # @line L2
    return theta, delta


def exchange(theta0: float, a: float, b: float, t1: float, hold: float) -> tuple[float, float, float, float]:
    """The four timestamps of one exchange, for a server clock that is theta0
    ahead of the client clock, outbound delay a, return delay b, and a server
    hold time `hold` between t2 and t3."""
    t2 = t1 + a + theta0
    t3 = t2 + hold
    t4 = t3 - theta0 + b
    return t1, t2, t3, t4


@dataclass
class Peer:
    """One server as the client sees it: a shift register of (offset, delay) samples."""

    name: str
    disp: float = 0.001  # a fixed dispersion term for the root distance
    samples: list[tuple[float, float]] = field(default_factory=list)

    def add(self, theta: float, delta: float) -> None:
        self.samples.insert(0, (theta, delta))
        del self.samples[NSTAGE:]  # @line L3

    def clock_filter(self) -> tuple[float, float, float]:
        """Return (offset, delay, peer jitter) of the sample with the least delay."""
        best = min(self.samples, key=lambda s: s[1])  # @line L4
        theta, delta = best
        others = [s for s in self.samples if s is not best]
        jit = math.sqrt(sum((s[0] - theta) ** 2 for s in others) / len(others)) if others else 0.0
        return theta, delta, jit

    def root_distance(self) -> float:
        _, delta, _ = self.clock_filter()
        return delta / 2 + self.disp


def ntp_select(cands: list[tuple[float, float]]) -> Optional[tuple[float, float, int]]:
    """RFC 5905, Section 11.2.1, steps 1 to 6, for candidates (theta, lam)."""
    m = len(cands)
    pts = sorted(p for theta, lam in cands for p in ((theta - lam, -1), (theta, 0), (theta + lam, +1)))
    f = 0
    while 2 * f < m:
        d, c, low = 0, 0, math.inf
        for edge, t in pts:
            c += 1 if t == -1 else -1 if t == 1 else 0
            d += t == 0
            if c >= m - f:
                low = edge
                break
        c, high = 0, -math.inf
        for edge, t in reversed(pts):
            c += 1 if t == 1 else -1 if t == -1 else 0
            d += t == 0
            if c >= m - f:
                high = edge
                break
        if d <= f and low < high:  # the text says d = f; Appendix A.5.5.1 accepts d <= f
            return low, high, f
        f += 1
    return None


def mitigate(peers: list[Peer]) -> Optional[dict]:
    """Select, cluster and combine. Returns the system offset and the survivors."""
    stats = {p.name: (*p.clock_filter(), p.root_distance()) for p in peers}  # name -> (theta, delta, jitter, lam)
    sel = ntp_select([(s[0], s[3]) for s in stats.values()])  # @line L5
    if sel is None:
        return None
    low, high, _ = sel
    surv = [name for name, s in stats.items() if low <= s[0] <= high]  # truechimers by midpoint
    while True:  # @line L6
        if len(surv) <= NMIN:
            break
        psi_s = {}
        for a in surv:
            diffs = [(stats[a][0] - stats[b][0]) ** 2 for b in surv if b != a]
            psi_s[a] = math.sqrt(sum(diffs) / len(diffs))
        worst = max(surv, key=lambda a: (psi_s[a], a))
        if psi_s[worst] < min(stats[a][2] for a in surv):
            break
        surv.remove(worst)
    w = {a: 1 / stats[a][3] for a in surv}  # @line L7
    offset = sum(w[a] * stats[a][0] for a in surv) / sum(w.values())
    return {"offset": offset, "survivors": sorted(surv), "interval": (low, high)}


def poll(peer: Peer, theta0: float, rng: random.Random, dmin: float, spread: float, asym: float = 0.0) -> tuple[float, float]:
    """One seeded exchange with a server whose clock is theta0 ahead.
    asym adds that much to the outbound delay only."""
    a = dmin + rng.expovariate(1 / spread) + asym
    b = dmin + rng.expovariate(1 / spread)
    theta, delta = on_wire(*exchange(theta0, a, b, rng.uniform(0, 1e4), rng.uniform(0, 1e-4)))
    peer.add(theta, delta)
    return theta, delta
