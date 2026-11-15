# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/model-reference-adaptive-control/. The authors are listed in prov/V7E58W.jsonl.

"""Lyapunov based model reference adaptive control with full state feedback.

Plant:  x' = A x + b u          (A, b unknown, single input)
Model:  x_m' = A_m x_m + b_m r  (A_m Hurwitz, chosen by the designer)
Control: u = k^T x + l r

Matching condition: there are k*, l* with A + b k*^T = A_m and b l* = b_m.
The sign of l* must be known. With e = x - x_m, P the solution of
A_m^T P + P A_m = -Q (Q symmetric positive definite) and gamma > 0, the
adaptive laws

    k' = -gamma sgn(l*) x (b_m^T P e)
    l' = -gamma sgn(l*) r (b_m^T P e)

make V = e^T P e + (|k - k*|^2 + (l - l*)^2) / (gamma |l*|)
satisfy V' = -e^T Q e <= 0.

The simulation uses the classical RK4 method with a fixed step dt from
ctlsim. The time t1 must be an integer multiple of dt.
"""

from ctlmat import eye, kron, solve, transpose, unvec, vec
from ctlsim import rk4_step

__all__ = ["lyapunov_p", "mrac", "lyapunov_v"]


def _steps(t1, dt):
    n = round(t1 / dt)
    assert abs(n * dt - t1) <= 1e-9 * max(1.0, abs(t1)), "dt must divide t1"
    return n


def lyapunov_p(Am, Q):
    """Solve A_m^T P + P A_m = -Q by the Kronecker form (exact for Fraction input)."""
    n = len(Am)
    At = transpose(Am)
    # vec(At P) = (I kron At) vec(P), vec(P Am) = (Am^T kron I) vec(P)
    I = eye(n)
    K = [[x + y for x, y in zip(r1, r2)] for r1, r2 in zip(kron(I, At), kron(At, I))]
    p = solve(K, [-v for v in vec(Q)])
    return unvec(p, n, n)


def mrac(A, b, Am, bm, Q, gamma, sign_l, r, t1, dt, k0=None, l0=0.0, x0=None, xm0=None, every=1):
    """Simulate Lyapunov MRAC. r(t) is the reference signal.

    Returns (ts, xs, xms, ks, ls) sampled every `every` steps.
    """
    n = len(A)
    P = [[float(v) for v in row] for row in lyapunov_p(Am, Q)]  # @line L1
    Pbm = [sum(P[j][i] * bm[j] for j in range(n)) for i in range(n)]  # (b_m^T P) as a row
    k = [0.0] * n if k0 is None else [float(v) for v in k0]
    x = [0.0] * n if x0 is None else [float(v) for v in x0]
    xm = [0.0] * n if xm0 is None else [float(v) for v in xm0]
    s = x + xm + k + [float(l0)]  # @line L2

    def f(t, z, _u):
        x, xm, k, l = z[:n], z[n:2 * n], z[2 * n:3 * n], z[3 * n]
        rt = r(t)  # @line L4
        e = [xi - mi for xi, mi in zip(x, xm)]  # @line L5
        u = sum(ki * xi for ki, xi in zip(k, x)) + l * rt  # @line L6
        dx = [sum(a * xi for a, xi in zip(row, x)) + bi * u for row, bi in zip(A, b)]  # @line L7
        dxm = [sum(a * xi for a, xi in zip(row, xm)) + bi * rt for row, bi in zip(Am, bm)]
        s_e = sum(p * ei for p, ei in zip(Pbm, e))
        dk = [-gamma * sign_l * xi * s_e for xi in x]  # @line L8
        dl = -gamma * sign_l * rt * s_e
        return dx + dxm + dk + [dl]

    N = _steps(t1, dt)
    ts, xs, xms, ks, ls = [0.0], [s[:n]], [s[n:2 * n]], [s[2 * n:3 * n]], [s[3 * n]]
    for i in range(N):  # @line L3
        s = rk4_step(f, i * dt, s, None, dt)  # @line L9
        if (i + 1) % every == 0:
            ts.append((i + 1) * dt)
            xs.append(s[:n])
            xms.append(s[n:2 * n])
            ks.append(s[2 * n:3 * n])
            ls.append(s[3 * n])
    return ts, xs, xms, ks, ls  # @line L10


def lyapunov_v(P, gamma, l_star, k_star, x, xm, k, l):
    """V = e^T P e + (|k - k*|^2 + (l - l*)^2) / (gamma |l*|)."""
    n = len(x)
    e = [x[i] - xm[i] for i in range(n)]
    epe = sum(e[i] * P[i][j] * e[j] for i in range(n) for j in range(n))
    dk = sum((k[i] - k_star[i]) ** 2 for i in range(n))
    return epe + (dk + (l - l_star) ** 2) / (gamma * abs(l_star))
