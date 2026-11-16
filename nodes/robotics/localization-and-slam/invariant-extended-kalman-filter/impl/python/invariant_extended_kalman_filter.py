# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/invariant-extended-kalman-filter/. The authors are listed in prov/5ADY95.jsonl.

"""An invariant extended Kalman filter for a planar robot with GPS.

Vectors are lists of floats and matrices are lists of rows, as in rbm.py.
The state is a pose chi = (R(theta), p) in SE(2), stored as the 3x3 matrix
[[R, p], [0, 1]]. A tangent vector is xi = (xi_theta, xi_x, xi_y), and
exp(xi) is the matrix exponential of [[0, -xi_theta, xi_x],
[xi_theta, 0, xi_y], [0, 0, 0]].

Motion: chi_{k+1} = chi_k exp(u_k), where u_k is the body twist increment
over one step (for a car, u = (omega dt, v dt, 0)). Odometry reads
u_m = u + n with n ~ N(0, Q). GPS reads Y = p + V with V ~ N(0, N).

The error is e = chi_hat^-1 chi = exp(xi), so chi = chi_hat exp(xi). This is
the inverse of the left-invariant error eta^L = chi^-1 chi_hat of Barrau and
Bonnabel (2017). With noise-free odometry it evolves as
xi_{k+1} = Ad_{exp(-u_m)} xi_k exactly, whatever chi_hat is.
"""

import math

import rbm

SERIES = 1e-4  # below this |theta|, the coefficient functions use series


def _coeffs(t):
    """Return (sin t / t, (1 - cos t) / t)."""
    if abs(t) < SERIES:
        t2 = t * t
        return 1.0 - t2 / 6.0 + t2 * t2 / 120.0, t / 2.0 - t * t2 / 24.0
    return math.sin(t) / t, (1.0 - math.cos(t)) / t


def se2_exp(xi):
    """Return exp(xi) as a 3x3 matrix, with p = V(theta) (xi_x, xi_y)."""
    t, x, y = xi
    a, b = _coeffs(t)
    c, s = math.cos(t), math.sin(t)
    return [[c, -s, a * x - b * y], [s, c, b * x + a * y], [0.0, 0.0, 1.0]]


def se2_log(m):
    """Return xi with exp(xi) = m and xi_theta in (-pi, pi]."""
    t = math.atan2(m[1][0], m[0][0])
    px, py = m[0][2], m[1][2]
    if abs(t) < SERIES:
        h = 1.0 - t * t / 12.0
    else:
        h = (t / 2.0) * math.sin(t) / (1.0 - math.cos(t))  # (t/2) cot(t/2)
    # V^-1 = [[h, t/2], [-t/2, h]]
    return [t, h * px + (t / 2.0) * py, -(t / 2.0) * px + h * py]


def se2_inv(m):
    """Return the inverse [[R^T, -R^T p], [0, 1]]."""
    c, s = m[0][0], m[1][0]
    px, py = m[0][2], m[1][2]
    return [[c, s, -(c * px + s * py)], [-s, c, s * px - c * py], [0.0, 0.0, 1.0]]


def se2_adjoint(m):
    """Return Ad_m = [[1, 0, 0], [p_y, R], [-p_x, R]], so that m exp(xi) m^-1 = exp(Ad_m xi)."""
    c, s = m[0][0], m[1][0]
    px, py = m[0][2], m[1][2]
    return [[1.0, 0.0, 0.0], [py, c, -s], [-px, s, c]]


def inekf_predict(chi, p, u_m, q):
    """Return (chi, P) after one odometry increment u_m with noise covariance q."""
    chi = rbm.mul(chi, se2_exp(u_m))  # @line L1
    f = se2_adjoint(se2_exp([-x for x in u_m]))  # @line L2
    p = rbm.add(rbm.mul(rbm.mul(f, p), rbm.transpose(f)), q)  # @line L3
    return chi, p


H = [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


def inekf_correct(chi, p, y, n):
    """Return (chi, P, K) after one GPS reading y with noise covariance n (2x2)."""
    inv = se2_inv(chi)
    z = [inv[0][0] * y[0] + inv[0][1] * y[1] + inv[0][2], inv[1][0] * y[0] + inv[1][1] * y[1] + inv[1][2]]  # @line L4
    r = [[chi[0][0], chi[0][1]], [chi[1][0], chi[1][1]]]
    n_hat = rbm.mul(rbm.mul(rbm.transpose(r), n), r)  # R^T N R, equal to N if N is isotropic  # @line L5
    ht = rbm.transpose(H)
    s = rbm.add(rbm.mul(rbm.mul(H, p), ht), n_hat)  # @line L5
    pht = rbm.mul(p, ht)
    k = rbm.transpose(rbm.solve(s, rbm.transpose(pht)))  # K = P H^T S^-1  # @line L6
    chi = rbm.mul(chi, se2_exp(rbm.matvec(k, z)))  # @line L7
    ikh = rbm.sub(rbm.eye(3), rbm.mul(k, H))
    p = rbm.add(rbm.mul(rbm.mul(ikh, p), rbm.transpose(ikh)), rbm.mul(rbm.mul(k, n_hat), rbm.transpose(k)))  # @line L8
    return chi, p, k


def pose(theta, x, y):
    """Return the SE(2) matrix of the pose (theta, x, y)."""
    c, s = math.cos(theta), math.sin(theta)
    return [[c, -s, x], [s, c, y], [0.0, 0.0, 1.0]]
