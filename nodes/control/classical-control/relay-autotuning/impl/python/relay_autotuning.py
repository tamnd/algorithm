# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relay-autotuning/. The authors are listed in prov/WBZ78H.jsonl.

"""Relay feedback autotuning (Astrom and Hagglund, 1984).

A relay with the output levels +d and -d (and an optional hysteresis eps)
closes the loop around the plant x' = A x + B u(t - delay), y = C x. The loop
settles into a limit cycle. From its period T and its amplitude a, the
describing function of the relay gives the estimate of the ultimate point

    K = 4 d / (pi a),   T_u = T,

where the estimate lies at the phase -180 + asin(eps/a) degrees. A tuning
rule then turns K and T into PID settings.

The plant is simulated with the classical Runge-Kutta method (ctlsim) with
the step dt. The relay acts at every step, and the delay must be a whole
number of steps. Switching times and zero crossings are found by linear
interpolation between steps.

exact_relay_cycle computes the true symmetric limit cycle of a relay with
no hysteresis around a plant with no delay, from the matrix exponential.
"""

import math
from collections import deque

from ctlmat import expm, matvec, solve
from ctlsim import rk4_step, lti

__all__ = [
    "relay_experiment", "analyze_cycle", "relay_estimate", "exact_relay_cycle",
    "ultimate_cycle_rule", "relay_autotune",
]

RULES = {
    "P": (0.5, None, None),
    "PI": (0.45, 1 / 1.2, None),
    "PID": (0.6, 1 / 2, 1 / 8),
}


def relay_experiment(A, B, C, d, t1, dt, eps=0.0, delay=0.0, r=0.0, x0=None):
    """Run the relay loop from x0 (rest by default) until t1.

    The relay output is u = +d when e = r - y > eps, u = -d when e < -eps,
    and keeps its last value in between. It starts at +d. Returns (ts, ys, us).
    """
    if d <= 0 or eps < 0:
        raise ValueError("need d > 0 and eps >= 0")
    n = round(t1 / dt)
    if abs(n * dt - t1) > 1e-9 * t1:
        raise ValueError("t1 is not a multiple of dt")
    m = round(delay / dt)
    if abs(m * dt - delay) > 1e-9 * max(delay, dt):
        raise ValueError("the delay is not a multiple of dt")
    f = lti(A, B)
    x = [0.0] * len(A) if x0 is None else list(x0)
    line = deque([0.0] * m)   # inputs on their way through the delay
    u = d  # @line L1
    ts, ys, us = [0.0], [matvec([C], x)[0]], []
    for k in range(n):
        e = r - ys[-1]  # @line L2
        if e > eps:
            u = d
        elif e < -eps:
            u = -d
        if m:
            line.append(u)
            ua = line.popleft()
        else:
            ua = u
        x = rk4_step(f, k * dt, x, [ua], dt)  # @line L3
        ts.append((k + 1) * dt)
        ys.append(matvec([C], x)[0])
        us.append(u)
    return ts, ys, us


def analyze_cycle(ts, ys, r=0.0, periods=3):
    """Return (T, a, center) of the last `periods` full periods of ys.

    T is the mean time between upward crossings of the level r, found by
    linear interpolation. a is half the peak-to-peak value over the same
    time, and center the mean of the largest and the smallest value.
    """
    up = []
    for k in range(1, len(ys)):  # @line L4
        if ys[k - 1] < r <= ys[k]:
            s = (r - ys[k - 1]) / (ys[k] - ys[k - 1])
            up.append(ts[k - 1] + s * (ts[k] - ts[k - 1]))
    if len(up) < periods + 2:
        raise ValueError("too few periods: run the experiment longer")
    t_a, t_b = up[-1 - periods], up[-1]
    T = (t_b - t_a) / periods  # @line L5
    window = [y for t, y in zip(ts, ys) if t_a <= t <= t_b]
    hi, lo = max(window), min(window)
    return T, (hi - lo) / 2, (hi + lo) / 2  # @line L6


def relay_estimate(d, a, eps=0.0):
    """Return (K, phase): the describing function estimate 4 d/(pi a) of the
    gain that puts the loop at the point found, and its phase in radians."""
    if a <= eps:
        raise ValueError("the amplitude must exceed the hysteresis")
    return 4 * d / (math.pi * a), -math.pi + math.asin(eps / a)  # @line L7


