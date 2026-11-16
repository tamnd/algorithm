# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paden-kahan-subproblems/. The authors are listed in prov/MGK2K1.jsonl.
"""The three Paden-Kahan subproblems and an elbow arm solved with them.

Each subproblem is about rotations about unit axes w that pass through a
point r. A rotation by theta takes a point x to r + Rot(w, theta) (x - r),
which is exp([xi] theta) x for the revolute twist xi = (w, -w x r).

- subproblem1(w, r, p, q): theta with exp([xi] theta) p = q.
- subproblem2(w1, w2, r, p, q): all (theta1, theta2) with
  exp([xi1] theta1) exp([xi2] theta2) p = q, for two axes that meet at r.
- subproblem3(w, r, p, q, delta): all theta with |exp([xi] theta) p - q| = delta.

elbow_ik(g_d, lengths) applies them to a six joint elbow arm with a
spherical wrist (the arm of Murray, Li and Sastry, Section 3.3) and
returns every solution, up to 8. The arm is in the space form of the
product of exponentials, T(theta) = exp([S1] theta1) ... exp([S6] theta6) M.
The subproblems return an empty list, or None for subproblem 1, when
there is no solution.
"""

import math

import rbm

TOL = 1e-9


def _proj(w, x):
    """Return the part of x orthogonal to the unit vector w."""
    d = rbm.dot(w, x)
    return [xi - d * wi for xi, wi in zip(x, w)]


def rotate_about(w, r, theta, x):
    """Return the image of the point x under the rotation by theta about the line (w, r)."""
    rot = rbm.so3_exp([theta * wi for wi in w])
    return rbm.add(r, rbm.matvec(rot, rbm.sub(x, r)))


def subproblem1(w, r, p, q, tol=TOL):
    """Return theta with Rot(w, theta) (p - r) = q - r, or None if there is none.

    If p lies on the axis, every theta works and 0.0 is returned.
    """
    u = rbm.sub(p, r)  # @line L1
    v = rbm.sub(q, r)
    u1 = _proj(w, u)  # @line L2
    v1 = _proj(w, v)
    scale = 1.0 + rbm.norm(u) + rbm.norm(v)
    if abs(rbm.dot(w, u) - rbm.dot(w, v)) > tol * scale or abs(rbm.norm(u1) - rbm.norm(v1)) > tol * scale:  # @line L3
        return None
    if rbm.norm(u1) <= tol * scale:
        return 0.0
    return math.atan2(rbm.dot(w, rbm.cross(u1, v1)), rbm.dot(u1, v1))  # @line L4


def subproblem2(w1, w2, r, p, q, tol=TOL):
    """Return the list of (theta1, theta2) with Rot1(theta1) Rot2(theta2) p = q.

    The axes (w1, r) and (w2, r) meet at r and are not parallel. The list
    has 0, 1 or 2 pairs.
    """
    u = rbm.sub(p, r)  # @line L5
    v = rbm.sub(q, r)
    k = rbm.dot(w1, w2)
    if abs(rbm.norm(u) - rbm.norm(v)) > tol * (1.0 + rbm.norm(u)):
        return []
    alpha = (k * rbm.dot(w2, u) - rbm.dot(w1, v)) / (k * k - 1.0)  # @line L6
    beta = (k * rbm.dot(w1, v) - rbm.dot(w2, u)) / (k * k - 1.0)
    w12 = rbm.cross(w1, w2)
    g2 = (rbm.dot(u, u) - alpha * alpha - beta * beta - 2.0 * alpha * beta * k) / rbm.dot(w12, w12)  # @line L7
    if g2 < -tol * (1.0 + rbm.dot(u, u)):  # @line L8
        return []
    g = math.sqrt(max(g2, 0.0))
    gammas = [g, -g] if g > tol * (1.0 + rbm.norm(u)) else [0.0]
    out = []
    for gamma in gammas:  # @line L9
        z = [alpha * a + beta * b + gamma * c for a, b, c in zip(w1, w2, w12)]  # @line L10
        c = rbm.add(r, z)
        th2 = subproblem1(w2, r, p, c, tol=1e-6)  # @line L11
        th1 = subproblem1(w1, r, c, q, tol=1e-6)
        if th1 is not None and th2 is not None:
            out.append((th1, th2))  # @line L12
    return out


