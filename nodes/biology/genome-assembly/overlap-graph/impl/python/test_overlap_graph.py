# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/overlap-graph/. The authors are listed in prov/QXKQRZ.jsonl.

import random

import pytest

from overlap_graph import OverlapGraph, suffix_prefix_overlap


def test_page_example() -> None:
    reads = ["TACGGAT", "CGGATCA", "GATCATG", "TCATGCA", "ATGCATT"]
    g = OverlapGraph(reads, 2)
    g.check_invariant()
    assert g.out_arcs(0) == [(1, 5), (2, 3), (4, 2)]
    assert g.out_arcs(1) == [(2, 5), (3, 3)]
    assert g.out_arcs(2) == [(3, 5), (4, 3)]
    assert g.out_arcs(3) == [(4, 5)]
    assert g.out_arcs(4) == []
    assert g.in_arcs(4) == [(3, 5), (2, 3), (0, 2)]
    assert g.num_arcs() == 8
    assert g.spell([0, 1, 2, 3, 4]) == "TACGGATCATGCATT"
    assert g.spell([0, 2, 4]) == "TACGGATCATGCATT"
    assert g.spell([0, 4]) == "TACGGATGCATT"
    assert OverlapGraph(reads, 3).num_arcs() == 7
    assert OverlapGraph(reads, 4).num_arcs() == 4
    assert OverlapGraph(reads, 1).num_arcs() == 12


def test_edges() -> None:
    assert OverlapGraph([], 1).num_arcs() == 0
    g = OverlapGraph(["ACGT"], 1)
    assert g.num_arcs() == 0
    assert g.spell([0]) == "ACGT"
    assert g.spell([]) == ""
    g = OverlapGraph(["AAA", "AAA"], 1)
    g.check_invariant()
    assert g.weight(0, 1) == 2 and g.weight(1, 0) == 2
    g = OverlapGraph(["ACG", "CGT"], 3)
    assert g.num_arcs() == 0
    with pytest.raises(ValueError):
        OverlapGraph(["A"], 0)
    with pytest.raises(ValueError):
        OverlapGraph(["ACG", "TTT"], 1).spell([0, 1])


def test_contained_read_has_no_full_length_arc() -> None:
    g = OverlapGraph(["ACGTT", "CGT", "GTTA"], 1)
    g.check_invariant()
    assert g.weight(1, 0) == 0
    assert g.weight(1, 2) == 2
    assert g.weight(0, 2) == 3


def test_random_against_naive() -> None:
    rng = random.Random(12345)
    for _ in range(600):
        m = rng.randrange(0, 7)
        alphabet = rng.choice(["AC", "ACGT"])
        reads = ["".join(rng.choice(alphabet) for _ in range(rng.randrange(1, 9))) for _ in range(m)]
        ell = rng.randrange(1, 5)
        g = OverlapGraph(reads, ell)
        g.check_invariant()
        for i in range(m):
            for j in range(m):
                if i != j:
                    w = suffix_prefix_overlap(reads[i], reads[j])
                    assert g.weight(i, j) == (w if w >= ell else 0)


def test_spell_contains_every_read_on_path() -> None:
    rng = random.Random(99)
    for _ in range(200):
        x = "".join(rng.choice("ACGT") for _ in range(30))
        starts = sorted(rng.sample(range(0, 22), 6))
        reads = [x[s:s + 8] for s in starts]
        g = OverlapGraph(reads, 1)
        path = [0]
        for q in range(1, len(reads)):
            if g.weight(path[-1], q) > 0:
                path.append(q)
        text = g.spell(path)
        for q in path:
            assert reads[q] in text
