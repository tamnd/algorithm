# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lead-lag-compensator/. The authors are listed in prov/8T0JHX.jsonl.

"""Lead and lag compensators, designed on the Bode plot of the loop.

A transfer function is a pair (num, den) of polynomials in s, highest power
first. The loop is the unity negative feedback loop with L = P C.

- lead(alpha, T) is C(s) = (1 + alpha T s) / (1 + T s) with alpha > 1.
- lag(beta, T) is C(s) = (1 + T s) / (1 + beta T s) with beta > 1.

Both have C(0) = 1, so a separate gain k sets the low frequency gain.
Phases are in degrees and frequencies in rad/s.
"""

import bisect
import cmath
import functools
import math

from ctlmat import polyadd, polymul, polyroots, polyval

__all__ = [
    "lead", "lag", "series", "freq", "phase_deg", "max_lead",
    "alpha_for_phase", "place_lead", "design_lag", "margins",
    "design", "closed_loop_poles",
]

W_LO = 1e-4
W_HI = 1e4
PER_DECADE = 200


def lead(alpha, T):
    """Return (num, den) of the lead network (1 + alpha T s) / (1 + T s)."""
    if not alpha > 1 or not T > 0:
        raise ValueError("lead: need alpha > 1 and T > 0")
    return [alpha * T, 1.0], [T, 1.0]


def lag(beta, T):
    """Return (num, den) of the lag network (1 + T s) / (1 + beta T s)."""
    if not beta > 1 or not T > 0:
        raise ValueError("lag: need beta > 1 and T > 0")
    return [T, 1.0], [beta * T, 1.0]


def series(*systems):
    """Return the product of the transfer functions (num, den)."""
    num, den = [1.0], [1.0]
    for n, d in systems:
        num = polymul(num, n)
        den = polymul(den, d)
    return num, den


def freq(num, den, w):
    """Return the complex value G(j w)."""
    s = 1j * w
    return polyval(num, s) / polyval(den, s)


def _trailing(p):
    """Return (number of roots at s = 0, lowest nonzero coefficient)."""
    count = 0
    for c in reversed(p):
        if c != 0:
            return count, c
        count += 1
    raise ValueError("zero polynomial")


def phase_deg(num, den, w):
    """Return the continuous phase of G(j w) in degrees, for W_LO <= w <= W_HI.

    At low frequency G(j w) is close to c (j w)^m, where m is the number of
    zeros at s = 0 minus the number of poles there, so the phase starts at
    90 m degrees (minus 180 if c < 0). From there the phase is unwrapped
    along a logarithmic grid, so it has no jumps of 360 degrees.
    """
    return _cached_phase_fn(tuple(num), tuple(den))(w)


@functools.lru_cache(maxsize=64)
def _cached_phase_fn(num, den):
    return _phase_fn(list(num), list(den))


def _phase_fn(num, den):
    zn, cn = _trailing(num)
    zd, cd = _trailing(den)
    base = 90.0 * (zn - zd) + (0.0 if cn / cd > 0 else -180.0)
    grid = _grid()
    unwrapped = []
    ref = base
    for w in grid:
        raw = math.degrees(cmath.phase(freq(num, den, w)))
        ref = raw + 360.0 * round((ref - raw) / 360.0)
        unwrapped.append(ref)

    def ph(w):
        if not W_LO <= w <= W_HI:
            raise ValueError("phase_deg: w is outside the grid")
        i = min(bisect.bisect_left(grid, w), len(grid) - 1)
        raw = math.degrees(cmath.phase(freq(num, den, w)))
        return raw + 360.0 * round((unwrapped[i] - raw) / 360.0)

    return ph


def max_lead(alpha, T):
    """Return (phi_max in degrees, omega_m, |C(j omega_m)|) of lead(alpha, T)."""
    if not alpha > 1 or not T > 0:
        raise ValueError("max_lead: need alpha > 1 and T > 0")
    phi = math.degrees(math.asin((alpha - 1) / (alpha + 1)))
    return phi, 1.0 / (T * math.sqrt(alpha)), math.sqrt(alpha)


