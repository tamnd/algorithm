# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/low-rank-plus-sparse-mri/. The authors are listed in prov/FVJ0PD.jsonl.

"""Low-rank plus sparse (L+S) reconstruction of dynamic MRI (Otazo, Candes and Sodickson 2015).

A series is a list of nt frames. Each frame is an n1 x n2 complex image,
stored row-major as one list of n1 * n2 numbers, so the series is the
Casorati matrix with one column per frame.

Encoding operator E: frame t and coil j give the k-space M_t F_u (c_j x_t),
with the unitary 2D DFT F_u (F_u^H F_u = I), the 0/1 mask M_t of frame t
and the coil map c_j (one coil with c = 1 if no maps are given). The data
are stored on the full grid, with zeros where M_t = 0. With
sum_j |c_j|^2 <= 1 at every pixel, ||E|| <= 1.

Sparsifying transform T: the unitary DFT along time at each pixel.

The method minimizes, by proximal gradient steps on the pair (L, S),

    F(L, S) = (1/2) ||E(L + S) - d||^2 + lamL ||L||_* + lamS ||T S||_1,

with the nuclear norm ||L||_* (the sum of the singular values of the
Casorati matrix) and the l1 norm of the complex entries. The gradient of
the data term in (L, S) has the Lipschitz constant 2 ||E||^2, so the
objective does not increase for t <= 1 / ||E||^2 and decreases by at
least (1/t - ||E||^2) ||change||^2 per step. With t = 1 the update has
the form of Table 1 of Otazo et al., which is the boundary case for
||E|| = 1. The start here is L_0 = S_0 = 0.

Complex SVD: imgla.svd is for real matrices, so singular value
thresholding uses the real symmetric embedding of the nt x nt Gram matrix
and imgla.sym_eig. This small piece of code lives here and not in a helper.

Cost per iteration, for P = n1 n2 pixels, nt frames and nc coils:
O(nt nc P log P) for E and E^H with the FFT, O(P nt log nt) for T and T^H
when nt is a power of two, O(P nt^2) for the Gram matrix and the product
L W, and O(nt^3) per Jacobi sweep.
"""

import math

from imgkit import dft, dft2, idft, idft2, unflatten
from imgla import sym_eig


# ------------------------------------------------------------------ operators


def _fu2(frame, n1, n2):
    s = 1.0 / math.sqrt(n1 * n2)
    return [v * s for row in dft2(unflatten(frame, n1, n2)) for v in row]


def _fu2h(kspace, n1, n2):
    s = math.sqrt(n1 * n2)
    return [v * s for row in idft2(unflatten(kspace, n1, n2)) for v in row]


def encode(series, masks, n1, n2, coils=None):
    """E(x): data[t][j] = M_t F_u (c_j x_t) on the full grid."""
    out = []
    for t, frame in enumerate(series):
        per_coil = []
        for cmap in coils or [None]:
            img = frame if cmap is None else [c * v for c, v in zip(cmap, frame)]
            k = _fu2(img, n1, n2)
            per_coil.append([v if m else 0j for v, m in zip(k, masks[t])])
        out.append(per_coil)
    return out


def encode_adjoint(data, masks, n1, n2, coils=None):
    """E^H(d): x_t = sum_j conj(c_j) F_u^H (M_t d[t][j])."""
    out = []
    for t, per_coil in enumerate(data):
        acc = [0j] * (n1 * n2)
        for j, k in enumerate(per_coil):
            img = _fu2h([v if m else 0j for v, m in zip(k, masks[t])], n1, n2)
            if coils is None:
                acc = [a + v for a, v in zip(acc, img)]
            else:
                acc = [a + c.conjugate() * v for a, c, v in zip(acc, coils[j], img)]
        out.append(acc)
    return out


def temporal_ft(series):
    """T: the unitary DFT along time at each pixel."""
    nt = len(series)
    s = 1.0 / math.sqrt(nt)
    cols = [dft([frame[p] for frame in series]) for p in range(len(series[0]))]
    return [[col[f] * s for col in cols] for f in range(nt)]


def temporal_ift(series):
    """T^H = T^(-1)."""
    nt = len(series)
    s = math.sqrt(nt)
    cols = [idft([frame[p] for frame in series]) for p in range(len(series[0]))]
    return [[col[f] * s for col in cols] for f in range(nt)]


# ------------------------------------------------------------------ proximal maps


