# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rabin-karp/. The authors are listed in prov/1B6QTQ.jsonl.

import random

import pytest

from rabin_karp import MERSENNE_61, codes, rabin_karp


def naive(t, q) -> list[int]:
    return [s for s in range(len(t) - len(q) + 1) if t[s : s + len(q)] == q]


def ints(x: str) -> list[int]:
    return ["abcd".index(ch) for ch in x]


def poly_hash(x, r: int, p: int) -> int:
    v = 0
    for c in codes(x):
        v = (v * r + c) % p
    return v


def test_example() -> None:
    # a and b have the codes 1 and 2, as on the page.
    t, q = ints("abababbb"), ints("aba")
    stats: dict[str, int] = {}
    assert rabin_karp(t, q, p=13, base=5, stats=stats) == [0, 2]
    assert stats == {"hits": 3, "spurious": 1}
    assert rabin_karp(t, q, p=13, base=5, verify=False) == [0, 2, 5]


def test_example_hashes() -> None:
    code = {"a": 1, "b": 2}
    def h(x: str) -> int:
        v = 0
        for ch in x:
            v = (v * 5 + code[ch]) % 13
        return v
    assert [h("abababbb"[s : s + 3]) for s in range(6)] == [10, 5, 10, 5, 11, 10]
    assert [r for r in range(13) if (r * r + 1) % 13 == 0] == [5, 8]


def test_edges() -> None:
    assert rabin_karp("", "") == [0]
    assert rabin_karp("abc", "") == [0, 1, 2, 3]
    assert rabin_karp("", "a") == []
    assert rabin_karp("ab", "abc") == []
    assert rabin_karp("aaaa", "aa") == [0, 1, 2]
    assert rabin_karp("abc", "abc") == [0]
    assert rabin_karp([0, 1, 0, 1, 0], [0, 1, 0]) == [0, 2]
    with pytest.raises(ValueError):
        rabin_karp("abc", "b", p=11)


def test_base_zero_and_one_still_exact() -> None:
    # Bad bases give many hash hits, but verification keeps the answer exact.
    for b in (0, 1):
        assert rabin_karp("abcabcba", "abc", p=101, base=b) == [0, 3]
    stats: dict[str, int] = {}
    rabin_karp("abccbaabc", "abc", p=101, base=1, stats=stats)
    assert stats["spurious"] >= 1  # anagrams collide when r = 1


def test_random_vs_naive() -> None:
    rng = random.Random(20261105)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(400):
            n = rng.randrange(0, 40)
            if rng.random() < 0.3:
                unit = "".join(rng.choice(alphabet) for _ in range(rng.randrange(1, 4)))
                t = (unit * (n // len(unit) + 1))[:n]
            else:
                t = "".join(rng.choice(alphabet) for _ in range(n))
            kind = rng.randrange(4)
            if kind == 0 and t:
                i = rng.randrange(len(t))
                q = t[i : i + rng.randrange(0, 8)]
            elif kind == 1 and t:
                q = t[: rng.randrange(0, len(t) + 1)]
            elif kind == 2 and t:
                q = t[rng.randrange(0, len(t) + 1) :]
            else:
                q = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 6)))
            expected = naive(t, q)
            assert rabin_karp(t, q) == expected
            # A tiny prime gives many spurious hits; verification removes them all.
            p = rng.choice([101, 103, 107])
            stats: dict[str, int] = {}
            assert rabin_karp(ints(t), ints(q), p=p, stats=stats) == expected
            if q and len(q) <= len(t):
                assert stats["hits"] == len(expected) + stats["spurious"]
            mc = rabin_karp(ints(t), ints(q), p=p, base=rng.randrange(p), verify=False)
            assert set(expected) <= set(mc)


def test_collision_count_per_window() -> None:
    # For fixed distinct strings of length m, at most m - 1 of the p bases give equal hashes.
    rng = random.Random(7)
    p = 101
    for _ in range(300):
        m = rng.randrange(1, 7)
        x = "".join(rng.choice("abcd") for _ in range(m))
        y = "".join(rng.choice("abcd") for _ in range(m))
        if x == y:
            continue
        bad = sum(poly_hash(ints(x), r, p) == poly_hash(ints(y), r, p) for r in range(p))
        assert bad <= m - 1


def test_window_update_matches_direct_hash() -> None:
    rng = random.Random(3)
    for _ in range(200):
        t = "".join(rng.choice("abcd") for _ in range(rng.randrange(1, 30)))
        m = rng.randrange(1, len(t) + 1)
        r = rng.randrange(MERSENNE_61)
        expected_hits = [
            s for s in range(len(t) - m + 1) if poly_hash(t[s : s + m], r, MERSENNE_61) == poly_hash(t[:m], r, MERSENNE_61)
        ]
        assert rabin_karp(t, t[:m], base=r, verify=False) == expected_hits
