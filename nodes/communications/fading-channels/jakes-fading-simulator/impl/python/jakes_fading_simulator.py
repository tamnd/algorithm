# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jakes-fading-simulator/. The authors are listed in prov/43NN0S.jsonl.

"""The Jakes simulator: a deterministic sum of sinusoids for Rayleigh fading.

Clarke's model has the autocorrelation Omega J0(2 pi f_D tau). The Jakes
simulator approximates it with N = 4M + 2 plane waves at the equally spaced
angles 2 pi n / N. By symmetry only M + 1 oscillators are needed: the
frequencies w_0 = 2 pi f_D and w_n = 2 pi f_D cos(2 pi n / N), n = 1..M,
with the gains a_n = 2 cos(beta_n), b_n = 2 sin(beta_n), beta_n = pi n / M,
and a_0 = b_0 = 1 (sqrt(2) cos(pi / 4)). The form follows eqs. (6) and (7) of
Zheng and Xiao 2003. With the factor sqrt(2 Omega / N), the time-average
power is Omega.

The optional phases (one per oscillator) give the variant with random
phases of Pop and Beaulieu 2001, which is wide-sense stationary over the
ensemble of phases.
"""

import math


def jakes_coefficients(m: int) -> tuple[int, list[float], list[float], list[float]]:
    """N, the normalized frequencies cos(2 pi n / N) and the gains a_n, b_n for n = 0..M."""
    if m < 1:
        raise ValueError("need M >= 1")
    n = 4 * m + 2  # @line L1
    nu = [1.0] + [math.cos(2.0 * math.pi * k / n) for k in range(1, m + 1)]  # @line L2
    beta = [math.pi / 4.0] + [math.pi * k / m for k in range(1, m + 1)]  # @line L3
    a = [math.sqrt(2.0) * math.cos(beta[0])] + [2.0 * math.cos(x) for x in beta[1:]]  # @line L4
    b = [math.sqrt(2.0) * math.sin(beta[0])] + [2.0 * math.sin(x) for x in beta[1:]]
    return n, nu, a, b


def jakes(m: int, fd: float, times: list[float], omega: float = 1.0, phases: list[float] | None = None) -> list[complex]:
    """The fading gains h(t) of the Jakes simulator with M + 1 oscillators at the given times.

    fd is the maximum Doppler shift in Hz and times are in seconds. phases, if
    given, holds M + 1 oscillator phases (the variant of Pop and Beaulieu).
    """
    n, nu, a, b = jakes_coefficients(m)
    if phases is None:
        phases = [0.0] * (m + 1)
    if len(phases) != m + 1:
        raise ValueError("need M + 1 phases")
    w = [2.0 * math.pi * fd * v for v in nu]
    g = math.sqrt(2.0 * omega / n)
    out = []
    for t in times:
        osc = [math.cos(w[k] * t + phases[k]) for k in range(m + 1)]
        c = sum(a[k] * osc[k] for k in range(m + 1))  # @line L5
        s = sum(b[k] * osc[k] for k in range(m + 1))  # @line L6
        out.append(g * complex(c, s))  # @line L7
    return out


def time_autocorrelation(m: int, x: float) -> float:
    """The time-average autocorrelation <h(t + tau) conj(h(t))> / Omega at x = 2 pi f_D tau.

    It is (2 / N) (cos x + 2 sum_{n=1}^{M} cos(x cos(2 pi n / N))), the N-point
    trapezoid rule for J0(x).
    """
    n, nu, _, _ = jakes_coefficients(m)
    return (2.0 / n) * (math.cos(x) + 2.0 * sum(math.cos(x * v) for v in nu[1:]))


def quadrature_correlations(m: int, x: float) -> tuple[float, float, float]:
    """The time-average correlations <c c>, <s s> and <c s> of the two quadratures, each normalized by the power of one quadrature."""
    n, nu, a, b = jakes_coefficients(m)
    rcc = (2.0 / n) * sum(a[k] ** 2 * math.cos(x * nu[k]) for k in range(m + 1))
    rss = (2.0 / n) * sum(b[k] ** 2 * math.cos(x * nu[k]) for k in range(m + 1))
    rcs = (2.0 / n) * sum(a[k] * b[k] * math.cos(x * nu[k]) for k in range(m + 1))
    return rcc, rss, rcs


def bessel_j(order: int, x: float, points: int = 2048) -> float:
    """J_n(x) = (1 / 2 pi) integral over [0, 2 pi) of cos(n t - x sin t) dt, by the trapezoid rule.

    The integrand is periodic and smooth, so the rule converges very fast when
    points is well above order + |x|.
    """
    h = 2.0 * math.pi / points
    return sum(math.cos(order * k * h - x * math.sin(k * h)) for k in range(points)) / points


def j0(x: float) -> float:
    """The Bessel function J0(x)."""
    return bessel_j(0, x)


def aliasing_series(m: int, x: float, terms: int = 4) -> float:
    """J0(x) + 2 sum_{k>=1} (-1)^k J_{kN}(x), the exact value of the Jakes autocorrelation."""
    n = 4 * m + 2
    return j0(x) + 2.0 * sum((-1) ** k * bessel_j(k * n, x) for k in range(1, terms + 1))


def power_at_zero(m: int) -> float:
    """|h(0)|^2 / Omega for zero phases: (2 / N) ((sum a)^2 + (sum b)^2)."""
    n, _, a, b = jakes_coefficients(m)
    return (2.0 / n) * (sum(a) ** 2 + sum(b) ** 2)
