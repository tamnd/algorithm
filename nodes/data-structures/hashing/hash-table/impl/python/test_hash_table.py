# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-table/. The authors are listed in prov/42GYZ4.jsonl.

import random

from hash_table import HashTable


def keys_of(t: HashTable) -> list[list[int]]:
    return [[k for k, _ in b] for b in t.buckets]


def test_page_example() -> None:
    t: HashTable[int, str] = HashTable(4)
    states = []
    for k in [10, 22, 31, 4, 15, 28, 17]:
        t.insert(k, str(k))
        t.check_invariant()
        states.append(keys_of(t))
    assert states[3] == [[4], [], [10, 22], [31]]
    assert states[4] == [[], [], [10], [], [4], [], [22], [31, 15]]
    assert states[6] == [[], [17], [10], [], [4, 28], [], [22], [31, 15]]
    assert t.m == 8 and len(t) == 7
    assert t.search(28) == "28"
    assert t.search(12) is None
    assert t.delete(22)
    assert len(t) == 6 and t.search(22) is None
    t.check_invariant()


def test_edges() -> None:
    t: HashTable[str, int] = HashTable(1)
    assert t.search("a") is None and not t.delete("a") and len(t) == 0
    t.insert("a", 1)
    t.insert("a", 2)
    assert len(t) == 1 and t.search("a") == 2
    t.insert("b", None)  # type: ignore[arg-type]
    assert t.contains("b") and t.search("b") is None
    assert t.delete("a") and not t.delete("a")
    t.check_invariant()


def test_all_keys_collide() -> None:
    t: HashTable[int, int] = HashTable(4, h=lambda k: 0)
    for k in range(50):
        t.insert(k, k * k)
        t.check_invariant()
    assert all(t.search(k) == k * k for k in range(50))
    assert sum(1 for b in t.buckets if b) == 1


def test_big_and_negative_keys() -> None:
    t: HashTable[int, int] = HashTable()
    ks = [2**63 - 1, -(2**63), -1, -2, 0, 2**64 + 5]
    for k in ks:
        t.insert(k, k)
    t.check_invariant()
    assert all(t.search(k) == k for k in ks)


def test_random_against_dict() -> None:
    rng = random.Random(4242)
    for trial in range(600):
        h = (lambda k: k % 3) if trial % 5 == 0 else hash
        t: HashTable[int, int] = HashTable(rng.randint(1, 5), h=h)
        model: dict[int, int] = {}
        for _ in range(rng.randint(0, 60)):
            k = rng.randint(-20, 20)
            op = rng.random()
            if op < 0.5:
                v = rng.randint(0, 99)
                t.insert(k, v)
                model[k] = v
            elif op < 0.75:
                assert t.delete(k) == (k in model)
                model.pop(k, None)
            else:
                assert t.search(k) == model.get(k)
            t.check_invariant()
            assert len(t) == len(model)
        assert dict(t.items()) == model
