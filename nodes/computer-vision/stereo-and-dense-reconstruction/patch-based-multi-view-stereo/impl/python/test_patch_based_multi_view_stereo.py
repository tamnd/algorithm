# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/patch-based-multi-view-stereo/. The authors are listed in prov/22G2KD.jsonl.

import functools
import math
import random

from patch_based_multi_view_stereo import (
    Model,
    Params,
    Patch,
    center,
    dot,
    expand,
    filter_patches,
    match,
    midpoint_triangulate,
    neighbors,
    pmvs,
    project,
    ray,
    sub,
    unit,
)

W = H = 24
K = [[40.0, 0.0, 11.5], [0.0, 40.0, 11.5], [0.0, 0.0, 1.0]]
I3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]

# The plane Z = 4 + 0.15 X - 0.1 Y, written as N . X = D with a unit N.
N = unit([-0.15, 0.1, 1.0])
D = 4.0 * N[2]


def texture(seed):
    rng = random.Random(seed)
    waves = []
    for _ in range(5):
        period = rng.uniform(0.3, 0.8)
        ang = rng.uniform(0.0, math.pi)
        k = 2.0 * math.pi / period
        waves.append((k * math.cos(ang), k * math.sin(ang), rng.uniform(0.0, 6.3), rng.uniform(15.0, 25.0)))

    def g(a, b):
        return 128.0 + sum(amp * math.sin(kx * a + ky * b + ph) for kx, ky, ph, amp in waves)

    return g


def camera(c, R=I3):
    t = [-sum(R[i][j] * c[j] for j in range(3)) for i in range(3)]
    return (K, R, t)


def render(cam, tex):
    C = center(cam)
    img = [[0.0] * W for _ in range(H)]
    for v in range(H):
        for u in range(W):
            d = ray(cam, u, v)
            s = (D - dot(N, C)) / dot(N, d)
            X = [C[k] + s * d[k] for k in range(3)]
            img[v][u] = tex(X[0], X[1])
    return img


def scene(extra_features=True):
    tex = texture(1)
    cams = [camera([0.0, 0.0, 0.0]), camera([0.5, 0.0, 0.0]), camera([0.1, 0.45, 0.0])]
    images = [render(c, tex) for c in cams]
    pts = []
    for X in (-0.5, 0.0, 0.5):
        for Y in (-0.4, 0.4):
            pts.append([X, Y, 4.0 + 0.15 * X - 0.1 * Y])
    rng = random.Random(2)
    features = []
    for cam in cams:
        f = [project(cam, X) for X in pts]
        f = [q for q in f if 0 <= q[0] <= W - 1 and 0 <= q[1] <= H - 1]
        if extra_features:
            f += [(rng.uniform(2, W - 3), rng.uniform(2, H - 3)) for _ in range(2)]
        features.append(f)
    return images, cams, features


def on_plane(X):
    return dot(N, X) - D


def test_midpoint_triangulation() -> None:
    rng = random.Random(4)
    for _ in range(50):
        X = [rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(3, 5)]
        c1, c2 = [rng.uniform(-1, 1), 0.0, 0.0], [0.0, rng.uniform(-1, 1), 0.5]
        Y = midpoint_triangulate(c1, unit(sub(X, c1)), c2, unit(sub(X, c2)))
        assert max(abs(a - b) for a, b in zip(X, Y)) < 1e-9


def test_ray_and_project() -> None:
    cam = camera([0.3, -0.2, 0.1])
    C = center(cam)
    for u, v in ((0.0, 0.0), (11.5, 11.5), (20.25, 3.5)):
        d = ray(cam, u, v)
        q = project(cam, [C[k] + 3.0 * d[k] for k in range(3)])
        assert abs(q[0] - u) < 1e-9 and abs(q[1] - v) < 1e-9


