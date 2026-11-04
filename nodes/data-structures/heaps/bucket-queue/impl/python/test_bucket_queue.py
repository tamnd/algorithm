# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bucket-queue/. The authors are listed in prov/DVKCF0.jsonl.

import random

import pytest

from bucket_queue import BucketQueue


def test_example() -> None:
    q: BucketQueue[str] = BucketQueue(6)
    for x, k in [("a", 4), ("b", 2), ("c", 5), ("d", 2), ("e", 6)]:
        q.insert(x, k)
    q.check_invariant()
    assert q.cur == 2
    assert q.extract_min() == ("b", 2)
    assert q.extract_min() == ("d", 2)
    q.decrease_key("c", 3)
    assert q.extract_min() == ("c", 3)
    q.insert("f", 1)
    assert q.cur == 1
    q.delete("a")
    assert q.extract_min() == ("f", 1)
    assert q.extract_min() == ("e", 6)
    assert len(q) == 0
    q.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        BucketQueue(-1)
    q: BucketQueue[int] = BucketQueue(0)
    with pytest.raises(IndexError):
        q.extract_min()
    with pytest.raises(IndexError):
        q.find_min()
    with pytest.raises(ValueError):
        q.insert(1, 1)
    q.insert(1, 0)
    with pytest.raises(KeyError):
        q.insert(1, 0)
    assert 1 in q
    assert q.find_min() == (1, 0)
    with pytest.raises(ValueError):
        q.decrease_key(1, 1)
    with pytest.raises(KeyError):
        q.delete(2)
    assert q.extract_min() == (1, 0)


def test_fifo_within_bucket() -> None:
    q: BucketQueue[int] = BucketQueue(3)
    for x in range(10):
        q.insert(x, 1)
    assert [q.extract_min()[0] for _ in range(10)] == list(range(10))


def test_monotone_scan_count() -> None:
    # Dial's use: keys never go below the last extracted key.
    c = 50
    q: BucketQueue[int] = BucketQueue(c)
    rng = random.Random(7)
    last = 0
    q.insert(0, 0)
    nxt = 1
    out = []
    while len(q):
        x, k = q.extract_min()
        assert k >= last
        last = k
        out.append(k)
        for _ in range(rng.randrange(3)):
            if nxt < 200:
                q.insert(nxt, min(c, k + rng.randrange(5)))
                nxt += 1
    assert out == sorted(out)
    assert q.cur <= c + 1


def test_random_against_model() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        c = rng.randrange(1, 12)
        q: BucketQueue[int] = BucketQueue(c)
        model: dict[int, int] = {}
        order: dict[int, int] = {}
        stamp = 0
        nxt = 0
        for _ in range(rng.randrange(1, 40)):
            op = rng.randrange(4)
            if op == 0 or not model:
                k = rng.randrange(c + 1)
                q.insert(nxt, k)
                model[nxt] = k
                order[nxt] = stamp
                stamp += 1
                nxt += 1
            elif op == 1:
                x = min(model, key=lambda y: (model[y], order[y]))
                assert q.extract_min() == (x, model.pop(x))
            elif op == 2:
                x = rng.choice(sorted(model))
                k = rng.randrange(model[x] + 1)
                q.decrease_key(x, k)
                model[x] = k
                order[x] = stamp
                stamp += 1
            else:
                x = rng.choice(sorted(model))
                assert q.delete(x) == model.pop(x)
            q.check_invariant()
            assert len(q) == len(model)
