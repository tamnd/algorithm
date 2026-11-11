# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lempel-ziv-factorization/. The authors are listed in prov/N569BT.jsonl.

# There is no standard library routine for the LZ factorization. The tests use
# factorizations worked out by hand, the example of Kärkkäinen, Kempa and
# Puglisi (CPM 2013, Section 2: zzzzzipzip has 5 factors), and a quadratic
# brute force that follows the definition.

import math
import random

from lempel_ziv_factorization import lz_factorize, suffix_array


def brute(t: str, overlap: bool = True) -> list[tuple[int, int]]:
    """(start, length) of each factor, straight from the definition."""
    out, i, n = [], 0, len(t)
    while i < n:
        best = 0
        for j in range(i):
            k = 0
            while i + k < n and t[j + k] == t[i + k] and (overlap or j + k < i):
                k += 1
            best = max(best, k)
        out.append((i, max(best, 1)))
        i += max(best, 1)
    return out


def pieces(t: str) -> list[str]:
    return [t[s:s + ln] for s, ln, _ in lz_factorize(t)]


def test_hand_examples() -> None:
    assert pieces("abababab") == ["a", "b", "ababab"]
    assert pieces("aaaaaaaa") == ["a", "aaaaaaa"]
    assert pieces("abracadabra") == ["a", "b", "r", "a", "c", "a", "d", "abra"]
    assert pieces("zzzzzipzip") == ["z", "zzzz", "i", "p", "zip"]
    assert pieces("") == [] and pieces("x") == ["x"]


def test_without_self_reference_has_more_factors() -> None:
    assert [ln for _, ln in brute("abababab", overlap=False)] == [1, 1, 2, 4]
    assert [ln for _, ln in brute("aaaaaaaa", overlap=False)] == [1, 1, 2, 4]


def test_sources_are_earlier_copies() -> None:
    t = "mississippi$mississippi"
    for s, ln, src in lz_factorize(t):
        if src < 0:
            assert ln == 1 and t[s] not in t[:s]
        else:
            assert src < s and t[src:src + ln] == t[s:s + ln]


def test_suffix_array() -> None:
    assert suffix_array("banana") == [5, 3, 1, 0, 4, 2]
    rng = random.Random(8)
    for _ in range(100):
        t = "".join(rng.choice("ab") for _ in range(rng.randrange(1, 30)))
        assert suffix_array(t) == sorted(range(len(t)), key=lambda i: t[i:])


def test_matches_brute_force() -> None:
    rng = random.Random(9)
    for _ in range(400):
        t = "".join(rng.choice("abc"[: rng.randrange(1, 4)]) for _ in range(rng.randrange(0, 40)))
        assert [(s, ln) for s, ln, _ in lz_factorize(t)] == brute(t)


def test_bytes_and_long_inputs() -> None:
    rng = random.Random(10)
    data = bytes(rng.randrange(256) for _ in range(3000))
    f = lz_factorize(data)
    assert sum(ln for _, ln, _ in f) == len(data)
    run = b"a" * 5000
    assert len(lz_factorize(run)) == 2
    fib = "a"
    prev = "b"
    while len(fib) < 3000:
        fib, prev = fib + prev, fib
    # The factor count of a Fibonacci word grows like the logarithm of its length.
    assert len(lz_factorize(fib)) < 3 * math.log2(len(fib))


def test_count_is_at_most_twice_lz78() -> None:
    rng = random.Random(12)
    for _ in range(100):
        t = "".join(rng.choice("ab") for _ in range(rng.randrange(1, 200)))
        phrases, cur, seen = 0, "", {""}
        for ch in t:
            cur += ch
            if cur not in seen:
                seen.add(cur)
                phrases += 1
                cur = ""
        phrases += cur != ""
        assert len(lz_factorize(t)) <= 2 * phrases
