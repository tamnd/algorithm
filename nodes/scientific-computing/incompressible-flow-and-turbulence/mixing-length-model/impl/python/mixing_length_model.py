# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mixing-length-model/. The authors are listed in prov/QA49H0.jsonl.

"""Prandtl mixing length model for the mean velocity near a wall, in wall units.

All quantities are in wall units: y+ = u_tau y / nu, U+ = U / u_tau, and the
total shear stress is tau+ = tau / (rho u_tau^2). The mean momentum balance is

    (1 + nu_t+) dU+/dy+ = tau+(y+),   nu_t+ = l+^2 |dU+/dy+|,

with the mixing length l+ = kappa y+ (times the van Driest damping factor
1 - exp(-y+ / A+) when A+ is given).
"""

import math
from typing import Callable, Optional

KAPPA = 0.41


def mixing_length(y_plus: float, kappa: float = KAPPA, a_plus: Optional[float] = None) -> float:
    """l+ = kappa y+, or kappa y+ (1 - exp(-y+ / A+)) with van Driest damping."""
    damping = 1.0 if a_plus is None else 1.0 - math.exp(-y_plus / a_plus)
    return kappa * y_plus * damping


def velocity_gradient(tau_plus: float, l_plus: float) -> float:
    """The root g of (1 + l+^2 |g|) g = tau+ that has the sign of tau+.

    Written as 2 tau / (1 + sqrt(1 + 4 l^2 |tau|)) to avoid cancellation.
    """
    return 2.0 * tau_plus / (1.0 + math.sqrt(1.0 + 4.0 * l_plus * l_plus * abs(tau_plus)))


def eddy_viscosity(y_plus: float, dudy_plus: float, kappa: float = KAPPA, a_plus: Optional[float] = None) -> float:
    """nu_t+ = l+^2 |dU+/dy+|."""
    l = mixing_length(y_plus, kappa, a_plus)
    return l * l * abs(dudy_plus)


def profile(
    y_max: float,
    n: int,
    kappa: float = KAPPA,
    a_plus: Optional[float] = None,
    stress: Callable[[float], float] = lambda y: 1.0,
) -> tuple[list[float], list[float]]:
    """Mean velocity U+(y+) on the uniform grid y_i = i y_max / n, i = 0..n.

    The gradient comes from the local momentum balance and is integrated
    from the wall (U+ = 0 at y+ = 0) with the trapezoidal rule.
    """
    if n < 1 or y_max <= 0:
        raise ValueError("need n >= 1 and y_max > 0")
    h = y_max / n  # @line L1
    u = [0.0]  # @line L1
    ys = [i * h for i in range(n + 1)]  # @line L2
    g = []
    for y in ys:  # @line L2
        l = mixing_length(y, kappa, a_plus)  # @line L3
        g.append(velocity_gradient(stress(y), l))  # @line L4
    for i in range(1, n + 1):  # @line L5
        u.append(u[-1] + 0.5 * h * (g[i - 1] + g[i]))  # @line L6
    return ys, u  # @line L7


def channel_stress(re_tau: float) -> Callable[[float], float]:
    """Total shear stress tau+ = 1 - y+ / Re_tau of fully developed channel flow."""
    return lambda y: 1.0 - y / re_tau


def exact_profile_no_damping(y_plus: float, kappa: float = KAPPA) -> float:
    """Closed form of U+ for l+ = kappa y+ and tau+ = 1.

    U+ = asinh(2 kappa y) / kappa - (sqrt(1 + 4 kappa^2 y^2) - 1) / (2 kappa^2 y).
    """
    if y_plus == 0:
        return 0.0
    s = math.sqrt(1.0 + 4.0 * kappa * kappa * y_plus * y_plus)
    return math.asinh(2.0 * kappa * y_plus) / kappa - (s - 1.0) / (2.0 * kappa * kappa * y_plus)


def log_intercept_no_damping(kappa: float = KAPPA) -> float:
    """The limit of U+ - ln(y+) / kappa for l+ = kappa y+: (ln(4 kappa) - 1) / kappa."""
    return (math.log(4.0 * kappa) - 1.0) / kappa


def log_intercept(y_max: float, n: int, kappa: float = KAPPA, a_plus: Optional[float] = None) -> float:
    """U+(y_max) - ln(y_max) / kappa from a constant stress profile."""
    _, u = profile(y_max, n, kappa, a_plus)
    return u[-1] - math.log(y_max) / kappa
