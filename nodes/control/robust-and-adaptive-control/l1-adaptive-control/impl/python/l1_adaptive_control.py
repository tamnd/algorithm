# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/l1-adaptive-control/. The authors are listed in prov/S1SMGT.jsonl.

"""L1 adaptive control of a scalar plant with an unknown state feedback gain.

Plant:      x' = a_m x + b (u + theta x),   a_m < 0, b > 0 known, theta unknown
            with |theta| <= theta_b.
Predictor:  xh' = a_m xh + b (u + thetah x)
Adaptation: thetah' = Gamma Proj(thetah, -xt p b x),  xt = xh - x,
            p = -1 / (2 a_m) solves 2 a_m p = -1.
Control:    u = C(s) (k_g r - thetah x),  C(s) = omega_c / (s + omega_c),
            k_g = -a_m / b, as the state u' = omega_c (k_g r - thetah x - u).

Proj is the smooth projection operator with
f(theta) = (theta^2 - theta_b^2) / (eps theta_b^2): it leaves y unchanged
inside the ball |theta| <= theta_b, and on the outer band it removes the
outward part of y in proportion to f, so |thetah| <= theta_b sqrt(1 + eps)
for all time.

The simulation uses the classical RK4 method with a fixed step dt from
ctlsim. The time t1 must be an integer multiple of dt.
"""

import math

from ctlsim import rk4_step

__all__ = ["proj", "l1_simulate", "l1_norm_g", "prediction_bound"]


def _steps(t1, dt):
    n = round(t1 / dt)
    assert abs(n * dt - t1) <= 1e-9 * max(1.0, abs(t1)), "dt must divide t1"
    return n


def proj(theta, y, theta_b, eps):
    """Smooth projection operator for a scalar parameter."""
    f = (theta * theta - theta_b * theta_b) / (eps * theta_b * theta_b)
    df = 2.0 * theta / (eps * theta_b * theta_b)
    if f > 0 and y * df > 0:
        return y - f * y  # the scalar form of y - f grad f grad f^T y / |grad f|^2
    return y


def l1_simulate(theta, theta_b, eps, gamma, omega_c, r, t1, dt, a_m=-1.0, b=1.0,
                thetah0=0.0, x0=0.0, every=1):
    """Simulate the L1 adaptive controller. r(t) is the reference.

    Returns (ts, xs, xhs, thetahs, us) sampled every `every` steps.
    """
    p = -1.0 / (2.0 * a_m)
    k_g = -a_m / b
    s = [float(x0), float(x0), float(thetah0), 0.0]  # @line L1

    def f(t, z, _u):
        x, xh, th, u = z
        rt = r(t)  # @line L3
        xt = xh - x  # @line L4
        dx = a_m * x + b * (u + theta * x)
        dxh = a_m * xh + b * (u + th * x)  # @line L5
        dth = gamma * proj(th, -xt * p * b * x, theta_b, eps)  # @line L6
        du = omega_c * (k_g * rt - th * x - u)  # @line L7
        return [dx, dxh, dth, du]

    N = _steps(t1, dt)
    out = ([0.0], [s[0]], [s[1]], [s[2]], [s[3]])
    for i in range(N):  # @line L2
        s = rk4_step(f, i * dt, s, None, dt)  # @line L8
        if (i + 1) % every == 0:
            out[0].append((i + 1) * dt)
            for j in range(4):
                out[j + 1].append(s[j])
    return out  # @line L9


def l1_norm_g(omega_c):
    """L1 norm of the impulse response of G(s) = s / ((s + 1)(s + omega_c)).

    G = H (1 - C) with H = 1 / (s + 1) and C = omega_c / (s + omega_c). The
    impulse response (omega_c e^(-omega_c t) - e^(-t)) / (omega_c - 1)
    changes sign once, at t0 = ln(omega_c) / (omega_c - 1), and integrates
    to G(0) = 0, so the norm is twice its integral over [0, t0].
    """
    if omega_c == 1.0:
        return 2.0 / math.e
    t0 = math.log(omega_c) / (omega_c - 1.0)
    return 2.0 * (math.exp(-t0) - math.exp(-omega_c * t0)) / (omega_c - 1.0)


def prediction_bound(thetah0, theta, gamma, a_m=-1.0):
    """Bound on |xh - x| from V = p xt^2 + (thetah - theta)^2 / Gamma, xt(0) = 0."""
    p = -1.0 / (2.0 * a_m)
    return math.sqrt((thetah0 - theta) ** 2 / (gamma * p))
