# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bwa/. The authors are listed in prov/M5J6FC.jsonl.

import random

from bwa import BWA, Counter, calculate_d, edit_distance, naive_ends, naive_smems, sellers_table


def rand_dna(rng: random.Random, n: int) -> str:
    return "".join(rng.choice("ACGT") for _ in range(n))


def test_edit_distance() -> None:
    assert edit_distance("GATTACA", "GATACA") == 1
    assert edit_distance("", "ACG") == 3
    assert edit_distance("ACGT", "TGCA") == 4


def test_page_example_d_array() -> None:
    bwa = BWA("ACGTTACGGA")
    # pieces: ACGTA is not a substring (ACGTT is), nor is ACGGT
    assert calculate_d(bwa.rev, "ACGTAACGGT") == [0, 0, 0, 0, 1, 1, 1, 1, 1, 2]
    assert calculate_d(bwa.rev, "TTACG") == [0, 0, 0, 0, 0]


def test_page_example_search() -> None:
    bwa = BWA("ACGTTACGGA")
    with_d, without_d = Counter(), Counter()
    assert bwa.end_positions("ACGTAACGGT", 1, True, with_d) == set()
    assert bwa.end_positions("ACGTAACGGT", 1, False, without_d) == set()
    assert (with_d.states, without_d.states) == (1, 34)
    assert bwa.end_positions("ACGTAACGGT", 2) == {9, 10}
    assert naive_ends("ACGTTACGGA", "ACGTAACGGT", 2) == {9, 10}
    assert bwa.end_positions("TTACG", 0) == {8}


def test_d_is_a_lower_bound() -> None:
    rng = random.Random(1)
    for _ in range(100):
        ref = rand_dna(rng, rng.randrange(5, 30))
        bwa = BWA(ref)
        w = rand_dna(rng, rng.randrange(1, 9))
        d = calculate_d(bwa.rev, w)
        table = sellers_table(ref, w)
        for i in range(len(w)):
            assert d[i] <= min(table[i + 1])


def test_sellers_table_matches_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(30):
        ref = rand_dna(rng, rng.randrange(0, 12))
        w = rand_dna(rng, rng.randrange(1, 5))
        table = sellers_table(ref, w)
        for e in range(len(ref) + 1):
            assert table[-1][e] == min(edit_distance(w, ref[s:e]) for s in range(e + 1))


def test_search_against_sellers() -> None:
    rng = random.Random(2)
    for _ in range(80):
        ref = rand_dna(rng, rng.randrange(5, 40))
        w = rand_dna(rng, rng.randrange(3, 8))
        if rng.random() < 0.6:
            s = rng.randrange(0, len(ref) - 2)
            w = ref[s:s + rng.randrange(3, 8)]
            w = list(w)
            for _ in range(rng.randrange(0, 2)):
                p = rng.randrange(len(w))
                op = rng.randrange(3)
                if op == 0:
                    w[p] = rng.choice("ACGT")
                elif op == 1 and len(w) > 3:
                    del w[p]
                else:
                    w.insert(p, rng.choice("ACGT"))
            w = "".join(w)
        bwa = BWA(ref)
        for z in (0, 1, 2):
            if z >= len(w):
                continue
            assert bwa.end_positions(w, z) == naive_ends(ref, w, z)
            assert bwa.end_positions(w, z, use_d=False) == naive_ends(ref, w, z)


def test_d_prunes_the_search() -> None:
    rng = random.Random(3)
    ref = rand_dna(rng, 400)
    bwa = BWA(ref)
    with_d = Counter()
    without_d = Counter()
    for _ in range(10):
        w = rand_dna(rng, 12)  # mostly absent reads, where D prunes most
        a = bwa.end_positions(w, 1, True, with_d)
        b = bwa.end_positions(w, 1, False, without_d)
        assert a == b
    assert with_d.states < without_d.states


def test_smems_against_naive() -> None:
    rng = random.Random(4)
    for _ in range(100):
        ref = rand_dna(rng, rng.randrange(1, 40))
        q = rand_dna(rng, rng.randrange(1, 15))
        assert BWA(ref).smems(q) == naive_smems(ref, q)


def test_smem_example() -> None:
    bwa = BWA("GATTACAGATTACC")
    assert bwa.matching_statistics("CATTACAGGATTAC") == [2, 7, 6, 5, 4, 3, 2, 1, 6, 5, 4, 3, 2, 1]
    assert bwa.smems("CATTACAGGATTAC") == [(0, 2), (1, 8), (8, 14)]
