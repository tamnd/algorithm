# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semi-persistent-array/. The authors are listed in prov/07TV6Q.jsonl.

import random

import pytest

from semi_persistent_array import SemiPersistentArray


def test_example() -> None:
    v0 = SemiPersistentArray([0, 0, 0, 0])
    v1 = v0.set(1, 5)
    v2 = v1.set(3, 7)
    v3 = v2.set(1, 9)
    assert v3.to_list() == [0, 9, 0, 7]
    assert v3._store.a == [0, 9, 0, 7]
    assert v0.get(1) == 0 and v1.get(1) == 5 and v2.get(1) == 5 and v2.get(3) == 7
    assert v1.to_list() == [0, 5, 0, 0]
    # Update v1: the array is rolled back to v1, and v2, v3 become invalid.
    v4 = v1.set(2, 4)
    assert v4.to_list() == [0, 5, 4, 0]
    assert v1.to_list() == [0, 5, 0, 0] and v0.to_list() == [0, 0, 0, 0]
    assert not v2.is_valid() and not v3.is_valid()
    with pytest.raises(ValueError):
        v3.get(0)
    with pytest.raises(ValueError):
        v2.set(0, 1)
    for v in (v0, v1, v4):
        v.check_invariant()


def test_edges() -> None:
    e: SemiPersistentArray[int] = SemiPersistentArray([])
    assert len(e) == 0 and e.to_list() == []
    with pytest.raises(IndexError):
        e.get(0)
    one = SemiPersistentArray(["a"])
    two = one.set(0, "b")
    same = two.set(0, "b")
    assert same.to_list() == ["b"] and one.get(0) == "a"
    again = one.set(0, "c")
    assert again.get(0) == "c" and not two.is_valid() and not same.is_valid()
    with pytest.raises(IndexError):
        again.set(1, "x")
    again.check_invariant()


def test_deep() -> None:
    n = 1000
    v0 = SemiPersistentArray(list(range(n)))
    v = v0
    versions = [v0]
    for k in range(200000):
        v = v.set(k % n, -k)
        if k % 5000 == 0:
            versions.append(v)
    assert v.get(5) == -199005
    assert v0.get(5) == 5  # walks 200000 diffs without recursion
    w = v0.set(0, 42)  # rolls back 200000 diffs
    assert w.to_list()[:3] == [42, 1, 2]
    assert all(not x.is_valid() for x in versions[1:])
    w.check_invariant()


def test_random_semi_persistent_use() -> None:
    rng = random.Random(8080)
    for _ in range(500):
        n = rng.randint(1, 6)
        start = [rng.randint(0, 9) for _ in range(n)]
        v0 = SemiPersistentArray(start)
        # path holds the valid versions, oldest first, with their models.
        path = [(v0, list(start))]
        dead = []
        for _ in range(rng.randint(1, 40)):
            j = rng.randrange(len(path))
            v, m = path[j]
            if rng.random() < 0.5:
                i, x = rng.randrange(n), rng.randint(0, 9)
                w = v.set(i, x)
                dead.extend(p for p, _ in path[j + 1 :])
                m2 = list(m)
                m2[i] = x
                path = path[: j + 1] + [(w, m2)]
            else:
                i = rng.randrange(n)
                assert v.get(i) == m[i]
        for v, m in path:
            assert v.is_valid() and v.to_list() == m
            v.check_invariant()
        for v in dead:
            assert not v.is_valid()
            with pytest.raises(ValueError):
                v.get(0)
