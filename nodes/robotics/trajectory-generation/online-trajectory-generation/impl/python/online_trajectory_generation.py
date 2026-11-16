# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-trajectory-generation/. The authors are listed in prov/T2ZEJ5.jsonl.
"""Online trajectory generation for one axis, with velocity and acceleration bounds.

This is the second-order case (Type II in the classification of Kroger and
Wahl): the state is (position, velocity), |v| <= V and |a| <= A. In each
control cycle, min_time_profile() computes the time-optimal motion from the
current state to the target state, and otg_step() moves the state along it
by one cycle time dt. The target may change between two cycles.

A profile is a list of (duration, acceleration) pieces with at most three
pieces: a ramp, a cruise at |v| = V (possibly of zero length), and a ramp.
"""

import math


def _candidates(p0, v0, pT, vT, V, A):
    """All bang-cruise-bang profiles that reach the target; each is (time, pieces)."""
    D = pT - p0
    out = []
    for sigma in (1, -1):  # @line L2
        r = sigma * A * D + (v0 * v0 + vT * vT) / 2  # @line L3
        if r < 0:
            continue
        for vp in (math.sqrt(r), -math.sqrt(r)):  # @line L4
            if sigma * (vp - v0) < -1e-12 or sigma * (vp - vT) < -1e-12:  # @line L5
                continue
            if abs(vp) <= V:  # @line L6
                t1 = max(0.0, sigma * (vp - v0) / A)
                t3 = max(0.0, sigma * (vp - vT) / A)
                pieces = [(t1, sigma * A), (0.0, 0.0), (t3, -sigma * A)]
            else:  # @line L7
                vc = sigma * V
                t1 = sigma * (vc - v0) / A
                t3 = sigma * (vc - vT) / A
                d_ramps = (2 * vc * vc - v0 * v0 - vT * vT) / (2 * sigma * A)
                t2 = (D - d_ramps) / vc
                pieces = [(t1, sigma * A), (t2, 0.0), (t3, -sigma * A)]
            out.append((sum(d for d, _ in pieces), pieces))  # @line L8
    return out


def min_time_profile(p0, v0, pT, vT, V, A):
    """Time-optimal profile from (p0, v0) to (pT, vT); returns (time, pieces)."""
    if V <= 0 or A <= 0:
        raise ValueError("V and A must be positive")
    if abs(v0) > V + 1e-12 or abs(vT) > V + 1e-12:
        raise ValueError("start and target velocities must satisfy |v| <= V")
    cands = _candidates(p0, v0, pT, vT, V, A)  # @line L1
    return min(cands, key=lambda c: c[0])  # @line L9


def evaluate(p0, v0, pieces, t):
    """State (p, v, a) at time t along the pieces (t beyond the end holds the final state)."""
    p, v = p0, v0
    for dur, a in pieces:
        h = min(dur, t)
        if h > 0:
            p += v * h + a * h * h / 2
            v += a * h
        t -= dur
        if t <= 0:
            return p, v, a
    return p, v, 0.0


def otg_step(p, v, pT, vT, V, A, dt):
    """One control cycle: plan from the current state, then move by dt along the plan."""
    T, pieces = min_time_profile(p, v, pT, vT, V, A)  # @line L10
    if T <= dt:
        return pT, vT, T  # @line L11
    p1, v1, _ = evaluate(p, v, pieces, dt)  # @line L12
    return p1, max(-V, min(V, v1)), T


def envelope_reachable(p0, v0, pT, vT, V, A, T, steps=2000):
    """Brute-force test: can (pT, vT) be reached at exactly time T?

    Every admissible velocity lies between l(t) = max(v0 - A t, -V, vT - A (T - t))
    and u(t) = min(v0 + A t, V, vT + A (T - t)). Both bounds are admissible
    when |v0 - vT| <= A T, and so is every convex combination. So the target is
    reachable at T exactly when p0 + integral(l) <= pT <= p0 + integral(u).
    """
    if abs(v0 - vT) > A * T + 1e-12:
        return False
    h = T / steps
    lo = hi = 0.0
    for k in range(steps):
        t = (k + 0.5) * h
        hi += min(v0 + A * t, V, vT + A * (T - t)) * h
        lo += max(v0 - A * t, -V, vT - A * (T - t)) * h
    return p0 + lo - 1e-9 <= pT <= p0 + hi + 1e-9
