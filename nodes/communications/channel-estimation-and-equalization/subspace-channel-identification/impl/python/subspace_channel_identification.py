# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subspace-channel-identification/. The authors are listed in prov/8ZFGWM.jsonl.

"""Subspace blind identification of a single-input multiple-output FIR channel.

The channel has P outputs (P samples per symbol, or P antennas) and L taps:
y[k] = sum_l h(l) a[k-l] + w[k], with h(l) a vector of length P. The
stacked vector h = (h(0); h(1); ...; h(L-1)) has length P L, so h[l*P + p]
is tap l of subchannel p.

A window of N output vectors Y[k] = (y[k]; y[k-1]; ...; y[k-N+1]) is
H_N (a[k], ..., a[k-N-L+2]) + noise, where H_N is the P N by (N + L - 1)
block Toeplitz matrix whose block (i, m) is h(m - i). If the subchannels
have no common zero and N >= L, H_N has full column rank. Every vector g of
the noise subspace of R = E[Y Y^H] then satisfies g^H H_N = 0, which is a
set of linear equations in h. Their least squares solution with |h| = 1 is
the eigenvector of the smallest eigenvalue of Q = sum_g G(g)^H G(g).

The Hermitian eigenproblems are solved by the cyclic Jacobi method on the
real symmetric matrix [[B, -C], [C, B]] of A = B + j C.
"""

import math


def jacobi_eigh(a: list[list[float]], tol: float = 1e-14, sweeps: int = 100) -> tuple[list[float], list[list[float]]]:
    """Eigenvalues (ascending) and eigenvectors (as lists) of a real symmetric matrix, by cyclic Jacobi rotations."""
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
    """Eigenvalues (ascending) and eigenvectors of a Hermitian matrix A = B + j C.

    The real matrix [[B, -C], [C, B]] has each eigenvalue of A twice; an
    eigenvector (x; y) of it gives the eigenvector x + j y of A. The result
    has 2 n entries: each eigenvalue of A appears twice, with eigenvectors u
    and j u (up to rotation within the pair).
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
    return vals, [[complex(v[i], v[i + n]) for i in range(n)] for v in vecs]


def block_toeplitz(h: list[complex], p: int, n: int) -> list[list[complex]]:
    """The P N by (N + L - 1) matrix H_N, with block (i, m) equal to h(m - i)."""
    taps = len(h) // p
    cols = n + taps - 1
    out = [[0j] * cols for _ in range(p * n)]
    for i in range(n):
        for l in range(taps):
            for q in range(p):
                out[i * p + q][i + l] = complex(h[l * p + q])
    return out


def stack(y: list[list[complex]], n: int) -> list[list[complex]]:
    """The windows Y[k] = (y[k]; y[k-1]; ...; y[k-N+1]) for k = N-1, ..., len(y)-1."""
    return [[complex(v) for i in range(n) for v in y[k - i]] for k in range(n - 1, len(y))]


def sample_covariance(windows: list[list[complex]]) -> list[list[complex]]:
    """(1/K) sum of Y Y^H over the windows."""
    d = len(windows[0])
    r = [[0j] * d for _ in range(d)]
    for w in windows:
        wc = [v.conjugate() for v in w]
        for i in range(d):
            wi, ri = w[i], r[i]
            for k in range(d):
                ri[k] += wi * wc[k]
    k = len(windows)
    return [[v / k for v in row] for row in r]


def subspace_identify(r: list[list[complex]], p: int, taps: int, n: int) -> list[complex]:
    """Estimate h (length P L, unit norm, up to a complex scalar) from the covariance R of the windows of N outputs."""
    if p < 2 or taps < 1 or n < taps or len(r) != p * n:
        raise ValueError("need P >= 2, N >= L and R of size P N")
    k_noise = p * n - (n + taps - 1)
    if k_noise < 1:
        raise ValueError("no noise subspace: need P N > N + L - 1")
    vals, vecs = hermitian_eigh(r)  # @line L2
    noise = vecs[: 2 * k_noise]  # @line L2
    q = [[0j] * (p * taps) for _ in range(p * taps)]  # @line L3
    for g in noise:  # @line L4
        blocks = [g[i * p : (i + 1) * p] for i in range(n)]
        for m in range(n + taps - 1):  # @line L5
            row = [0j] * (p * taps)  # @line L5
            for l in range(taps):  # @line L5
                if 0 <= m - l < n:  # @line L5
                    for s in range(p):  # @line L5
                        row[l * p + s] = blocks[m - l][s].conjugate()  # @line L5
            rc = [v.conjugate() for v in row]  # @line L6
            for i in range(p * taps):  # @line L6
                for k in range(p * taps):  # @line L6
                    q[i][k] += rc[i] * row[k]  # @line L6
    qvals, qvecs = hermitian_eigh(q)  # @line L7
    h = qvecs[0]  # @line L7
    norm = math.sqrt(sum(abs(v) ** 2 for v in h))  # @line L7
    return [v / norm for v in h]  # @line L8


def identify_from_samples(y: list[list[complex]], p: int, taps: int, n: int) -> list[complex]:
    """Form the sample covariance of the windows (line L1) and run subspace_identify."""
    r = sample_covariance(stack(y, n))  # @line L1
    return subspace_identify(r, p, taps, n)


def q_eigenvalues(r: list[list[complex]], p: int, taps: int, n: int) -> list[float]:
    """The eigenvalues of Q (each twice, ascending), to test identifiability."""
    k_noise = p * n - (n + taps - 1)
    vals, vecs = hermitian_eigh(r)
    q = [[0j] * (p * taps) for _ in range(p * taps)]
    for g in vecs[: 2 * k_noise]:
        blocks = [g[i * p : (i + 1) * p] for i in range(n)]
        for m in range(n + taps - 1):
            row = [0j] * (p * taps)
            for l in range(taps):
                if 0 <= m - l < n:
                    for s in range(p):
                        row[l * p + s] = blocks[m - l][s].conjugate()
            for i in range(p * taps):
                for k in range(p * taps):
                    q[i][k] += row[i].conjugate() * row[k]
    return hermitian_eigh(q)[0]
