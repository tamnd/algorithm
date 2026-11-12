# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ray-marching/. The authors are listed in prov/DR3SGB.jsonl.
"""Fixed-step ray marching.

march_surface finds the first sign change of F(t) = f(o + t d) on a grid of step dt and refines
it by bisection. march_volume integrates a density along the ray with the midpoint rule.
"""

import math


def march_surface(F, t0: float, t1: float, dt: float, refine: int = 30, lipschitz: float | None = None):
    """Return (t, certified) for the first sample interval where F changes from > 0 to <= 0.

    t is the right end of the bracket after `refine` bisection steps, so F(t) <= 0 and a root lies
    in [t - dt / 2**refine, t]. If no sample has F <= 0, t is None. When `lipschitz` is a bound L
    on |F'|, certified tells whether every earlier interval satisfies F(a) + F(b) > L * dt, which
    proves that no root was skipped before the bracket.
    """
    t, k = t0, 0  # @line L1
    ft = F(t)
    certified = True
    if ft <= 0:  # @line L2
        return t, certified
    while t < t1:  # @line L3
        k += 1
        tn = min(t0 + k * dt, t1)  # @line L4
        fn = F(tn)  # @line L5
        if fn <= 0:  # @line L6
            a, b = t, tn  # @line L7
            for _ in range(refine):  # @line L8
                m = 0.5 * (a + b)  # @line L9
                if F(m) > 0:  # @line L10
                    a = m
                else:
                    b = m
            return b, certified  # @line L11
        if lipschitz is not None and ft + fn <= lipschitz * (tn - t):
            certified = False  # a thin feature may hide in [t, tn]
        t, ft = tn, fn  # @line L12
    return None, certified  # @line L13


def march_volume(sigma, t0: float, t1: float, dt: float) -> float:
    """Transmittance exp(-integral of sigma from t0 to t1), with the midpoint rule on steps of dt.

    The midpoint rule is exact when sigma is linear in t on each step.
    """
    n = max(1, math.ceil((t1 - t0) / dt - 1e-12))
    h = (t1 - t0) / n
    tau = 0.0
    for k in range(n):
        tau += sigma(t0 + (k + 0.5) * h) * h
    return math.exp(-tau)
