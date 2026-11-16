# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-structure-from-motion/. The authors are listed in prov/K15KYC.jsonl.

import math
import random

from cvgeom import random_scene
from cvla import det, inv, matvec, mul, svd, transpose
from incremental_structure_from_motion import (EYE3, ba_cost, bundle_adjust, dlt_pnp,
                                               incremental_structure_from_motion, normalize,
                                               relative_pose_ransac, reproj_error)


def make_tracks(seed, n_cams=5, n_pts=40, visible=0.8, noise=0.0, outliers=0.0):
    rng = random.Random(seed)
    sc = random_scene(rng, n=n_pts, n_cams=n_cams, max_angle=0.5, distance=5.0)
    tracks = []
    for j in range(n_pts):
        views = [i for i in range(n_cams) if rng.random() < visible]
        if len(views) < 2:
            views = rng.sample(range(n_cams), 2)
        tr = {}
        for i in views:
            u, v = sc["x"][i][j]
            if rng.random() < outliers:
                u, v = rng.uniform(0, 640), rng.uniform(0, 480)
            else:
                u, v = u + rng.gauss(0, noise), v + rng.gauss(0, noise)
            tr[i] = (u, v)
        tracks.append(tr)
    return sc, tracks


def umeyama(src, dst):
    """s, R, t minimizing sum ||s R src + t - dst||^2."""
    n = len(src)
    ms = [sum(p[a] for p in src) / n for a in range(3)]
    md = [sum(p[a] for p in dst) / n for a in range(3)]
    cov = [[sum((d[a] - md[a]) * (s[b] - ms[b]) for s, d in zip(src, dst)) / n for b in range(3)]
           for a in range(3)]
    u, sv, v = svd(cov)
    sgn = [1.0, 1.0, 1.0 if det(mul(u, transpose(v))) > 0 else -1.0]
    r = mul(mul(u, [[sgn[0], 0, 0], [0, sgn[1], 0], [0, 0, sgn[2]]]), transpose(v))
    var = sum(sum((p[a] - ms[a]) ** 2 for a in range(3)) for p in src) / n
    s = sum(x * g for x, g in zip(sv, sgn)) / var
    t = [md[a] - s * sum(r[a][b] * ms[b] for b in range(3)) for a in range(3)]
    return s, r, t


def point_error(sc, pts):
    js = sorted(pts)
    s, r, t = umeyama([pts[j] for j in js], [sc["X"][j] for j in js])
    errs = [math.dist([s * x + t[a] for a, x in enumerate(matvec(r, pts[j]))], sc["X"][j]) for j in js]
    return max(errs)


def test_exact_tracks_give_the_true_scene_up_to_similarity():
    sc, tracks = make_tracks(1)
    cams, pts, obs = incremental_structure_from_motion(sc["K"][0], tracks)
    assert sorted(cams) == list(range(5))
    assert len(pts) == 40
    assert point_error(sc, pts) < 1e-6
    a = [i for i in cams if cams[i][0] == EYE3 and cams[i][1] == [0.0, 0.0, 0.0]]
    assert len(a) == 1


def test_noise_and_outliers():
    sc, tracks = make_tracks(2, n_cams=5, n_pts=40, noise=0.5, outliers=0.05)
    cams, pts, obs = incremental_structure_from_motion(sc["K"][0], tracks, tau_px=3.0)
    assert sorted(cams) == list(range(5))
    assert len(pts) >= 34
    f = sc["K"][0][0][0]
    kinv = inv(sc["K"][0])
    errs = [reproj_error(cams[i], pts[j], normalize(kinv, tracks[j][i])) * f for i, j in obs]
    assert max(errs) < 3.0
    assert math.sqrt(sum(e * e for e in errs) / len(errs)) < 1.0
    # the shape error is small compared with the scene size of 2 units
    assert point_error(sc, pts) < 0.05


def test_relative_pose_matches_the_truth():
    rng = random.Random(3)
    sc = random_scene(rng, n=30, n_cams=2, first_identity=True, max_angle=0.5)
    kinv = inv(sc["K"][0])
    x1 = [normalize(kinv, p) for p in sc["x"][0]]
    x2 = [normalize(kinv, p) for p in sc["x"][1]]
    (r, t), inl = relative_pose_ransac(x1, x2, 1e-3, rng)
    assert len(inl) == 30
    tt = sc["t"][1]
    n = math.sqrt(sum(v * v for v in tt))
    assert max(abs(a - b) for ra, rb in zip(r, sc["R"][1]) for a, b in zip(ra, rb)) < 1e-8
    assert max(abs(a - b / n) for a, b in zip(t, tt)) < 1e-8


def test_dlt_pnp_is_exact_on_exact_data():
    rng = random.Random(4)
    sc = random_scene(rng, n=10, n_cams=1, max_angle=1.0)
    kinv = inv(sc["K"][0])
    r, t = dlt_pnp(sc["X"], [normalize(kinv, p) for p in sc["x"][0]])
    assert max(abs(a - b) for ra, rb in zip(r, sc["R"][0]) for a, b in zip(ra, rb)) < 1e-8
    assert max(abs(a - b) for a, b in zip(t, sc["t"][0])) < 1e-8


def test_bundle_adjustment_lowers_the_cost():
    sc, tracks = make_tracks(5, n_cams=3, n_pts=15, visible=1.0, noise=1.0)
    kinv = inv(sc["K"][0])
    rng = random.Random(5)
    cams = {i: (sc["R"][i], sc["t"][i]) for i in range(3)}
    pts = {j: [x + rng.gauss(0, 0.05) for x in sc["X"][j]] for j in range(15)}
    obs = {(i, j): normalize(kinv, tracks[j][i]) for j in range(15) for i in tracks[j]}
    f0 = ba_cost(cams, pts, obs)
    cams2, pts2 = bundle_adjust(cams, pts, obs, 0)
    assert ba_cost(cams2, pts2, obs) < 0.01 * f0
