# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vector-loop-closure/. The authors are listed in prov/V3P14V.jsonl.

"""Vector loop closure for the planar four-bar and the offset slider-crank.

Four-bar notation (Norton): ground d from O2 = (0, 0) to O4 = (d, 0), input
(crank) a from O2 to the crank pin A, coupler b from A to B, output c from O4
to B. All angles are measured counterclockwise from the +x axis, which is the
ground line. The loop equation is

    a e^(i theta2) + b e^(i theta3) - c e^(i theta4) - d = 0.

For a given theta2 the half-angle substitution t = tan(theta4 / 2) turns the
loop into A t^2 + B t + C = 0. Its two roots are the two assemblies. The
branch of an assembly is +1 when B lies to the left of the directed line from
A to O4 and -1 when it lies to the right. With the ground on the +x axis and
the crank above it, branch +1 is the open assembly and -1 the crossed one.

Slider-crank: crank a from O2 = (0, 0) to A, connecting rod b from A to the
slider pin B = (x, e), and the slider moves on the line y = e (offset e). The
loop is a e^(i theta2) + b e^(i theta3) - x - i e = 0. Branch +1 has the
slider pin to the right of A (x > a cos theta2), branch -1 to the left.

Floats are used for the angles. The Grashof tests use the link lengths as
given, so they are exact for int or Fraction lengths.
"""

import math

TOL = 1e-12


def freudenstein_k(a, b, c, d):
    """The constants K1, K2, K3 of the four-bar."""
    return d / a, d / c, (a * a - b * b + c * c + d * d) / (2 * a * c)


def _branch(a, c, d, theta2, theta4):
    """+1 if B is left of the directed line A -> O4, -1 if right, 0 if on it."""
    ax, ay = a * math.cos(theta2), a * math.sin(theta2)
    bx, by = d + c * math.cos(theta4), c * math.sin(theta4)
    cross = (d - ax) * (by - ay) - (0.0 - ay) * (bx - ax)
    scale = (abs(a) + abs(c) + abs(d)) ** 2
    if abs(cross) <= 1e-12 * scale:
        return 0
    return 1 if cross > 0 else -1


def fourbar_positions(a, b, c, d, theta2):
    """The assemblies of the four-bar at the input angle theta2.

    Returns a list of (theta3, theta4, branch), with the open assembly
    (branch +1) first. The list is empty when the loop cannot close, and it
    holds one entry when the two assemblies coincide (a toggle position).
    """
    k1, k2, k3 = freudenstein_k(a, b, c, d)  # @line L1
    c2, s2 = math.cos(theta2), math.sin(theta2)
    qa = c2 - k1 - k2 * c2 + k3  # @line L2
    qb = -2.0 * s2
    qc = k1 - (k2 + 1.0) * c2 + k3
    disc = qb * qb - 4.0 * qa * qc  # @line L3
    scale = (abs(qa) + abs(qb) + abs(qc)) ** 2 + 1.0
    if disc < -TOL * scale:  # @line L4
        return []
    # stable roots of qa t^2 + qb t + qc = 0, kept as angles so that t = inf
    # (theta4 = pi, when qa = 0) needs no special case
    if disc <= TOL * scale:
        halves = [math.atan2(-qb, 2.0 * qa)]  # a double root: a toggle position
    else:
        r = math.sqrt(disc)
        q = -0.5 * (qb + (r if qb >= 0 else -r))
        halves = [math.atan2(q, qa), math.atan2(qc, q)]  # @line L5
    out = []
    for h in halves:
        t4 = 2.0 * h
        t3 = math.atan2(c * math.sin(t4) - a * s2, d + c * math.cos(t4) - a * c2)  # @line L6
        out.append((t3, t4, _branch(a, c, d, theta2, t4)))  # @line L7
    if len(out) == 2 and abs(math.remainder(out[0][1] - out[1][1], 2 * math.pi)) <= 1e-9:
        out = [out[0]]
    out.sort(key=lambda p: -p[2])
    return out  # @line L8


