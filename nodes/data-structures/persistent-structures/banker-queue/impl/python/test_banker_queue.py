# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/banker-queue/. The authors are listed in prov/WBJ0ZE.jsonl.

import random

import pytest

from banker_queue import BankerQueue


def test_example() -> None:
    q0: BankerQueue[int] = BankerQueue()
    q = q0
    lengths = []
    for x in [1, 2, 3, 4, 5]:
        q = q.snoc(x)
        q.check_invariant()
        lengths.append(q.lengths())
    assert lengths == [(1, 0), (1, 1), (3, 0), (3, 1), (3, 2)]
    q5 = q
    assert q5.head() == 1
    q6 = q5.tail()
    assert q6.lengths() == (2, 2)
    q7 = q6.tail()
    assert q7.lengths() == (3, 0)
    assert q7.to_list() == [3, 4, 5]
    # the old versions are unchanged
    assert q5.to_list() == [1, 2, 3, 4, 5]
    assert q6.to_list() == [2, 3, 4, 5]
    assert q0.to_list() == []


def test_edges() -> None:
    q: BankerQueue[str] = BankerQueue()
    assert q.is_empty() and len(q) == 0
    with pytest.raises(IndexError):
        q.head()
    with pytest.raises(IndexError):
        q.tail()
    one = q.snoc("a")
    assert one.head() == "a" and one.tail().is_empty()
    same = q.snoc(7).snoc(7).snoc(7)
    assert same.to_list() == [7, 7, 7]


def test_persistent_reuse() -> None:
    q: BankerQueue[int] = BankerQueue()
    for x in range(7):
        q = q.snoc(x)
    # q has lf = lr = ... ; branch it in many ways
    a = q.snoc(100)
    b = q.snoc(200)
    c = q.tail()
    assert a.to_list() == list(range(7)) + [100]
    assert b.to_list() == list(range(7)) + [200]
    assert c.to_list() == list(range(1, 7))
    assert q.to_list() == list(range(7))


def test_random_against_list() -> None:
    rng = random.Random(20261104)
    for _ in range(500):
        versions: list[tuple[BankerQueue[int], list[int]]] = [(BankerQueue(), [])]
        for _ in range(rng.randrange(1, 40)):
            q, model = versions[rng.randrange(len(versions))]  # any old version
            if model and rng.random() < 0.4:
                assert q.head() == model[0]
                q2, m2 = q.tail(), model[1:]
            else:
                x = rng.randrange(1000)
                q2, m2 = q.snoc(x), model + [x]
            assert len(q2) == len(m2)
            versions.append((q2, m2))
        for q, model in versions:
            q.check_invariant()
            assert q.to_list() == model
