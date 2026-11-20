# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-simulation-monte-carlo/. The authors are listed in prov/8HF9Q3.jsonl.
"""Direct simulation Monte Carlo (DSMC) for a dilute hard-sphere gas.

The gas lives in a periodic box of length L in x and cross-section area
A, cut into M equal cells along x. Each simulated particle stands for
F_N real molecules and carries a position x and a velocity (vx, vy, vz).
Units have m = k = 1. A time step of size dt has two parts:

1. Move: every particle streams freely, x <- x + vx dt (periodic).
2. Collide: in each cell, Bird's no-time-counter (NTC) scheme draws
       n_cand = 1/2 N_c (N_c - 1) F_N (sigma g)_max dt / V_c
   candidate pairs (the fractional part is carried to the next step),
   picks each pair at random, and accepts it with probability
   sigma g / (sigma g)_max. A hard-sphere collision keeps the centre of
   mass velocity and turns the relative velocity g to a uniform random
   direction, so momentum and energy are conserved exactly.

Bird writes the candidate count with N_c times the time average of N_c
in place of N_c (N_c - 1); for a cell with a fixed number of particles
the form used here gives the exact pair collision rate.
"""

import math


class Gas:
    """The state of a DSMC run."""

    def __init__(self, x, v, length, ncells, f_n, sigma, area=1.0):
        self.x = list(x)
        self.v = [list(u) for u in v]
        self.length = length
        self.ncells = ncells
        self.f_n = f_n
        self.sigma = sigma  # hard-sphere total cross section pi d^2
        self.cell_volume = area * length / ncells
        vmax = max(math.sqrt(u[0] ** 2 + u[1] ** 2 + u[2] ** 2) for u in self.v)
        self.g_max = [2.0 * vmax] * ncells  # an upper bound on |v_i - v_j| at the start
        self.carry = [0.0] * ncells
        self.collisions = 0
        self.candidates = 0


def random_unit_vector(rng):
    cos_t = 2.0 * rng.random() - 1.0
    sin_t = math.sqrt(max(0.0, 1.0 - cos_t * cos_t))
    phi = 2.0 * math.pi * rng.random()
    return sin_t * math.cos(phi), sin_t * math.sin(phi), cos_t


def dsmc_step(gas: Gas, dt: float, rng) -> None:
    """Advance the gas by one time step."""
    n = len(gas.x)
    for i in range(n):  # @line L1
        gas.x[i] = (gas.x[i] + gas.v[i][0] * dt) % gas.length
    cells = [[] for _ in range(gas.ncells)]
    width = gas.length / gas.ncells
    for i in range(n):  # @line L2
        cells[min(int(gas.x[i] / width), gas.ncells - 1)].append(i)
    for c, members in enumerate(cells):  # @line L3
        nc = len(members)
        if nc < 2:
            continue
        want = 0.5 * nc * (nc - 1) * gas.f_n * gas.sigma * gas.g_max[c] * dt / gas.cell_volume
        want += gas.carry[c]  # @line L4
        n_cand = int(want)
        gas.carry[c] = want - n_cand
        for _ in range(n_cand):  # @line L5
            gas.candidates += 1
            a = members[int(rng.random() * nc)]
            b = members[int(rng.random() * (nc - 1))]
            if b == a:
                b = members[nc - 1]
            va, vb = gas.v[a], gas.v[b]
            g = math.sqrt((va[0] - vb[0]) ** 2 + (va[1] - vb[1]) ** 2 + (va[2] - vb[2]) ** 2)  # @line L6
            if g > gas.g_max[c]:
                gas.g_max[c] = g  # @line L7
            if rng.random() * gas.g_max[c] >= g:  # @line L8
                continue
            gas.collisions += 1
            ux, uy, uz = random_unit_vector(rng)  # @line L9
            cm = [(va[k] + vb[k]) * 0.5 for k in range(3)]
            half = (0.5 * g * ux, 0.5 * g * uy, 0.5 * g * uz)
            gas.v[a] = [cm[k] + half[k] for k in range(3)]  # @line L10
            gas.v[b] = [cm[k] - half[k] for k in range(3)]


def maxwellian(n, temperature, rng):
    """n velocities from the Maxwell-Boltzmann law with m = k = 1."""
    s = math.sqrt(temperature)
    return [[rng.gauss(0.0, s), rng.gauss(0.0, s), rng.gauss(0.0, s)] for _ in range(n)]


def temperature(v) -> float:
    """Kinetic temperature in the frame of the mean velocity."""
    n = len(v)
    mean = [sum(u[k] for u in v) / n for k in range(3)]
    return sum((u[k] - mean[k]) ** 2 for u in v for k in range(3)) / (3.0 * n)


def momentum_and_energy(v):
    p = [sum(u[k] for u in v) for k in range(3)]
    e = 0.5 * sum(u[0] ** 2 + u[1] ** 2 + u[2] ** 2 for u in v)
    return p, e
