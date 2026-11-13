# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/time-frequency-uncertainty/. The authors are listed in prov/TQ9C7X.jsonl.

import cmath
import itertools
import math
import random

from time_frequency_uncertainty import (
    dft,
    fourier_transform,
    frequency_moments_by_derivative,
    frequency_moments_by_transform,
    gaussian,
    moments,
    picket_fence,
    support_size,
    time_moments,
    uncertainty_product,
)


def test_gaussian_reaches_one_half_by_numerical_fourier_transform() -> None:
    # sigma_omega comes from |X|^2 with X itself computed by quadrature, not from a formula.
    for a in (0.25, 1.0, 4.0):
        x, _ = gaussian(a)
        t_half = 8 / math.sqrt(a)
        w_half = 12 * math.sqrt(a)
        energy, _, vt = time_moments(x, -t_half, t_half, 400)
        mass, mw, vw = frequency_moments_by_transform(x, -t_half, t_half, 400, w_half, 480)
        assert abs(vt - 1 / (4 * a)) <= 1e-12 / a
        assert abs(vw - a) <= 1e-12 * a
        assert abs(mw) <= 1e-12
        assert abs(math.sqrt(vt * vw) - 0.5) <= 1e-12
        # Plancherel: the spectrum carries 2 pi times the energy
        assert abs(mass - 2 * math.pi * energy) <= 1e-10 * mass


def test_shifted_modulated_gaussian_is_still_extremal() -> None:
    a, t0, w0 = 0.7, 1.5, 3.0
    x, dx = gaussian(a, t0, w0)
    _, mt, vt = time_moments(x, t0 - 9, t0 + 9, 600)
    w = [w0 - 14 + 28 * j / 560 for j in range(561)]
    spectrum = fourier_transform(x, w, t0 - 9, t0 + 9, 600)
    _, mw, vw = moments([abs(v) ** 2 for v in spectrum], w, 28 / 560)
    assert abs(mt - t0) <= 1e-12 and abs(mw - w0) <= 1e-12
    assert abs(math.sqrt(vt * vw) - 0.5) <= 1e-12
    md, vd = frequency_moments_by_derivative(x, dx, t0 - 9, t0 + 9, 600)
    assert abs(md - mw) <= 1e-12 and abs(vd - vw) <= 1e-12


def test_chirped_gaussian_is_strictly_above_the_bound() -> None:
    a = 1.0
    for b in (0.5, 2.0):
        x, dx = gaussian(a, chirp=b)
        _, _, vt = time_moments(x, -6, 6, 1200)
        _, _, vw = frequency_moments_by_transform(x, -6, 6, 1200, 20, 800)
        want = 0.5 * math.sqrt(1 + (b / a) ** 2)
        assert abs(math.sqrt(vt * vw) - want) <= 1e-10
        assert abs(uncertainty_product(x, dx, -6, 6, 1200) - want) <= 1e-10


def test_two_sided_exponential() -> None:
    def x(t: float) -> complex:
        return complex(math.exp(-abs(t)))

    def dx(t: float) -> complex:
        return complex(-math.copysign(1.0, t) * math.exp(-abs(t)))

    # the kink at 0 is a grid node, so Simpson panels do not straddle it
    assert abs(uncertainty_product(x, dx, -30, 30, 6000) - 1 / math.sqrt(2)) <= 1e-7


def test_triangle() -> None:
    def x(t: float) -> complex:
        return complex(max(0.0, 1 - abs(t)))

    def dx(t: float) -> complex:
        # one-sided slopes at the kinks; the grid ends exactly on t = -1 and t = 1
        return complex(-math.copysign(1.0, t) if abs(t) <= 1 else 0.0)

    _, _, vt = time_moments(x, -1, 1, 2000)
    assert abs(vt - 0.1) <= 1e-12
    assert abs(uncertainty_product(x, dx, -1, 1, 2000) - math.sqrt(0.3)) <= 1e-9


