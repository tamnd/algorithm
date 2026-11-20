# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spirit/. The authors are listed in prov/VXHK1N.jsonl.

"""SPIRiT: iterative self-consistent parallel imaging reconstruction (Lustig and Pauly 2010).

Conventions: the k-space of coil k is an n x n array in DFT order, rows first,
and rows and columns wrap around as in the DFT. mask[kappa][l] is True where
the sample was acquired; the sampling pattern may be any pattern. A block of
fully sampled center rows (the calibration region) gives the kernel.

The kernel G predicts each sample of coil a from the samples of all coils in
a kr x kc patch around it, without the sample itself:

    (G x)_a(kappa) = sum_b sum_d g[a][b][d] x_b(kappa + d),   g[a][a][0] = 0.

SPIRiT asks for a k-space x that is consistent with the kernel, x = G x, and
with the data, x = y on the acquired samples. With the data kept exactly,
the unknowns z are the missing samples, and the method minimizes
||(G - I)(x0 + P^T z)||^2 by CGLS (conjugate gradients on the normal
equations), where x0 is the zero-filled data and P^T puts z on the missing
samples. The kernel size, the calibration region and the small
regularization of the fit are choices.

Inside, each coil is a flat row-major list of n * n samples, and a shift by
d is a fixed permutation of the indices.
"""

import math
from typing import Callable, Optional, Sequence

from imgla import solve

Array = list[list[complex]]
Kernel = list[list[dict[tuple[int, int], complex]]]
Flat = list[list[complex]]


