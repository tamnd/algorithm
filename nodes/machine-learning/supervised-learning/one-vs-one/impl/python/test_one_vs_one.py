# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-vs-one/. The authors are listed in prov/W9KQF9.jsonl.

import random
from itertools import combinations

from one_vs_one import (least_squares_learner, predict, predict_confidence_tiebreak, predict_ddag,
                        train, votes)


def test_pairs_and_training_subsets() -> None:
    seen = []

    def spy(X, t):
        seen.append((len(X), sum(1 for v in t if v == 1)))
        return lambda x: 0.0

    y = [0, 0, 1, 1, 1, 2, 2, 2, 2, 3]
    models = train([[0.0]] * len(y), y, 4, spy)
    assert sorted(models) == list(combinations(range(4), 2))
    assert len(models) == 4 * 3 // 2
    assert seen == [(5, 2), (6, 2), (3, 2), (7, 3), (4, 3), (5, 4)]


def test_votes_sum_to_number_of_pairs() -> None:
    rng = random.Random(3)
    for k in range(2, 7):
        models = {p: (lambda s: (lambda x: s))(rng.uniform(-1, 1)) for p in combinations(range(k), 2)}
        assert sum(votes(models, k, [0.0])) == k * (k - 1) // 2


def test_cycle_tie_rules() -> None:
    # 0 beats 1, 1 beats 2, 2 beats 0: one vote each
    models = {(0, 1): lambda x: 0.2, (1, 2): lambda x: 0.9, (0, 2): lambda x: -0.5}
    assert votes(models, 3, [0.0]) == [1, 1, 1]
    assert predict(models, 3, [0.0]) == 0
    # confidences: class 0: 0.2 - 0.5 = -0.3; class 1: -0.2 + 0.9 = 0.7; class 2: -0.9 + 0.5 = -0.4
    assert predict_confidence_tiebreak(models, 3, [0.0]) == 1
    # DDAG tests 0 against 2 first (2 wins), then 1 against 2 (1 wins)
    assert predict_ddag(models, 3, [0.0]) == 1


def test_middle_class_with_linear_pairs() -> None:
    X = [[(i + 0.5) / 10] for i in range(30)]
    y = [int(x[0]) for x in X]
    models = train(X, y, 3, least_squares_learner())
    assert all(predict(models, 3, x) == t for x, t in zip(X, y))
    assert all(predict_ddag(models, 3, x) == t for x, t in zip(X, y))


def test_ddag_agrees_with_votes_without_cycles() -> None:
    rng = random.Random(5)
    for _ in range(300):
        k = rng.randint(2, 6)
        rank = list(range(k))
        rng.shuffle(rank)  # a total order: class rank[0] beats all, and so on
        pos = {c: r for r, c in enumerate(rank)}
        models = {(i, j): (lambda s: (lambda x: s))(1.0 if pos[i] < pos[j] else -1.0)
                  for i, j in combinations(range(k), 2)}
        assert predict(models, k, [0.0]) == rank[0] == predict_ddag(models, k, [0.0])


def test_accuracy_on_blobs() -> None:
    rng = random.Random(1)

    def blobs(per):
        X, y = [], []
        for j in range(4):
            for _ in range(per):
                X.append([rng.gauss(6.0 * j, 1.0), rng.gauss(6.0 * (j % 2), 1.0)])
                y.append(j)
        return X, y

    X, y = blobs(40)
    models = train(X, y, 4, least_squares_learner())
    Xt, yt = blobs(40)
    assert sum(predict(models, 4, x) == t for x, t in zip(Xt, yt)) / len(yt) > 0.95
