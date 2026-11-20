# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metadynamics/. The authors are listed in prov/EGQBSZ.jsonl.
"""Metadynamics (Laio and Parrinello 2002) and its well-tempered form
(Barducci, Bussi and Parrinello 2008) on a one-dimensional coordinate s = x.

The walker follows overdamped Langevin dynamics on U + V, stepped by the
Euler-Maruyama method with time step h,

    x <- x - h (U'(x) + V'(x)) + sqrt(2 kT h) xi,   xi ~ N(0, 1).

Every tau steps a Gaussian of width sigma is added to the bias V at the
current s. In standard metadynamics the height is a constant w, and -V
follows F only up to fluctuations of order w that do not die out. In the
well-tempered form the height is w exp(-V(s) / (k dT)), the bias converges,
and F(s) is estimated by -((kT + k dT) / k dT) V(s) up to a constant.

The bias is kept on a grid as values and slopes, and read back by cubic
Hermite interpolation, so the force is the exact derivative of the bias that
is read. One step costs O(1) and one deposit costs O(grid size).
"""

import math
from typing import Callable, Optional


class GridBias:
    """A sum of Gaussians kept on a uniform grid over [lo, hi]."""

    def __init__(self, lo: float, hi: float, n: int):
        self.lo, self.hi, self.n = lo, hi, n
        self.dx = (hi - lo) / (n - 1)
        self.v = [0.0] * n
        self.d = [0.0] * n

    def deposit(self, center: float, height: float, sigma: float) -> None:
        for i in range(self.n):
            s = self.lo + i * self.dx
            g = height * math.exp(-0.5 * ((s - center) / sigma) ** 2)
            self.v[i] += g
            self.d[i] -= g * (s - center) / (sigma * sigma)

    def _cell(self, x: float):
        t = (x - self.lo) / self.dx
        i = min(max(int(t), 0), self.n - 2)
        return i, t - i

    def value(self, x: float) -> float:
        if x < self.lo or x > self.hi:
            return 0.0
        i, t = self._cell(x)
        h00 = (1 + 2 * t) * (1 - t) ** 2
        h10 = t * (1 - t) ** 2
        h01 = t * t * (3 - 2 * t)
        h11 = t * t * (t - 1)
        return (h00 * self.v[i] + h10 * self.dx * self.d[i]
                + h01 * self.v[i + 1] + h11 * self.dx * self.d[i + 1])

    def deriv(self, x: float) -> float:
        if x < self.lo or x > self.hi:
            return 0.0
        i, t = self._cell(x)
        g00 = 6 * t * (t - 1)
        g10 = (1 - t) * (1 - 3 * t)
        g01 = -g00
        g11 = t * (3 * t - 2)
        return (g00 * self.v[i] / self.dx + g10 * self.d[i]
                + g01 * self.v[i + 1] / self.dx + g11 * self.d[i + 1])


def metadynamics(du: Callable[[float], float], x0: float, kT: float, h: float, steps: int,
                 height: float, sigma: float, tau: int, rng,
                 bias_temp: Optional[float] = None,
                 grid: tuple = (-2.5, 2.5, 501)) -> tuple[GridBias, list[float]]:
    """Run metadynamics; bias_temp = k dT gives the well-tempered form, None the standard one.

    Returns the bias and the trajectory of x.
    """
    bias = GridBias(*grid)                                       # @line L1
    noise = math.sqrt(2.0 * kT * h)
    x, xs = x0, []
    for n in range(1, steps + 1):                                # @line L2
        x += -h * (du(x) + bias.deriv(x)) + noise * rng.gauss(0.0, 1.0)  # @line L3
        xs.append(x)
        if n % tau == 0:                                         # @line L4
            w = height
            if bias_temp is not None:
                w = height * math.exp(-bias.value(x) / bias_temp)  # @line L5
            bias.deposit(x, w, sigma)                            # @line L6
    return bias, xs


def free_energy_estimate(bias: GridBias, kT: float, bias_temp: Optional[float] = None) -> list[float]:
    """F on the grid, up to a constant: -V for standard, -((kT + k dT) / k dT) V for well-tempered."""
    factor = 1.0 if bias_temp is None else (kT + bias_temp) / bias_temp  # @line L7
    return [-factor * v for v in bias.v]                         # @line L7


def double_well(height: float):
    """U(x) = height (x^2 - 1)^2 and its derivative."""
    return (lambda x: height * (x * x - 1.0) ** 2,
            lambda x: 4.0 * height * x * (x * x - 1.0))
