# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modeller/. The authors are listed in prov/1ZBXCP.jsonl.

"""Comparative modeling by satisfaction of spatial restraints, on C-alpha atoms.

This is the method of MODELLER (Sali and Blundell 1993) in a small form:

1. Derive distance restraints for the target from the aligned template
   residues, plus chain restraints between residues i and i + 1.
2. Each restraint is a Gaussian density p(d) with mean d0 and spread sigma,
   so the objective F = -sum ln p(d) is, up to a constant,
       F(x) = sum over restraints of ((|x_i - x_j| - d0) / sigma)^2 / 2.
3. Minimize F by conjugate gradients, refine by molecular dynamics with
   simulated annealing, and minimize again by conjugate gradients.

The real program uses many more kinds of restraints (dihedral angles,
side-chain atoms, statistical terms) and all heavy atoms. Distances alone
do not fix the hand of the model: a mirror image has the same F.

Coordinates are lists of 3-tuples of floats. All randomness comes from an
explicit random.Random passed by the caller.
"""

import math
import random
from typing import List, Sequence, Tuple

Vec = Tuple[float, float, float]
Restraint = Tuple[int, int, float, float]  # (i, j, d0, sigma), i < j

CA_CA = 3.8  # distance between consecutive C-alpha atoms, in angstrom


def dist(p: Sequence[float], q: Sequence[float]) -> float:
    return math.sqrt(sum((p[k] - q[k]) ** 2 for k in range(3)))


def derive_restraints(
    template: Sequence[Vec], alignment: Sequence[Tuple[int, int]], n: int,
    cutoff: float = 12.0, sigma: float = 0.5, chain_sigma: float = 0.1,
) -> List[Restraint]:
    """Restraints on a target of n residues from a template and an alignment.

    alignment holds pairs (i, k): target residue i is aligned to template residue k.
    """
    restraints: List[Restraint] = []
    pairs = sorted(alignment)
    for a in range(len(pairs)):  # @line L1
        for b in range(a + 1, len(pairs)):
            (i, k), (j, l) = pairs[a], pairs[b]
            d = dist(template[k], template[l])
            if d <= cutoff and j != i + 1:  # @line L2
                restraints.append((i, j, d, sigma))  # @line L3
    for i in range(n - 1):  # @line L4
        restraints.append((i, i + 1, CA_CA, chain_sigma))
    return restraints


def objective(x: Sequence[Vec], restraints: Sequence[Restraint]) -> float:
    """F(x) = sum ((d - d0) / sigma)^2 / 2, the negative log density up to a constant."""
    f = 0.0
    for i, j, d0, s in restraints:
        f += 0.5 * ((dist(x[i], x[j]) - d0) / s) ** 2
    return f


def gradient(x: Sequence[Vec], restraints: Sequence[Restraint]) -> List[List[float]]:
    g = [[0.0, 0.0, 0.0] for _ in x]
    for i, j, d0, s in restraints:
        diff = [x[i][k] - x[j][k] for k in range(3)]
        d = math.sqrt(sum(v * v for v in diff))
        if d == 0.0:
            continue  # the gradient of |x_i - x_j| is not defined here; skip the term
        c = (d - d0) / (s * s * d)
        for k in range(3):
            g[i][k] += c * diff[k]
            g[j][k] -= c * diff[k]
    return g


def _add(x, p, t):
    return [tuple(x[i][k] + t * p[i][k] for k in range(3)) for i in range(len(x))]


def _dot(u, v) -> float:
    return sum(u[i][k] * v[i][k] for i in range(len(u)) for k in range(3))


def conjugate_gradients(x, restraints, max_iter: int = 3000, tol: float = 1e-12):
    """Polak-Ribiere conjugate gradients with a backtracking (Armijo) line search.

    Stops when the squared norm of the gradient is at most tol, or after max_iter steps.
    """
    x = [tuple(p) for p in x]
    f = objective(x, restraints)
    g = gradient(x, restraints)
    p = [[-v for v in row] for row in g]
    t = 1.0
    for _ in range(max_iter):
        gg = _dot(g, g)
        if gg <= tol:
            break
        slope = _dot(g, p)
        if slope >= 0:  # not a descent direction: restart along the steepest descent
            p = [[-v for v in row] for row in g]
            slope = -gg
        t = min(1.0, 4.0 * t)  # start from a step a little longer than the last accepted one
        while True:
            x_new = _add(x, p, t)
            f_new = objective(x_new, restraints)
            if f_new <= f + 1e-4 * t * slope or t < 1e-14:
                break
            t *= 0.5
        g_new = gradient(x_new, restraints)
        beta = max(0.0, (_dot(g_new, g_new) - _dot(g_new, g)) / gg)  # Polak-Ribiere, with restart
        p = [[-g_new[i][k] + beta * p[i][k] for k in range(3)] for i in range(len(x))]
        x, f, g = x_new, f_new, g_new
    return x


def md_anneal(x, restraints, rng: random.Random, temps=(4.0, 2.0, 1.0, 0.5, 0.2, 0.05),
              steps: int = 150, dt: float = 0.02):
    """Molecular dynamics on F with unit masses, at a falling temperature.

    Velocity Verlet steps; at the start of each stage the velocities are drawn
    from the Maxwell distribution of that temperature (k_B = 1).
    """
    x = [list(p) for p in x]
    g = gradient(x, restraints)
    for temp in temps:
        v = [[rng.gauss(0.0, math.sqrt(temp)) for _ in range(3)] for _ in x]
        for _ in range(steps):
            for i in range(len(x)):
                for k in range(3):
                    v[i][k] -= 0.5 * dt * g[i][k]
                    x[i][k] += dt * v[i][k]
            g = gradient(x, restraints)
            for i in range(len(x)):
                for k in range(3):
                    v[i][k] -= 0.5 * dt * g[i][k]
    return [tuple(p) for p in x]


def initial_model(template, alignment, n, rng: random.Random):
    """Copy the aligned C-alpha atoms; put each other residue near its chain neighbour."""
    x: List[Vec] = [None] * n
    for i, k in alignment:
        x[i] = tuple(template[k])
    first = next((i for i in range(n) if x[i] is not None), None)
    if first is None:
        x[0], first = (0.0, 0.0, 0.0), 0
    for i in list(range(first + 1, n)) + list(range(first - 1, -1, -1)):
        if x[i] is None:
            ref = x[i - 1] if i > first else x[i + 1]
            u = [rng.gauss(0.0, 1.0) for _ in range(3)]
            nu = math.sqrt(sum(c * c for c in u)) or 1.0
            x[i] = tuple(ref[k] + CA_CA * u[k] / nu for k in range(3))
    return x


def modeller(template, alignment, n, rng: random.Random, anneal: bool = True):
    """Build a C-alpha model of a target of n residues. Returns (coordinates, restraints)."""
    restraints = derive_restraints(template, alignment, n)  # @line L1 @line L2 @line L3 @line L4
    x = initial_model(template, alignment, n, rng)  # @line L5
    x = conjugate_gradients(x, restraints)  # @line L6
    if anneal:
        x = md_anneal(x, restraints, rng)  # @line L7
        x = conjugate_gradients(x, restraints)  # @line L8
    return x, restraints  # @line L9


def drms(x, y, pairs) -> float:
    """Root mean square difference of the distances over the given pairs of indices."""
    s = sum((dist(x[i], x[j]) - dist(y[k], y[l])) ** 2 for (i, k), (j, l) in pairs)
    return math.sqrt(s / max(1, len(pairs)))
