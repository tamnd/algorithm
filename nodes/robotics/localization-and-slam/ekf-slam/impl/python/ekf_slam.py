# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ekf-slam/. The authors are listed in prov/P959WA.jsonl.

"""EKF SLAM: one Gaussian over the robot pose and all landmark positions.

The state is mu = [x, y, theta, m1x, m1y, m2x, m2y, ...] and Sigma is its
covariance, a list of rows. The planar models follow Thrun, Burgard and Fox
(2005), Chapter 10: the velocity motion model with the control noise
M = diag(a1 v^2 + a2 omega^2, a3 v^2 + a4 omega^2), and range-bearing
readings z = (r, phi) with the noise covariance Q. A landmark enters the
state at its first reading, through the inverse measurement model.

The three core steps are generic, so that the tests can run them on a linear
model too. They change mu and Sigma in place:

  predict(mu, sigma, rdim, mu_x, g, rx)        robot block and cross terms, O(n)
  augment(mu, sigma, idx, new_mean, gs, gz, q)  add a landmark, O(n)
  update(mu, sigma, idx, nu, h, q)              one reading, O(n^2)

Here n = len(mu), rdim is the size of the robot state, idx lists the state
entries that a reading depends on, and h is the Jacobian with respect to
those entries only (all other columns of the full Jacobian are zero).
"""

import math

import rbm
import robest

STRAIGHT = 1e-9  # below this |omega|, the robot moves on a straight line
RDIM = 3  # the planar pose (x, y, theta)


# ---------------------------------------------------------------- planar models


def motion(x, u, dt):
    """Return the noise-free pose after the control u = (v, omega) for dt seconds."""
    px, py, th = x[0], x[1], x[2]
    v, w = u
    if abs(w) < STRAIGHT:
        return [px + v * dt * math.cos(th), py + v * dt * math.sin(th), th]
    r = v / w
    return [
        px - r * math.sin(th) + r * math.sin(th + w * dt),
        py + r * math.cos(th) - r * math.cos(th + w * dt),
        robest.wrap_angle(th + w * dt),
    ]


def motion_jacobians(x, u, dt):
    """Return G = d motion / d pose (3x3) and V = d motion / d u (3x2)."""
    th = x[2]
    v, w = u
    if abs(w) < STRAIGHT:
        c, s = math.cos(th), math.sin(th)
        g = [[1.0, 0.0, -v * dt * s], [0.0, 1.0, v * dt * c], [0.0, 0.0, 1.0]]
        vj = [[dt * c, -v * dt * dt * s / 2.0], [dt * s, v * dt * dt * c / 2.0], [0.0, dt]]
        return g, vj
    s0, c0 = math.sin(th), math.cos(th)
    s1, c1 = math.sin(th + w * dt), math.cos(th + w * dt)
    g = [[1.0, 0.0, v / w * (c1 - c0)], [0.0, 1.0, v / w * (s1 - s0)], [0.0, 0.0, 1.0]]
    vj = [
        [(s1 - s0) / w, v * (s0 - s1) / (w * w) + v * c1 * dt / w],
        [(c0 - c1) / w, -v * (c0 - c1) / (w * w) + v * s1 * dt / w],
        [0.0, dt],
    ]
    return g, vj


def control_noise(u, alphas):
    """Return M = diag(a1 v^2 + a2 omega^2, a3 v^2 + a4 omega^2)."""
    v, w = u
    a1, a2, a3, a4 = alphas
    return [[a1 * v * v + a2 * w * w, 0.0], [0.0, a3 * v * v + a4 * w * w]]


def measure(x, m):
    """Return the expected (range, bearing) of the landmark m from the pose x."""
    dx, dy = m[0] - x[0], m[1] - x[1]
    return [math.hypot(dx, dy), robest.wrap_angle(math.atan2(dy, dx) - x[2])]


