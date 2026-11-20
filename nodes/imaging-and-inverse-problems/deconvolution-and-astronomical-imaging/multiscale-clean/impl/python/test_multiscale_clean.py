# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiscale-clean/. The authors are listed in prov/KXJYFX.jsonl.

import random

from imgkit import dft2, idft2, new_image
from multiscale_clean import conv_fft, gaussian_blob, multiscale_clean, scale_function, scale_misfit


def beam_and_dirty(sky, w):
    n1, n2 = len(sky), len(sky[0])
    s = n1 * n2 / sum(sum(r) for r in w)
    beam = [[v.real * s for v in row] for row in idft2(w)]
    vis = dft2(sky)
    prod = [[a * b for a, b in zip(ra, rb)] for ra, rb in zip(w, vis)]
    dirty = [[v.real * s for v in row] for row in idft2(prod)]
    return beam, dirty


def mask_1d(n, freqs):
    w = [0.0] * n
    for k in freqs:
        w[k % n] = 1.0
        w[-k % n] = 1.0
    return [w]


def mask_2d(n, fraction, rng):
    w = new_image(n, n)
    for k in range(-1, 2):
        for l in range(-1, 2):
            w[k % n][l % n] = 1.0
    for k in range(n):
        for l in range(n):
            if rng.random() < fraction:
                w[k][l] = 1.0
                w[-k % n][-l % n] = 1.0
    return w


def max_abs(img):
    return max(abs(v) for row in img for v in row)


def page_example():
    n = 32
    w = mask_1d(n, (0, 1, 2, 3, 5, 7, 10))
    sky = gaussian_blob(1, n, 0, 10, 2.0, 4.0)
    sky[0][24] += 1.0
    beam, dirty = beam_and_dirty(sky, w)
    return sky, w, beam, dirty


def hogbom_reference(dirty, beam, gain, max_iter):
    n1, n2 = len(dirty), len(dirty[0])
    r = [list(row) for row in dirty]
    comps = []
    for _ in range(max_iter):
        i0, j0 = max(((i, j) for i in range(n1) for j in range(n2)), key=lambda p: abs(r[p[0]][p[1]]))
        c = gain * r[i0][j0] / beam[0][0]
        comps.append((i0, j0, c))
        for i in range(n1):
            for j in range(n2):
                r[i][j] -= c * beam[(i - i0) % n1][(j - j0) % n2]
    return comps, r


def test_scale_functions():
    d = scale_function(8, 8, 0)
    assert d[0][0] == 1.0 and sum(sum(r) for r in d) == 1.0
    for size in (2, 3, 5):
        ph = scale_function(16, 16, size)
        assert abs(sum(sum(r) for r in ph) - 1.0) < 1e-12
        assert all(ph[i][j] == ph[-i % 16][-j % 16] for i in range(16) for j in range(16))
    try:
        multiscale_clean([[1.0, 0.0]], [[1.0, 0.0]], [2])
    except ValueError:
        pass
    else:
        raise AssertionError("the delta scale is required")


def test_one_scale_is_hogbom():
    rng = random.Random(2)
    w = mask_2d(16, 0.2, rng)
    sky = new_image(16, 16)
    for _ in range(4):
        sky[rng.randrange(16)][rng.randrange(16)] += rng.uniform(0.5, 1.5)
    beam, dirty = beam_and_dirty(sky, w)
    _, res, comps, _ = multiscale_clean(dirty, beam, [0], gain=0.2, max_iter=25)
    ref, rres = hogbom_reference(dirty, beam, 0.2, 25)
    assert [(i, j) for _, i, j, _ in comps] == [(i, j) for i, j, _ in ref]
    assert max(abs(a[3] - b[2]) for a, b in zip(comps, ref)) < 1e-12
    assert max(abs(a - b) for ra, rb in zip(res, rres) for a, b in zip(ra, rb)) < 1e-12


def test_smoothed_residuals_stay_exact():
    rng = random.Random(8)
    w = mask_2d(16, 0.25, rng)
    sky = gaussian_blob(16, 16, 5, 6, 1.5, 3.0)
    sky[12][3] += 1.0
    beam, dirty = beam_and_dirty(sky, w)
    sizes = [0, 2, 4]
    model, res, comps, smoothed = multiscale_clean(dirty, beam, sizes, gain=0.2, max_iter=40)
    assert len({s for s, _, _, _ in comps}) >= 2
    pred = conv_fft(model, beam)
    true_res = [[d - p for d, p in zip(rd, rp)] for rd, rp in zip(dirty, pred)]
    for size, sm in zip(sizes, smoothed):
        want = conv_fft(true_res, scale_function(16, 16, size))
        assert max(abs(a - b) for ra, rb in zip(sm, want) for a, b in zip(ra, rb)) < 1e-10
    assert max(abs(a - b) for ra, rb in zip(res, true_res) for a, b in zip(ra, rb)) < 1e-10


def test_misfit_drops_by_the_proved_amount():
    sky, w, beam, dirty = page_example()
    sizes = [0, 3, 6]
    phis = [scale_function(1, 32, s) for s in sizes]
    bss = [conv_fft(ph, ph, beam)[0][0] for ph in phis]
    for gain in (0.3, 1.0, 1.8):
        q = scale_misfit(new_image(1, 32), sky, w)
        for t in range(1, 9):
            model, _, comps, _ = multiscale_clean(dirty, beam, sizes, gain=gain, max_iter=t)
            s, _, _, c = comps[-1]
            q2 = scale_misfit(model, sky, w)
            assert abs((q - q2) - (2 - gain) / gain * c * c * bss[s]) < 1e-9
            assert q2 < q
            q = q2


def test_converges_to_the_data():
    rng = random.Random(4)
    w = mask_2d(16, 0.3, rng)
    sky = gaussian_blob(16, 16, 8, 8, 2.0, 5.0)
    beam, dirty = beam_and_dirty(sky, w)
    model, res, _, _ = multiscale_clean(dirty, beam, [0, 2, 4], gain=0.5, max_iter=300)
    assert max_abs(res) < 1e-2 * max_abs(dirty)
    assert scale_misfit(model, sky, w) < 1e-4 * scale_misfit(new_image(16, 16), sky, w)


def test_extended_source_needs_fewer_components():
    sky, w, beam, dirty = page_example()
    tol = 0.01 * max_abs(dirty)

    def run(sizes):
        model, res, comps, _ = multiscale_clean(dirty, beam, sizes, gain=0.3, threshold=0.0, max_iter=200)
        for k in range(1, len(comps) + 1):
            m, r, _, _ = multiscale_clean(dirty, beam, sizes, gain=0.3, max_iter=k)
            if max_abs(r) < tol:
                return k, max(abs(a - b) for a, b in zip(m[0], sky[0]))
        raise AssertionError("did not converge")

    k_point, err_point = run([0])
    k_multi, err_multi = run([0, 3, 6])
    assert (k_point, k_multi) == (65, 35)
    assert err_multi < 0.5 * err_point
