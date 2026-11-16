# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graphslam/. The authors are listed in prov/DRMB6N.jsonl.

"""GraphSLAM of Thrun and Montemerlo, as in Probabilistic Robotics, Chapter 11.

A planar robot has the poses x_0, ..., x_T, each (x, y, theta) in meters and
radians, and the map has point landmarks m_j = (x, y). The correspondences
are known.

Motion: x_t = g(u_t, x_(t-1)) + noise with covariance Rm, where the control
u_t = (dx, dy, dtheta) is the motion in the frame of x_(t-1).
Measurement: z = (range, bearing) = h(x_t, m_j) + noise with covariance Qm.

The four steps follow the tables of the book:
  initialize  compose the controls to get the poses, and set each landmark
              from its first measurement
  linearize   build the information matrix Omega and the vector xi over all
              poses and landmarks
  reduce      remove the landmarks from Omega and xi by the Schur complement
  solve       solve the reduced system for the path, then recover the
              landmarks one by one
GraphSLAM repeats linearize, reduce and solve until the estimate stops
changing.

Angles inside the estimate are not wrapped, so that the linear system stays
continuous. Each angle difference that enters xi is wrapped to [-pi, pi).

Vectors are lists, matrices are lists of rows. The dense inverse of the
reduced matrix costs O(p^3) for p poses, which is the cost the book states
for this step.
"""

import math

ANCHOR = 1e8  # the information that pins x_0 at its initial mean (the book uses infinity)


def wrap(a):
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def motion(x, u):
    """Return g(u, x): the pose x moved by u, given in the frame of x."""
    c, s = math.cos(x[2]), math.sin(x[2])
    return [x[0] + c * u[0] - s * u[1], x[1] + s * u[0] + c * u[1], x[2] + u[2]]


def motion_jacobian(x, u):
    """Return G = dg/dx at x."""
    c, s = math.cos(x[2]), math.sin(x[2])
    return [[1.0, 0.0, -s * u[0] - c * u[1]], [0.0, 1.0, c * u[0] - s * u[1]], [0.0, 0.0, 1.0]]


def measure(x, m):
    """Return h(x, m) = (range, bearing) of the landmark m from the pose x."""
    dx, dy = m[0] - x[0], m[1] - x[1]
    return [math.hypot(dx, dy), wrap(math.atan2(dy, dx) - x[2])]


def measure_jacobian(x, m):
    """Return the 2 by 5 matrix dh/d(x, m)."""
    dx, dy = m[0] - x[0], m[1] - x[1]
    q = dx * dx + dy * dy
    r = math.sqrt(q)
    return [[-dx / r, -dy / r, 0.0, dx / r, dy / r], [dy / q, -dx / q, -1.0, -dy / q, dx / q]]


# ------------------------------------------------------------ small dense algebra


