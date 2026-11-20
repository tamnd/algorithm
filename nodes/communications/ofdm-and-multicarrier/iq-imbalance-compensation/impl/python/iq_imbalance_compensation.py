# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iq-imbalance-compensation/. The authors are listed in prov/GSXKAS.jsonl.

"""Compensation of receiver IQ imbalance in OFDM, per mirror pair of subcarriers.

The receiver mixes the signal down on two branches. If the I branch is ideal
and the Q branch has gain g and phase error phi, the complex baseband signal
y becomes

    r = Re(y) + j g (Im(y) cos(phi) - Re(y) sin(phi)) = mu y + nu conj(y)
    mu = (1 + g e^(-j phi)) / 2,   nu = (1 - g e^(j phi)) / 2

The DFT of conj(y) at k is conj(Y[-k]), so after the DFT (unitary pair) and
a channel H, subcarrier k sees its mirror -k:

    R[k] = A[k] X[k] + B[k] conj(X[-k]),   A[k] = mu H[k],   B[k] = nu conj(H[-k])

Two training symbols T1 and T2 give two equations per k, which a 2x2 solve
turns into A[k] and B[k]. Data on the pair (k, -k) then follows from

    [ A[k]        B[k]       ] [ X[k]        ]   [ R[k]        ]
    [ conj(B[-k]) conj(A[-k])] [ conj(X[-k]) ] = [ conj(R[-k]) ]

Subcarrier 0 (DC) and N/2 are their own mirrors and carry no data here.
Indices are taken modulo N, so -k is N - k.
"""

import cmath

import cbb


def mu_nu(g: float, phi: float) -> tuple[complex, complex]:
    """mu and nu for Q-branch gain g and phase error phi (radians)."""
    return (1 + g * cmath.exp(-1j * phi)) / 2, (1 - g * cmath.exp(1j * phi)) / 2


def impair(y: list[complex], g: float, phi: float) -> list[complex]:
    """Apply the imbalance to time samples: r = mu y + nu conj(y)."""
    mu, nu = mu_nu(g, phi)
    return [mu * v + nu * v.conjugate() for v in y]


def estimate(r1: list[complex], r2: list[complex], t1: list[complex], t2: list[complex]) -> tuple[list[complex], list[complex]]:
    """A[k] and B[k] for k != 0, N/2 from two received training symbols (after the DFT)."""
    n = len(r1)
    a = [0j] * n
    b = [0j] * n
    for k in range(1, n):
        if 2 * k == n:
            continue
        m = (n - k) % n
        mat = [[t1[k], t1[m].conjugate()], [t2[k], t2[m].conjugate()]]  # @line L1
        a[k], b[k] = cbb.solve(mat, [r1[k], r2[k]])  # @line L2
    return a, b


def compensate(r: list[complex], a: list[complex], b: list[complex]) -> list[complex]:
    """The data estimates X[k] for k != 0, N/2 (zero there), solving each mirror pair."""
    n = len(r)
    x = [0j] * n
    for k in range(1, n):
        if 2 * k == n:
            continue
        m = n - k
        mat = [[a[k], b[k]], [b[m].conjugate(), a[m].conjugate()]]  # @line L3
        x[k], _ = cbb.solve(mat, [r[k], r[m].conjugate()])  # @line L4
    return x  # @line L5


def image_coefficient(a: list[complex], b: list[complex]) -> complex:
    """c = nu / conj(mu), from the mean of B[k] / conj(A[-k]) over the used k.

    In the time domain z = r - c conj(r) equals (mu - |nu|^2 / conj(mu)) y, with no image.
    """
    n = len(a)
    ks = [k for k in range(1, n) if 2 * k != n]
    return sum(b[k] / a[n - k].conjugate() for k in ks) / len(ks)
