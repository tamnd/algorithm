# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bagging/. The authors are listed in prov/251C6Y.jsonl.

import itertools
import math
import random
from fractions import Fraction

from bagging import bag, bootstrap_sample, expected_distinct_fraction, fit_one_nn, fit_stump, oob_error, oob_predict, predict


def test_distinct_fraction_by_enumeration() -> None:
    for n in range(1, 7):
        total = sum(len(set(s)) for s in itertools.product(range(n), repeat=n))
        assert Fraction(total, n ** n * n) == expected_distinct_fraction(n)


def test_distinct_fraction_tends_to_one_minus_one_over_e() -> None:
    limit = 1 - math.exp(-1)
    prev = 1.0
    for n in (1, 2, 3, 5, 10, 100, 1000, 10000):
        f = float(expected_distinct_fraction(n)) if n <= 1000 else 1 - (1 - 1 / n) ** n
        assert f >= limit  # (1 - 1/n)^n <= 1/e
        assert f - limit <= 1 / (math.e * n) + 1e-15  # (1 - 1/n)^n >= (1 - 1/n) / e
        assert f <= prev + 1e-15  # decreasing in n
        prev = f
    rng = random.Random(1)
    n, trials = 500, 400
    mean = sum(len(set(bootstrap_sample(n, rng))) for _ in range(trials)) / (n * trials)
    assert abs(mean - float(expected_distinct_fraction(n))) < 0.005


def test_oob_uses_only_models_that_did_not_see_the_example() -> None:
    # A learner that answers exactly on its own training inputs and 0 elsewhere: any leak shows up.
    def fit_memory(xs, ys):
        table = dict(zip(xs, ys))
        return lambda x: table.get(x, 0.0)

    rng = random.Random(2)
    xs = list(range(20))
    ys = [float(rng.randrange(1, 10)) for _ in xs]
    models = bag(xs, ys, fit_memory, 30, rng)
    for i in xs:
        p = oob_predict(models, xs, i, "regression")
        if any(i not in in_bag for _, in_bag in models):
            assert p == 0.0
        else:
            assert p is None
        for f, in_bag in models:
            if i in in_bag:
                assert f(xs[i]) == ys[i]
    assert oob_error(models, xs, ys, "regression") > 0.0


def test_oob_matches_a_direct_recomputation() -> None:
    rng = random.Random(3)
    xs = [rng.random() for _ in range(25)]
    ys = [int(x > 0.5) if rng.random() > 0.2 else int(x <= 0.5) for x in xs]
    models = bag(xs, ys, fit_one_nn, 15, rng)
    for i in range(25):
        votes = [f(xs[i]) for f, in_bag in models if i not in in_bag]
        p = oob_predict(models, xs, i, "classification")
        if votes:
            assert votes.count(p) == max(votes.count(v) for v in set(votes))
            assert p == min(v for v in set(votes) if votes.count(v) == votes.count(p))


def test_average_beats_the_mean_member_by_its_spread() -> None:
    # For squared loss, (y - mean f_b)^2 = mean (y - f_b)^2 - var_b f_b(x): Jensen's inequality with its gap.
    rng = random.Random(4)
    xs = [rng.uniform(0, 1) for _ in range(30)]
    ys = [math.sin(6 * x) + rng.gauss(0, 0.3) for x in xs]
    models = bag(xs, ys, fit_stump, 25, rng)
    for x in (0.1, 0.35, 0.6, 0.9):
        for y in (-1.0, 0.0, 0.7):
            preds = [f(x) for f, _ in models]
            mean = sum(preds) / len(preds)
            spread = sum((p - mean) ** 2 for p in preds) / len(preds)
            avg_member = sum((y - p) ** 2 for p in preds) / len(preds)
            assert abs(predict(models, x, "regression") - mean) < 1e-12
            assert abs((y - mean) ** 2 - (avg_member - spread)) < 1e-9