def kernel_offsets(kr: int, kc: int) -> list[tuple[int, int]]:
    """The patch offsets (dr, dc), centered on (0, 0)."""
    return [(dr, dc) for dr in range(-(kr // 2), kr - kr // 2) for dc in range(-(kc // 2), kc - kc // 2)]


def calib_rows(n: int, acs: int) -> list[int]:
    """DFT indices of the acs center rows, signed frequencies -acs/2 .. acs/2 - 1, in order."""
    return [(f + n) % n for f in range(-(acs // 2), acs - acs // 2)]


def calibrate(ksp: Sequence[Array], acs: int, kr: int = 3, kc: int = 3, lam: float = 1e-8) -> Kernel:
    """Fit g[a][b][d] by regularized least squares on the patches inside the calibration rows."""
    c, n = len(ksp), len(ksp[0])
    offs = kernel_offsets(kr, kc)
    rows = calib_rows(n, acs)
    lo, hi = -min(o[0] for o in offs), max(o[0] for o in offs)
    cols = [(b, d) for b in range(c) for d in offs]
    patches = []
    for t in range(lo, len(rows) - hi):
        kappa = rows[t]
        for l in range(n):
            patches.append([ksp[b][(kappa + d[0]) % n][(l + d[1]) % n] for b, d in cols])
    m = len(cols)
    gram = [[sum(p[i].conjugate() * p[j] for p in patches) for j in range(m)] for i in range(m)]
    reg = lam * sum(gram[i][i].real for i in range(m)) / m
    g: Kernel = []
    for a in range(c):
        target = cols.index((a, (0, 0)))
        keep = [i for i in range(m) if i != target]
        sub = [[gram[i][j] + (reg if i == j else 0.0) for j in keep] for i in keep]
        rhs = [gram[i][target] for i in keep]
        w = solve(sub, rhs)
        row = [dict() for _ in range(c)]
        for i, wi in zip(keep, w):
            b, d = cols[i]
            row[b][d] = wi
        g.append(row)
    return g


def _perm(n: int, dr: int, dc: int) -> list[int]:
    """Indices with out[kappa * n + l] = x[((kappa + dr) % n) * n + (l + dc) % n]."""
    return [((kappa + dr) % n) * n + (l + dc) % n for kappa in range(n) for l in range(n)]


def _g_flat(x: Flat, g: Kernel, n: int, adjoint: bool = False) -> Flat:
    """G x (or G^H x) on flat coils."""
    c = len(x)
    offs = sorted({d for row in g for gab in row for d in gab})
    out = [[0j] * (n * n) for _ in range(c)]
    for d in offs:
        # G: shift by d. G^H: shift by -d, (G^H y)_a(kappa) = sum_b sum_d conj(g[b][a][d]) y_b(kappa - d).
        perm = _perm(n, -d[0], -d[1]) if adjoint else _perm(n, d[0], d[1])
        for b in range(c):
            src = None
            for a in range(c):
                w = g[b][a].get(d) if adjoint else g[a][b].get(d)
                if w is None:
                    continue
                if adjoint:
                    w = w.conjugate()
                if src is None:
                    xb = x[b]
                    src = [xb[i] for i in perm]
                out[a] = [u + w * v for u, v in zip(out[a], src)]
    return out


def _flatten(x: Sequence[Array]) -> Flat:
    return [[v for row in a for v in row] for a in x]


def _unflatten(x: Flat, n: int) -> list[Array]:
    return [[a[i * n:(i + 1) * n] for i in range(n)] for a in x]


def apply_g(x: Sequence[Array], g: Kernel) -> list[Array]:
    """(G x)_a(kappa) = sum_b sum_d g[a][b][d] x_b(kappa + d)."""
    n = len(x[0])
    return _unflatten(_g_flat(_flatten(x), g, n), n)


def apply_g_adjoint(y: Sequence[Array], g: Kernel) -> list[Array]:
    """(G^H y)_b(kappa) = sum_a sum_d conj(g[a][b][d]) y_a(kappa - d)."""
    n = len(y[0])
    return _unflatten(_g_flat(_flatten(y), g, n, adjoint=True), n)


def _norm2(x: Flat) -> float:
    return sum(abs(v) ** 2 for a in x for v in a)


def spirit(
    y: Sequence[Array],
    mask: Sequence[Sequence[bool]],
    acs: int,
    iters: int,
    kr: int = 3,
    kc: int = 3,
    lam: float = 1e-8,
    g: Optional[Kernel] = None,
    callback: Optional[Callable[[int, float], None]] = None,
) -> list[Array]:
    """Return the full k-space of every coil. y holds the acquired samples; the others are never read.

    callback(t, ||r||) sees the residual norm ||(G - I) x|| after each iteration.
    """
    n = len(y[0])
    if g is None:
        g = calibrate(y, acs, kr, kc, lam)  # @line L1
    mflat = [mk for mrow in mask for mk in mrow]
    x0 = [[v if mk else 0j for v, mk in zip(a, mflat)] for a in _flatten(y)]  # @line L2

    def op(z: Flat) -> Flat:  # B z = (G - I) P^T z, with z stored as full arrays that are 0 on the acquired samples  # @line L3
        return [[u - v for u, v in zip(ga, za)] for ga, za in zip(_g_flat(z, g, n), z)]

    def op_h(w: Flat) -> Flat:  # B^H w = P (G^H - I) w
        return [[0j if mk else u - v for u, v, mk in zip(ga, wa, mflat)] for ga, wa in zip(_g_flat(w, g, n, True), w)]

    r = [[v - u for u, v in zip(ga, xa)] for ga, xa in zip(_g_flat(x0, g, n), x0)]  # @line L4
    z = [[0j] * (n * n) for _ in x0]
    s = op_h(r)
    p = s
    gamma = _norm2(s)
    for t in range(iters):  # @line L5
        if gamma == 0.0:
            break
        q = op(p)  # @line L6
        alpha = gamma / _norm2(q)  # @line L7
        z = [[u + alpha * v for u, v in zip(za, pa)] for za, pa in zip(z, p)]  # @line L8
        r = [[u - alpha * v for u, v in zip(ra, qa)] for ra, qa in zip(r, q)]
        s = op_h(r)  # @line L9
        gamma_new = _norm2(s)
        beta = gamma_new / gamma
        p = [[u + beta * v for u, v in zip(sa, pa)] for sa, pa in zip(s, p)]
        gamma = gamma_new
        if callback is not None:
            callback(t + 1, math.sqrt(_norm2(r)))
    return _unflatten([[u + v for u, v in zip(xa, za)] for xa, za in zip(x0, z)], n)  # @line L10
