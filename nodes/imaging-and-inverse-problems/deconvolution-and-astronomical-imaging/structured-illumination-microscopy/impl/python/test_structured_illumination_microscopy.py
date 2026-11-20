# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structured-illumination-microscopy/. The authors are listed in prov/BKPK9D.jsonl.

import math
import random

from imgkit import circ_conv2, dft2, gauss_noise, idft2
from structured_illumination_microscopy import (
    extended_support,
    inv3,
    mixing_matrix,
    otf_incoherent,
    pattern,
    psf_of_otf,
    separate_bands,
    sim_frames,
    sim_reconstruct,
    widefield,
    wiener_deconvolve,
)

PHASES = (0.0, 2 * math.pi / 3, 4 * math.pi / 3)


def rand_image(rng, n):
    return [[rng.random() for _ in range(n)] for _ in range(n)]


def max_diff(a, b):
    return max(abs(a[r][c] - b[r][c]) for r in range(len(a)) for c in range(len(a[0])))


def rel_err(a, b):
    num = sum((a[r][c] - b[r][c]) ** 2 for r in range(len(a)) for c in range(len(a[0])))
    den = sum(b[r][c] ** 2 for r in range(len(a)) for c in range(len(a[0])))
    return math.sqrt(num / den)


def test_forward_model_is_periodic_convolution():
    rng = random.Random(1)
    n = 8
    h = otf_incoherent(n, n, 2.5)
    psf = psf_of_otf(h)
    x = rand_image(rng, n)
    k0 = (1, 2)
    frames = sim_frames(x, h, k0, PHASES, 0.8)
    for phi, d in zip(PHASES, frames):
        p = pattern(n, n, k0, phi, 0.8)
        lit = [[p[r][c] * x[r][c] for c in range(n)] for r in range(n)]
        assert max_diff(d, circ_conv2(lit, psf)) < 1e-12


def test_band_separation_is_exact():
    rng = random.Random(2)
    n = 16
    h = otf_incoherent(n, n, 4)
    x = rand_image(rng, n)
    u, v = 1, 3
    phases = (0.3, 1.9, 4.4)
    s0, sp, sm = separate_bands(sim_frames(x, h, (u, v), phases, 0.7), phases, 0.7)
    big_x = dft2(x)
    for r in range(n):
        for c in range(n):
            assert abs(s0[r][c] - h[r][c] * big_x[r][c]) < 1e-9
            assert abs(sp[r][c] - h[r][c] * big_x[(r - u) % n][(c - v) % n]) < 1e-9
            assert abs(sm[r][c] - h[r][c] * big_x[(r + u) % n][(c + v) % n]) < 1e-9


def test_noise_free_output_is_projection_on_extended_support():
    rng = random.Random(3)
    n = 16
    h = otf_incoherent(n, n, 3)
    x = rand_image(rng, n)
    k0s = [(0, 3), (3, 0), (2, -2)]
    frames = [sim_frames(x, h, k0, PHASES, 1.0) for k0 in k0s]
    out = sim_reconstruct(frames, k0s, PHASES, 1.0, h, w=0.0)
    mask = extended_support(h, k0s)
    big_x = dft2(x)
    proj = idft2([[big_x[r][c] if mask[r][c] else 0j for c in range(n)] for r in range(n)])
    assert max_diff(out, [[z.real for z in row] for row in proj]) < 1e-9


def test_grating_beyond_cutoff_is_recovered():
    n, kc = 32, 6
    h = otf_incoherent(n, n, kc)
    x = [[1 + math.cos(2 * math.pi * 9 * c / n) for c in range(n)] for _ in range(n)]
    frames = sim_frames(x, h, (0, 5), PHASES, 1.0)
    wf = widefield(frames)
    flat = [v for row in wf for v in row]
    assert max(flat) - min(flat) < 1e-9
    out = sim_reconstruct([frames], [(0, 5)], PHASES, 1.0, h)
    assert max_diff(out, x) < 1e-9
    # A grating at frequency 12 is beyond kc + |k0| = 11 and stays invisible.
    y = [[1 + math.cos(2 * math.pi * 12 * c / n) for c in range(n)] for _ in range(n)]
    out = sim_reconstruct([sim_frames(y, h, (0, 5), PHASES, 1.0)], [(0, 5)], PHASES, 1.0, h)
    assert max_diff(out, [[1.0] * n for _ in range(n)]) < 1e-9


def test_equal_phases_or_zero_depth_raise():
    for phases, m in (((0.0, 0.0, 1.0), 1.0), (PHASES, 0.0)):
        try:
            inv3(mixing_matrix(phases, m))
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")


def test_inverse_of_mixing_matrix():
    a = mixing_matrix((0.1, 2.0, 3.7), 0.9)
    b = inv3(a)
    for i in range(3):
        for j in range(3):
            v = sum(a[i][t] * b[t][j] for t in range(3))
            assert abs(v - (1 if i == j else 0)) < 1e-12


def test_beats_widefield_wiener_with_noise():
    # A random image with every frequency up to radius 8 kept, seen with the
    # cutoff 5 and four stripe directions of length about 4.
    rng = random.Random(7)
    n, kc = 32, 5
    h = otf_incoherent(n, n, kc)
    big = dft2(rand_image(rng, n))
    for r in range(n):
        for c in range(n):
            if math.hypot(min(r, n - r), min(c, n - c)) > 8:
                big[r][c] = 0j
    x = [[z.real for z in row] for row in idft2(big)]
    k0s = [(0, 4), (4, 0), (3, 3), (3, -3)]
    sigma = 1e-2
    frames = []
    for k0 in k0s:
        clean = sim_frames(x, h, k0, PHASES, 1.0)
        frames.append([[[d[r][c] + e[r][c] for c in range(n)] for r in range(n)]
                       for d, e in ((d, gauss_noise(rng, (n, n), sigma)) for d in clean)])
    out = sim_reconstruct(frames, k0s, PHASES, 1.0, h, w=1e-3)
    wf = wiener_deconvolve(widefield(frames[0]), h, 1e-3)
    assert rel_err(out, x) < 0.5 * rel_err(wf, x)
