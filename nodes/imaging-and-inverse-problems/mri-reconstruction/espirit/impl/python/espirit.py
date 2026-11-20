# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/espirit/. The authors are listed in prov/CN1ST0.jsonl.

"""ESPIRiT: coil maps as eigenvectors of a calibration operator (Uecker et al. 2014).

Conventions: the k-space of coil k is an n x n array in DFT order (rows
first), of the coil image f_k with the unitary DFT F / n. The ACS block is
the center acs x acs part of k-space (signed frequencies -acs/2 .. acs/2 - 1
on both axes), where every sample is known.

Step 1. Put every kr x kc patch of the ACS block of all coils as a row of the
calibration matrix A. The entry (b, d) of a row is x_b(kappa + d). Keep the
right singular vectors v_l of A with sigma_l > t_s sigma_1 (the signal space).

Step 2. For each pixel p, build the c x c matrix

    G(p) = (1 / K) sum_l a_l(p) a_l(p)^H,   a_l(p)[a] = sum_d conj(v_l(a, d)) exp(2 pi i d . p / n),

with K = kr kc. A null vector v of A (A v = 0) gives sum_b conj(a(p)[b]) f_b(p) = 0
in the image domain, so the coil vector s(p) is orthogonal to every null
a(p), and G(p) s(p) = s(p) when the signal space is exact. The coil maps are the eigenvectors of G(p) with eigenvalue
1. The code takes the top eigenvector, makes its coil 0 entry real and
positive, and sets the map to 0 where the top eigenvalue is below t_e.

The kernel size, the ACS size and the thresholds t_s and t_e are choices.
"""

import cmath
import math
from typing import Sequence

Array = list[list[complex]]
Matrix = list[list[complex]]


def herm_eig(a: Sequence[Sequence[complex]], tol: float = 1e-14, max_sweeps: int = 60) -> tuple[list[float], Matrix]:
    """Eigenvalues (descending) and eigenvectors (as columns) of a complex Hermitian matrix.

    Cyclic Jacobi method with complex rotations. Returns (w, Q) with A = Q diag(w) Q^H.
    """
    n = len(a)
    m = [[complex(v) for v in row] for row in a]
    q = [[1.0 + 0j if i == j else 0j for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        off = sum(abs(m[i][j]) ** 2 for i in range(n) for j in range(n) if i != j)
        scale = sum(abs(m[i][i]) ** 2 for i in range(n)) + off
        if off <= tol * tol * scale or off == 0.0:
            break
        for p in range(n - 1):
            for r in range(p + 1, n):
                apr = m[p][r]
                b = abs(apr)
                if b == 0.0:
                    continue
                ph = apr / b  # exp(i phi)
                alpha, beta = m[p][p].real, m[r][r].real
                theta = (beta - alpha) / (2.0 * b)
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = c * t
                sp = s * ph.conjugate()  # s exp(-i phi)
                cp = c * ph.conjugate()  # c exp(-i phi)
                # columns: J = diag(1, exp(-i phi)) [[c, s], [-s, c]]
                for k in range(n):
                    mkp, mkr = m[k][p], m[k][r]
                    m[k][p] = c * mkp - sp * mkr
                    m[k][r] = s * mkp + cp * mkr
                # rows: the conjugate coefficients
                rp, rr = m[p], m[r]
                for k in range(n):
                    mpk, mrk = rp[k], rr[k]
                    rp[k] = c * mpk - sp.conjugate() * mrk
                    rr[k] = s * mpk + cp.conjugate() * mrk
                m[p][r] = m[r][p] = 0j
                for k in range(n):
                    qkp, qkr = q[k][p], q[k][r]
                    q[k][p] = c * qkp - sp * qkr
                    q[k][r] = s * qkp + cp * qkr
    order = sorted(range(n), key=lambda i: -m[i][i].real)
    return [m[i][i].real for i in order], [[q[k][i] for i in order] for k in range(n)]


def kernel_offsets(kr: int, kc: int) -> list[tuple[int, int]]:
    """The patch offsets (dr, dc), from (0, 0) to (kr - 1, kc - 1)."""
    return [(dr, dc) for dr in range(kr) for dc in range(kc)]


def calibration_matrix(ksp: Sequence[Array], acs: int, kr: int, kc: int) -> Matrix:
    """One row per kr x kc patch inside the ACS block; column (b, d) holds x_b(kappa + d)."""
    c, n = len(ksp), len(ksp[0])
    idx = [(f + n) % n for f in range(-(acs // 2), acs - acs // 2)]
    offs = kernel_offsets(kr, kc)
    rows = []
    for u in range(acs - kr + 1):
        for v in range(acs - kc + 1):
            rows.append([ksp[b][idx[u + dr]][idx[v + dc]] for b in range(c) for dr, dc in offs])
    return rows


def signal_space(ksp: Sequence[Array], acs: int, kr: int = 3, kc: int = 3, t_s: float = 1e-3) -> tuple[list[float], Matrix]:
    """Singular values of the calibration matrix and the kept right singular vectors (as columns)."""
    a = calibration_matrix(ksp, acs, kr, kc)
    m = len(a[0])
    gram = [[sum(row[i].conjugate() * row[j] for row in a) for j in range(m)] for i in range(m)]
    w, q = herm_eig(gram)
    sig = [math.sqrt(max(x, 0.0)) for x in w]
    keep = [l for l in range(m) if sig[l] > t_s * sig[0]]
    return sig, [[q[i][l] for l in keep] for i in range(m)]


def espirit(
    ksp: Sequence[Array],
    acs: int,
    kr: int = 3,
    kc: int = 3,
    t_s: float = 1e-3,
    t_e: float = 0.9,
) -> tuple[list[Array], list[list[float]]]:
    """Return (maps, eig): maps[k] is the n x n map of coil k, eig the top eigenvalue of G(p) at each pixel."""
    c, n = len(ksp), len(ksp[0])
    offs = kernel_offsets(kr, kc)
    kk = kr * kc
    _, v = signal_space(ksp, acs, kr, kc, t_s)  # @line L1
    nv = len(v[0])  # @line L2
    maps = [[[0j] * n for _ in range(n)] for _ in range(c)]
    eig = [[0.0] * n for _ in range(n)]
    for i in range(n):  # @line L3
        for j in range(n):
            ph = [cmath.exp(2j * math.pi * (dr * i + dc * j) / n) for dr, dc in offs]
            avec = [[sum(v[b * kk + t][l].conjugate() * ph[t] for t in range(kk)) for b in range(c)] for l in range(nv)]  # @line L4
            g = [[sum(al[a] * al[b].conjugate() for al in avec) / kk for b in range(c)] for a in range(c)]  # @line L5
            w, q = herm_eig(g)  # @line L6
            u = [q[a][0] for a in range(c)]
            eig[i][j] = w[0]
            if w[0] < t_e:  # @line L7
                continue
            ref = u[0] / abs(u[0]) if abs(u[0]) > 0 else 1.0
            for a in range(c):
                maps[a][i][j] = u[a] / ref
    return maps, eig  # @line L8
