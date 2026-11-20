# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gerchberg-saxton-algorithm/. The authors are listed in prov/QDZSDB.jsonl.

import cmath
import math
import random

from gerchberg_saxton_algorithm import (
    fourier_error,
    fourier_projection,
    gerchberg_saxton,
    object_error,
    with_magnitude,
)
from imgkit import dft, idft


def dist(a, b):
    return math.sqrt(sum(abs(x - y) ** 2 for x, y in zip(a, b)))


def dist_up_to_phase(g, f):
    """min over c with |c| = 1 of ||g - c f||."""
    ip = sum(x.conjugate() * y for x, y in zip(f, g))
    c = ip / abs(ip) if abs(ip) > 0 else 1.0
    return dist(g, [c * v for v in f])


def problem(seed, n=16, k=8):
    """A complex signal with k nonzero entries, padded with zeros to length n."""
    rng = random.Random(seed)
    f = [rng.uniform(0.5, 1.5) * cmath.exp(1j * rng.uniform(-math.pi, math.pi)) if j < k else 0j
         for j in range(n)]
    mag = [abs(v) for v in f]
    amp = [abs(v) for v in dft(f)]
    return f, mag, amp


def test_fourier_projection_is_a_nearest_point() -> None:
    rng = random.Random(1)
    _, _, amp = problem(1)
    g = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(16)]
    p = fourier_projection(g, amp)
    assert max(abs(abs(v) - a) for v, a in zip(dft(p), amp)) < 1e-9
    d0 = dist(g, p)
    assert abs(d0 - fourier_error(g, amp)) < 1e-9
    for _ in range(100):
        other = idft([a * cmath.exp(1j * rng.uniform(0, 2 * math.pi)) for a in amp])
        assert dist(g, other) >= d0 - 1e-9


def test_object_projection_is_a_nearest_point() -> None:
    rng = random.Random(2)
    _, mag, _ = problem(2)
    g = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(16)]
    p = with_magnitude(g, mag)
    d0 = dist(g, p)
    assert abs(d0 - object_error(g, mag)) < 1e-12
    for _ in range(100):
        other = [m * cmath.exp(1j * rng.uniform(0, 2 * math.pi)) for m in mag]
        assert dist(g, other) >= d0 - 1e-12


def test_true_signal_is_a_fixed_point() -> None:
    f, mag, amp = problem(3)
    g, errors = gerchberg_saxton(mag, amp, [cmath.phase(v) for v in f], 3)
    assert dist(g, f) < 1e-9
    assert max(errors) < 1e-9


def test_error_never_increases() -> None:
    rng = random.Random(4)
    for seed in (5, 6, 7):
        _, mag, amp = problem(seed)
        phase0 = [rng.uniform(-math.pi, math.pi) for _ in range(16)]
        _, errors = gerchberg_saxton(mag, amp, phase0, 60)
        for e0, e1 in zip(errors, errors[1:]):
            assert e1 <= e0 + 1e-10
        assert errors[-1] < errors[0]


def test_error_sandwich_of_one_step() -> None:
    rng = random.Random(8)
    _, mag, amp = problem(9)
    g = [m * cmath.exp(1j * rng.uniform(-math.pi, math.pi)) for m in mag]
    for _ in range(5):
        gp = fourier_projection(g, amp)
        e_f = fourier_error(g, amp)
        e_0 = object_error(gp, mag)
        g_next = with_magnitude(gp, mag)
        assert fourier_error(g_next, amp) <= e_0 + 1e-10
        assert e_0 <= e_f + 1e-10
        g = g_next


def test_consistent_pair_from_a_nearby_start() -> None:
    # Known answer: a consistent pair (mag, amp) of a zero padded signal and a start
    # within 0.3 rad of the true phase. The result must match f up to a global phase.
    rng = random.Random(10)
    for seed in (11, 12, 13):
        f, mag, amp = problem(seed)
        phase0 = [cmath.phase(v) + rng.uniform(-0.3, 0.3) for v in f]
        g, errors = gerchberg_saxton(mag, amp, phase0, 250)
        assert errors[-1] < 1e-9
        assert dist_up_to_phase(g, f) < 1e-8 * math.sqrt(sum(m * m for m in mag))


def test_example_of_the_page() -> None:
    f = [1, 1j, -1, 2, 0, 0, 0, 0]
    mag = [abs(v) for v in f]
    amp = [abs(v) for v in dft(f)]
    s2 = math.sqrt(2)
    expected = [math.sqrt(5), s2 - 1, math.sqrt(13), 3 + s2, math.sqrt(5), 1 + s2, math.sqrt(5), 3 - s2]
    assert max(abs(a - b) for a, b in zip(amp, expected)) < 1e-12
    for seed in range(1, 6):
        rng = random.Random(seed)
        phase0 = [rng.uniform(-math.pi, math.pi) for _ in f]
        g, errors = gerchberg_saxton(mag, amp, phase0, 200)
        assert errors[-1] < 1e-12
        assert dist_up_to_phase(g, f) < 1e-10