def alpha_for_phase(phi):
    """Return alpha whose lead network has a largest phase of phi degrees."""
    if not 0 < phi < 90:
        raise ValueError("alpha_for_phase: need 0 < phi < 90 degrees")
    s = math.sin(math.radians(phi))
    return (1 + s) / (1 - s)


def _grid():
    n = int(round(math.log10(W_HI / W_LO) * PER_DECADE))
    return [W_LO * (W_HI / W_LO) ** (i / n) for i in range(n + 1)]


def _bisect(f, a, b, iters=100):
    """Root of f between a and b (f(a), f(b) of opposite signs), in log w."""
    fa = f(a)
    la, lb = math.log(a), math.log(b)
    for _ in range(iters):
        lm = 0.5 * (la + lb)
        fm = f(math.exp(lm))
        if (fm > 0) == (fa > 0):
            la, fa = lm, fm
        else:
            lb = lm
    return math.exp(0.5 * (la + lb))


def _crossings(f, grid):
    out = []
    prev_w, prev_f = grid[0], f(grid[0])
    for w in grid[1:]:
        fw = f(w)
        if fw == 0:
            out.append(w)
        elif (fw > 0) != (prev_f > 0) and prev_f != 0:
            out.append(_bisect(f, prev_w, w))
        prev_w, prev_f = w, fw
    return out


def _log_gain(num, den):
    return lambda w: math.log(abs(freq(num, den, w)))


def place_lead(num, den, alpha):
    """Place lead(alpha, T) on the plant (num, den), gain already set.

    The largest lead is put at the new crossover: omega_m is the highest
    frequency where |P(j omega)| = 1/sqrt(alpha), because the lead adds
    sqrt(alpha) of gain there. Return (C_num, C_den, omega_m, T).
    """
    if not alpha > 1:
        raise ValueError("place_lead: need alpha > 1")
    target = -0.5 * math.log(alpha)
    lg = _log_gain(num, den)
    xs = _crossings(lambda w: lg(w) - target, _grid())
    if not xs:
        raise ValueError("place_lead: |P| never equals 1/sqrt(alpha)")
    wm = xs[-1]
    T = 1.0 / (wm * math.sqrt(alpha))
    cn, cd = lead(alpha, T)
    return cn, cd, wm, T


def design_lag(num, den, pm, allowance=5.0, ratio=10.0):
    """Design lag(beta, T) for a phase margin of pm degrees on the plant.

    The new crossover omega_c is the highest frequency where the plant phase
    is -180 + pm + allowance degrees; the allowance pays for the phase lag
    that the lag network keeps at omega_c. Then beta = |P(j omega_c)|, so
    that the lag brings the gain at omega_c down to 1, and the lag zero
    1/T is put a factor ratio below omega_c. Return (C_num, C_den, omega_c,
    beta, T).
    """
    if not 0 < pm < 180 or not ratio > 1:
        raise ValueError("design_lag: need 0 < pm < 180 and ratio > 1")
    target = -180.0 + pm + allowance
    ph = _phase_fn(num, den)
    xs = _crossings(lambda w: ph(w) - target, _grid())
    if not xs:
        raise ValueError("design_lag: the plant phase never reaches the target")
    wc = xs[-1]
    beta = abs(freq(num, den, wc))
    if not beta > 1:
        raise ValueError("design_lag: |P| is not above 1 at the new crossover")
    T = ratio / wc
    cn, cd = lag(beta, T)
    return cn, cd, wc, beta, T


def _golden_max(f, a, b, iters=80):
    g = (math.sqrt(5) - 1) / 2
    la, lb = math.log(a), math.log(b)
    x1 = lb - g * (lb - la)
    x2 = la + g * (lb - la)
    f1, f2 = f(math.exp(x1)), f(math.exp(x2))
    for _ in range(iters):
        if f1 < f2:
            la, x1, f1 = x1, x2, f2
            x2 = la + g * (lb - la)
            f2 = f(math.exp(x2))
        else:
            lb, x2, f2 = x2, x1, f1
            x1 = lb - g * (lb - la)
            f1 = f(math.exp(x1))
    w = math.exp(0.5 * (la + lb))
    return f(w), w


