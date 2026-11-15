# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/high-gain-observer/. The authors are listed in prov/CY2X2T.jsonl.

"""High-gain observer for a system in observable (chain of integrators) form

    x_i' = x_(i+1),   i = 1, ..., n - 1,
    x_n' = phi(x, u),   y = x_1,

with a nominal model phi0 of phi (phi0 = 0 is allowed). The observer is

    xh_i' = xh_(i+1) + (alpha_i / eps^i) (y - xh_1),   i = 1, ..., n - 1,
    xh_n' = phi0(xh, u) + (alpha_n / eps^n) (y - xh_1),

where s^n + alpha_1 s^(n-1) + ... + alpha_n is Hurwitz and eps > 0 is small.
In the scaled errors eta_i = (x_i - xh_i) / eps^(n-i) the error equation is

    eps eta' = A0 eta + eps B delta,   delta = phi(x, u) - phi0(xh, u),

with A0 the companion matrix of the polynomial above, so the error decays
on the time scale eps and ends of size O(eps^(n+1-i)) in x_i.

observer_rhs returns xh' for use inside an ODE solver. With exact data and
an exact phi0 the result is exact (int and Fraction stay exact).
"""

from fractions import Fraction

__all__ = ["observer_rhs", "saturate", "peak_bound_n2"]


def _pow_div(a, eps, i):
    d = eps ** i
    if isinstance(a, int) and isinstance(d, int):
        return Fraction(a, d)
    return a / d


def observer_rhs(xh, y, u, eps, alpha, phi0):
    """Return the derivative of the estimate xh.

    alpha: the n coefficients alpha_1..alpha_n of a Hurwitz polynomial.
    phi0(xh, u): the nominal model of the last equation.
    """
    n = len(xh)
    if len(alpha) != n:
        raise ValueError("alpha must have len(xh) entries")
    if eps <= 0:
        raise ValueError("eps must be positive")
    e = y - xh[0]  # @line L1
    dx = []
    for i in range(1, n):  # @line L2
        dx.append(xh[i] + _pow_div(alpha[i - 1], eps, i) * e)  # @line L3
    dx.append(phi0(xh, u) + _pow_div(alpha[n - 1], eps, n) * e)  # @line L4
    return dx  # @line L5


def saturate(v, m):
    """Clip v to [-m, m]; the usual guard against peaking."""
    return max(-m, min(m, v))


def peak_bound_n2(e1_0, eps):
    """Peak of |e2| for n = 2, alpha = (2, 1), delta = 0, e2(0) = 0.

    Then e2(t) = -(t / eps) exp(-t / eps) e1(0) / eps, with the peak
    |e1(0)| / (e eps) at t = eps.
    """
    import math
    return abs(e1_0) / (math.e * eps)
