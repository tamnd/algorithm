# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-gradient-autofocus/. The authors are listed in prov/Y2C9T3.jsonl.

import cmath
import math
import random

from phase_gradient_autofocus import apply_phase, pga, pga_once, remove_linear

N, M = 64, 24
Q = [((k - N / 2) / (N / 2)) ** 2 for k in range(N)]
SMOOTH = [8 * q + 3 * ((k - N / 2) / (N / 2)) ** 3 for k, q in enumerate(Q)]


def rms(v):
    return math.sqrt(sum(x * x for x in v) / len(v))


def points_only(seed):
    rng = random.Random(seed)
    img = [[0j] * N for _ in range(M)]
    for m in range(M):
        img[m][rng.randrange(N)] = complex(rng.gauss(0, 1), rng.gauss(0, 1))
    return img


def with_clutter(seed):
    rng = random.Random(seed)
    img = [[complex(rng.gauss(0, 0.3), rng.gauss(0, 0.3)) for _ in range(N)] for _ in range(M)]
    for m in range(M):
        img[m][rng.randrange(N)] += rng.choice([3, 4, 5]) * cmath.exp(2j * math.pi * rng.random())
    return img


def test_one_iteration_is_exact_for_isolated_points() -> None:
    """Theorem: one point per range bin, no clutter, full window: phi is found up to a + b k."""
    rng = random.Random(5)
    phi = [s + rng.gauss(0, 0.3) for s in SMOOTH]
    est, width = pga_once(apply_phase(points_only(5), phi), width=N)
    assert width == N
    assert max(abs(r) for r in remove_linear([p - e for p, e in zip(phi, est)])) < 1e-9


def test_reduces_a_smooth_phase_error_in_clutter() -> None:
    """Measurement: bright points in Gaussian clutter, default adaptive window."""
    start = rms(remove_linear(SMOOTH))
    assert start > 2.0
    for seed in (1, 2, 3, 4):
        _, est = pga(apply_phase(with_clutter(seed), SMOOTH))
        assert rms(remove_linear([p - e for p, e in zip(SMOOTH, est)])) < 0.25


def test_agrees_with_a_brute_force_search_on_a_quadratic_error() -> None:
    """Reference: try every quadratic coefficient on a grid and keep the sharpest image."""
    blurred = apply_phase(with_clutter(11), [6.0 * q for q in Q])

    def sharpness(c):
        img = apply_phase(blurred, [-c * q for q in Q])
        return sum(abs(v) ** 4 for row in img for v in row)

    brute = max((0.25 * i for i in range(41)), key=sharpness)
    _, est = pga(blurred)
    qc = remove_linear(Q)
    c_pga = sum(a * b for a, b in zip(qc, est)) / sum(a * a for a in qc)
    assert abs(brute - 6.0) <= 0.25
    assert abs(c_pga - brute) < 0.4


def test_apply_phase_round_trip() -> None:
    img = with_clutter(3)
    back = apply_phase(apply_phase(img, SMOOTH), [-p for p in SMOOTH])
    assert max(abs(a - b) for ra, rb in zip(img, back) for a, b in zip(ra, rb)) < 1e-9


def test_linear_phase_only_shifts_the_image() -> None:
    img = points_only(2)
    shifted = apply_phase(img, [2 * math.pi * 3 * k / N for k in range(N)])
    for row, srow in zip(img, shifted):
        for j in range(N):
            assert abs(srow[j] - row[(j + 3) % N]) < 1e-9
    assert max(abs(v) for v in remove_linear([1.5 + 0.2 * k for k in range(N)])) < 1e-12