@functools.lru_cache(maxsize=None)
def full_run():
    images, cams, features = scene()
    model = Model(images, cams, Params())
    match(model, features)
    matched = len(model.patches)
    for _ in range(model.prm.rounds):
        expand(model, model.patches)
        filter_patches(model)
    return model, matched


def test_discrepancy_is_low_on_the_surface() -> None:
    images, cams, _ = scene()
    model = Model(images, cams, Params())
    X = [0.1, 0.05, 4.0 + 0.015 - 0.005]
    p = Patch(X, [-x for x in N], 0)
    p.V = model.visible(p)
    assert p.V == [0, 1, 2]
    g = {}
    for s in (0.9, 0.95, 1.0, 1.05, 1.1):
        p.c = [x * s for x in X]          # move it along the reference ray
        g[s] = model.g_star(p, p.V)
    assert g[1.0] < 0.01
    assert min(g, key=g.get) == 1.0


def test_reconstruction() -> None:
    model, matched = full_run()
    prm = model.prm
    ps = model.patches
    assert matched == 6
    assert len(ps) >= 40
    errs = sorted(abs(on_plane(p.c)) for p in ps)
    coss = sorted(-dot(p.n, N) for p in ps)
    assert errs[-1] < 0.1 and errs[len(errs) // 2] < 0.03      # 0.1 is one pixel at Z = 4
    assert coss[0] > 0.5 and coss[len(coss) // 2] > 0.95
    for p in ps:
        assert len(p.Vs) >= prm.gamma and p.ref in p.Vs
        assert p.g <= prm.alpha
    # Coverage of the cells of the reference image that the other images also see.
    covered = total = 0
    for cx in range(1, 7):
        for cy in range(1, 7):
            total += 1
            covered += bool(model.cells[0].get((cx, cy)))
    assert covered >= 0.8 * total


def copy_model():
    done, _ = full_run()
    model = Model(done.images, done.cams, Params())
    for p in done.patches:
        q = Patch(list(p.c), list(p.n), p.ref)
        q.V, q.Vs, q.g = list(p.V), list(p.Vs), p.g
        model.register(q)
    return model


def test_filter_keeps_a_clean_model() -> None:
    model = copy_model()
    assert filter_patches(model) == 0


def test_filter_removes_an_outlier() -> None:
    model = copy_model()
    count = len(model.patches)
    # A patch 0.4 in front of the plane, put in by hand into a full region.
    X = [0.0, 0.0, 3.6]
    bad = Patch(X, [0.0, 0.0, -1.0], 0)
    bad.V = bad.Vs = [0, 1, 2]
    model.register(bad)
    removed = filter_patches(model)
    assert bad not in model.patches
    assert removed <= 1 + count // 20
    for i in range(3):
        for lst in model.cells[i].values():
            assert all(q is not bad for q in lst)


def test_neighbors_relation() -> None:
    a = Patch([0.0, 0.0, 4.0], [0.0, 0.0, -1.0], 0)
    b = Patch([0.3, 0.0, 4.0], [0.0, 0.0, -1.0], 0)
    c = Patch([0.3, 0.0, 4.3], [0.0, 0.0, -1.0], 0)
    assert neighbors(a, b, 0.1) and neighbors(b, a, 0.1)
    assert not neighbors(a, c, 0.1)


def test_cells_and_termination() -> None:
    model, _ = full_run()
    # Every patch sits in the cell of its projection in each image of V*,
    # and expanding again from a finished model adds nothing.
    for p in model.patches:
        for i in p.Vs:
            assert any(q is p for q in model.cells[i][model.cell_of(i, p.c)])
    copy = copy_model()
    before = len(copy.patches)
    expand(copy, copy.patches)
    assert len(copy.patches) == before


def test_deterministic() -> None:
    images, cams, features = scene()
    m1 = pmvs(images, cams, features, Params(rounds=1))
    m2, _ = full_run()
    assert [p.c for p in m1.patches] == [p.c for p in m2.patches]
