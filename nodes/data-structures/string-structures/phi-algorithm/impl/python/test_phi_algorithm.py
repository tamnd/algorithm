# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phi-algorithm/. The authors are listed in prov/46X4G6.jsonl.

import random

from phi_algorithm import lcp_array, naive_lcp, plcp_array, suffix_array


def test_example() -> None:
    t = "banana"
    sa = suffix_array(t)
    assert sa == [5, 3, 1, 0, 4, 2]
    assert plcp_array(t, sa) == [0, 3, 2, 1, 0, 0]
    assert lcp_array(t, sa) == [0, 1, 3, 0, 0, 2]


def test_edges() -> None:
    assert lcp_array("", []) == [] and lcp_array("a", [0]) == [0]
    t = "aaaaaaa"
    assert lcp_array(t, suffix_array(t)) == [0, 1, 2, 3, 4, 5, 6]
    t = "abcdefg"
    assert lcp_array(t, suffix_array(t)) == [0] * 7
    t = [3, 1, 3, 1, 3]  # integer alphabets work too
    assert lcp_array(t, suffix_array(t)) == naive_lcp(t, suffix_array(t))


def test_plcp_property() -> None:
    # plcp[i + 1] >= plcp[i] - 1, the fact the algorithm relies on
    rng = random.Random(7)
    for _ in range(200):
        t = "".join(rng.choice("ab") for _ in range(rng.randint(1, 40)))
        p = plcp_array(t, suffix_array(t))
        assert all(p[i + 1] >= p[i] - 1 for i in range(len(t) - 1))


def test_random_against_naive() -> None:
    rng = random.Random(2009)
    for case in range(600):
        t = "".join(rng.choice("ab" if case % 2 else "acgt") for _ in range(rng.randint(0, 60)))
        sa = suffix_array(t)
        assert lcp_array(t, sa) == naive_lcp(t, sa)
