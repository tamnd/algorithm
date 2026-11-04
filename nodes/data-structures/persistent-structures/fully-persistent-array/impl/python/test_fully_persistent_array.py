# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fully-persistent-array/. The authors are listed in prov/MX556Y.jsonl.

import math
import random

import pytest

from fully_persistent_array import FullyPersistentArray


def test_example() -> None:
    a = FullyPersistentArray([10, 20, 30, 40])
    assert a.node_count() == 7
    v1 = a.set(0, 2, 33)
    v2 = a.set(0, 0, 11)
    v3 = a.set(v1, 3, 44)
    assert (v1, v2, v3) == (1, 2, 3)
    assert a.to_list(0) == [10, 20, 30, 40]
    assert a.to_list(1) == [10, 20, 33, 40]
    assert a.to_list(2) == [11, 20, 30, 40]
    assert a.to_list(3) == [10, 20, 33, 44]
    assert a.get(3, 2) == 33 and a.get(2, 2) == 30
    assert a.node_count() == 16


def test_edges() -> None:
    e: FullyPersistentArray[int] = FullyPersistentArray([])
    assert len(e) == 0 and e.to_list(0) == []
    with pytest.raises(IndexError):
        e.get(0, 0)
    one = FullyPersistentArray([5])
    v = one.set(0, 0, 6)
    assert one.get(0, 0) == 5 and one.get(v, 0) == 6
    with pytest.raises(IndexError):
        one.get(2, 0)
    with pytest.raises(IndexError):
        one.set(0, 1, 0)


def test_random_version_tree() -> None:
    rng = random.Random(556)
    checks = 0
    for n in (1, 2, 3, 7, 8, 13, 64, 100):
        init = [rng.randrange(1000) for _ in range(n)]
        a = FullyPersistentArray(init)
        ref = [list(init)]
        for _ in range(300):
            t = rng.randrange(len(ref))
            if rng.random() < 0.5:
                i = rng.randrange(n)
                x = rng.randrange(1000)
                v = a.set(t, i, x)
                assert v == len(ref)
                new = list(ref[t])
                new[i] = x
                ref.append(new)
            else:
                i = rng.randrange(n)
                assert a.get(t, i) == ref[t][i]
            checks += 1
        for t, r in enumerate(ref):
            assert a.to_list(t) == r
            checks += 1
        bound = (2 * n - 1) + (len(ref) - 1) * (math.ceil(math.log2(n)) + 1)
        assert a.node_count() <= bound
    assert checks >= 500
