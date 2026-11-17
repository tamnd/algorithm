# SPDX-License-Identifier: MIT
# Shared helper of the graphics-and-signals animation and simulation pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""The 2D cubic spline kernel, a uniform grid neighbor search and the SPH density.

This file is copied byte for byte into each impl/python folder that needs it.
It holds no solver step of a page: no equation of state, no pressure force,
no pressure solve and no time integration. The method of each page lives in
its slug file.

Conventions (prompts/graphics-ext.md, "Particles and SPH"):
- Positions are 2D tuples (x, y) in meters. Masses are in kg; in 2D a
  density is in kg/m^2.
- h is the smoothing length. The cubic spline of Monaghan has support 2h:
  W(r, h) = 0 for r >= 2h.
- grad_w(xij, h) is the gradient of W(|x_i - x_j|, h) with respect to x_i,
  where xij = x_i - x_j. It is antisymmetric: grad_w(-xij) = -grad_w(xij).
- The density of particle i is rho_i = sum_j m_j W(|x_i - x_j|, h), with
  j = i included.
"""

import math

# The 2D normalization constant of the cubic spline: W(0, h) = SIGMA_2D / h^2.
SIGMA_2D = 10.0 / (7.0 * math.pi)


def w_cubic(r, h):
    """Return the 2D cubic spline kernel W(r, h) for a distance r >= 0.

    W = SIGMA_2D / h^2 * (1 - 1.5 q^2 + 0.75 q^3) for 0 <= q < 1,
    W = SIGMA_2D / h^2 * 0.25 (2 - q)^3 for 1 <= q < 2, and W = 0 for
    q >= 2, with q = r / h. Unit 1/m^2. Cost O(1).
    """
    q = r / h
    s = SIGMA_2D / (h * h)
    if q < 1.0:
        return s * (1.0 - 1.5 * q * q + 0.75 * q * q * q)
    if q < 2.0:
        t = 2.0 - q
        return s * 0.25 * t * t * t
    return 0.0


def dw_cubic(r, h):
    """Return the radial derivative dW/dr of the 2D cubic spline. Unit 1/m^3."""
    q = r / h
    s = SIGMA_2D / (h * h * h)
    if q < 1.0:
        return s * (-3.0 * q + 2.25 * q * q)
    if q < 2.0:
        t = 2.0 - q
        return s * (-0.75 * t * t)
    return 0.0


def grad_w(xij, h):
    """Return the gradient of W(|xij|, h) with respect to x_i, for xij = x_i - x_j.

    The gradient is dW/dr * xij / |xij|. It is (0, 0) at r = 0, where the
    kernel has a smooth maximum. Cost O(1).
    """
    r = math.hypot(xij[0], xij[1])
    if r == 0.0:
        return (0.0, 0.0)
    d = dw_cubic(r, h) / r
    return (d * xij[0], d * xij[1])


def neighbor_pairs(positions, radius):
    """Return the sorted list of pairs (i, j), i < j, with |x_i - x_j| < radius.

    The search puts the particles in a uniform grid of square cells of side
    radius, keyed by (floor(x / radius), floor(y / radius)). Two particles at
    a distance below radius are in the same cell or in adjacent cells, so
    the search looks only at the 3 by 3 block of cells around each particle.
    The result is the same as a test of all pairs. For the cubic spline,
    pass radius = 2h. Cost O(n + q') for q' candidate pairs in adjacent
    cells; this is O(n) when the number of particles per cell is bounded.
    """
    cells = {}
    keys = []
    for i, p in enumerate(positions):
        key = (math.floor(p[0] / radius), math.floor(p[1] / radius))
        keys.append(key)
        cells.setdefault(key, []).append(i)
    r2 = radius * radius
    pairs = []
    for i, p in enumerate(positions):
        cx, cy = keys[i]
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in cells.get((cx + dx, cy + dy), ()):
                    if j <= i:
                        continue
                    ex = p[0] - positions[j][0]
                    ey = p[1] - positions[j][1]
                    if ex * ex + ey * ey < r2:
                        pairs.append((i, j))
    pairs.sort()
    return pairs


def neighbor_lists(positions, radius):
    """Return, for each particle i, the sorted list of j != i with |x_i - x_j| < radius."""
    lists = [[] for _ in positions]
    for i, j in neighbor_pairs(positions, radius):
        lists[i].append(j)
        lists[j].append(i)
    for nb in lists:
        nb.sort()
    return lists


def density(positions, masses, h):
    """Return the list of SPH densities rho_i = sum_j m_j W(|x_i - x_j|, h), j = i included.

    The sum runs over the neighbor pairs at distances below 2h, found with
    the grid search. Cost O(n + q) for q neighbor pairs.
    """
    w0 = w_cubic(0.0, h)
    rho = [m * w0 for m in masses]
    for i, j in neighbor_pairs(positions, 2.0 * h):
        r = math.hypot(positions[i][0] - positions[j][0], positions[i][1] - positions[j][1])
        w = w_cubic(r, h)
        rho[i] += masses[j] * w
        rho[j] += masses[i] * w
    return rho
