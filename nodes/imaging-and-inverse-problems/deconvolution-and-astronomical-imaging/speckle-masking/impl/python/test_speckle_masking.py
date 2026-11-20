# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/speckle-masking/. The authors are listed in prov/A53FCA.jsonl.

import cmath
import math

from speckle_masking import (
    bispectra,
    modulus_from_reference,
    object_spectrum,
    phase_error,
    power_spectrum,
    reconstruct,
    shift_frames,
    simulate_frames,
    speckle_masking_phase,
)

N, D, SIGMA, RADIUS = 16, 6, 3.0, 4
POINTS = {(0, 0): 1.0, (2, 1): 0.6, (-1, 3): 0.35}


def wrap(a):
    return abs(cmath.phase(cmath.exp(1j * a)))


def rms_error(phase, obj):
    a1 = cmath.phase(obj[1][0]) - phase[(1, 0)]
    a2 = cmath.phase(obj[0][1]) - phase[(0, 1)]
    errs = [wrap(ph - cmath.phase(obj[u[0] % N][u[1] % N]) + a1 * u[0] + a2 * u[1]) for u, ph in phase.items()]
    return math.sqrt(sum(e * e for e in errs) / len(errs))


def test_bispectrum_does_not_see_image_motion():
    obj = object_spectrum(POINTS, N)
    frames = simulate_frames(obj, N, D, SIGMA, 4, 3)
    still = bispectra(frames)
    moved = bispectra(shift_frames(frames, 9, 3))
    for a, b in zip(still, moved):
        for ra, rb in zip(a, b):
            for x, y in zip(ra, rb):
                assert abs(x - y) < 1e-12


def test_antithetic_bispectrum_has_the_closure_phase():
    obj = object_spectrum(POINTS, N)
    b1, _ = bispectra(simulate_frames(obj, N, D, SIGMA, 3, 7))
    ph = [[cmath.phase(v) for v in row] for row in obj]
    for k1 in range(N):
        for k2 in range(N):
            if abs(b1[k1][k2]) > 1e-9:
                want = ph[k1][k2] + ph[1][0] - ph[(k1 + 1) % N][k2]
                d = wrap(cmath.phase(b1[k1][k2]) - want)
                assert d < 1e-7 or abs(d - math.pi) < 1e-7


def test_antithetic_average_gives_the_phase_up_to_a_shift():
    obj = object_spectrum(POINTS, N)
    frames = shift_frames(simulate_frames(obj, N, D, SIGMA, 50, 1), 5, 2)
    phase = speckle_masking_phase(bispectra(frames), N, RADIUS)
    assert len(phase) == 49
    assert phase_error(phase, obj, N) < 1e-9
    tilted = speckle_masking_phase(bispectra(frames), N, RADIUS, tilt=(cmath.phase(obj[1][0]), cmath.phase(obj[0][1])))
    for u, ph in tilted.items():
        assert wrap(ph - cmath.phase(obj[u[0] % N][u[1] % N])) < 1e-9


def test_one_frame_is_not_enough_and_averaging_converges():
    obj = object_spectrum(POINTS, N)
    frames = simulate_frames(obj, N, D, SIGMA, 300, 1, antithetic=False)
    one = rms_error(speckle_masking_phase(bispectra(frames[:1]), N, RADIUS), obj)
    many = rms_error(speckle_masking_phase(bispectra(frames), N, RADIUS), obj)
    assert one > 1.0
    assert many < 0.05


def test_reconstruction_with_a_reference_star():
    obj = object_spectrum(POINTS, N)
    frames = simulate_frames(obj, N, D, SIGMA, 50, 1)
    ref = simulate_frames(object_spectrum({(0, 0): 1.0}, N), N, D, SIGMA, 50, 2)
    tilt = (cmath.phase(obj[1][0]), cmath.phase(obj[0][1]))
    phase = speckle_masking_phase(bispectra(frames), N, RADIUS, tilt)
    img = reconstruct(modulus_from_reference(power_spectrum(frames), power_spectrum(ref), phase), phase, N)
    exact = {u: abs(obj[u[0] % N][u[1] % N]) for u in phase}
    true = reconstruct(exact, {u: cmath.phase(obj[u[0] % N][u[1] % N]) for u in phase}, N)
    peak = max(max(row) for row in true)
    assert max(abs(a - b) for ra, rb in zip(img, true) for a, b in zip(ra, rb)) < 0.05 * peak
