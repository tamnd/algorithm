# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-vs-rest/. The authors are listed in prov/56YRRQ.jsonl.

import random

from one_vs_rest import least_squares_learner, predict, predict_hard_votes, train


def blobs(rng: random.Random, k: int, per: int) -> tuple[list[list[float]], list[int]]:
    X, y = [], []
    for j in range(k):
        cx, cy = 6.0 * j, 6.0 * (j % 2)
        for _ in range(per):
            X.append([rng.gauss(cx, 1.0), rng.gauss(cy, 1.0)])
            y.append(j)
    return X, y


def test_trains_k_classifiers_on_all_examples() -> None:
    seen = []

    def spy(X, t):
        seen.append((len(X), sum(1 for v in t if v == 1)))
        return lambda x: 0.0

    train([[0.0]] * 10, [0, 0, 1, 1, 1, 2, 2, 2, 2, 2], 3, spy)
    assert seen == [(10, 2), (10, 3), (10, 5)]  # all n examples each time; few positives


def test_accuracy_on_separated_blobs() -> None:
    rng = random.Random(1)
    X, y = blobs(rng, 4, 40)
    f = train(X, y, 4, least_squares_learner())
    Xt, yt = blobs(rng, 4, 40)
    acc = sum(predict(f, x) == t for x, t in zip(Xt, yt)) / len(yt)
    assert acc > 0.95


def test_tie_goes_to_smallest_index() -> None:
    f = [lambda x: 0.5, lambda x: 0.7, lambda x: 0.7]
    assert predict(f, [0.0]) == 1


def test_masking_of_the_middle_class() -> None:
    X = [[(i + 0.5) / 10] for i in range(30)]
    y = [int(x[0]) for x in X]  # class 0 on [0,1), 1 on [1,2), 2 on [2,3)
    f = train(X, y, 3, least_squares_learner())
    pred = [predict(f, x) for x in X]
    assert 1 not in pred  # the middle class is never predicted
    assert sum(p == t for p, t in zip(pred, y)) == 20
    # with the feature x^2 added, the middle class is found; two boundary points are wrong
    X2 = [[x[0], x[0] ** 2] for x in X]
    f2 = train(X2, y, 3, least_squares_learner())
    pred2 = [predict(f2, x) for x in X2]
    assert all(p == 1 for p, t in zip(pred2, y) if t == 1)
    assert sum(p == t for p, t in zip(pred2, y)) == 28


def test_hard_votes_can_be_empty_or_ambiguous() -> None:
    X = [[(i + 0.5) / 10] for i in range(30)]
    y = [int(x[0]) for x in X]
    f = train(X, y, 3, least_squares_learner())
    sizes = {len(predict_hard_votes(f, x)) for x in X}
    assert 0 in sizes
