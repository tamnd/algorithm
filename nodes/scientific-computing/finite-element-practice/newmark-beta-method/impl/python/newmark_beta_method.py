# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newmark-beta-method/. The authors are listed in prov/DKETH0.jsonl.

"""Newmark-beta time stepping for M a + C v + K d = F(t) and its nonlinear form.

Matrices are lists of rows and vectors are lists, as in scimat. The step is dt.
With Fraction data and Fraction parameters the linear steps are exact.
"""

import math

import scimat


def newmark(M, C, K, F, d0, v0, dt, nsteps, beta=0.25, gamma=0.5):
    """Integrate M a + C v + K d = F(t) with the Newmark-beta method.

    F is a function of t that returns the load vector. Return the lists of
    displacements, velocities and accelerations at t = 0, dt, ..., nsteps dt.
    """
    n = len(d0)
    d, v = list(d0), list(v0)
    rhs0 = scimat.sub(scimat.sub(F(0 * dt), scimat.matvec(C, v)), scimat.matvec(K, d))
    a = scimat.solve(M, rhs0)  # @line L1
    lhs = [[M[i][j] + gamma * dt * C[i][j] + beta * dt * dt * K[i][j] for j in range(n)] for i in range(n)]
    ds, vs, accs = [list(d)], [list(v)], [list(a)]
    for k in range(nsteps):  # @line L2
        t1 = (k + 1) * dt
        dp = [d[i] + dt * v[i] + dt * dt / 2 * (1 - 2 * beta) * a[i] for i in range(n)]  # @line L3
        vp = [v[i] + (1 - gamma) * dt * a[i] for i in range(n)]  # @line L4
        r = scimat.sub(scimat.sub(F(t1), scimat.matvec(C, vp)), scimat.matvec(K, dp))
        a = scimat.solve(lhs, r)  # @line L5
        d = [dp[i] + beta * dt * dt * a[i] for i in range(n)]  # @line L6
        v = [vp[i] + gamma * dt * a[i] for i in range(n)]  # @line L7
        ds.append(d)
        vs.append(v)
        accs.append(a)
    return ds, vs, accs  # @line L8


def newmark_nonlinear(M, C, fint, tangent, F, d0, v0, dt, nsteps, beta=0.25, gamma=0.5, tol=1e-12, maxit=30):
    """Integrate M a + C v + fint(d) = F(t) with Newmark-beta and Newton iterations.

    tangent(d) returns the stiffness matrix d fint / d d. Each step solves the
    residual equation for a_(n+1) by Newton's method with the effective
    tangent M + gamma dt C + beta dt^2 K_T. Return (ds, vs, accs, iterations).
    """
    n = len(d0)
    d, v = list(d0), list(v0)
    a = scimat.solve(M, scimat.sub(scimat.sub(F(0 * dt), scimat.matvec(C, v)), fint(d)))
    ds, vs, accs, its = [list(d)], [list(v)], [list(a)], []
    for k in range(nsteps):
        t1 = (k + 1) * dt
        dp = [d[i] + dt * v[i] + dt * dt / 2 * (1 - 2 * beta) * a[i] for i in range(n)]
        vp = [v[i] + (1 - gamma) * dt * a[i] for i in range(n)]
        anew = list(a)
        for it in range(maxit):
            dn = [dp[i] + beta * dt * dt * anew[i] for i in range(n)]
            vn = [vp[i] + gamma * dt * anew[i] for i in range(n)]
            res = scimat.sub(scimat.add(scimat.add(scimat.matvec(M, anew), scimat.matvec(C, vn)), fint(dn)), F(t1))
            if scimat.norm2(res) <= tol * (1 + scimat.norm2(F(t1))):
                break
            kt = tangent(dn)
            jac = [[M[i][j] + gamma * dt * C[i][j] + beta * dt * dt * kt[i][j] for j in range(n)] for i in range(n)]
            da = scimat.solve(jac, res)
            anew = [anew[i] - da[i] for i in range(n)]
        else:
            raise RuntimeError("Newton iteration did not converge")
        a = anew
        d = [dp[i] + beta * dt * dt * a[i] for i in range(n)]
        v = [vp[i] + gamma * dt * a[i] for i in range(n)]
        ds.append(d)
        vs.append(v)
        accs.append(a)
        its.append(it)
    return ds, vs, accs, its


def amplification_matrix(omega_dt, beta, gamma, xi=0.0):
    """Return the 2 by 2 matrix A with (d, dt v)_(n+1) = A (d, dt v)_n.

    It is for the free single degree of freedom oscillator a + 2 xi omega v +
    omega^2 d = 0 with dt = 1 and omega = omega_dt, so it depends only on
    omega dt, xi and the parameters.
    """
    m, c, k = [[1.0]], [[2 * xi * omega_dt]], [[omega_dt * omega_dt]]
    cols = []
    for d0, v0 in ((1.0, 0.0), (0.0, 1.0)):
        ds, vs, _ = newmark(m, c, k, lambda t: [0.0], [d0], [v0], 1.0, 1, beta, gamma)
        cols.append((ds[1][0], vs[1][0]))
    return [[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]]


def spectral_radius_2x2(a):
    """Return the largest modulus of the eigenvalues of a real 2 by 2 matrix."""
    tr = a[0][0] + a[1][1]
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    disc = tr * tr / 4 - det
    if disc >= 0:
        s = math.sqrt(disc)
        return max(abs(tr / 2 + s), abs(tr / 2 - s))
    return math.sqrt(det)


def critical_omega_dt(beta, gamma):
    """Return the stability limit of omega dt for an undamped linear oscillator.

    Valid for gamma >= 1/2. Return math.inf when 2 beta >= gamma (unconditional).
    """
    if 2 * beta >= gamma:
        return math.inf
    return 1 / math.sqrt(gamma / 2 - beta)
