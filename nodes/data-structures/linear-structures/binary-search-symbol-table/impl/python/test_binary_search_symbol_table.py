# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-search-symbol-table/. The authors are listed in prov/7XC042.jsonl.

import bisect
import random

from binary_search_symbol_table import BinarySearchST


def test_page_example() -> None:
    st: BinarySearchST[str, int] = BinarySearchST()
    for i, c in enumerate("SEARCHEXAMPLE"):
        st.put(c, i)
        st.check_invariant()
    assert "".join(st.keys) == "ACEHLMPRSX"
    assert st.vals == [8, 4, 12, 5, 11, 9, 10, 3, 0, 7]
    assert st.get("E") == 12 and st.get("F") is None
    assert st.rank("F") == 3
    assert st.ceiling("F") == "H" and st.floor("F") == "E"
    assert st.select(5) == "M"
    assert st.size_range("F", "Q") == 4
    st.delete("H")
    assert "".join(st.keys) == "ACELMPRSX"
    assert st.min() == "A" and st.max() == "X"


def test_empty_and_edges() -> None:
    st: BinarySearchST[int, str] = BinarySearchST()
    assert st.rank(5) == 0 and st.get(5) is None
    assert st.floor(5) is None and st.ceiling(5) is None
    st.delete(5)
    st.put(5, "a")
    assert st.floor(4) is None and st.ceiling(6) is None
    assert st.floor(5) == 5 and st.ceiling(5) == 5
    assert st.size_range(6, 1) == 0
    st.delete(5)
    assert len(st) == 0


def test_random_against_dict() -> None:
    rng = random.Random(1946)
    for _ in range(600):
        st: BinarySearchST[int, int] = BinarySearchST()
        model: dict[int, int] = {}
        for _ in range(rng.randrange(1, 40)):
            k = rng.randrange(30)
            r = rng.random()
            if r < 0.6:
                v = rng.randrange(1000)
                st.put(k, v); model[k] = v
            else:
                st.delete(k); model.pop(k, None)
            st.check_invariant()
            ks = sorted(model)
            assert st.keys == ks and st.vals == [model[x] for x in ks]
            q = rng.randrange(-2, 33)
            assert st.rank(q) == bisect.bisect_left(ks, q)
            assert st.get(q) == model.get(q)
            fl = [x for x in ks if x <= q]
            ce = [x for x in ks if x >= q]
            assert st.floor(q) == (fl[-1] if fl else None)
            assert st.ceiling(q) == (ce[0] if ce else None)
            lo, hi = sorted((rng.randrange(30), rng.randrange(30)))
            assert st.size_range(lo, hi) == sum(1 for x in ks if lo <= x <= hi)
