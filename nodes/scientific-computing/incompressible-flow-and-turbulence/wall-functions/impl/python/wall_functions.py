# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wall-functions/. The authors are listed in prov/7MSEKR.jsonl.

"""Log-law wall functions: the friction velocity from the velocity at the
first grid point, the wall values of k, epsilon and omega, the Launder-Spalding
form and Spalding's single formula for the whole inner layer.

Units are SI. Wall units: y+ = u_tau y / nu, u+ = U / u_tau.
"""

import math

KAPPA = 0.41
B = 5.2
C_MU = 0.09


def log_law(y_plus: float, kappa: float = KAPPA, b: float = B) -> float:
    """u+ = ln(y+) / kappa + B."""
    return math.log(y_plus) / kappa + b


def crossover(kappa: float = KAPPA, b: float = B) -> float:
    """The y+ above 1 where the linear law u+ = y+ meets the log law."""
    y = 11.0
    for _ in range(50):
        g = y - math.log(y) / kappa - b
        dy = g / (1.0 - 1.0 / (kappa * y))
        y -= dy
        if abs(dy) < 1e-14 * y:
            break
    return y


def friction_velocity(u_p: float, y_p: float, nu: float, kappa: float = KAPPA, b: float = B, tol: float = 1e-12) -> float:
    """u_tau such that U_P = u_tau u+(y_P u_tau / nu), with the linear law below the crossover."""
    if u_p <= 0 or y_p <= 0 or nu <= 0:
        raise ValueError("need positive U_P, y_P and nu")
    y_c = crossover(kappa, b)  # @line L1
    u = math.sqrt(nu * u_p / y_p)  # @line L2
    if y_p * u / nu <= y_c:  # @line L3
        return u  # @line L3
    for _ in range(100):  # @line L4
        s = math.log(y_p * u / nu) / kappa + b  # @line L5
        f = u * s - u_p  # @line L5
        u -= f / (s + 1.0 / kappa)  # @line L6
        if abs(f) <= tol * u_p:  # @line L7
            break
    return u  # @line L8


def wall_shear_stress(u_p: float, y_p: float, nu: float, rho: float, kappa: float = KAPPA, b: float = B) -> float:
    """tau_w = rho u_tau^2 in Pa."""
    u = friction_velocity(u_p, y_p, nu, kappa, b)
    return rho * u * u  # @line L8


def wall_values(u_tau: float, y_p: float, kappa: float = KAPPA, c_mu: float = C_MU) -> tuple[float, float, float]:
    """Equilibrium k, epsilon and omega at the first point: u_tau^2/sqrt(C_mu), u_tau^3/(kappa y), u_tau/(sqrt(C_mu) kappa y)."""
    k = u_tau * u_tau / math.sqrt(c_mu)
    eps = u_tau**3 / (kappa * y_p)
    omega = u_tau / (math.sqrt(c_mu) * kappa * y_p)
    return k, eps, omega


def launder_spalding_stress(u_p: float, k_p: float, y_p: float, nu: float, kappa: float = KAPPA, b: float = B, c_mu: float = C_MU) -> float:
    """tau_w / rho = kappa u* U_P / ln(E y*), with u* = C_mu^(1/4) sqrt(k_P), y* = u* y_P / nu, E = exp(kappa B)."""
    u_star = c_mu**0.25 * math.sqrt(k_p)
    y_star = u_star * y_p / nu
    e = math.exp(kappa * b)
    return kappa * u_star * u_p / math.log(e * y_star)


def spalding_y_plus(u_plus: float, kappa: float = KAPPA, b: float = B) -> float:
    """Spalding's law: y+ = u+ + exp(-kappa B) (exp(kappa u+) - 1 - kappa u+ - (kappa u+)^2/2 - (kappa u+)^3/6)."""
    x = kappa * u_plus
    return u_plus + math.exp(-kappa * b) * (math.exp(x) - 1.0 - x - x * x / 2.0 - x**3 / 6.0)


def spalding_u_plus(y_plus: float, kappa: float = KAPPA, b: float = B) -> float:
    """Invert Spalding's law by bisection; y+ is increasing in u+."""
    lo, hi = 0.0, max(1.0, y_plus)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if spalding_y_plus(mid, kappa, b) < y_plus:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)
