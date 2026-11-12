# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fasta-algorithm/. The authors are listed in prov/VK9YGQ.jsonl.

import itertools
import random

from fasta_algorithm import (
    banded_local_score,
    diagonal_regions,
    fasta_pair,
    fasta_search,
    join_regions,
    ktup_matches,
    rescore,
    smith_waterman,
)


def dna(a: str, b: str) -> int:
    return 5 if a == b else -4


def rand_seq(rng: random.Random, n: int) -> str:
    return "".join(rng.choice("ACGT") for _ in range(n))


def test_ktup_matches_against_naive_scan() -> None:
    rng = random.Random(1)
    for _ in range(100):
        q, y = rand_seq(rng, rng.randint(0, 20)), rand_seq(rng, rng.randint(0, 20))
        k = rng.randint(1, 4)
        naive = [(i, j) for j in range(len(y) - k + 1) for i in range(len(q) - k + 1) if q[i : i + k] == y[j : j + k]]
        assert sorted(ktup_matches(q, y, k)) == sorted(naive)


def test_rescore_is_the_best_subsegment() -> None:
    rng = random.Random(2)
    for _ in range(200):
        q, y = rand_seq(rng, 20), rand_seq(rng, 20)
        i0, j0 = rng.randint(0, 10), rng.randint(0, 10)
        length = rng.randint(0, 20 - max(i0, j0))
        a, b, ln, s = rescore(q, y, (i0, j0, length, 0), dna)
        assert b - a == j0 - i0 and i0 <= a and a + ln <= i0 + length
        assert s == sum(dna(q[a + k], y[b + k]) for k in range(ln))
        brute = max(
            [0] + [sum(dna(q[i0 + k], y[j0 + k]) for k in range(u, v)) for u in range(length) for v in range(u + 1, length + 1)]
        )
        assert s == brute


def test_join_regions_against_all_subsets() -> None:
    rng = random.Random(3)
    for _ in range(200):
        regions = []
        for _ in range(rng.randint(1, 6)):
            regions.append((rng.randint(0, 30), rng.randint(0, 30), rng.randint(1, 6), rng.randint(1, 40)))
        pen = rng.randint(0, 25)
        brute = 0
        for r in range(1, len(regions) + 1):
            for sub in itertools.combinations(regions, r):
                chain = sorted(sub)
                if all(
                    a[0] + a[2] <= b[0] and a[1] + a[2] <= b[1] for a, b in zip(chain, chain[1:])
                ):
                    brute = max(brute, sum(x[3] for x in chain) - pen * (len(chain) - 1))
        assert join_regions(regions, pen) == brute


def test_full_band_is_smith_waterman() -> None:
    rng = random.Random(4)
    for _ in range(100):
        q, y = rand_seq(rng, rng.randint(1, 15)), rand_seq(rng, rng.randint(1, 15))
        assert banded_local_score(q, y, dna, 4, 0, 40) == smith_waterman(q, y, dna, 4)


def test_score_order_init1_opt_sw() -> None:
    rng = random.Random(5)
    for _ in range(200):
        q = rand_seq(rng, 40)
        y = rand_seq(rng, 15) + q[8:30] + rand_seq(rng, 15)
        if rng.random() < 0.5:
            pos = rng.randint(16, 30)
            y = y[:pos] + rand_seq(rng, rng.randint(1, 5)) + y[pos:]
        r = fasta_pair(q, y, 2, dna, 4, penalty=20, gap=8, width=8)
        assert r["init1"] <= r["opt"] <= smith_waterman(q, y, dna, 8)
        assert r["init1"] <= r["initn"]


def test_band_can_miss_the_best_alignment() -> None:
    # The second half of the shared part is shifted by 12 positions, so the
    # best alignment leaves a band of width 8 around the first half.
    rng = random.Random(6)
    a, b = rand_seq(rng, 20), rand_seq(rng, 20)
    q = a + b
    y = a + rand_seq(rng, 12) + b
    narrow = fasta_pair(q, y, 2, dna, 4, gap=1, width=8)
    assert narrow["opt"] < smith_waterman(q, y, dna, 1)
    wide = fasta_pair(q, y, 2, dna, 4, gap=1, width=32)
    assert wide["opt"] == smith_waterman(q, y, dna, 1)


def test_no_ktup_match_means_no_score() -> None:
    q = "ACACACACAC"
    y = "AGAGAGAGAG"
    assert fasta_pair(q, y, 2, dna, 4) == {"init1": 0, "initn": 0, "opt": 0}
    # ACACACACA against AGAGAGAGA: 5 matches and 4 mismatches give 25 - 16
    assert smith_waterman(q, y, dna, 4) == 9


def test_regions_follow_the_distance_rule() -> None:
    # Matches at subject 0 and 5 on diagonal 0, ktup 2, value 4:
    # gap = 5 - 2 = 3 <= 4, so they join with score 4 - 3 + 4 = 5.
    regs = diagonal_regions([(0, 0), (5, 5)], 2, 4)
    assert regs == [(0, 0, 7, 5)]
    # at distance 6 > 4 they stay apart
    regs = diagonal_regions([(0, 0), (8, 8)], 2, 4)
    assert sorted(regs) == [(0, 0, 2, 4), (8, 8, 2, 4)]


def test_search_ranks_the_planted_relative_first() -> None:
    rng = random.Random(7)
    q = rand_seq(rng, 60)
    lib = [rand_seq(rng, 80) for _ in range(9)]
    lib.insert(4, rand_seq(rng, 10) + q[5:55] + rand_seq(rng, 10))
    res = fasta_search(q, lib, 4, dna, 16, top=3)
    assert res[0][0] == 4
