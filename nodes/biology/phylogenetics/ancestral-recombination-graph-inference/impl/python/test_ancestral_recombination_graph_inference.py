# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ancestral-recombination-graph-inference/. The authors are listed in prov/EM1WEQ.jsonl.

import random
from itertools import combinations

from ancestral_recombination_graph_inference import (
    haplotype_bound,
    hudson_kaplan,
    hudson_kaplan_original,
    incompatible,
    parse,
    r_min,
    stab,
)

# Figure 1 of Gusfield, Eddhu and Langley (2004), rows a to g, root 00000
GEL = parse(["00010", "10010", "00100", "10100", "01100", "01101", "00101"])


def test_gel_example():
    pairs = [(i, j) for i, j in combinations(range(5), 2) if incompatible(GEL, i, j)]
    assert pairs == [(0, 2), (0, 3), (1, 4)]
    assert hudson_kaplan(GEL) == 1     # the intervals (0, 2) and (0, 3) overlap (1, 4)
    assert haplotype_bound(GEL) == 2   # sites 0, 1, 2, 3, 4 hold 8 haplotypes with the root: 8 - 5 - 1
    assert r_min(GEL) == 2


def test_stab_against_brute_force():
    rng = random.Random(1)
    for _ in range(300):
        m = rng.randint(2, 8)
        iv = [tuple(sorted(rng.sample(range(m), 2))) for _ in range(rng.randint(0, 6))]
        best = None
        for k in range(m):
            for gaps in combinations(range(1, m), k):
                if all(any(i < g <= j for g in gaps) for i, j in iv):
                    best = k
                    break
            if best is not None:
                break
        assert stab(iv) == best


def random_matrix(rng, n, m):
    return [[rng.randint(0, 1) for _ in range(m)] for _ in range(n)]


def test_bounds_against_exact_minimum():
    rng = random.Random(3)
    seen = set()
    for _ in range(250):
        n, m = rng.randint(2, 4), rng.randint(2, 4)
        M = random_matrix(rng, n, m)
        rm, rh, exact = hudson_kaplan(M), haplotype_bound(M), r_min(M)
        assert hudson_kaplan_original(M) == rm
        assert rm <= rh <= exact
        # the unrooted test finds fewer incompatible pairs, so its bound is weaker
        assert hudson_kaplan(M, rooted=False) <= rm
        seen.add((rm, rh, exact))
    assert any(rh < exact for _, rh, exact in seen)   # the bounds are not always tight
    # R_M < R_h happens on the GEL matrix


def test_zero_exactly_for_perfect_phylogenies():
    # R_min = 0 if and only if no pair of sites shows 01, 10 and 11 (the root gives 00)
    rng = random.Random(4)
    for _ in range(300):
        M = random_matrix(rng, rng.randint(2, 6), rng.randint(2, 5))
        m = len(M[0])
        tree = not any(incompatible(M, i, j) for i, j in combinations(range(m), 2))
        try:
            zero = r_min(M, limit=0) == 0
        except ValueError:   # no history without recombination
            zero = False
        assert zero == tree


def test_small_cases_by_hand():
    # three gametes 01, 10, 11 with the root 00: one recombination
    assert r_min(parse(["01", "10", "11"])) == 1
    # the same rows without 11 fit one tree
    assert r_min(parse(["01", "10"])) == 0
    # two separate conflicts need two breakpoints
    M = parse(["0100", "1000", "1100", "0001", "0010", "0011"])
    assert hudson_kaplan(M) == 2 and r_min(M) == 2
    # both lower bounds give 1, but two recombinations are needed
    M = parse(["1101", "1100", "0011", "0111"])
    assert hudson_kaplan(M) == haplotype_bound(M) == 1 and r_min(M) == 2
    # adding a copy of a row or a column of zeros changes nothing
    M2 = parse(["01100", "10100", "11000", "11000"])
    M3 = parse(["011", "101", "110"])
    assert r_min(M2) == r_min(M3)
