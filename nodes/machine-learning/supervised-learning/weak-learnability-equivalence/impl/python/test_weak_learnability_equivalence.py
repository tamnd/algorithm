# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-learnability-equivalence/. The authors are listed in prov/XAZCTX.jsonl.

import math
import random

from weak_learnability_equivalence import adaboost, best_stump, circle_data, predict, stump_predict

XS, YS = circle_data(200, random.Random(1))


def test_bounds_hold_at_every_round() -> None:
    vote, log = adaboost(XS, YS, 300)
    assert len(log) == 300
    for r in log:
        assert 0 < r["eps"] <= 0.5
        assert abs(r["z"] - r["z_direct"]) < 1e-12
        assert abs(r["mass_on_wrong"] - 0.5) < 1e-9  # h_t is useless for the next distribution
        assert r["train_error"] <= r["prod_z"] + 1e-12
        assert r["prod_z"] <= r["exp_bound"] + 1e-12


def test_product_of_normalizers_is_the_exponential_loss() -> None:
    vote, log = adaboost(XS, YS, 60)
    loss = sum(math.exp(-y * sum(a * stump_predict(h, x) for a, h in vote)) for x, y in zip(XS, YS)) / len(XS)
    assert abs(loss - log[-1]["prod_z"]) < 1e-9
    err = sum(predict(vote, x) != y for x, y in zip(XS, YS)) / len(XS)
    assert err == log[-1]["train_error"]


def test_best_stump_matches_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(30):
        xs, ys = circle_data(rng.randint(2, 25), rng)
        w = [rng.random() for _ in xs]
        _, e = best_stump(xs, ys, w)
        best = math.inf
        for f in range(2):
            for thr in [-math.inf] + [x[f] for x in xs]:
                for sgn in (1, -1):
                    best = min(best, sum(wi for x, y, wi in zip(xs, ys, w) if stump_predict((f, thr, sgn), x) != y))
        assert abs(e - best / sum(w)) < 1e-12


def test_zero_training_error_once_the_bound_drops_below_one_over_m() -> None:
    xs, ys = circle_data(30, random.Random(4))
    vote, log = adaboost(xs, ys, 2000)
    hit = [r for r in log if r["exp_bound"] < 1 / len(xs)]
    assert hit
    for r in hit:
        assert r["train_error"] == 0.0
