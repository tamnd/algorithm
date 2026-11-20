# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/error-reduction-algorithm/. The authors are listed in prov/HKZC9V.jsonl.

import cmath
import math
import random

from error_reduction_algorithm import (
    error_reduction,
    fourier_error,
    magnitude_projection,
    object_error,
    object_projection,
)
from imgkit import dft2, idft2


def dist(a, b):
    return math.sqrt(sum(abs(x - y) ** 2 for ra, rb in zip(a, b) for x, y in zip(ra, rb)))


def problem(seed, n=8, k=4):
    """A nonnegative k x k object in the corner of an n x n frame, its support and magnitudes."""
    rng = random.Random(seed)
    f = [[rng.uniform(0.2, 1.0) if i < k and j < k else 0.0 for j in range(n)] for i in range(n)]
    support = [[i < k and j < k for j in range(n)] for i in range(n)]
    amp = [[abs(v) for v in row] for row in dft2(f)]
    return f, support, amp


def random_image(rng, n, cplx=True):
    if cplx:
        return [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)] for _ in range(n)]
    return [[rng.uniform(0, 1) for _ in range(n)] for _ in range(n)]


def test_magnitude_projection_is_a_nearest_point() -> None:
    rng = random.Random(1)
    _, _, amp = problem(1)
    g = random_image(rng, 8)
    p = magnitude_projection(g, amp)
    assert max(abs(abs(v) - a) for rv, ra in zip(dft2(p), amp) for v, a in zip(rv, ra)) < 1e-9
    d0 = dist(g, p)
    assert abs(d0 - fourier_error(g, amp)) < 1e-9
    for _ in range(50):
        phases = [[cmath.exp(1j * rng.uniform(0, 2 * math.pi)) for _ in range(8)] for _ in range(8)]
        other = idft2([[a * ph for a, ph in zip(ra, rp)] for ra, rp in zip(amp, phases)])
        assert dist(g, other) >= d0 - 1e-9


def test_object_projection_is_a_nearest_point() -> None:
    rng = random.Random(2)
    _, support, _ = problem(2)
    g = random_image(rng, 8)
    for positive in (False, True):
        p = object_projection(g, support, positive)
        d0 = dist(g, p)
        assert abs(d0 - object_error(g, support, positive)) < 1e-12
        for _ in range(50):
            q = [[(rng.uniform(0, 2) if positive else complex(rng.gauss(0, 1), rng.gauss(0, 1))) if s else 0.0
                  for s in row] for row in support]
            assert dist(g, q) >= d0 - 1e-12


def test_true_object_is_a_fixed_point() -> None:
    f, support, amp = problem(3)
    for positive in (False, True):
        g, errors = error_reduction(amp, support, f, 3, positive)
        assert dist(g, f) < 1e-9
        assert max(errors) < 1e-9


def test_error_never_increases() -> None:
    rng = random.Random(4)
    for seed, positive in ((5, True), (6, False)):
        _, support, amp = problem(seed)
        g0 = random_image(rng, 8, cplx=not positive)
        _, errors = error_reduction(amp, support, g0, 40, positive)
        for e0, e1 in zip(errors, errors[1:]):
            assert e1 <= e0 + 1e-10
        assert errors[-1] < errors[0]


def test_error_sandwich_of_one_step() -> None:
    rng = random.Random(7)
    _, support, amp = problem(8)
    g = object_projection(random_image(rng, 8, cplx=False), support, True)
    for _ in range(5):
        gp = magnitude_projection(g, amp)
        e_f = fourier_error(g, amp)
        e_0 = object_error(gp, support, True)
        g_next = object_projection(gp, support, True)
        assert fourier_error(g_next, amp) <= e_0 + 1e-10
        assert e_0 <= e_f + 1e-10
        g = g_next


def test_step_is_steepest_descent_with_unit_step() -> None:
    rng = random.Random(9)
    _, _, amp = problem(10)
    g = random_image(rng, 8)
    grad = [[v - p for v, p in zip(rv, rp)] for rv, rp in zip(g, magnitude_projection(g, amp))]
    for _ in range(4):
        d = random_image(rng, 8)
        h = 1e-5
        plus = [[v + h * w for v, w in zip(rv, rd)] for rv, rd in zip(g, d)]
        minus = [[v - h * w for v, w in zip(rv, rd)] for rv, rd in zip(g, d)]
        fd = (0.5 * fourier_error(plus, amp) ** 2 - 0.5 * fourier_error(minus, amp) ** 2) / (2 * h)
        exact = sum((a.conjugate() * b).real for ra, rb in zip(grad, d) for a, b in zip(ra, rb))
        assert abs(fd - exact) < 1e-6 * (1 + abs(exact))
