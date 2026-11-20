# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-alpha-method/. The authors are listed in prov/1NTWAK.jsonl.

"""Generalized-alpha time stepping (Chung and Hulbert 1993) for M a + C v + K d = F(t).

Matrices are lists of rows and vectors are lists, as in scimat. The step is dt.
The equation of motion is enforced at shifted points inside the step:
    M a_(n+1-am) + C v_(n+1-af) + K d_(n+1-af) = F(t_(n+1-af)),
with x_(n+1-alpha) = (1 - alpha) x_(n+1) + alpha x_n, and the Newmark updates
for d and v. With Fraction data and parameters the steps are exact.
"""

import cmath
import math

import scimat


def chung_hulbert(rho_inf):
    """Return (alpha_m, alpha_f, beta, gamma) for the high frequency limit rho_inf in [0, 1]."""
    if not 0 <= rho_inf <= 1:
        raise ValueError("rho_inf must be in [0, 1]")
    am = (2 * rho_inf - 1) / (rho_inf + 1)
    af = rho_inf / (rho_inf + 1)
    gamma = (1 - 2 * am + 2 * af) / 2
    beta = (1 - am + af) ** 2 / 4
    return am, af, beta, gamma


def hht(alpha):
    """Return the parameters of the HHT-alpha method; alpha in [0, 1/3] (am = 0, af = alpha)."""
    if not 0 <= alpha <= 1 / 3:
        raise ValueError("alpha must be in [0, 1/3]")
    return 0 * alpha, alpha, (1 + alpha) ** 2 / 4, (1 + 2 * alpha) / 2


def wbz(rho_inf):
    """Return the parameters of the WBZ-alpha method (af = 0) for rho_inf in [0, 1]."""
    am = (rho_inf - 1) / (rho_inf + 1)
    return am, 0 * am, (1 - am) ** 2 / 4, (1 - 2 * am) / 2


def step(M, C, K, F, t, d, v, a, dt, am, af, beta, gamma):
    """Advance (d, v, a) at time t by one generalized-alpha step and return the new triple."""
    n = len(d)
    lhs = [[(1 - am) * M[i][j] + (1 - af) * (gamma * dt * C[i][j] + beta * dt * dt * K[i][j]) for j in range(n)] for i in range(n)]
    dp = [d[i] + dt * v[i] + dt * dt / 2 * (1 - 2 * beta) * a[i] for i in range(n)]  # @line L3
    vp = [v[i] + (1 - gamma) * dt * a[i] for i in range(n)]  # @line L4
    dm = [(1 - af) * dp[i] + af * d[i] for i in range(n)]
    vm = [(1 - af) * vp[i] + af * v[i] for i in range(n)]
    rhs = scimat.sub(F(t + (1 - af) * dt), scimat.add(scimat.scale(am, scimat.matvec(M, a)), scimat.add(scimat.matvec(C, vm), scimat.matvec(K, dm))))  # @line L5
    a1 = scimat.solve(lhs, rhs)  # @line L6
    d1 = [dp[i] + beta * dt * dt * a1[i] for i in range(n)]  # @line L7
    v1 = [vp[i] + gamma * dt * a1[i] for i in range(n)]  # @line L8
    return d1, v1, a1


def generalized_alpha(M, C, K, F, d0, v0, dt, nsteps, rho_inf=None, params=None):
    """Integrate M a + C v + K d = F(t) from (d0, v0) with nsteps steps of size dt.

    Give either rho_inf (Chung-Hulbert parameters) or params = (am, af, beta, gamma).
    Return the lists of displacements, velocities and accelerations.
    """
    if params is None:
        params = chung_hulbert(rho_inf)
    am, af, beta, gamma = params
    d, v = list(d0), list(v0)
    a = scimat.solve(M, scimat.sub(scimat.sub(F(0 * dt), scimat.matvec(C, v)), scimat.matvec(K, d)))  # @line L1
    ds, vs, accs = [d], [v], [a]
    for k in range(nsteps):  # @line L2
        d, v, a = step(M, C, K, F, k * dt, d, v, a, dt, am, af, beta, gamma)
        ds.append(d)
        vs.append(v)
        accs.append(a)
    return ds, vs, accs  # @line L9


def amplification_matrix(omega_dt, params, xi=0.0):
    """Return the 3 by 3 matrix A with (d, dt v, dt^2 a)_(n+1) = A (d, dt v, dt^2 a)_n.

    It is for a + 2 xi omega v + omega^2 d = 0 with dt = 1 and omega = omega_dt.
    """
    am, af, beta, gamma = params
    m, c, k = [[1.0]], [[2 * xi * omega_dt]], [[omega_dt * omega_dt]]
    cols = []
    for x in ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)):
        d1, v1, a1 = step(m, c, k, lambda t: [0.0], 0.0, [x[0]], [x[1]], [x[2]], 1.0, am, af, beta, gamma)
        cols.append((d1[0], v1[0], a1[0]))
    return [[cols[j][i] for j in range(3)] for i in range(3)]


def eigenvalues_3x3(a):
    """Return the three complex eigenvalues of a real 3 by 3 matrix (Durand-Kerner on its cubic)."""
    tr = a[0][0] + a[1][1] + a[2][2]
    minors = (a[0][0] * a[1][1] - a[0][1] * a[1][0]) + (a[0][0] * a[2][2] - a[0][2] * a[2][0]) + (a[1][1] * a[2][2] - a[1][2] * a[2][1])
    det = scimat.det(a)
    # characteristic polynomial: z^3 - tr z^2 + minors z - det
    def p(z):
        return ((z - tr) * z + minors) * z - det

    scale = 1 + abs(tr) + abs(minors) + abs(det)
    roots = [scale * (0.4 + 0.9j) ** k for k in range(3)]
    for _ in range(500):
        new = []
        for i, z in enumerate(roots):
            den = 1
            for j, w in enumerate(roots):
                if j != i:
                    den *= z - w
            new.append(z - p(z) / den if den != 0 else z + 1e-12)
        done = max(abs(x - y) for x, y in zip(new, roots)) < 1e-15 * scale
        roots = new
        if done:
            break
    return roots


def spectral_radius(omega_dt, params, xi=0.0):
    """Return the spectral radius of the step matrix at omega dt."""
    return max(abs(z) for z in eigenvalues_3x3(amplification_matrix(omega_dt, params, xi)))


def principal_root(omega_dt, params):
    """Return the eigenvalue near exp(i omega dt) (positive imaginary part) of the undamped step.

    Return None if the principal roots are real (no oscillation per step).
    """
    roots = eigenvalues_3x3(amplification_matrix(omega_dt, params))
    best = max(roots, key=lambda z: z.imag)
    if best.imag <= 1e-14:
        return None
    return best


def damping_ratio_and_period_error(omega_dt, params):
    """Return (algorithmic damping ratio, relative period error) at omega dt.

    The principal root is exp(omega_dt (-xi_bar + i) * wbar / omega) in polar form;
    xi_bar = -ln|z| / arg z and the period error is omega_dt / arg z - 1.
    """
    z = principal_root(omega_dt, params)
    ang = cmath.phase(z)
    return -math.log(abs(z)) / ang, omega_dt / ang - 1
