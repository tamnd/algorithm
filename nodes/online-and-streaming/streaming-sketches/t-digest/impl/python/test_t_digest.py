# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-digest/. The authors are listed in prov/ND6BPW.jsonl.

import bisect
import math
import random

import pytest

from t_digest import TDigest, lopsided_attack, max_rank_error

STREAM = [12, 3, 17, 8, 1, 15, 6, 10, 4, 14, 9, 2, 19, 7, 11, 5, 18, 13, 16, 20]


def build(values, delta, scale, buffer_size):
    t = TDigest(delta, scale, buffer_size)
    for x in values:
        t.insert(x)
    return t


def test_worked_example() -> None:
    t = build([float(x) for x in STREAM], 10, "k1", 100)
    t.compress()
    assert t.means == [1.0, 3.5, 8.5, 14.0, 18.0, 20.0]
    assert t.weights == [1, 4, 6, 5, 3, 1]
    assert all(k <= 1 for k in t.k_sizes())
    assert t.rank(10.0) == 9.5
    assert t.query(0.5) == 10.5
    u = build([float(x) for x in STREAM], 10, "k0", 100)
    u.compress()
    assert u.means == [2.5, 6.5, 10.0, 13.5, 17.5, 20.0]
    assert u.weights == [4, 4, 3, 4, 4, 1]


def test_edges() -> None:
    t = TDigest(10)
    with pytest.raises(ValueError):
        t.query(0.5)
    assert t.rank(3.0) == 0
    t.insert(7.0)
    assert t.query(0.5) == 7.0 and t.rank(6.0) == 0 and t.rank(7.0) == 1
    for _ in range(50):
        t.insert(7.0)
    t.check_invariant()
    assert t.query(0.3) == 7.0


def test_size_bound_and_weights_on_random_streams() -> None:
    rng = random.Random(2019)
    for _ in range(500):
        delta = rng.choice([5, 10, 20, 50])
        scale = rng.choice(["k0", "k1"])
        t = TDigest(delta, scale, buffer_size=rng.randint(1, 60))
        n = rng.randint(1, 600)
        kind = rng.randrange(3)
        values = [rng.random() for _ in range(n)]
        if kind == 1:
            values.sort()
        elif kind == 2:
            values = [rng.expovariate(1.0) ** 3 for _ in range(n)]
        for x in values:
            t.insert(x)
        t.check_invariant()  # at most ceil(delta) centroids, weights add up to n
        for k, w in zip(t.k_sizes(), t.weights):
            assert w == 1 or k <= 1 + 1e-9


def test_merge_keeps_weight_and_size() -> None:
    rng = random.Random(4)
    for _ in range(100):
        delta = rng.choice([10, 30])
        a = build([rng.gauss(0, 1) for _ in range(rng.randint(1, 300))], delta, "k1", 40)
        b = build([rng.gauss(2, 1) for _ in range(rng.randint(1, 300))], delta, "k1", 40)
        na, nb = a.n, b.n
        a.merge(b)
        a.check_invariant()
        assert a.n == na + nb


def test_accuracy_on_iid_data_is_good_in_practice() -> None:
    # An empirical check only: the t-digest has no worst-case guarantee.
    rng = random.Random(7)
    n, delta = 20000, 100
    values = [rng.random() for _ in range(n)]
    t = build(values, delta, "k1", 500)
    data = sorted(values)
    for phi in (0.001, 0.01, 0.1, 0.5, 0.9, 0.99, 0.999):
        x = data[math.ceil(phi * n) - 1]
        assert abs(t.rank(x) - bisect.bisect_right(data, x)) <= 0.01 * n


def test_adversarial_stream_breaks_the_accuracy() -> None:
    t, stream = lopsided_attack(20, 30)
    t.check_invariant()
    assert len(t.means) <= 20
    # More than 80 percent of the stream is misranked at some point.
    assert max_rank_error(t, stream) >= 0.8
