# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/w-projection/. The authors are listed in prov/0A2NXG.jsonl.

import random

from w_projection import (
    image_direct,
    predict_direct,
    w_kernel,
    w_project_image,
    w_project_predict,
)

N, DL = 16, 0.05


def page_data(wmax=6.0):
    """A source at the center and one near a corner, 40 grid visibilities with five w values."""
    rng = random.Random(1)
    sky = [[0.0] * N for _ in range(N)]
    sky[8][8] = 1.0
    sky[1][14] = 1.0
    vis = []
    for _ in range(40):
        ku, kv = rng.randint(-5, 5), rng.randint(-5, 5)
        w = rng.choice((-wmax, -wmax / 2, 0.0, wmax / 2, wmax))
        vis.append((ku, kv, w, 0, 1.0))
    vals = predict_direct(sky, vis, DL)
    return sky, [(ku, kv, w, v, wt) for (ku, kv, w, _, wt), v in zip(vis, vals)]


def rel_err(a, b):
    return max(abs(x - y) for x, y in zip(a, b)) / max(abs(y) for y in b)


def img_err(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def test_kernel_at_w_zero_is_a_delta():
    k = w_kernel(N, DL, 0.0)
    assert abs(k[(0, 0)] - 1.0) < 1e-12
    assert all(abs(v) < 1e-12 for q, v in k.items() if q != (0, 0))


def test_full_kernel_has_unit_energy():
    for w in (2.0, 6.0, -9.5):
        k = w_kernel(N, DL, w)
        assert len(k) == N * N
        assert abs(sum(abs(v) ** 2 for v in k.values()) - 1.0) < 1e-12


def test_full_kernel_is_exact():
    sky, vis = page_data()
    exact = [v for _, _, _, v, _ in vis]
    assert rel_err(w_project_predict(sky, vis, DL), exact) < 1e-12
    assert img_err(w_project_image(vis, N, DL), image_direct(vis, N, DL)) < 1e-12


def test_gridding_is_the_adjoint_of_degridding():
    rng = random.Random(6)
    _, vis = page_data()
    vis = [(ku, kv, w, complex(rng.gauss(0, 1), rng.gauss(0, 1)), rng.uniform(0.5, 2.0)) for ku, kv, w, _, _ in vis]
    x = [[rng.gauss(0, 1) for _ in range(N)] for _ in range(N)]
    total = sum(v[4] for v in vis)
    for support in (1, 3):
        img = w_project_image(vis, N, DL, support)
        pred = w_project_predict(x, vis, DL, support)
        lhs = sum(x[i][j] * img[i][j] for i in range(N) for j in range(N))
        rhs = sum(wt * (val * p.conjugate()).real for (_, _, _, val, wt), p in zip(vis, pred)) / total
        assert abs(lhs - rhs) < 1e-10


def test_error_falls_with_the_support():
    sky, vis = page_data()
    exact = [v for _, _, _, v, _ in vis]
    errs = [rel_err(w_project_predict(sky, vis, DL, s), exact) for s in (1, 2, 4, 6)]
    assert all(a > b for a, b in zip(errs, errs[1:]))
    assert errs[-1] < 0.07
    flat = [(ku, kv, 0.0, v, wt) for ku, kv, _, v, wt in vis]
    no_correction = rel_err(w_project_predict(sky, flat, DL, 0), exact)
    assert no_correction > 0.9 and errs[1] < 0.35


def test_a_source_at_the_center_needs_no_correction():
    sky, vis = page_data()
    sky[1][14] = 0.0
    exact = predict_direct(sky, vis, DL)
    flat = [(ku, kv, 0.0, v, wt) for ku, kv, _, v, wt in vis]
    assert rel_err(w_project_predict(sky, flat, DL, 0), exact) < 1e-12
