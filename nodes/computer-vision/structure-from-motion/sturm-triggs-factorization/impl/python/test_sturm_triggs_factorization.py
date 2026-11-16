# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sturm-triggs-factorization/. The authors are listed in prov/JQNS8Q.jsonl.

import math
import random

import pytest

from cvgeom import add_noise, random_scene
from cvla import matvec, svd
from sturm_triggs_factorization import (apply, chained_depths, normalizing_transform,
                                        reprojection_errors, sturm_triggs_factorization)


def make_scene(seed, n_cams=4, n_pts=20, max_angle=0.4, distance=4.0):
    rng = random.Random(seed)
    sc = random_scene(rng, n=n_pts, n_cams=n_cams, max_angle=max_angle, distance=distance)
    return rng, sc


def test_exact_data_reprojects_exactly():
    for seed in range(3):
        _, sc = make_scene(seed)
        res = sturm_triggs_factorization(sc["x"])
        assert res["S"][4] < 1e-9 * res["S"][0]
        assert max(reprojection_errors(res["P"], res["X"], sc["x"])) < 1e-6


def test_chained_depths_are_true_depths_up_to_row_and_column_scales():
    _, sc = make_scene(3, n_cams=5)
    ts = [normalizing_transform(f) for f in sc["x"]]
    xn = [[apply(t, p) for p in f] for t, f in zip(ts, sc["x"])]
    lam = chained_depths(xn)
    true = [[matvec(r, x)[2] + t[2] for x in sc["X"]] for r, t in zip(sc["R"], sc["t"])]
    ratio = [[a / b for a, b in zip(ra, rb)] for ra, rb in zip(lam, true)]
    # ratio[i][p] = a_i b_p, so the ratio matrix has rank 1
    for i in range(5):
        for p in range(len(sc["X"])):
            assert abs(ratio[i][p] * ratio[0][0] - ratio[i][0] * ratio[0][p]) < 1e-8 * abs(ratio[0][0] * ratio[i][p])


def test_result_is_projectively_equivalent_to_the_truth():
    _, sc = make_scene(4, n_cams=3, n_pts=15)
    res = sturm_triggs_factorization(sc["x"])
    # find H with X_true ~ H X_rec by the DLT: for each pair of coordinates
    # (i, j), X_true[i] (H X_rec)[j] - X_true[j] (H X_rec)[i] = 0
    xr = res["X"]
    xt = [x + [1.0] for x in sc["X"]]
    rows = []
    for a, b in zip(xr, xt):
        for i in range(4):
            for j in range(i + 1, 4):
                r = [0.0] * 16
                for k in range(4):
                    r[4 * j + k] += b[i] * a[k]
                    r[4 * i + k] -= b[j] * a[k]
                rows.append(r)
    _, s, v = svd(rows)
    assert s[15] < 1e-9 * s[0]
    h = [[v[4 * i + k][15] for k in range(4)] for i in range(4)]
    for a, b in zip(xr, xt):
        y = matvec(h, a)
        y = [c / y[3] for c in y]
        assert max(abs(c - d) for c, d in zip(y, b)) < 1e-6


def test_noise_gives_small_reprojection_errors():
    rng, sc = make_scene(5, n_cams=4, n_pts=30)
    obs = [add_noise(rng, f, 0.5) for f in sc["x"]]
    res = sturm_triggs_factorization(obs)
    err = reprojection_errors(res["P"], res["X"], obs)
    rms = math.sqrt(sum(e * e for e in err) / len(err))
    assert rms < 2.0


def test_two_images_are_enough():
    _, sc = make_scene(6, n_cams=2, n_pts=12)
    res = sturm_triggs_factorization(sc["x"])
    assert max(reprojection_errors(res["P"], res["X"], sc["x"])) < 1e-6


def test_too_few_points_are_rejected():
    _, sc = make_scene(7, n_cams=3, n_pts=7)
    with pytest.raises(ValueError):
        sturm_triggs_factorization(sc["x"])


def test_unit_depths_break_the_rank():
    # with all depths set to 1 (the affine guess), W of perspective data has rank above 4
    _, sc = make_scene(8, n_cams=4, n_pts=20, distance=2.5)
    ts = [normalizing_transform(f) for f in sc["x"]]
    w = []
    for t, f in zip(ts, sc["x"]):
        pts = [apply(t, p) for p in f]
        for k in range(3):
            w.append([p[k] for p in pts])
    s = svd(w)[1]
    assert s[4] > 1e-4 * s[0]
    res = sturm_triggs_factorization(sc["x"])
    assert res["S"][4] < 1e-9 * res["S"][0]
