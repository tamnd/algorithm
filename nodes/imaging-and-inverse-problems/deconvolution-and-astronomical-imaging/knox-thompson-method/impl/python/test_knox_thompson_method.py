# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knox-thompson-method/. The authors are listed in prov/SH6M7B.jsonl.

import cmath
import math
import random

from knox_thompson_method import (
    cross_spectra,
    knox_thompson_phase,
    modulus_from_reference,
    object_spectrum,
    phase_error,
    phase_screen,
    power_spectrum,
    pupil_mask,
    reconstruct,
    screen_amplitude,
    simulate_frames,
    transfer_function,
)

N, D, SIGMA, RADIUS = 16, 6, 3.0, 4
POINTS = {(0, 0): 1.0, (2, 1): 0.6, (-1, 3): 0.35}


def wrap(a):
    return abs(cmath.phase(cmath.exp(1j * a)))


def rms_error(phase, obj):
    errs = [wrap(ph - cmath.phase(obj[u[0] % N][u[1] % N])) for u, ph in phase.items()]
    return math.sqrt(sum(e * e for e in errs) / len(errs))


def test_transfer_function_of_one_frame():
    rng = random.Random(4)
    t = transfer_function(phase_screen(rng, screen_amplitude(N, SIGMA)), pupil_mask(N, D))
    assert abs(t[0][0] - 1.0) < 1e-12
    for k1 in range(N):
        for k2 in range(N):
            assert abs(t[k1][k2] - t[-k1 % N][-k2 % N].conjugate()) < 1e-12
            assert abs(t[k1][k2]) <= 1.0 + 1e-12
            if min(k1, N - k1) >= D or min(k2, N - k2) >= D:
                assert abs(t[k1][k2]) < 1e-12


def test_antithetic_cross_spectrum_has_the_object_phase_difference():
    obj = object_spectrum(POINTS, N)
    c1, _ = cross_spectra(simulate_frames(obj, N, D, SIGMA, 3, 7, antithetic=True))
    for k1 in range(N):
        for k2 in range(N):
            if abs(c1[k1][k2]) > 1e-9:
                want = cmath.phase(obj[k1][k2]) - cmath.phase(obj[(k1 + 1) % N][k2])
                d = wrap(cmath.phase(c1[k1][k2]) - want)
                assert d < 1e-7 or abs(d - math.pi) < 1e-7


def test_antithetic_average_gives_the_exact_phase():
    obj = object_spectrum(POINTS, N)
    phase = knox_thompson_phase(cross_spectra(simulate_frames(obj, N, D, SIGMA, 50, 1)), N, RADIUS)
    assert len(phase) == 49
    assert phase_error(phase, obj, N) < 1e-9
    for (a, b), ph in phase.items():
        assert wrap(ph + phase[(-a, -b)]) < 1e-9


def test_one_frame_is_not_enough_and_averaging_converges():
    obj = object_spectrum(POINTS, N)
    frames = simulate_frames(obj, N, D, SIGMA, 300, 1, antithetic=False)
    one = rms_error(knox_thompson_phase(cross_spectra(frames[:1]), N, RADIUS), obj)
    many = rms_error(knox_thompson_phase(cross_spectra(frames), N, RADIUS), obj)
    assert one > 1.0
    assert many < 0.15


def test_reconstruction_with_a_reference_star():
    obj = object_spectrum(POINTS, N)
    frames = simulate_frames(obj, N, D, SIGMA, 50, 1)
    ref = simulate_frames(object_spectrum({(0, 0): 1.0}, N), N, D, SIGMA, 50, 2)
    phase = knox_thompson_phase(cross_spectra(frames), N, RADIUS)
    img = reconstruct(modulus_from_reference(power_spectrum(frames), power_spectrum(ref), phase), phase, N)
    exact = {u: abs(obj[u[0] % N][u[1] % N]) for u in phase}
    true = reconstruct(exact, {u: cmath.phase(obj[u[0] % N][u[1] % N]) for u in phase}, N)
    peak = max(max(row) for row in true)
    assert max(abs(a - b) for ra, rb in zip(img, true) for a, b in zip(ra, rb)) < 0.05 * peak
    assert img[N // 2][N // 2] == max(max(row) for row in img)