def ultimate_cycle_rule(ku, tu, kind="PID"):
    """The Ziegler-Nichols ultimate cycle rule: (K, Ti or None, Td)."""
    kf, tif, tdf = RULES[kind]
    return kf * ku, None if tif is None else tif * tu, 0 if tdf is None else tdf * tu


def relay_autotune(A, B, C, d, t1, dt, eps=0.0, delay=0.0, kind="PID", periods=3):
    """Run the experiment, analyze the last periods and apply the rule.

    Returns (K, Ti, Td, ku, tu, a)."""
    ts, ys, _ = relay_experiment(A, B, C, d, t1, dt, eps=eps, delay=delay)
    tu, a, _ = analyze_cycle(ts, ys, periods=periods)
    ku, _ = relay_estimate(d, a, eps)
    K, Ti, Td = ultimate_cycle_rule(ku, tu, kind)  # @line L8
    return K, Ti, Td, ku, tu, a


def _flow(A, B, tau):
    """Return (Phi, Gamma) = (e^(A tau), int_0^tau e^(A s) ds B)."""
    n, m = len(A), len(B[0])
    big = [list(A[i]) + list(B[i]) for i in range(n)] + [[0.0] * (n + m) for _ in range(m)]
    E = expm([[tau * v for v in row] for row in big])
    return [row[:n] for row in E[:n]], [row[n:] for row in E[:n]]


def _start_state(A, B, d, tau):
    Phi, Gam = _flow(A, B, tau)
    n = len(A)
    M = [[(1.0 if i == j else 0.0) + Phi[i][j] for j in range(n)] for i in range(n)]
    g = [-d * Gam[i][0] for i in range(n)]
    return solve(M, g)


def exact_relay_cycle(A, B, C, d, tau_max=50.0, grid=5000):
    """Return (T, a, x0) of the symmetric relay cycle, no hysteresis, no delay.

    At t = 0, y crosses 0 going down and the relay switches to +d. Over the
    half period tau, x(tau) = -x(0), so x0 = -(I + Phi)^(-1) Gamma d, and tau
    solves C x0(tau) = 0. The first sign change of C x0 on a grid is refined
    by bisection. a = -min y over the half period, from a fine grid and a
    parabola through the three smallest neighbours.
    """
    def h(tau):
        return matvec([C], _start_state(A, B, d, tau))[0]

    taus = [tau_max * (i + 1) / grid for i in range(grid)]
    prev = h(taus[0])
    lo = hi = None
    for t0, t1 in zip(taus, taus[1:]):
        cur = h(t1)
        if prev != 0 and (prev > 0) != (cur > 0):
            lo, hi = t0, t1
            break
        prev = cur
    if lo is None:
        raise ValueError("no relay cycle found below tau_max")
    s_lo = h(lo) > 0
    for _ in range(100):
        mid = (lo + hi) / 2
        if (h(mid) > 0) == s_lo:
            lo = mid
        else:
            hi = mid
        if hi - lo <= 1e-14 * hi:
            break
    tau = (lo + hi) / 2
    x0 = _start_state(A, B, d, tau)
    k = 2000
    step = tau / k
    Phi, Gam = _flow(A, B, step)
    x = list(x0)
    yv = [matvec([C], x)[0]]
    for _ in range(k):
        x = [sum(p * v for p, v in zip(row, x)) + g[0] * d for row, g in zip(Phi, Gam)]
        yv.append(matvec([C], x)[0])
    j = min(range(1, k), key=lambda i: yv[i])
    y0, y1, y2 = yv[j - 1], yv[j], yv[j + 1]
    den = y0 - 2 * y1 + y2
    ymin = y1 - (y0 - y2) ** 2 / (8 * den) if den > 0 else y1
    return 2 * tau, -ymin, x0


def _self_test():
    A = [[-1.0, 0.0, 0.0], [1.0, -1.0, 0.0], [0.0, 1.0, -1.0]]
    B = [[1.0], [0.0], [0.0]]
    C = [0.0, 0.0, 1.0]
    T, a, _ = exact_relay_cycle(A, B, C, 1.0)
    assert 3.0 < T < 4.0 and 0.1 < a < 0.2
    return True


if __name__ == "__main__":
    _self_test()
