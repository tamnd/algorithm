# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ekf-localization/. The authors are listed in prov/EVPG4E.jsonl.

"""EKF localization with the velocity motion model and range-bearing landmarks.

The notation follows Thrun, Burgard and Fox (2005), Section 7.4.
The state is the planar pose mu = [x, y, theta]; Sigma is its 3x3 covariance.
A control is u = (v, omega), held for dt seconds. The noise of the control has
the covariance M = diag(a1 v^2 + a2 omega^2, a3 v^2 + a4 omega^2).
A landmark is a point (m_x, m_y) of the map. A measurement of a landmark is
z = (r, phi), the range and the bearing relative to the heading, with the
noise covariance Q = diag(sigma_r^2, sigma_phi^2). Angles wrap to [-pi, pi).
"""

import math

import rbm
import robest

STRAIGHT = 1e-9  # below this |omega|, the robot moves on a straight line


def motion(mu, u, dt):
    """Return the noise-free pose after the control u = (v, omega) for dt seconds."""
    x, y, th = mu
    v, w = u
    if abs(w) < STRAIGHT:
        return [x + v * dt * math.cos(th), y + v * dt * math.sin(th), th]
    r = v / w
    return [
        x - r * math.sin(th) + r * math.sin(th + w * dt),
        y + r * math.cos(th) - r * math.cos(th + w * dt),
        robest.wrap_angle(th + w * dt),
    ]


def motion_jacobians(mu, u, dt):
    """Return G = d motion / d mu and V = d motion / d u at (mu, u)."""
    _, _, th = mu
    v, w = u
    if abs(w) < STRAIGHT:
        c, s = math.cos(th), math.sin(th)
        g = [[1.0, 0.0, -v * dt * s], [0.0, 1.0, v * dt * c], [0.0, 0.0, 1.0]]
        vj = [[dt * c, -v * dt * dt * s / 2.0], [dt * s, v * dt * dt * c / 2.0], [0.0, dt]]
        return g, vj
    s0, c0 = math.sin(th), math.cos(th)
    s1, c1 = math.sin(th + w * dt), math.cos(th + w * dt)
    g = [[1.0, 0.0, -v / w * c0 + v / w * c1], [0.0, 1.0, -v / w * s0 + v / w * s1], [0.0, 0.0, 1.0]]
    vj = [
        [(-s0 + s1) / w, v * (s0 - s1) / (w * w) + v * c1 * dt / w],
        [(c0 - c1) / w, -v * (c0 - c1) / (w * w) + v * s1 * dt / w],
        [0.0, dt],
    ]
    return g, vj


def measure(mu, landmark):
    """Return the expected (range, bearing) of a landmark from the pose mu."""
    dx, dy = landmark[0] - mu[0], landmark[1] - mu[1]
    return [math.hypot(dx, dy), robest.wrap_angle(math.atan2(dy, dx) - mu[2])]


def measure_jacobian(mu, landmark):
    """Return H = d measure / d mu (2x3)."""
    dx, dy = landmark[0] - mu[0], landmark[1] - mu[1]
    q = dx * dx + dy * dy
    sq = math.sqrt(q)
    return [[-dx / sq, -dy / sq, 0.0], [dy / q, -dx / q, -1.0]]


def predict(mu, sigma, u, dt, alphas):
    """The prediction of EKF localization: lines L1 to L5."""
    v, w = u
    a1, a2, a3, a4 = alphas
    g, vj = motion_jacobians(mu, u, dt)  # @line L1
    m = [[a1 * v * v + a2 * w * w, 0.0], [0.0, a3 * v * v + a4 * w * w]]  # @line L2
    mu_bar = motion(mu, u, dt)  # @line L3
    sigma_bar = rbm.add(rbm.mul(rbm.mul(g, sigma), rbm.transpose(g)), rbm.mul(rbm.mul(vj, m), rbm.transpose(vj)))  # @line L4
    return mu_bar, sigma_bar


def innovation(mu, sigma, z, landmark, q):
    """Return (nu, H, S): the innovation z - h(mu), its Jacobian and its covariance."""
    zhat = measure(mu, landmark)  # @line L7
    h = measure_jacobian(mu, landmark)  # @line L8
    s = rbm.add(rbm.mul(rbm.mul(h, sigma), rbm.transpose(h)), q)  # @line L9
    nu = [z[0] - zhat[0], robest.wrap_angle(z[1] - zhat[1])]
    return nu, h, s


def update(mu, sigma, z, landmark, q):
    """The correction with one measurement of a known landmark: lines L7 to L12."""
    nu, h, s = innovation(mu, sigma, z, landmark, q)
    k = rbm.mul(rbm.mul(sigma, rbm.transpose(h)), rbm.inv(s))  # @line L10
    dmu = rbm.matvec(k, nu)
    mu = [mu[0] + dmu[0], mu[1] + dmu[1], robest.wrap_angle(mu[2] + dmu[2])]  # @line L11
    sigma = rbm.mul(rbm.sub(rbm.eye(3), rbm.mul(k, h)), sigma)  # @line L12
    sigma = [[(sigma[i][j] + sigma[j][i]) / 2.0 for j in range(3)] for i in range(3)]
    return mu, sigma


def associate(mu, sigma, z, landmarks, q, gate):
    """Return the index of the most likely landmark for z, or None if it fails the gate.

    The likelihood of landmark j is N(nu_j; 0, S_j). A landmark is a candidate
    only if nu_j^T S_j^(-1) nu_j <= gate (for example 9.210, the 0.99 quantile
    of the chi-square distribution with 2 degrees of freedom).
    """
    best, best_ll = None, -math.inf
    for j, lm in enumerate(landmarks):
        nu, _, s = innovation(mu, sigma, z, lm, q)
        d2 = robest.mahalanobis2(nu, [0.0, 0.0], s)
        if d2 > gate:
            continue
        ll = -0.5 * d2 - 0.5 * math.log(rbm.det(s))
        if ll > best_ll:
            best, best_ll = j, ll
    return best


def ekf_localization(mu, sigma, u, dt, zs, landmarks, alphas, q, correspondences=None, gate=robest.CHI2[(2, 0.99)]):
    """One step of EKF localization: lines L1 to L13.

    zs is a list of (range, bearing) readings. If correspondences is given,
    correspondences[i] is the index of the landmark of zs[i] (the case of
    known correspondences in Thrun et al., Section 7.4). Otherwise each reading is associated by maximum
    likelihood with a chi-square gate, and a reading that fails the gate is
    ignored. Return (mu, Sigma, the list of the used landmark indices).
    """
    mu, sigma = predict(mu, sigma, u, dt, alphas)
    used = []
    for i, z in enumerate(zs):  # @line L5
        j = correspondences[i] if correspondences is not None else associate(mu, sigma, z, landmarks, q, gate)  # @line L6
        if j is None:
            used.append(None)
            continue
        mu, sigma = update(mu, sigma, z, landmarks[j], q)
        used.append(j)
    return mu, sigma, used  # @line L13
