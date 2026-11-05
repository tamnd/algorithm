# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-horspool/. The authors are listed in prov/3G04XE.jsonl.

import random

from set_horspool import build, set_horspool


def naive(t, pats) -> list[tuple[int, int]]:
    out = []
    for j, q in enumerate(pats):
        for s in range(len(t) - len(q) + 1):
            if t[s : s + len(q)] == q:
                out.append((s, j))
    return sorted(out)


def test_example() -> None:
    pats = ["aab", "abaa", "bab"]
    _, _, lmin, shift = build(pats)
    assert lmin == 3 and shift == {"a": 1, "b": 2}
    stats: dict[str, int] = {}
    got = set_horspool("cabaabcbabaab", pats, stats)
    assert got == [(1, 1), (3, 0), (7, 2), (8, 1), (10, 0)]
    assert stats == {"reads": 27, "windows": 7}


def test_small_cases() -> None:
    assert set_horspool("", []) == []
    assert set_horspool("", [""]) == [(0, 0)]
    assert set_horspool("ab", ["", "x", "abc"]) == [(0, 0), (1, 0), (2, 0)]
    assert set_horspool("ushers", ["he", "she", "his", "hers"]) == [(1, 1), (2, 0), (2, 3)]
    assert set_horspool("aaaa", ["aa", "a", "aa"]) == naive("aaaa", ["aa", "a", "aa"])
    assert set_horspool([1, 2, 1, 2], [[2, 1], [1]]) == [(0, 1), (1, 0), (2, 1)]


def test_shift_is_largest_safe() -> None:
    # The shift of each character is the smallest distance at which some pattern can end.
    rng = random.Random(5)
    for _ in range(300):
        pats = ["".join(rng.choice("abc") for _ in range(rng.randint(1, 6))) for _ in range(rng.randint(1, 4))]
        _, _, lmin, shift = build(pats)
        for c in "abcd":
            want = lmin
            for q in pats:
                for d in range(1, len(q)):
                    if q[len(q) - 1 - d] == c:
                        want = min(want, d)
            assert shift.get(c, lmin) == want


def random_text(rng: random.Random, sigma: int, n: int) -> str:
    kind = rng.randrange(3)
    if kind == 0:
        return "".join(rng.choice("abcd"[:sigma]) for _ in range(n))
    period = "".join(rng.choice("abcd"[:sigma]) for _ in range(rng.randint(1, 4)))
    s = (period * (n // len(period) + 1))[:n]
    if kind == 2 and n > 0:
        i = rng.randrange(n)
        s = s[:i] + rng.choice("abcd"[:sigma]) + s[i + 1 :]
    return s


def random_patterns(rng: random.Random, t: str, sigma: int) -> list[str]:
    pats: list[str] = []
    for _ in range(rng.randint(1, 6)):
        kind = rng.randrange(5)
        if kind == 0 and t:
            i = rng.randrange(len(t))
            pats.append(t[i : i + rng.randint(1, 6)])
        elif kind == 1 and pats:
            q = rng.choice(pats)
            pats.append(q[: rng.randint(0, len(q))])  # a prefix of another pattern
        elif kind == 2 and pats:
            q = rng.choice(pats)
            pats.append(q[rng.randint(0, len(q)) :])  # a suffix of another pattern
        elif kind == 3 and pats:
            pats.append(rng.choice(pats))  # a pattern listed twice
        else:
            pats.append(random_text(rng, sigma, rng.randint(0, 6)))
    return pats


def test_random_against_naive() -> None:
    rng = random.Random(20261106)
    cases = 0
    for sigma in (1, 2, 4):
        for _ in range(500):
            t = random_text(rng, sigma, rng.randint(0, 40))
            pats = random_patterns(rng, t, sigma)
            assert set_horspool(t, pats) == naive(t, pats)
            cases += 1
    assert cases >= 500


def test_worst_case_reads() -> None:
    # Text a^n and pattern b a^(L-1) with L >= 3: every window reads L characters
    # (L - 1 that match and one that does not) and shifts by 1.
    for L in (3, 4, 8):
        stats: dict[str, int] = {}
        assert set_horspool("a" * 100, ["b" + "a" * (L - 1)], stats) == []
        assert stats["windows"] == 100 - L + 1
        assert stats["reads"] == (100 - L + 1) * L
