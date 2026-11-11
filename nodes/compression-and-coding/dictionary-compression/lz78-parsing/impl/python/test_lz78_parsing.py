# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lz78-parsing/. The authors are listed in prov/HYAQNT.jsonl.

# There is no standard library routine for the LZ78 parse. The tests use parses
# worked out by hand, a brute force from the definition, and the two counting
# bounds proved on the page.

import math
import random

from lz78_parsing import lz78_parse


def split(t: str) -> list[str]:
    return [t[s:s + ln] for s, ln in lz78_parse(t)]


def brute(t: str) -> list[str]:
    phrases: list[str] = []
    i = 0
    while i < len(t):
        k = 0
        while i + k < len(t) and t[i:i + k + 1] in phrases:
            k += 1
        w = t[i:i + k + 1]
        phrases.append(w)
        i += len(w)
    return phrases


def test_hand_examples() -> None:
    assert split("abracadabra") == ["a", "b", "r", "ac", "ad", "ab", "ra"]
    assert split("aaaaaaaa") == ["a", "aa", "aaa", "aa"]
    assert split("abababab") == ["a", "b", "ab", "aba", "b"]
    assert split("") == [] and split("q") == ["q"]


def test_matches_definition() -> None:
    rng = random.Random(41)
    for _ in range(300):
        t = "".join(rng.choice("abc"[: rng.randrange(1, 4)]) for _ in range(rng.randrange(60)))
        assert split(t) == brute(t)


def test_counting_bounds() -> None:
    rng = random.Random(42)
    for sigma in (2, 4, 16):
        for n in (100, 1000, 5000):
            t = [rng.randrange(sigma) for _ in range(n)]
            c = len(lz78_parse(t))
            new = c - 1  # all phrases but possibly the last are new
            # Lower bound: a prefix-closed set of new phrases has total length at most 1 + 2 + ... + new.
            assert n <= new * (new + 1) // 2 + new + 1
            # Upper bound: new * log_sigma(new / (2 sigma)) <= 2n when new >= 2 sigma,
            # so new <= max(4n / log_sigma n, 2 sigma sqrt(n)).
            if new >= 2 * sigma:
                assert new * math.log(new / (2 * sigma), sigma) <= 2 * n
            assert new <= max(4 * n / math.log(n, sigma), 2 * sigma * math.sqrt(n))
    # The worst case for the lower bound: a run of k(k+1)/2 equal symbols.
    k = 40
    assert len(lz78_parse("a" * (k * (k + 1) // 2))) == k