def inverse(a):
    """Return the inverse of a square matrix by Gauss-Jordan with partial pivoting."""
    n = len(a)
    m = [list(map(float, a[r])) + [1.0 if c == r else 0.0 for c in range(n)] for r in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0.0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        f = m[c][c]
        m[c] = [v / f for v in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0.0:
                f = m[r][c]
                m[r] = [v - f * w for v, w in zip(m[r], m[c])]
    return [row[n:] for row in m]


def matvec(a, x):
    return [sum(ai * xi for ai, xi in zip(row, x)) for row in a]


def _add_block(big, rows, cols, blk, sign=1.0):
    for a, r in enumerate(rows):
        for b, c in enumerate(cols):
            big[r][c] += sign * blk[a][b]


def _quad(jt_rows, w, j_cols):
    """Return J^T W J for J given by its columns (lists)."""
    return [[sum(ci[a] * w[a][b] * cj[b] for a in range(len(w)) for b in range(len(w))) for cj in j_cols] for ci in jt_rows]


# ------------------------------------------------------------------ the steps


class Problem:
    """Controls u[1..T], measurements (t, j, z), and the noise covariances."""

    def __init__(self, controls, measurements, n_landmarks, rm, qm):
        self.u = controls  # controls[t - 1] is u_t
        self.z = measurements
        self.m = n_landmarks
        self.T = len(controls)
        self.rinv = inverse(rm)
        self.qinv = inverse(qm)

    def pose_index(self, t):
        return list(range(3 * t, 3 * t + 3))

    def landmark_index(self, j):
        b = 3 * (self.T + 1) + 2 * j
        return [b, b + 1]

    def size(self):
        return 3 * (self.T + 1) + 2 * self.m


def initialize(pb):
    """Return the initial mean: poses by dead reckoning, landmarks from their first measurement."""
    mu = [[0.0, 0.0, 0.0]]  # @line L1
    for t in range(1, pb.T + 1):
        mu.append(motion(mu[-1], pb.u[t - 1]))
    lm = [None] * pb.m
    for t, j, z in pb.z:
        if lm[j] is None:
            x = mu[t]
            lm[j] = [x[0] + z[0] * math.cos(z[1] + x[2]), x[1] + z[0] * math.sin(z[1] + x[2])]
    if any(l is None for l in lm):
        raise ValueError("every landmark needs a measurement")
    return mu, lm


def linearize(pb, mu, lm):
    """Return (Omega, xi) of all poses and landmarks, linearized at (mu, lm)."""
    n = pb.size()
    om = [[0.0] * n for _ in range(n)]  # @line L2
    xi = [0.0] * n
    for k in range(3):
        om[k][k] += ANCHOR  # x_0 is pinned at its mean, which is 0
    for t in range(1, pb.T + 1):  # @line L3
        u, xp = pb.u[t - 1], mu[t - 1]
        xhat = motion(xp, u)
        xhat[2] = mu[t][2] + wrap(xhat[2] - mu[t][2])  # keep the angle near mu_t
        g = motion_jacobian(xp, u)
        # the residual is x_t - G x_(t-1) - (xhat - G mu_(t-1)); its matrix is [-G  I]
        cols = [[-g[a][c] for a in range(3)] for c in range(3)] + [[1.0 if a == c else 0.0 for a in range(3)] for c in range(3)]
        idx = pb.pose_index(t - 1) + pb.pose_index(t)
        _add_block(om, idx, idx, _quad(cols, pb.rinv, cols))  # @line L4
        rhs = [xhat[a] - sum(g[a][b] * xp[b] for b in range(3)) for a in range(3)]
        for r, col in zip(idx, cols):
            xi[r] += sum(col[a] * pb.rinv[a][b] * rhs[b] for a in range(3) for b in range(3))
    for t, j, z in pb.z:  # @line L5
        x, m = mu[t], lm[j]
        zhat = measure(x, m)
        hj = measure_jacobian(x, m)
        cols = [[hj[a][c] for a in range(2)] for c in range(5)]
        idx = pb.pose_index(t) + pb.landmark_index(j)
        _add_block(om, idx, idx, _quad(cols, pb.qinv, cols))  # @line L6
        state = list(x) + list(m)
        innov = [z[0] - zhat[0], wrap(z[1] - zhat[1])]
        rhs = [innov[a] + sum(hj[a][b] * state[b] for b in range(5)) for a in range(2)]
        for r, col in zip(idx, cols):
            xi[r] += sum(col[a] * pb.qinv[a][b] * rhs[b] for a in range(2) for b in range(2))
    return om, xi


def observers(pb):
    """Return tau: for each landmark, the sorted list of poses that measured it."""
    tau = [set() for _ in range(pb.m)]
    for t, j, _ in pb.z:
        tau[j].add(t)
    return [sorted(s) for s in tau]


def reduce(pb, om, xi):
    """Return (Omega~, xi~) over the poses only, by removing each landmark."""
    p = 3 * (pb.T + 1)
    omr = [row[:p] for row in om[:p]]  # @line L7
    xir = xi[:p]
    for j, ts in enumerate(observers(pb)):  # @line L8
        lj = pb.landmark_index(j)
        rows = [r for t in ts for r in pb.pose_index(t)]
        ojj_inv = inverse([[om[a][b] for b in lj] for a in lj])
        otj = [[om[r][c] for c in lj] for r in rows]  # Omega_(tau(j), j)
        k = [[sum(otj[a][c] * ojj_inv[c][d] for c in range(2)) for d in range(2)] for a in range(len(rows))]
        for a, r in enumerate(rows):
            xir[r] -= sum(k[a][d] * xi[lj[d]] for d in range(2))  # @line L9
            for b, s in enumerate(rows):
                omr[r][s] -= sum(k[a][d] * otj[b][d] for d in range(2))  # @line L10
    return omr, xir


def solve(pb, omr, xir, om, xi):
    """Return (poses, landmarks, Sigma of the path)."""
    sigma = inverse(omr)  # @line L11
    flat = matvec(sigma, xir)  # @line L12
    poses = [flat[3 * t:3 * t + 3] for t in range(pb.T + 1)]
    lms = []
    for j, ts in enumerate(observers(pb)):  # @line L13
        lj = pb.landmark_index(j)
        rows = [r for t in ts for r in pb.pose_index(t)]
        rhs = [xi[a] - sum(om[a][r] * flat[r] for r in rows) for a in lj]
        ojj_inv = inverse([[om[a][b] for b in lj] for a in lj])
        lms.append(matvec(ojj_inv, rhs))  # @line L14
    return poses, lms, sigma


def graphslam(pb, iterations=20, tol=1e-10):
    """Return (poses, landmarks, Sigma, number of iterations)."""
    mu, lm = initialize(pb)  # @line L15
    it = 0
    for it in range(1, iterations + 1):  # @line L16
        om, xi = linearize(pb, mu, lm)  # @line L17
        omr, xir = reduce(pb, om, xi)  # @line L18
        new_mu, new_lm, sigma = solve(pb, omr, xir, om, xi)  # @line L19
        step = max(abs(a - b) for p, q in zip(new_mu, mu) for a, b in zip(p, q))
        step = max([step] + [abs(a - b) for p, q in zip(new_lm, lm) for a, b in zip(p, q)])
        mu, lm = new_mu, new_lm
        if step < tol:  # @line L20
            break
    return mu, lm, sigma, it  # @line L21
