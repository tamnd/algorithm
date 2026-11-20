# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tong-xu-kailath-identification/. The authors are listed in prov/WX9EA1.jsonl.

"""Tong-Xu-Kailath blind identification from the correlations at lags 0 and 1.

The channel has P outputs and L taps: y[k] = sum_l h(l) a[k-l] + w[k], with
h(l) a vector of length P, white symbols of unit power and white noise of
power sigma^2. The stacked channel h = (h(0); ...; h(L-1)) has length P L,
so h[l*P + p] is tap l of subchannel p.

The window Y[k] = (y[k]; ...; y[k-N+1]) is H_N s[k] + noise, with the
block Toeplitz H_N (block (i, m) = h(m - i)) and s[k] = (a[k], ..., a[k-N-L+2]).
Its correlations are
    R(0) = E[Y[k] Y[k]^H]   = H_N H_N^H + sigma^2 I,
    R(1) = E[Y[k] Y[k-1]^H] = H_N J H_N^H + sigma^2 (J_N kron I_P),
where J is the shift with ones just below the diagonal. With no common zero
of the subchannels and N >= L, H_N has full column rank d = N + L - 1. Then
F = Lambda^(-1/2) U^H from the d nonzero eigenpairs of R(0) - sigma^2 I
makes V = F H_N unitary, M = F (R(1) - sigma^2 J_N kron I_P) F^H = V J V^H,
the first column v_0 of V spans the null space of M^H, the next columns are
v_l = M^l v_0, and h(l) is block 0 of U Lambda^(1/2) v_l.
"""

import math