def gram_function(series, g):
    """The matrix W = V diag(g(sigma_i^2)) V^H of the Gram matrix X^H X = V diag(sigma^2) V^H.

    The Hermitian nt x nt Gram matrix G is embedded as the real symmetric
    matrix [[Re G, -Im G], [Im G, Re G]], where each eigenvalue of G
    appears twice, and W is read from the sum of g(lambda) q q^T over its
    eigenpairs. Returns (W, s2) with s2 the eigenvalues of G in descending
    order.
    """
    nt = len(series)
    gm = [[sum(a.conjugate() * b for a, b in zip(series[i], series[j])) for j in range(nt)] for i in range(nt)]
    emb = [[0.0] * (2 * nt) for _ in range(2 * nt)]
    for i in range(nt):
        for j in range(nt):
            re, im = gm[i][j].real, gm[i][j].imag
            emb[i][j] = re
            emb[i + nt][j + nt] = re
            emb[i][j + nt] = -im
            emb[i + nt][j] = im
    vals, vecs = sym_eig(emb)
    gv = [g(max(v, 0.0)) for v in vals]
    w = [[0j] * nt for _ in range(nt)]
    for i in range(nt):
        for j in range(nt):
            re = sum(gv[q] * vecs[i][q] * vecs[j][q] for q in range(2 * nt))
            im = sum(gv[q] * vecs[i + nt][q] * vecs[j][q] for q in range(2 * nt))
            w[i][j] = complex(re, im)
    desc = sorted((max(v, 0.0) for v in vals), reverse=True)
    return w, [desc[2 * i] for i in range(nt)]


def svt(series, tau):
    """Singular value thresholding: U diag(max(sigma - tau, 0)) V^H = X V diag(max(1 - tau / sigma, 0)) V^H."""
    if tau <= 0:
        return [list(frame) for frame in series]

    def shrink(lam):
        sig = math.sqrt(lam)
        return max(1.0 - tau / sig, 0.0) if sig > 0 else 0.0

    w, _ = gram_function(series, shrink)
    nt = len(series)
    npix = len(series[0])
    return [[sum(series[i][p] * w[i][j] for i in range(nt)) for p in range(npix)] for j in range(nt)]


def nuclear_norm(series):
    """The sum of the singular values of the Casorati matrix."""
    _, s2 = gram_function(series, lambda lam: 0.0)
    return sum(math.sqrt(v) for v in s2)


def soft(z, tau):
    """Complex soft thresholding: (z / |z|) max(|z| - tau, 0)."""
    a = abs(z)
    return z * (1.0 - tau / a) if a > tau else 0j


# ------------------------------------------------------------------ the method


def objective(low, sparse, data, masks, n1, n2, lam_l, lam_s, coils=None):
    """F(L, S) = (1/2) ||E(L + S) - d||^2 + lamL ||L||_* + lamS ||T S||_1."""
    xs = [[a + b for a, b in zip(fl, fs)] for fl, fs in zip(low, sparse)]
    ex = encode(xs, masks, n1, n2, coils)
    fit = 0.5 * sum(abs(a - b) ** 2 for et, dt in zip(ex, data) for ej, dj in zip(et, dt) for a, b in zip(ej, dj))
    ts = temporal_ft(sparse)
    return fit + lam_l * nuclear_norm(low) + lam_s * sum(abs(v) for frame in ts for v in frame)


def l_plus_s(data, masks, n1, n2, lam_l, lam_s, step=1.0, iters=50, coils=None, history=None):
    """Recover L and S from dynamic k-space data d (one entry per frame and coil).

    step is the step t; the objective does not increase for t <= 1 / ||E||^2.
    If history is a list, F(L_k, S_k) is appended for k = 0, ..., iters.
    """
    nt = len(data)
    npix = n1 * n2
    low = [[0j] * npix for _ in range(nt)]  # @line L1
    sparse = [[0j] * npix for _ in range(nt)]
    m = [[step * v for v in frame] for frame in encode_adjoint(data, masks, n1, n2, coils)]
    if history is not None:
        history.append(objective(low, sparse, data, masks, n1, n2, lam_l, lam_s, coils))
    for _ in range(iters):  # @line L2
        new_low = svt([[a - b for a, b in zip(fm, fs)] for fm, fs in zip(m, sparse)], step * lam_l)  # @line L3
        diff = temporal_ft([[a - b for a, b in zip(fm, fl)] for fm, fl in zip(m, low)])  # @line L4
        new_sparse = temporal_ift([[soft(v, step * lam_s) for v in frame] for frame in diff])
        low, sparse = new_low, new_sparse  # @line L5
        xs = [[a + b for a, b in zip(fl, fs)] for fl, fs in zip(low, sparse)]  # @line L6
        ex = encode(xs, masks, n1, n2, coils)
        resid = [[[a - b for a, b in zip(ej, dj)] for ej, dj in zip(et, dt)] for et, dt in zip(ex, data)]
        grad = encode_adjoint(resid, masks, n1, n2, coils)
        m = [[x - step * g for x, g in zip(fx, fg)] for fx, fg in zip(xs, grad)]
        if history is not None:
            history.append(objective(low, sparse, data, masks, n1, n2, lam_l, lam_s, coils))
    return low, sparse  # @line L7
