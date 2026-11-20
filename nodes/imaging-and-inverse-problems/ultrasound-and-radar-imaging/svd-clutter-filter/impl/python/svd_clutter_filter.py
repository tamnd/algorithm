# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/svd-clutter-filter/. The authors are listed in prov/BBV2DJ.jsonl.
"""The spatiotemporal SVD clutter filter of ultrafast Doppler ultrasound.

The input is a stack of N complex IQ frames frames[t][i][j] (slow time t,
depth i, lateral position j). The Casorati matrix S has one row per pixel and
one column per frame. With the singular values sigma_1 >= sigma_2 >= ... and
the right singular vectors v_j of S, the filter keeps the components k1 + 1 to
k2 (1-based):

    S_f = S P,  P = sum_{j = k1 + 1}^{k2} v_j v_j^H,

which equals sum_{j = k1 + 1}^{k2} sigma_j u_j v_j^H. The first k1 components
are the tissue (clutter) and the components after k2 are noise. The cut-off
ranks k1 and k2 are choices of the user, not outputs of the method.

The right singular vectors are the eigenvectors of the N x N Gram matrix
C = S^H S. This module finds them with the real symmetric eigensolver of
imgla, applied to the real 2N x 2N matrix [[Re C, -Im C], [Im C, Re C]].
"""

import cmath
import math
import random

from imgla import sym_eig


def casorati(frames):
    """The Casorati matrix: row p = i * nx + j holds the slow time samples of pixel (i, j)."""
    nt, nz, nx = len(frames), len(frames[0]), len(frames[0][0])
    return [[frames[t][i][j] for t in range(nt)] for i in range(nz) for j in range(nx)]


def frames_of(s, nz, nx):
    """The inverse of casorati: the list of frames of a pixels by slow time matrix."""
    nt = len(s[0])
    return [[[s[i * nx + j][t] for j in range(nx)] for i in range(nz)] for t in range(nt)]


def gram(s):
    """C = S^H S, the N x N Hermitian Gram matrix of the slow time columns."""
    n = len(s[0])
    c = [[0j] * n for _ in range(n)]
    for row in s:
        conj = [v.conjugate() for v in row]
        for a in range(n):
            ca, cr = conj[a], c[a]
            for b in range(n):
                cr[b] += ca * row[b]
    return c


def _embedded_eig(c):
    """Eigenpairs of the real embedding of a Hermitian C, eigenvalues in descending order.

    Each eigenvalue of C appears twice. The eigenvectors are the columns of the
    returned 2N x 2N real matrix.
    """
    n = len(c)
    emb = [[c[i][j].real for j in range(n)] + [-c[i][j].imag for j in range(n)] for i in range(n)]
    emb += [[c[i][j].imag for j in range(n)] + [c[i][j].real for j in range(n)] for i in range(n)]
    w, q = sym_eig(emb)
    order = list(range(2 * n - 1, -1, -1))
    return [w[k] for k in order], [[row[k] for k in order] for row in q]


def _projector(q, n, lo, hi):
    """The complex N x N projector onto the right singular vectors lo + 1 .. hi (1-based).

    The real columns 2 lo .. 2 hi - 1 of q span the embedding of that complex
    subspace. Their real projector is [[Re P, -Im P], [Im P, Re P]], so P is read
    from its left blocks.
    """
    cols = range(2 * lo, 2 * hi)
    p = [[0j] * n for _ in range(n)]
    for a in range(n):
        qa, qia = q[a], q[n + a]
        for b in range(n):
            qb = q[b]
            re = sum(qa[m] * qb[m] for m in cols)
            im = sum(qia[m] * qb[m] for m in cols)
            p[a][b] = complex(re, im)
    return p


def singular_values(s):
    """The singular values of S in descending order (the square roots of the eigenvalues of S^H S)."""
    w, _ = _embedded_eig(gram(s))
    return [math.sqrt(max(0.0, w[2 * j])) for j in range(len(s[0]))]


