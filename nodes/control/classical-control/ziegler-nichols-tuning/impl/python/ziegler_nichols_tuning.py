# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ziegler-nichols-tuning/. The authors are listed in prov/7QVRVJ.jsonl.

"""Ziegler-Nichols tuning, by the ultimate cycle method and by the step
response method.

The plant is P(s) = num(s)/den(s) e^(-s delay), with polynomials highest
power first. The ultimate point is the smallest omega_u > 0 where the phase
of P(j omega) is -180 degrees; then K_u = 1/|P(j omega_u)| and
T_u = 2 pi/omega_u. The phase is made continuous in omega: it starts at
-90 degrees per net pole at the origin, and the phase of the rational
part is unwrapped along a log grid of frequencies (the grid must be fine
enough that the phase moves less than 180 degrees between neighbours).
The delay adds -omega delay exactly.

The rules return (K, Ti, Td) of the ideal form K (1 + 1/(Ti s) + Td s), with
Ti = None for no integral action and Td = 0 for no derivative action.
They are the rules of Ziegler and Nichols (1942). They are rules of thumb,
not optimal settings.
"""

import cmath
import math

from ctlmat import polyval

__all__ = [
    "phase", "phase_scan", "ultimate_point", "ultimate_cycle_rule", "tangent_fit",
    "step_response_rule",
]

ULTIMATE_RULES = {
    "P": (0.5, None, None),
    "PI": (0.45, 1 / 1.2, None),
    "PID": (0.6, 1 / 2, 1 / 8),
}


def _wrap(x):
    """Return x - 2 pi k in (-pi, pi]."""
    return math.remainder(x, 2 * math.pi)


def _rational_arg(num, den, w):
    return cmath.phase(polyval(num, 1j * w) / polyval(den, 1j * w))


def _low_frequency_phase(num, den):
    """Phase of P(j w) as w -> 0+: -90 degrees per net pole at the origin.

    Raises ValueError for a negative low-frequency gain, where the
    controller needs the reverse action.
    """
    def lowest(p):
        k = 0
        while p[len(p) - 1 - k] == 0:
            k += 1
        return p[len(p) - 1 - k], k

    cn, kn = lowest(num)
    cd, kd = lowest(den)
    # P(j w) is close to (cn/cd) (j w)^(-k), with phase arg(cn/cd) - k pi/2.
    if cn / cd < 0:
        raise ValueError("negative low-frequency gain: use the reverse action")
    return -(kd - kn) * math.pi / 2


def phase_scan(num, den, delay, ws):
    """Continuous phase of P(j w) at the increasing frequencies ws > 0.

    The phase of the rational part is unwrapped from one point to the
    next, which is right when it changes by less than 180 degrees between
    neighbours. The delay adds -w delay exactly.
    """
    ph0 = _low_frequency_phase(num, den)
    prev_arg = None
    total = None
    out = []
    for w in ws:
        a = _rational_arg(num, den, w)
        if total is None:
            total = ph0 + _wrap(a - ph0)
        else:
            total += _wrap(a - prev_arg)
        prev_arg = a
        out.append(total - w * delay)
    return out


def phase(num, den, delay, w, grid=2000):
    """Continuous phase of P(j w) in radians, for w > 0."""
    lo = min(1e-6, w)
    ws = [lo * (w / lo) ** (i / grid) for i in range(grid + 1)]
    return phase_scan(num, den, delay, ws)[-1]


def ultimate_point(num, den, delay=0.0, w_max=1e3, grid=4000):
    """Return (K_u, T_u, w_u) by a scan on a log grid and bisection.

    Raises ValueError if the phase does not reach -180 degrees below w_max.
    Then no finite ultimate gain exists, as for 1/(s + 1)^2.
    """
    lo = 1e-6
    ws = [lo * (w_max / lo) ** (i / grid) for i in range(grid + 1)]
    phs = phase_scan(num, den, delay, ws)  # @line L1
    if phs[0] <= -math.pi:
        raise ValueError("the phase is at or below -180 degrees at low frequency")
    for i in range(1, grid + 1):  # @line L2
        if phs[i] <= -math.pi:
            a, b, base, base_arg = ws[i - 1], ws[i], phs[i - 1] + ws[i - 1] * delay, _rational_arg(num, den, ws[i - 1])
            break
    else:
        raise ValueError("no phase crossover below w_max")

    def g(w):
        return base + _wrap(_rational_arg(num, den, w) - base_arg) - w * delay + math.pi

    for _ in range(200):  # @line L3
        mid = (a + b) / 2
        if g(mid) > 0:
            a = mid
        else:
            b = mid
        if b - a <= 1e-15 * b:
            break
    wu = (a + b) / 2
    ku = abs(polyval(den, 1j * wu) / polyval(num, 1j * wu))  # @line L4
    return ku, 2 * math.pi / wu, wu


def ultimate_cycle_rule(ku, tu, kind="PID"):
    """Ziegler-Nichols ultimate cycle rule: (K, Ti, Td)."""
    kf, tif, tdf = ULTIMATE_RULES[kind]  # @line L5
    return kf * ku, None if tif is None else tif * tu, 0 if tdf is None else tdf * tu


def tangent_fit(ts, ys, du=1.0):
    """Fit the tangent at the steepest point of a step response.

    ts, ys: samples of the response to an input step of size du at t = 0,
    from rest, with a uniform time step. Returns (R, L, a): R the largest
    slope per unit input (central differences), L the time where the
    tangent crosses y = y(0) (the apparent delay), and a = R L.
    """
    n = len(ts)
    if n < 5:
        raise ValueError("too few samples")
    dt = ts[1] - ts[0]
    best = max(range(1, n - 1), key=lambda k: ys[k + 1] - ys[k - 1])  # @line L6
    if best == n - 2:
        raise ValueError("the steepest point is at the end of the record")
    slope = (ys[best + 1] - ys[best - 1]) / (2 * dt)
    if slope <= 0:
        raise ValueError("the response does not rise")
    L = ts[best] - (ys[best] - ys[0]) / slope  # @line L7
    R = slope / du
    return R, L, R * L


def step_response_rule(a, L, kind="PID"):
    """Ziegler-Nichols step response rule (1942) from a = R L and L.

    P: K = 1/a. PI: K = 0.9/a, Ti = L/0.3. PID: K = 1.2/a, Ti = 2 L,
    Td = L/2. Many books round the PI integral time to 3 L.
    """
    if kind == "P":  # @line L8
        return 1 / a, None, 0
    if kind == "PI":
        return 0.9 / a, L / 0.3, 0
    if kind == "PID":
        return 1.2 / a, 2 * L, L / 2
    raise ValueError("kind must be P, PI or PID")


def _self_test():
    ku, tu, wu = ultimate_point([1.0], [1.0, 3.0, 3.0, 1.0])
    assert abs(ku - 8) < 1e-9 and abs(wu - math.sqrt(3)) < 1e-9
    return True


if __name__ == "__main__":
    _self_test()
