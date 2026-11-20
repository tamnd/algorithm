# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slice-grappa/. The authors are listed in prov/863VBG.jsonl.

"""Slice-GRAPPA for simultaneous multi-slice imaging (Setsompop et al. 2012).

Conventions: the k-space of coil k of one slice is an n x n array in DFT
order, rows kappa (phase encoding) first, with the unitary DFT F / n. A scan
excites S slices at once, so each coil records the sum of the k-space of the
slices. With blipped CAIPI, slice z is shifted by Delta_z rows in the image
(a phase ramp exp(-2 pi i kappa Delta_z / n) on the k-space rows), so the
slices overlap less in the collapsed image.

Slice-GRAPPA fits one kernel per slice. The kernel maps a patch of the
collapsed k-space of all coils to the k-space sample of every coil of that
slice. The fit uses single-slice calibration data of each slice, summed into
a synthetic collapsed calibration. The kernel size (kr x kc), the calibration
rows and the small regularization are choices.
"""

import cmath
import math
from typing import Sequence

from imgla import solve

Array = list[list[complex]]


def caipi_shift(ksp: Array, shift: float) -> Array:
    """Shift the image by `shift` rows: multiply row kappa by exp(-2 pi i kappa shift / n)."""
    n = len(ksp)
    out = []
    for kappa, row in enumerate(ksp):
        ph = cmath.exp(-2j * math.pi * kappa * shift / n)
        out.append([v * ph for v in row])
    return out


def collapse(slices: Sequence[Sequence[Array]], shifts: Sequence[float]) -> list[Array]:
    """The collapsed k-space of each coil: the sum over slices of the shifted slice k-space."""
    c, n = len(slices[0]), len(slices[0][0])
    out = [[[0j] * n for _ in range(n)] for _ in range(c)]
    for sl, d in zip(slices, shifts):
        for k in range(c):
            sh = caipi_shift(sl[k], d)
            for kappa in range(n):
                row, src = out[k][kappa], sh[kappa]
                for l in range(n):
                    row[l] += src[l]
    return out


def calib_rows(n: int, acs: int) -> list[int]:
    """DFT indices of the acs center rows, signed frequencies -acs/2 .. acs/2 - 1, in order."""
    return [(f + n) % n for f in range(-(acs // 2), acs - acs // 2)]


def _offsets(kr: int, kc: int) -> list[tuple[int, int]]:
    return [(dr, dc) for dr in range(-(kr // 2), kr - kr // 2) for dc in range(-(kc // 2), kc - kc // 2)]


def _patch(ksp: Sequence[Array], kappa: int, l: int, offs) -> list[complex]:
    n = len(ksp[0])
    return [ksp[k][(kappa + dr) % n][(l + dc) % n] for k in range(len(ksp)) for dr, dc in offs]


def slice_grappa(
    y: Sequence[Array],
    calib: Sequence[Sequence[Array]],
    shifts: Sequence[float],
    acs: int = 16,
    kr: int = 3,
    kc: int = 3,
    lam: float = 1e-8,
) -> list[list[Array]]:
    """Separate the collapsed k-space y (one n x n array per coil) into the S slices.

    calib[z] holds the single-slice calibration k-space of slice z (its center
    rows are read). Returns out[z][k], the k-space of coil k of slice z.
    """
    c, n = len(y), len(y[0])
    offs = _offsets(kr, kc)
    rows = calib_rows(n, acs)
    y_cal = collapse(calib, shifts)  # @line L1
    lo = -min(o[0] for o in offs)
    hi = max(o[0] for o in offs)
    result = []
    for z, d in enumerate(shifts):  # @line L2
        target = [caipi_shift(calib[z][k], d) for k in range(c)]
        a_rows, b_rows = [], []
        for t in range(lo, len(rows) - hi):  # @line L3
            kappa = rows[t]
            for l in range(n):
                a_rows.append(_patch(y_cal, kappa, l, offs))
                b_rows.append([target[k][kappa][l] for k in range(c)])
        m = len(a_rows[0])
        gram = [[sum(ar[p].conjugate() * ar[q] for ar in a_rows) for q in range(m)] for p in range(m)]
        reg = lam * sum(gram[p][p].real for p in range(m)) / m
        for p in range(m):
            gram[p][p] += reg
        rhs = [[sum(ar[p].conjugate() * br[a] for ar, br in zip(a_rows, b_rows)) for a in range(c)] for p in range(m)]
        wz = solve(gram, rhs)  # @line L4
        xz = [[[0j] * n for _ in range(n)] for _ in range(c)]
        for kappa in range(n):  # @line L5
            for l in range(n):
                u = _patch(y, kappa, l, offs)  # @line L6
                for a in range(c):
                    xz[a][kappa][l] = sum(us * wz[s][a] for s, us in enumerate(u))  # @line L7
        result.append([caipi_shift(xz[k], -d) for k in range(c)])  # @line L8
    return result  # @line L9
