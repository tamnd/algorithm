# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mass-spring-system/. The authors are listed in prov/4B6KHP.jsonl.

"""A 2D mass-spring system with damped springs, advanced by symplectic Euler.

A spring (i, j, L, k) pulls its two particles with the force
f_i = (k (l - L) + c (v_j - v_i) . u) u and f_j = -f_i, where d = x_j - x_i,
l = |d| and u = d / l. The damping acts along the spring only, so every force
is central. A particle with inverse mass 0 is fixed. Positions are (x, y) with
y up, in metres; gravity is (0, -9.81) m/s^2.
"""

import math

GRAVITY = (0.0, -9.81)


def grid(nx, ny, spacing, k_struct, k_shear=0.0, k_bend=0.0):
    """A regular nx by ny grid of particles and its springs.

    Structural springs join (i, j) to (i + 1, j) and (i, j + 1); shear springs
    join the two diagonals of each cell; bending springs join (i, j) to
    (i + 2, j) and (i, j + 2), as in Provot 1995, Section 2.1. Return
    (positions, springs) with springs as tuples (a, b, rest, k).
    """
    def idx(i, j):
        return j * nx + i

    x = [(i * spacing, j * spacing) for j in range(ny) for i in range(nx)]
    springs = []

    def add(a, b, k):
        if k > 0.0:
            springs.append((a, b, math.dist(x[a], x[b]), k))

    for j in range(ny):
        for i in range(nx):
            if i + 1 < nx:
                add(idx(i, j), idx(i + 1, j), k_struct)
            if j + 1 < ny:
                add(idx(i, j), idx(i, j + 1), k_struct)
            if i + 1 < nx and j + 1 < ny:
                add(idx(i, j), idx(i + 1, j + 1), k_shear)
                add(idx(i + 1, j), idx(i, j + 1), k_shear)
            if i + 2 < nx:
                add(idx(i, j), idx(i + 2, j), k_bend)
            if j + 2 < ny:
                add(idx(i, j), idx(i, j + 2), k_bend)
    return x, springs


def forces(x, v, mass, springs, damping=0.0, gravity=(0.0, 0.0)):
    """Total force on each particle: gravity, spring and spring damping."""
    f = [[m * gravity[0], m * gravity[1]] for m in mass]  # @line L1
    for a, b, rest, k in springs:
        dx = x[b][0] - x[a][0]
        dy = x[b][1] - x[a][1]
        length = math.hypot(dx, dy)  # @line L2
        ux, uy = dx / length, dy / length
        rel = (v[b][0] - v[a][0]) * ux + (v[b][1] - v[a][1]) * uy
        s = k * (length - rest) + damping * rel  # @line L3
        f[a][0] += s * ux  # @line L4
        f[a][1] += s * uy
        f[b][0] -= s * ux
        f[b][1] -= s * uy
    return f


def step(x, v, inv_mass, mass, springs, dt, damping=0.0, gravity=(0.0, 0.0)):
    """One symplectic Euler step (velocity first). Return new lists (x, v)."""
    f = forces(x, v, mass, springs, damping, gravity)
    nv = []
    nx_ = []
    for i in range(len(x)):
        w = inv_mass[i]
        vi = (v[i][0] + dt * w * f[i][0], v[i][1] + dt * w * f[i][1])  # @line L5
        nv.append(vi)
        nx_.append((x[i][0] + dt * vi[0], x[i][1] + dt * vi[1]))  # @line L6
    return nx_, nv


def spring_energy(x, springs):
    """Elastic energy sum of k (l - L)^2 / 2."""
    e = 0.0
    for a, b, rest, k in springs:
        e += 0.5 * k * (math.dist(x[a], x[b]) - rest) ** 2
    return e


def kinetic_energy(v, mass):
    return sum(0.5 * m * (vi[0] ** 2 + vi[1] ** 2) for vi, m in zip(v, mass))


def momentum(x, v, mass):
    """Linear momentum (px, py) and angular momentum about the origin."""
    px = sum(m * vi[0] for vi, m in zip(v, mass))
    py = sum(m * vi[1] for vi, m in zip(v, mass))
    lz = sum(m * (xi[0] * vi[1] - xi[1] * vi[0]) for xi, vi, m in zip(x, v, mass))
    return px, py, lz


def step_limit(k, m):
    """Largest stable symplectic Euler step for one mass m on a spring k to a fixed point: 2 / omega."""
    return 2.0 / math.sqrt(k / m)


def uniaxial_energy_per_cell(k, k_d, spacing, strain, angle):
    """Small-strain energy of one cell of the square lattice under uniaxial strain.

    Leading term of the energy of an infinite lattice with structural springs k
    and diagonal springs k_d, stretched by strain along the direction angle:
    (spacing^2 strain^2 / 2) (k + k_d + c^2 s^2 (4 k_d - 2 k)).
    """
    c, s = math.cos(angle), math.sin(angle)
    return 0.5 * spacing ** 2 * strain ** 2 * (k + k_d + c * c * s * s * (4.0 * k_d - 2.0 * k))
