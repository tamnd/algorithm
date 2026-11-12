# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stacking/. The authors are listed in prov/2W5J8D.jsonl.

import math
import random

from stacking import fit_mean, fit_one_nn, in_sample, k_folds, make_ridge, nnls, out_of_fold, sse, stack

LEARNERS = [fit_one_nn, make_ridge(1.0), fit_mean]


def noisy(rng: random.Random, n: int):
    xs = [rng.uniform(0, 3) for _ in range(n)]
    return xs, [math.sin(2 * x) + 0.5 * x + rng.gauss(0, 0.4) for x in xs]


def test_folds_partition_the_data() -> None:
    rng = random.Random(1)
    for n, k in ((10, 3), (17, 5), (5, 5), (40, 10)):
        folds = k_folds(n, k, rng)
        assert sorted(i for f in folds for i in f) == list(range(n))
        assert max(map(len, folds)) - min(map(len, folds)) <= 1


def test_out_of_fold_predictions_never_see_their_example() -> None:
    def fit_memory(xs, ys):
        table = dict(zip(xs, ys))
        return lambda x: table.get(x, -1.0)

    rng = random.Random(2)
    xs = [float(i) for i in range(12)]
    ys = [float(rng.randrange(10)) for _ in xs]
    z = out_of_fold(xs, ys, [fit_memory], k_folds(12, 4, rng))
    assert all(row[0] == -1.0 for row in z)
    assert all(row[0] == y for row, y in zip(in_sample(xs, ys, [fit_memory]), ys))


def test_nnls_satisfies_the_kkt_conditions() -> None:
    rng = random.Random(3)
    for _ in range(40):
        n, cols = rng.randrange(4, 12), rng.randrange(1, 5)
        z = [[rng.gauss(0, 1) for _ in range(cols)] for _ in range(n)]
        y = [rng.gauss(0, 1) for _ in range(n)]
        w = nnls(z, y)
        assert min(w) >= 0.0
        r = [sum(a * b for a, b in zip(w, row)) - yy for row, yy in zip(z, y)]
        grad = [2 * sum(row[c] * rr for row, rr in zip(z, r)) for c in range(cols)]
        for c in range(cols):
            if w[c] > 1e-9:
                assert abs(grad[c]) < 1e-7
            else:
                assert grad[c] > -1e-7
        # No random non-negative point is better.
        best = sse(z, y, w)
        for _ in range(50):
            v = [max(0.0, wc + rng.gauss(0, 0.3)) for wc in w]
            assert sse(z, y, v) >= best - 1e-9


def test_in_sample_level_one_fit_is_too_optimistic() -> None:
    rng = random.Random(4)
    xs, ys = noisy(rng, 40)
    # Leaky: 1-NN predicts each training target exactly, so NNLS puts all the weight on it,
    # and the apparent error of the stacked fit is zero.
    z_in = in_sample(xs, ys, LEARNERS)
    w_in = nnls(z_in, ys)
    assert abs(w_in[0] - 1.0) < 1e-9 and abs(w_in[1]) < 1e-9 and abs(w_in[2]) < 1e-9
    assert sse(z_in, ys, w_in) < 1e-18
    # The out-of-fold predictions show the real error of the same combination.
    z_oof = out_of_fold(xs, ys, LEARNERS, k_folds(40, 5, rng))
    assert sse(z_oof, ys, w_in) > 0.1 * len(ys) * 0.4 ** 2
    # And on fresh data the leaky combination is far from its apparent error of 0.
    tx, ty = noisy(rng, 200)
    f = fit_one_nn(xs, ys)
    assert sum((f(x) - y) ** 2 for x, y in zip(tx, ty)) / len(tx) > 0.1


def test_stacked_predictor_is_the_weighted_sum_of_refitted_learners() -> None:
    rng = random.Random(5)
    xs, ys = noisy(rng, 30)
    w, g = stack(xs, ys, LEARNERS, 5, random.Random(6))
    assert min(w) >= 0.0
    fs = [fit(xs, ys) for fit in LEARNERS]
    for x in (0.1, 1.3, 2.9):
        assert abs(g(x) - sum(wl * f(x) for wl, f in zip(w, fs))) < 1e-12
    # Same folds give the same OOF matrix, so the same weights.
    z = out_of_fold(xs, ys, LEARNERS, k_folds(30, 5, random.Random(6)))
    assert nnls(z, ys) == w
