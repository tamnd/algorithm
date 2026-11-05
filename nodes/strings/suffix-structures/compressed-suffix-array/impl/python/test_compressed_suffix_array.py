# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compressed-suffix-array/. The authors are listed in prov/M2B1RW.jsonl.

import random

from compressed_suffix_array import CompressedSuffixArray


def naive(text: str) -> tuple[list[int], list[int]]:
    t = text + "\0"
    sa = sorted(range(len(t)), key=lambda i: t[i:])
    isa = [0] * len(t)
    for i, p in enumerate(sa):
        isa[p] = i
    return sa, [isa[(p + 1) % len(t)] for p in sa]


def check(text: str, step: int, block: int) -> None:
    csa = CompressedSuffixArray(text, step=step, block=block)
    sa, psi = naive(text)
    n = len(text)
    assert [csa.psi(i) for i in range(n + 1)] == psi
    assert [csa.lookup(i) for i in range(n + 1)] == sa
    assert [csa.inverse(p) for p in range(n + 1)] == [sa.index(p) for p in range(n + 1)]
    assert "".join(csa.extract(0, n)) == text
    pats = {text[i:j] for i in range(n) for j in range(i + 1, min(n, i + 4) + 1)} | {"x", "ab", "ba", "aa"}
    for pat in pats:
        occ = [i for i in range(n - len(pat) + 1) if text.startswith(pat, i)]
        assert csa.locate(pat) == occ


def test_banana() -> None:
    csa = CompressedSuffixArray("banana", step=2, block=4)
    assert [csa.psi(i) for i in range(7)] == [4, 0, 5, 6, 3, 1, 2]
    assert [csa.first(i) for i in range(7)] == [0, 1, 1, 1, 2, 3, 3]
    assert csa.find("ana") == (2, 4) and csa.locate("ana") == [1, 3]
    assert csa.lookup(2) == 3 and csa.extract(1, 4) == list("ana")
    check("banana", 2, 4)


def test_special() -> None:
    check("", 3, 2)
    for n in range(1, 30):
        check("a" * n, 4, 8)
        check("ab" * n, 3, 5)


def test_random() -> None:
    rng = random.Random(3)
    for trial in range(600):
        sigma = (1, 2, 4)[trial % 3]
        text = "".join(rng.choice("acgt"[:sigma]) for _ in range(rng.randrange(0, 30)))
        check(text, rng.randrange(1, 7), rng.randrange(1, 10))
