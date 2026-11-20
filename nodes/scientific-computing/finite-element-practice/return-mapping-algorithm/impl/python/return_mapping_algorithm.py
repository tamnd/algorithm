# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/return-mapping-algorithm/. The authors are listed in prov/PD9SMC.jsonl.

"""Return mapping for rate-independent plasticity with linear hardening.

return_map_1d: one-dimensional plasticity with isotropic and kinematic hardening.
radial_return: three-dimensional J2 (von Mises) plasticity, closed form radial
return and the consistent tangent of Simo and Taylor (1985).

Both solve the backward Euler equations of the flow rule exactly for one strain
increment. Tensors are 3 by 3 lists; a fourth order tangent is a 9 by 9 list
indexed by (3 i + j, 3 k + l). With Fraction data the 1D map is exact.
"""

import math


def return_map_1d(eps, state, E, sy, K=0, H=0):
    """Return (sigma, new_state, tangent) for the total strain eps.

    state = (eps_p, alpha, q): plastic strain, equivalent plastic strain and
    back stress at the end of the last converged step. K is the isotropic and
    H the kinematic hardening modulus.
    """
    eps_p, alpha, q = state
    sig_tr = E * (eps - eps_p)  # @line L1
    xi = sig_tr - q
    f_tr = abs(xi) - (sy + K * alpha)  # @line L2
    if f_tr <= 0:  # @line L3
        return sig_tr, state, E  # @line L4
    dgam = f_tr / (E + K + H)  # @line L5
    sgn = 1 if xi > 0 else -1
    sig = sig_tr - E * dgam * sgn  # @line L6
    new = (eps_p + dgam * sgn, alpha + dgam, q + H * dgam * sgn)  # @line L7
    tangent = E * (K + H) / (E + K + H)  # @line L8
    return sig, new, tangent


def _trace(a):
    return a[0][0] + a[1][1] + a[2][2]


def dev(a):
    """Return the deviatoric part of a 3 by 3 tensor."""
    t = _trace(a) / 3
    return [[a[i][j] - (t if i == j else 0) for j in range(3)] for i in range(3)]


def tnorm(a):
    """Return the Frobenius norm sqrt(a : a)."""
    return math.sqrt(sum(a[i][j] ** 2 for i in range(3) for j in range(3)))


def zero_state():
    """Return the virgin state (eps_p, alpha, beta) for radial_return."""
    z = [[0.0] * 3 for _ in range(3)]
    return (z, 0.0, [row[:] for row in z])


def radial_return(eps, state, kappa, mu, sy, K=0.0, H=0.0):
    """Return (sigma, new_state, tangent, dgamma) for J2 plasticity at total strain eps.

    state = (eps_p, alpha, beta): plastic strain tensor, equivalent plastic
    strain and back stress. The yield function is
    f = |dev(sigma) - beta| - sqrt(2/3) (sy + K alpha),
    with linear isotropic (K) and kinematic (H) hardening.
    """
    eps_p, alpha, beta = state
    e = dev(eps)
    s_tr = [[2 * mu * (e[i][j] - eps_p[i][j]) for j in range(3)] for i in range(3)]  # @line L1
    xi = [[s_tr[i][j] - beta[i][j] for j in range(3)] for i in range(3)]
    nxi = tnorm(xi)
    r = math.sqrt(2 / 3)
    f_tr = nxi - r * (sy + K * alpha)  # @line L2
    p = kappa * _trace(eps)
    if f_tr <= 0:  # @line L3
        sig = [[s_tr[i][j] + (p if i == j else 0) for j in range(3)] for i in range(3)]
        return sig, state, elastic_tangent(kappa, mu), 0.0  # @line L4
    dgam = f_tr / (2 * mu + 2 / 3 * (K + H))  # @line L5
    n = [[xi[i][j] / nxi for j in range(3)] for i in range(3)]
    sig = [[s_tr[i][j] - 2 * mu * dgam * n[i][j] + (p if i == j else 0) for j in range(3)] for i in range(3)]  # @line L6
    new = (
        [[eps_p[i][j] + dgam * n[i][j] for j in range(3)] for i in range(3)],
        alpha + r * dgam,
        [[beta[i][j] + 2 / 3 * H * dgam * n[i][j] for j in range(3)] for i in range(3)],
    )  # @line L7
    theta = 1 - 2 * mu * dgam / nxi
    theta_bar = 1 / (1 + (K + H) / (3 * mu)) - (1 - theta)
    tangent = _tangent(kappa, mu, theta, theta_bar, n)  # @line L8
    return sig, new, tangent, dgam