def margins(num, den):
    """Return a dict of the margins of the loop L = num/den.

    Keys: "wgc" (gain crossover frequencies), "pm" (smallest phase margin in
    degrees, None without a gain crossover), "wpc" (phase crossover
    frequencies, where the phase passes -180 + 360 k), "gm" (smallest
    1/|L| over the phase crossovers, math.inf without one), "ms" and "wms"
    (the peak of |S| = 1/|1 + L| and its frequency).
    """
    grid = _grid()
    lg = _log_gain(num, den)
    ph = _phase_fn(num, den)
    wgc = _crossings(lg, grid)
    pms = []
    for w in wgc:
        p = ph(w) + 180.0
        pms.append((p + 180.0) % 360.0 - 180.0)
    hs = [(ph(w) + 180.0) / 360.0 for w in grid]
    wpc = []
    for i in range(1, len(grid)):
        k0, k1 = math.floor(hs[i - 1]), math.floor(hs[i])
        if k0 != k1:
            k = max(k0, k1)
            wpc.append(_bisect(lambda w: ph(w) + 180.0 - 360.0 * k, grid[i - 1], grid[i]))
    gms = [1.0 / abs(freq(num, den, w)) for w in wpc]

    def s_mag(w):
        return 1.0 / abs(1.0 + freq(num, den, w))

    vals = [s_mag(w) for w in grid]
    i = max(range(len(grid)), key=lambda j: vals[j])
    a = grid[max(i - 1, 0)]
    b = grid[min(i + 1, len(grid) - 1)]
    ms, wms = _golden_max(s_mag, a, b)
    if vals[i] > ms:
        ms, wms = vals[i], grid[i]
    return {
        "wgc": wgc,
        "pm": min(pms) if pms else None,
        "wpc": wpc,
        "gm": min(gms) if gms else math.inf,
        "ms": ms,
        "wms": wms,
    }


def design(num, den, pm, kind="lead", extra=None):
    """LEAD-LAG-DESIGN: a lead or lag network for a phase margin of pm degrees.

    The plant (num, den) already holds the gain set by the error constant.
    extra is the phase allowance in degrees (default 10 for lead, 5 for
    lag). Return (C_num, C_den); C = 1 if the plant already has the margin.
    """
    if kind not in ("lead", "lag"):
        raise ValueError("design: kind must be 'lead' or 'lag'")
    if not 0 < pm < 180:
        raise ValueError("design: need 0 < pm < 180")
    if extra is None:
        extra = 10.0 if kind == "lead" else 5.0
    m = margins(num, den)  # @line L1
    pm0 = m["pm"]
    if pm0 is None:
        raise ValueError("design: the plant has no gain crossover")
    if pm0 >= pm:  # @line L2
        return [1.0], [1.0]
    grid = _grid()
    if kind == "lead":  # @line L3
        phi = pm - pm0 + extra  # @line L4
        alpha = alpha_for_phase(phi)  # @line L5
        lg = _log_gain(num, den)
        target = -0.5 * math.log(alpha)
        xs = _crossings(lambda w: lg(w) - target, grid)  # @line L6
        if not xs:
            raise ValueError("design: |P| never equals 1/sqrt(alpha)")
        wm = xs[-1]
        T = 1.0 / (wm * math.sqrt(alpha))  # @line L7
        return lead(alpha, T)  # @line L8
    ph = _phase_fn(num, den)  # @line L9
    xs = _crossings(lambda w: ph(w) - (-180.0 + pm + extra), grid)  # @line L10
    if not xs:
        raise ValueError("design: the plant phase never reaches the target")
    wc = xs[-1]
    beta = abs(freq(num, den, wc))  # @line L11
    if not beta > 1:
        raise ValueError("design: |P| is not above 1 at the new crossover")
    T = 10.0 / wc  # @line L12
    return lag(beta, T)  # @line L13


def closed_loop_poles(num, den):
    """Return the roots of den + num, the poles of L / (1 + L)."""
    return polyroots(polyadd(den, num))
