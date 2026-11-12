# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kmer-index/. The authors are listed in prov/3PGQMC.jsonl.

import itertools
import random

from kmer_index import KmerIndex, kmer_codes, naive_lookup


def rand_dna(rng: random.Random, n: int, alphabet: str = "ACGT") -> str:
    return "".join(rng.choice(alphabet) for _ in range(n))


def test_page_example() -> None:
    t = "ACGTACGTTACG"
    idx = KmerIndex(t, 3)
    assert idx.lookup("ACG") == [0, 4, 9]
    assert idx.lookup("CGT") == [1, 5]
    assert idx.lookup("GTA") == [2]
    assert idx.lookup("GTT") == [6]
    assert idx.lookup("TAC") == [3, 8]
    assert idx.lookup("TTA") == [7]
    assert idx.lookup("AAA") == []
    assert idx.off[-1] == len(t) - 3 + 1
    # the slots in code order
    assert idx.pos == [0, 4, 9, 1, 5, 2, 6, 3, 8, 7]
    assert idx.seed_hits("TTACGA") == [(0, 7), (1, 3), (1, 8), (2, 0), (2, 4), (2, 9)]


def test_rolling_codes() -> None:
    assert kmer_codes("ACGT", 2) == [(0, 1), (1, 6), (2, 11)]
    assert kmer_codes("ACNGTA", 2) == [(0, 1), (3, 11), (4, 12)]
    assert kmer_codes("AC", 3) == []


def test_edges() -> None:
    idx = KmerIndex("", 2)
    assert idx.lookup("AC") == [] and idx.pos == []
    idx = KmerIndex("AAAA", 2)
    assert idx.lookup("AA") == [0, 1, 2]
    assert idx.lookup("A") == []
    assert idx.lookup("AN") == []
    idx = KmerIndex("ACGNNACG", 3)
    assert idx.lookup("ACG") == [0, 5]
    assert idx.count("CGN") == 0


def test_against_naive_scan() -> None:
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randrange(0, 60)
        t = rand_dna(rng, n, "ACGT" if rng.random() < 0.8 else "ACGTN")
        k = rng.randrange(1, 5)
        step = rng.choice([1, 1, 2, k])
        idx = KmerIndex(t, k, step)
        for tup in itertools.product("ACGT", repeat=k):
            x = "".join(tup)
            assert idx.lookup(x) == naive_lookup(t, x, step)
        # every indexed slot is used once
        assert sorted(idx.pos) == sorted(p for p, _ in kmer_codes(t, k, step))


def test_seed_hits_against_naive() -> None:
    rng = random.Random(11)
    for _ in range(100):
        t = rand_dna(rng, rng.randrange(0, 80))
        q = rand_dna(rng, rng.randrange(0, 20))
        k = rng.randrange(1, 4)
        idx = KmerIndex(t, k)
        want = sorted((i, j) for i in range(len(q) - k + 1) for j in range(len(t) - k + 1)
                      if q[i:i + k] == t[j:j + k])
        assert sorted(idx.seed_hits(q)) == want


def test_sampled_index_guarantee() -> None:
    # With step = k, any exact match of length >= 2k - 1 holds a whole indexed k-mer.
    rng = random.Random(5)
    for _ in range(200):
        k = rng.randrange(2, 6)
        t = rand_dna(rng, rng.randrange(2 * k, 80))
        idx = KmerIndex(t, k, step=k)
        length = rng.randrange(2 * k - 1, min(len(t), 3 * k) + 1)
        s = rng.randrange(0, len(t) - length + 1)
        q = t[s:s + length]
        assert any(p >= s and p + k <= s + length for _, p in idx.seed_hits(q))
