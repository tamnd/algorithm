# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asd-pocs/. The authors are listed in prov/4RF9RF.jsonl.

import math
import random

import imgkit as ik
from asd_pocs import asd_pocs, residual_norm, tv, tv_grad

# Three ellipses, values 0, 0.5, 1 and 1.5: a piecewise constant phantom.
TABLE = [
    (1.0, 0.7, 0.5, 0.0, 0.0, 0.0),
    (0.5, 0.25, 0.25, 0.25, 0.1, 0.0),
    (-0.5, 0.15, 0.3, -0.3, -0.05, 0.0),
]


def test_tv_values() -> None:
    n = 4
    assert abs(tv([2.0] * (n * n), n, eta=0.5) - n * n * 0.5) < 1e-12
    # left half 0, right half 1: one unit jump in each row
    step = [0.0 if j < n // 2 else 1.0 for i in range(n) for j in range(n)]
    assert abs(tv(step, n, eta=1e-12) - n) < 1e-9


def test_tv_gradient_matches_finite_differences() -> None:
    rng = random.Random(1)
    n, eta, h = 5, 0.1, 1e-6
    x = [rng.uniform(0, 1) for _ in range(n * n)]
    g = tv_grad(x, n, eta)
    for k in range(n * n):
        xp, xm = list(x), list(x)
        xp[k] += h
        xm[k] -= h
        fd = (tv(xp, n, eta) - tv(xm, n, eta)) / (2 * h)
        assert abs(fd - g[k]) < 1e-6


def test_without_tv_steps_it_is_art_with_positivity() -> None:
    # a consistent 2 x 2 system: rows, columns and the two diagonals
    rows = [
        [(0, 1.0), (1, 1.0)], [(2, 1.0), (3, 1.0)], [(0, 1.0), (2, 1.0)],
        [(1, 1.0), (3, 1.0)], [(0, 1.0), (3, 1.0)], [(1, 1.0), (2, 1.0)],
    ]
    xt = [1.0, 2.0, 3.0, 5.0]
    y = [sum(w * xt[j] for j, w in row) for row in rows]
    x = asd_pocs(rows, 2, y, eps=0.0, iters=200, beta_red=1.0, ng=0)
    assert max(abs(a - b) for a, b in zip(x, xt)) < 1e-9
    # one sweep by hand: the first ray sets x0 = x1 = 3/2, the second x2 = x3 = 4, ...
    seen = []
    asd_pocs(rows[:2], 2, y[:2], eps=0.0, iters=1, ng=0, callback=lambda k, x, dd: seen.append(x))
    assert seen[0] == [1.5, 1.5, 4.0, 4.0]


def test_sparse_view_phantom_beats_art() -> None:
    n, nbins, na, iters = 16, 23, 6, 200
    rows = ik.parallel_beam_matrix(n, [k * math.pi / na for k in range(na)], nbins)
    xt = ik.flatten(ik.ellipse_phantom(n, TABLE))
    y = ik.sp_matvec(rows, xt)
    eps = 1e-3 * math.sqrt(sum(t * t for t in y))
    nt = math.sqrt(sum(t * t for t in xt))
    art = asd_pocs(rows, n, y, eps, iters=iters, ng=0)
    tvr = asd_pocs(rows, n, y, eps, iters=iters, ng=10, alpha=0.05)
    e_art = math.dist(art, xt) / nt
    e_tv = math.dist(tvr, xt) / nt
    # measured: 0.068 for ART and 0.050 for ASD-POCS
    assert e_tv < 0.8 * e_art
    assert tv(tvr, n) < tv(art, n)
    assert min(tvr) >= 0.0
    assert residual_norm(rows, y, tvr) < 0.05


def test_positivity_holds_with_noisy_data() -> None:
    n, nbins, na = 8, 13, 4
    rows = ik.parallel_beam_matrix(n, [k * math.pi / na for k in range(na)], nbins)
    rng = random.Random(2)
    xt = ik.flatten(ik.disk_phantom(n, 0.5))
    y = [t + rng.gauss(0.0, 0.05) for t in ik.sp_matvec(rows, xt)]
    x = asd_pocs(rows, n, y, eps=0.05 * math.sqrt(len(y)), iters=30)
    assert min(x) >= 0.0
