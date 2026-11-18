# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/motion-retargeting/. The authors are listed in prov/0KV7A9.jsonl.
"""Motion retargeting by a minimal displacement curve (after Gleicher 1998).

The character is a planar leg: a root position (rx, ry), a hip angle a1
measured from the downward direction, and a knee angle a2 relative to the
thigh, with the link lengths l1 and l2. The foot is at

    root + l1 (sin a1, -cos a1) + l2 (sin(a1 + a2), -cos(a1 + a2)).

The new motion is q(t) + d(t), where q is the source motion sampled at the
frames and d is a displacement, one uniform cubic B-spline per degree of
freedom, with control points c spaced `spacing` frames apart. The method
solves

    min c^T W c  subject to  foot(q(t_f) + d(t_f)) = p_f for every constrained frame f,

with W diagonal (one weight per degree of freedom). Each step linearizes the
constraints at the current c and takes the minimum norm solution of the
linear constraints, c = W^(-1) J^T (J W^(-1) J^T)^(-1) (J c - r), which is a
step of sequential quadratic programming with the Hessian of the objective.
"""

import math

from anim import solve

DOF = 4


def bspline(s):
    """Return the centered uniform cubic B-spline basis B(s), with support (-2, 2)."""
    s = abs(s)
    if s < 1.0:
        return (4.0 - 6.0 * s * s + 3.0 * s ** 3) / 6.0
    if s < 2.0:
        return (2.0 - s) ** 3 / 6.0
    return 0.0


def control_count(frames, spacing):
    """Return the number of control points per degree of freedom."""
    return int(math.floor((frames - 1) / spacing)) + 4


def basis(frame, spacing, count):
    """Return [(j, B(frame / spacing - j + 1))] for the control points that are not zero."""
    u = frame / spacing + 1.0
    lo = max(0, int(math.floor(u)) - 1)
    hi = min(count - 1, int(math.floor(u)) + 2)
    return [(j, bspline(u - j)) for j in range(lo, hi + 1) if bspline(u - j) != 0.0]


def displacement(c, frame, spacing, count):
    """Return d(frame), one value per degree of freedom; c is indexed [dof * count + j]."""
    b = basis(frame, spacing, count)
    return [sum(w * c[k * count + j] for j, w in b) for k in range(DOF)]


def foot(q, lengths):
    """Return the foot position of the pose q = (rx, ry, a1, a2)."""
    rx, ry, a1, a2 = q
    l1, l2 = lengths
    return (
        rx + l1 * math.sin(a1) + l2 * math.sin(a1 + a2),
        ry - l1 * math.cos(a1) - l2 * math.cos(a1 + a2),
    )


def foot_jacobian(q, lengths):
    """Return the 2 by 4 Jacobian of the foot position in (rx, ry, a1, a2)."""
    _, _, a1, a2 = q
    l1, l2 = lengths
    c12, s12 = math.cos(a1 + a2), math.sin(a1 + a2)
    return [
        [1.0, 0.0, l1 * math.cos(a1) + l2 * c12, l2 * c12],
        [0.0, 1.0, l1 * math.sin(a1) + l2 * s12, l2 * s12],
    ]


def retarget(source, lengths, constraints, spacing=2, weights=(1.0, 1.0, 1.0, 1.0), max_iter=50, tol=1e-11):
    """Return (motion, c, iterations) for the new character.

    source is a list of poses (rx, ry, a1, a2), one per frame. constraints is
    a list of (frame, (px, py)): the foot of the new character must be at p
    at that frame.
    """
    frames = len(source)
    count = control_count(frames, spacing)
    size = DOF * count
    winv = [1.0 / weights[k] for k in range(DOF) for _ in range(count)]
    c = [0.0] * size  # @line L1
    for it in range(1, max_iter + 1):  # @line L2
        jac, res = [], []
        for f, p in constraints:  # @line L3
            q = [a + b for a, b in zip(source[f], displacement(c, f, spacing, count))]
            g = foot(q, lengths)
            jq = foot_jacobian(q, lengths)
            b = basis(f, spacing, count)
            for row in range(2):
                r = [0.0] * size
                for k in range(DOF):
                    for j, w in b:
                        r[k * count + j] = jq[row][k] * w
                jac.append(r)
                res.append(g[row] - p[row])
        m = len(res)
        jc = [sum(x * y for x, y in zip(r, c)) for r in jac]
        rhs = [a - b for a, b in zip(jc, res)]  # @line L4
        gram = [[sum(jac[a][i] * winv[i] * jac[b][i] for i in range(size)) for b in range(m)] for a in range(m)]
        mu = solve(gram, rhs)  # @line L5
        new = [winv[i] * sum(jac[a][i] * mu[a] for a in range(m)) for i in range(size)]  # @line L6
        change = max(abs(x - y) for x, y in zip(new, c))
        c = new
        if change <= tol * (1.0 + max(abs(v) for v in c)) and max(abs(v) for v in res) <= 1e-9:  # @line L7
            break
    motion = []
    for f in range(frames):  # @line L8
        motion.append(tuple(a + b for a, b in zip(source[f], displacement(c, f, spacing, count))))
    return motion, c, it
