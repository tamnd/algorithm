# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tomasi-kanade-factorization/. The authors are listed in prov/0876R2.jsonl.

import math
import random

import pytest

from cvgeom import axis_angle_to_R, random_rotation
from cvla import dot, mul, svd, transpose
from tomasi_kanade_factorization import (measurement_matrix, metric_rows, reproject,
                                         tomasi_kanade_factorization)


def make_tracks(seed, n_frames=5, n_pts=12, noise=0.0, max_angle=0.6):
    rng = random.Random(seed)
    pts = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(n_pts)]
    base = random_rotation(rng)
    rots = []
    for _ in range(n_frames):
        axis = [rng.gauss(0, 1) for _ in range(3)]
        rots.append(mul(axis_angle_to_R(axis, rng.uniform(0, max_angle)), base))
    obs = []
    for r in rots:
        a, b = rng.uniform(-5, 5), rng.uniform(-5, 5)
        obs.append([(dot(r[0], p) + a + rng.gauss(0, noise) if noise else dot(r[0], p) + a,
                     dot(r[1], p) + b + rng.gauss(0, noise) if noise else dot(r[1], p) + b)
                    for p in pts])
    return pts, rots, obs


def distances(pts):
    return [math.dist(p, q) for i, p in enumerate(pts) for q in pts[i + 1:]]


def test_exact_tracks_give_the_true_shape():
    for seed in range(3):
        pts, _, obs = make_tracks(seed)
        res = tomasi_kanade_factorization(obs)
        # the centered matrix has rank 3
        assert res["S"][3] < 1e-9 * res["S"][0]
        # M X + t reproduces W
        w = measurement_matrix(obs)
        rep = reproject(res)
        assert max(abs(a - b) for ra, rb in zip(w, rep) for a, b in zip(ra, rb)) < 1e-9
        # the shape is right up to a rotation, a translation and a reflection
        for d1, d2 in zip(distances(pts), distances(res["X"])):
            assert abs(d1 - d2) < 1e-8


def test_rows_are_orthonormal_and_frame_zero_is_fixed():
    _, _, obs = make_tracks(4, n_frames=6)
    res = tomasi_kanade_factorization(obs)
    m = res["M"]
    for f in range(6):
        a, b = m[2 * f], m[2 * f + 1]
        assert abs(dot(a, a) - 1) < 1e-9 and abs(dot(b, b) - 1) < 1e-9
        assert abs(dot(a, b)) < 1e-9
    assert max(abs(x - y) for x, y in zip(m[0] + m[1], [1, 0, 0, 0, 1, 0])) < 1e-9


def test_true_rotations_up_to_one_world_rotation():
    _, rots, obs = make_tracks(5, n_frames=4)
    m = tomasi_kanade_factorization(obs)["M"]
    # M_f = rows of R_f G for one orthogonal G; G = R_0^T [m_0; m_1; m_0 x m_1] up to a mirror
    for f in range(4):
        for k in (0, 1):
            # inner products between all camera rows are invariant under G
            for g in range(4):
                for l in (0, 1):
                    want = dot(rots[f][k], rots[g][l])
                    got = dot(m[2 * f + k], m[2 * g + l])
                    assert abs(want - got) < 1e-9


def test_noise_gives_a_small_error():
    pts, _, obs = make_tracks(7, n_frames=8, n_pts=20, noise=0.002)
    res = tomasi_kanade_factorization(obs)
    err = max(abs(d1 - d2) for d1, d2 in zip(distances(pts), distances(res["X"])))
    assert err < 0.02
    # the fourth singular value is at the noise level
    assert res["S"][3] < 0.05 * res["S"][2]


def test_two_frames_do_not_fix_the_metric_matrix():
    _, _, obs = make_tracks(8, n_frames=2)
    w = measurement_matrix(obs)
    n = len(w[0])
    t = [sum(r) / n for r in w]
    u, s, _ = svd([[x - tr for x in r] for r, tr in zip(w, t)])
    m_hat = [[u[i][k] * math.sqrt(s[k]) for k in range(min(3, len(s)))] for i in range(4)]
    g = metric_rows(m_hat)
    sv = svd(g)[1]
    # 6 equations in 6 unknowns, but only rank 5: a one-parameter family remains
    assert sv[4] > 1e-6 * sv[0]
    assert sv[5] < 1e-9 * sv[0]
    with pytest.raises(ValueError):
        tomasi_kanade_factorization(obs)


def test_mirror_shape_fits_equally_well():
    pts, _, obs = make_tracks(9)
    res = tomasi_kanade_factorization(obs)
    # flipping depth and the third column of M gives the same image data
    m2 = [[r[0], r[1], -r[2]] for r in res["M"]]
    x2 = [[p[0], p[1], -p[2]] for p in res["X"]]
    rep1 = reproject(res)
    rep2 = reproject({"M": m2, "t": res["t"], "X": x2})
    assert max(abs(a - b) for ra, rb in zip(rep1, rep2) for a, b in zip(ra, rb)) < 1e-12
    for f in range(len(m2) // 2):
        assert abs(dot(m2[2 * f], m2[2 * f + 1])) < 1e-9
