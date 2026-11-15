# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/user-based-collaborative-filtering/. The authors are listed in prov/SEEFZS.jsonl.

import math

import recs
from user_based_collaborative_filtering import UserBasedCF, pearson

TOL = 1e-9


def dense(train, m, n):
    return [[train.get((u, i)) for i in range(n)] for u in range(m)]


def brute(rows, u, i, k=None):
    """The prediction formula written out on a dense matrix with None gaps."""
    n = len(rows[0])

    def mean(a):
        vals = [x for x in rows[a] if x is not None]
        return sum(vals) / len(vals)

    def w(a, b):
        ma, mb = mean(a), mean(b)
        co = [t for t in range(n) if rows[a][t] is not None and rows[b][t] is not None]
        x = [rows[a][t] - ma for t in co]
        y = [rows[b][t] - mb for t in co]
        # The same float expression as the module, so that exact ties
        # (frequent with integer ratings) stay ties in the top-k choice.
        sx = sum(t * t for t in x)
        sy = sum(t * t for t in y)
        if sx == 0 or sy == 0:
            return 0.0
        return sum(a1 * b1 for a1, b1 in zip(x, y)) / math.sqrt(sx * sy)

    nb = [(w(u, v), v) for v in range(len(rows)) if v != u and rows[v][i] is not None]
    if k is not None:
        nb = sorted(nb, key=lambda t: (-t[0], t[1]))[:k]
    den = sum(abs(t[0]) for t in nb)
    if den == 0:
        return mean(u)
    return mean(u) + sum(t[0] * (rows[t[1]][i] - mean(t[1])) for t in nb) / den


def test_toy_weight_and_prediction():
    train = recs.toy()
    model = UserBasedCF(train)
    # u1 and u2 share items 1, 2 and 4; centered vectors (5/3, 2/3, -7/3), (1/4, 5/4, -7/4).
    exact = (16 / 3) / math.sqrt((26 / 3) * (75 / 16))
    assert abs(model.weight(0, 1) - exact) < 1e-12
    rows = dense(train, 4, 4)
    for u, i in [(0, 2), (3, 0)]:
        assert abs(model.predict(u, i) - brute(rows, u, i)) < TOL
    assert abs(model.predict(0, 2) - 3.933603130898395) < TOL


def test_matches_brute_force_on_planted_matrices():
    for seed in range(5):
        full = recs.planted(9, 7, 2, seed, rounded=True)
        train, hidden = recs.split(full, 0.3, seed)
        rows = dense(train, 9, 7)
        for k in (None, 1, 3):
            model = UserBasedCF(train, k=k)
            for u, i in hidden:
                assert abs(model.predict(u, i) - brute(rows, u, i, k)) < TOL


def test_weight_symmetric_and_in_range():
    full = recs.planted(8, 6, 2, 11, noise=0.3)
    train, _ = recs.split(full, 0.4, 11)
    model = UserBasedCF(train)
    for u in range(8):
        for v in range(8):
            w = model.weight(u, v)
            assert abs(w - model.weight(v, u)) < 1e-15
            assert -1 - TOL <= w <= 1 + TOL


def test_shift_of_one_user():
    full = recs.planted(7, 6, 2, 5, noise=0.2)
    train, hidden = recs.split(full, 0.3, 5)
    shifted = {k: (v + 0.7 if k[0] == 2 else v) for k, v in train.items()}
    a, b = UserBasedCF(train), UserBasedCF(shifted)
    for u in range(7):
        for v in range(7):
            assert abs(a.weight(u, v) - b.weight(u, v)) < TOL
    for u, i in hidden:
        extra = 0.7 if u == 2 else 0.0
        assert abs(a.predict(u, i) + extra - b.predict(u, i)) < TOL


def test_no_overlap_gives_user_mean():
    train = {(0, 0): 4.0, (0, 1): 2.0, (1, 2): 5.0, (1, 3): 1.0}
    assert pearson({0: 4.0, 1: 2.0}, {2: 5.0, 3: 1.0}, 3.0, 3.0) == 0.0
    model = UserBasedCF(train)
    assert model.predict(0, 2) == 3.0
    assert model.predict(9, 0) == 3.0
