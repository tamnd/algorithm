# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mit-rule/. The authors are listed in prov/B6VAKD.jsonl.

"""The MIT rule for model reference adaptation.

The model following error is e = y - y_m. The MIT rule moves each
controller parameter along the negative gradient of e^2 / 2:

    theta' = -gamma psi e,   psi an approximation of de/dtheta.

Two classic cases are here.

1. Adaptation of a feedforward gain. The plant is k G(s) with k > 0
   unknown, the model is k0 G(s), and u = theta u_c. Then
   de/dtheta = k G u_c = (k / k0) y_m, and the constant k / k0 > 0 goes
   into gamma, so theta' = -gamma y_m e.

2. A first order plant y' = -a y + b u with b > 0, the model
   y_m' = -a_m y_m + b_m u_c and u = theta_1 u_c - theta_2 y. The exact
   sensitivities need the unknown plant. With the plant pole replaced by
   the model pole, psi_1 = a_m / (p + a_m) u_c and
   psi_2 = -a_m / (p + a_m) y, so theta_1' = -gamma psi_1 e and
   theta_2' = +gamma (a_m / (p + a_m) y) e.

Every simulation uses the classical RK4 method with a fixed step dt from
ctlsim. The time t1 must be an integer multiple of dt.
"""

from ctlsim import rk4_step

__all__ = [
    "mit_feedforward_gain", "mit_first_order", "feedforward_theta_poly",
    "cubic_is_hurwitz",
]


def _steps(t1, dt):
    n = round(t1 / dt)
    assert abs(n * dt - t1) <= 1e-9 * max(1.0, abs(t1)), "dt must divide t1"
    return n


def mit_feedforward_gain(A, b, c, k, k0, gamma, uc, t1, dt, theta0=0.0, x0=None, xm0=None, every=1):
    """Simulate the MIT rule for the feedforward gain of the plant k G(s).

    G(s) = c (sI - A)^(-1) b is given in state space (A a list of rows,
    b and c flat lists). uc(t) is the command signal. Returns the lists
    (ts, thetas, errors), sampled every `every` steps.
    """
    n = len(A)
    x0 = [0.0] * n if x0 is None else list(x0)
    xm0 = [0.0] * n if xm0 is None else list(xm0)
    s = x0 + xm0 + [float(theta0)]  # @line L1

    def f(t, z, _u):
        x, xm, th = z[:n], z[n:2 * n], z[2 * n]
        r = uc(t)  # @line L3
        y = sum(ci * xi for ci, xi in zip(c, x))
        ym = sum(ci * xi for ci, xi in zip(c, xm))
        e = y - ym  # @line L4
        psi = ym  # @line L5
        u = th * r  # @line L6
        dx = [sum(a * xi for a, xi in zip(row, x)) + bi * k * u for row, bi in zip(A, b)]
        dxm = [sum(a * xi for a, xi in zip(row, xm)) + bi * k0 * r for row, bi in zip(A, b)]
        return dx + dxm + [-gamma * psi * e]  # @line L7

    N = _steps(t1, dt)
    ts, thetas, errors = [0.0], [s[2 * n]], [_err(s, c, n)]
    for i in range(N):  # @line L2
        s = rk4_step(f, i * dt, s, None, dt)  # @line L8
        if (i + 1) % every == 0:
            ts.append((i + 1) * dt)
            thetas.append(s[2 * n])
            errors.append(_err(s, c, n))
    return ts, thetas, errors  # @line L9


def _err(s, c, n):
    y = sum(ci * xi for ci, xi in zip(c, s[:n]))
    ym = sum(ci * xi for ci, xi in zip(c, s[n:2 * n]))
    return y - ym


def mit_first_order(a, b, am, bm, gamma, uc, t1, dt, theta0=(0.0, 0.0), every=1):
    """Simulate the MIT rule with two parameters on y' = -a y + b u.

    The controller is u = theta_1 u_c - theta_2 y. The ideal values are
    theta_1 = b_m / b and theta_2 = (a_m - a) / b. Returns
    (ts, theta1s, theta2s, errors), sampled every `every` steps.
    """
    s = [0.0, 0.0, 0.0, 0.0, float(theta0[0]), float(theta0[1])]  # @line L1
    # state: y, y_m, filtered u_c, filtered y, theta_1, theta_2

    def f(t, z, _u):
        y, ym, p1, p2, th1, th2 = z
        r = uc(t)  # @line L3
        e = y - ym  # @line L4
        psi1, psi2 = p1, -p2  # @line L5
        u = th1 * r - th2 * y  # @line L6
        dth1 = -gamma * psi1 * e  # @line L7
        dth2 = -gamma * psi2 * e
        return [-a * y + b * u, -am * ym + bm * r, -am * p1 + am * r, -am * p2 + am * y, dth1, dth2]

    N = _steps(t1, dt)
    ts, th1s, th2s, errs = [0.0], [s[4]], [s[5]], [0.0]
    for i in range(N):  # @line L2
        s = rk4_step(f, i * dt, s, None, dt)  # @line L8
        if (i + 1) % every == 0:
            ts.append((i + 1) * dt)
            th1s.append(s[4])
            th2s.append(s[5])
            errs.append(s[0] - s[1])
    return ts, th1s, th2s, errs  # @line L9


def feedforward_theta_poly(a1, a2, k, k0, gamma, u0):
    """Characteristic polynomial of theta for G(s) = 1 / (s^2 + a1 s + a2).

    With a constant command u_c = u0 and the model output at rest at
    y_m = k0 u0 / a2, the MIT rule gives the linear equation
    theta''' + a1 theta'' + a2 theta' + (gamma k k0 u0^2 / a2) theta = const.
    """
    return [1, a1, a2, gamma * k * k0 * u0 * u0 / a2]


def cubic_is_hurwitz(p):
    """Routh test for s^3 + p1 s^2 + p2 s + p3 (p[0] > 0)."""
    p0, p1, p2, p3 = p
    return p0 > 0 and p1 > 0 and p3 > 0 and p1 * p2 > p0 * p3
