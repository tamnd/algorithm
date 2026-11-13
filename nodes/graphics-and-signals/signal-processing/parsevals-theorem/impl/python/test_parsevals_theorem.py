# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parsevals-theorem/. The authors are listed in prov/3S9P1H.jsonl.

import cmath
import math
import random
from fractions import Fraction

from parsevals_theorem import autocorrelation, dtft, energy, frequency_mean, inner, spectral_energy


def simpson_mean(g, n: int = 2000) -> float:
    """(1/(2 pi)) times the integral of g over [-pi, pi], by composite Simpson."""
    h = 2 * math.pi / n
    total = 0.0
    for j in range(n + 1):
        w = 1 if j in (0, n) else (4 if j % 2 else 2)
        total += w * g(-math.pi + j * h)
    return total * h / 3 / (2 * math.pi)


def fold(x, m):
    y = [0] * m
    for k, v in enumerate(x):
        y[k % m] += v
    return y


def random_sequence(rng: random.Random, n: int) -> list[complex]:
    return [complex(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(n)]


def test_energy_matches_the_integral_by_simpson() -> None:
    rng = random.Random(1)
    for n in range(1, 9):
        x = random_sequence(rng, n)
        want = energy(x)
        got = simpson_mean(lambda w: abs(dtft(x, w)) ** 2)
        assert abs(got - want) <= 1e-9 * want


def test_trapezoid_is_exact_once_m_reaches_the_length() -> None:
    rng = random.Random(2)
    for n in range(1, 13):
        x = random_sequence(rng, n)
        for m in range(n, n + 4):
            assert abs(spectral_energy(x, m) - energy(x)) <= 1e-9 * energy(x)


def test_too_few_frequencies_measure_the_folded_energy() -> None:
    # Below m = len(x) the mean of |X|^2 at the m bins is the energy of the folded
    # sequence, which is the sum of r[d] over the multiples d of m, computed exactly.
    rng = random.Random(3)
    for n in range(2, 11):
        x = [Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(n)]
        for m in range(1, n):
            exact = sum(autocorrelation(x, d) for d in range(-(n - 1), n) if d % m == 0)
            assert exact == energy(fold(x, m))
            got = spectral_energy([float(v) for v in x], m)
            assert abs(got - float(exact)) <= 1e-9 * (1 + abs(float(exact)))


def test_inner_products_are_kept() -> None:
    rng = random.Random(4)
    for n in range(1, 8):
        x = random_sequence(rng, n)
        y = random_sequence(rng, n)
        want = inner(x, y)
        got = sum(dtft(x, 2 * math.pi * k / n) * dtft(y, 2 * math.pi * k / n).conjugate() for k in range(n)) / n
        assert abs(got - want) <= 1e-9 * (1 + abs(want))


def test_autocorrelation_is_the_inverse_dtft_of_the_power() -> None:
    x = [Fraction(1), Fraction(2), Fraction(0), Fraction(-1)]
    r = {d: autocorrelation(x, d) for d in range(-3, 4)}
    assert r[0] == 6 and r[1] == 2 and r[2] == -2 and r[3] == -1 and r[-1] == 2
    for d in range(-3, 4):
        got = frequency_mean(lambda w: (abs(dtft([1, 2, 0, -1], w)) ** 2 * cmath.exp(1j * w * d)).real, 8)
        assert abs(got - float(r[d])) <= 1e-12


def test_geometric_sequence() -> None:
    # x[n] = a^n, n >= 0: energy 1 / (1 - a^2) and |X|^2 = 1 / (1 - 2 a cos w + a^2).
    for a in (0.1, 0.5, 0.9, -0.7):
        want = 1 / (1 - a * a)
        got = frequency_mean(lambda w: 1 / (1 - 2 * a * math.cos(w) + a * a), 400)
        assert abs(got - want) <= 1e-12 * want


def test_ideal_lowpass_energy() -> None:
    # h[n] = sin(wc n) / (pi n) has energy wc / pi; the tail beyond |n| = N is below 2 / (pi^2 N).
    for wc in (0.5, 1.0, 2.0):
        n_max = 4000
        partial = (wc / math.pi) ** 2 + 2 * sum((math.sin(wc * n) / (math.pi * n)) ** 2 for n in range(1, n_max + 1))
        assert 0 <= wc / math.pi - partial <= 2 / (math.pi**2 * n_max)


def test_basel_sum() -> None:
    # X(w) = w on (-pi, pi) has x[0] = 0 and |x[n]| = 1 / n, so the sum of 2 / n^2 is pi^2 / 3.
    n_max = 100000
    partial = sum(2.0 / (n * n) for n in range(1, n_max + 1))
    want = simpson_mean(lambda w: w * w)
    assert abs(want - math.pi**2 / 3) <= 1e-12
    assert 0 <= want - partial <= 2.0 / n_max


def test_filter_output_energy() -> None:
    rng = random.Random(5)
    h = [rng.uniform(-1, 1) for _ in range(5)]
    x = [rng.uniform(-1, 1) for _ in range(9)]
    y = [sum(h[i] * x[k - i] for i in range(len(h)) if 0 <= k - i < len(x)) for k in range(len(h) + len(x) - 1)]
    got = frequency_mean(lambda w: abs(dtft(h, w)) ** 2 * abs(dtft(x, w)) ** 2, len(y))
    assert abs(got - energy(y)) <= 1e-9 * energy(y)


def test_other_powers_are_not_kept() -> None:
    # For x = (1, 1), |X|^2 = 2 + 2 cos w; the fourth powers give 2 in time and 6 in frequency.
    x = [1.0, 1.0]
    assert sum(abs(v) ** 4 for v in x) == 2
    assert abs(frequency_mean(lambda w: abs(dtft(x, w)) ** 4, 8) - 6) <= 1e-12
