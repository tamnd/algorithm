# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-extended-information-filter/. The authors are listed in prov/1KKHWC.jsonl.

"""The sparse extended information filter (SEIF) for planar SLAM.

After Thrun, Burgard and Fox (2005), Chapter 12, and Thrun et al. (2004).
The state is y = (x, y, theta, m1x, m1y, m2x, m2y, ...). The filter keeps
the information matrix Omega, the information vector xi and an estimate mu
of the mean. A landmark is *active* if Omega links it to the pose. The
sparsification step keeps at most max_active active landmarks: it removes
the links between the pose and the other ones by an approximation, so that
Omega stays sparse.

Motion, update and sparsification change only the entries of the pose and
of the active landmarks. Omega is stored as a dense list of rows to keep
the code short; with a sparse store, these steps cost constant time when
the number of active landmarks is bounded. The mean recovery scans whole
rows of Omega here, which a sparse store would also avoid.

The models are the velocity motion model with the control noise
M = diag(a1 v^2 + a2 w^2, a3 v^2 + a4 w^2) and range-bearing readings with
the noise covariance Q, as on the EKF SLAM page.
"""

import math

import rbm
import robest

STRAIGHT = 1e-9


# ---------------------------------------------------------------- planar models


def motion_offset(x, u, dt):
    """Return delta with motion(x) = x + delta, and the Jacobians G (3x3) and V (3x2)."""
    th = x[2]
    v, w = u
    if abs(w) < STRAIGHT:
        c, s = math.cos(th), math.sin(th)
        delta = [v * dt * c, v * dt * s, 0.0]
        g = [[1.0, 0.0, -v * dt * s], [0.0, 1.0, v * dt * c], [0.0, 0.0, 1.0]]
        vj = [[dt * c, -v * dt * dt * s / 2.0], [dt * s, v * dt * dt * c / 2.0], [0.0, dt]]
        return delta, g, vj
    r = v / w
    s0, c0 = math.sin(th), math.cos(th)
    s1, c1 = math.sin(th + w * dt), math.cos(th + w * dt)
    delta = [-r * s0 + r * s1, r * c0 - r * c1, w * dt]
    g = [[1.0, 0.0, r * (c1 - c0)], [0.0, 1.0, r * (s1 - s0)], [0.0, 0.0, 1.0]]
    vj = [
        [(s1 - s0) / w, v * (s0 - s1) / (w * w) + v * c1 * dt / w],
        [(c0 - c1) / w, -v * (c0 - c1) / (w * w) + v * s1 * dt / w],
        [0.0, dt],
    ]
    return delta, g, vj


def measure(x, m):
    """Return the expected (range, bearing) of the landmark m from the pose x."""
    dx, dy = m[0] - x[0], m[1] - x[1]
    return [math.hypot(dx, dy), robest.wrap_angle(math.atan2(dy, dx) - x[2])]


def measure_jacobian(x, m):
    """Return the 2x5 Jacobian of measure with respect to (x, y, theta, mx, my)."""
    dx, dy = m[0] - x[0], m[1] - x[1]
    q = dx * dx + dy * dy
    s = math.sqrt(q)
    return [
        [-dx / s, -dy / s, 0.0, dx / s, dy / s],
        [dy / q, -dx / q, -1.0, -dy / q, dx / q],
    ]


def inverse_measure(x, z):
    """Return the landmark that gives the reading z = (r, phi) from the pose x."""
    a = x[2] + z[1]
    return [x[0] + z[0] * math.cos(a), x[1] + z[0] * math.sin(a)]


# ---------------------------------------------------------------- small helpers


def sub_matrix(a, rows, cols):
    return [[a[r][c] for c in cols] for r in rows]


def marginalize(block, keep, out):
    """Return the information matrix of the variables keep after the variables out are removed.

    block is a dict-like accessor block(r, c); keep and out are lists of
    indices. The result is Omega_kk - Omega_ko Omega_oo^(-1) Omega_ok.
    """
    okk = [[block(r, c) for c in keep] for r in keep]
    if not out:
        return okk
    oko = [[block(r, c) for c in out] for r in keep]
    ooo = [[block(r, c) for c in out] for r in out]
    sol = rbm.solve(ooo, rbm.transpose(oko))  # Omega_oo^(-1) Omega_ok
    return rbm.sub(okk, rbm.mul(oko, sol))


