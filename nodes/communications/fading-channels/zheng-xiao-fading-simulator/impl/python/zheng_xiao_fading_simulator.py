# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zheng-xiao-fading-simulator/. The authors are listed in prov/97VH88.jsonl.

"""The Zheng-Xiao statistical sum-of-sinusoids simulator for Rayleigh fading.

Eq. (14) of Zheng and Xiao 2003: with M sinusoids,
    X_c(t) = sum_n cos(psi_n) cos(w_d t cos(alpha_n) + phi_n),
    X_s(t) = sum_n sin(psi_n) cos(w_d t cos(alpha_n) + phi_n),
    alpha_n = (2 pi n - pi + theta) / (4 M), n = 1..M,
where psi_n, phi_n and theta are independent and uniform on [-pi, pi).
The fading gain is h = sqrt(2 Omega / M) (X_c + j X_s), so E|h|^2 = Omega.

The 2003 paper used one phase phi for all n. Xiao, Zheng and Beaulieu 2006
showed that this form is not Gaussian for short times and that its squared
envelope is not stationary; they use an independent phi_n for each n. The
default here is the corrected form; common_phase=True gives the 2003 form.
Both have the exact second-order statistics of Clarke's model.
"""

import math
import random


def draw_parameters(m: int, rng: random.Random, common_phase: bool = False) -> tuple[list[float], list[float], list[float]]:
    """One random draw of the angles alpha_n, the gain phases psi_n and the Doppler phases phi_n."""
    if m < 1:
        raise ValueError("need M >= 1")
    theta = rng.uniform(-math.pi, math.pi)  # @line L1
    psi = [rng.uniform(-math.pi, math.pi) for _ in range(m)]  # @line L2
    if common_phase:
        phi = [rng.uniform(-math.pi, math.pi)] * m
    else:
        phi = [rng.uniform(-math.pi, math.pi) for _ in range(m)]  # @line L3
    alpha = [(2.0 * math.pi * n - math.pi + theta) / (4.0 * m) for n in range(1, m + 1)]  # @line L4
    return alpha, psi, phi


def gains(fd: float, times: list[float], alpha: list[float], psi: list[float], phi: list[float], omega: float = 1.0) -> list[complex]:
    """h(t) at the given times for one fixed draw of the parameters."""
    m = len(alpha)
    wd = 2.0 * math.pi * fd
    g = math.sqrt(2.0 * omega / m)
    cp = [math.cos(p) for p in psi]
    sp = [math.sin(p) for p in psi]
    nu = [math.cos(a) for a in alpha]
    out = []
    for t in times:
        osc = [math.cos(wd * t * nu[n] + phi[n]) for n in range(m)]
        xc = sum(cp[n] * osc[n] for n in range(m))  # @line L5
        xs = sum(sp[n] * osc[n] for n in range(m))
        out.append(g * complex(xc, xs))  # @line L6
    return out


def zheng_xiao(m: int, fd: float, times: list[float], rng: random.Random, omega: float = 1.0, common_phase: bool = False) -> list[complex]:
    """One realization of the Zheng-Xiao simulator with M sinusoids at the given times."""
    alpha, psi, phi = draw_parameters(m, rng, common_phase)
    return gains(fd, times, alpha, psi, phi, omega)


def theta_average(m: int, x: float, points: int = 2000) -> float:
    """E over theta of (1 / M) sum_n cos(x cos(alpha_n)), by Simpson's rule over theta in [-pi, pi].

    This is the normalized autocorrelation E[h(t + tau) conj(h(t))] / Omega at
    x = 2 pi f_D tau. The theorem of Zheng and Xiao says that it equals J0(x).
    """
    if points % 2:
        points += 1
    h = 2.0 * math.pi / points

    def f(theta):
        return sum(math.cos(x * math.cos((2.0 * math.pi * n - math.pi + theta) / (4.0 * m))) for n in range(1, m + 1)) / m

    s = f(-math.pi) + f(math.pi)
    for k in range(1, points):
        s += (4 if k % 2 else 2) * f(-math.pi + k * h)
    return s * h / 3.0 / (2.0 * math.pi)


def fourth_moment(m: int, common_phase: bool) -> float:
    """E|h(0)|^4 / Omega^2: 2 - 1 / (2M) with a phase per sinusoid, 3 - 3 / (2M) with one common phase."""
    return 3.0 - 1.5 / m if common_phase else 2.0 - 0.5 / m


def j0(x: float, points: int = 2048) -> float:
    """J0(x) = (1 / 2 pi) integral over [0, 2 pi) of cos(x sin t) dt, by the trapezoid rule."""
    h = 2.0 * math.pi / points
    return sum(math.cos(x * math.sin(k * h)) for k in range(points)) / points