def _delta(i, j):
    return 1.0 if i == j else 0.0


def _tangent(kappa, mu, theta, theta_bar, n):
    c = [[0.0] * 9 for _ in range(9)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    sym = 0.5 * (_delta(i, k) * _delta(j, l) + _delta(i, l) * _delta(j, k))
                    idev = sym - _delta(i, j) * _delta(k, l) / 3
                    c[3 * i + j][3 * k + l] = (
                        kappa * _delta(i, j) * _delta(k, l) + 2 * mu * theta * idev - 2 * mu * theta_bar * n[i][j] * n[k][l]
                    )
    return c


def elastic_tangent(kappa, mu):
    """Return the isotropic elastic tangent as a 9 by 9 list."""
    z = [[0.0] * 3 for _ in range(3)]
    return _tangent(kappa, mu, 1.0, 0.0, z)


def yield_value(sig, state, sy, K=0.0):
    """Return f(sigma, state) = |dev(sigma) - beta| - sqrt(2/3)(sy + K alpha)."""
    _, alpha, beta = state
    s = dev(sig)
    return tnorm([[s[i][j] - beta[i][j] for j in range(3)] for i in range(3)]) - math.sqrt(2 / 3) * (sy + K * alpha)


def bar_newton(areas, lengths, u_end, E, sy, K=0, H=0, consistent=True, tol=1e-12, maxit=50):
    """Solve a bar of elements in series, fixed at the left end, with a prescribed end displacement.

    Each element has one strain. The unknowns are the interior node displacements.
    Return (stresses, number of Newton iterations). With consistent=False the
    elastic modulus is used as the tangent, as in the initial stiffness method.
    """
    m = len(areas)
    states = [(0, 0, 0)] * m
    u = [u_end * sum(lengths[: i + 1]) / sum(lengths) for i in range(m)]  # node 1 .. m, last fixed
    for it in range(maxit):
        res = [0.0] * (m - 1)
        kt = [[0.0] * (m - 1) for _ in range(m - 1)]
        sig = []
        for e in range(m):
            left = u[e - 1] if e > 0 else 0.0
            strain = (u[e] - left) / lengths[e]
            s, _, tan = return_map_1d(strain, states[e], E, sy, K, H)
            sig.append(s)
            k = (tan if consistent else E) * areas[e] / lengths[e]
            # internal force of element e on its left node (e - 1) and right node (e)
            for a, sign in ((e - 1, -1), (e, 1)):
                if 0 <= a < m - 1:
                    res[a] += sign * s * areas[e]
                    for b, sign2 in ((e - 1, -1), (e, 1)):
                        if 0 <= b < m - 1:
                            kt[a][b] += sign * sign2 * k
        if max(abs(x) for x in res) <= tol * max(abs(x) * a for x, a in zip(sig, areas)):
            return sig, it
        du = _solve_dense(kt, res)
        for a in range(m - 1):
            u[a] -= du[a]
    raise RuntimeError("Newton did not converge")


def _solve_dense(a, b):
    n = len(b)
    a = [row[:] + [b[i]] for i, row in enumerate(a)]
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(a[i][k]))
        a[k], a[p] = a[p], a[k]
        for i in range(k + 1, n):
            f = a[i][k] / a[k][k]
            for j in range(k, n + 1):
                a[i][j] -= f * a[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (a[i][n] - sum(a[i][j] * x[j] for j in range(i + 1, n))) / a[i][i]
    return x
