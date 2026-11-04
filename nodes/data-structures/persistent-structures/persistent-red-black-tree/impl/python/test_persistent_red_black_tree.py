# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-red-black-tree/. The authors are listed in prov/3F3XMG.jsonl.

import random

from persistent_red_black_tree import PersistentRedBlackTree


def shape(t: PersistentRedBlackTree[int]) -> str:
    def go(n: object) -> str:
        if n is None:
            return "."
        c = "R" if n.red else "B"  # type: ignore[attr-defined]
        left, right = go(n.left), go(n.right)  # type: ignore[attr-defined]
        if left == "." and right == ".":
            return f"{c}{n.key}"  # type: ignore[attr-defined]
        return f"({left} {c}{n.key} {right})"  # type: ignore[attr-defined]

    return go(t._root)


def test_example() -> None:
    vs = [PersistentRedBlackTree[int]()]
    for k in [1, 2, 3, 4, 5]:
        vs.append(vs[-1].insert(k))
    assert shape(vs[3]) == "(B1 B2 B3)"
    assert shape(vs[4]) == "(B1 B2 (. B3 R4))"
    assert shape(vs[5]) == "(B1 B2 (B3 R4 B5))"
    v6 = vs[5].delete(2)
    assert shape(v6) == "((. B1 R3) B4 B5)"
    assert list(vs[5].keys()) == [1, 2, 3, 4, 5]
    assert list(v6.keys()) == [1, 3, 4, 5]
    for v in vs + [v6]:
        v.check_invariant()


def test_edges() -> None:
    e = PersistentRedBlackTree[int]()
    assert e.delete(3) is e and not e.contains(3) and e.check_invariant() == 0
    one = e.insert(3)
    assert one.insert(3) is one and one.delete(4) is one
    assert list(one.delete(3).keys()) == []


def test_sorted_input_stays_balanced() -> None:
    t = PersistentRedBlackTree[int]()
    for k in range(4096):
        t = t.insert(k)
    bh = t.check_invariant()
    assert bh <= 13  # black height at most lg(n + 1) + 1
    for k in range(0, 4096, 2):
        t = t.delete(k)
    t.check_invariant()
    assert list(t.keys()) == list(range(1, 4096, 2))


def test_random_versions_against_sets() -> None:
    rng = random.Random(5150)
    for _ in range(600):
        versions = [PersistentRedBlackTree[int]()]
        models: list[frozenset[int]] = [frozenset()]
        for _ in range(rng.randint(1, 50)):
            j = rng.randrange(len(versions))
            k = rng.randint(0, 25)
            if rng.random() < 0.55:
                versions.append(versions[j].insert(k))
                models.append(models[j] | {k})
            else:
                versions.append(versions[j].delete(k))
                models.append(models[j] - {k})
            versions[-1].check_invariant()
        for v, m in zip(versions, models):
            v.check_invariant()
            assert list(v.keys()) == sorted(m)
            assert all(v.contains(k) == (k in m) for k in range(-1, 27))
