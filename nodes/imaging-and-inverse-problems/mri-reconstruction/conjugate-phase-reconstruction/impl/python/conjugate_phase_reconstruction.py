# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conjugate-phase-reconstruction/. The authors are listed in prov/ES8X47.jsonl.

"""Conjugate phase reconstruction with off-resonance correction.

Signal model (single coil, no relaxation during the readout): sample j at
k-space position k_j (cycles per unit length) and time t_j (seconds) is
    s_j = sum_i x_i exp(-i omega_i t_j) exp(-i 2 pi k_j . r_i),
where pixel i sits at r_i and has off-resonance frequency omega_i (rad/s).
Write this as s = A x.

Conjugate phase reconstruction undoes both phase terms at each pixel and
weights each sample by its density compensation weight w_j:
    xhat_i = sum_j w_j s_j exp(+i 2 pi k_j . r_i) exp(+i omega_i t_j),
that is xhat = A^H W s. It is exact when A^H W A = I, for example on a
full Cartesian grid with w_j = 1 / m and a constant omega. Otherwise it is
an approximation: it ignores the change of omega inside the support of the
point spread function.

Cost: O(m n) complex exponentials for m samples and n pixels.
"""

import cmath
import math
from typing import Sequence

Vec = Sequence[float]


def forward(x: Sequence[complex], pos: Sequence[Vec], omega: Sequence[float], ks: Sequence[Vec], ts: Sequence[float]) -> list[complex]:
    """s = A x, the signal of image x with field map omega at samples (ks, ts)."""
    out = []
    for k, t in zip(ks, ts):
        acc = 0j
        for xi, r, om in zip(x, pos, omega):
            ph = -om * t - 2.0 * math.pi * sum(a * b for a, b in zip(k, r))
            acc += xi * cmath.exp(1j * ph)
        out.append(acc)
    return out


def conjugate_phase(
    s: Sequence[complex],
    ks: Sequence[Vec],
    ts: Sequence[float],
    w: Sequence[float],
    pos: Sequence[Vec],
    omega: Sequence[float],
) -> list[complex]:
    """xhat = A^H W s: the conjugate phase image at the pixel positions pos."""
    xhat = []
    for r, om in zip(pos, omega):  # @line L1
        acc = 0j  # @line L2
        for sj, k, t, wj in zip(s, ks, ts, w):  # @line L3
            ph = 2.0 * math.pi * sum(a * b for a, b in zip(k, r)) + om * t
            acc += wj * sj * cmath.exp(1j * ph)  # @line L4
        xhat.append(acc)  # @line L5
    return xhat  # @line L6


def pixel_grid(n: int) -> list[tuple[float, float]]:
    """Pixel positions (column, row) - n/2 in pixel units, row-major, for an n x n image."""
    return [(c - n // 2, a - n // 2) for a in range(n) for c in range(n)]


def epi_cartesian(n: int, fov: float, esp: float = 5e-4, dwell: float = 4e-6, t0: float = 0.0):
    """A full n x n Cartesian k-space grid in EPI order and its sample times.

    k = (u, v) / fov with u, v in -n/2 .. n/2 - 1; with pixel_grid positions,
    fov = n gives the DFT grid. Line v is read at
    t0 + (v + n/2) esp, and sample u of a line adds (u + n/2) dwell. The
    readout direction alternates line by line, as in EPI. Returns (ks, ts).
    """
    ks, ts = [], []
    for li, v in enumerate(range(-n // 2, n // 2)):
        us = list(range(-n // 2, n // 2))
        if li % 2:
            us.reverse()
        for q, u in enumerate(us):
            ks.append((u / fov, v / fov))
            ts.append(t0 + li * esp + q * dwell)
    return ks, ts
