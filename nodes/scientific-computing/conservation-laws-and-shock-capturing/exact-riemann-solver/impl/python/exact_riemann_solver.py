# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exact-riemann-solver/. The authors are listed in prov/P7B1QH.jsonl.

"""Exact Riemann solver for the 1D Euler equations of an ideal gas (Toro 2009, Chapter 4).

States are primitive triples (rho, u, p). The solver finds the star pressure p* by
Newton iteration on the pressure function, starting from the two-rarefaction guess,
then samples the self-similar solution at xi = x / t.
"""

from math import sqrt


class VacuumError(ValueError):
    """The data generate a vacuum: the pressure function has no positive root."""


def sound_speed(rho: float, p: float, gamma: float) -> float:
    return sqrt(gamma * p / rho)


def wave_function(p: float, rho_k: float, p_k: float, c_k: float, gamma: float) -> tuple[float, float]:
    """The function f_K(p) of Toro, Section 4.2, and its derivative, for the side K."""
    if p > p_k:  # shock: the Rankine-Hugoniot relation
        a = 2.0 / ((gamma + 1.0) * rho_k)
        b = (gamma - 1.0) / (gamma + 1.0) * p_k
        q = sqrt(a / (p + b))
        return (p - p_k) * q, q * (1.0 - 0.5 * (p - p_k) / (p + b))
    z = (gamma - 1.0) / (2.0 * gamma)  # rarefaction: the isentropic relation
    r = p / p_k
    return 2.0 * c_k / (gamma - 1.0) * (r**z - 1.0), r ** (-(gamma + 1.0) / (2.0 * gamma)) / (rho_k * c_k)


def pressure_function(p: float, left: tuple, right: tuple, gamma: float) -> tuple[float, float]:
    """f(p) = f_L(p) + f_R(p) + u_R - u_L and f'(p). The root of f is p*."""
    rl, ul, pl = left
    rr, ur, pr = right
    fl, dl = wave_function(p, rl, pl, sound_speed(rl, pl, gamma), gamma)
    fr, dr = wave_function(p, rr, pr, sound_speed(rr, pr, gamma), gamma)
    return fl + fr + ur - ul, dl + dr


def star_state(left: tuple, right: tuple, gamma: float = 1.4, tol: float = 1e-12, maxit: int = 100) -> dict:
    """Return p*, u*, the two star densities, the wave speeds and the Newton iteration count."""
    rl, ul, pl = left
    rr, ur, pr = right
    cl, cr = sound_speed(rl, pl, gamma), sound_speed(rr, pr, gamma)
    if 2.0 / (gamma - 1.0) * (cl + cr) <= ur - ul:  # @line L1
        raise VacuumError("the data generate a vacuum")
    z = (gamma - 1.0) / (2.0 * gamma)
    p = ((cl + cr - 0.5 * (gamma - 1.0) * (ur - ul)) / (cl / pl**z + cr / pr**z)) ** (1.0 / z)  # @line L2
    its = 0
    for its in range(1, maxit + 1):  # @line L3
        f, df = pressure_function(p, left, right, gamma)  # @line L4
        p_new = p - f / df  # @line L5
        if p_new <= 0.0:  # @line L6
            p_new = tol * min(pl, pr)
        change = 2.0 * abs(p_new - p) / (p_new + p)  # @line L7
        p = p_new
        if change < tol:  # @line L8
            break
    else:
        raise RuntimeError("Newton iteration did not converge")
    fl, _ = wave_function(p, rl, pl, cl, gamma)
    fr, _ = wave_function(p, rr, pr, cr, gamma)
    u = 0.5 * (ul + ur) + 0.5 * (fr - fl)  # @line L9
    g1 = (gamma - 1.0) / (gamma + 1.0)
    out = {"p": p, "u": u, "iterations": its}
    for side, (rk, uk, pk, ck, sgn) in (("L", (rl, ul, pl, cl, -1.0)), ("R", (rr, ur, pr, cr, 1.0))):
        if p > pk:  # @line L10: a shock on this side
            out["rho_" + side] = rk * (p / pk + g1) / (g1 * p / pk + 1.0)
            s = uk + sgn * ck * sqrt((gamma + 1.0) / (2.0 * gamma) * p / pk + z)
            out["shock_" + side] = s
            out["head_" + side] = out["tail_" + side] = s
        else:  # @line L11: a rarefaction on this side
            out["rho_" + side] = rk * (p / pk) ** (1.0 / gamma)
            out["head_" + side] = uk + sgn * ck
            out["tail_" + side] = u + sgn * ck * (p / pk) ** z
    return out


def sample(xi: float, left: tuple, right: tuple, gamma: float = 1.4, star: dict | None = None) -> tuple[float, float, float]:
    """The primitive state (rho, u, p) of the exact solution at xi = x / t (Toro, Section 4.5)."""
    if star is None:
        star = star_state(left, right, gamma)
    p, u = star["p"], star["u"]
    if xi <= u:  # @line L12: left of the contact
        rk, uk, pk, sgn, side = left[0], left[1], left[2], 1.0, "L"
    else:
        rk, uk, pk, sgn, side = right[0], right[1], right[2], -1.0, "R"
    ck = sound_speed(rk, pk, gamma)
    head, tail = star["head_" + side], star["tail_" + side]
    # sgn = +1 on the left: the left wave lies at xi < u. Mirror the right side.
    if sgn * (xi - head) <= 0.0:  # @line L13: outside the wave, the data state
        return (rk, uk, pk)
    if sgn * (xi - tail) >= 0.0:  # @line L14: between the wave and the contact
        return (star["rho_" + side], u, p)
    # @line L15: inside a rarefaction fan
    g = gamma
    w = 2.0 / (g + 1.0) + sgn * (g - 1.0) / ((g + 1.0) * ck) * (uk - xi)
    rho = rk * w ** (2.0 / (g - 1.0))
    vel = 2.0 / (g + 1.0) * (sgn * ck + 0.5 * (g - 1.0) * uk + xi)
    return (rho, vel, pk * w ** (2.0 * g / (g - 1.0)))


def euler_flux(state: tuple, gamma: float = 1.4) -> tuple[float, float, float]:
    """Physical flux (rho u, rho u^2 + p, u (E + p)) of a primitive state."""
    rho, u, p = state
    e = p / (gamma - 1.0) + 0.5 * rho * u * u
    return (rho * u, rho * u * u + p, u * (e + p))


def godunov_flux(left: tuple, right: tuple, gamma: float = 1.4) -> tuple[float, float, float]:
    """The flux of the exact solution on the line x = 0, as used by Godunov's method."""
    return euler_flux(sample(0.0, left, right, gamma), gamma)
