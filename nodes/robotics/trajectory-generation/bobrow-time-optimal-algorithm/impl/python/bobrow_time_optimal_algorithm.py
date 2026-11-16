# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bobrow-time-optimal-algorithm/. The authors are listed in prov/BWJG6T.jsonl.
"""Time-optimal path parameterization by numerical integration (Bobrow,
Dubowsky and Gibson 1985; Shin and McKay 1985), in the form of Lynch and
Park, Modern Robotics, Section 9.4.

The path parameter s runs over [0, 1]. The code works with x = s'^2
instead of s', so the phase-plane equation s'' = u becomes dx/ds = 2 u.
rows_fn(s) returns the constraint rows (a, b, c, lo, hi) at s, which mean

    lo <= a u + b x + c <= hi.

Torque limits of an arm along a path have this form, with a = M q_s,
b = M q_ss + C(q, q_s) q_s and c = g(q). At each (s, x) the admissible
accelerations form an interval [L(s, x), U(s, x)]; the maximum velocity
curve (MVC) is the largest x where the interval is not empty.

bobrow(rows_fn, h) integrates the U and L curves with RK4 at a fixed step h
in s, finds the switch points (binary search for the L curve that touches
the MVC), and returns the profile as a list of (s, x) points and the switch
points. Cost: O(1 / h) RK4 steps per curve and O(log(1 / tol)) curves per
binary search, so O(k log(1 / tol) / h) evaluations of rows_fn for k
switches. Velocity limits, which make a flat MVC that the profile must
follow, are not handled; see the page.
"""

import math

INF = math.inf
TOL = 1e-12


def accel_bounds(rows, x):
    """Return (L, U), the least and the largest admissible u at the state x.

    Rows with a = 0 do not bound u; they only bound x and are checked by
    mvc. L > U means that x is above the MVC.
    """
    lo_u, hi_u = -INF, INF
    for a, b, c, lo, hi in rows:
        if a == 0.0:
            continue
        r = b * x + c
        b1, b2 = (lo - r) / a, (hi - r) / a
        if a < 0.0:
            b1, b2 = b2, b1
        lo_u, hi_u = max(lo_u, b1), min(hi_u, b2)
    return lo_u, hi_u


def mvc(rows):
    """Largest x >= 0 with L(x) <= U(x) and every a = 0 row met; INF if none.

    For a lower bound (lo - b x - c) / a and an upper bound (hi - b x - c) / a'
    the condition lower <= upper is linear in x, so the MVC is the least of
    finitely many ratios (this is Fourier-Motzkin elimination of u).
    """
    lowers, uppers, best = [], [], INF
    for a, b, c, lo, hi in rows:
        if a == 0.0:
            if b > 0.0 and hi < INF:
                best = min(best, (hi - c) / b)
            if b < 0.0 and lo > -INF:
                best = min(best, (lo - c) / b)
            continue
        # u >= (p - b x) / a style bounds written as (const, slope) / a
        for bound, is_upper in ((lo, False), (hi, True)):
            if abs(bound) == INF:
                continue
            k = ((bound - c) / a, -b / a)  # u bound = k0 + k1 x
            upper = is_upper if a > 0.0 else not is_upper
            (uppers if upper else lowers).append(k)
    for l0, l1 in lowers:
        for u0, u1 in uppers:
            # need l0 + l1 x <= u0 + u1 x, that is (l1 - u1) x <= u0 - l0
            slope, rhs = l1 - u1, u0 - l0
            if slope > 0.0:
                best = min(best, rhs / slope)
            elif rhs < 0.0 and slope == 0.0:
                return 0.0
    return max(best, 0.0)


def _rk4(rows_fn, s, x, h, pick):
    """One RK4 step of dx/ds = 2 u(s, x) with u = pick(L, U), step h (signed)."""

    def f(ss, xx):
        lo, hi = accel_bounds(rows_fn(ss), max(xx, 0.0))
        return 2.0 * (hi if pick == "U" else lo)

    k1 = f(s, x)
    k2 = f(s + h / 2.0, x + h * k1 / 2.0)
    k3 = f(s + h / 2.0, x + h * k2 / 2.0)
    k4 = f(s + h, x + h * k3)
    return x + h * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0


def _above(rows_fn, s, x):
    return x > mvc(rows_fn(s)) * (1.0 + 1e-12) + TOL


def integrate(rows_fn, s0, x0, h, pick, forward, stop=None):
    """Integrate the U or L curve from (s0, x0) on the grid of step h.

    Stop when the curve goes above the MVC ("mvc"), reaches x <= 0 ("zero"),
    leaves [0, 1] ("end"), or when stop(s, x) is true ("stop"). Return
    (points, reason); the points stay below the MVC.
    """
    pts = [(s0, x0)]
    step = h if forward else -h
    n = int(round((1.0 - s0) / h)) if forward else int(round(s0 / h))
    s, x = s0, x0
    for k in range(1, n + 1):
        s_new = s0 + k * step
        x_new = _rk4(rows_fn, s, x, step, pick)
        if _above(rows_fn, s_new, x_new):
            return pts, "mvc"
        if x_new <= 0.0:
            pts.append((s_new, 0.0))
            return pts, "zero"
        pts.append((s_new, x_new))
        if stop is not None and stop(s_new, x_new):
            return pts, "stop"
        s, x = s_new, x_new
    return pts, "end"


