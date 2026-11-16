# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dubins-path/. The authors are listed in prov/4DQ75R.jsonl.

"""Shortest path of a forward-only car with a minimum turning radius rho (Dubins 1957).

A pose is (x, y, theta) in meters and radians. The car moves forward, and its curvature
is at most 1 / rho. Dubins proved that a shortest path is one of six words: LSL, RSR,
LSR, RSL, RLR, LRL, where L is a left arc of radius rho, R a right arc of radius rho and
S a straight segment. Some segments can have length zero.

The algorithm puts the start at the origin of a frame whose x axis points to the goal,
scales lengths by 1 / rho, computes the three segment lengths (t, p, q) of each word in
closed form (Shkel and Lumelsky 2001; LaValle 2006, Section 15.3.1), and keeps the
shortest word.
"""

import math

TWO_PI = 2.0 * math.pi
EPS = 1e-10
WORDS = ("LSL", "RSR", "LSR", "RSL", "RLR", "LRL")


def mod2pi(a):
    """Angle in [0, 2 pi). A value within EPS below 2 pi is rounding noise of 0."""
    r = math.fmod(a, TWO_PI)
    if r < 0.0:
        r += TWO_PI
    if r > TWO_PI - EPS:
        r = 0.0
    return r


def wrap(a):
    """Angle in [-pi, pi)."""
    return (a + math.pi) % TWO_PI - math.pi


def word_lengths(word, d, alpha, beta):
    """Normalized segment lengths (t, p, q) of one word, or None if the word does not exist.

    d is the distance between the positions divided by rho. alpha and beta are the start
    and goal headings, measured from the direction of the line from start to goal.
    """
    sa, ca, sb, cb = math.sin(alpha), math.cos(alpha), math.sin(beta), math.cos(beta)
    c_ab = math.cos(alpha - beta)
    if word in ("LSL", "RSR"):
        sign = 1.0 if word == "LSL" else -1.0
        p2 = 2.0 + d * d - 2.0 * c_ab + 2.0 * d * sign * (sa - sb)
        if p2 < -EPS:
            return None
        p = math.sqrt(max(p2, 0.0))
        vx, vy = (d + sa - sb, cb - ca) if word == "LSL" else (d - sa + sb, ca - cb)
        # (vx, vy) joins the two circle centers and has length p. When the two circles are
        # the same, its direction is rounding noise, and the path is a single arc.
        g = math.atan2(vy, vx) if math.hypot(vx, vy) > EPS else alpha
        if word == "LSL":
            return mod2pi(g - alpha), p, mod2pi(beta - g)
        return mod2pi(alpha - g), p, mod2pi(g - beta)
    if word == "LSR":
        p2 = -2.0 + d * d + 2.0 * c_ab + 2.0 * d * (sa + sb)
        if p2 < -EPS:
            return None
        p = math.sqrt(max(p2, 0.0))
        g = math.atan2(-ca - cb, d + sa + sb) - math.atan2(-2.0, p)
        return mod2pi(g - alpha), p, mod2pi(g - beta)
    if word == "RSL":
        p2 = -2.0 + d * d + 2.0 * c_ab - 2.0 * d * (sa + sb)
        if p2 < -EPS:
            return None
        p = math.sqrt(max(p2, 0.0))
        g = math.atan2(ca + cb, d - sa - sb) - math.atan2(2.0, p)
        return mod2pi(alpha - g), p, mod2pi(beta - g)
    if word in ("RLR", "LRL"):
        if word == "RLR":
            c = (6.0 - d * d + 2.0 * c_ab + 2.0 * d * (sa - sb)) / 8.0
        else:
            c = (6.0 - d * d + 2.0 * c_ab + 2.0 * d * (sb - sa)) / 8.0
        if abs(c) > 1.0 + EPS:
            return None
        p = TWO_PI - math.acos(max(-1.0, min(1.0, c)))
        if word == "RLR":
            t = mod2pi(alpha - math.atan2(ca - cb, d - sa + sb) + p / 2.0)
            return t, p, mod2pi(alpha - beta - t + p)
        t = mod2pi(-alpha - math.atan2(ca - cb, d + sa - sb) + p / 2.0)
        return t, p, mod2pi(beta - alpha - t + p)
    raise ValueError(word)


def dubins_candidates(q0, q1, rho):
    """Every word that exists, as (length, word, (l1, l2, l3)) with lengths in meters."""
    dx, dy = q1[0] - q0[0], q1[1] - q0[1]  # @line L1
    d = math.hypot(dx, dy) / rho  # @line L1
    phi = math.atan2(dy, dx) if d > 0.0 else 0.0  # @line L1
    alpha, beta = mod2pi(q0[2] - phi), mod2pi(q1[2] - phi)  # @line L2
    out = []
    for w in WORDS:  # @line L4
        tpq = word_lengths(w, d, alpha, beta)  # @line L5
        if tpq is not None:  # @line L5
            seg = tuple(rho * s for s in tpq)  # @line L5
            out.append((sum(seg), w, seg))  # @line L5
    return out


def dubins_path(q0, q1, rho):
    """Shortest Dubins path: (length, word, (l1, l2, l3)) with segment lengths in meters."""
    best = None  # @line L3
    for cand in dubins_candidates(q0, q1, rho):  # @line L4
        if best is None or cand[0] < best[0]:  # @line L6
            best = cand  # @line L6
    return best  # @line L7


def step(q, kind, s, rho):
    """Exact pose after a signed arc length s on one segment (kind is 'L', 'R' or 'S')."""
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
    """Pose at the end of a path given by its word and segment lengths, heading in [-pi, pi)."""
    q = q0
    for kind, s in zip(word, lengths):
        q = step(q, kind, s, rho)
    return q[0], q[1], wrap(q[2])


def sample(q0, word, lengths, rho, ds):
    """Poses along the path, at most ds apart in arc length, for drawing or collision checks."""
    pts = [q0]
    q = q0
    for kind, s in zip(word, lengths):
        n = max(1, int(math.ceil(abs(s) / ds)))
        for i in range(1, n + 1):
            pts.append(step(q, kind, s * i / n, rho))
        q = pts[-1]
    return pts
