# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gerchberg-saxton-algorithm/. The authors are listed in prov/QDZSDB.jsonl.

"""The Gerchberg-Saxton algorithm: a phase from two magnitudes.

A complex signal f of length n is unknown. Its magnitude a = |f| in the
object plane and the magnitude A = |DFT(f)| in the Fourier plane are known
(unnormalized forward DFT, 1/n on the inverse, as in imgkit). Each iteration
puts the known magnitude on one plane and keeps the phase, then does the
same on the other plane. The errors use the unitary DFT:

    E_F(g)^2 = (1 / n) sum_u (|G_u| - A_u)^2,
    E_0(g')^2 = sum_j (|g'_j| - a_j)^2.

E_F does not increase from one iteration to the next.
"""

import cmath
import math

from imgkit import dft, idft


def with_magnitude(z, mag):
    """The vector with magnitudes mag and the phases of z (phase 0 where z is 0)."""
    return [m * v / abs(v) if abs(v) > 0.0 else complex(m) for v, m in zip(z, mag)]


def fourier_projection(g, amp):
    """P_F g: a nearest signal to g whose DFT magnitude is amp."""
    return idft(with_magnitude(dft(g), amp))


def fourier_error(g, amp):
    """E_F(g) = ||g - P_F g||."""
    n = len(g)
    return math.sqrt(sum((abs(v) - a) ** 2 for v, a in zip(dft(g), amp)) / n)


def object_error(gp, mag):
    """E_0(g') = ||g' - P_O g'||."""
    return math.sqrt(sum((abs(v) - a) ** 2 for v, a in zip(gp, mag)))


def gerchberg_saxton(mag, amp, phase0, iters):
    """Run Gerchberg-Saxton. Returns (g, errors) with errors[k] = E_F(g_k), k = 0 .. iters."""
    g = [m * cmath.exp(1j * p) for m, p in zip(mag, phase0)]  # @line L1
    n = len(g)
    errors = []
    for _ in range(iters):  # @line L2
        gf = dft(g)  # @line L3
        errors.append(math.sqrt(sum((abs(v) - a) ** 2 for v, a in zip(gf, amp)) / n))
        gpf = with_magnitude(gf, amp)  # @line L4
        gp = idft(gpf)  # @line L5
        g = with_magnitude(gp, mag)  # @line L6
    errors.append(fourier_error(g, amp))
    return g, errors  # @line L7
