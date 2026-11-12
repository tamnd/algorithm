# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mummer/. The authors are listed in prov/VB8A1D.jsonl.

import random

from mummer import (brute_force_chain, chain_mums, edit_distance, find_mums, lcp_array, mummer,
                    naive_mems, naive_mums, suffix_array)


def rand_dna(rng: random.Random, n: int) -> str:
    return "".join(rng.choice("ACGT") for _ in range(n))


def test_lcp_array() -> None:
    rng = random.Random(1)
    for _ in range(50):
        s = rand_dna(rng, rng.randrange(1, 30)) + "$"
        sa = suffix_array(s)
        lcp = lcp_array(s, sa)
        for r in range(1, len(s)):
            x, y = s[sa[r - 1]:], s[sa[r]:]
            h = 0
            while h < min(len(x), len(y)) and x[h] == y[h]:
                h += 1
            assert lcp[r] == h


def test_mums_against_naive_scan() -> None:
    rng = random.Random(2)
    for _ in range(300):
        a = rand_dna(rng, rng.randrange(1, 25))
        b = rand_dna(rng, rng.randrange(1, 25))
        if rng.random() < 0.5:
            b = a[: rng.randrange(len(a) + 1)] + rand_dna(rng, 2) + a[rng.randrange(len(a) + 1):]
        m = rng.randrange(1, 4)
        mums = find_mums(a, b, m)
        assert mums == naive_mums(a, b, m)
        assert set(mums) <= set(naive_mems(a, b, m))


def test_chain_against_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(150):
        a = rand_dna(rng, rng.randrange(5, 40))
        b = rand_dna(rng, rng.randrange(5, 40))
        mums = find_mums(a, b, 1)[:12]
        chain = chain_mums(mums)
        assert sum(m[2] for m in chain) == brute_force_chain(mums)
        assert all(x[0] < y[0] and x[1] < y[1] for x, y in zip(chain, chain[1:]))


def test_page_example() -> None:
    a = "GATTACAGGCTTACGATCCA"
    b = "GATTACATGCTTACGTTCCATT"
    assert find_mums(a, b, 3) == [(0, 0, 7), (8, 8, 7), (16, 16, 4)]
    chain, gaps, cost = mummer(a, b, 3)
    assert chain == [(0, 0, 7), (8, 8, 7), (16, 16, 4)]
    assert gaps == [("SNP", 1), ("SNP", 1), ("insertion", 2)]
    assert cost == 4 == edit_distance(a, b)


def test_repeat_gap() -> None:
    # ACGTA and ACCCTTGG share the letter A of A[4]: the MUMs overlap in A
    a, b = "ACGTACCCTTGG", "ACGTAGACCCTTGG"
    assert find_mums(a, b, 3) == [(0, 0, 5), (4, 6, 8)]
    chain, gaps, cost = mummer(a, b, 3)
    assert gaps == [("repeat", 2)] and cost == 2 == edit_distance(a, b)


def test_alignment_cost_is_an_upper_bound() -> None:
    rng = random.Random(4)
    for _ in range(60):
        a = rand_dna(rng, rng.randrange(10, 50))
        b = list(a)
        for _ in range(rng.randrange(0, 4)):
            p = rng.randrange(len(b))
            op = rng.randrange(3)
            if op == 0:
                b[p] = rng.choice("ACGT")
            elif op == 1:
                del b[p]
            else:
                b.insert(p, rng.choice("ACGT"))
        b = "".join(b)
        _, _, cost = mummer(a, b, 4)
        assert cost >= edit_distance(a, b)


def test_snps_only() -> None:
    rng = random.Random(5)
    for _ in range(30):
        a = rand_dna(rng, 200)
        b = list(a)
        for p in range(20, 180, 25):  # 7 SNPs, 24 bases apart
            b[p] = {"A": "C", "C": "G", "G": "T", "T": "A"}[b[p]]
        b = "".join(b)
        chain, gaps, cost = mummer(a, b, 12)
        assert gaps == [("SNP", 1)] * 7 and cost == 7 and len(chain) == 8
