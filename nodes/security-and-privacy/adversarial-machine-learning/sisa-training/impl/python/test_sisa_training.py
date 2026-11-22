# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sisa-training/. The authors are listed in prov/P6S600.jsonl.

"""Tests of SISA on seeded synthetic data: deletion gives bit for bit the model of retraining from scratch."""

import copy
import random
from fractions import Fraction

import mlkit as m
from sisa_training import assign, gd_steps, predict, sisa_delete, sisa_train


def retrain_from_scratch(records, where, shards, slices, steps, lr, l2):
    """An independent trainer: for each shard, from zero, gradient steps on slices 0..r for r = 0, 1, ..."""
    d = len(next(iter(records.values()))[0])
    rows = []
    for k in range(shards):
        w, b = [0.0] * d, 0.0
        row = [([0.0] * d, 0.0)]
        for r in range(slices):
            data = [records[i] for t in range(r + 1) for i in sorted(i for i in records if where[i] == (k, t))]
            n = len(data)
            for _ in range(steps if n else 0):
                gw, gb = [0.0] * d, 0.0
                for x, y in data:
                    g = m.sigmoid(m.dot(w, x) + b) - y
                    for j in range(d):
                        gw[j] += g * x[j]
                    gb += g
                w = [w[j] - lr * (gw[j] / n + l2 * w[j]) for j in range(d)]
                b -= lr * gb / n
            row.append((list(w), b))
        rows.append(row)
    return rows


def random_records(rng: random.Random, n: int, d: int) -> dict[int, tuple[list[float], int]]:
    data = m.make_blobs(rng, n, d, [[-1.0] * d, [1.0] * d], 1.0)
    ids = rng.sample(range(100), n)
    return dict(zip(ids, data))


def test_partition_is_disjoint_and_balanced() -> None:
    rng = random.Random(4101)
    for _ in range(200):
        n, s, r = rng.randint(1, 40), rng.randint(1, 4), rng.randint(1, 4)
        ids = rng.sample(range(1000), n)
        where = assign(ids, s, r, rng.randrange(10**6))
        assert sorted(where) == sorted(ids)
        sizes = [sum(1 for i in ids if where[i][0] == k) for k in range(s)]
        assert max(sizes) - min(sizes) <= 1
        for k in range(s):
            sl = [sum(1 for i in ids if where[i] == (k, t)) for t in range(r)]
            assert sum(sl) == sizes[k] and all(0 <= t < r for _, t in (where[i] for i in ids))
            if sizes[k] >= r:
                assert max(sl) - min(sl) <= 1


def test_one_shard_and_one_slice_is_plain_training() -> None:
    rng = random.Random(4102)
    recs = random_records(rng, 20, 3)
    where = {i: (0, 0) for i in recs}
    model = sisa_train(recs, where, 1, 1, 30, 0.5, 0.01)
    data = [recs[i] for i in sorted(recs)]
    w, b = m.train_logistic(data, 30, 0.5, 0.01)
    assert model.ckpt[0][1] == (w, b)


def test_deletion_equals_retraining_from_scratch() -> None:
    """The theorem of the page, bit for bit, on 500 random instances and sequences of deletions."""
    rng = random.Random(4103)
    for _ in range(500):
        n, d = rng.randint(4, 10), rng.randint(1, 3)
        shards, slices, steps = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 2)
        lr, l2 = rng.choice([0.1, 0.5, 1.0]), rng.choice([0.0, 0.01])
        recs = random_records(rng, n, d)
        where = assign(list(recs), shards, slices, rng.randrange(10**6))
        model = sisa_train(recs, where, shards, slices, steps, lr, l2)
        assert model.ckpt == retrain_from_scratch(recs, where, shards, slices, steps, lr, l2)
        left = dict(recs)
        for victim in rng.sample(sorted(recs), rng.randint(1, min(3, n - 1))):
            k, r = where[victim]
            before = copy.deepcopy(model.ckpt)
            sisa_delete(model, victim)
            del left[victim]
            assert model.ckpt == retrain_from_scratch(left, where, shards, slices, steps, lr, l2)
            # the other shards and the checkpoints up to slice r are untouched
            for kk in range(shards):
                if kk != k:
                    assert model.ckpt[kk] == before[kk]
            assert model.ckpt[k][: r + 1] == before[k][: r + 1]


def test_average_cost_of_a_deletion() -> None:
    """With S shards of R slices of m records each, the mean cost is E (R + 1) (m (2R + 1) - 3) / 6."""
    rng = random.Random(4104)
    for shards, slices, size, steps in [(1, 1, 3, 2), (2, 3, 2, 1), (3, 2, 4, 2), (2, 4, 3, 1)]:
        n = shards * slices * size
        recs = random_records(rng, n, 2)
        where = assign(list(recs), shards, slices, 7)
        model = sisa_train(recs, where, shards, slices, steps, 0.5, 0.0)
        assert model.cost == shards * steps * size * slices * (slices + 1) // 2
        total = 0
        for victim in recs:
            fresh = sisa_train(recs, where, shards, slices, steps, 0.5, 0.0)
            total += sisa_delete(fresh, victim)
        mean = Fraction(total, n)
        assert mean == Fraction(steps * (slices + 1) * (size * (2 * slices + 1) - 3), 6)


def test_vote_and_accuracy_on_blobs() -> None:
    rng = random.Random(4105)
    recs = random_records(rng, 60, 2)
    test = m.make_blobs(rng, 200, 2, [[-1.0, -1.0], [1.0, 1.0]], 1.0)
    where = assign(list(recs), 3, 2, 11)
    model = sisa_train(recs, where, 3, 2, 40, 0.5, 0.01)
    for x, _ in test[:50]:
        votes = [1 if m.dot(row[-1][0], x) + row[-1][1] > 0 else 0 for row in model.ckpt]
        assert predict(model, x) == (1 if sum(votes) >= 2 else 0)
    assert m.accuracy(lambda x: predict(model, x), test) >= 0.85
    for victim in sorted(recs)[:10]:
        sisa_delete(model, victim)
    assert m.accuracy(lambda x: predict(model, x), test) >= 0.85


def test_gradient_steps_on_empty_data_do_nothing() -> None:
    start = ([0.5, -1.0], 0.25)
    assert gd_steps(start, [], 10, 0.5, 0.1) == (([0.5, -1.0], 0.25), 0)
