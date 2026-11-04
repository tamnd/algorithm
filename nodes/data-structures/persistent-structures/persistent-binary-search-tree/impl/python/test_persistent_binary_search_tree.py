# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-binary-search-tree/. The authors are listed in prov/F9C8A3.jsonl.

import random

from persistent_binary_search_tree import PersistentBinarySearchTree, count_nodes


def test_example() -> None:
    vs = [PersistentBinarySearchTree[int]()]
    for k in [50, 30, 70, 20, 40, 60, 80]:
        vs.append(vs[-1].insert(k))
    assert count_nodes(*vs) == 1 + 2 + 2 + 3 + 3 + 3 + 3
    v7 = vs[7]
    v8 = v7.insert(35)
    assert count_nodes(v7, v8) - count_nodes(v7) == 4
    v9 = v8.delete(50)
    assert count_nodes(v8, v9) - count_nodes(v8) == 2
    assert v9._root is not None and v9._root.key == 60
    assert list(v7.keys()) == [20, 30, 40, 50, 60, 70, 80]
    assert list(v8.keys()) == [20, 30, 35, 40, 50, 60, 70, 80]
    assert list(v9.keys()) == [20, 30, 35, 40, 60, 70, 80]
    # v9 shares the whole left subtree of v8.
    assert v8._root is not None and v9._root.left is v8._root.left


def test_edges() -> None:
    e = PersistentBinarySearchTree[int]()
    assert not e.contains(1) and list(e.keys()) == [] and e.delete(1) is e
    one = e.insert(1)
    assert one.insert(1) is one and one.delete(2) is one
    assert list(one.delete(1).keys()) == [] and list(one.keys()) == [1]


def test_sorted_input_is_tall_but_safe() -> None:
    t = PersistentBinarySearchTree[int]()
    for k in range(5000):
        t = t.insert(k)
    assert t.height() == 5000
    assert t.contains(4999) and not t.contains(5000)
    t2 = t.delete(0)
    assert t.contains(0) and not t2.contains(0)


def test_random_versions_against_sets() -> None:
    rng = random.Random(8361)
    for _ in range(500):
        versions = [PersistentBinarySearchTree[int]()]
        models: list[frozenset[int]] = [frozenset()]
        for _ in range(rng.randint(1, 30)):
            j = rng.randrange(len(versions))
            k = rng.randint(0, 15)
            if rng.random() < 0.6:
                versions.append(versions[j].insert(k))
                models.append(models[j] | {k})
            else:
                versions.append(versions[j].delete(k))
                models.append(models[j] - {k})
            versions[-1].check_invariant()
        for v, m in zip(versions, models):
            assert list(v.keys()) == sorted(m)
            for k in range(-1, 17):
                assert v.contains(k) == (k in m)
