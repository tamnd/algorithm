# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cross-lingual-embedding-mapping/. The authors are listed in prov/CP9A01.jsonl.

import math
import random

from cross_lingual_embedding_mapping import (
    apply,
    fit_orthogonal,
    identity,
    least_squares_map,
    loss,
    matmul,
    orthogonality_error,
    polar_newton,
    precision_at_1,
    procrustes_map,
    svd,
    translate,
    transpose,
)


def random_orthogonal(rng, d):
    """Gram-Schmidt on a Gaussian matrix: a random orthogonal matrix (det may be -1)."""
    cols = []
    while len(cols) < d:
        v = [rng.gauss(0, 1) for _ in range(d)]
        for c in cols:
            dot = sum(a * b for a, b in zip(v, c))
            v = [a - dot * b for a, b in zip(v, c)]
        n = math.sqrt(sum(a * a for a in v))
        if n > 1e-3:
            cols.append([a / n for a in v])
    return transpose(cols)


def gaussian_rows(rng, n, d):
    return [[rng.gauss(0, 1) for _ in range(d)] for _ in range(n)]


def max_abs_diff(a, b):
    return max(abs(x - y) for r, s in zip(a, b) for x, y in zip(r, s))


def test_svd_reconstructs():
    rng = random.Random(1)
    for d in (1, 2, 3, 5, 8, 16):
        m = gaussian_rows(rng, d, d)
        u, s, v = svd(m)
        assert orthogonality_error(u) < 1e-9
        assert orthogonality_error(v) < 1e-9
        assert all(s[i] >= s[i + 1] >= 0 for i in range(d - 1))
        us = [[u[i][j] * s[j] for j in range(d)] for i in range(d)]
        assert max_abs_diff(matmul(us, transpose(v)), m) < 1e-9


def test_recovers_planted_rotation():
    rng = random.Random(2)
    for d in (2, 4, 8, 16):
        q = random_orthogonal(rng, d)
        x = gaussian_rows(rng, 3 * d, d)
        y = [apply(q, xi) for xi in x]
        w = procrustes_map(x, y)
        assert orthogonality_error(w) < 1e-9
        assert max_abs_diff(w, q) < 1e-9


def test_planted_rotation_with_noise():
    rng = random.Random(3)
    d = 6
    q = random_orthogonal(rng, d)
    x = gaussian_rows(rng, 200, d)
    y = [[a + rng.gauss(0, 0.05) for a in apply(q, xi)] for xi in x]
    w = procrustes_map(x, y)
    assert orthogonality_error(w) < 1e-9
    assert max_abs_diff(w, q) < 0.05
    assert loss(w, x, y) <= loss(q, x, y) + 1e-9


def test_no_orthogonal_matrix_does_better():
    rng = random.Random(4)
    for d in (2, 3, 4):
        x = gaussian_rows(rng, 10, d)
        y = gaussian_rows(rng, 10, d)
        w = procrustes_map(x, y)
        best = loss(w, x, y)
        for _ in range(300):
            assert loss(random_orthogonal(rng, d), x, y) >= best - 1e-9


def test_brute_force_over_angles_in_two_dimensions():
    rng = random.Random(5)
    x = gaussian_rows(rng, 8, 2)
    y = gaussian_rows(rng, 8, 2)
    best = loss(procrustes_map(x, y), x, y)
    grid = math.inf
    for k in range(20000):
        th = 2 * math.pi * k / 20000
        c, s = math.cos(th), math.sin(th)
        grid = min(grid, loss([[c, -s], [s, c]], x, y), loss([[c, s], [s, -c]], x, y))
    assert best <= grid + 1e-9
    assert grid - best < 1e-3


def test_reflection_case():
    x = [[1.0, 0.0], [0.0, 1.0]]
    y = [[1.0, 0.0], [0.0, -1.0]]
    w = procrustes_map(x, y)
    assert max_abs_diff(w, [[1.0, 0.0], [0.0, -1.0]]) < 1e-12
    assert loss(w, x, y) < 1e-24
    for k in range(360):
        th = math.radians(k)
        c, s = math.cos(th), math.sin(th)
        assert abs(loss([[c, -s], [s, c]], x, y) - 4.0) < 1e-12


def test_polar_newton_agrees():
    rng = random.Random(6)
    for d in (2, 3, 7):
        x = gaussian_rows(rng, 12, d)
        y = gaussian_rows(rng, 12, d)
        m = matmul(transpose(y), x)
        assert max_abs_diff(polar_newton(m), procrustes_map(x, y)) < 1e-9


def test_rank_deficient_dictionary_still_orthogonal():
    rng = random.Random(7)
    d = 5
    q = random_orthogonal(rng, d)
    x = gaussian_rows(rng, 2, d)  # only 2 pairs: M has rank 2
    y = [apply(q, xi) for xi in x]
    w = procrustes_map(x, y)
    assert orthogonality_error(w) < 1e-9
    assert loss(w, x, y) < 1e-18


def test_least_squares_map():
    rng = random.Random(8)
    d = 4
    q = random_orthogonal(rng, d)
    x = gaussian_rows(rng, 30, d)
    y = [apply(q, xi) for xi in x]
    assert max_abs_diff(least_squares_map(x, y), q) < 1e-9
    y_noisy = [[a + rng.gauss(0, 0.3) for a in yi] for yi in y]
    ls = least_squares_map(x, y_noisy)
    orth = procrustes_map(x, y_noisy)
    assert loss(ls, x, y_noisy) <= loss(orth, x, y_noisy) + 1e-9
    assert orthogonality_error(ls) > 1e-3


def test_translation_of_planted_lexicon():
    rng = random.Random(9)
    d, n = 8, 40
    q = random_orthogonal(rng, d)
    src = {f"s{i}": [rng.gauss(0, 1) for _ in range(d)] for i in range(n)}
    tgt = {f"t{i}": [a + rng.gauss(0, 0.01) for a in apply(q, src[f"s{i}"])] for i in range(n)}
    seed = [f"s{i}" for i in range(16)]
    w = fit_orthogonal([src[s] for s in seed], [tgt["t" + s[1:]] for s in seed])
    assert orthogonality_error(w) < 1e-9
    held = {s: src[s] for s in src if s not in seed}
    pred = translate(w, held, tgt)
    gold = {s: {"t" + s[1:]} for s in held}
    assert precision_at_1(pred, gold) == 1.0
    assert precision_at_1(translate(identity(d), held, tgt), gold) < 0.5