def subproblem3(w, r, p, q, delta, tol=TOL):
    """Return the list of theta with |Rot(w, theta) (p - r) + r - q| = delta.

    The list has 0, 1 or 2 angles in (-pi, pi].
    """
    u = rbm.sub(p, r)  # @line L13
    v = rbm.sub(q, r)
    u1 = _proj(w, u)
    v1 = _proj(w, v)
    d2 = delta * delta - rbm.dot(w, rbm.sub(p, q)) ** 2  # @line L14
    th0 = math.atan2(rbm.dot(w, rbm.cross(u1, v1)), rbm.dot(u1, v1))  # @line L15
    nu, nv = rbm.norm(u1), rbm.norm(v1)
    if nu <= tol or nv <= tol:
        return []
    c = (nu * nu + nv * nv - d2) / (2.0 * nu * nv)  # @line L16
    if abs(c) > 1.0 + tol:  # @line L17
        return []
    c = max(-1.0, min(1.0, c))
    a = math.acos(c)
    if a <= tol:
        return [_wrap(th0)]
    return [_wrap(th0 - a), _wrap(th0 + a)]  # @line L18


def _wrap(x):
    """Return x moved into (-pi, pi]."""
    y = math.fmod(x + math.pi, 2.0 * math.pi)
    if y <= 0.0:
        y += 2.0 * math.pi
    return y - math.pi


# ---------------------------------------------------------------- the elbow arm


def elbow_arm(l0=1.0, l1=1.0, l2=1.0, l3=0.5):
    """Return (axes, M, points) of the elbow arm with a spherical wrist.

    axes is a list of six (w, r) pairs at the zero configuration. The
    shoulder is at (0, 0, l0), the elbow at (0, l1, l0) and the wrist
    center at (0, l1 + l2, l0); the tool point is l3 further along y.
    """
    qs = [0.0, 0.0, l0]
    qe = [0.0, l1, l0]
    qw = [0.0, l1 + l2, l0]
    z, mx, y = [0.0, 0.0, 1.0], [-1.0, 0.0, 0.0], [0.0, 1.0, 0.0]
    axes = [(z, [0.0, 0.0, 0.0]), (mx, qs), (mx, qe), (z, qw), (mx, qw), (y, qw)]
    m = rbm.make_T(rbm.eye(3), [0.0, l1 + l2 + l3, l0])
    return axes, m, {"shoulder": qs, "elbow": qe, "wrist": qw}


def screw(w, r):
    """Return the space screw axis (w, -w x r) of a revolute joint."""
    return list(w) + [-x for x in rbm.cross(w, r)]


def fk(axes, m, theta):
    """Return T(theta) = exp([S1] theta1) ... exp([Sn] thetan) M."""
    t = rbm.eye(4)
    for (w, r), th in zip(axes, theta):
        t = rbm.mul(t, rbm.se3_exp([x * th for x in screw(w, r)]))
    return rbm.mul(t, m)


def elbow_ik(axes, m, points, g_d):
    """Return every theta (a list of 6-tuples) with fk(axes, m, theta) = g_d."""
    qs, qw = points["shoulder"], points["wrist"]
    g1 = rbm.mul(g_d, rbm.T_inv(m))
    pw = rbm.T_apply(g1, qw)  # where the wrist center must go
    delta = rbm.norm(rbm.sub(pw, qs))
    (w1, _), (w2, _), (w3, r3), (w4, _), (w5, _), (w6, _) = axes
    sols = []
    for th3 in subproblem3(w3, r3, qw, qs, delta):
        p3 = rotate_about(w3, r3, th3, qw)
        for th1, th2 in subproblem2(w1, w2, qs, p3, pw):
            t123 = fk(axes[:3], rbm.eye(4), [th1, th2, th3])
            g2 = rbm.mul(rbm.T_inv(t123), g1)  # = exp([S4] th4) exp([S5] th5) exp([S6] th6)
            p6 = rbm.add(qw, w6)  # a point on axis 6, off axes 4 and 5
            for th4, th5 in subproblem2(w4, w5, qw, p6, rbm.T_apply(g2, p6)):
                t45 = fk(axes[3:5], rbm.eye(4), [th4, th5])
                g3 = rbm.mul(rbm.T_inv(t45), g2)  # = exp([S6] th6)
                p = rbm.add(qw, w4)  # a point off axis 6
                th6 = subproblem1(w6, qw, p, rbm.T_apply(g3, p), tol=1e-6)
                if th6 is not None:
                    sols.append(tuple(_wrap(x) for x in (th1, th2, th3, th4, th5, th6)))
    return sols
