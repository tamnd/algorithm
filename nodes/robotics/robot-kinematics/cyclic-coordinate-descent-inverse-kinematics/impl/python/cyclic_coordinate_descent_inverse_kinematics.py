# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyclic-coordinate-descent-inverse-kinematics/. The authors are listed in prov/JXW2FC.jsonl.
"""Cyclic coordinate descent (CCD) inverse kinematics for a serial chain of
revolute joints in 3D, with a position target for the end effector.

The chain is a list of joints. Joint i has a unit axis axes[i] and a link
vector links[i], both given in the frame of the link before the joint (the
world frame for joint 0). With all angles zero the frames are aligned.
Joint 0 sits at the origin, joint i + 1 sits at the end of link i, and the
end effector sits at the end of the last link.

- joint_frames(axes, links, q) returns the world positions and axes of the
  joints and the end effector position.
- best_angle(w, p, e, t) returns the angle about the axis (w, p) that brings
  the point e as close as possible to the point t, in closed form.
- ccd_sweep(...) updates the joints once each, from the tip to the base.
- ik_ccd(...) repeats sweeps and returns (q, errors, ok).

Vectors are lists of 3 floats. The module needs only the standard library.
"""

import math


def add(a, b):
    return [x + y for x, y in zip(a, b)]


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def scale(s, a):
    return [s * x for x in a]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def norm(a):
    return math.sqrt(dot(a, a))


def rotate(w, phi, x):
    """Rotate the vector x about the unit axis w by the angle phi (Rodrigues)."""
    c, s = math.cos(phi), math.sin(phi)
    return add(add(scale(c, x), scale(s, cross(w, x))), scale((1.0 - c) * dot(w, x), w))


def rot_matrix(w, phi):
    cols = [rotate(w, phi, e) for e in ([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0])]
    return [[cols[j][i] for j in range(3)] for i in range(3)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def matvec(a, x):
    return [dot(row, x) for row in a]


def joint_frames(axes, links, q):
    """Return (positions, world_axes, end) of the chain at the joint angles q."""
    r = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    p = [0.0, 0.0, 0.0]
    positions, world_axes = [], []
    for a, link, angle in zip(axes, links, q):
        positions.append(p)
        world_axes.append(matvec(r, a))
        r = matmul(r, rot_matrix(a, angle))
        p = add(p, matvec(r, link))
    return positions, world_axes, p


def best_angle(w, p, e, t):
    """Return the angle phi about the axis through p along the unit vector w
    that minimizes |p + R(w, phi)(e - p) - t|."""
    u, v = sub(e, p), sub(t, p)
    u_perp = sub(u, scale(dot(w, u), w))  # @line L6
    v_perp = sub(v, scale(dot(w, v), w))  # @line L6
    a = dot(u_perp, v_perp)  # @line L7
    b = dot(w, cross(u_perp, v_perp))  # @line L7
    if a == 0.0 and b == 0.0:
        return 0.0  # every angle is as good
    return math.atan2(b, a)  # @line L7


def ccd_sweep(axes, links, q, target):
    """One sweep from the tip to the base. Return (new q, end effector position).

    Turning joint i moves only the end effector and the joints after i, so the
    positions and axes of joints 0 to i - 1, found once by forward kinematics,
    stay valid, and the end effector is rotated in place.
    """
    q = list(q)
    positions, world_axes, e = joint_frames(axes, links, q)  # @line L3
    for i in range(len(q) - 1, -1, -1):  # @line L5
        w, p = world_axes[i], positions[i]
        phi = best_angle(w, p, e, target)  # @line L6
        q[i] += phi  # @line L8
        e = add(p, rotate(w, phi, sub(e, p)))  # @line L8
    return q, e


def ik_ccd(axes, links, target, q0, eps=1e-10, max_sweeps=1000, min_gain=0.0):
    """Repeat CCD sweeps. Return (q, errors, ok), with errors[k] the distance
    to the target after k sweeps.

    The loop stops when the error is at most eps (ok is True), or when a sweep
    lowers the error by at most min_gain, or after max_sweeps sweeps.
    """
    q = [float(x) for x in q0]  # @line L1
    err = norm(sub(joint_frames(axes, links, q)[2], target))
    errors = [err]
    for _ in range(max_sweeps):  # @line L2
        if err <= eps:  # @line L4
            return q, errors, True  # @line L4
        q, e = ccd_sweep(axes, links, q, target)  # @line L5
        new_err = norm(sub(e, target))
        errors.append(new_err)
        if err - new_err <= min_gain and new_err > eps:
            return q, errors, False
        err = new_err
    return q, errors, err <= eps  # @line L9


def planar_chain(lengths):
    """A planar chain in the x-y plane: every axis is z and every link points along x."""
    return [[0.0, 0.0, 1.0] for _ in lengths], [[length, 0.0, 0.0] for length in lengths]