def sparsify_info(om, xi, mu, x, mp, m0):
    """Remove the links between the variables x and m0, in place: line L12.

    om and xi are the information matrix and vector, mu the mean, and x, mp
    and m0 lists of indices. Every variable that om links to x must be in
    mp or m0; the other variables (the passive ones, m-) are fixed at
    their mean. The new matrix is Omega1 - Omega2 + Omega3, where
      Omega1 is the information of (x, m+) given m- after m0 is removed,
      Omega2 is the information of m+ given m- after x and m0 are removed,
      Omega3 is the information of all variables but x after x is removed.
    It describes p(x | m+, m- = mu-) p(m). The mean mu does not change,
    and xi changes by (new Omega - Omega) mu. Only the block of x, m+ and
    m0 changes.
    """
    s = x + mp + m0
    pos = {g: a for a, g in enumerate(s)}
    k = len(s)
    nx = len(x)

    def blk(r, c):
        return om[r][c]

    o1 = marginalize(blk, x + mp, m0)
    o2 = marginalize(blk, mp, x + m0)
    oxs = [[om[r][c] for c in s] for r in x]  # Omega[x, S]
    sol = rbm.solve(sub_matrix(om, x, x), oxs)  # Omega_xx^(-1) Omega[x, S]
    new = sub_matrix(om, s, s)
    for a in range(k):
        for b in range(k):
            new[a][b] -= sum(oxs[c][a] * sol[c][b] for c in range(nx))  # Omega3 - Omega, on S
    for a, ra in enumerate(x + mp):
        for b, rb in enumerate(x + mp):
            new[pos[ra]][pos[rb]] += o1[a][b]
    for a, ra in enumerate(mp):
        for b, rb in enumerate(mp):
            new[pos[ra]][pos[rb]] -= o2[a][b]
    new = [[(new[a][b] + new[b][a]) / 2.0 for b in range(k)] for a in range(k)]
    for a in range(nx):
        for b in m0:
            new[a][pos[b]] = 0.0  # zero by the formula, up to rounding
            new[pos[b]][a] = 0.0
    diff = [sum((new[a][b] - om[s[a]][s[b]]) * mu[s[b]] for b in range(k)) for a in range(k)]
    for a in range(k):
        xi[s[a]] += diff[a]  # @line L12
        for b in range(k):
            om[s[a]][s[b]] = new[a][b]


# ---------------------------------------------------------------- the filter


