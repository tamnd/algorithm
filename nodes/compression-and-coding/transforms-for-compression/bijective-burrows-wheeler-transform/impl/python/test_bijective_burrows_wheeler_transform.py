# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bijective-burrows-wheeler-transform/. The authors are listed in prov/R9BPTQ.jsonl.

# Oracles: a brute-force Lyndon factorization (the first factor is the longest
# Lyndon prefix), an omega order sort that compares long prefixes of the
# infinite powers, and an exhaustive check that the transform is a bijection on
# all strings of each small length.

import itertools
import random
from functools import cmp_to_key

from bijective_burrows_wheeler_transform import (
    bbwt,
    inverse_bbwt,
    lf_mapping,
    lyndon_factorization,
)


def is_lyndon(w: str) -> bool:
    return all(w < w[i:] + w[:i] for i in range(1, len(w)))


def brute_lyndon(s: str) -> list[str]:
    out = []
    while s:
        k = max(k for k in range(1, len(s) + 1) if is_lyndon(s[:k]))
        out.append(s[:k])
        s = s[k:]
    return out


def brute_bbwt(s: str) -> str:
    rots = [w[i:] + w[:i] for w in brute_lyndon(s) for i in range(len(w))]

    def cmp(u: str, v: str) -> int:
        a = (u * (len(v) + 1))[: len(u) * len(v) + 1]
        b = (v * (len(u) + 1))[: len(u) * len(v) + 1]
        return (a > b) - (a < b)

    rots.sort(key=cmp_to_key(cmp))
    return "".join(r[-1] for r in rots)


def test_worked_examples() -> None:
    assert lyndon_factorization("banana") == ["b", "an", "an", "a"]
    assert bbwt("banana") == "annbaa"
    assert inverse_bbwt("annbaa") == "banana"
    assert lyndon_factorization("abracadabra") == ["abracad", "abr", "a"]
    assert bbwt("abracadabra") == brute_bbwt("abracadabra")
    assert lf_mapping("annbaa") == [0, 4, 5, 3, 1, 2]


def test_edges() -> None:
    assert bbwt("") == "" and inverse_bbwt("") == ""
    assert bbwt("a") == "a" and inverse_bbwt("a") == "a"
    assert bbwt("aaaa") == "aaaa" and inverse_bbwt("aaaa") == "aaaa"
    assert lyndon_factorization("aaaa") == ["a", "a", "a", "a"]
    assert lyndon_factorization("dcba") == ["d", "c", "b", "a"]


def test_duval_against_brute_force() -> None:
    rng = random.Random(9)
    for _ in range(500):
        s = "".join(rng.choice("abc") for _ in range(rng.randrange(0, 15)))
        f = lyndon_factorization(s)
        assert f == brute_lyndon(s)
        assert "".join(f) == s
        assert all(is_lyndon(w) for w in f)
        assert all(f[i] >= f[i + 1] for i in range(len(f) - 1))


def test_bijective_on_all_short_strings() -> None:
    for alphabet, max_len in (("ab", 10), ("abc", 6)):
        for n in range(max_len + 1):
            images = set()
            for tup in itertools.product(alphabet, repeat=n):
                s = "".join(tup)
                t = bbwt(s)
                assert sorted(t) == sorted(s)
                assert inverse_bbwt(t) == s
                images.add(t)
            assert len(images) == len(alphabet) ** n  # injective, so onto Sigma^n


def test_against_brute_and_random() -> None:
    rng = random.Random(2009)
    for _ in range(300):
        s = "".join(rng.choice("abcd"[: rng.randrange(1, 5)]) for _ in range(rng.randrange(0, 40)))
        assert bbwt(s) == brute_bbwt(s)
        assert inverse_bbwt(bbwt(s)) == s
    for s in ["xy" * 60, "z" * 150, "mississippi" * 10, "".join(chr(rng.randrange(33, 127)) for _ in range(200))]:
        assert inverse_bbwt(bbwt(s)) == s
