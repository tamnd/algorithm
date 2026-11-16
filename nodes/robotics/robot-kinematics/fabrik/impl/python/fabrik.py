# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fabrik/. The authors are listed in prov/W25J11.jsonl.
"""FABRIK (forward and backward reaching inverse kinematics) for an
unconstrained chain of points, after Aristidou and Lasenby (2011).

The chain is a list of joint positions p_0, ..., p_n (each a list of floats,
in any dimension) with link lengths d_1, ..., d_n, where d_i = |p_i - p_(i-1)|.
The base p_0 stays fixed and the end effector p_n should reach a target t.

- place(a, b, d) returns the point at distance d from a on the ray towards b.
- backward_pass and forward_pass are the two half steps.
- fabrik(points, lengths, target, ...) returns (points, errors, ok).
- planar_angles(points) turns a planar chain into relative joint angles,
  so that the result can be checked by forward kinematics.

The module needs only the standard library.
"""

import math


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def place(a, b, d):
    """Return the point at distance d from a, on the ray from a towards b.

    If b equals a, the direction is not defined; the first axis is used.
    """
    r = dist(a, b)
    if r == 0.0:
        return [a[0] + d] + list(a[1:])
    lam = d / r
    return [(1.0 - lam) * x + lam * y for x, y in zip(a, b)]


def backward_pass(points, lengths, target):
    """Put the end effector on the target and pull the chain after it."""
    n = len(lengths)
    points[n] = list(target)  # @line L7
    for i in range(n - 1, -1, -1):  # @line L7
        points[i] = place(points[i + 1], points[i], lengths[i])  # @line L7


def forward_pass(points, lengths, base):
    """Put the first joint back on the base and push the chain from it."""
    points[0] = list(base)  # @line L8
    for i in range(len(lengths)):  # @line L8
        points[i + 1] = place(points[i], points[i + 1], lengths[i])  # @line L8


def fabrik(points, lengths, target, eps=1e-10, max_iter=1000):
    """Return (points, errors, ok). errors[k] is |p_n - t| after k iterations.

    If the target is out of reach, the chain is stretched along the line
    from the base towards the target, and ok is False.
    """
    points = [list(p) for p in points]
    base = list(points[0])  # @line L1
    n = len(lengths)
    if dist(base, target) > sum(lengths):  # @line L2
        for i in range(n):  # @line L3
            points[i + 1] = place(points[i], target, lengths[i])  # @line L3
        return points, [dist(points[n], target)], False  # @line L4
    errors = [dist(points[n], target)]
    for _ in range(max_iter):  # @line L5
        if errors[-1] <= eps:  # @line L6
            return points, errors, True  # @line L6
        backward_pass(points, lengths, target)  # @line L7
        forward_pass(points, lengths, base)  # @line L8
        errors.append(dist(points[n], target))
    return points, errors, errors[-1] <= eps  # @line L9


def chain_from_angles(lengths, q):
    """The joint positions of a planar chain with relative angles q, base at the origin."""
    pts = [[0.0, 0.0]]
    a = 0.0
    for length, t in zip(lengths, q):
        a += t
        x, y = pts[-1]
        pts.append([x + length * math.cos(a), y + length * math.sin(a)])
    return pts


def planar_angles(points):
    """Relative joint angles of a planar chain, each in (-pi, pi]."""
    q, prev = [], 0.0
    for a, b in zip(points, points[1:]):
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        q.append(math.remainder(ang - prev, 2.0 * math.pi))
        prev = ang
    return q
