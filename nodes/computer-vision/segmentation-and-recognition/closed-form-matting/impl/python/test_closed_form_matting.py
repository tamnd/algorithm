# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/closed-form-matting/. The authors are listed in prov/YQKAHR.jsonl.

import random

from closed_form_matting import (
    closed_form_matting,
    composite,
    cost_j,
    matting_laplacian,
    quadratic_form,
    solve_matte,
)
from cvla import sym_eig


def gray_image(rng, h, w):
    return [[rng.random() for _ in range(w)] for _ in range(h)]


def color_image(rng, h, w):
    return [[[rng.random() for _ in range(3)] for _ in range(w)] for _ in range(h)]


def test_example_blurred_edge():
    row = [0.1, 0.2, 0.5, 0.9, 0.9]
    img = [row[:] for _ in range(3)]
    scribbles = {}
    for v in range(3):
        scribbles[v * 5] = 0.0
        scribbles[v * 5 + 4] = 1.0
    alpha = closed_form_matting(img, scribbles, 1e-6)
    assert [round(x, 4) for x in alpha[5:10]] == [0.0, 0.125, 0.5, 1.0, 1.0]
    alpha = closed_form_matting(img, scribbles, 0.1)
    assert [round(x, 4) for x in alpha[5:10]] == [0.0, 0.2295, 0.512, 0.8615, 1.0]


def test_laplacian_is_symmetric_with_zero_row_sums_and_psd():
    rng = random.Random(4)
    for img in (gray_image(rng, 4, 4), color_image(rng, 4, 4)):
        lap = matting_laplacian(img, 1e-3)
        n = len(lap)
        for i in range(n):
            assert abs(sum(lap[i])) < 1e-12
            for j in range(n):
                assert abs(lap[i][j] - lap[j][i]) < 1e-12
        w, _ = sym_eig(lap)
        assert w[0] > -1e-10
        assert abs(w[0]) < 1e-10
        assert w[1] > 1e-8


def test_theorem_1_quadratic_form_equals_min_over_a_b():
    rng = random.Random(7)
    for img in (gray_image(rng, 4, 5), color_image(rng, 4, 4)):
        for eps in (1e-3, 0.1):
            lap = matting_laplacian(img, eps)
            for _ in range(5):
                alpha = [rng.uniform(-0.5, 1.5) for _ in range(len(lap))]
                assert abs(quadratic_form(lap, alpha) - cost_j(img, alpha, eps)) < 1e-9


def test_eps_zero_null_space_holds_the_channels():
    rng = random.Random(9)
    img = color_image(rng, 4, 4)
    lap = matting_laplacian(img, 0.0)
    flat = [x for row in img for x in row]
    for ch in range(3):
        y = [p[ch] for p in flat]
        r = [sum(lap[i][j] * y[j] for j in range(16)) for i in range(16)]
        assert max(abs(t) for t in r) < 1e-9


def test_theorem_3_recovers_the_true_matte():
    rng = random.Random(12)
    h, w = 4, 5
    n = h * w
    alpha = [rng.random() for _ in range(n)]
    for fg, bg in ((0.85, 0.15), ([0.9, 0.2, 0.1], [0.1, 0.3, 0.8])):
        flat = composite(alpha, [fg] * n, [bg] * n)
        img = [flat[v * w:(v + 1) * w] for v in range(h)]
        scribbles = {0: alpha[0], 7: alpha[7], 19: alpha[19]}
        got = closed_form_matting(img, scribbles, 1e-8)
        assert max(abs(x - y) for x, y in zip(got, alpha)) < 1e-5


def test_solution_minimizes_and_complements():
    rng = random.Random(21)
    img = color_image(rng, 4, 4)
    lap = matting_laplacian(img, 1e-2)
    scribbles = {0: 0.0, 3: 0.0, 12: 1.0, 15: 1.0}
    alpha = solve_matte(lap, scribbles)
    best = quadratic_form(lap, alpha)
    for _ in range(100):
        y = [a if p in scribbles else a + rng.uniform(-0.1, 0.1) for p, a in enumerate(alpha)]
        assert quadratic_form(lap, y) >= best - 1e-12
    flipped = solve_matte(lap, {p: 1.0 - s for p, s in scribbles.items()})
    assert all(abs(a + b - 1.0) < 1e-9 for a, b in zip(alpha, flipped))
    ones = solve_matte(lap, {p: 1.0 for p in scribbles})
    assert all(abs(a - 1.0) < 1e-9 for a in ones)


def test_alpha_can_leave_the_unit_interval():
    rng = random.Random(1)
    found = False
    for _ in range(10):
        img = gray_image(rng, 4, 5)
        alpha = closed_form_matting(img, {0: 0.0, 4: 0.0, 15: 1.0, 19: 1.0}, 1e-3)
        if min(alpha) < -1e-6 or max(alpha) > 1 + 1e-6:
            found = True
    assert found
