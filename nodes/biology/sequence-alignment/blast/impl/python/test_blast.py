# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blast/. The authors are listed in prov/0132T2.jsonl.

import itertools
import random

from blast import (
    INF,
    best_ungapped,
    blast,
    blast_pair,
    extend,
    neighborhood,
    segment_score,
    smith_waterman_linear,
)

AA = "ARNDCQEGHILKMFPSTWYV"
# Rows P, Q and G of BLOSUM62 (Henikoff and Henikoff 1992), copied by hand
# from the NCBI matrix file, columns in the order of AA.
B62_ROWS = {
    "P": [-1, -2, -2, -1, -3, -1, -1, -2, -2, -3, -3, -1, -2, -4, 7, -1, -1, -4, -3, -2],
    "Q": [-1, 1, 0, 0, -3, 5, 2, -2, 0, -3, -2, 1, 0, -3, -1, 0, -1, -2, -1, -2],
    "G": [0, -2, 0, -1, -3, -2, -2, 6, -2, -4, -4, -2, -3, -3, -2, 0, -2, -2, -3, -3],
}


def b62(a: str, b: str) -> int:
    return B62_ROWS[a][AA.index(b)]


def dna(a: str, b: str) -> int:
    return 1 if a == b else -2


def rand_seq(rng: random.Random, n: int, alphabet: str = "ACGT") -> str:
    return "".join(rng.choice(alphabet) for _ in range(n))


def test_neighborhood_of_pqg() -> None:
    table = neighborhood("PQG", 3, 13, AA, b62)
    assert sorted(table, key=lambda u: (-sum(b62(a, b) for a, b in zip("PQG", u)), u)) == [
        "PQG", "PEG", "PKG", "PRG", "PDG", "PHG", "PMG", "PNG", "PSG",
    ]
    assert len(neighborhood("PQG", 3, 12, AA, b62)) == 16
    assert len(neighborhood("PQG", 3, 11, AA, b62)) == 21


def test_neighborhood_against_brute_force() -> None:
    rng = random.Random(1)
    alphabet = "ACGT"

    def sc(a: str, b: str) -> int:
        return 2 if a == b else (-1 if {a, b} in ({"A", "G"}, {"C", "T"}) else -3)

    for _ in range(40):
        q = rand_seq(rng, rng.randint(3, 9))
        w, t = rng.randint(1, 3), rng.randint(-3, 6)
        brute: dict[str, list[int]] = {}
        for i in range(len(q) - w + 1):
            for word in map("".join, itertools.product(alphabet, repeat=w)):
                if sum(sc(a, b) for a, b in zip(q[i : i + w], word)) >= t:
                    brute.setdefault(word, []).append(i)
        got = neighborhood(q, w, t, alphabet, sc)
        assert {k: sorted(v) for k, v in got.items()} == brute


def test_extension_with_infinite_x_finds_best_segment_through_the_word() -> None:
    rng = random.Random(2)
    for _ in range(300):
        q, y = rand_seq(rng, rng.randint(4, 14)), rand_seq(rng, rng.randint(4, 14))
        w = rng.randint(1, 3)
        i, j = rng.randint(0, len(q) - w), rng.randint(0, len(y) - w)
        a, b, length, s = extend(q, y, i, j, w, INF, dna)
        assert s == segment_score(q, y, a, b, length, dna)
        best = max(
            segment_score(q, y, i - l, j - l, l + w + r, dna)
            for l in range(min(i, j) + 1)
            for r in range(min(len(q) - i - w, len(y) - j - w) + 1)
        )
        assert s == best


def test_completeness_with_infinite_x() -> None:
    # Each segment pair with score >= S that contains a word pair with
    # score >= T is matched by a reported HSP on its diagonal that contains
    # the word pair and scores at least as much.
    rng = random.Random(3)
    w, t, cutoff = 2, 2, 4
    for _ in range(60):
        q, y = rand_seq(rng, rng.randint(6, 14)), rand_seq(rng, rng.randint(6, 14))
        table = neighborhood(q, w, t, "ACGT", dna)
        hsps = blast_pair(q, y, table, w, INF, cutoff, dna, skip_covered=False)
        for i in range(len(q)):
            for j in range(len(y)):
                for length in range(w, min(len(q) - i, len(y) - j) + 1):
                    s = segment_score(q, y, i, j, length, dna)
                    if s < cutoff:
                        continue
                    for k in range(length - w + 1):
                        if segment_score(q, y, i + k, j + k, w, dna) >= t:
                            ok = any(
                                b - a == j - i and a <= i + k and i + k + w <= a + ln and sc >= s
                                for a, b, ln, sc in hsps
                            )
                            assert ok


def test_best_hsp_is_the_msp_when_every_word_is_a_hit() -> None:
    rng = random.Random(4)
    for _ in range(100):
        q, y = rand_seq(rng, rng.randint(1, 12)), rand_seq(rng, rng.randint(1, 12))
        table = neighborhood(q, 1, -10, "ACGT", dna)
        hsps = blast_pair(q, y, table, 1, INF, -10, dna, skip_covered=False)
        assert max([0] + [h[3] for h in hsps]) == best_ungapped(q, y, dna)


def test_reported_scores_are_true_scores() -> None:
    rng = random.Random(5)
    for _ in range(100):
        q, y = rand_seq(rng, 40), rand_seq(rng, 60)
        y = y[:20] + q[5:25] + y[20:]
        for x in (2, 5, INF):
            for two_hit in (False, True):
                for _, (a, b, ln, s) in blast(q, [y], 4, 4, x, 8, "ACGT", dna, two_hit, 12):
                    assert s == segment_score(q, y, a, b, ln, dna) and s >= 8


def test_planted_match_is_found() -> None:
    rng = random.Random(6)
    q = rand_seq(rng, 50)
    y = rand_seq(rng, 30) + q[10:40] + rand_seq(rng, 30)
    res = blast(q, [rand_seq(rng, 80), y], 11, 11, 20, 25, "ACGT", dna)
    assert any(idx == 1 and s >= 30 for idx, (_, _, _, s) in res)


def test_blast_misses_what_smith_waterman_finds() -> None:
    # The two sequences agree everywhere except at every eighth position, so
    # no 11-letter word is shared and BLASTN-style seeding finds nothing.
    rng = random.Random(7)
    q = rand_seq(rng, 64)
    y = "".join(("C" if c != "C" else "G") if k % 8 == 7 else c for k, c in enumerate(q))
    assert blast(q, [y], 11, 11, 20, 1, "ACGT", dna) == []
    assert best_ungapped(q, y, dna) == 56 - 2 * 8 + 2  # 7 x 8 matches, 7 inner mismatches
    assert smith_waterman_linear(q, y, dna, 2) >= 42


def test_two_hit_needs_two_hits_on_a_diagonal() -> None:
    q = "ACGTACCTGA"
    y = "TTACGTACCTGATT"
    table = neighborhood(q, 3, 3, "ACGT", dna)
    one = blast_pair(q, y, table, 3, INF, 5, dna)
    two = blast_pair(q, y, table, 3, INF, 5, dna, two_hit=True, a=40)
    assert one == two == [(0, 2, 10, 10)]
    # a single isolated word pair triggers the one-hit method only
    q2, y2 = "AAAACGTTTT", "GGGGCGTCCC"
    t2 = neighborhood(q2, 3, 3, "ACGT", dna)
    assert blast_pair(q2, y2, t2, 3, INF, 3, dna) != []
    assert blast_pair(q2, y2, t2, 3, INF, 3, dna, two_hit=True) == []
