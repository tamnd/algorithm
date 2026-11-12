# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blat/. The authors are listed in prov/6CXMHF.jsonl.

import random

from blat import (blat_candidates, build_index, clumps, multiple_hits, naive_clumps,
                  naive_multiple_hits, naive_near_hits, naive_perfect_hits, near_perfect_hits,
                  perfect_hits, whole_tiles)

DB = "GCTAAAGACAATTACATAACATACACGTCAGCACGAAACT"
QUERY = "AATTACATAAAATACACGTCAG"  # DB[9:31] with C -> A at query position 10


def rand_dna(rng: random.Random, n: int) -> str:
    return "".join(rng.choice("ACGT") for _ in range(n))


def test_page_example() -> None:
    idx = build_index(DB, 4)
    assert sorted(p for ps in idx.values() for p in ps) == list(range(0, 37, 4))
    hits = perfect_hits(idx, QUERY, 4)
    assert sorted(hits) == [(3, 12), (11, 20), (12, 12), (15, 24)]
    kept = multiple_hits(hits, 2, 10)
    assert kept == [(3, 12), (11, 20), (15, 24)]  # the lone hit on diagonal 0 goes
    assert clumps(kept, 10) == [(3, 15, 12, 24)]
    assert clumps(kept, 5) == [(3, 3, 12, 12), (11, 15, 20, 24)]
    assert blat_candidates(DB, QUERY, k=4, n_hits=2, window=10, max_gap=10) == [(3, 15, 12, 24)]


def test_index_and_hits_against_naive_scan() -> None:
    rng = random.Random(1)
    for _ in range(150):
        db = rand_dna(rng, rng.randrange(0, 60))
        q = rand_dna(rng, rng.randrange(0, 25))
        k = rng.randrange(2, 6)
        idx = build_index(db, k)
        assert sorted(perfect_hits(idx, q, k)) == naive_perfect_hits(db, q, k)
        assert near_perfect_hits(idx, q, k) == naive_near_hits(db, q, k)


def test_overused_tiles_are_dropped() -> None:
    db = "ACGT" * 10 + "TTTT"
    idx = build_index(db, 4, max_occ=3)
    assert "ACGT" not in idx and idx["TTTT"] == [40]


def test_multiple_hits_against_naive() -> None:
    rng = random.Random(2)
    for _ in range(200):
        hits = sorted({(rng.randrange(30), rng.randrange(30)) for _ in range(rng.randrange(0, 25))})
        n_hits, window = rng.randrange(1, 4), rng.randrange(0, 12)
        assert multiple_hits(hits, n_hits, window) == naive_multiple_hits(hits, n_hits, window)


def test_clumps_against_naive() -> None:
    rng = random.Random(3)
    for _ in range(200):
        hits = sorted({(rng.randrange(40), rng.randrange(40)) for _ in range(rng.randrange(0, 20))})
        gap = rng.randrange(0, 10)
        assert clumps(hits, gap) == naive_clumps(hits, gap)


def test_tile_guarantee() -> None:
    # an exact match of length h holds at least floor((h + 1) / k) - 1 whole tiles
    for k in range(1, 8):
        for h in range(0, 40):
            worst = min(whole_tiles(s, h, k) for s in range(0, 3 * k))
            assert worst == max(0, (h + 1) // k - 1)


def test_planted_match_is_found() -> None:
    rng = random.Random(4)
    k = 8
    for _ in range(20):
        db = rand_dna(rng, 3000)
        s = rng.randrange(0, 2900)
        q = rand_dna(rng, 20) + db[s:s + 2 * k - 1] + rand_dna(rng, 20)
        hits = perfect_hits(build_index(db, k), q, k)
        assert any(t - qq == s - 20 for qq, t in hits)  # a hit on the planted diagonal
