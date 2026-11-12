# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/string-graph/. The authors are listed in prov/6QAKRR.jsonl.

import random
from typing import List, Set, Tuple

import pytest

from string_graph import StringGraph, all_overlaps


def reachable_offsets(g: StringGraph, u: int, limit: int) -> Set[Tuple[int, int]]:
    # States (vertex, total offset) reachable from u in the string graph, offsets up to limit.
    seen = {(u, 0)}
    stack = [(u, 0)]
    while stack:
        v, s = stack.pop()
        for d, x in g.edges[v]:
            if s + d <= limit and (x, s + d) not in seen:
                seen.add((x, s + d))
                stack.append((x, s + d))
    return seen


def test_all_overlaps() -> None:
    assert all_overlaps("ABABA", "ABAB") == [3, 1]
    assert all_overlaps("ACGT", "GTAA") == [2]
    assert all_overlaps("", "A") == []
    assert all_overlaps("AAAA", "AAAA") == [3, 2, 1]


def test_page_example() -> None:
    reads = ["TACGGAT", "CGGATCA", "GGATC", "GATCATG", "TCATGCA", "ATGCATT"]
    g = StringGraph(reads, 2)
    g.check_invariant()
    assert g.contained == ["GGATC"]
    assert g.reads == ["TACGGAT", "CGGATCA", "GATCATG", "TCATGCA", "ATGCATT"]
    assert g.num_overlap_edges() == 8
    assert g.num_edges() == 5
    assert g.out_edges(0) == [(2, 1), (5, 4)]
    assert g.out_edges(1) == [(2, 2)]
    assert g.out_edges(2) == [(2, 3)]
    assert g.out_edges(3) == [(2, 4)]
    assert g.out_edges(4) == []
    assert g.spell(0, [(2, 1), (2, 2), (2, 3), (2, 4)]) == "TACGGATCATGCATT"
    assert g.spell(0, [(5, 4)]) == "TACGGATGCATT"
    assert StringGraph(reads, 3).num_edges() == 4


def test_edges() -> None:
    g = StringGraph([], 1)
    assert g.num_vertices() == 0 and g.num_edges() == 0
    g = StringGraph(["ACGT", "ACGT", "CG"], 1)
    assert g.reads == ["ACGT"] and g.contained == ["CG"]
    assert g.spell(0, []) == "ACGT"
    with pytest.raises(ValueError):
        StringGraph(["A"], 0)
    with pytest.raises(ValueError):
        StringGraph(["ACG", "TTT"], 1).spell(0, [(1, 1)])


def test_periodic_reads_keep_multi_edges() -> None:
    g = StringGraph(["ABABAB", "BABABA"], 1)
    g.check_invariant()
    assert g.overlap_edges[0] == [(1, 1), (3, 1), (5, 1)]
    # Without a third read no edge is transitive, so all three offsets stay.
    assert g.edges[0] == [(1, 1), (3, 1), (5, 1)]
    g = StringGraph(["ABABAB", "BABABA", "ABABAC"], 1)
    g.check_invariant()
    assert g.overlap_edges[0] == [(1, 1), (2, 2), (3, 1), (4, 2), (5, 1)]
    # Both edges 0 -> 2 go through read 1 with the same total offset, so both are transitive.
    assert g.edges[0] == [(1, 1), (3, 1), (5, 1)]
    assert g.edges[1] == [(1, 0), (1, 2), (3, 0), (5, 0)]


def test_two_edges_to_one_read_disable_the_skip() -> None:
    # From read 1, edge (1, 2, 5) has the witness (3, 3), and (1, 3, 3) is eliminated only
    # through read 2 itself. Skipping eliminated edges would keep (1, 2, 5).
    g = StringGraph(["ABA", "BBBBAB", "BBABB", "BABBA"], 1)
    g.check_invariant()
    assert g.overlap_edges[1] == [(2, 2), (3, 3), (4, 0), (5, 2), (5, 3)]
    assert g.edges[1] == [(2, 2), (4, 0)]


def test_random_against_definition_and_paths() -> None:
    rng = random.Random(4242)
    for _ in range(2500):
        m = rng.randrange(1, 8)
        alphabet = rng.choice(["AB", "ACGT"])
        reads = ["".join(rng.choice(alphabet) for _ in range(rng.randrange(1, 9))) for _ in range(m)]
        ell = rng.randrange(1, 4)
        g = StringGraph(reads, ell)
        g.check_invariant()
        for u in range(g.num_vertices()):
            limit = max((d for d, _ in g.overlap_edges[u]), default=0)
            reach = reachable_offsets(g, u, limit)
            for d, x in g.overlap_edges[u]:
                assert (x, d) in reach


def test_repeat_free_genome_gives_one_path() -> None:
    rng = random.Random(77)
    done = 0
    while done < 150:
        x = "".join(rng.choice("ACGT") for _ in range(40))
        ell = 6
        if len({x[p:p + ell] for p in range(len(x) - ell + 1)}) < len(x) - ell + 1:
            continue
        reads: List[str] = []
        start = 0
        while True:
            length = rng.randrange(ell + 2, 13)
            end = min(start + length, len(x))
            reads.append(x[start:end])
            if end == len(x):
                break
            start = rng.randrange(start + 1, end - ell + 1)
        rng.shuffle(reads)
        g = StringGraph(reads, ell)
        heads = [v for v in range(g.num_vertices()) if all(v != w for u in range(g.num_vertices()) for _, w in g.edges[u])]
        assert len(heads) == 1
        v = heads[0]
        steps = []
        while g.edges[v]:
            assert len(g.edges[v]) == 1
            steps.append(g.edges[v][0])
            v = g.edges[v][0][1]
        assert len(steps) == g.num_vertices() - 1
        assert g.spell(heads[0], steps) == x
        done += 1
