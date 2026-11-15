# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rankboost/. The authors are listed in prov/FQ86DQ.jsonl.

import math
import random

from rankboost import (
    alpha_of,
    best_weak_ranker,
    crucial_pairs,
    fit,
    method2_alpha,
    method2_z,
    r_value,
    ranking_loss,
    w_values,
    weak,
)

EXAMPLE = [([[0.0, 1.0], [1.0, 0.0], [2.0, 2.0], [3.0, 1.0]], [0, 1, 2, 1])]


def random_queries(seed, n_queries=4, n_docs=6, d=3):
    rng = random.Random(seed)
    queries = []
    for _ in range(n_queries):
        xs = [[rng.randint(0, 9) / 9.0 for _ in range(d)] for _ in range(n_docs)]
        y = [rng.randint(0, 2) for _ in range(n_docs)]
        queries.append((xs, y))
    return queries


def replay(queries, model):
    """The distributions D_1, ..., D_T recomputed from the fitted model."""
    pts = crucial_pairs(queries)
    dist = [1.0 / len(pts)] * len(pts)
    out = []
    for a, f, theta in model:
        out.append(dist)
        h = weak(f, theta)
        new = [d * math.exp(a * (h(x0) - h(x1))) for d, (x0, x1) in zip(dist, pts)]
        z = sum(new)
        dist = [v / z for v in new]
    return pts, out


def test_page_example():
    pts = crucial_pairs(EXAMPLE)
    assert len(pts) == 5
    model, zs = fit(EXAMPLE, 2)
    a1, f1, t1 = model[0]
    assert (f1, t1) == (0, 0.5)
    assert abs(a1 - math.log(2)) < 1e-12
    assert abs(zs[0] - 0.7) < 1e-12
    assert (model[1][1], model[1][2]) == (1, 1.5)
    assert abs(ranking_loss(model[:1], pts) - 0.4) < 1e-12
    assert ranking_loss(model, pts) == 0.0


def test_weak_ranker_is_brute_force_best():
    for seed in range(5):
        queries = random_queries(seed)
        model, _ = fit(queries, 4)
        pts, dists = replay(queries, model)
        for (a, f, theta), dist in zip(model, dists):
            r = r_value(weak(f, theta), pts, dist)
            values = sorted(set(v for p in pts for x in p for v in x))
            for ff in range(3):
                for tt in values:
                    assert abs(r_value(weak(ff, tt), pts, dist)) <= abs(r) + 1e-12
            assert abs(a - 0.5 * math.log((1 + r) / (1 - r))) < 1e-12


def test_z_matches_formula_and_square_root_bound():
    for seed in range(5):
        queries = random_queries(seed + 10)
        model, zs = fit(queries, 5)
        pts, dists = replay(queries, model)
        for (a, f, theta), dist, z in zip(model, dists, zs):
            h = weak(f, theta)
            direct = sum(d * math.exp(a * (h(x0) - h(x1))) for d, (x0, x1) in zip(dist, pts))
            assert abs(direct - z) < 1e-12
            r = r_value(h, pts, dist)
            assert z <= math.sqrt(1 - r * r) + 1e-12
            w = w_values(h, pts, dist)
            assert abs(r - (w[-1] - w[1])) < 1e-12


def test_ranking_loss_bounded_by_product_of_z():
    for seed in range(5):
        queries = random_queries(seed + 20)
        pts = crucial_pairs(queries)
        model, zs = fit(queries, 8)
        prod = 1.0
        for t in range(1, len(model) + 1):
            prod *= zs[t - 1]
            assert ranking_loss(model[:t], pts) <= prod + 1e-12


def test_method2_alpha_minimizes_z():
    queries = random_queries(30)
    pts = crucial_pairs(queries)
    dist = [1.0 / len(pts)] * len(pts)
    f, theta, _ = best_weak_ranker(pts, dist)
    h = weak(f, theta)
    w = w_values(h, pts, dist)
    a = method2_alpha(w)

    def z(alpha):
        return w[-1] * math.exp(-alpha) + w[0] + w[1] * math.exp(alpha)

    assert abs(z(a) - method2_z(w)) < 1e-12
    grid = [i / 1000.0 for i in range(-3000, 3001)]
    assert all(z(a) <= z(b) + 1e-12 for b in grid)


def test_clipping_of_perfect_weak_ranker():
    # One weak ranker orders every pair, so r = 1 and alpha is clipped.
    queries = [([[0.0], [1.0]], [0, 1])]
    model, zs = fit(queries, 1)
    assert math.isfinite(model[0][0]) and model[0][0] > 10
    assert alpha_of(1.0) == alpha_of(2.0)


def test_ties_count_as_errors():
    pts = crucial_pairs([([[0.0], [0.0]], [0, 1])])
    assert ranking_loss([], pts) == 1.0
