# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/suffix-array-search/. The authors are listed in prov/VMB6DY.jsonl.

import math
import random

from suffix_array_search import lcp_lr, sa_bound, sa_range


def naive_sa(s: str) -> list[int]:
    return sorted(range(len(s)), key=lambda i: s[i:])


def naive_lcp(s: str, sa: list[int]) -> list[int]:
    out = [0] * len(sa)
    for r in range(1, len(sa)):
        a, b, k = s[sa[r - 1]:], s[sa[r]:], 0
        while k < len(a) and k < len(b) and a[k] == b[k]:
            k += 1
        out[r] = k
    return out


def naive_range(s: str, sa: list[int], p: str) -> tuple[int, int]:
    heads = [s[i:i + len(p)] for i in sa]
    lo = sum(1 for h in heads if h < p)
    return lo, lo + sum(1 for h in heads if h == p)


def setup(s: str) -> tuple[list[int], list[int]]:
    sa = naive_sa(s)
    return sa, naive_lcp(s, sa)


def test_example() -> None:
    s = "mississippi"
    sa, lcp = setup(s)
    assert sa == [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    assert lcp == [0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]
    assert sa_range(s, sa, lcp, "ssi") == (9, 11)
    assert sa_range(s, sa, lcp, "issi") == (2, 4)
    assert sa_range(s, sa, lcp, "i") == (0, 4)
    assert sa_range(s, sa, lcp, "sp") == (9, 9)
    assert sa_range(s, sa, lcp, "z") == (11, 11)
    assert sa_range(s, sa, lcp, "a") == (0, 0)
    llcp, rlcp = lcp_lr(lcp)
    assert llcp[5] == 0 and rlcp[5] == 0
    assert llcp[8] == 0 and rlcp[8] == 0
    assert llcp[6] == 1 and rlcp[6] == 0


def test_lcp_lr_against_naive() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(0, 40)
        s = "".join(rng.choice("ab"[: rng.choice([1, 2])]) for _ in range(n))
        sa, lcp = setup(s)
        llcp, rlcp = lcp_lr(lcp)

        def pair(a: int, b: int) -> int:
            if a < 0 or b >= n:
                return 0
            return min(lcp[a + 1:b + 1])

        stack = [(-1, n)]
        while stack:
            lo, hi = stack.pop()
            if hi - lo <= 1:
                continue
            mid = (lo + hi) // 2
            assert llcp[mid] == pair(lo, mid) and rlcp[mid] == pair(mid, hi)
            stack += [(lo, mid), (mid, hi)]


def test_edges() -> None:
    assert sa_range("", [], [], "a") == (0, 0)
    assert sa_range("a", [0], [0], "a") == (0, 1)
    assert sa_range("a", [0], [0], "aa") == (1, 1)
    s = "aaaaaaaa"
    sa, lcp = setup(s)
    assert sa_range(s, sa, lcp, "aaa") == (2, 8)
    assert sa_range(s, sa, lcp, "a" * 9) == (8, 8)


def test_comparison_bound() -> None:
    rng = random.Random(77)
    for s in ("a" * 400, "ab" * 200, "".join(rng.choice("ab") for _ in range(400))):
        sa, lcp = setup(s)
        llcp, rlcp = lcp_lr(lcp)
        for m in (1, 5, 50, 150):
            i = rng.randrange(len(s) - m)
            for p in (s[i:i + m], s[i:i + m - 1] + "c", "a" * m):
                for strict in (False, True):
                    c = [0]
                    sa_bound(s, sa, llcp, rlcp, p, strict, c)
                    assert c[0] <= m + 2 * math.ceil(math.log2(len(s) + 1))


def test_random_against_naive() -> None:
    rng = random.Random(1993)
    for trial in range(700):
        sigma = "abcd"[: rng.choice([1, 2, 4])]
        n = rng.randint(0, 30)
        s = "".join(rng.choice(sigma) for _ in range(n))
        if trial % 35 == 0:
            s = rng.choice(["a" * n, "ab" * (n // 2), ""])
        sa, lcp = setup(s)
        for _ in range(10):
            p = "".join(rng.choice(sigma + "e") for _ in range(rng.randint(1, 6)))
            if s and rng.random() < 0.6:
                i = rng.randrange(len(s))
                p = s[i:rng.randint(i + 1, len(s))]
            assert sa_range(s, sa, lcp, p) == naive_range(s, sa, p)
