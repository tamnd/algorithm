# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/suffix-tree/. The authors are listed in prov/21ZQTC.jsonl.

import random

from suffix_tree import SuffixTree


def naive_occ(s: str, p: str) -> list[int]:
    return [i for i in range(len(s) - len(p) + 1) if s[i:i + len(p)] == p]


def naive_node_count(s: str) -> int:
    """Leaves of S$ plus the root plus the right-branching substrings of S."""
    t = list(s) + [None]
    n = len(s)
    ext: dict[str, set] = {}
    for i in range(n):
        for j in range(i + 1, n + 1):
            ext.setdefault(s[i:j], set()).add(t[j])
    inner = sum(1 for x in ext.values() if len(x) >= 2)
    return (n + 1) + 1 + inner


def test_example() -> None:
    st = SuffixTree("banana")
    st.check_invariant()
    assert st.suffix_array() == [5, 3, 1, 0, 4, 2]
    assert st.node_count() == 11 and st.leaf_count() == 7
    assert st.occurrences("ana") == [1, 3]
    assert st.count("an") == 2 and st.count("nab") == 0
    assert st.count("") == 6
    st = SuffixTree("abab")
    st.check_invariant()
    assert st.node_count() == naive_node_count("abab") == 8


def test_edges() -> None:
    st = SuffixTree("")
    st.check_invariant()
    assert st.node_count() == 2 and st.suffix_array() == []
    assert st.count("a") == 0 and st.count("") == 0
    for n in (1, 2, 50, 300):
        st = SuffixTree("a" * n)
        st.check_invariant()
        assert st.node_count() == 2 * n + 1
        assert st.suffix_array() == list(range(n - 1, -1, -1))
    st = SuffixTree([3, 1, 4, 1, 5, 9, 2, 6])
    st.check_invariant()
    assert st.suffix_array() == [1, 3, 6, 0, 2, 4, 7, 5]


def test_random_against_naive() -> None:
    rng = random.Random(1973)
    for trial in range(600):
        sigma = "abcd"[: rng.choice([1, 2, 4])]
        n = rng.randint(0, 25)
        s = "".join(rng.choice(sigma) for _ in range(n))
        if trial % 30 == 0:
            s = rng.choice(["a" * n, "ab" * (n // 2), ""])
        st = SuffixTree(s)
        st.check_invariant()
        assert st.suffix_array() == sorted(range(len(s)), key=lambda i: s[i:])
        assert st.node_count() == naive_node_count(s)
        for _ in range(8):
            p = "".join(rng.choice(sigma + "e") for _ in range(rng.randint(0, 5)))
            if s and rng.random() < 0.5:
                i = rng.randrange(len(s))
                p = s[i:rng.randint(i, len(s))]
            occ = naive_occ(s, p)
            assert st.occurrences(p) == (occ if p else list(range(len(s))))
            assert st.count(p) == (len(occ) if p else len(s))
            assert st.contains(p) == (bool(occ) or p == "")
