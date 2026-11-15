# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/process-reaction-curve/. The authors are listed in prov/QACT9Z.jsonl.

"""Fit a first order plus dead time (FOPDT) model to a recorded step response.

The model is G(s) = K e^(-L s) / (T s + 1). Its unit step response is 0
for t < L and K (1 - e^(-(t - L) / T)) for t >= L.

Input: sample times t[0] < t[1] < ... (the step of size du is applied at
t[0]) and the output samples y[i], from rest at y[0] until the response has
settled at y[-1]. The normalized response is z = (y - y[0]) / (y[-1] - y[0]).

Two methods:
- "tangent": the line of largest slope through the curve (the tangent at the
  inflection point). It meets z = 0 at t = L and z = 1 at t = L + T. The
  slope is taken from the chords of the samples, so the result is exact for
  a sampled FOPDT response whose dead time is a sample time, and close to
  the tangent of a smooth curve when the sampling is fine.
- "two-point": the times t28 and t63 where z reaches 1 - e^(-1/3) (about
  28.3 percent) and 1 - e^(-1) (about 63.2 percent), by linear
  interpolation. Then T = 1.5 (t63 - t28) and L = t63 - T. These are the
  exact values for a FOPDT response.

Precondition: at least 3 samples, strictly increasing times, du != 0, and
y[-1] != y[0]. z should rise monotonically; with noise the result is
sensitive, see the page.

Cost: O(n) for n samples, in the real RAM.
"""

import math
from typing import Sequence, Tuple

P28 = 1.0 - math.exp(-1.0 / 3.0)
P63 = 1.0 - math.exp(-1.0)


def _crossing(t: Sequence, z: Sequence, level: float) -> float:
    """First time where z reaches level, by linear interpolation."""
    for i in range(1, len(z)):
        if z[i] >= level:
            if z[i] == z[i - 1]:
                return t[i]
            return t[i - 1] + (level - z[i - 1]) * (t[i] - t[i - 1]) / (z[i] - z[i - 1])
    raise ValueError("the response never reaches the level")


def fit_fopdt(t: Sequence, y: Sequence, du: float,
              method: str = "two-point") -> Tuple[float, float, float]:
    """Return (K, L, T) of the FOPDT model fitted to the step response."""
    if len(t) != len(y) or len(t) < 3:
        raise ValueError("need at least 3 samples of t and y")
    if any(t[i] >= t[i + 1] for i in range(len(t) - 1)):
        raise ValueError("times must be strictly increasing")
    if du == 0 or y[-1] == y[0]:
        raise ValueError("need a nonzero step and a nonzero change of the output")
    k = (y[-1] - y[0]) / du  # @line L1
    z = [(v - y[0]) / (y[-1] - y[0]) for v in y]  # @line L2
    if method == "two-point":  # @line L3
        t28 = _crossing(t, z, P28) - t[0]  # @line L4
        t63 = _crossing(t, z, P63) - t[0]
        tau = 1.5 * (t63 - t28)  # @line L5
        dead = t63 - tau  # @line L6
    elif method == "tangent":
        best = None
        for i in range(len(z) - 1):  # @line L7
            s = (z[i + 1] - z[i]) / (t[i + 1] - t[i])
            if best is None or s > best[0]:
                best = (s, 0.5 * (t[i] + t[i + 1]) - t[0], 0.5 * (z[i] + z[i + 1]))
        s, tm, zm = best
        if s <= 0:
            raise ValueError("the normalized response does not rise")
        dead = tm - zm / s  # @line L8
        tau = 1.0 / s  # @line L9
    else:
        raise ValueError("method must be 'two-point' or 'tangent'")
    return k, dead, tau  # @line L10


def fopdt_step(k: float, dead: float, tau: float, t: float) -> float:
    """Unit step response of K e^(-L s) / (T s + 1) at time t."""
    if t < dead:
        return 0.0
    return k * (1.0 - math.exp(-(t - dead) / tau))
