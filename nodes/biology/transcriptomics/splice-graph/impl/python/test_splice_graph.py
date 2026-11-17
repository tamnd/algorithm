# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/splice-graph/. The authors are listed in prov/7RCBRT.jsonl.

import random
from itertools import combinations

from splice_graph import SpliceGraph


def project(transcript, start, length):
    """The genome blocks of the read transcript[start:start + length], where transcript is a list of exons."""
    blocks, offset = [], 0
    for s, e in transcript:
        lo, hi = max(start, offset), min(start + length, offset + e - s)
        if lo < hi:
            gs, ge = s + lo - offset, s + hi - offset
            if blocks and blocks[-1][1] == gs:
                blocks[-1] = (blocks[-1][0], ge)
            else:
                blocks.append((gs, ge))
        offset += e - s
    return blocks


def random_locus(rng: random.Random):
    """Random exons on a short genome, transcripts as chains of them, and reads from the transcripts."""
    points = sorted(rng.sample(range(1, 80), 2 * rng.randint(2, 4)))
    exons = [(points[i], points[i + 1]) for i in range(0, len(points), 2)]
    transcripts = []
    for _ in range(rng.randint(1, 4)):
        chosen = sorted(rng.sample(exons, rng.randint(1, len(exons))))
        # An alternative donor or acceptor: move one exon end inside the exon.
        if rng.random() < 0.5:
            j = rng.randrange(len(chosen))
            s, e = chosen[j]
            if e - s >= 3:
                chosen[j] = (s, rng.randint(s + 1, e - 1)) if rng.random() < 0.5 else (rng.randint(s + 1, e - 1), e)
        transcripts.append(chosen)
    alignments = []
    for t in transcripts:
        tlen = sum(e - s for s, e in t)
        alignments.append(project(t, 0, tlen))
        for _ in range(rng.randint(0, 6)):
            length = rng.randint(1, tlen)
            alignments.append(project(t, rng.randint(0, tlen - length), length))
    return alignments


def nodes_by_positions(alignments):
    """The nodes from the definition: runs of covered bases with no donor or acceptor inside."""
    covered, cuts = set(), set()
    for a in alignments:
        for s, e in a:
            covered.update(range(s, e))
        for (_, d), (acc, _) in zip(a, a[1:]):
            cuts.update((d, acc))
    nodes, start = [], None
    for p in range(min(covered), max(covered) + 2):
        inside = p in covered
        if start is not None and (not inside or p in cuts):
            nodes.append((start, p))
            start = None
        if inside and start is None:
            start = p
    return nodes


def test_worked_example():
    # E1 [0, 100), E2 [200, 300) with a second acceptor at 250, E3 [400, 500).
    t1 = [(0, 100), (200, 300), (400, 500)]
    t2 = [(0, 100), (250, 300), (400, 500)]
    t3 = [(0, 100), (400, 500)]
    g = SpliceGraph([t1, t2, t3])
    assert g.nodes == [(0, 100), (200, 250), (250, 300), (400, 500)]
    assert sorted(g.edges) == [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3)]
    assert g.paths() == [[0, 1, 2, 3], [0, 2, 3], [0, 3]]
    assert g.count_paths() == 3
    assert [g.spell(p) for p in g.paths()] == [t1, t2, t3]
    assert g.path_of([(80, 100), (250, 270)]) == [0, 2]


def test_nodes_match_the_definition():
    rng = random.Random(1)
    for _ in range(500):
        alignments = random_locus(rng)
        assert SpliceGraph(alignments).nodes == nodes_by_positions(alignments)


def test_edges_are_the_steps_of_the_alignment_paths():
    rng = random.Random(2)
    for _ in range(500):
        alignments = random_locus(rng)
        g = SpliceGraph(alignments)
        steps = set()
        for a in alignments:
            p = g.path_of(a)
            assert p == sorted(set(p))
            steps.update(zip(p, p[1:]))
        assert g.edges == steps
        for u, v in g.edges:
            assert g.nodes[u][1] <= g.nodes[v][0]


def test_every_transcript_is_a_path():
    rng = random.Random(3)
    for _ in range(300):
        alignments = random_locus(rng)
        g = SpliceGraph(alignments)
        for a in alignments:
            p = g.path_of(a)
            assert all((u, v) in g.edges for u, v in zip(p, p[1:]))
            # The path spells the same introns, and each block lies inside its exon.
            exons = g.spell(p)
            assert len(exons) == len(a)
            for (s, e), (xs, xe) in zip(a, exons):
                assert xs <= s < e <= xe
            for i in range(len(a) - 1):
                assert exons[i][1] == a[i][1] and exons[i + 1][0] == a[i + 1][0]


def test_paths_against_brute_force():
    rng = random.Random(4)
    checked = 0
    while checked < 300:
        g = SpliceGraph(random_locus(rng))
        n = len(g.nodes)
        if n > 12:
            continue
        checked += 1
        src, snk = set(g.sources()), set(g.sinks())
        brute = []
        for r in range(1, n + 1):
            for sub in combinations(range(n), r):
                if sub[0] in src and sub[-1] in snk and all((u, v) in g.edges for u, v in zip(sub, sub[1:])):
                    brute.append(list(sub))
        assert g.paths() == sorted(brute)
        assert g.count_paths() == len(brute)
