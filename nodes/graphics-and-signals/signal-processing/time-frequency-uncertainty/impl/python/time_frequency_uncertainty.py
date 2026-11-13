# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/time-frequency-uncertainty/. The authors are listed in prov/TQ9C7X.jsonl.

"""Numerical time and frequency spreads, and the discrete support uncertainty.

A signal is a callable x(t) returning a complex number. Its Fourier transform
is X(omega) = integral of x(t) e^(-i omega t) dt, omega in radians per unit
time. The spreads are the standard deviations of the densities |x(t)|^2 and
|X(omega)|^2, normalized to total mass one. Heisenberg-Gabor says
sigma_t sigma_omega >= 1/2, with equality exactly for modulated, shifted
Gaussians C exp(-a (t - t0)^2) exp(i omega0 t), a > 0.
"""

import cmath
import math
from typing import Callable, Sequence

Signal = Callable[[float], complex]


def simpson(values: Sequence[float | complex], h: float) -> float | complex:
    """Composite Simpson rule on equally spaced values (an odd number of them)."""
    n = len(values) - 1
    if n < 2 or n % 2:
        raise ValueError("Simpson needs an even number of intervals")
    s = values[0] + values[-1] + 4 * sum(values[1:n:2]) + 2 * sum(values[2:n:2])
    return s * h / 3


def _nodes(a: float, b: float, n: int) -> tuple[list[float], float]:
    h = (b - a) / n
    return [a + j * h for j in range(n + 1)], h


def moments(density: Sequence[float], nodes: Sequence[float], h: float) -> tuple[float, float, float]:
    """Return (mass, mean, variance) of a sampled nonnegative density by Simpson."""
    mass = simpson(density, h)
    mean = simpson([u * d for u, d in zip(nodes, density)], h) / mass
    var = simpson([(u - mean) ** 2 * d for u, d in zip(nodes, density)], h) / mass
    return mass, mean, var


def time_moments(x: Signal, a: float, b: float, n: int) -> tuple[float, float, float]:
    """Energy, mean time and time variance of x on [a, b] with n intervals."""
    t, h = _nodes(a, b, n)
    return moments([abs(x(u)) ** 2 for u in t], t, h)


def fourier_transform(x: Signal, omegas: Sequence[float], a: float, b: float, n: int) -> list[complex]:
    """X(omega) = integral over [a, b] of x(t) e^(-i omega t) dt, by Simpson, at each omega."""
    t, h = _nodes(a, b, n)
    xs = [x(u) for u in t]
    return [simpson([v * cmath.exp(-1j * w * u) for v, u in zip(xs, t)], h) for w in omegas]


def frequency_moments_by_transform(
    x: Signal, a: float, b: float, n: int, wmax: float, m: int
) -> tuple[float, float, float]:
    """Mass, mean and variance of |X(omega)|^2 on [-wmax, wmax], X computed by quadrature."""
    w, h = _nodes(-wmax, wmax, m)
    spectrum = fourier_transform(x, w, a, b, n)
    return moments([abs(v) ** 2 for v in spectrum], w, h)


def frequency_moments_by_derivative(x: Signal, dx: Signal, a: float, b: float, n: int) -> tuple[float, float]:
    """Mean and variance of |X|^2 from x and x' alone, by Plancherel.

    Since x' has transform i omega X, the mean frequency is
    Im(integral of conj(x) x') / energy and the variance is
    integral of |x' - i mean x|^2 / energy.
    """
    t, h = _nodes(a, b, n)
    xs = [x(u) for u in t]
    ds = [dx(u) for u in t]
    energy = simpson([abs(v) ** 2 for v in xs], h)
    mean = simpson([v.conjugate() * d for v, d in zip(xs, ds)], h).imag / energy
    var = simpson([abs(d - 1j * mean * v) ** 2 for v, d in zip(xs, ds)], h) / energy
    return mean, var


def uncertainty_product(x: Signal, dx: Signal, a: float, b: float, n: int) -> float:
    """sigma_t sigma_omega with sigma_omega from the derivative form."""
    _, _, vt = time_moments(x, a, b, n)
    _, vw = frequency_moments_by_derivative(x, dx, a, b, n)
    return math.sqrt(vt * vw)


def gaussian(a: float, t0: float = 0.0, w0: float = 0.0, chirp: float = 0.0) -> tuple[Signal, Signal]:
    """exp(-(a - i chirp)(t - t0)^2 + i w0 t) and its derivative."""
    c = complex(a, -chirp)

    def x(t: float) -> complex:
        return cmath.exp(-c * (t - t0) ** 2 + 1j * w0 * t)

    def dx(t: float) -> complex:
        return (-2 * c * (t - t0) + 1j * w0) * x(t)

    return x, dx


def dft(v: Sequence[complex]) -> list[complex]:
    """Direct DFT, X_k = sum of v[j] e^(-2 pi i j k / N)."""
    n = len(v)
    return [sum(v[j] * cmath.exp(-2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def support_size(v: Sequence[complex], tol: float = 1e-9) -> int:
    """Number of entries with magnitude above tol."""
    return sum(1 for z in v if abs(z) > tol)


def picket_fence(n: int, spacing: int) -> list[float]:
    """1 at multiples of spacing, 0 elsewhere; spacing must divide n."""
    if n % spacing:
        raise ValueError("spacing must divide n")
    return [1.0 if j % spacing == 0 else 0.0 for j in range(n)]
