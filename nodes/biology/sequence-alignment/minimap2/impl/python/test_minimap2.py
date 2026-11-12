# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimap2/. The authors are listed in prov/5DG5E4.jsonl.

import random

from minimap2 import (
    Index,
    best_chain,
    brute_force_best,
    chain_scores,
    gap_cost,
    kmer_hashes,
    map_read,
    naive_sketch,
    revcomp,
    sketch,
)


def rand_dna(rng: random.Random, n: int) -> str:
    return "".join(rng.choice("ACGT") for _ in range(n))


def test_gap_cost() -> None:
    assert gap_cost(0, 15) == 0
    assert gap_cost(1, 15) == 0
    assert gap_cost(-4, 15) == 1
    assert gap_cost(100, 15) == 15 + 3


def test_sketch_against_naive() -> None:
    rng = random.Random(3)
    for _ in range(150):
        s = rand_dna(rng, rng.randrange(0, 120))
        if rng.random() < 0.2 and s:
            p = rng.randrange(len(s))
            s = s[:p] + "N" + s[p + 1:]
        k = rng.randrange(2, 8)
        w = rng.randrange(1, 8)
        assert sketch(s, w, k) == naive_sketch(s, w, k)


def test_both_strands_select_the_same_kmers() -> None:
    rng = random.Random(4)
    s = rand_dna(rng, 300)
    k, w = 9, 5
    fwd = {(h, pos - k + 1) for h, pos, _ in sketch(s, w, k)}
    rev = {(h, len(s) - 1 - pos) for h, pos, _ in sketch(revcomp(s), w, k)}
    assert fwd == rev


def test_shared_window_gives_shared_minimizer() -> None:
    rng = random.Random(5)
    k, w = 7, 6
    for _ in range(100):
        core = rand_dna(rng, w + k - 1)
        a = rand_dna(rng, 20) + core + rand_dna(rng, 20)
        b = rand_dna(rng, 15) + core + rand_dna(rng, 10)
        if len(kmer_hashes(core, k)) < w:
            continue  # a palindromic k-mer was skipped, so no full window
        ha = {h for h, _, _ in sketch(a, w, k)}
        hb = {h for h, _, _ in sketch(b, w, k)}
        assert ha & hb


def random_anchors(rng: random.Random, n: int) -> list:
    pts = set()
    while len(pts) < n:
        pts.add((rng.randrange(0, 60), rng.randrange(0, 60)))
    return sorted((x, y, rng.randrange(3, 8)) for x, y in pts)


def test_exact_chaining_against_brute_force() -> None:
    rng = random.Random(6)
    for _ in range(300):
        a = random_anchors(rng, rng.randrange(1, 9))
        gap = rng.choice([10, 25, 1000])
        f, _ = chain_scores(a, h=len(a) + 1, max_gap=gap)
        assert max(f) == brute_force_best(a, gap)


def test_heuristic_never_beats_exact() -> None:
    rng = random.Random(7)
    for _ in range(100):
        a = random_anchors(rng, rng.randrange(1, 40))
        exact, _ = chain_scores(a, h=len(a) + 1, max_gap=1000)
        heur, _ = chain_scores(a, h=2, max_gap=1000)
        assert all(x <= y for x, y in zip(heur, exact))


def test_backtrack_gives_a_valid_chain() -> None:
    rng = random.Random(8)
    for _ in range(100):
        a = random_anchors(rng, rng.randrange(1, 30))
        score, ch = best_chain(a, h=len(a) + 1, max_gap=1000)
        assert all(a[j][1] < a[i][1] for j, i in zip(ch, ch[1:]))
        f, _ = chain_scores(a, h=len(a) + 1, max_gap=1000)
        assert score == max(f)


def mutate(rng: random.Random, s: str, rate: float) -> str:
    out = []
    for ch in s:
        r = rng.random()
        if r < rate / 3:
            out.append(rng.choice([c for c in "ACGT" if c != ch]))
        elif r < 2 * rate / 3:
            continue  # deletion
        elif r < rate:
            out.append(ch)
            out.append(rng.choice("ACGT"))  # insertion
        else:
            out.append(ch)
    return "".join(out)


def test_simulated_reads_map_to_their_origin() -> None:
    rng = random.Random(9)
    ref = rand_dna(rng, 10000)
    index = Index(ref, w=10, k=15)
    good = 0
    trials = 20
    for _ in range(trials):
        start = rng.randrange(0, len(ref) - 1000)
        read = mutate(rng, ref[start:start + 1000], 0.05)
        strand = rng.randrange(2)
        if strand:
            read = revcomp(read)
        hit = map_read(index, read)
        if hit is not None and hit[0] == strand and abs(hit[1] - start) <= 50:
            good += 1
    assert good == trials
