# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grappa/. The authors are listed in prov/KY1RH2.jsonl.

"""GRAPPA: generalized autocalibrating partially parallel acquisitions (Griswold et al. 2002).

Conventions: the k-space of coil k is an n x n array in DFT order, with the
phase encoding rows kappa as the first index and the readout columns l as the
second. The scan keeps the rows kappa = 0, R, 2R, ... and a block of
consecutive rows at the center (the ACS rows, autocalibration signal). Rows
and columns wrap around, as the DFT does.

For each offset delta = 1, ..., R - 1, a kernel predicts the sample of every
coil at (kappa, l) from the acquired samples of all coils at the rows
kappa - delta + R t (t in the block range) and the columns l - w, ..., l + w.
The weights are fitted by least squares on the ACS rows, where every row is
known. The kernel shape (the number of blocks nb and the half width w) and the
small regularization are choices.
"""

from typing import Sequence

from imgla import solve

Array = list[list[complex]]


def signed(kappa: int, n: int) -> int:
    """The signed frequency of DFT index kappa."""
    return kappa if kappa < n // 2 else kappa - n


def acs_rows(n: int, acs: int) -> list[int]:
    """The DFT indices of the acs center rows: signed frequencies -acs/2 .. acs/2 - 1, in increasing order."""
    return [(f + n) % n for f in range(-(acs // 2), acs - acs // 2)]


def grappa_mask(n: int, r: int, acs: int) -> list[bool]:
    """True for the acquired rows: kappa = 0 mod R, and the ACS rows."""
    keep = [kappa % r == 0 for kappa in range(n)]
    for kappa in acs_rows(n, acs):
        keep[kappa] = True
    return keep


def source_offsets(r: int, delta: int, nb: int, w: int) -> list[tuple[int, int]]:
    """Row and column offsets of the kernel sources, relative to the target at offset delta."""
    blocks = range(-(nb // 2 - 1), nb // 2 + 1)
    return [(-delta + r * t, d) for t in blocks for d in range(-w, w + 1)]


def calibrate(
    ksp: Sequence[Array],
    r: int,
    acs: int,
    nb: int = 2,
    w: int = 1,
    lam: float = 1e-8,
) -> dict[int, list[list[complex]]]:
    """Fit one weight matrix W_delta (sources x coils) for each delta = 1 .. R - 1 on the ACS rows."""
    c, n = len(ksp), len(ksp[0])
    rows = acs_rows(n, acs)
    weights = {}
    for delta in range(1, r):  # @line L1
        offs = source_offsets(r, delta, nb, w)
        lo = min(o[0] for o in offs)
        hi = max(o[0] for o in offs)
        a_rows, b_rows = [], []
        for t in range(max(0, -lo), min(len(rows), len(rows) - hi)):  # @line L2
            kappa = rows[t]
            for l in range(n):
                a_rows.append([ksp[k][(kappa + dr) % n][(l + dc) % n] for k in range(c) for dr, dc in offs])
                b_rows.append([ksp[k][kappa][l] for k in range(c)])
        m = len(a_rows[0])
        gram = [[sum(row[p].conjugate() * row[q] for row in a_rows) for q in range(m)] for p in range(m)]
        reg = lam * sum(gram[p][p].real for p in range(m)) / m
        for p in range(m):
            gram[p][p] += reg
        rhs = [[sum(ar[p].conjugate() * br[a] for ar, br in zip(a_rows, b_rows)) for a in range(c)] for p in range(m)]
        weights[delta] = solve(gram, rhs)  # @line L3
    return weights


def grappa(
    ksp: Sequence[Array],
    r: int,
    acs: int,
    nb: int = 2,
    w: int = 1,
    lam: float = 1e-8,
) -> list[Array]:
    """Fill the rows that were not acquired. ksp holds the acquired rows; the others are never read."""
    c, n = len(ksp), len(ksp[0])
    if n % r != 0:
        raise ValueError("n must be a multiple of R")
    keep = grappa_mask(n, r, acs)
    weights = calibrate(ksp, r, acs, nb, w, lam)
    out = [[list(ksp[k][kappa]) if keep[kappa] else [0j] * n for kappa in range(n)] for k in range(c)]
    for kappa in range(n):  # @line L4
        if keep[kappa]:
            continue
        delta = kappa % r  # @line L5
        offs = source_offsets(r, delta, nb, w)
        wd = weights[delta]
        for l in range(n):  # @line L6
            u = [ksp[k][(kappa + dr) % n][(l + dc) % n] for k in range(c) for dr, dc in offs]  # @line L7
            for a in range(c):
                out[a][kappa][l] = sum(us * wd[s][a] for s, us in enumerate(u))  # @line L8
    return out  # @line L9