def fourbar_velocities(a, b, c, theta2, theta3, theta4, omega2):
    """omega3 and omega4 from the derivative of the loop equation.

    Raises ZeroDivisionError at a toggle position, where theta3 = theta4 mod pi.
    """
    # [-b sin t3,  c sin t4] [w3]   [ a w2 sin t2]
    # [ b cos t3, -c cos t4] [w4] = [-a w2 cos t2]
    m11, m12 = -b * math.sin(theta3), c * math.sin(theta4)  # @line L9
    m21, m22 = b * math.cos(theta3), -c * math.cos(theta4)
    r1, r2 = a * omega2 * math.sin(theta2), -a * omega2 * math.cos(theta2)
    det = m11 * m22 - m12 * m21
    if abs(det) <= 1e-14 * (abs(b) * abs(c) + 1.0):
        raise ZeroDivisionError("toggle position: the velocity is not determined")
    return (r1 * m22 - m12 * r2) / det, (m11 * r2 - r1 * m21) / det


def fourbar_residual(a, b, c, d, theta2, theta3, theta4):
    """|a e^(i t2) + b e^(i t3) - c e^(i t4) - d|."""
    z = a * complex(math.cos(theta2), math.sin(theta2)) + b * complex(math.cos(theta3), math.sin(theta3))
    z -= c * complex(math.cos(theta4), math.sin(theta4)) + d
    return abs(z)


def slider_crank_positions(a, b, e, theta2):
    """The assemblies of the offset slider-crank: a list of (x, theta3, branch)."""
    ax, ay = a * math.cos(theta2), a * math.sin(theta2)
    h = e - ay
    disc = b * b - h * h
    if disc < -TOL * (b * b + 1.0):
        return []
    r = math.sqrt(max(disc, 0.0))
    out = []
    for sign in (1, -1) if r > 0 else (1,):
        x = ax + sign * r
        out.append((x, math.atan2(h, x - ax), sign if r > 0 else 0))
    return out


def slider_crank_velocity(a, b, theta2, theta3, omega2):
    """omega3 and the slider speed dx/dt from the derivative of the loop."""
    # real: -a w2 sin t2 - b w3 sin t3 - x' = 0, imag: a w2 cos t2 + b w3 cos t3 = 0
    c3 = math.cos(theta3)
    if abs(c3) <= 1e-14:
        raise ZeroDivisionError("the rod is perpendicular to the slide")
    w3 = -a * omega2 * math.cos(theta2) / (b * c3)
    return w3, -a * omega2 * math.sin(theta2) - b * w3 * math.sin(theta3)


def slider_crank_residual(a, b, e, theta2, x, theta3):
    z = a * complex(math.cos(theta2), math.sin(theta2)) + b * complex(math.cos(theta3), math.sin(theta3))
    return abs(z - complex(x, e))


def joint_turns_fully(x, y, u, v):
    """True if the joint between adjacent links x and y turns through 360 degrees.

    u and v are the other two links. The joint angle phi is feasible exactly
    when the diagonal delta, delta^2 = x^2 + y^2 - 2 x y cos(phi), closes a
    triangle with u and v, so the test is exact for int or Fraction lengths.
    """
    return x + y <= u + v and abs(x - y) >= abs(u - v)


def grashof_class(a, b, c, d):
    """The class of the four-bar with ground d, input a, coupler b, output c.

    Returns one of 'crank-rocker', 'double-crank', 'grashof double-rocker',
    'rocker-crank', 'change point' or 'triple-rocker'. Assumes positive
    lengths and that the loop closes, 2 l <= a + b + c + d.
    """
    links = sorted([a, b, c, d])
    s, p, q, l = links
    if s + l > p + q:
        return "triple-rocker"
    if s + l == p + q:
        return "change point"
    if d == s:
        return "double-crank"
    if a == s:
        return "crank-rocker"
    if c == s:
        return "rocker-crank"
    return "grashof double-rocker"


def input_turns_by_sweep(a, b, c, d, steps=720):
    """True if the loop closes at every theta2 of a sweep that holds 0 and pi."""
    for k in range(steps):
        theta2 = 2 * math.pi * k / steps
        if not fourbar_positions(a, b, c, d, theta2):
            return False
    return True