def svd_filter_matrix(s, tissue_cut, noise_cut=None):
    """Filter a Casorati matrix. Returns (S_f, sigma) with S_f = S P as in the module text."""
    n = len(s[0])
    hi = n if noise_cut is None else noise_cut
    if not 0 <= tissue_cut <= hi <= n:
        raise ValueError("need 0 <= tissue_cut <= noise_cut <= number of frames")
    c = gram(s)  # @line L2
    w, q = _embedded_eig(c)  # @line L3
    sigma = [math.sqrt(max(0.0, w[2 * j])) for j in range(n)]
    p = _projector(q, n, tissue_cut, hi)  # @line L5
    sf = [[sum(row[a] * p[a][b] for a in range(n)) for b in range(n)] for row in s]  # @line L6
    return sf, sigma


def svd_clutter_filter(frames, tissue_cut, noise_cut=None):
    """Filter a stack of IQ frames. Returns (filtered frames, power Doppler image, sigma).

    tissue_cut = k1 components are removed as tissue; components after
    noise_cut = k2 are removed as noise (None keeps all of them).
    """
    nt, nz, nx = len(frames), len(frames[0]), len(frames[0][0])
    s = casorati(frames)  # @line L1
    if not 0 <= tissue_cut <= (nt if noise_cut is None else noise_cut) <= nt:  # @line L4
        raise ValueError("need 0 <= tissue_cut <= noise_cut <= number of frames")
    sf, sigma = svd_filter_matrix(s, tissue_cut, noise_cut)
    pd = [[sum(abs(v) ** 2 for v in sf[i * nx + j]) / nt for j in range(nx)] for i in range(nz)]  # @line L7
    return frames_of(sf, nz, nx), pd, sigma  # @line L8


def simulate(nz, nx, nt, vessel_rows, seed, tissue_amp=10.0, blood_amp=1.0, noise=0.05, prf=1.0):
    """A small synthetic ultrafast Doppler acquisition.

    Tissue: a speckle field of strong amplitude in every pixel (scaled by 0.3
    inside the vessel, for the vessel wall and side lobes), moved by a slow
    common axial motion (breathing), so its phase changes smoothly in slow time
    with a small depth dependence. Blood: weak speckle in
    the rows of vessel_rows, with Doppler frequencies that follow a parabolic
    profile across the vessel and decorrelate from pulse to pulse (a random phase
    step with standard deviation 0.5 rad per pulse). Noise: white,
    complex Gaussian. Returns (frames, vessel_mask).
    """
    rng = random.Random(seed)

    def cgauss(sig):
        return complex(rng.gauss(0.0, sig / math.sqrt(2.0)), rng.gauss(0.0, sig / math.sqrt(2.0)))

    tissue = [[cgauss(tissue_amp) for _ in range(nx)] for _ in range(nz)]
    blood = [[cgauss(blood_amp) for _ in range(nx)] for _ in range(nz)]
    lo, hi = vessel_rows
    mid, half = 0.5 * (lo + hi - 1), 0.5 * (hi - lo) + 0.5
    mask = [[lo <= i < hi for _ in range(nx)] for i in range(nz)]
    frames = []
    for t in range(nt):
        motion = 0.6 * math.sin(2.0 * math.pi * t / (2.0 * nt))
        frame = []
        for i in range(nz):
            row = []
            for j in range(nx):
                val = tissue[i][j] * cmath.exp(1j * motion * (1.0 + 0.1 * i / nz))
                if mask[i][j]:
                    fd = 0.3 * prf * (1.0 - ((i - mid) / half) ** 2)
                    blood[i][j] *= cmath.exp(1j * rng.gauss(0.0, 0.5))
                    val = 0.3 * val + blood[i][j] * cmath.exp(2j * math.pi * fd * t / prf)
                row.append(val + cgauss(noise))
            frame.append(row)
        frames.append(frame)
    return frames, mask
