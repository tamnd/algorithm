# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/homodyne-reconstruction/. The authors are listed in prov/4ZY7XX.jsonl.

"""Homodyne reconstruction of partial Fourier MRI data (Noll, Nishimura and Macovski 1991).

k-space convention: a list y of length n (n even) in DFT order, so index k
holds the signed frequency k for k < n/2 and k - n for k >= n/2. The data are
unitary DFT samples, y = F_u x with F_u = n^(-1/2) F. The scan acquires the
signed frequencies -n/2, ..., k0 with 0 <= k0 < n/2 - 1; the entries of y at
the frequencies k0 + 1, ..., n/2 - 1 are not read.

For an image x = exp(i phi0) rho with a constant phase phi0 and rho >= 0, the
output is rho exactly (see proofs/correctness.md). For a smooth phase the
output is an approximation.

Cost: two inverse DFTs of length n and O(n) other work per line, so
O(n log n) with the radix-2 FFT of imgkit when n is a power of two.
"""

import math
from typing import Sequence

from imgkit import dft, idft


def signed_freq(k: int, n: int) -> int:
    """The signed frequency of DFT index k: k for k < n/2, k - n otherwise."""
    return k if k < n // 2 else k - n


def homodyne_weights(n: int, k0: int, kind: str = "step") -> list[float]:
    """The homodyne filter H in DFT order. H(f) + H(-f) = 2 for every frequency f.

    kind "step": 2 on the high frequencies of the acquired side, 1 on the
    symmetric band |f| <= k0 and at f = -n/2, 0 on the missing side.
    kind "ramp": the same, with a linear ramp 1 - f / (k0 + 1) on |f| <= k0.
    """
    h = [0.0] * n
    for k in range(n):
        f = signed_freq(k, n)
        if f > k0:
            h[k] = 0.0
        elif abs(f) <= k0:
            h[k] = 1.0 if kind == "step" else 1.0 - f / (k0 + 1)
        elif f == -(n // 2):
            h[k] = 1.0
        else:
            h[k] = 2.0
    return h


def triangle_window(n: int, k0: int) -> list[float]:
    """T(f) = 1 - |f| / (k0 + 1) on |f| <= k0, 0 elsewhere, in DFT order."""
    t = [0.0] * n
    for k in range(n):
        f = signed_freq(k, n)
        if abs(f) <= k0:
            t[k] = 1.0 - abs(f) / (k0 + 1)
    return t


def unitary_idft(y: Sequence[complex]) -> list[complex]:
    """F_u^H y = sqrt(n) times the inverse DFT."""
    s = math.sqrt(len(y))
    return [v * s for v in idft(list(y))]


def unitary_dft(x: Sequence[complex]) -> list[complex]:
    """F_u x = n^(-1/2) times the DFT."""
    s = 1.0 / math.sqrt(len(x))
    return [v * s for v in dft(list(x))]


def homodyne_1d(y: Sequence[complex], k0: int, kind: str = "step") -> list[float]:
    """The real image rho from partial k-space y (DFT order, frequencies -n/2 .. k0 acquired)."""
    n = len(y)
    if n % 2 or not 0 <= k0 < n // 2 - 1:
        raise ValueError("need an even n and 0 <= k0 < n/2 - 1")
    h = homodyne_weights(n, k0, kind)  # @line L1
    t = triangle_window(n, k0)  # @line L2
    z = unitary_idft([h[k] * y[k] for k in range(n)])  # @line L3
    low = unitary_idft([t[k] * y[k] for k in range(n)])  # @line L4
    rho = [0.0] * n
    for j in range(n):  # @line L5
        if low[j] == 0:  # @line L6
            rho[j] = 0.0
        else:
            rho[j] = (low[j].conjugate() * z[j]).real / abs(low[j])  # @line L7
    return rho  # @line L8


def homodyne_2d(kspace: Sequence[Sequence[complex]], k0: int, kind: str = "step") -> list[list[float]]:
    """Homodyne on an image whose k-space rows (axis 0, phase encoding) are partial.

    kspace[a][b] is the unitary 2D DFT sample at row frequency index a and
    column frequency index b, both in DFT order. All columns are acquired.
    The inverse DFT along the columns (the readout) gives one 1D problem per
    image column, and each one is solved by homodyne_1d.
    """
    n1, n2 = len(kspace), len(kspace[0])
    hybrid = [unitary_idft(row) for row in kspace]  # rows: ky; columns: x
    out = [[0.0] * n2 for _ in range(n1)]
    for j in range(n2):
        col = homodyne_1d([hybrid[a][j] for a in range(n1)], k0, kind)
        for i in range(n1):
            out[i][j] = col[i]
    return out


def unitary_dft2(img: Sequence[Sequence[complex]]) -> list[list[complex]]:
    """The unitary 2D DFT of an image (DFT order on both axes)."""
    rows = [unitary_dft(r) for r in img]
    cols = [unitary_dft(list(c)) for c in zip(*rows)]
    return [list(r) for r in zip(*cols)]


def partial_mask(n: int, k0: int) -> list[bool]:
    """True at the acquired DFT indices: the signed frequencies -n/2 .. k0."""
    return [signed_freq(k, n) <= k0 for k in range(n)]


def zero_filled_1d(y: Sequence[complex], k0: int) -> list[complex]:
    """The zero-filled image: F_u^H of y with the missing samples set to 0."""
    m = partial_mask(len(y), k0)
    return unitary_idft([v if a else 0.0 for v, a in zip(y, m)])
