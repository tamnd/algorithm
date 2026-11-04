# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/union-find-with-rollback/. The authors are listed in prov/CSRV45.jsonl.

import random

import pytest

from union_find_with_rollback import UnionFindWithRollback


def test_example() -> None:
    u: UnionFindWithRollback[int] = UnionFindWithRollback()
    for x in range(6):
        u.make_set(x)
    assert u.union(0, 1) and u.union(2, 3)
    t = u.snapshot()
    assert t == 2
    assert u.union(1, 3) and u.union(4, 5)
    assert not u.union(0, 2)
    u.check_invariant()
    assert [u.parent[x] for x in range(6)] == [1, 3, 3, 3, 5, 5]
    assert u.history == [(0, 1), (2, 3), (1, 3), (4, 5), None]
    assert u.connected(0, 2)
    u.rollback(t)
    u.check_invariant()
    assert [u.parent[x] for x in range(6)] == [1, 1, 3, 3, 4, 5]
    assert u.size[1] == 2 and u.size[3] == 2 and u.size[5] == 1
    assert not u.connected(0, 2)
    assert u.count == 4


def test_edges() -> None:
    u: UnionFindWithRollback[str] = UnionFindWithRollback()
    with pytest.raises(IndexError):
        u.undo()
    u.make_set("a")
    assert not u.union("a", "a")
    u.undo()
    assert u.snapshot() == 0
    with pytest.raises(ValueError):
        u.rollback(1)
    with pytest.raises(ValueError):
        u.make_set("a")


def test_height_is_logarithmic() -> None:
    u: UnionFindWithRollback[int] = UnionFindWithRollback()
    n = 1 << 11
    for x in range(n):
        u.make_set(x)
    for x in range(1, n):
        u.union(x, x - 1)
    u.check_invariant()
    u.rollback(0)
    assert u.count == n
    u.check_invariant()


def test_random_against_label_stack() -> None:
    rng = random.Random(41)
    for _ in range(500):
        n = rng.randrange(1, 12)
        u: UnionFindWithRollback[int] = UnionFindWithRollback()
        for x in range(n):
            u.make_set(x)
        labels = [list(range(n))]
        for _ in range(rng.randrange(40)):
            r = rng.random()
            label = labels[-1]
            a, b = rng.randrange(n), rng.randrange(n)
            if r < 0.45:
                assert u.union(a, b) == (label[a] != label[b])
                old, new = label[a], label[b]
                labels.append([new if v == old else v for v in label])
            elif r < 0.65 and len(labels) > 1:
                u.undo()
                labels.pop()
            elif r < 0.75:
                t = rng.randrange(len(labels))
                u.rollback(t)
                del labels[t + 1 :]
            else:
                assert u.connected(a, b) == (label[a] == label[b])
            u.check_invariant()
            assert u.count == len(set(labels[-1]))
