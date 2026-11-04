# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-search-symbol-table/. The authors are listed in prov/5G5MVH.jsonl.

import random

from sequential_search_symbol_table import SequentialSearchST


def test_example() -> None:
    st: SequentialSearchST[str, int] = SequentialSearchST()
    totals = []
    for v, k in enumerate("SEARCHEXAMPLE"):
        st.put(k, v)
        totals.append(st.compares)
        st.check_invariant()
    assert totals == [0, 1, 3, 6, 10, 15, 20, 26, 31, 38, 46, 55, 64]
    assert list(st.keys()) == list("LPMXHCRAES")
    assert [st.get(k) for k in "LPMXHCRAES"] == [11, 10, 9, 7, 5, 4, 3, 8, 12, 0]
    before = st.compares
    assert st.get("R") == 3 and st.compares - before == 7
    before = st.compares
    assert st.get("Z") is None and st.compares - before == 10


def test_edges() -> None:
    st: SequentialSearchST[int, str] = SequentialSearchST()
    assert st.get(1) is None and len(st) == 0 and not st.contains(1)
    st.delete(1)
    st.put(1, "a")
    st.put(1, "b")
    assert len(st) == 1 and st.get(1) == "b"
    st.put(2, "c")
    st.delete(1)
    assert list(st.keys()) == [2] and st.get(1) is None
    st.delete(2)
    assert len(st) == 0 and st.first is None
    st.check_invariant()


def test_build_compares() -> None:
    for n in range(0, 40):
        st: SequentialSearchST[int, int] = SequentialSearchST()
        for k in range(n):
            st.put(k, k)
        assert st.compares == n * (n - 1) // 2


def test_equal_values_not_identity() -> None:
    st: SequentialSearchST[str, int] = SequentialSearchST()
    a = "".join(["ke", "y"])
    st.put(a, 1)
    st.put("key", 2)
    assert len(st) == 1 and st.get("key") == 2


def test_random_against_dict() -> None:
    rng = random.Random(31)
    for _ in range(600):
        st: SequentialSearchST[int, int] = SequentialSearchST()
        model: dict[int, int] = {}
        for _ in range(rng.randint(0, 50)):
            k, r = rng.randrange(12), rng.random()
            if r < 0.4:
                assert st.get(k) == model.get(k)
                assert st.contains(k) == (k in model)
            elif r < 0.8:
                v = rng.randrange(1000)
                st.put(k, v)
                model[k] = v
            else:
                st.delete(k)
                model.pop(k, None)
            st.check_invariant()
            assert len(st) == len(model)
            assert sorted(st.keys()) == sorted(model)