def measure_jacobians(x, m):
    """Return Hx = d measure / d pose (2x3) and Hm = d measure / d m (2x2)."""
    dx, dy = m[0] - x[0], m[1] - x[1]
    q = dx * dx + dy * dy
    sq = math.sqrt(q)
    hx = [[-dx / sq, -dy / sq, 0.0], [dy / q, -dx / q, -1.0]]
    hm = [[dx / sq, dy / sq], [-dy / q, dx / q]]
    return hx, hm


def inverse_measure(x, z):
    """Return the landmark position that gives the reading z = (r, phi) from the pose x."""
    a = x[2] + z[1]
    return [x[0] + z[0] * math.cos(a), x[1] + z[0] * math.sin(a)]


def inverse_jacobians(x, z):
    """Return Gx = d inverse_measure / d pose (2x3) and Gz = d inverse_measure / d z (2x2)."""
    a = x[2] + z[1]
    c, s = math.cos(a), math.sin(a)
    gx = [[1.0, 0.0, -z[0] * s], [0.0, 1.0, z[0] * c]]
    gz = [[c, -z[0] * s], [s, z[0] * c]]
    return gx, gz


# ---------------------------------------------------------------- generic core


def predict(mu, sigma, rdim, mu_x, g, rx):
    """Move the robot part of the belief, in place: lines L2 to L4.

    mu_x is the predicted robot state, g the Jacobian of the motion with
    respect to the robot state, and rx the covariance of the motion noise in
    robot coordinates. The map block of Sigma does not change, so the cost
    is O(n) for a fixed rdim.
    """
    n = len(mu)
    mu[:rdim] = mu_x  # @line L2
    sxx = [row[:rdim] for row in sigma[:rdim]]
    sxx = rbm.add(rbm.mul(rbm.mul(g, sxx), rbm.transpose(g)), rx)  # @line L3
    sxm = rbm.mul(g, [row[rdim:] for row in sigma[:rdim]]) if n > rdim else [[] for _ in range(rdim)]  # @line L4
    for i in range(rdim):
        sigma[i][:rdim] = sxx[i]
        sigma[i][rdim:] = sxm[i]
    for j in range(n - rdim):
        for i in range(rdim):
            sigma[rdim + j][i] = sxm[i][j]


def augment(mu, sigma, idx, new_mean, gs, gz, q):
    """Append a new landmark to the state, in place: line L7.

    The landmark is new_mean = f(state[idx], z). gs is d f / d state[idx]
    and gz is d f / d z, and q is the covariance of z. The new rows of Sigma
    are gs Sigma[idx, :], and the new diagonal block is
    gs Sigma[idx, idx] gs^T + gz q gz^T.
    """
    n = len(mu)
    k = len(new_mean)
    cross = [[sum(gs[a][c] * sigma[idx[c]][col] for c in range(len(idx))) for col in range(n)] for a in range(k)]
    sii = [[sigma[r][c] for c in idx] for r in idx]
    block = rbm.add(rbm.mul(rbm.mul(gs, sii), rbm.transpose(gs)), rbm.mul(rbm.mul(gz, q), rbm.transpose(gz)))
    for r in range(n):
        sigma[r].extend(cross[a][r] for a in range(k))
    for a in range(k):
        sigma.append(cross[a] + block[a])
    mu.extend(new_mean)


def update(mu, sigma, idx, nu, h, q):
    """Apply one reading with innovation nu, in place: lines L9 to L11.

    h is the Jacobian of the reading with respect to state[idx]. The full
    Jacobian H is zero outside the columns idx, so Sigma H^T costs O(n) and
    the covariance update Sigma - K S K^T costs O(n^2).
    """
    n = len(mu)
    d = len(nu)
    k = len(idx)
    pht = [[sum(sigma[r][idx[c]] * h[a][c] for c in range(k)) for a in range(d)] for r in range(n)]
    s = [[sum(h[a][c] * pht[idx[c]][b] for c in range(k)) + q[a][b] for b in range(d)] for a in range(d)]
    sinv = rbm.inv(s)  # @line L9
    kg = [[sum(pht[r][a] * sinv[a][b] for a in range(d)) for b in range(d)] for r in range(n)]
    for r in range(n):
        mu[r] += sum(kg[r][b] * nu[b] for b in range(d))  # @line L10
    for r in range(n):
        kr = kg[r]
        row = sigma[r]
        for c in range(r, n):
            val = row[c] - sum(kr[a] * pht[c][a] for a in range(d))  # @line L11
            row[c] = val
            sigma[c][r] = val


