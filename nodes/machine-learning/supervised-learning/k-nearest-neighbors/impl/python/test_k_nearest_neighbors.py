# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-nearest-neighbors/. The authors are listed in prov/4WACV7.jsonl.

import math
import random

import pytest

from k_nearest_neighbors import euclidean, k_nearest, knn_classify, knn_regress, leave_one_out_error

X = [(1, 1), (2, 1), (1, 3), (4, 2), (5, 4), (3, 4), (2, 4)]
Y = ["A", "A", "A", "B", "B", "B", "A"]
T = [2, 3, 4, 6, 9, 7, 6]
Q = (3, 2)


def test_worked_example() -> None:
    assert [i for _, i in k_nearest(X, Q, 5)] == [3, 1, 5, 0, 2]
    assert [knn_classify(X, Y, Q, k) for k in range(1, 8)] == ["B", "B", "B", "B", "A", "A", "A"]
    assert knn_classify(X, Y, Q, 4, weighted=True) == "B"
    assert knn_classify(X, Y, Q, 5, weighted=True) == "A"
    assert knn_regress(X, T, Q, 3) == pytest.approx(16 / 3)
    want = (6 / 1 + 3 / math.sqrt(2) + 7 / 2) / (1 + 1 / math.sqrt(2) + 1 / 2)
    assert knn_regress(X, T, Q, 3, weighted=True) == pytest.approx(want)


def test_vote_tie_goes_to_nearest_class() -> None:
    # k = 4 gives two votes for each class; the nearest neighbor (index 3) is B.
    assert knn_classify(X, Y, Q, 4) == "B"
    assert knn_classify([(0,), (1,), (-2,), (3,)], [1, 2, 1, 2], (0.4,), 4) == 1


def test_selection_against_full_sort() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n, d = rng.randrange(1, 30), rng.randrange(1, 4)
        xs = [tuple(rng.randrange(-3, 4) for _ in range(d)) for _ in range(n)]
        q = tuple(rng.randrange(-3, 4) for _ in range(d))
        k = rng.randrange(1, n + 3)
        want = sorted((euclidean(x, q), i) for i, x in enumerate(xs))[:k]
        assert k_nearest(xs, q, k) == want


def test_vote_against_counting() -> None:
    rng = random.Random(6)
    for _ in range(300):
        n = rng.randrange(1, 25)
        xs = [(rng.random(), rng.random()) for _ in range(n)]
        ys = [rng.randrange(3) for _ in range(n)]
        q = (rng.random(), rng.random())
        k = rng.randrange(1, n + 1)
        order = sorted(range(n), key=lambda i: (euclidean(xs[i], q), i))[:k]
        counts = {c: sum(ys[i] == c for i in order) for c in set(ys[i] for i in order)}
        top = max(counts.values())
        want = next(ys[i] for i in order if counts[ys[i]] == top)
        assert knn_classify(xs, ys, q, k) == want


def test_one_nn_memorizes_distinct_points() -> None:
    rng = random.Random(7)
    xs = [(rng.random(), rng.random(), rng.random()) for _ in range(50)]
    ys = [rng.randrange(2) for _ in range(50)]
    assert all(knn_classify(xs, ys, x, 1) == y for x, y in zip(xs, ys))


def test_regression_k_equals_n_is_the_mean() -> None:
    rng = random.Random(8)
    xs = [(rng.random(),) for _ in range(20)]
    ts = [rng.uniform(-5, 5) for _ in range(20)]
    assert knn_regress(xs, ts, (0.3,), 20) == pytest.approx(sum(ts) / 20)


def test_weighted_exact_match_takes_all_weight() -> None:
    assert knn_classify([(0,), (1,), (1.1,)], ["a", "b", "b"], (0,), 3, weighted=True) == "a"
    assert knn_regress([(0,), (1,)], [5.0, 9.0], (0,), 2, weighted=True) == 5.0


def test_leave_one_out_on_separated_clusters() -> None:
    rng = random.Random(9)
    xs = [(rng.gauss(0, 0.3), rng.gauss(0, 0.3)) for _ in range(20)]
    xs += [(rng.gauss(5, 0.3), rng.gauss(5, 0.3)) for _ in range(20)]
    ys = [0] * 20 + [1] * 20
    assert leave_one_out_error(xs, ys, 3) == 0.0


def test_bad_k() -> None:
    with pytest.raises(ValueError):
        k_nearest(X, Q, 0)
