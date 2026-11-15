# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-mode-observer/. The authors are listed in prov/V32494.jsonl.

"""A sliding mode observer with super-twisting injection for systems

    x1' = x2,
    x2' = f0(x1, u) + F(t, x1, x2),   y = x1,

where f0 is known, F is unknown and |F| <= L along the motion. The observer is

    xh1' = xh2 + lam |e|^(1/2) sgn(e),
    xh2' = f0(y, u) + alpha sgn(e),      e = y - xh1,

and is run in sampled form with explicit Euler steps of length h. The
errors e1 = x1 - xh1 and e2 = x2 - xh2 obey the super-twisting equations

    e1' = e2 - lam |e1|^(1/2) sgn(e1),   e2' = F - alpha sgn(e1),

so e1 and e2 reach zero in finite time when alpha > L + 2 L^2 / lam^2, and
then the average of alpha sgn(e) equals F (the equivalent output injection).
"""

import math

__all__ = ["sgn", "SlidingModeObserver"]


def sgn(s):
    """Return -1, 0 or 1."""
    return (s > 0) - (s < 0)


class SlidingModeObserver:
    """Sampled super-twisting observer for a second order mechanical system.

    f0(y, u): the known part of x2'. lam, alpha: the injection gains.
    h: the sampling period. xh0: the initial estimate (xh1, xh2).
    """

    def __init__(self, f0, lam, alpha, h, xh0=(0.0, 0.0)):
        if lam <= 0 or alpha <= 0:
            raise ValueError("lam and alpha must be positive")
        if h <= 0:
            raise ValueError("h must be positive")
        self.f0 = f0
        self.lam = lam
        self.alpha = alpha
        self.h = h
        self.xh = list(xh0)
        self.injection = 0.0

    def step(self, y, u=None):
        """Use the sample y at the current instant; return the next estimate."""
        x1, x2 = self.xh
        e = y - x1  # @line L1
        v1 = self.lam * math.sqrt(abs(e)) * sgn(e)  # @line L2
        v2 = self.alpha * sgn(e)  # @line L2
        n1 = x1 + self.h * (x2 + v1)  # @line L3
        n2 = x2 + self.h * (self.f0(y, u) + v2)  # @line L4
        self.xh = [n1, n2]
        self.injection = v2
        return list(self.xh)  # @line L5