def hermite_function(n: int) -> tuple:
    def h(k: int, t: float) -> float:
        a, b = 1.0, 2 * t
        if k == 0:
            return a
        for j in range(1, k):
            a, b = b, 2 * t * b - 2 * j * a
        return b

    def x(t: float) -> complex:
        return complex(h(n, t) * math.exp(-t * t / 2))

    def dx(t: float) -> complex:
        lower = 2 * n * h(n - 1, t) if n else 0.0
        return complex((lower - t * h(n, t)) * math.exp(-t * t / 2))

    return x, dx


def test_hermite_functions_give_n_plus_one_half() -> None:
    for n in range(5):
        x, dx = hermite_function(n)
        assert abs(uncertainty_product(x, dx, -12, 12, 1200) - (n + 0.5)) <= 1e-9
    x, _ = hermite_function(3)
    _, _, vt = time_moments(x, -12, 12, 1200)
    _, _, vw = frequency_moments_by_transform(x, -12, 12, 1200, 12, 600)
    assert abs(math.sqrt(vt * vw) - 3.5) <= 1e-9


def test_box_has_infinite_frequency_spread() -> None:
    # X(omega) = 2 sin(omega / 2) / omega, so the truncated second moment is 4W - 4 sin W.
    for wmax in (10.0, 40.0, 120.0):
        m = 1200
        w = [-wmax + 2 * wmax * j / m for j in range(m + 1)]
        spectrum = fourier_transform(lambda t: 1.0 + 0j, w, -0.5, 0.5, 600)
        second = moments([u * u * abs(v) ** 2 for u, v in zip(w, spectrum)], w, 2 * wmax / m)[0]
        # Simpson in t and in omega, both with steps of about 0.2 radians at the top frequency
        assert abs(second - (4 * wmax - 4 * math.sin(wmax))) <= 3e-5 * wmax


def test_random_signals_respect_the_bound() -> None:
    rng = random.Random(7)
    for _ in range(40):
        terms = [
            (complex(rng.uniform(-1, 1), rng.uniform(-1, 1)), rng.uniform(0.3, 3), rng.uniform(-2, 2), rng.uniform(-3, 3))
            for _ in range(3)
        ]
        parts = [(c, gaussian(a, t0, w0)) for c, a, t0, w0 in terms]

        def x(t: float, parts=parts) -> complex:
            return sum(c * g(t) for c, (g, _) in parts)

        def dx(t: float, parts=parts) -> complex:
            return sum(c * d(t) for c, (_, d) in parts)

        assert uncertainty_product(x, dx, -14, 14, 1400) >= 0.5 - 1e-10


def test_perturbing_the_gaussian_raises_the_product() -> None:
    base = gaussian(1.0)
    bump = gaussian(1.0, t0=0.8)
    previous = 0.5
    for eps in (0.01, 0.05, 0.2):
        def x(t: float, e=eps) -> complex:
            return base[0](t) + e * bump[0](t)

        def dx(t: float, e=eps) -> complex:
            return base[1](t) + e * bump[1](t)

        p = uncertainty_product(x, dx, -10, 10, 1000)
        assert p > previous + 1e-9
        previous = p


def test_discrete_support_bound_exhaustively() -> None:
    # Donoho and Stark: N_t N_f >= N, checked on every nonzero vector with entries in {-1, 0, 1}.
    n = 8
    best = n * n
    for v in itertools.product((-1, 0, 1), repeat=n):
        if any(v):
            p = support_size(v) * support_size(dft(v))
            assert p >= n
            best = min(best, p)
    assert best == n


def test_prime_length_sum_bound_exhaustively() -> None:
    # Tao: for prime N, N_t + N_f >= N + 1.
    n = 7
    for v in itertools.product((-1, 0, 1), repeat=n):
        if any(v):
            assert support_size(v) + support_size(dft(v)) >= n + 1


def test_picket_fences_attain_the_discrete_bound() -> None:
    n = 36
    for spacing in (1, 2, 3, 4, 6, 9, 12, 18, 36):
        v = picket_fence(n, spacing)
        assert support_size(v) == n // spacing
        assert support_size(dft(v)) == spacing
        # a shift and a modulation keep both support sizes
        shifted = [v[(j - 5) % n] * cmath.exp(2j * math.pi * 7 * j / n) for j in range(n)]
        assert support_size(shifted) * support_size(dft(shifted)) == n