class Seif:
    """A SEIF over the pose and the landmarks seen so far."""

    def __init__(self, pose, pose_cov, max_active, alphas, q):
        self.mu = list(pose)
        self.omega = rbm.inv(pose_cov)
        self.xi = rbm.matvec(self.omega, self.mu)
        self.ids = []  # landmark identifiers in the order of the state
        self.active = []  # active slots, the most recently seen last
        self.max_active = max_active
        self.alphas = alphas
        self.q = q
        self.qinv = rbm.inv(q)
        self.next_cd = 0  # round robin pointer of the mean recovery

    # -------------------------------------------------------- indices

    @staticmethod
    def index(slot):
        return 3 + 2 * slot

    def block_indices(self, slots):
        out = []
        for s in slots:
            j = self.index(s)
            out.extend([j, j + 1])
        return out

    def local(self):
        """Return the indices of the pose and of the active landmarks."""
        return [0, 1, 2] + self.block_indices(self.active)

    # -------------------------------------------------------- motion: lines L1 to L5

    def motion(self, u, dt):
        mu = self.mu
        delta, g, vj = motion_offset(mu, u, dt)  # @line L1
        v, w = u
        a1, a2, a3, a4 = self.alphas
        m = [[a1 * v * v + a2 * w * w, 0.0], [0.0, a3 * v * v + a4 * w * w]]
        r = rbm.mul(rbm.mul(vj, m), rbm.transpose(vj))
        idx = self.local()
        k = len(idx)
        old = sub_matrix(self.omega, idx, idx)
        # Phi = (I + Psi)^T Omega (I + Psi) with I + Psi = G^(-1) on the pose: only the
        # pose rows and columns change, and only in the local block.
        ginv = rbm.inv(g)
        tmat = rbm.eye(k)
        for a in range(3):
            for b in range(3):
                tmat[a][b] = ginv[a][b]
        phi = rbm.mul(rbm.mul(rbm.transpose(tmat), old), tmat)  # @line L2
        phi_xx = [row[:3] for row in phi[:3]]
        inner = rbm.mul(r, rbm.inv(rbm.add(rbm.eye(3), rbm.mul(phi_xx, r))))  # R (I + Phi_xx R)^(-1)
        phi_x = [row[:3] for row in phi]  # Phi F_x^T, k by 3
        kappa = rbm.mul(rbm.mul(phi_x, inner), rbm.transpose(phi_x))  # @line L3
        new = rbm.sub(phi, kappa)
        new = [[(new[a][b] + new[b][a]) / 2.0 for b in range(k)] for a in range(k)]
        dmu = [sum((new[a][b] - old[a][b]) * mu[idx[b]] for b in range(k)) for a in range(k)]
        ndelta = [sum(new[a][b] * delta[b] for b in range(3)) for a in range(k)]
        for a in range(k):
            self.xi[idx[a]] += dmu[a] + ndelta[a]  # @line L4
            for b in range(k):
                self.omega[idx[a]][idx[b]] = new[a][b]
        for a in range(3):
            mu[a] += delta[a]  # @line L5
        # The heading is not wrapped here: xi encodes the mean, and wrapping
        # mu alone would make the two disagree by a multiple of 2 pi.

    # -------------------------------------------------------- readings: lines L6 to L9

    def add_landmark(self, lid, mean):
        n = len(self.mu)
        for row in self.omega:
            row.extend([0.0, 0.0])
        self.omega.append([0.0] * (n + 2))
        self.omega.append([0.0] * (n + 2))
        self.xi.extend([0.0, 0.0])
        self.mu.extend(mean)
        self.ids.append(lid)
        return len(self.ids) - 1

    def update(self, zs, lids):
        for z, lid in zip(zs, lids):  # @line L6
            if lid not in self.ids:
                self.add_landmark(lid, inverse_measure(self.mu, z))  # @line L7
            slot = self.ids.index(lid)
            j = self.index(slot)
            idx = [0, 1, 2, j, j + 1]
            mu = self.mu
            m = mu[j:j + 2]
            zhat = measure(mu, m)
            h = measure_jacobian(mu, m)  # @line L8
            nu = [z[0] - zhat[0], robest.wrap_angle(z[1] - zhat[1])]
            target = [nu[a] + sum(h[a][c] * mu[idx[c]] for c in range(5)) for a in range(2)]
            hq = rbm.mul(rbm.transpose(h), self.qinv)
            info = rbm.mul(hq, h)
            vec = rbm.matvec(hq, target)
            for a in range(5):
                self.xi[idx[a]] += vec[a]  # @line L9
                for b in range(5):
                    self.omega[idx[a]][idx[b]] += info[a][b]
            if slot in self.active:
                self.active.remove(slot)
            self.active.append(slot)

    # -------------------------------------------------------- sparsification: lines L10 to L12

    def sparsify(self):
        """Deactivate the landmarks seen least recently until at most max_active remain."""
        if len(self.active) <= self.max_active:  # @line L10
            return []
        cut = len(self.active) - self.max_active
        m0_slots, mp_slots = self.active[:cut], self.active[cut:]  # @line L11
        self.sparsify_slots(m0_slots, mp_slots)
        self.active = mp_slots
        return m0_slots

    def sparsify_slots(self, m0_slots, mp_slots):
        """Remove the links between the pose and the landmarks m0, keeping those to m+."""
        sparsify_info(self.omega, self.xi, self.mu, [0, 1, 2], self.block_indices(mp_slots), self.block_indices(m0_slots))

    # -------------------------------------------------------- mean recovery: line L13

    def recover_mean(self, extra=2, sweeps=1, joint=True):
        """Block coordinate descent on Omega mu = xi.

        With joint=True, the pose and the active landmarks form one block,
        solved together; otherwise each is its own block, as in plain
        coordinate descent. Then `extra` passive landmarks, in round robin
        order, are solved one at a time. Each block solve costs constant
        time for a bounded active set, apart from the row scans."""
        n_lm = len(self.ids)
        others = [s for s in range(n_lm) if s not in self.active]
        chosen = []
        for _ in range(min(extra, len(others))):
            self.next_cd %= n_lm
            while self.next_cd in self.active:
                self.next_cd = (self.next_cd + 1) % n_lm
            chosen.append(self.next_cd)
            self.next_cd += 1
        if joint:
            blocks = [self.local()]
        else:
            blocks = [[0, 1, 2]] + [[self.index(s), self.index(s) + 1] for s in self.active]
        blocks += [[self.index(s), self.index(s) + 1] for s in chosen]
        for _ in range(sweeps):
            for b in blocks:
                self.solve_block(b)  # @line L13

    def solve_block(self, b):
        """Set mu[b] to the minimizer of the quadratic with all other entries fixed."""
        om, mu = self.omega, self.mu
        rhs = []
        for r in b:
            row = om[r]
            acc = self.xi[r] - sum(row[c] * mu[c] for c in range(len(mu)))
            acc += sum(row[c] * mu[c] for c in b)
            rhs.append(acc)
        new = rbm.solve(sub_matrix(om, b, b), rhs)
        for a, r in enumerate(b):
            mu[r] = new[a]

    def recover_mean_exact(self):
        """Set mu = Omega^(-1) xi by a dense solve, O(n^3)."""
        self.mu = rbm.solve(self.omega, self.xi)

    # -------------------------------------------------------- one step

    def step(self, u, dt, zs, lids, extra=2):
        """One SEIF step: lines L1 to L14."""
        self.motion(u, dt)
        self.update(zs, lids)
        self.sparsify()
        self.recover_mean(extra)
        return self.mu  # @line L14
