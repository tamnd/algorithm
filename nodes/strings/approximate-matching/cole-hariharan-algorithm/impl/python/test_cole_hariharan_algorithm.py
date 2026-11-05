# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cole-hariharan-algorithm/. The authors are listed in prov/5Z7RCS.jsonl.

import random

import pytest
from cole_hariharan_algorithm import (
    candidate_windows,
    cole_hariharan,
    find_breaks,
    find_occurrences,
    period,
    plan,
)


def brute(pattern: str, text: str, k: int) -> list[int]:
    """Starts s with min over j of ed(pattern, text[s:j]) <= k, by one table per start."""
    m, n = len(pattern), len(text)
    out = []
    for s in range(n + 1):
        prev = list(range(m + 1))
        best = prev[m]
        for j in range(s, n):
            cur = [prev[0] + 1] + [0] * m
            for i in range(1, m + 1):
                cur[i] = min(cur[i - 1] + 1, prev[i] + 1, prev[i - 1] + (pattern[i - 1] != text[j]))
            prev = cur
            best = min(best, prev[m])
        if best <= k:
            out.append(s)
    return out


def naive_period(s: str) -> int:
    for p in range(1, len(s) + 1):
        if all(s[i] == s[i + p] for i in range(len(s) - p)):
            return p
    return 0


def test_example() -> None:
    p = "CCGTAATGCCTTTCCC"
    t = "TAACAGAGTTTTCCGTACTGCCTTCCCTCGAATGCGTGT"
    assert plan(p, 2) == [0, 4, 8, 12]
    assert find_occurrences(["CCGT", "AATG", "CCTT", "TCCC"], t) == {
        "CCGT": [12], "AATG": [30], "CCTT": [20], "TCCC": [23]}
    assert candidate_windows(p, t, 2, [0, 4, 8, 12]) == [5, 6, 7]
    assert cole_hariharan(p, t, 2) == [12] == brute(p, t, 2)
    assert cole_hariharan(p, t, 3) == [11, 12, 13] == brute(p, t, 3)


def test_edges() -> None:
    assert cole_hariharan("", "", 0) == [0]
    assert cole_hariharan("", "ab", 0) == [0, 1, 2]
    assert cole_hariharan("a", "", 0) == []
    assert cole_hariharan("a", "", 1) == [0]
    assert cole_hariharan("ab", "ab", 5) == [0, 1, 2]
    assert cole_hariharan("aba", "xxabaxx", 0) == [2]
    with pytest.raises(ValueError):
        cole_hariharan("a", "a", -1)


def test_breaks_and_periods() -> None:
    rng = random.Random(7)
    assert period("") == 0 and period("abab") == 2 and period("abc") == 3
    for _ in range(3000):
        alphabet = rng.choice(["a", "ab", "acgt"])
        s = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 25)))
        assert period(s) == naive_period(s)
        length, want = rng.randint(1, 9), rng.randint(0, 6)
        p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 60)))
        offsets = find_breaks(p, length, want)
        assert len(offsets) <= want
        for a, b in zip(offsets, offsets[1:]):
            assert a + length <= b
        for o in offsets:
            assert o + length <= len(p) and 2 * naive_period(p[o:o + length]) > length
        if offsets:
            words = [p[o:o + length] for o in offsets]
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 80)))
            occ = find_occurrences(words, t)
            for w in words:
                assert occ[w] == [i for i in range(len(t) - length + 1) if t[i:i + length] == w]


def planted(rng: random.Random, alphabet: str, m: int, n: int, k: int) -> tuple[str, str]:
    p = "".join(rng.choice(alphabet) for _ in range(m))
    t = "".join(rng.choice(alphabet) for _ in range(n))
    if m and rng.random() < 0.7:
        a = list(p)
        for _ in range(rng.randint(0, k + 1)):
            op, pos = rng.randint(0, 2), rng.randint(0, len(a))
            if op == 0:
                a.insert(pos, rng.choice(alphabet))
            elif pos < len(a):
                if op == 1:
                    del a[pos]
                else:
                    a[pos] = rng.choice(alphabet)
        cut = rng.randint(0, n)
        t = t[:cut] + "".join(a) + t[cut:]
    return p, t


@pytest.mark.parametrize("alphabet", ["ab", "acgt"])
def test_random_against_brute_force(alphabet: str) -> None:
    rng = random.Random(len(alphabet))
    sparse = 0
    for _ in range(700):
        k = rng.choice([0, 1, 1, 2, 2, 3])
        m = rng.choice([0, 1, 2, 5, rng.randint(0, 20), rng.randint(16, 40), 2 * k ** 3 + rng.randint(0, 20)])
        p, t = planted(rng, alphabet, m, rng.randint(0, 60), k)
        sparse += plan(p, k) is not None
        assert cole_hariharan(p, t, k) == brute(p, t, k), (p, t, k)
    assert sparse > 100


def test_mostly_periodic_pattern_uses_fallback() -> None:
    p = "ab" * 12
    assert plan(p, 2) is None
    t = "ab" * 10 + "b" + "ab" * 10
    assert cole_hariharan(p, t, 2) == brute(p, t, 2)
