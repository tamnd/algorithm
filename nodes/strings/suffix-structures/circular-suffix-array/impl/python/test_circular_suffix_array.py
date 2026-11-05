# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circular-suffix-array/. The authors are listed in prov/DE34MK.jsonl.

import random

from circular_suffix_array import CircularSuffixArray, cyclic_sort


def naive_ca(t):
    return sorted(range(len(t)), key=lambda i: (t[i:] + t[:i], i))


def texts(seed: int, count: int = 700, maxn: int = 14) -> list[str]:
    rng = random.Random(seed)
    out = ["", "a", "aa", "ab", "ba"]
    for n in range(1, 13):
        out += ["a" * n, "ab" * n, "aab" * n]
    for _ in range(count):
        sigma = rng.choice([1, 2, 4])
        out.append("".join(rng.choice("abcd"[:sigma]) for _ in range(rng.randrange(maxn + 1))))
    return out


def test_examples() -> None:
    x = CircularSuffixArray("banana")
    assert x.ca == [5, 3, 1, 0, 4, 2]
    assert x.bwt() == (list("nnbaaa"), 3)
    x = CircularSuffixArray("abab")
    assert x.ca == [0, 2, 1, 3]
    assert x.cls == [0, 1, 0, 1]
    x = CircularSuffixArray("abracadabra")
    assert "".join(x.bwt()[0]) == "rdarcaaaabb"
    assert x.find("aa") == [10]
    assert x.find("abra") == [0, 7]


def test_edges() -> None:
    x = CircularSuffixArray("")
    assert x.ca == [] and x.bwt() == ([], -1) and x.find("a") == []
    x = CircularSuffixArray("z")
    assert x.ca == [0] and x.bwt() == (["z"], 0)
    assert CircularSuffixArray("aaaa").ca == [0, 1, 2, 3]
    assert CircularSuffixArray([2, 1, 2, 1]).ca == [1, 3, 0, 2]


def test_against_naive() -> None:
    for t in texts(5):
        x = CircularSuffixArray(t)
        x.check_invariant()
        assert x.ca == naive_ca(t)
        n = len(t)
        if n:
            assert x.least_rotation() == min(range(n), key=lambda i: (t[i:] + t[:i], i))
            doubled = t + t
            for m in range(1, n + 1):
                for p in {doubled[i : i + m] for i in range(n)} | {"ca"[: min(m, 2)]}:
                    want = [i for i in range(n) if doubled[i : i + len(p)] == p]
                    assert x.find(p) == want


def test_sentinel_gives_suffix_array() -> None:
    rng = random.Random(9)
    for _ in range(300):
        t = "".join(rng.choice("ab") for _ in range(rng.randrange(12))) + "$"
        sa = sorted(range(len(t)), key=lambda i: t[i:])
        assert cyclic_sort(t)[0] == sa