def _interp(curve, s):
    """Value at s of a curve given by points with increasing s (linear)."""
    lo, hi = 0, len(curve) - 1
    if s <= curve[0][0]:
        return curve[0][1]
    if s >= curve[-1][0]:
        return curve[-1][1]
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if curve[mid][0] <= s:
            lo = mid
        else:
            hi = mid
    (s1, x1), (s2, x2) = curve[lo], curve[hi]
    return x1 + (x2 - x1) * (s - s1) / (s2 - s1)


def _crossing(p1, p2, curve):
    """Point where the segment p1 p2 meets the curve, by linear interpolation."""
    d1 = p1[1] - _interp(curve, p1[0])
    d2 = p2[1] - _interp(curve, p2[0])
    t = d1 / (d1 - d2) if d1 != d2 else 0.0
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def bobrow(rows_fn, h=1e-3, tol=1e-10, max_switches=50):
    """Return (profile, switches) or None if no admissible profile is found.

    profile: list of (s, x) points with increasing s from (0, 0) to (1, 0).
    switches: list of (s, kind) with kind "UL" (maximum to minimum
    acceleration) or "LU" (minimum to maximum).
    """
    if accel_bounds(rows_fn(0.0), 0.0)[1] <= 0.0:
        return None
    back, _ = integrate(rows_fn, 1.0, 0.0, h, "L", forward=False)  # @line L1
    final = back[::-1]
    s_i, x_i = 0.0, 0.0  # @line L2
    switches, pieces = [], []
    for _ in range(max_switches):  # @line L3
        f_start = final[0][0]

        def meets_final(s, x):
            return s >= f_start and x >= _interp(final, s)

        acc, why = integrate(rows_fn, s_i, x_i, h, "U", True, meets_final)  # @line L4
        if why == "stop":  # @line L5
            cross = _crossing(acc[-2], acc[-1], final)
            switches.append((cross[0], "UL"))
            pieces.append(acc[:-1] + [cross])
            pieces.append([p for p in final if p[0] > cross[0]])
            return [p for piece in pieces for p in piece], switches
        if why != "mvc":
            return None
        s_lim, x_lim = acc[-1]  # @line L6
        low, high = 0.0, x_lim  # @line L7
        best = None
        while high - low > tol * max(1.0, x_lim):
            mid = 0.5 * (low + high)
            test, why = integrate(rows_fn, s_lim, mid, h, "L", True)
            if why == "mvc":
                high = mid
            else:
                low, best = mid, test
        if best is None:
            return None
        s_tan, x_tan = min(best, key=lambda p: mvc(rows_fn(p[0])) - p[1])  # @line L8

        def meets_acc(s, x, acc=acc):
            return s <= acc[-1][0] and x >= _interp(acc, s)

        dec, why = integrate(rows_fn, s_tan, x_tan, h, "L", False, meets_acc)  # @line L9
        if why != "stop":
            return None
        sw = _crossing(dec[-2], dec[-1], acc)
        switches.append((sw[0], "UL"))  # @line L10
        switches.append((s_tan, "LU"))
        pieces.append([p for p in acc if p[0] < sw[0]] + [sw])
        pieces.append([p for p in dec[::-1] if p[0] > sw[0]])
        s_i, x_i = s_tan, x_tan  # @line L11
        pieces[-1] = pieces[-1][:-1]  # the next U curve starts at (s_tan, x_tan)
    return None


def traversal_time(profile):
    """Time of the profile, with x linear between points: sum of 2 ds / (sqrt + sqrt)."""
    t = 0.0
    for (s1, x1), (s2, x2) in zip(profile, profile[1:]):
        den = math.sqrt(max(x1, 0.0)) + math.sqrt(max(x2, 0.0))
        if s2 > s1:
            if den == 0.0:
                return INF
            t += 2.0 * (s2 - s1) / den
    return t


def profile_value(profile, s):
    """x of the profile at s (linear interpolation)."""
    return _interp(profile, s)


# ---------------------------------------------------------------- examples


def single_axis(dist, amax):
    """rows_fn of q(s) = dist * s with |q''| <= amax."""
    return lambda s: [(dist, 0.0, 0.0, -amax, amax)]


def arm2r(q0, q1, tau_max):
    """rows_fn of the planar 2R arm (unit links, unit point masses at the
    link ends, horizontal plane) along q(s) = q0 + s (q1 - q0), torque limits.
    """
    dq = [q1[0] - q0[0], q1[1] - q0[1]]

    def rows_fn(s):
        q2 = q0[1] + s * dq[1]
        c2, s2 = math.cos(q2), math.sin(q2)
        m11, m12 = 3.0 + 2.0 * c2, 1.0 + c2
        a = [m11 * dq[0] + m12 * dq[1], m12 * dq[0] + dq[1]]
        b = [-s2 * (2.0 * dq[0] * dq[1] + dq[1] * dq[1]), s2 * dq[0] * dq[0]]
        return [(a[j], b[j], 0.0, -tau_max[j], tau_max[j]) for j in range(2)]

    return rows_fn
