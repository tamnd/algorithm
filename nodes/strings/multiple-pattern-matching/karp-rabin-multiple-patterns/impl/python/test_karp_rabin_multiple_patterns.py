# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-rabin-multiple-patterns/. The authors are listed in prov/HKXC4R.jsonl.

import random

from karp_rabin_multiple_patterns import karp_rabin_set, poly_hash


def naive(t, pats) -> list[tuple[int, int]]:
    out = []
    for j, q in enumerate(pats):
        for s in range(len(t) - len(q) + 1):
            if t[s : s + len(q)] == q:
                out.append((s, j))
    return sorted(out)


def ints(x: str) -> list[int]:
    return ["abcd".index(ch) for ch in x]


def test_example() -> None:
    # a and b have the codes 1 and 2, as on the page; p = 13 and r = 5.
    t = ints("abababbb")
    pats = [ints(x) for x in ["aba", "abb", "aba", "baa"]]
    assert [poly_hash([v + 1 for v in q], 5, 13) for q in pats] == [10, 11, 10, 4]
    stats: dict[str, int] = {}
    got = karp_rabin_set(t, pats, p=13, base=5, stats=stats)
    assert got == [(0, 0), (0, 2), (2, 0), (2, 2), (4, 1)]
    assert stats == {"checks": 4, "failed": 1}
    mc = karp_rabin_set(t, pats, p=13, base=5, verify=False)
    assert mc == sorted(got + [(5, 0), (5, 2)])


def test_small_cases() -> None:
    assert karp_rabin_set("", []) == []
    assert karp_rabin_set("", [""]) == [(0, 0)]
    assert karp_rabin_set("ab", ["", "x", "abc"]) == [(0, 0), (1, 0), (2, 0)]
    assert karp_rabin_set("aaaa", ["aa", "a", "aa"]) == sorted(
        [(0, 0), (1, 0), (2, 0), (0, 2), (1, 2), (2, 2)] + [(s, 1) for s in range(4)]
    )
    assert karp_rabin_set("ushers", ["he", "she", "his", "hers"]) == [(1, 1), (2, 0), (2, 3)]


def test_bad_bases_stay_exact() -> None:
    # r = 0 and r = 1 make many windows collide; the output is still exact.
    t = "abbaabab" * 5
    pats = ["ab", "ba", "aabb", "bbaa", "abab", "baba", ""]
    for r in (0, 1, 2):
        assert karp_rabin_set(t, pats, base=r) == naive(t, pats)


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
    pats = []
    for _ in range(rng.randint(1, 6)):
        kind = rng.randrange(5)
        if kind == 0 and t:
            i = rng.randrange(len(t))
            pats.append(t[i : i + rng.randint(1, 5)])
        elif kind == 1 and pats:
            q = rng.choice(pats)
            pats.append(q[: rng.randint(0, len(q))])  # a prefix of another pattern
        elif kind == 2 and pats:
            q = rng.choice(pats)
            pats.append(q[rng.randint(0, len(q)) :])  # a suffix of another pattern
        elif kind == 3 and pats:
            pats.append(rng.choice(pats))  # a pattern listed twice
        else:
            pats.append(random_text(rng, sigma, rng.randint(0, 5)))
    return pats


def test_random_against_naive() -> None:
    rng = random.Random(20261106)
    cases = 0
    for sigma in (1, 2, 4):
        for _ in range(400):
            t = random_text(rng, sigma, rng.randint(0, 30))
            pats = random_patterns(rng, t, sigma)
            want = naive(t, pats)
            assert karp_rabin_set(t, pats) == want
            # A tiny prime forces many failed verifications; the answer stays exact.
            # The codes are then 1 to 4, below every such prime.
            p = rng.choice([5, 7, 11, 13])
            ti, pi = ints(t), [ints(q) for q in pats]
            assert karp_rabin_set(ti, pi, p=p) == want
            # Without verification the answer contains every true pair.
            mc = karp_rabin_set(ti, pi, p=p, verify=False)
            assert set(want) <= set(mc)
            cases += 1
    assert cases >= 500


def test_int_sequences() -> None:
    rng = random.Random(7)
    for _ in range(200):
        t = [rng.randrange(3) for _ in range(rng.randint(0, 25))]
        pats = [[rng.randrange(3) for _ in range(rng.randint(0, 4))] for _ in range(rng.randint(1, 5))]
        assert karp_rabin_set(t, pats) == naive(t, pats)
