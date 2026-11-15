# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matrix-factorization-recommendation/. The authors are listed in prov/99YS69.jsonl.

import random

import recs
import matrix_factorization_recommendation as mf

H = 1e-6  # step of the central differences
TOL = 1e-6  # allowed gap, relative to max(1, |gradient entry|)


def random_model(m, n, r, train, seed, biased=True):
    rng = random.Random(seed)
    model = mf.init(m, n, r, train, seed, scale=0.5, biased=biased)
    if biased:
        model.bu = [rng.uniform(-0.5, 0.5) for _ in range(m)]
        model.bi = [rng.uniform(-0.5, 0.5) for _ in range(n)]
    return model


def params(model):
    """(list, index) handles for each parameter of the model."""
    out = []
    if model.biased:
        out += [(model.bu, u) for u in range(model.m)]
        out += [(model.bi, i) for i in range(model.n)]
    out += [(row, f) for row in model.p for f in range(model.r)]
    out += [(row, f) for row in model.q for f in range(model.r)]
    return out


def flat_gradient(model, train, lam):
    gbu, gbi, gp, gq = mf.gradient(model, train, lam)
    out = []
    if model.biased:
        out += gbu + gbi
    for row in gp + gq:
        out += row
    return out


def test_gradient_matches_central_differences():
    for biased in (True, False):
        full = recs.planted(5, 4, 2, 3, noise=0.2)
        train, _ = recs.split(full, 0.3, 3)
        model = random_model(5, 4, 2, train, 8, biased)
        lam = 0.3
        g = flat_gradient(model, train, lam)
        for (vec, k), gk in zip(params(model), g):
            old = vec[k]
            vec[k] = old + H
            up = mf.objective(model, train, lam)
            vec[k] = old - H
            down = mf.objective(model, train, lam)
            vec[k] = old
            num = (up - down) / (2 * H)
            assert abs(num - gk) <= TOL * max(1.0, abs(gk))


def test_sgd_step_is_half_gradient_step_on_one_rating():
    full = recs.planted(4, 4, 3, 5)
    train, _ = recs.split(full, 0.25, 5)
    lam, gamma = 0.1, 0.05
    for (u, i), v in sorted(train.items()):
        model = random_model(4, 4, 3, train, u * 4 + i)
        g = flat_gradient(model, {(u, i): v}, lam)
        before = [vec[k] for vec, k in params(model)]
        mf.sgd_step(model, u, i, v, lam, gamma)
        after = [vec[k] for vec, k in params(model)]
        for b, a, gk in zip(before, after, g):
            assert abs(a - (b - gamma / 2 * gk)) < 1e-12


def test_hand_example():
    # One factor, no bias: p = 1, q = 2, r = 5, gamma = lam = 0.1.
    model = mf.Model(1, 1, 1, biased=False)
    model.p, model.q = [[1.0]], [[2.0]]
    mf.sgd_step(model, 0, 0, 5.0, 0.1, 0.1)
    assert abs(model.p[0][0] - 1.59) < 1e-12
    assert abs(model.q[0][0] - 2.28) < 1e-12


def test_toy_step_of_the_page():
    # Biased, one factor, mu = 41/14, zero biases, p_u1 = q_i1 = 0.5,
    # the rating r(u1, i1) = 5, gamma = lam = 0.1.
    train = recs.toy()
    model = mf.Model(4, 4, 1, mu=recs.global_mean(train))
    model.p[0], model.q[0] = [0.5], [0.5]
    lam = gamma = 0.1
    before = mf.objective(model, {(0, 0): 5.0}, lam)
    mf.sgd_step(model, 0, 0, 5.0, lam, gamma)
    after = mf.objective(model, {(0, 0): 5.0}, lam)
    e = 5.0 - (41 / 14 + 0.25)
    assert abs(model.bu[0] - 0.1 * e) < 1e-12 and abs(model.bi[0] - 0.1 * e) < 1e-12
    assert abs(model.p[0][0] - (0.5 + 0.1 * (0.5 * e - 0.05))) < 1e-12
    assert abs(model.predict(0, 0) - 3.6363369) < 1e-6
    assert abs(before - 3.3676020) < 1e-6 and abs(after - 1.9349083) < 1e-6


def test_zero_factors_stay_zero():
    # p = q = 0 is a stationary point in the factors: SGD never leaves it.
    train = recs.toy()
    model = mf.Model(4, 4, 2, mu=recs.global_mean(train))
    mf.sgd_epoch(model, train, 0.05, 0.05, sorted(train))
    assert all(a == 0.0 for row in model.p + model.q for a in row)
    assert any(b != 0.0 for b in model.bu)


def test_training_lowers_objective_and_beats_the_mean():
    full = recs.planted(20, 15, 2, 1, noise=0.1)
    train, hidden = recs.split(full, 0.3, 1)
    lam, gamma = 0.02, 0.02
    start = mf.init(20, 15, 2, train, 4)
    model = mf.fit(train, 20, 15, 2, lam=lam, gamma=gamma, epochs=200, seed=4)
    assert mf.objective(model, train, lam) < 0.2 * mf.objective(start, train, lam)
    mu = recs.global_mean(train)
    assert recs.rmse(model.predict, hidden) < recs.rmse(lambda u, i: mu, hidden)


def test_unbiased_model_keeps_zero_biases():
    train, _ = recs.split(recs.planted(6, 5, 2, 2), 0.2, 2)
    model = mf.fit(train, 6, 5, 2, epochs=5, biased=False)
    assert model.mu == 0.0 and set(model.bu) == {0.0} and set(model.bi) == {0.0}
