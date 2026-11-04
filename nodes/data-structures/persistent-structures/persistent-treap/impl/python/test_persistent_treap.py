# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-treap/. The authors are listed in prov/XM4DVE.jsonl.

import random

import pytest

from persistent_treap import PersistentTreap, count_nodes


def _shape(t):  # type: ignore[no-untyped-def]
    if t is None:
        return None
    return (t.key, _shape(t.left), _shape(t.right))


def test_example() -> None:
    prios = {50: 0.9, 30: 0.6, 70: 0.8, 20: 0.3, 40: 0.5, 60: 0.7, 80: 0.4}
    v0 = PersistentTreap(seed=1)
    for k in (20, 30, 40, 50, 60, 70, 80):
        v0 = v0.insert(k, prios[k])
    assert _shape(v0._root) == (
        50,
        (30, (20, None, None), (40, None, None)),
        (70, (60, None, None), (80, None, None)),
    )
    v1 = v0.insert(65, 0.75)
    assert _shape(v1._root) == (
        50,
        (30, (20, None, None), (40, None, None)),
        (70, (65, (60, None, None), None), (80, None, None)),
    )
    assert count_nodes(v0, v1) == 7 + 4
    v2 = v1.delete(50)
    assert _shape(v2._root) == (
        70,
        (65, (60, (30, (20, None, None), (40, None, None)), None), None),
        (80, None, None),
    )
    assert count_nodes(v0, v1, v2) == 11 + 3
    assert v0.keys() == [20, 30, 40, 50, 60, 70, 80]
    assert v1.keys() == [20, 30, 40, 50, 60, 65, 70, 80]
    assert v2.keys() == [20, 30, 40, 60, 65, 70, 80]
    a, b = v1.split(45)
    assert a.keys() == [20, 30, 40] and b.keys() == [50, 60, 65, 70, 80]
    assert a.merge(b).keys() == v1.keys()
    for v in (v0, v1, v2, a, b):
        v.check_invariant()


def test_edges() -> None:
    e = PersistentTreap(seed=7)
    assert len(e) == 0 and e.keys() == [] and not e.contains(3)
    assert e.delete(3) is e
    one = e.insert(3)
    assert one.insert(3) is one
    assert one.keys() == [3] and e.keys() == []
    assert one.delete(3).keys() == []
    assert one.min() == one.max() == 3 and one.kth(0) == 3
    with pytest.raises(ValueError):
        e.min()
    with pytest.raises(IndexError):
        one.kth(1)
    with pytest.raises(ValueError):
        one.merge(one)
    x, y = e.split(0)
    assert len(x) == len(y) == 0
    assert e.merge(one).keys() == [3] and one.merge(e).keys() == [3]


def test_deep_sorted_input() -> None:
    t = PersistentTreap(seed=99)
    n = 50000
    for k in range(n):
        t = t.insert(k)
    assert len(t) == n and t.kth(n // 2) == n // 2
    assert t.height() < 80
    t.check_invariant()
    u = t
    for k in range(0, n, 2):
        u = u.delete(k)
    assert len(u) == n // 2 and len(t) == n
    u.check_invariant()


def test_random_version_tree() -> None:
    rng = random.Random(6007)
    for run in range(500):
        versions = [PersistentTreap(seed=run)]
        model = [set()]
        for _ in range(rng.randint(1, 40)):
            v = rng.randrange(len(versions))
            k = rng.randint(0, 20)
            op = rng.random()
            if op < 0.45:
                versions.append(versions[v].insert(k))
                model.append(model[v] | {k})
            elif op < 0.8:
                versions.append(versions[v].delete(k))
                model.append(model[v] - {k})
            elif op < 0.9:
                a, b = versions[v].split(k)
                assert a.keys() == sorted(x for x in model[v] if x < k)
                assert b.keys() == sorted(x for x in model[v] if x >= k)
                versions.append(a.merge(b))
                model.append(set(model[v]))
            else:
                assert versions[v].contains(k) == (k in model[v])
        for t, m in zip(versions, model):
            assert t.keys() == sorted(m)
            assert len(t) == len(m)
            t.check_invariant()
