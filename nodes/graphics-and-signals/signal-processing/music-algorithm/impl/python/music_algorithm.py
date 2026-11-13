# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/music-algorithm/. The authors are listed in prov/PF6V7J.jsonl.

"""MUSIC: frequencies of d complex sinusoids in white noise from the noise eigenvectors of a covariance.

The steering vector is a(w) = (1, e^{iw}, ..., e^{i(m-1)w}), w in radians per sample.
The eigen solver is a cyclic complex Jacobi method written here; no library is used.
"""

import cmath
import math
from typing import Sequence


def hermitian_eigen(a: Sequence[Sequence[complex]], tol: float = 1e-14, sweeps: int = 100) -> tuple[list[float], list[list[complex]]]:
    """Eigenvalues (descending) and eigenvectors (as columns of V) of a Hermitian matrix.

    Cyclic Jacobi: each step removes the phase of a[p][q] with a diagonal unitary, then
    zeroes it with a real plane rotation. Cost: O(m^3) per sweep, a few sweeps.
    """
    m = len(a)
    A = [[complex(v) for v in row] for row in a]
    V = [[complex(i == j) for j in range(m)] for i in range(m)]
    scale = math.sqrt(sum(abs(v) ** 2 for row in A for v in row)) or 1.0
    for _ in range(sweeps):
        off = math.sqrt(sum(abs(A[i][j]) ** 2 for i in range(m) for j in range(m) if i != j))
        if off <= tol * scale:
            break
        for p in range(m - 1):
            for q in range(p + 1, m):
                b = A[p][q]
                r = abs(b)
                if r <= 1e-300:
                    continue
                ph = b / r
                for k in range(m):  # column q times conj(ph), row q times ph
                    A[k][q] *= ph.conjugate()
                    V[k][q] *= ph.conjugate()
                for k in range(m):
                    A[q][k] *= ph
                app, aqq = A[p][p].real, A[q][q].real
                theta = (aqq - app) / (2 * r)
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(m):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p], A[k][q] = c * akp - s * akq, s * akp + c * akq
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p], V[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
                for k in range(m):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k], A[q][k] = c * apk - s * aqk, s * apk + c * aqk
                A[p][q] = A[q][p] = 0j
    order = sorted(range(m), key=lambda i: -A[i][i].real)
    values = [A[i][i].real for i in order]
    vectors = [[V[k][i] for i in order] for k in range(m)]
    return values, vectors


def steering(w: float, m: int) -> list[complex]:
    return [cmath.exp(1j * w * k) for k in range(m)]


def sample_covariance(x: Sequence[complex], m: int) -> list[list[complex]]:
    """(1/K) sum of y_t y_t^H over the K = N - m + 1 windows y_t = (x[t], ..., x[t + m - 1])."""
    n = len(x)
    k = n - m + 1
    if m < 1 or k < 1:
        raise ValueError("need 1 <= m <= N")
    R = [[0j] * m for _ in range(m)]
    for t in range(k):
        y = x[t:t + m]
        for i in range(m):
            for j in range(m):
                R[i][j] += y[i] * y[j].conjugate()
    return [[v / k for v in row] for row in R]


def model_covariance(freqs: Sequence[float], powers: Sequence[float], noise: float, m: int) -> list[list[complex]]:
    """The exact covariance sum of P_k a(w_k) a(w_k)^H plus noise times I."""
    R = [[complex(noise if i == j else 0) for j in range(m)] for i in range(m)]
    for w, pw in zip(freqs, powers):
        a = steering(w, m)
        for i in range(m):
            for j in range(m):
                R[i][j] += pw * a[i] * a[j].conjugate()
    return R


def noise_projector(R: Sequence[Sequence[complex]], d: int) -> list[list[complex]]:
    """G G^H for the m - d eigenvectors of the smallest eigenvalues."""
    m = len(R)
    _, U = hermitian_eigen(R)  # @line L1
    G = [row[d:] for row in U]  # @line L2
    return [[sum(G[i][k] * G[j][k].conjugate() for k in range(m - d)) for j in range(m)] for i in range(m)]


def diagonal_sums(P: Sequence[Sequence[complex]]) -> list[complex]:
    """q[k] = sum of P[i][i + k] for k = 0 .. m - 1, so a(w)^H P a(w) = q[0] + 2 Re sum q[k] e^{iwk}."""
    m = len(P)
    return [sum(P[i][i + k] for i in range(m - k)) for k in range(m)]


def null_spectrum(q: Sequence[complex], w: float) -> float:
    """a(w)^H P a(w), the squared norm of G^H a(w), from the diagonal sums of P = G G^H.

    MUSIC's pseudospectrum is its reciprocal. Cost: O(m) per frequency.
    """
    step = cmath.exp(1j * w)
    z = step
    total = q[0].real
    for k in range(1, len(q)):
        total += 2 * (q[k] * z).real
        z *= step
    return total


def pseudospectrum(R: Sequence[Sequence[complex]], d: int, w: float) -> float:
    return 1 / max(null_spectrum(diagonal_sums(noise_projector(R, d)), w), 1e-300)


def music(R: Sequence[Sequence[complex]], d: int, grid: int = 1024, tol: float = 1e-12) -> list[float]:
    """The d frequencies in [-pi, pi) where 1 / ||G^H a(w)||^2 has its highest peaks.

    Precondition: R is Hermitian m x m with d < m. Cost: O(m^3) for the eigenvectors,
    O(grid m) for the search and O(m log(1/tol)) per refinement.
    """
    m = len(R)
    if not 0 < d < m:
        raise ValueError("need 0 < d < m")
    P = diagonal_sums(noise_projector(R, d))
    ws = [-math.pi + 2 * math.pi * i / grid for i in range(grid)]
    vals = [null_spectrum(P, w) for w in ws]  # @line L3
    minima = [i for i in range(grid) if vals[i] <= vals[i - 1] and vals[i] < vals[(i + 1) % grid]]
    minima.sort(key=lambda i: vals[i])
    found = []
    for i in minima[:d]:  # @line L4
        lo, hi = ws[i] - 2 * math.pi / grid, ws[i] + 2 * math.pi / grid
        g = (math.sqrt(5) - 1) / 2
        x1, x2 = hi - g * (hi - lo), lo + g * (hi - lo)
        f1, f2 = null_spectrum(P, x1), null_spectrum(P, x2)
        while hi - lo > tol:  # @line L5
            if f1 < f2:
                hi, x2, f2 = x2, x1, f1
                x1 = hi - g * (hi - lo)
                f1 = null_spectrum(P, x1)
            else:
                lo, x1, f1 = x1, x2, f2
                x2 = lo + g * (hi - lo)
                f2 = null_spectrum(P, x2)
        w = (lo + hi) / 2
        found.append((w + math.pi) % (2 * math.pi) - math.pi)
    return sorted(found)  # @line L6
