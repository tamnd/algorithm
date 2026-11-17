# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/projected-gauss-seidel/. The authors are listed in prov/MA63NH.jsonl.

"""Projected Gauss-Seidel for contact impulses, in matrix form and as sequential impulses.

The problem: given A (n x n, A_ii > 0), b and bounds lo_i <= hi_i, find lam with

    lo <= lam <= hi,  w = A lam + b,
    w_i >= 0 where lam_i = lo_i,  w_i <= 0 where lam_i = hi_i,  w_i = 0 in between.

For a contact, lam_i is an impulse, w_i the relative velocity along the
constraint row after the impulse, A = J M^-1 J^T and b = J v0 + bias.

A bound entry is either a pair (lo, hi) or a triple ("friction", k, mu), which
means the box [-mu lam_k, mu lam_k] around the current normal impulse lam_k.

The matrix-free version (sequential impulses) keeps body velocities instead of
A. In exact arithmetic it produces the same lam as the matrix version.
"""

INF = float("inf")


def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x


def row_bounds(entry, lam):
    if len(entry) == 3 and entry[0] == "friction":
        _, k, mu = entry
        return -mu * lam[k], mu * lam[k]
    return entry


def pgs(A, b, bounds, sweeps, lam0=None, trace=None):
    """Run a fixed number of projected Gauss-Seidel sweeps and return lam."""
    n = len(b)
    lam = list(lam0) if lam0 is not None else [0 * b[i] for i in range(n)]  # @line L1
    for _ in range(sweeps):  # @line L2
        for i in range(n):  # @line L3
            r = b[i] + sum(A[i][j] * lam[j] for j in range(n))  # @line L4
            lo, hi = row_bounds(bounds[i], lam)  # @line L5
            lam[i] = clamp(lam[i] - r / A[i][i], lo, hi)  # @line L6
        if trace is not None:
            trace.append(list(lam))
    return lam  # @line L7


def residual(A, b, lam):
    return [b[i] + sum(A[i][j] * lam[j] for j in range(len(b))) for i in range(len(b))]


def violation(A, b, bounds, lam):
    """The largest violation of the box complementarity conditions (0 for an exact solution)."""
    w = residual(A, b, lam)
    worst = 0
    for i, wi in enumerate(w):
        lo, hi = row_bounds(bounds[i], lam)
        x = lam[i]
        worst = max(worst, lo - x, x - hi)
        # the projected residual: zero exactly when the row update would not move lam_i
        worst = max(worst, abs(clamp(x - wi, lo, hi) - x))
    return worst


def objective(A, b, lam):
    n = len(b)
    return sum(lam[i] * A[i][j] * lam[j] for i in range(n) for j in range(n)) / 2 + sum(b[i] * lam[i] for i in range(n))


# ---------------------------------------------------------------- sequential impulses


class Body:
    """A 2D rigid body: mass m, moment of inertia I, velocity v, angular velocity w."""

    def __init__(self, m, I, v, w):
        self.inv_m = 0 if m is None else 1 / m
        self.inv_I = 0 if I is None else 1 / I
        self.v = list(v)
        self.w = w


def ground():
    return Body(None, None, (0, 0), 0)


def cross2(r, d):
    return r[0] * d[1] - r[1] * d[0]


class Row:
    """One constraint row: the impulse lam * d acts on body a at r_a, and -lam * d on body b at r_b."""

    def __init__(self, a, b, r_a, r_b, d):
        self.a, self.b, self.r_a, self.r_b, self.d = a, b, r_a, r_b, d
        self.ca, self.cb = cross2(r_a, d), cross2(r_b, d)

    def jacobian(self, nbodies):
        """The row of J, three entries (v_x, v_y, w) per body."""
        J = [0] * (3 * nbodies)
        J[3 * self.a:3 * self.a + 3] = [self.d[0], self.d[1], self.ca]
        J[3 * self.b:3 * self.b + 3] = [-self.d[0], -self.d[1], -self.cb]
        return J


def row_velocity(row, bodies):
    A, B = bodies[row.a], bodies[row.b]
    return (row.d[0] * (A.v[0] - B.v[0]) + row.d[1] * (A.v[1] - B.v[1])
            + A.w * row.ca - B.w * row.cb)


def row_mass(row, bodies):
    """K_ii = J_i M^-1 J_i^T."""
    A, B = bodies[row.a], bodies[row.b]
    dd = row.d[0] * row.d[0] + row.d[1] * row.d[1]
    return (A.inv_m + B.inv_m) * dd + A.inv_I * row.ca * row.ca + B.inv_I * row.cb * row.cb


def apply_row(row, bodies, dlam):
    A, B = bodies[row.a], bodies[row.b]
    for k in range(2):
        A.v[k] += A.inv_m * dlam * row.d[k]
        B.v[k] -= B.inv_m * dlam * row.d[k]
    A.w += A.inv_I * dlam * row.ca
    B.w -= B.inv_I * dlam * row.cb


def sequential_impulses(bodies, rows, bias, bounds, sweeps, lam0=None):
    """Matrix-free PGS: update body velocities in place and return the accumulated impulses."""
    n = len(rows)
    lam = list(lam0) if lam0 is not None else [0] * n  # @line L1
    for i in range(n):  # warm start: apply the initial impulses once
        if lam[i]:
            apply_row(rows[i], bodies, lam[i])
    K = [row_mass(r, bodies) for r in rows]
    for _ in range(sweeps):  # @line L2
        for i in range(n):  # @line L3
            r = row_velocity(rows[i], bodies) + bias[i]  # @line L4
            lo, hi = row_bounds(bounds[i], lam)  # @line L5
            new = clamp(lam[i] - r / K[i], lo, hi)  # @line L6
            apply_row(rows[i], bodies, new - lam[i])  # clamp the total, apply the change
            lam[i] = new  # @line L6
    return lam  # @line L7


def assemble(bodies, rows, bias):
    """A = J M^-1 J^T and b = J v + bias for the current body velocities."""
    nb = len(bodies)
    J = [r.jacobian(nb) for r in rows]
    inv = []
    for body in bodies:
        inv += [body.inv_m, body.inv_m, body.inv_I]
    v = []
    for body in bodies:
        v += [body.v[0], body.v[1], body.w]
    A = [[sum(Ji[k] * inv[k] * Jj[k] for k in range(3 * nb)) for Jj in J] for Ji in J]
    b = [sum(Ji[k] * v[k] for k in range(3 * nb)) + bias[i] for i, Ji in enumerate(J)]
    return A, b
