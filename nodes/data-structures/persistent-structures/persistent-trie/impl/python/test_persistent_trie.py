# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-trie/. The authors are listed in prov/BSY6SQ.jsonl.

import random
from collections import Counter

import pytest

from persistent_trie import PersistentTrie


def test_example() -> None:
    a = [5, 1, 6, 3]
    t = PersistentTrie(3)
    vs = [0]
    for x in a:
        vs.append(t.insert(vs[-1], x))
    assert t.num_nodes() == 1 + 4 * 4
    assert t.max_xor(vs[1], vs[3], 4) == 5
    assert t.max_xor(vs[0], vs[4], 4) == 7
    assert t.max_xor(vs[2], vs[4], 0) == 6
    assert t.keys(vs[2]) == [1, 5] and t.keys(vs[4]) == [1, 3, 5, 6]
    w = t.remove(vs[4], 6)
    assert t.keys(w) == [1, 3, 5] and t.keys(vs[4]) == [1, 3, 5, 6]
    assert t.max_xor(0, w, 0) == 5
    t.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        PersistentTrie(0)
    t = PersistentTrie(1)
    assert t.size(0) == 0 and t.keys(0) == [] and t.count(0, 1) == 0
    v = t.remove(0, 1)
    assert t.keys(v) == [] and t.num_nodes() == 1
    v = t.insert(0, 1)
    v = t.insert(v, 1)
    assert t.count(v, 1) == 2 and t.size(v) == 2
    assert t.max_xor(0, v, 1) == 0 and t.max_xor(0, v, 0) == 1
    with pytest.raises(ValueError):
        t.max_xor(v, v, 0)
    with pytest.raises(ValueError):
        t.insert(0, 2)
    with pytest.raises(IndexError):
        t.count(99, 0)
    t.check_invariant()


def test_deep() -> None:
    w = 30
    t = PersistentTrie(w)
    rng = random.Random(11)
    v = 0
    xs = [rng.randrange(1 << w) for _ in range(20000)]
    for x in xs:
        v = t.insert(v, x)
    assert t.num_nodes() == 1 + 20000 * (w + 1)
    y = rng.randrange(1 << w)
    assert t.max_xor(0, v, y) == max(x ^ y for x in xs)
    assert t.size(v) == 20000


def test_random_version_tree() -> None:
    rng = random.Random(9091)
    for _ in range(500):
        w = rng.randint(1, 5)
        t = PersistentTrie(w)
        model = [Counter()]
        for _ in range(rng.randint(1, 30)):
            v = rng.randrange(len(model))
            x = rng.randrange(1 << w)
            op = rng.random()
            if op < 0.5:
                assert t.insert(v, x) == len(model)
                model.append(model[v] + Counter([x]))
            elif op < 0.8:
                assert t.remove(v, x) == len(model)
                m = Counter(model[v])
                if m[x] > 0:
                    m[x] -= 1
                model.append(+m)
            else:
                assert t.count(v, x) == model[v][x]
        for v, m in enumerate(model):
            assert t.keys(v) == sorted(m.elements())
        t.check_invariant()


def test_random_range_max_xor() -> None:
    rng = random.Random(4242)
    for _ in range(500):
        w = rng.randint(1, 6)
        a = [rng.randrange(1 << w) for _ in range(rng.randint(1, 12))]
        t = PersistentTrie(w)
        vs = [0]
        for x in a:
            vs.append(t.insert(vs[-1], x))
        l = rng.randrange(len(a))
        r = rng.randint(l + 1, len(a))
        y = rng.randrange(1 << w)
        assert t.max_xor(vs[l], vs[r], y) == max(x ^ y for x in a[l:r])
