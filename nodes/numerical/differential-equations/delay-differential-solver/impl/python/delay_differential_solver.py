# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delay-differential-solver/. The authors are listed in prov/J3P31B.jsonl.

"""Classical Runge-Kutta 4 for delay differential equations with constant delays.

Solves y'(t) = f(t, y(t), [y(t - tau_1), ..., y(t - tau_m)]) on [t0, T] with
y = phi on [t0 - max tau, t0]. Delayed values come from phi or from the cubic
Hermite interpolant of the computed steps (dense output). The grid contains all
breakpoints t0 + n_1 tau_1 + ... + n_m tau_m with 1 <= n_1 + ... + n_m <= 4, and
no step is longer than the smallest delay, so every delayed value lies in the
already computed past and the method stays explicit.
"""

import bisect
import math
from dataclasses import dataclass, field
from itertools import product
from typing import Any, Callable, List, Sequence

# A step count within this relative amount of an integer is rounded to it.
GRID_SLACK = 1e-9
# Order of the method; breakpoints reached by at most ORDER delays are tracked.
ORDER = 4


def _axpy(a, x, y):
    """y + a x for lists."""
    return [yi + a * xi for xi, yi in zip(x, y)]


def hermite(ta, ya, fa, tb, yb, fb, s):
    """Cubic Hermite interpolant on [ta, tb] with values ya, yb and slopes fa, fb, at s."""
    k = tb - ta
    th = (s - ta) / k
    h00 = (2 * th - 3) * th * th + 1
    h10 = ((th - 2) * th + 1) * th
    h01 = (3 - 2 * th) * th * th
    h11 = (th - 1) * th * th
    return [h00 * a + h10 * k * p + h01 * b + h11 * k * q
            for a, p, b, q in zip(ya, fa, yb, fb)]


def breakpoints(t0, T, taus: Sequence, order: int = ORDER) -> List:
    """Sorted points t0 < b_1 < ... < b_K = T: sums of at most `order` delays, then T."""
    span = T - t0
    pts = set()
    for ns in product(range(order + 1), repeat=len(taus)):
        if 1 <= sum(ns) <= order:
            b = t0 + sum(n * tau for n, tau in zip(ns, taus))
            if b < T:
                pts.add(b)
    out = [t0]
    for b in sorted(pts):
        if b - out[-1] > GRID_SLACK * span:     # merge points closer than rounding
            out.append(b)
    if T - out[-1] <= GRID_SLACK * span and len(out) > 1:
        out.pop()
    out.append(T)
    return out


class History:
    """The computed solution: phi before t0, cubic Hermite pieces after."""

    def __init__(self, t0, phi, scalar):
        self.t0, self.phi, self.scalar = t0, phi, scalar
        self.ts: List[Any] = []
        self.ys: List[List[Any]] = []
        self.fs: List[List[Any]] = []
        self.lookups = 0

    def _phi(self, s):
        v = self.phi(s)
        return [v] if self.scalar else list(v)

    def push(self, t, y, fval):
        self.ts.append(t)
        self.ys.append(y)
        self.fs.append(fval)

    def value(self, s):                          # @line L11
        """y(s) as a list: phi(s) for s <= t0, else the Hermite piece containing s."""
        self.lookups += 1
        if s <= self.t0:
            return self._phi(s)
        if s > self.ts[-1]:
            raise ValueError("delayed time %r lies beyond the computed solution" % (s,))
        i = bisect.bisect_left(self.ts, s)       # ts[i-1] < s <= ts[i]
        if self.ts[i] == s:
            return list(self.ys[i])
        return hermite(self.ts[i - 1], self.ys[i - 1], self.fs[i - 1],
                       self.ts[i], self.ys[i], self.fs[i], s)

    def __call__(self, s):
        v = self.value(s)
        return v[0] if self.scalar else v


@dataclass
class DDEResult:
    """Final time and value, steps, evaluations of f, history lookups, breakpoints, dense solution."""

    t: Any
    y: Any
    steps: int
    f_evals: int
    lookups: int
    grid_breakpoints: List[Any] = field(default_factory=list)
    solution: Any = None


def dde_rk4(f: Callable, phi: Callable, taus: Sequence, t0, T, h,
            track_breakpoints: bool = True) -> DDEResult:
    """Solve y'(t) = f(t, y, [y(t - tau_j)]_j), y = phi on [t0 - max tau, t0], up to T.

    y may be a scalar or a list. The step size is at most min(h, min tau); with
    track_breakpoints=False the grid ignores the breakpoints (to show the order loss).
    """
    taus = list(taus)
    if not taus or any(tau <= 0 for tau in taus):
        raise ValueError("delays must be positive")
    if h <= 0:
        raise ValueError("step size must be positive")
    if T < t0:
        raise ValueError("T must not precede t0")
    v0 = phi(t0)
    scalar = not isinstance(v0, (list, tuple))
    hist = History(t0, phi, scalar)
    y = [v0] if scalar else list(v0)

    def F(t, yv, zs):
        if scalar:
            return [f(t, yv[0], [z[0] for z in zs])]
        return list(f(t, yv, zs))

    def lags(s):
        return [hist.value(s - tau) for tau in taus]

    def out(v):
        return v[0] if scalar else v

    if T == t0:
        return DDEResult(t0, out(y), 0, 0, 0, [t0], hist)

    H = min(h, min(taus))                                            # @line L2
    if track_breakpoints:
        B = breakpoints(t0, T, taus)                                 # @line L1
    else:
        B = [t0, T]
    evals = 1
    fy = F(t0, y, lags(t0))                                          # @line L3
    hist.push(t0, y, fy)
    steps = 0
    t = t0
    for i in range(1, len(B)):                                       # @line L4
        a, b = B[i - 1], B[i]
        n = max(1, math.ceil((b - a) / H - GRID_SLACK))              # @line L5
        k = (b - a) / n
        for r in range(1, n + 1):                                    # @line L6
            t = a + (r - 1) * k
            half = t + k / 2
            zh = lags(half)                                          # @line L7
            k1 = fy
            k2 = F(half, _axpy(k / 2, k1, y), zh)
            k3 = F(half, _axpy(k / 2, k2, y), zh)
            tn = b if r == n else a + r * k
            zn = lags(tn)
            k4 = F(tn, _axpy(k, k3, y), zn)                          # @line L8
            y = [yi + k / 6 * (p + 2 * q + 2 * u + w)
                 for yi, p, q, u, w in zip(y, k1, k2, k3, k4)]       # @line L9
            fy = F(tn, y, zn)                                        # @line L10
            hist.push(tn, y, fy)
            evals += 4
            steps += 1
            t = tn
    return DDEResult(t, out(y), steps, evals, hist.lookups, B, hist)  # @line L12


def exact_unit_delay(t, c=1):
    """Exact solution of y'(t) = -c y(t - 1), y = 1 on [-1, 0], by the method of steps.

    On [n - 1, n], y(t) = sum_(k=0)^n (-c)^k (t - k + 1)^k / k!.
    """
    if t <= 0:
        return 1
    n = math.ceil(t)
    total = 0
    fact = 1
    for k in range(n + 1):
        if k > 0:
            fact *= k
        total += (-c) ** k * (t - k + 1) ** k / fact
    return total
