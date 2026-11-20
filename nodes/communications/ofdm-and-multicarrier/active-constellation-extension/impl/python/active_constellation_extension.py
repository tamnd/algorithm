# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/active-constellation-extension/. The authors are listed in prov/6XWF0B.jsonl.

"""Active constellation extension (Krongold and Jones) by clipping and projection.

The outer points of a square QAM constellation may move away from the
decision boundaries without any loss: the receiver still decides the same
point, and the distance to every other point can only grow. Each coordinate
at the largest level may grow outward; each inner coordinate stays fixed. The
set of allowed positions of each subcarrier is therefore a convex set (a
quadrant, a half-line or a point), and the projection onto it acts on the
real and imaginary parts separately.

Each iteration clips the oversampled symbol at the magnitude a, takes the
in-band subcarrier values of the clipping noise, adds mu times them to the
current subcarrier values, projects every subcarrier back onto its allowed
set, and forms the new symbol. The symbol stays band-limited, because it is
always the transform of N subcarrier values. The FFT is a radix-2 FFT, so N
and L must be powers of two.
"""

import cmath
import math
from typing import Sequence


def fft(a: Sequence[complex], inverse: bool = False) -> list[complex]:
    """Radix-2 FFT with no scale factor: sum_n a[n] e^(-+ j 2 pi k n / n_len)."""
    n = len(a)
    if n == 0 or n & (n - 1):
        raise ValueError("the length must be a power of two")
    out = [complex(v) for v in a]
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            out[i], out[j] = out[j], out[i]
    sign = 1 if inverse else -1
    size = 2
    while size <= n:
        half = size // 2
        tw = [cmath.exp(sign * 2j * math.pi * k / size) for k in range(half)]
        for s in range(0, n, size):
            for k in range(half):
                u = out[s + k]
                v = out[s + k + half] * tw[k]
                out[s + k] = u + v
                out[s + k + half] = u - v
        size *= 2
    return out


def to_time(X: Sequence[complex], L: int) -> list[complex]:
    """sqrt(L) F^H Z: the OFDM symbol of X oversampled by L, zeros in the middle of the spectrum."""
    n = len(X)
    z = [0j] * (L * n)
    z[: n // 2] = [complex(v) for v in X[: n // 2]]
    z[L * n - n + n // 2:] = [complex(v) for v in X[n // 2:]]
    s = 1.0 / math.sqrt(n)
    return [v * s for v in fft(z, inverse=True)]


def to_bins(x: Sequence[complex], L: int) -> list[complex]:
    """The N in-band subcarrier values of an oversampled symbol: the inverse of to_time."""
    n = len(x) // L
    c = fft(x)
    s = 1.0 / (L * math.sqrt(n))
    return [v * s for v in c[: n // 2] + c[L * n - n // 2:]]


def papr(x: Sequence[complex]) -> float:
    """max |x[m]|^2 over the time average of |x[m]|^2."""
    p = [abs(v) ** 2 for v in x]
    return max(p) / (sum(p) / len(p))


def _project_axis(u: float, u0: float, outer: float, tol: float = 1e-9) -> float:
    """Project the coordinate u onto the allowed set of the original coordinate u0."""
    if abs(abs(u0) - outer) > tol:
        return u0
    if u0 > 0:
        return max(u, u0)
    return min(u, u0)


def project(z: complex, x0: complex, outer: float) -> complex:
    """The nearest point to z in the extension region of the constellation point x0.

    outer is the largest coordinate magnitude of the square constellation.
    """
    return complex(_project_axis(z.real, x0.real, outer), _project_axis(z.imag, x0.imag, outer))


def clip_noise(x: Sequence[complex], a: float) -> list[complex]:
    """clip(x, a) - x: zero where |x| <= a, else the part of x above magnitude a, with a minus sign."""
    return [(a / abs(v) - 1.0) * v if abs(v) > a else 0j for v in x]


def active_constellation_extension(
    X: Sequence[complex], points: Sequence[complex], L: int, a: float, mu: float, iterations: int
) -> tuple[list[complex], list[complex]]:
    """Return the oversampled symbol and the extended subcarrier values.

    Every X[k] is a point of the square constellation points; a is the clipping
    magnitude and mu the step size.
    """
    outer = max(abs(p.real) for p in points)
    Y = [complex(v) for v in X]  # @line L1
    x = to_time(Y, L)  # @line L2
    for _ in range(iterations):  # @line L3
        e = clip_noise(x, a)  # @line L4
        if not any(e):  # @line L5
            break
        E = to_bins(e, L)  # @line L6
        Y = [project(y + mu * d, x0, outer) for y, d, x0 in zip(Y, E, X)]  # @line L7
        x = to_time(Y, L)  # @line L8
    return x, Y  # @line L9
