# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kasai-algorithm/. The authors are listed in prov/0Z6PM0.jsonl.

import random

from kasai_algorithm import kasai, phi_lcp


def naive_sa(t):
    return sorted(range(len(t)), key=lambda i: t[i:])


def naive_lcp_array(t):
    sa = naive_sa(t)
    out = []
    for i in range(len(t)):
        if i == 0:
            out.append(0)
            continue
        a, b = t[sa[i - 1] :], t[sa[i] :]
        k = 0
        while k < len(a) and k < len(b) and a[k] == b[k]:
            k += 1
        out.append(k)
    return out


def texts(seed: int, count: int = 700, maxn: int = 16) -> list[str]:
    rng = random.Random(seed)
    out = ["", "a", "aa", "ab", "ba"]
    for n in range(1, 14):
        out += ["a" * n, "ab" * n, "aab" * n, "abaab" * (n // 2 + 1)]
    for _ in range(count):
        sigma = rng.choice([1, 2, 4])
        out.append("".join(rng.choice("abcd"[:sigma]) for _ in range(rng.randrange(maxn + 1))))
    return out


def test_examples() -> None:
    assert kasai("banana", [5, 3, 1, 0, 4, 2]) == [0, 1, 3, 0, 0, 2]
    t = "mississippi"
    assert kasai(t, naive_sa(t)) == [0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]


def test_edges() -> None:
    assert kasai("", []) == []
    assert kasai("x", [0]) == [0]
    assert kasai("aaaaa", [4, 3, 2, 1, 0]) == [0, 1, 2, 3, 4]
    assert kasai([2, 0, 2, 0], naive_sa([2, 0, 2, 0])) == [0, 1, 0, 2]


def test_against_naive() -> None:
    for t in texts(11):
        sa = naive_sa(t)
        want = naive_lcp_array(t)
        assert kasai(t, sa) == want
        assert phi_lcp(t, sa) == want


def test_long_unary_is_linear() -> None:
    t = "a" * 3000
    assert kasai(t, list(range(2999, -1, -1))) == list(range(3000))
