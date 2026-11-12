# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bowtie/. The authors are listed in prov/1P62H4.jsonl.

import random

from bowtie import Bowtie, FMIndex, naive


def rand_dna(rng: random.Random, n: int) -> str:
    return "".join(rng.choice("ACGT") for _ in range(n))


def test_exact_search_against_scan() -> None:
    rng = random.Random(1)
    for _ in range(100):
        t = rand_dna(rng, rng.randrange(0, 60))
        fm = FMIndex(t)
        p = rand_dna(rng, rng.randrange(1, 4))
        want = [s for s in range(len(t) - len(p) + 1) if t[s:s + len(p)] == p]
        assert fm.exact(p) == want


def test_page_example() -> None:
    ref = "GATTACAGATTGCA"
    bt = Bowtie(ref)
    hits, _ = bt.align("GATTAC", k=1)
    assert hits == [(0, "+", 0), (7, "+", 1)]
    assert hits == naive(ref, "GATTAC", 1)


def test_backtracking_against_scan() -> None:
    rng = random.Random(2)
    for _ in range(150):
        ref = rand_dna(rng, rng.randrange(10, 80))
        read = rand_dna(rng, rng.randrange(3, 10))
        if rng.random() < 0.7:
            s = rng.randrange(0, len(ref) - len(read) + 1)
            read = list(ref[s:s + len(read)])
            for _ in range(rng.randrange(0, 3)):
                read[rng.randrange(len(read))] = rng.choice("ACGT")
            read = "".join(read)
        bt = Bowtie(ref)
        for k in (0, 1, 2):
            hits, _ = bt.align(read, k=k, double=False)
            assert hits == naive(ref, read, k)


def test_double_indexing_against_scan() -> None:
    rng = random.Random(3)
    for _ in range(150):
        ref = rand_dna(rng, rng.randrange(10, 80))
        read = rand_dna(rng, rng.randrange(2, 10))
        if rng.random() < 0.7:
            s = rng.randrange(0, len(ref) - len(read) + 1)
            read = list(ref[s:s + len(read)])
            read[rng.randrange(len(read))] = rng.choice("ACGT")
            read = "".join(read)
        bt = Bowtie(ref)
        for k in (0, 1):
            hits, _ = bt.align(read, k=k, double=True)
            assert hits == naive(ref, read, k)


def test_double_indexing_backtracks_less() -> None:
    rng = random.Random(4)
    ref = rand_dna(rng, 3000)
    bt = Bowtie(ref)
    plain = double = 0
    for _ in range(30):
        s = rng.randrange(0, len(ref) - 30)
        read = list(ref[s:s + 30])
        read[rng.randrange(30)] = rng.choice("ACGT")
        read = "".join(read)
        h1, c1 = bt.align(read, k=1, double=False)
        h2, c2 = bt.align(read, k=1, double=True)
        assert h1 == h2
        plain += c1.steps
        double += c2.steps
    assert double < plain


def test_backtrack_limit_can_miss_hits() -> None:
    ref = "GATTACAGATTGCA"
    bt = Bowtie(ref)
    hits, cnt = bt.align("GATTAC", k=1, double=False, limit=0)
    assert hits == [(0, "+", 0)]
    assert cnt.backtracks == 0
