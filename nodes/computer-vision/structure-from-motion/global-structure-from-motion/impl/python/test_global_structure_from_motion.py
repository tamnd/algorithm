# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/global-structure-from-motion/. The authors are listed in prov/JSXC11.jsonl.

import math
import random

from cvgeom import axis_angle_to_R, make_K, random_scene, rot_x, rot_y
from cvla import det, inv, matvec, mul, svd, sym_eig, transpose
from global_structure_from_motion import (angle, average_rotations, direction_matrix, directions,
                                          filter_edges, global_structure_from_motion, normalize,
                                          reproj_error, translation_averaging)


def ring_cameras():
    """Five cameras on a sphere of radius 3 around the origin, looking at it."""
    k = make_K(800, 800, 320, 240)
    cams = []
    for a, b in [(-0.4, 0.0), (-0.2, 0.25), (0.0, -0.25), (0.2, 0.25), (0.4, 0.0)]:
        q = mul(rot_y(a), rot_x(b))
        r = transpose(q)
        c = matvec(q, [0.0, 0.0, -3.0])
        cams.append((k, r, [-x for x in matvec(r, c)]))
    return cams


def make_tracks(seed, n_pts=40, visible=0.8, noise=0.0, outliers=0.0):
    rng = random.Random(seed)
    sc = random_scene(rng, n=n_pts, cams=ring_cameras())
    n_cams = 5
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


def aligned_error(src, dst):
    s, r, t = umeyama(src, dst)
    return max(math.dist([s * x + t[a] for a, x in enumerate(matvec(r, p))], q) for p, q in zip(src, dst))


def center(pose):
    r, t = pose
    return [-x for x in matvec(transpose(r), t)]


def exact_relative(sc, pairs):
    rel = {}
    for i, j in pairs:
        rij = mul(sc["R"][j], transpose(sc["R"][i]))
        tij = [sc["t"][j][a] - sum(rij[a][b] * sc["t"][i][b] for b in range(3)) for a in range(3)]
        n = math.sqrt(sum(x * x for x in tij))
        rel[(i, j)] = (rij, [x / n for x in tij])
    return rel


def test_exact_tracks_give_the_true_scene_up_to_similarity():
    sc, tracks = make_tracks(1)
    cams, pts, obs = global_structure_from_motion(sc["K"][0], tracks)
    assert sorted(cams) == list(range(5))
    assert len(pts) == 40
    js = sorted(pts)
    assert aligned_error([pts[j] for j in js], [sc["X"][j] for j in js]) < 1e-6
    assert cams[0][0] == [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


def test_noise_and_outliers():
    sc, tracks = make_tracks(2, noise=0.5, outliers=0.05)
    cams, pts, obs = global_structure_from_motion(sc["K"][0], tracks)
    assert sorted(cams) == list(range(5))
    assert len(pts) >= 34
    f = sc["K"][0][0][0]
    kinv = inv(sc["K"][0])
    errs = [reproj_error(cams[i], pts[j], normalize(kinv, tracks[j][i])) * f for i, j in obs]
    assert max(errs) < 3.0
    assert math.sqrt(sum(e * e for e in errs) / len(errs)) < 1.0
    js = sorted(pts)
    assert aligned_error([pts[j] for j in js], [sc["X"][j] for j in js]) < 0.05
    assert aligned_error([center(cams[i]) for i in range(5)],
                         [center((sc["R"][i], sc["t"][i])) for i in range(5)]) < 0.1


def test_the_edge_filter_removes_a_wrong_relative_rotation():
    sc = random_scene(random.Random(3), n=4, n_cams=6, max_angle=0.6)
    pairs = [(i, j) for i in range(6) for j in range(i + 1, 6)]
    rel = exact_relative(sc, pairs)
    r, t = rel[(1, 4)]
    rel[(1, 4)] = (mul(axis_angle_to_R([1.0, 2.0, 0.5], 0.5), r), t)
    rots = average_rotations(6, [(i, j, r) for (i, j), (r, _) in rel.items()])
    for k in range(6):
        # R_k = R_k^true R_0^true^T, since R_0 = I. The Geman-McClure cost
        # keeps a small pull from the wrong edge, so the match is not exact.
        assert angle(rots[k], mul(sc["R"][k], transpose(sc["R"][0]))) < 2e-3
    kept = filter_edges(rots, rel, 0.1)
    assert sorted(kept) == [p for p in pairs if p != (1, 4)]


def test_translation_averaging_on_exact_directions():
    sc = random_scene(random.Random(4), n=4, n_cams=6, max_angle=0.8)
    rots = [mul(r, transpose(sc["R"][0])) for r in sc["R"]]
    pairs = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5), (0, 2), (1, 3), (2, 4), (3, 5)]
    rel = exact_relative(sc, pairs)
    cs = translation_averaging(6, directions(rots, rel))
    true = [matvec(sc["R"][0], [a - b for a, b in zip(center((sc["R"][k], sc["t"][k])),
                                                        center((sc["R"][0], sc["t"][0])))])
            for k in range(6)]
    s = math.sqrt(sum(x * x for c in true for x in c))
    assert max(abs(a - b / s) for c, d in zip(cs, true) for a, b in zip(c, d)) < 1e-9


def test_a_tree_of_directions_does_not_fix_the_centers():
    sc = random_scene(random.Random(5), n=4, n_cams=4, max_angle=0.8)
    rots = [mul(r, transpose(sc["R"][0])) for r in sc["R"]]
    chain = directions(rots, exact_relative(sc, [(0, 1), (1, 2), (2, 3)]))
    w, _ = sym_eig(direction_matrix(4, chain))
    assert sum(1 for x in w if abs(x) < 1e-9) == 3
    full = directions(rots, exact_relative(sc, [(0, 1), (1, 2), (2, 3), (0, 3)]))
    w, _ = sym_eig(direction_matrix(4, full))
    assert sum(1 for x in w if abs(x) < 1e-9) == 1
