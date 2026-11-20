# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parabolic-radon-transform/. The authors are listed in prov/5J6KMF.jsonl.
"""The least-squares parabolic Radon transform and its use for multiple removal.

A gather is a list of traces d[i] (offset x_i), each with n samples at k * dt.
A model is a list of traces m[j] (curvature q_j in s/m^2) with n samples at
tau = k * dt. The forward operator sums the model along parabolas,

    d(t, x_i) = sum_j m(t - q_j x_i^2, q_j),

with the time shifts done exactly in the frequency domain on a periodic time
axis. For each frequency w_k = 2 pi k' / (n dt) (k' the signed index) it is
the matrix L_k[i][j] = exp(-1j w_k q_j x_i^2), and the damped least-squares
model is M_k = (L_k^H L_k + mu I)^(-1) L_k^H D_k. Use an odd n: then there is
no Nyquist bin, a real model gives real data, and the shifts are exact.
"""

import cmath
import math

import imgkit as ik
import imgla as la


def omega(k, n, dt):
    """The angular frequency of DFT bin k (signed index k or k - n)."""
    ks = k if k <= n // 2 else k - n
    return 2.0 * math.pi * ks / (n * dt)


def operator_matrix(w, offsets, qs):
    """L[i][j] = exp(-1j w q_j x_i^2)."""
    return [[cmath.exp(-1j * w * q * x * x) for q in qs] for x in offsets]


def _spectra(traces):
    return [ik.dft(tr) for tr in traces]


def _traces(spectra):
    return [[v.real for v in ik.idft(sp)] for sp in spectra]


def forward(m, offsets, qs, dt):
    """d = L m: sum the model traces along the parabolas t = tau + q x^2."""
    n = len(m[0])
    mf = _spectra(m)
    df = [[0j] * n for _ in offsets]
    for k in range(n):
        lk = operator_matrix(omega(k, n, dt), offsets, qs)
        col = la.matvec(lk, [mf[j][k] for j in range(len(qs))])
        for i in range(len(offsets)):
            df[i][k] = col[i]
    return _traces(df)


def adjoint(d, offsets, qs, dt):
    """m = L^T d: the plain parabolic stack (sum the data along each parabola)."""
    n = len(d[0])
    dfs = _spectra(d)
    mf = [[0j] * n for _ in qs]
    for k in range(n):
        lk = operator_matrix(omega(k, n, dt), offsets, qs)
        col = la.rmatvec(lk, [dfs[i][k] for i in range(len(offsets))])
        for j in range(len(qs)):
            mf[j][k] = col[j]
    return _traces(mf)


def demultiple(d, offsets, qs, dt, mu, q_cut):
    """Least-squares parabolic Radon transform and multiple removal.

    d must be NMO-corrected with the primary velocity, so the primaries are
    flat (q near 0) and the multiples curve down (q > 0). Returns
    (m, primaries, multiples): the model, d minus the predicted multiples,
    and the predicted multiples (built from the model at q_j > q_cut).
    """
    n = len(d[0])
    nq = len(qs)
    dfs = _spectra(d)  # @line L1
    mf = [[0j] * n for _ in qs]
    mulf = [[0j] * n for _ in offsets]
    for k in range(n):  # @line L2
        lk = operator_matrix(omega(k, n, dt), offsets, qs)  # @line L3
        dk = [dfs[i][k] for i in range(len(offsets))]
        lh = la.conj_transpose(lk)
        normal = la.matmul(lh, lk)
        for j in range(nq):
            normal[j][j] += mu
        mk = la.solve(normal, la.matvec(lh, dk))  # @line L4
        keep = [mk[j] if qs[j] > q_cut else 0j for j in range(nq)]  # @line L5
        dmul = la.matvec(lk, keep)  # @line L6
        for j in range(nq):
            mf[j][k] = mk[j]
        for i in range(len(offsets)):
            mulf[i][k] = dmul[i]
    m = _traces(mf)  # @line L7
    multiples = _traces(mulf)
    primaries = [[a - b for a, b in zip(tr, mt)] for tr, mt in zip(d, multiples)]
    return m, primaries, multiples  # @line L8


def residual_moveout(t0, x, v_primary, v_multiple):
    """Exact residual time of a multiple after NMO with the primary velocity.

    The multiple arrives at sqrt(t0^2 + x^2 / v_multiple^2); NMO with
    v_primary maps it to sqrt(t0^2 + x^2 (1 / v_multiple^2 - 1 / v_primary^2)).
    """
    return math.sqrt(t0 * t0 + x * x * (1.0 / v_multiple ** 2 - 1.0 / v_primary ** 2)) - t0


def parabolic_curvature(t0, v_primary, v_multiple):
    """q = (1 / v_multiple^2 - 1 / v_primary^2) / (2 t0), the small-offset parabola."""
    return (1.0 / v_multiple ** 2 - 1.0 / v_primary ** 2) / (2.0 * t0)
