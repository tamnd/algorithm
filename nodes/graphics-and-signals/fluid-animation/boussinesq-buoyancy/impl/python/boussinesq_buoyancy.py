# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boussinesq-buoyancy/. The authors are listed in prov/QV9FZM.jsonl.

"""The buoyancy force of smoke in the form of Fedkiw, Stam and Jensen (2001), on a 2D MAC grid.

    f = (-alpha s + beta (T - T_amb)) y_hat

s is the smoke density and T the temperature, both at the cell centers.
alpha >= 0 (m/s^2 per unit of s) and beta >= 0 (m/(s^2 K)) are constants.
The force is a vertical acceleration, so it lives on the v faces: each v face
gets the mean of s and T over the two cells below and above it. Faces that
touch a SOLID cell, which include the top and the bottom of the grid, get no
force; the pressure projection sets them.

The flow stays incompressible with one constant density rho. The density
difference of the hot or smoky gas appears only through this force.
"""

import macgrid


def buoyancy(s, T, alpha, beta, T_amb):
    """The upward acceleration -alpha s + beta (T - T_amb)."""
    return -alpha * s + beta * (T - T_amb)  # @line L1


def add_buoyancy(g, s, T, dt, alpha, beta, T_amb):
    """v += dt f on every v face that does not touch a SOLID cell."""
    if alpha < 0.0 or beta < 0.0 or dt <= 0.0:
        raise ValueError("need alpha >= 0, beta >= 0 and dt > 0")
    for i in range(g.nx):
        for j in range(1, g.ny):
            if macgrid.is_solid_v_face(g, i, j):
                continue
            sf = 0.5 * (s[i][j - 1] + s[i][j])  # @line L2
            Tf = 0.5 * (T[i][j - 1] + T[i][j])
            g.v[i][j] += dt * buoyancy(sf, Tf, alpha, beta, T_amb)  # @line L3


def step(g, s, T, dt, rho, alpha, beta, T_amb):
    """One smoke step: buoyancy, advection of the velocity, s and T, projection. Returns the new (s, T)."""
    add_buoyancy(g, s, T, dt, alpha, beta, T_amb)
    nu, nv = macgrid.advect_velocity(g, dt)  # @line L4
    s2 = macgrid.advect(g, s, dt)
    T2 = macgrid.advect(g, T, dt)
    g.u, g.v = nu, nv
    macgrid.project(g, dt, rho)  # @line L5
    return s2, T2


def ideal_gas_beta(gravity, T_amb):
    """beta = g / T_amb: the slope of g (rho_amb - rho) / rho_amb in T at T = T_amb for an ideal gas at fixed pressure."""
    if T_amb <= 0.0:
        raise ValueError("T_amb must be > 0 (kelvin)")
    return gravity / T_amb


def ideal_gas_force(gravity, T, T_amb):
    """g (rho_amb - rho) / rho_amb = g (T - T_amb) / T for an ideal gas at fixed pressure, without linearization."""
    return gravity * (T - T_amb) / T


def centroid_height(field, base, dx):
    """The height of the center of (field - base) over the cells, weighted by the excess."""
    num = den = 0.0
    for col in field:
        for j, t in enumerate(col):
            w = t - base
            num += w * (j + 0.5) * dx
            den += w
    return num / den
