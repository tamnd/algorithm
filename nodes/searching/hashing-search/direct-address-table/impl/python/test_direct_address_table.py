# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-address-table/. The authors are listed in prov/QBRTYG.jsonl.

import random

import pytest

from direct_address_table import DirectAddressTable, SparseDirectAddressTable


def test_page_example() -> None:
    t: DirectAddressTable[str] = DirectAddressTable(10)
    t.insert(3, "a")
    t.insert(7, "b")
    t.insert(0, "c")
    assert len(t) == 3
    t.insert(3, "d")
    assert len(t) == 3 and t.search(3) == "d"
    assert t.delete(7)
    assert not t.delete(5)
    assert len(t) == 2
    assert t.search(7) is None and list(t.keys()) == [0, 3]
    t.check_invariant()


def test_sparse_page_example() -> None:
    t: SparseDirectAddressTable[int] = SparseDirectAddressTable(8, garbage_seed=1)
    for k in [5, 2, 7]:
        t.insert(k, 10 * k)
    assert t.keys() == [5, 2, 7]
    assert [t.idx[5], t.idx[2], t.idx[7]] == [0, 1, 2]
    assert t.delete(5)
    assert t.keys() == [7, 2] and t.idx[7] == 0 and t.idx[5] == 0
    assert not t.contains(5)
    t.idx[4] = 1  # garbage that points into the used part
    assert not t.contains(4)
    t.check_invariant()


def test_none_value_and_range() -> None:
    t: DirectAddressTable[None] = DirectAddressTable(3)
    t.insert(1, None)
    assert t.contains(1) and t.search(1) is None and len(t) == 1
    for bad in (-1, 3):
        with pytest.raises(KeyError):
            t.search(bad)
    s: SparseDirectAddressTable[int] = SparseDirectAddressTable(0)
    with pytest.raises(KeyError):
        s.insert(0, 1)
    assert len(DirectAddressTable(0)) == 0


def test_sparse_clear() -> None:
    t: SparseDirectAddressTable[int] = SparseDirectAddressTable(20, garbage_seed=3)
    for k in range(0, 20, 3):
        t.insert(k, k)
    t.clear()
    assert len(t) == 0 and all(not t.contains(k) for k in range(20))
    t.insert(4, 9)
    assert t.search(4) == 9 and t.keys() == [4]
    t.check_invariant()


def test_random_against_dict() -> None:
    rng = random.Random(2024)
    for trial in range(600):
        u = rng.randint(1, 30)
        a: DirectAddressTable[int] = DirectAddressTable(u)
        b: SparseDirectAddressTable[int] = SparseDirectAddressTable(u, garbage_seed=trial)
        model: dict[int, int] = {}
        for _ in range(rng.randint(0, 60)):
            k = rng.randrange(u)
            op = rng.random()
            if op < 0.45:
                v = rng.randint(0, 99)
                a.insert(k, v)
                b.insert(k, v)
                model[k] = v
            elif op < 0.75:
                assert a.delete(k) == (k in model) == b.delete(k)
                model.pop(k, None)
            elif op < 0.78:
                b.clear()
                for key in list(model):
                    a.delete(key)
                model.clear()
            else:
                assert a.search(k) == model.get(k) == b.search(k)
            a.check_invariant()
            b.check_invariant()
            assert len(a) == len(model) == len(b)
            assert list(a.keys()) == sorted(model) == sorted(b.keys())
