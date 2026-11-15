# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extremum-seeking-control/. The authors are listed in prov/Y83ZRN.jsonl.

"""Classical perturbation based extremum seeking for a static map.

The performance y = J(theta) is measured, but J is unknown. The scheme
applies theta = thetah + a sin(omega t) (one dither per component, with
distinct frequencies), removes the slow part of y with a washout filter
y - eta, eta' = h (y - eta), multiplies by sin(omega t) (demodulation), and
integrates:

    thetah_i' = -k_i (y - eta) sin(omega_i t).

For k_i > 0 this seeks a minimum; for k_i < 0 a maximum. On average,
thetah_i' is about -k_i (a_i / 2) dJ/dtheta_i: gradient descent with the
gain k_i a_i / 2.

The simulation uses the classical RK4 method with a fixed step dt from
ctlsim. The time t1 must be an integer multiple of dt.
"""

import math

from ctlsim import rk4_step

__all__ = ["esc_simulate", "demodulated_average"]


def _steps(t1, dt):
    n = round(t1 / dt)
    assert abs(n * dt - t1) <= 1e-9 * max(1.0, abs(t1)), "dt must divide t1"
    return n


def esc_simulate(J, a, omega, k, h, theta0, t1, dt, every=1):
    """Simulate extremum seeking on the map J (a function of a list).

    a, omega, k and theta0 are lists with one entry per parameter. Returns
    (ts, thetahs, ys) sampled every `every` steps, where thetahs holds the
    estimates (without the dither) and ys the measured J.
    """
    n = len(theta0)
    s = [float(v) for v in theta0] + [J([float(v) for v in theta0])]  # @line L1

    def f(t, z, _u):
        th, eta = z[:n], z[n]
        d = [a[i] * math.sin(omega[i] * t) for i in range(n)]  # @line L3
        y = J([th[i] + d[i] for i in range(n)])  # @line L4
        deta = h * (y - eta)  # @line L5
        xi = [(y - eta) * math.sin(omega[i] * t) for i in range(n)]  # @line L6
        dth = [-k[i] * xi[i] for i in range(n)]  # @line L7
        return dth + [deta]

    N = _steps(t1, dt)
    ts, ths, ys = [0.0], [s[:n]], [s[n]]
    for i in range(N):  # @line L2
        s = rk4_step(f, i * dt, s, None, dt)  # @line L8
        if (i + 1) % every == 0:
            t = (i + 1) * dt
            ts.append(t)
            ths.append(s[:n])
            ys.append(J([s[j] + a[j] * math.sin(omega[j] * t) for j in range(n)]))
    return ts, ths, ys  # @line L9


def demodulated_average(J1, theta, a, omega, m=2000):
    """Average of (J1(theta + a sin wt) - J1(theta)) sin wt over one period.

    J1 is a scalar function. The average is computed by the rectangle rule
    with m points, which is exact for trigonometric polynomials of degree
    below m. For J1 smooth it equals (a / 2) J1'(theta) + O(a^3).
    """
    T = 2.0 * math.pi / omega
    s = 0.0
    for j in range(m):
        t = j * T / m
        s += (J1(theta + a * math.sin(omega * t)) - J1(theta)) * math.sin(omega * t)
    return s / m
