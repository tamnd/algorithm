# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-epsilon-model/. The authors are listed in prov/FJGR38.jsonl.

"""Standard k-epsilon model: eddy viscosity, decay of homogeneous turbulence
and the log-layer relations, with the constants of Launder and Sharma (1974).

Units are SI: k in m^2/s^2, eps in m^2/s^3, nu_t in m^2/s, t in s.
"""

import math

C_MU = 0.09
C_1 = 1.44
C_2 = 1.92
SIGMA_K = 1.0
SIGMA_EPS = 1.3


def eddy_viscosity(k: float, eps: float, c_mu: float = C_MU) -> float:
    """nu_t = C_mu k^2 / eps."""
    if eps <= 0:
        raise ValueError("eps must be positive")
    return c_mu * k * k / eps


def decay_rhs(k: float, eps: float, c2: float = C_2) -> tuple[float, float]:
    """Right side of the model for homogeneous decaying turbulence (no production, no diffusion)."""
    return -eps, -c2 * eps * eps / k  # @line L2


def rk4_decay(k0: float, eps0: float, t_end: float, m: int, c2: float = C_2) -> tuple[float, float]:
    """Integrate dk/dt = -eps, deps/dt = -C_2 eps^2 / k from 0 to t_end with m steps of classical RK4."""
    if m < 1 or k0 <= 0 or eps0 <= 0:
        raise ValueError("need m >= 1 and positive k0, eps0")
    h = t_end / m  # @line L1
    k, e = k0, eps0  # @line L1
    for _ in range(m):  # @line L3
        a = decay_rhs(k, e, c2)  # @line L4
        b = decay_rhs(k + 0.5 * h * a[0], e + 0.5 * h * a[1], c2)  # @line L4
        c = decay_rhs(k + 0.5 * h * b[0], e + 0.5 * h * b[1], c2)  # @line L4
        d = decay_rhs(k + h * c[0], e + h * c[1], c2)  # @line L4
        k += h * (a[0] + 2 * b[0] + 2 * c[0] + d[0]) / 6  # @line L5
        e += h * (a[1] + 2 * b[1] + 2 * c[1] + d[1]) / 6  # @line L5
    return k, e  # @line L6


def decay_exponent(c2: float = C_2) -> float:
    """The power n in k ~ t^(-n) for decaying turbulence: n = 1 / (C_2 - 1)."""
    return 1.0 / (c2 - 1.0)


def exact_decay(k0: float, eps0: float, t: float, c2: float = C_2) -> tuple[float, float]:
    """Exact solution k = k0 (1 + t/t0)^(-n), eps = eps0 (1 + t/t0)^(-n-1), with t0 = n k0 / eps0."""
    n = decay_exponent(c2)
    t0 = n * k0 / eps0
    s = 1.0 + t / t0
    return k0 * s ** (-n), eps0 * s ** (-n - 1.0)


def log_layer_kappa(c_mu: float = C_MU, c1: float = C_1, c2: float = C_2, sigma_eps: float = SIGMA_EPS) -> float:
    """The von Karman constant implied by the model: kappa^2 = sigma_eps sqrt(C_mu) (C_2 - C_1)."""
    return math.sqrt(sigma_eps * math.sqrt(c_mu) * (c2 - c1))


def log_layer_state(u_tau: float, y: float, kappa: float = 0.41, c_mu: float = C_MU) -> tuple[float, float, float]:
    """k, eps and nu_t in an equilibrium log layer: k = u_tau^2 / sqrt(C_mu), eps = u_tau^3 / (kappa y)."""
    k = u_tau * u_tau / math.sqrt(c_mu)
    eps = u_tau**3 / (kappa * y)
    return k, eps, eddy_viscosity(k, eps, c_mu)
