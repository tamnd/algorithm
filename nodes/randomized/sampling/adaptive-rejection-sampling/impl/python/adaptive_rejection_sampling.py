# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-rejection-sampling/. The authors are listed in prov/7A5KY6.jsonl.

"""Adaptive rejection sampling (Gilks and Wild, 1992), tangent form.

For a log-concave density f = exp(h) / Z, the tangents of h at the points
of T form an upper hull u_T >= h, and the chords between neighbouring points
form a lower hull l_T <= h. Sample X from s_T ~ exp(u_T), a piecewise
exponential density; accept if W <= exp(l_T(X) - u_T(X)) (the squeeze, no
evaluation of h), else evaluate h(X), accept if W <= exp(h(X) - u_T(X)), and
add X to T. Each accepted X has density f whatever T is, so the outputs are
independent. Exact for exact arithmetic.
"""

import bisect
import math
import random
from typing import Callable, List, Sequence

INF = float("inf")


class ARS:
    def __init__(
        self,
        h: Callable[[float], float],
        dh: Callable[[float], float],
        xs: Sequence[float],
        lo: float = -INF,
        hi: float = INF,
    ) -> None:
        self.h, self.dh, self.lo, self.hi = h, dh, lo, hi
        self.x: List[float] = []
        self.hx: List[float] = []
        self.dx: List[float] = []
        self.evals = 0
        for t in sorted(xs):
            self._add(t)
        if lo == -INF and not self.dx[0] > 0:
            raise ValueError("the leftmost point needs h' > 0 on an unbounded domain")
        if hi == INF and not self.dx[-1] < 0:
            raise ValueError("the rightmost point needs h' < 0 on an unbounded domain")
        self._build()

    def _add(self, t: float, ht=None) -> None:
        i = bisect.bisect_left(self.x, t)
        if i < len(self.x) and self.x[i] == t:
            return
        self.evals += 1
        self.x.insert(i, t)
        self.hx.insert(i, self.h(t) if ht is None else ht)
        self.dx.insert(i, self.dh(t))

    def _build(self) -> None:
        x, hx, dx = self.x, self.hx, self.dx
        k = len(x)
        z = [self.lo]
        for j in range(k - 1):
            if dx[j] == dx[j + 1]:
                z.append(0.5 * (x[j] + x[j + 1]))
            else:
                z.append((hx[j + 1] - hx[j] - x[j + 1] * dx[j + 1] + x[j] * dx[j]) / (dx[j] - dx[j + 1]))
        z.append(self.hi)
        self.z = z
        # The mass of exp(u) on segment j, scaled by exp(-hmax) to avoid overflow.
        self.hmax = max(hx)
        mass = []
        for j in range(k):
            mass.append(self._seg_mass(j))
        self.cum = []
        s = 0.0
        for m in mass:
            s += m
            self.cum.append(s)

    def _seg_mass(self, j: int) -> float:
        a, b = self.hx[j] - self.hmax, self.dx[j]
        lo, hi = self.z[j] - self.x[j], self.z[j + 1] - self.x[j]
        if b == 0.0:
            return math.exp(a) * (hi - lo)
        return math.exp(a) * (math.exp(b * hi) - math.exp(b * lo)) / b

    def upper(self, t: float) -> float:
        j = bisect.bisect_left(self.z, t, 1, len(self.z) - 1) - 1
        return self.hx[j] + (t - self.x[j]) * self.dx[j]

    def lower(self, t: float) -> float:
        x = self.x
        if t < x[0] or t > x[-1]:
            return -INF
        j = max(0, bisect.bisect_right(x, t) - 1)
        if j == len(x) - 1:
            return self.hx[j]
        return ((x[j + 1] - t) * self.hx[j] + (t - x[j]) * self.hx[j + 1]) / (x[j + 1] - x[j])

    def _sample_hull(self, rng: random.Random) -> float:
        r = rng.random() * self.cum[-1]
        j = min(bisect.bisect_right(self.cum, r), len(self.cum) - 1)
        v = rng.random()
        b = self.dx[j]
        lo, hi = self.z[j] - self.x[j], self.z[j + 1] - self.x[j]
        if b == 0.0:
            return self.x[j] + lo + v * (hi - lo)
        elo, ehi = math.exp(b * lo), math.exp(b * hi)
        return self.x[j] + math.log(elo + v * (ehi - elo)) / b

    def sample(self, n: int, rng: random.Random) -> List[float]:
        out: List[float] = []  # @line L1
        while len(out) < n:  # @line L2
            t = self._sample_hull(rng)  # @line L3
            w = rng.random()  # @line L4
            ut = self.upper(t)
            if w <= math.exp(self.lower(t) - ut):  # @line L5
                out.append(t)  # @line L5
                continue
            ht = self.h(t)  # @line L6
            if w <= math.exp(ht - ut):  # @line L7
                out.append(t)  # @line L7
            self._add(t, ht)  # @line L8
            self._build()  # @line L8
        return out  # @line L9