def jacobi_eigh(a: list[list[float]], tol: float = 1e-14, sweeps: int = 100) -> tuple[list[float], list[list[float]]]:
    """Eigenvalues (ascending) and eigenvectors of a real symmetric matrix, by cyclic Jacobi rotations."""
    n = len(a)
    m = [list(map(float, r)) for r in a]
    v = [[1.0 if i == k else 0.0 for k in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(m[i][k] ** 2 for i in range(n) for k in range(n) if i != k)
        if off <= tol * tol * max(1.0, sum(m[i][i] ** 2 for i in range(n))):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if m[p][q] == 0.0:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for r in range(n):
                    mrp, mrq = m[r][p], m[r][q]
                    m[r][p], m[r][q] = c * mrp - s * mrq, s * mrp + c * mrq
                for r in range(n):
                    mpr, mqr = m[p][r], m[q][r]
                    m[p][r], m[q][r] = c * mpr - s * mqr, s * mpr + c * mqr
                for r in range(n):
                    vrp, vrq = v[r][p], v[r][q]
                    v[r][p], v[r][q] = c * vrp - s * vrq, s * vrp + c * vrq
    order = sorted(range(n), key=lambda i: m[i][i])
    return [m[i][i] for i in order], [[v[r][i] for r in range(n)] for i in order]


def hermitian_eigh(a: list[list[complex]]) -> tuple[list[float], list[list[complex]]]:
    """Eigenpairs of a Hermitian matrix, one per eigenvalue, ascending, with orthonormal eigenvectors.

    The real form [[B, -C], [C, B]] of A = B + j C has each eigenvalue twice.
    The pairs are split by Gram-Schmidt: a complex vector is kept only if it
    is not in the span of the vectors kept so far.
    """
    n = len(a)
    big = [[0.0] * (2 * n) for _ in range(2 * n)]
    for i in range(n):
        for k in range(n):
            b, c = complex(a[i][k]).real, complex(a[i][k]).imag
            big[i][k] = b
            big[i + n][k + n] = b
            big[i][k + n] = -c
            big[i + n][k] = c
    vals, vecs = jacobi_eigh(big)
    out_vals, out_vecs = [], []
    for lam, v in zip(vals, vecs):
        u = [complex(v[i], v[i + n]) for i in range(n)]
        for w in out_vecs:
            ip = sum(x.conjugate() * y for x, y in zip(w, u))
            u = [y - ip * x for x, y in zip(w, u)]
        nu = math.sqrt(sum(abs(x) ** 2 for x in u))
        if nu > 0.5 and len(out_vecs) < n:
            out_vals.append(lam)
            out_vecs.append([x / nu for x in u])
    return out_vals, out_vecs


def block_toeplitz(h: list[complex], p: int, n: int) -> list[list[complex]]:
    """The P N by (N + L - 1) matrix H_N, with block (i, m) equal to h(m - i)."""
    taps = len(h) // p
    out = [[0j] * (n + taps - 1) for _ in range(p * n)]
    for i in range(n):
        for l in range(taps):
            for q in range(p):
                out[i * p + q][i + l] = complex(h[l * p + q])
    return out


def correlations(y: list[list[complex]], n: int) -> tuple[list[list[complex]], list[list[complex]]]:
    """Sample estimates of R(0) = E[Y[k] Y[k]^H] and R(1) = E[Y[k] Y[k-1]^H] from the windows of N outputs."""
    wins = [[complex(v) for i in range(n) for v in y[k - i]] for k in range(n - 1, len(y))]
    d = len(wins[0])
    r0 = [[0j] * d for _ in range(d)]
    r1 = [[0j] * d for _ in range(d)]
    for t in range(len(wins)):
        w = wins[t]
        wc = [v.conjugate() for v in w]
        for i in range(d):
            for k in range(d):
                r0[i][k] += w[i] * wc[k]
        if t > 0:
            pc = [v.conjugate() for v in wins[t - 1]]
            for i in range(d):
                for k in range(d):
                    r1[i][k] += w[i] * pc[k]
    k0, k1 = len(wins), len(wins) - 1
    return [[v / k0 for v in r] for r in r0], [[v / k1 for v in r] for r in r1]


def txk_identify(
    r0: list[list[complex]], r1: list[list[complex]], p: int, taps: int, n: int, sigma2: float | None = None
) -> list[complex]:
    """Estimate h (length P L, up to a unit complex scalar) from R(0) and R(1) of windows of N outputs.

    If sigma2 is None, it is estimated as the mean of the P N - (N + L - 1) smallest eigenvalues of R(0).
    """
    d = n + taps - 1
    dim = p * n
    if p < 2 or taps < 1 or n < taps or len(r0) != dim or len(r1) != dim or dim <= d:
        raise ValueError("need P >= 2, N >= L, P N > N + L - 1 and R of size P N")
    if sigma2 is None:
        vals0, _ = hermitian_eigh(r0)
        sigma2 = sum(vals0[: dim - d]) / (dim - d)
    a0 = [[r0[i][k] - (sigma2 if i == k else 0) for k in range(dim)] for i in range(dim)]  # @line L1
    a1 = [[r1[i][k] - (sigma2 if i == k + p else 0) for k in range(dim)] for i in range(dim)]  # @line L1
    vals, vecs = hermitian_eigh(a0)  # @line L2
    lam, us = vals[dim - d :], vecs[dim - d :]  # @line L2
    if min(lam) <= 0:
        raise ValueError("R(0) - sigma^2 I has fewer than N + L - 1 positive eigenvalues")
    f = [[us[r][i].conjugate() / math.sqrt(lam[r]) for i in range(dim)] for r in range(d)]  # @line L3
    fa = [[sum(f[r][i] * a1[i][k] for i in range(dim)) for k in range(dim)] for r in range(d)]  # @line L4
    m = [[sum(fa[r][k] * f[c][k].conjugate() for k in range(dim)) for c in range(d)] for r in range(d)]  # @line L4
    mmh = [[sum(m[r][k] * m[c][k].conjugate() for k in range(d)) for c in range(d)] for r in range(d)]  # @line L5
    v = hermitian_eigh(mmh)[1][0]  # @line L5
    h = []
    for _ in range(taps):  # @line L6
        col = [sum(us[r][i] * math.sqrt(lam[r]) * v[r] for r in range(d)) for i in range(p)]  # @line L7
        h.extend(col)  # @line L7
        v = [sum(m[r][c] * v[c] for c in range(d)) for r in range(d)]  # @line L8
    return h  # @line L9
