# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-mass-spring/. The authors are listed in prov/CQQNYH.jsonl.

"""Fast simulation of mass-spring systems (Liu, Bargteil, O'Brien and Kavan 2013), in 2D.

One backward Euler step of a spring system is the minimization of

    g(x) = 1/2 (x - y)^T M (x - y) + h^2 (E(x) - x^T f_ext),   y = x_n + h alpha v_n,

with E(x) = sum 1/2 k (|x_a - x_b| - r)^2. Each spring term equals
min over |d| = r of 1/2 k |(x_a - x_b) - d|^2, so g is the minimum over the
spring directions d of a function that is quadratic in x. Block coordinate
descent alternates a local step (best d for fixed x: d = r (x_a - x_b) / |x_a - x_b|)
and a global step (best x for fixed d: one solve with the constant matrix
M + h^2 L, factored once by Cholesky). In 2D the matrix acts on the x and the
y coordinates separately.

Springs are tuples (a, b, rest, k). Particles in the set `fixed` do not move.
"""

import math

GRAVITY = (0.0, -9.81)


# ---------------------------------------------------------------- banded Cholesky


def bandwidth(a):
    n = len(a)
    bw = 0
    for i in range(n):
        for j in range(i):
            if a[i][j] != 0.0:
                bw = max(bw, i - j)
    return bw


def cholesky_band(a, bw):
    """Lower triangular R with R R^T = a, for a symmetric positive definite a of half bandwidth bw."""
    n = len(a)
    r = [[0.0] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - bw)
        for j in range(lo, i + 1):
            s = a[i][j]
            ri, rj = r[i], r[j]
            for k in range(max(lo, j - bw), j):
                s -= ri[k] * rj[k]
            if i == j:
                if s <= 0.0:
                    raise ValueError("matrix is not positive definite")
                ri[i] = math.sqrt(s)
            else:
                ri[j] = s / rj[j]
    return r


