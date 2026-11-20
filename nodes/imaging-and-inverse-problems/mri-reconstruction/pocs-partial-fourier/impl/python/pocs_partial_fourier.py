# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pocs-partial-fourier/. The authors are listed in prov/KZJ4DM.jsonl.

"""POCS partial Fourier reconstruction (after Haacke, Lindskog and Lin 1991).

k-space convention: a list y of length n (n even) in DFT order, so index k
holds the signed frequency k for k < n/2 and k - n for k >= n/2. The data are
unitary DFT samples, y = F_u x with F_u = n^(-1/2) F. The scan acquires the
signed frequencies -n/2, ..., k0 with 0 <= k0 < n/2 - 1; the other entries of
y are not read.

The method alternates two projections in C^n, seen as R^(2n) with the real
inner product Re <u, v>:
- P1, onto C1 = {rho p : rho real}, the images with the reference phase p:
  x_j <- Re(conj(p_j) x_j) p_j, with |p_j| = 1.
- P2, onto C2 = {x : (F_u x)_k = y_k for every acquired k}: replace the
  acquired k-space samples of x by the data. F_u is unitary, so this is the
  orthogonal projection.
Both sets are closed and convex (C1 is a real subspace, C2 an affine
subspace), so the iterates converge (see proofs/correctness.md).

The reference phase comes from the central band |k| <= k0, which is acquired
on both sides, weighted by a triangle window.

Cost: two DFTs of length n per iteration, O(K n log n) for K iterations
when n is a power of two.
"""

import math
from typing import Optional, Sequence

from imgkit import dft, idft


def signed_freq(k: int, n: int) -> int:
    """The signed frequency of DFT index k: k for k < n/2, k - n otherwise."""
    return k if k < n // 2 else k - n


def partial_mask(n: int, k0: int) -> list[bool]:
    """True at the acquired DFT indices: the signed frequencies -n/2 .. k0."""
    return [signed_freq(k, n) <= k0 for k in range(n)]


def unitary_dft(x: Sequence[complex]) -> list[complex]:
    """F_u x = n^(-1/2) times the DFT."""
    s = 1.0 / math.sqrt(len(x))
    return [v * s for v in dft(list(x))]


def unitary_idft(y: Sequence[complex]) -> list[complex]:
    """F_u^H y = sqrt(n) times the inverse DFT."""
    s = math.sqrt(len(y))
    return [v * s for v in idft(list(y))]


def reference_phase(y: Sequence[complex], k0: int) -> list[complex]:
    """Unit phase p of the low-resolution image of the band |f| <= k0 (triangle window); 1 where it is zero."""
    n = len(y)
    w = [0.0] * n
    for k in range(n):
        f = signed_freq(k, n)
        if abs(f) <= k0:
            w[k] = 1.0 - abs(f) / (k0 + 1)
    low = unitary_idft([w[k] * y[k] for k in range(n)])
    return [v / abs(v) if v != 0 else 1.0 + 0j for v in low]


def project_phase(x: Sequence[complex], p: Sequence[complex]) -> list[complex]:
    """P1: the nearest image of the form rho p with rho real."""
    return [(pj.conjugate() * xj).real * pj for xj, pj in zip(x, p)]


def project_data(x: Sequence[complex], y: Sequence[complex], mask: Sequence[bool]) -> list[complex]:
    """P2: the nearest image whose acquired k-space samples equal the data."""
    big = unitary_dft(x)
    return unitary_idft([yk if a else bk for yk, bk, a in zip(y, big, mask)])


def pocs_1d(
    y: Sequence[complex],
    k0: int,
    iters: int = 100,
    phase: Optional[Sequence[complex]] = None,
    history: Optional[list] = None,
) -> list[complex]:
    """POCS reconstruction of one line; returns the complex image estimate.

    phase: an optional unit reference phase; by default reference_phase(y, k0).
    history: if a list is given, each iterate is appended to it.
    """
    n = len(y)
    if n % 2 or not 0 <= k0 < n // 2 - 1:
        raise ValueError("need an even n and 0 <= k0 < n/2 - 1")
    mask = partial_mask(n, k0)
    p = list(phase) if phase is not None else reference_phase(y, k0)  # @line L1
    x = unitary_idft([yk if a else 0j for yk, a in zip(y, mask)])  # @line L2
    for _ in range(iters):  # @line L3
        x = project_phase(x, p)  # @line L4
        big = unitary_dft(x)  # @line L5
        big = [yk if a else bk for yk, bk, a in zip(y, big, mask)]  # @line L6
        x = unitary_idft(big)  # @line L7
        if history is not None:
            history.append(x)
    return x  # @line L8


def pocs_2d(kspace: Sequence[Sequence[complex]], k0: int, iters: int = 100) -> list[list[complex]]:
    """POCS on an image whose k-space rows (axis 0, phase encoding) are partial.

    kspace[a][b] is the unitary 2D DFT sample at row frequency index a and
    column frequency index b. All columns are acquired, so an inverse DFT
    along the columns splits the problem into one line per image column.
    """
    n1, n2 = len(kspace), len(kspace[0])
    hybrid = [unitary_idft(row) for row in kspace]
    out = [[0j] * n2 for _ in range(n1)]
    for j in range(n2):
        col = pocs_1d([hybrid[a][j] for a in range(n1)], k0, iters)
        for i in range(n1):
            out[i][j] = col[i]
    return out


def zero_filled_1d(y: Sequence[complex], k0: int) -> list[complex]:
    """The zero-filled image: F_u^H of y with the missing samples set to 0."""
    m = partial_mask(len(y), k0)
    return unitary_idft([v if a else 0j for v, a in zip(y, m)])
