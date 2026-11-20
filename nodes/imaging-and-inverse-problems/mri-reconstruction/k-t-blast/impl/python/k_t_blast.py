# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-t-blast/. The authors are listed in prov/MVRMMT.jsonl.

"""k-t BLAST and k-t SENSE (Tsao, Boesiger and Pruessmann 2003) for a series of 1D frames.

A series is a list of nt frames x[t][y], each a list of n complex pixels.
Frame t of coil c has the k-space F_u(c x_t), with the unitary DFT F_u
(F_u^H F_u = I) in DFT order. Data are stored on the full grid as
data[t][c][k], with zeros where the mask is 0. With no coil maps there is
one coil with c = 1.

Sampling: frame t keeps the lines k with k = shift * t (mod R). This is a
sheared lattice in k-t space. It needs n and nt divisible by R and shift
prime to R, so every line is sampled in nt / R frames.

x-f space: rho(y, f) is the unitary DFT along time of x(y, t). For the
lattice above, the zero filled data give, after the unitary inverse DFT
along k and the unitary DFT along t,

    rho_alias_c(y, f) = (1/R) sum_{j=0}^{R-1} c(y_j) rho(y_j, f_j),
    y_j = y + j n / R,  f_j = f + j shift nt / R (mod nt).

So the x-f grid splits into alias groups of R points, and each group is
one small linear system rho_alias = A rho_G with an nc x R matrix A.

Reconstruction of one group, with the prior power P = diag(|rho_train|^2)
from training data and the noise variance psi:

    rho_G = P A^H (A P A^H + psi I)^(-1) rho_alias.

This is the Wiener estimate for a zero-mean prior with covariance P and
white noise of variance psi. The time average (the baseline) is removed
before the unfolding and added back after it.
"""

import math

from imgkit import dft, idft
from imgla import solve


# ------------------------------------------------------------------ transforms


def _fu(x):
    s = 1.0 / math.sqrt(len(x))
    return [v * s for v in dft(x)]


def _fuh(k):
    s = math.sqrt(len(k))
    return [v * s for v in idft(k)]


def time_ft(rows):
    """Unitary DFT along time of rows[t][y]; returns rho[f][y]."""
    nt, n = len(rows), len(rows[0])
    cols = [_fu([rows[t][y] for t in range(nt)]) for y in range(n)]
    return [[cols[y][f] for y in range(n)] for f in range(nt)]


def time_ift(rho):
    """Inverse of time_ft."""
    nt, n = len(rho), len(rho[0])
    cols = [_fuh([rho[f][y] for f in range(nt)]) for y in range(n)]
    return [[cols[y][t] for y in range(n)] for t in range(nt)]


# ------------------------------------------------------------------ sampling


def lattice_mask(n, nt, r, shift=1):
    """mask[t][k] = 1 if k = shift * t (mod r)."""
    if n % r or nt % r or math.gcd(shift, r) != 1:
        raise ValueError("need n and nt divisible by r and shift prime to r")
    return [[1 if (k - shift * t) % r == 0 else 0 for k in range(n)] for t in range(nt)]


def acquire(series, mask, coils=None):
    """data[t][c][k] = mask[t][k] F_u(c x_t)(k)."""
    out = []
    for t, frame in enumerate(series):
        per_coil = []
        for cmap in coils or [None]:
            img = frame if cmap is None else [a * b for a, b in zip(cmap, frame)]
            per_coil.append([v if m else 0j for v, m in zip(_fu(img), mask[t])])
        out.append(per_coil)
    return out


def xf_alias(data):
    """rho_alias[c][f][y]: inverse DFT along k, then DFT along t, per coil."""
    nc = len(data[0])
    return [time_ft([_fuh(per_coil[c]) for per_coil in data]) for c in range(nc)]


def alias_groups(n, nt, r, shift=1):
    """The groups of R x-f points that fold onto one point (y0, f0), y0 < n / R."""
    return [
        [((y0 + j * n // r) % n, (f0 + j * shift * nt // r) % nt) for j in range(r)]
        for y0 in range(n // r)
        for f0 in range(nt)
    ]


# ------------------------------------------------------------------ prior


def training_power(train, remove_mean=True):
    """|rho_train(y, f)|^2 of a training series, by default after its time average is removed."""
    nt, n = len(train), len(train[0])
    mean = [sum(train[t][y] for t in range(nt)) / nt if remove_mean else 0j for y in range(n)]
    rho = time_ft([[train[t][y] - mean[y] for y in range(n)] for t in range(nt)])
    return [[abs(v) ** 2 for v in row] for row in rho]


def unfold_group(a, power, psi, v):
    """P A^H (A P A^H + psi I)^(-1) v for the nc x R matrix a and P = diag(power)."""
    nc, r = len(a), len(power)
    if all(p == 0 for p in power):
        return [0j] * r
    g = [
        [sum(a[i][q] * power[q] * a[j][q].conjugate() for q in range(r)) + (psi if i == j else 0) for j in range(nc)]
        for i in range(nc)
    ]
    w = solve(g, list(v))
    return [power[q] * sum(a[i][q].conjugate() * w[i] for i in range(nc)) for q in range(r)]


# ------------------------------------------------------------------ the method


def k_t_blast(data, mask, r, shift, power, psi, coils=None, baseline=True):
    """Reconstruct the series x[t][y] from lattice data.

    power[f][y] is the prior power in x-f space, usually training_power of a
    low resolution training series. psi >= 0 is the noise variance. With
    baseline=True the time average of the sampled data is removed first and
    added back at the end; the power should then come from a training
    series with its mean removed.
    """
    nt, nc, n = len(data), len(data[0]), len(data[0][0])
    base_k = []  # @line L1
    for c in range(nc):
        acc, cnt = [0j] * n, [0] * n
        for t in range(nt):
            for k in range(n):
                if mask[t][k] and baseline:
                    acc[k] += data[t][c][k]
                    cnt[k] += 1
        base_k.append([a / m if m else 0j for a, m in zip(acc, cnt)])
    diff = [[[(v - b) if m else 0j for v, b, m in zip(data[t][c], base_k[c], mask[t])] for c in range(nc)] for t in range(nt)]  # @line L2
    alias = xf_alias(diff)  # @line L3
    rho = [[0j] * n for _ in range(nt)]
    for group in alias_groups(n, nt, r, shift):  # @line L4
        a = [[(1.0 if coils is None else coils[c][y]) / r for (y, _) in group] for c in range(nc)]  # @line L5
        y0, f0 = group[0]
        est = unfold_group(a, [power[f][y] for (y, f) in group], psi, [alias[c][f0][y0] for c in range(nc)])  # @line L6
        for (y, f), val in zip(group, est):
            rho[f][y] = val
    series = time_ift(rho)  # @line L7
    base_imgs = [_fuh(base_k[c]) for c in range(nc)]
    if coils is None:
        base = base_imgs[0]
    else:
        den = [sum(abs(coils[c][y]) ** 2 for c in range(nc)) for y in range(n)]
        base = [
            sum(coils[c][y].conjugate() * base_imgs[c][y] for c in range(nc)) / den[y] if den[y] > 0 else 0j
            for y in range(n)
        ]
    return [[v + b for v, b in zip(frame, base)] for frame in series]  # @line L8
