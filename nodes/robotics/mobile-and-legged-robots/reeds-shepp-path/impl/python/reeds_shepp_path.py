# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reeds-shepp-path/. The authors are listed in prov/FYPPAD.jsonl.

"""Shortest path of a car that drives forward and backward with a minimum turning radius rho.

Reeds and Shepp (1990) proved that a shortest path has at most five segments and
belongs to a family of 48 words (Sussmann and Tang 1991 reduced the sufficient family
to 46). Each segment is a left arc L, a right arc R or a straight segment S, driven
forward (+) or backward (-). The code follows the formulas of Reeds and Shepp, Section 8,
in the form of the OMPL ReedsSheppStateSpace: nine base formulas (8.1, 8.2, 8.3, 8.4,
8.7, 8.8, 8.9, 8.10, 8.11), each applied to the goal and to three transformed goals
(time flip, reflection, and both), and for some families also to the goal seen
backward. A segment length is signed: positive means forward and negative backward.
"""

import math

TWO_PI = 2.0 * math.pi
HALF_PI = 0.5 * math.pi
ZERO = 1e-10

# Segment kinds of the 18 base types, as in the OMPL table.
TYPES = (
    "LRL", "RLR", "LRLR", "RLRL", "LRSL", "RLSR", "LSRL", "RSLR", "LRSR",
    "RLSL", "RSRL", "LSLR", "LSR", "RSL", "LSL", "RSR", "LRSLR", "RLSRL",
)


def wrap(a):
    """Angle in [-pi, pi)."""
    return (a + math.pi) % TWO_PI - math.pi


def polar(x, y):
    return math.hypot(x, y), math.atan2(y, x)


def tau_omega(u, v, xi, eta, phi):
    delta = wrap(u - v)
    a = math.sin(u) - math.sin(delta)
    b = math.cos(u) - math.cos(delta) - 1.0
    t1 = math.atan2(eta * a - xi * b, xi * a + eta * b)
    t2 = 2.0 * (math.cos(delta) - math.cos(v) - math.cos(u)) + 3.0
    tau = wrap(t1 + math.pi) if t2 < 0.0 else wrap(t1)
    omega = wrap(tau - u + v - phi)
    return tau, omega


# Base formulas. Each returns (t, u, v) or None. The goal (x, y, phi) is in the start
# frame and scaled by 1 / rho.

def lp_sp_lp(x, y, phi):  # formula 8.1: L+ S+ L+
    u, t = polar(x - math.sin(phi), y - 1.0 + math.cos(phi))
    if t >= -ZERO:
        v = wrap(phi - t)
        if v >= -ZERO:
            return t, u, v
    return None


def lp_sp_rp(x, y, phi):  # formula 8.2: L+ S+ R+
    u1, t1 = polar(x + math.sin(phi), y - 1.0 - math.cos(phi))
    u1 = u1 * u1
    if u1 >= 4.0:
        u = math.sqrt(u1 - 4.0)
        theta = math.atan2(2.0, u)
        t = wrap(t1 + theta)
        v = wrap(t - phi)
        if t >= -ZERO and v >= -ZERO:
            return t, u, v
    return None


def lp_rm_l(x, y, phi):  # formulas 8.3 and 8.4: L+ R- L
    xi, eta = x - math.sin(phi), y - 1.0 + math.cos(phi)
    u1, theta = polar(xi, eta)
    if u1 <= 4.0:
        u = -2.0 * math.asin(0.25 * u1)
        t = wrap(theta + 0.5 * u + math.pi)
        v = wrap(phi - t + u)
        if t >= -ZERO and u <= ZERO:
            return t, u, v
    return None


def lp_rup_lum_rm(x, y, phi):  # formula 8.7: L+ R+ L- R-
    xi, eta = x + math.sin(phi), y - 1.0 - math.cos(phi)
    rho = 0.25 * (2.0 + math.hypot(xi, eta))
    if rho <= 1.0:
        u = math.acos(rho)
        t, v = tau_omega(u, -u, xi, eta, phi)
        if t >= -ZERO and v <= ZERO:
            return t, u, v
    return None


def lp_rum_lum_rp(x, y, phi):  # formula 8.8: L+ R- L- R+
    xi, eta = x + math.sin(phi), y - 1.0 - math.cos(phi)
    rho = (20.0 - xi * xi - eta * eta) / 16.0
    if 0.0 <= rho <= 1.0:
        u = -math.acos(rho)
        if u >= -HALF_PI:
            t, v = tau_omega(u, u, xi, eta, phi)
            if t >= -ZERO and v >= -ZERO:
                return t, u, v
    return None


def lp_rm_sm_lm(x, y, phi):  # formula 8.9: L+ R-(pi/2) S- L-
    xi, eta = x - math.sin(phi), y - 1.0 + math.cos(phi)
    rho, theta = polar(xi, eta)
    if rho >= 2.0:
        r = math.sqrt(rho * rho - 4.0)
        u = 2.0 - r
        t = wrap(theta + math.atan2(r, -2.0))
        v = wrap(phi - HALF_PI - t)
        if t >= -ZERO and u <= ZERO and v <= ZERO:
            return t, u, v
    return None


def lp_rm_sm_rm(x, y, phi):  # formula 8.10: L+ R-(pi/2) S- R-
    xi, eta = x + math.sin(phi), y - 1.0 - math.cos(phi)
    rho, theta = polar(-eta, xi)
    if rho >= 2.0:
        t = theta
        u = 2.0 - rho
        v = wrap(t + HALF_PI - phi)
        if t >= -ZERO and u <= ZERO and v <= ZERO:
            return t, u, v
    return None


