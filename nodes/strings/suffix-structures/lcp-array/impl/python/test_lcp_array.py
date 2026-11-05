# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lcp-array/. The authors are listed in prov/6RWY4Y.jsonl.

import random

from lcp_array import LcpArray, suffix_array


def naive_sa(t):
    return sorted(range(len(t)), key=lambda i: t[i:])


def naive_lcp(a, b):
    k = 0
    while k < len(a) and k < len(b) and a[k] == b[k]:
        k += 1
    return k


def texts(seed: int, count: int = 600, maxn: int = 14) -> list[str]:
    rng = random.Random(seed)
    out = ["", "a", "aa", "ab", "ba"]
    for n in range(1, 13):
        out += ["a" * n, "ab" * n, "aab" * n]
    for _ in range(count):
        sigma = rng.choice([1, 2, 4])
        out.append("".join(rng.choice("abcd"[:sigma]) for _ in range(rng.randrange(maxn + 1))))
    return out


def test_examples() -> None:
    x = LcpArray("banana")
    assert x.sa == [5, 3, 1, 0, 4, 2]
    assert x.lcp == [0, 1, 3, 0, 0, 2]
    x = LcpArray("mississippi")
    assert x.lcp == [0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]
    assert x.lce(1, 4) == 4
    assert x.lcp_ranks(0, 3) == 1


def test_edges() -> None:
    x = LcpArray("")
    assert x.sa == [] and x.lcp == []
    assert x.lce(0, 0) == 0
    x = LcpArray("a")
    assert x.lcp == [0] and x.lce(0, 0) == 1
    assert LcpArray("aaaa").lcp == [0, 1, 2, 3]
    assert LcpArray([3, 1, 3, 1]).lcp == [0, 1, 0, 2]


def test_against_naive() -> None:
    for t in texts(7):
        x = LcpArray(t)
        x.check_invariant()
        assert x.sa == naive_sa(t)
        assert x.lcp == [0 if i == 0 else naive_lcp(t[x.sa[i - 1] :], t[x.sa[i] :]) for i in range(len(t))]
        for p in range(len(t) + 1):
            for q in range(len(t) + 1):
                assert x.lce(p, q) == naive_lcp(t[p:], t[q:])


def test_given_suffix_array() -> None:
    rng = random.Random(3)
    for _ in range(200):
        t = [rng.randrange(3) for _ in range(rng.randrange(20))]
        sa = naive_sa(t)
        assert suffix_array(t) == sa
        assert LcpArray(t, sa).lcp == LcpArray(t).lcp