# ---------------------------------------------------------------- planar EKF SLAM


def landmark_index(slot):
    """Return the index of the first coordinate of landmark slot in the state."""
    return RDIM + 2 * slot


def innovation(mu, sigma, slot, z, q):
    """Return (nu, idx, h, S) for the reading z of the landmark in the given slot."""
    j = landmark_index(slot)
    m = mu[j:j + 2]
    zhat = measure(mu, m)
    hx, hm = measure_jacobians(mu, m)
    h = [hx[0] + hm[0], hx[1] + hm[1]]
    idx = [0, 1, 2, j, j + 1]
    nu = [z[0] - zhat[0], robest.wrap_angle(z[1] - zhat[1])]
    s = [[sum(h[a][c] * sum(sigma[idx[c]][idx[e]] * h[b][e] for e in range(5)) for c in range(5)) + q[a][b] for b in range(2)] for a in range(2)]
    return nu, idx, h, s


def nearest(mu, sigma, z, q):
    """Return (slot, d2) of the landmark with the smallest nu^T S^(-1) nu, or (None, inf)."""
    best, best_d2 = None, math.inf
    for slot in range((len(mu) - RDIM) // 2):
        nu, _, _, s = innovation(mu, sigma, slot, z, q)
        d2 = robest.mahalanobis2(nu, [0.0, 0.0], s)
        if d2 < best_d2:
            best, best_d2 = slot, d2
    return best, best_d2


def ekf_slam(mu, sigma, ids, u, dt, zs, alphas, q, correspondences=None, gate=robest.CHI2[(2, 0.99)], new_gate=None):
    """One step of EKF SLAM, in place: lines L1 to L12.

    ids lists the landmark identifiers in the order of the state. With
    known correspondences, correspondences[i] is the identifier of the
    landmark of zs[i]. Otherwise each reading goes to the nearest landmark
    if its squared Mahalanobis distance is at most gate. If the distance is
    above new_gate (by default equal to gate), the reading starts a new
    landmark with the next free integer identifier; between the two
    thresholds the reading is dropped. Return the list of the identifiers
    used, with None for a dropped reading.
    """
    if new_gate is None:
        new_gate = gate
    g, vj = motion_jacobians(mu, u, dt)  # @line L1
    rx = rbm.mul(rbm.mul(vj, control_noise(u, alphas)), rbm.transpose(vj))
    predict(mu, sigma, RDIM, motion(mu, u, dt), g, rx)
    used = []
    for i, z in enumerate(zs):  # @line L5
        if correspondences is not None:
            lid = correspondences[i]
            slot = ids.index(lid) if lid in ids else None
        else:
            slot, d2 = nearest(mu, sigma, z, q)  # @line L6
            if gate < d2 <= new_gate:
                used.append(None)
                continue
            if d2 > new_gate:
                slot = None
            lid = ids[slot] if slot is not None else len(ids)
        if slot is None:
            gx, gz = inverse_jacobians(mu, z)
            augment(mu, sigma, [0, 1, 2], inverse_measure(mu, z), gx, gz, q)  # @line L7
            ids.append(lid)
            used.append(lid)
            continue
        nu, idx, h, _ = innovation(mu, sigma, slot, z, q)  # @line L8
        update(mu, sigma, idx, nu, h, q)
        mu[2] = robest.wrap_angle(mu[2])
        used.append(lid)
    return used  # @line L12
