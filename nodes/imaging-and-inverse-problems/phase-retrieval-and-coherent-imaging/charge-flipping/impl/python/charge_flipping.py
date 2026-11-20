# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/charge-flipping/. The authors are listed in prov/3DN6XM.jsonl.

"""Charge flipping (Oszlanyi and Suto 2004) for a periodic density in P1.

Conventions:
- The density rho is a real n1 x n2 image on one unit cell (use n1 = 1 for a
  1D cell). Its structure factors are the unnormalized DFT F = DFT2(rho), so
  F(h) = sum_x rho(x) exp(-2 pi i h . x / n), and rho = IDFT2(F) (imgkit).
- The data are the amplitudes amp[h] = |F(h)| for the indices with
  observed[h] true. F(0), the total charge, is usually not observed.
- A real density has Friedel symmetry F(-h) = conj(F(h)); the random start
  phases obey it, so every density in the iteration is real.

Cost per cycle: two 2D DFTs and O(n1 n2) other work.
"""

import cmath
import math
import random

from imgkit import dft2, idft2


def neg(k, l, n1, n2):
    """The index -h of h = (k, l), modulo the grid."""
    return (-k) % n1, (-l) % n2


def random_start(amp, observed, seed):
    """F(h) = amp exp(i phi) with random phases, Friedel pairs conjugate, F = 0 elsewhere.

    An index with h = -h (the origin, or a Nyquist index) gets the phase 0
    or pi, so that F(h) is real there.
    """
    rng = random.Random(seed)
    n1, n2 = len(amp), len(amp[0])
    f = [[0j] * n2 for _ in range(n1)]
    for k in range(n1):
        for l in range(n2):
            if not observed[k][l]:
                continue
            mk, ml = neg(k, l, n1, n2)
            if (mk, ml) == (k, l):
                f[k][l] = complex(amp[k][l] * rng.choice((1.0, -1.0)))
            elif (k, l) < (mk, ml):
                phi = rng.uniform(-math.pi, math.pi)
                f[k][l] = amp[k][l] * cmath.exp(1j * phi)
                f[mk][ml] = amp[mk][ml] * cmath.exp(-1j * phi)
    return f


def flip(rho, delta):
    """g = rho where rho > delta, and -rho elsewhere."""
    return [[v if v > delta else -v for v in row] for row in rho]


def r_factor(amp, observed, g_spec):
    """R = sum | |Fobs| - |G| | / sum |Fobs| over the observed indices (a convergence indicator)."""
    num = den = 0.0
    for ra, ro, rg in zip(amp, observed, g_spec):
        for a, o, g in zip(ra, ro, rg):
            if o:
                num += abs(a - abs(g))
                den += a
    return num / den


def charge_flipping(amp, observed, delta, cycles, seed=0, start=None):
    """Run charge flipping and return (rho, R) after the given number of cycles.

    start, if given, replaces the random start structure factors, F(0)
    included (it must obey Friedel symmetry). F(0) is free: the random start
    sets it to 0 unless it is observed, and every later cycle gives it the
    value G(0) of the flipped density.
    """
    n1, n2 = len(amp), len(amp[0])
    f = [list(row) for row in start] if start is not None else random_start(amp, observed, seed)  # @line L1
    rho, r = None, 1.0
    for _ in range(cycles):  # @line L2
        rho = [[v.real for v in row] for row in idft2(f)]  # @line L3
        g = flip(rho, delta)  # @line L4
        gs = dft2(g)  # @line L5
        r = r_factor(amp, observed, gs)
        for k in range(n1):  # @line L6
            for l in range(n2):
                if observed[k][l]:
                    s = gs[k][l]
                    f[k][l] = amp[k][l] * s / abs(s) if abs(s) > 0.0 else complex(amp[k][l])  # @line L7
                elif (k, l) == (0, 0):
                    f[k][l] = gs[0][0]  # @line L8
                else:
                    f[k][l] = 0j  # @line L9
    rho = [[v.real for v in row] for row in idft2(f)]
    return rho, r  # @line L10
