# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/error-state-kalman-filter/. The authors are listed in prov/2VDFY7.jsonl.

"""An error-state Kalman filter for attitude and gyro bias.

Vectors are lists of floats and matrices are lists of rows, as in rbm.py.
The nominal state is a unit Hamilton quaternion q (scalar first) of R_sb,
the attitude of the body in the space frame, and a gyro bias b. The error
state is dx = (dtheta, db) with the local (right) convention of Sola (2017):

    q_true = q (x) q{dtheta},  b_true = b + db,

where q{v} is the unit quaternion of the rotation vector v. A gyro reads
omega_m = omega + b_true + n with white noise n of standard deviation
sigma_g (rad/s) per sample, and the bias drifts as a random walk with
standard deviation sigma_w sqrt(dt). A vector sensor reads the body form
y = R_true^T d + v of a known unit direction d in {s}, with white noise v
of standard deviation sigma_v per axis.

The filter keeps the nominal state outside the Kalman filter and runs a
linear Kalman filter on dx, whose mean is zero between corrections.
"""

import rbm


def quat_of_rotvec(v):
    """Return q{v} = (cos(|v|/2), sin(|v|/2) v/|v|), with q{0} = (1, 0, 0, 0)."""
    return rbm.quat_from_axis_angle(v, rbm.norm(v))


def _normalize(q):
    n = rbm.norm(q)
    return [x / n for x in q]


def _block(a, b, c, d):
    """Return the 6x6 matrix [[a, b], [c, d]] from four 3x3 blocks."""
    return [a[i] + b[i] for i in range(3)] + [c[i] + d[i] for i in range(3)]


def eskf_predict(q, b, p, omega_m, dt, sigma_g, sigma_w):
    """Return (q, b, P) after one gyro sample of length dt."""
    w = rbm.sub(omega_m, b)  # @line L1
    wdt = rbm.scale(w, dt)
    q = _normalize(rbm.quat_mul(q, quat_of_rotvec(wdt)))  # @line L2
    z3 = rbm.zeros(3, 3)
    f = _block(rbm.transpose(rbm.so3_exp(wdt)), rbm.scale(rbm.eye(3), -dt), z3, rbm.eye(3))  # @line L3
    qg = sigma_g * sigma_g * dt * dt
    qw = sigma_w * sigma_w * dt
    p = rbm.mul(rbm.mul(f, p), rbm.transpose(f))  # @line L4
    for i in range(3):
        p[i][i] += qg  # @line L4
        p[i + 3][i + 3] += qw  # @line L4
    return q, list(b), p


def eskf_correct(q, b, p, y, d, sigma_v):
    """Return (q, b, P) after one direction measurement y of the known direction d."""
    y_hat = rbm.matvec(rbm.transpose(rbm.quat_to_rot(q)), d)  # @line L5
    h = [row + [0.0, 0.0, 0.0] for row in rbm.hat3(y_hat)]  # @line L6
    ht = rbm.transpose(h)
    s = rbm.mul(rbm.mul(h, p), ht)
    for i in range(3):
        s[i][i] += sigma_v * sigma_v
    pht = rbm.mul(p, ht)
    k = rbm.transpose(rbm.solve(s, rbm.transpose(pht)))  # K = P H^T S^-1, S symmetric  # @line L7
    dx = rbm.matvec(k, rbm.sub(y, y_hat))  # @line L8
    ikh = rbm.sub(rbm.eye(6), rbm.mul(k, h))
    p = rbm.mul(rbm.mul(ikh, p), rbm.transpose(ikh))  # @line L9
    kkt = rbm.mul(k, rbm.transpose(k))
    p = rbm.add(p, rbm.scale(kkt, sigma_v * sigma_v))  # Joseph form  # @line L9
    dtheta, db = dx[:3], dx[3:]
    q = _normalize(rbm.quat_mul(q, quat_of_rotvec(dtheta)))  # @line L10
    b = rbm.add(b, db)  # @line L10
    g = rbm.sub(rbm.eye(3), rbm.hat3(rbm.scale(dtheta, 0.5)))
    z3 = rbm.zeros(3, 3)
    gm = _block(g, z3, z3, rbm.eye(3))  # @line L11
    p = rbm.mul(rbm.mul(gm, p), rbm.transpose(gm))  # @line L11
    return q, b, p


def attitude_error(q_true, q):
    """Return dtheta with q_true = q (x) q{dtheta} (the local attitude error)."""
    r = rbm.mul(rbm.transpose(rbm.quat_to_rot(q)), rbm.quat_to_rot(q_true))
    return rbm.so3_log(r)
