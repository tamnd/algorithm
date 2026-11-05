# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/duval-algorithm/. The authors are listed in prov/2134ZX.jsonl.

import itertools
import random
from typing import List

from duval_algorithm import duval, lyndon_factors


def is_lyndon(w: str) -> bool:
    return len(w) > 0 and all(w < w[i:] + w[:i] for i in range(1, len(w)))


def brute(w: str) -> List[str]:
    # All factorizations into Lyndon words, kept only if nonincreasing.
    n = len(w)
    found: List[List[str]] = []
    for mask in range(1 << max(n - 1, 0)):
        if n == 0:
            break
        cuts = [0] + [i + 1 for i in range(n - 1) if mask >> i & 1] + [n]
        parts = [w[cuts[r] : cuts[r + 1]] for r in range(len(cuts) - 1)]
        if all(is_lyndon(x) for x in parts) and all(
            parts[r] >= parts[r + 1] for r in range(len(parts) - 1)
        ):
            found.append(parts)
    if n == 0:
        return []
    assert len(found) == 1
    return found[0]


def test_example() -> None:
    assert duval("ababaab") == [0, 2, 4]
    assert lyndon_factors("ababaab") == ["ab", "ab", "aab"]


def test_edges() -> None:
    assert duval("") == []
    assert lyndon_factors("a") == ["a"]
    assert lyndon_factors("aaa") == ["a", "a", "a"]
    assert lyndon_factors("ba") == ["b", "a"]
    assert lyndon_factors("abac") == ["abac"]
    assert lyndon_factors("aba") == ["ab", "a"]
    assert lyndon_factors("banana") == ["b", "an", "an", "a"]
    assert lyndon_factors([3, 1, 2, 1, 2]) == [[3], [1, 2], [1, 2]]


def test_exhaustive_small() -> None:
    for sigma in (1, 2, 3):
        for n in range(0, 9 if sigma < 3 else 7):
            for t in itertools.product("abc"[:sigma], repeat=n):
                w = "".join(t)
                assert lyndon_factors(w) == brute(w), w


def test_random() -> None:
    rng = random.Random(1983)
    for _ in range(800):
        sigma = rng.choice((1, 2, 3))
        n = rng.randint(0, 13)
        w = "".join(rng.choice("abc"[:sigma]) for _ in range(n))
        f = lyndon_factors(w)
        assert f == brute(w), w
        assert "".join(f) == w