def cholesky_solve(r, bw, b):
    """Solve R R^T x = b by a forward and a backward substitution."""
    n = len(r)
    z = [0.0] * n
    for i in range(n):
        s = b[i]
        ri = r[i]
        for k in range(max(0, i - bw), i):
            s -= ri[k] * z[k]
        z[i] = s / ri[i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = z[i]
        for k in range(i + 1, min(n, i + bw + 1)):
            s -= r[k][i] * x[k]
        x[i] = s / r[i][i]
    return x


# ---------------------------------------------------------------- the solver


class FastMassSpring:
    def __init__(self, n, springs, mass, h, fixed=(), alpha=1.0, gravity=GRAVITY):
        self.n = n
        self.springs = list(springs)
        self.mass = list(mass)
        self.h = h
        self.alpha = alpha  # the velocity in y is alpha v_n (ether drag, Liu et al. Section 4.1)
        self.fixed = set(fixed)
        self.free = [i for i in range(n) if i not in self.fixed]
        self.slot = {p: s for s, p in enumerate(self.free)}
        self.f_ext = [(m * gravity[0], m * gravity[1]) for m in self.mass]
        # A = M + h^2 L on the free particles; L is the stiffness-weighted graph Laplacian
        nf = len(self.free)
        a = [[0.0] * nf for _ in range(nf)]
        for p in self.free:
            a[self.slot[p]][self.slot[p]] = self.mass[p]
        self.coupling = []  # (free slot, fixed particle, h^2 k): the right side gets + h^2 k x_fixed
        h2 = h * h
        for sa, sb, rest, k in self.springs:
            for p, q in ((sa, sb), (sb, sa)):
                if p in self.fixed:
                    continue
                a[self.slot[p]][self.slot[p]] += h2 * k
                if q in self.fixed:
                    self.coupling.append((self.slot[p], q, h2 * k))
                else:
                    a[self.slot[p]][self.slot[q]] -= h2 * k
        self.bw = bandwidth(a)
        self.r = cholesky_band(a, self.bw)  # @line L1

    def local_step(self, x):
        """The best rest-length vector d of each spring for fixed x."""
        d = []
        for a, b, rest, k in self.springs:
            dx = x[a][0] - x[b][0]
            dy = x[a][1] - x[b][1]
            length = math.hypot(dx, dy)
            if length == 0.0:
                d.append((rest, 0.0))  # any direction is optimal for a spring of length zero
            else:
                d.append((rest * dx / length, rest * dy / length))  # @line L5
        return d

    def global_step(self, x, d, y):
        """The best free positions for fixed d: solve (M + h^2 L) x = M y + h^2 (J d + f_ext)."""
        h2 = self.h * self.h
        nf = len(self.free)
        rhs = [[self.mass[p] * y[p][c] + h2 * self.f_ext[p][c] for p in self.free] for c in range(2)]
        for (a, b, rest, k), di in zip(self.springs, d):
            for c in range(2):
                if a not in self.fixed:
                    rhs[c][self.slot[a]] += h2 * k * di[c]  # @line L6
                if b not in self.fixed:
                    rhs[c][self.slot[b]] -= h2 * k * di[c]
        for s, q, w in self.coupling:
            for c in range(2):
                rhs[c][s] += w * x[q][c]
        cols = [cholesky_solve(self.r, self.bw, rhs[c]) for c in range(2)]  # @line L7
        out = list(x)
        for s in range(nf):
            out[self.free[s]] = (cols[0][s], cols[1][s])
        return out

    def inertial_target(self, x, v):
        return [x[i] if i in self.fixed else
                (x[i][0] + self.h * self.alpha * v[i][0], x[i][1] + self.h * self.alpha * v[i][1])
                for i in range(self.n)]  # @line L2

    def step(self, x, v, iterations=10):
        """One step of backward Euler by `iterations` local and global steps. Return (x, v)."""
        y = self.inertial_target(x, v)
        z = list(y)  # @line L3
        for _ in range(iterations):  # @line L4
            d = self.local_step(z)
            z = self.global_step(z, d, y)
        new_v = [((z[i][0] - x[i][0]) / self.h, (z[i][1] - x[i][1]) / self.h) for i in range(self.n)]  # @line L8
        return z, new_v

    # ------------------------------------------------------------ energies for checks

    def spring_energy(self, x):
        e = 0.0
        for a, b, rest, k in self.springs:
            e += 0.5 * k * (math.dist(x[a], x[b]) - rest) ** 2
        return e

    def objective(self, x, y):
        """g(x) = 1/2 (x - y)^T M (x - y) + h^2 (E(x) - x^T f_ext) over the free particles."""
        h2 = self.h * self.h
        s = 0.0
        for p in self.free:
            s += 0.5 * self.mass[p] * ((x[p][0] - y[p][0]) ** 2 + (x[p][1] - y[p][1]) ** 2)
            s -= h2 * (x[p][0] * self.f_ext[p][0] + x[p][1] * self.f_ext[p][1])
        return s + h2 * self.spring_energy(x)

    def spring_forces(self, x):
        """Elastic forces -dE/dx on every particle."""
        f = [[0.0, 0.0] for _ in range(self.n)]
        for a, b, rest, k in self.springs:
            dx = x[a][0] - x[b][0]
            dy = x[a][1] - x[b][1]
            length = math.hypot(dx, dy)
            s = k * (length - rest) / length
            f[a][0] -= s * dx
            f[a][1] -= s * dy
            f[b][0] += s * dx
            f[b][1] += s * dy
        return f


def grid(nx, ny, spacing, k_struct, k_shear=0.0):
    """A grid with row j = 0 at the top (y = 0) and rows going down. Return (x, springs)."""
    def idx(i, j):
        return j * nx + i

    x = [(i * spacing, -j * spacing) for j in range(ny) for i in range(nx)]
    springs = []
    for j in range(ny):
        for i in range(nx):
            if i + 1 < nx:
                springs.append((idx(i, j), idx(i + 1, j), spacing, k_struct))
            if j + 1 < ny:
                springs.append((idx(i, j), idx(i, j + 1), spacing, k_struct))
            if k_shear > 0.0 and i + 1 < nx and j + 1 < ny:
                springs.append((idx(i, j), idx(i + 1, j + 1), spacing * math.sqrt(2.0), k_shear))
                springs.append((idx(i + 1, j), idx(i, j + 1), spacing * math.sqrt(2.0), k_shear))
    return x, springs
