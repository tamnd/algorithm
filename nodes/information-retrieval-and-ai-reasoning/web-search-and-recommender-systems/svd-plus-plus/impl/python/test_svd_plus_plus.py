# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/svd-plus-plus/. The authors are listed in prov/87CAT3.jsonl.

import math
import random

import recs
import svd_plus_plus as spp

H = 1e-6  # step of the central differences
TOL = 1e-6  # allowed gap, relative to max(1, |gradient entry|)


def random_model(m, n, r, train, seed, implicit=None):
    rng = random.Random(seed)
    model = spp.init(m, n, r, train, seed, implicit, scale=0.5)
    model.bu = [rng.uniform(-0.5, 0.5) for _ in range(m)]
    model.bi = [rng.uniform(-0.5, 0.5) for _ in range(n)]
    return model


def params(model):
    out = [(model.bu, u) for u in range(model.m)]
    out += [(model.bi, i) for i in range(model.n)]
    for mat in (model.p, model.q, model.y):
        out += [(row, f) for row in mat for f in range(model.r)]
    return out


def flat_gradient(model, train, lb, lf):
    gbu, gbi, gp, gq, gy = spp.gradient(model, train, lb, lf)
    out = gbu + gbi
    for row in gp + gq + gy:
        out += row
    return out


def test_gradient_matches_central_differences():
    full = recs.planted(5, 5, 2, 7, noise=0.2)
    train, _ = recs.split(full, 0.3, 7)
    # Implicit sets with an item the user did not rate.
    implicit = spp.implicit_from(train)
    implicit[0] = sorted(set(implicit[0]) | {4})
    model = random_model(5, 5, 2, train, 3, implicit)
    lb, lf = 0.1, 0.3
    g = flat_gradient(model, train, lb, lf)
    for (vec, k), gk in zip(params(model), g):
        old = vec[k]
        vec[k] = old + H
        up = spp.objective(model, train, lb, lf)
        vec[k] = old - H
        down = spp.objective(model, train, lb, lf)
        vec[k] = old
        assert abs((up - down) / (2 * H) - gk) <= TOL * max(1.0, abs(gk))


def test_sgd_step_is_half_gradient_step_on_one_rating():
    full = recs.planted(4, 5, 2, 9)
    train, _ = recs.split(full, 0.3, 9)
    lb, lf, gamma = 0.05, 0.1, 0.03
    for (u, i), v in sorted(train.items()):
        model = random_model(4, 5, 2, train, 10 * u + i)
        g = flat_gradient(model, {(u, i): v}, lb, lf)
        before = [vec[k] for vec, k in params(model)]
        spp.sgd_step(model, u, i, v, lb, lf, gamma)
        after = [vec[k] for vec, k in params(model)]
        for b, a, gk in zip(before, after, g):
            assert abs(a - (b - gamma / 2 * gk)) < 1e-12


def test_reduces_to_biased_factorization():
    """With every N(u) empty, SVD++ is the biased model trained the same way."""
    full = recs.planted(6, 5, 2, 2, noise=0.2)
    train, _ = recs.split(full, 0.3, 2)
    model = random_model(6, 5, 2, train, 5, implicit={})
    lam, gamma = 0.05, 0.02
    twin = {"bu": model.bu[:], "bi": model.bi[:], "p": [r[:] for r in model.p], "q": [r[:] for r in model.q]}
    order = sorted(train)
    random.Random(1).shuffle(order)
    spp.sgd_epoch(model, train, lam, lam, gamma, order)
    for u, i in order:  # the biased factorization step, written out
        v = train[(u, i)]
        e = v - (model.mu + twin["bu"][u] + twin["bi"][i] + sum(a * b for a, b in zip(twin["p"][u], twin["q"][i])))
        twin["bu"][u] += gamma * (e - lam * twin["bu"][u])
        twin["bi"][i] += gamma * (e - lam * twin["bi"][i])
        pu, qi = twin["p"][u], twin["q"][i]
        for f in range(2):
            a, b = pu[f], qi[f]
            pu[f] = a + gamma * (e * b - lam * a)
            qi[f] = b + gamma * (e * a - lam * b)
    assert all(abs(a - b) < 1e-12 for a, b in zip(model.bu, twin["bu"]))
    assert all(abs(a - b) < 1e-12 for a, b in zip(model.bi, twin["bi"]))
    for mat, other in ((model.p, twin["p"]), (model.q, twin["q"])):
        for ra, rb in zip(mat, other):
            assert all(abs(a - b) < 1e-12 for a, b in zip(ra, rb))


def test_toy_user_vector():
    train = recs.toy()
    model = spp.Model(4, 4, 1, 3.0, spp.implicit_from(train))
    model.bu = [0.2, 0.5, -0.5, -1.0]
    model.p = [[0.5], [0.5], [-0.5], [-0.5]]
    model.q = [[1.0], [1.0], [1.0], [-1.0]]
    model.y = [[0.4], [0.4], [0.4], [-0.4]]
    assert abs(model.user_vector(0)[0] - (0.5 + 0.4 / math.sqrt(3))) < 1e-12
    assert abs(model.predict(0, 2) - (3.7 + 0.4 / math.sqrt(3))) < 1e-12
    assert abs(model.predict(3, 0) - (1.5 + 0.4 / math.sqrt(3))) < 1e-12
    model.implicit[3] = [0, 1, 2, 3]  # user 4 also viewed item 1, with no rating
    assert abs(model.predict(3, 0) - 1.9) < 1e-12


def test_training_lowers_objective_and_beats_the_mean():
    full = recs.planted(20, 15, 2, 6, noise=0.1)
    train, hidden = recs.split(full, 0.3, 6)
    lb, lf = 0.005, 0.015
    start = spp.init(20, 15, 2, train, 2)
    model = spp.fit(train, 20, 15, 2, lb=lb, lf=lf, gamma=0.02, epochs=150, seed=2, decay=1.0)
    assert spp.objective(model, train, lb, lf) < 0.2 * spp.objective(start, train, lb, lf)
    mu = recs.global_mean(train)
    assert recs.rmse(model.predict, hidden) < recs.rmse(lambda u, i: mu, hidden)