def lp_rm_s_lm_rp(x, y, phi):  # formula 8.11: L+ R-(pi/2) S- L-(pi/2) R+
    xi, eta = x + math.sin(phi), y - 1.0 - math.cos(phi)
    rho, theta = polar(xi, eta)
    if rho >= 2.0:
        u = 4.0 - math.sqrt(rho * rho - 4.0)
        if u <= ZERO:
            t = wrap(math.atan2((4.0 - u) * xi - 2.0 * eta, -2.0 * xi + (u - 4.0) * eta))
            v = wrap(t - phi)
            if t >= -ZERO and v >= -ZERO:
                return t, u, v
    return None


def _four(f, x, y, phi):
    """The base formula on the goal and on its time flip, reflection, and both."""
    return (
        (f(x, y, phi), False, False),
        (f(-x, y, -phi), True, False),
        (f(x, -y, -phi), False, True),
        (f(-x, -y, phi), True, True),
    )


def _word(base, reflect):
    if not reflect:
        return base
    return base.translate(str.maketrans("LR", "RL"))


def candidates_unit(x, y, phi):
    """All candidate paths for radius 1, as (word, signed lengths)."""
    out = []

    def add(base, reflect, flip, lengths):  # @line L5
        s = -1.0 if flip else 1.0  # @line L5
        out.append((_word(base, reflect), tuple(s * a for a in lengths)))  # @line L5

    xb = x * math.cos(phi) + y * math.sin(phi)  # @line L3
    yb = x * math.sin(phi) - y * math.cos(phi)  # @line L3
    # CSC
    for r, flip, refl in _four(lp_sp_lp, x, y, phi):  # @line L4
        if r:
            add("LSL", refl, flip, r)
    for r, flip, refl in _four(lp_sp_rp, x, y, phi):  # @line L4
        if r:
            add("LSR", refl, flip, r)
    # CCC, forward and backward
    for r, flip, refl in _four(lp_rm_l, x, y, phi):  # @line L4
        if r:
            add("LRL", refl, flip, r)
    for r, flip, refl in _four(lp_rm_l, xb, yb, phi):  # @line L4
        if r:
            t, u, v = r
            add("LRL", refl, flip, (v, u, t))
    # CCCC
    for r, flip, refl in _four(lp_rup_lum_rm, x, y, phi):  # @line L4
        if r:
            t, u, v = r
            add("LRLR", refl, flip, (t, u, -u, v))
    for r, flip, refl in _four(lp_rum_lum_rp, x, y, phi):  # @line L4
        if r:
            t, u, v = r
            add("LRLR", refl, flip, (t, u, u, v))
    # CCSC, forward and backward
    for r, flip, refl in _four(lp_rm_sm_lm, x, y, phi):  # @line L4
        if r:
            t, u, v = r
            add("LRSL", refl, flip, (t, -HALF_PI, u, v))
    for r, flip, refl in _four(lp_rm_sm_rm, x, y, phi):  # @line L4
        if r:
            t, u, v = r
            add("LRSR", refl, flip, (t, -HALF_PI, u, v))
    for r, flip, refl in _four(lp_rm_sm_lm, xb, yb, phi):  # @line L4
        if r:
            t, u, v = r
            add("LSRL", refl, flip, (v, u, -HALF_PI, t))
    for r, flip, refl in _four(lp_rm_sm_rm, xb, yb, phi):  # @line L4
        if r:
            t, u, v = r
            add("RSRL", refl, flip, (v, u, -HALF_PI, t))
    # CCSCC
    for r, flip, refl in _four(lp_rm_s_lm_rp, x, y, phi):  # @line L4
        if r:
            t, u, v = r
            add("LRSLR", refl, flip, (t, -HALF_PI, u, -HALF_PI, v))
    return out


def reeds_shepp_candidates(q0, q1, rho):
    """All candidates as (length, word, signed segment lengths in meters)."""
    dx, dy = q1[0] - q0[0], q1[1] - q0[1]  # @line L1
    c, s = math.cos(q0[2]), math.sin(q0[2])  # @line L1
    x, y = (c * dx + s * dy) / rho, (-s * dx + c * dy) / rho  # @line L1
    phi = wrap(q1[2] - q0[2])  # @line L1
    out = []
    for word, lengths in candidates_unit(x, y, phi):  # @line L4
        seg = tuple(rho * a for a in lengths)  # @line L6
        out.append((sum(abs(a) for a in seg), word, seg))  # @line L6
    return out


def reeds_shepp_path(q0, q1, rho):
    """Shortest Reeds-Shepp path: (length, word, signed segment lengths in meters)."""
    best = None  # @line L2
    for cand in reeds_shepp_candidates(q0, q1, rho):
        if best is None or cand[0] < best[0]:  # @line L7
            best = cand  # @line L7
    return best  # @line L8


def step(q, kind, s, rho):
    """Exact pose after a signed arc length s (negative is backward) on one segment."""
    x, y, th = q
    if kind == "S":
        return x + s * math.cos(th), y + s * math.sin(th), th
    if kind == "L":
        nth = th + s / rho
        return x + rho * (math.sin(nth) - math.sin(th)), y - rho * (math.cos(nth) - math.cos(th)), nth
    if kind == "R":
        nth = th - s / rho
        return x - rho * (math.sin(nth) - math.sin(th)), y + rho * (math.cos(nth) - math.cos(th)), nth
    raise ValueError(kind)


def endpoint(q0, word, lengths, rho):
    q = q0
    for kind, s in zip(word, lengths):
        q = step(q, kind, s, rho)
    return q[0], q[1], wrap(q[2])


def gear_changes(lengths):
    """Number of switches between forward and backward along the path."""
    signs = [1 if a > 0 else -1 for a in lengths if abs(a) > 1e-12]
    return sum(1 for a, b in zip(signs, signs[1:]) if a != b)
