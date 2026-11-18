# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-bone-inverse-kinematics/. The authors are listed in prov/9Q6NF0.jsonl.
"""Analytic two-bone inverse kinematics with a pole vector.

A limb has the root a (shoulder or hip), the middle joint e (elbow or knee)
and the end f (wrist or ankle), with the bone lengths l1 = |e - a| and
l2 = |f - e|. Given a target t and a pole point p, the method:

1. clamps the distance d = |t - a| to [|l1 - l2|, l1 + l2];
2. finds the angle alpha at the root by the law of cosines;
3. puts the middle joint in the plane of a, t and p, on the side of p.

The end reaches t exactly when |l1 - l2| <= d <= l1 + l2. Otherwise it goes
to the reachable point nearest to t on the ray from a toward t, so an
unreachable far target gives the straight limb pointing at it.

planar_two_bone is the closed form of the planar 2R arm (joint angles
theta1 and theta2, both elbow solutions); it is the reference of the tests.
"""

import math

from anim import add, cross, dot, norm, normalize, scale, sub


def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x


def _orthogonal(x):
    """Return a unit vector orthogonal to the unit vector x (a fixed choice)."""
    k = min(range(3), key=lambda i: abs(x[i]))
    e = tuple(1.0 if i == k else 0.0 for i in range(3))
    return normalize(cross(cross(x, e), x))


def two_bone_ik(a, t, l1, l2, pole):
    """Return (e, f), the middle joint and the end of the limb.

    a: root position; t: target; l1, l2: bone lengths (positive);
    pole: a point that selects the bending plane and side.
    Raise ValueError if t = a (no direction to reach for).
    If the pole lies on the line through a and t, a fixed orthogonal
    direction is used instead.
    """
    v = sub(t, a)  # @line L1
    d = norm(v)
    if d == 0.0:
        raise ValueError("the target is at the root")
    dc = clamp(d, abs(l1 - l2), l1 + l2)  # @line L2
    x = scale(v, 1.0 / d)  # @line L3
    w = sub(pole, a)
    w = sub(w, scale(x, dot(w, x)))  # @line L4
    y = normalize(w) if norm(w) > 1e-12 * max(1.0, norm(sub(pole, a))) else _orthogonal(x)
    if dc == 0.0:
        ca, sa = 1.0, 0.0  # l1 = l2 and the limb folds onto itself
    else:
        ca = clamp((l1 * l1 + dc * dc - l2 * l2) / (2.0 * l1 * dc), -1.0, 1.0)  # @line L5
        # sin(alpha) by the product form of Heron's formula: it is exactly 0
        # for the straight limb, where sqrt(1 - ca^2) would give about 1e-8
        h2 = (dc + l1 + l2) * (l1 + l2 - dc) * (dc - l1 + l2) * (dc + l1 - l2)
        sa = min(1.0, math.sqrt(max(0.0, h2)) / (2.0 * l1 * dc))
    e = add(a, scale(add(scale(x, ca), scale(y, sa)), l1))  # @line L6
    f = add(a, scale(x, dc))  # @line L7
    return e, f  # @line L8


def bend_angle(l1, l2, d):
    """Return the bend theta2 = pi - beta of the middle joint for the distance d."""
    dc = clamp(d, abs(l1 - l2), l1 + l2)
    cb = clamp((l1 * l1 + l2 * l2 - dc * dc) / (2.0 * l1 * l2), -1.0, 1.0)
    return math.pi - math.acos(cb)


def planar_two_bone(x, y, l1, l2, elbow=1):
    """Closed form of the planar 2R arm: return (theta1, theta2).

    elbow = +1 gives theta2 >= 0, elbow = -1 gives theta2 <= 0. The target
    must be reachable.
    """
    c2 = (x * x + y * y - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)
    if c2 < -1.0 - 1e-12 or c2 > 1.0 + 1e-12:
        raise ValueError("the target is not reachable")
    th2 = elbow * math.acos(clamp(c2, -1.0, 1.0))
    th1 = math.atan2(y, x) - math.atan2(l2 * math.sin(th2), l1 + l2 * math.cos(th2))
    return th1, th2


def planar_fk(th1, th2, l1, l2):
    """Forward kinematics of the planar 2R arm: return (elbow, end)."""
    e = (l1 * math.cos(th1), l1 * math.sin(th1))
    f = (e[0] + l2 * math.cos(th1 + th2), e[1] + l2 * math.sin(th1 + th2))
    return e, f
