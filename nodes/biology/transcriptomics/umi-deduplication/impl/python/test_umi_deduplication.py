# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/umi-deduplication/. The authors are listed in prov/5HMHYS.jsonl.

import random

import pytest

from bioseq import hamming, mutate, random_dna
from umi_deduplication import (
    count_molecules,
    deduplicate,
    directional_edges,
    group_cluster,
    group_directional,
    group_unique,
    neighbors_hash,
    neighbors_pairs,
)

PAGE = {"ACGT": 50, "ACGA": 20, "ACGC": 2, "TCGA": 18, "TCGT": 1, "GGGG": 5}


def random_bundle(rng, n_umis, length, alphabet="ACGT"):
    """Random UMIs that are close to each other, so that the graph has many edges."""
    base = "".join(rng.choice(alphabet) for _ in range(length))
    counts = {}
    while len(counts) < n_umis:
        u = list(base)
        for _ in range(rng.randint(0, 2)):
            u[rng.randrange(length)] = rng.choice(alphabet)
        counts["".join(u)] = rng.choice([1, 1, 2, 3, 5, 8, 20, 60])
    return counts


def brute_force_directional(counts):
    """Reachability by a transitive closure of the edge matrix, then the greedy assignment."""
    umis = sorted(counts, key=lambda u: (-counts[u], u))
    n = len(umis)
    reach = [[i == j or (hamming(umis[i], umis[j]) == 1 and counts[umis[i]] >= 2 * counts[umis[j]] - 1)
              for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    taken, groups = set(), []
    for i in range(n):
        if i in taken:
            continue
        group = [j for j in range(n) if reach[i][j] and j not in taken]
        taken.update(group)
        groups.append([umis[j] for j in group])
    return groups


def components_brute(counts):
    """Connected components of the undirected distance-1 graph, by repeated merging of sets."""
    sets = [{u} for u in counts]
    merged = True
    while merged:
        merged = False
        for a in range(len(sets)):
            for b in range(a + 1, len(sets)):
                if any(hamming(x, y) == 1 for x in sets[a] for y in sets[b]):
                    sets[a] |= sets.pop(b)
                    merged = True
                    break
            if merged:
                break
    return sorted(sorted(s) for s in sets)


def test_page_example():
    assert directional_edges(PAGE) == {
        "ACGT": ["ACGA", "ACGC", "TCGT"], "ACGA": ["ACGC"], "TCGA": ["TCGT"],
        "GGGG": [], "ACGC": [], "TCGT": []}
    assert group_directional(PAGE) == [["ACGT", "ACGA", "ACGC", "TCGT"], ["TCGA"], ["GGGG"]]
    assert len(group_cluster(PAGE)) == 2
    assert len(group_unique(PAGE)) == 6


def test_against_brute_force():
    rng = random.Random(11)
    for _ in range(300):
        counts = random_bundle(rng, rng.randint(1, 12), rng.randint(3, 6))
        assert group_directional(counts) == brute_force_directional(counts)


def test_neighbor_methods_agree():
    rng = random.Random(12)
    for _ in range(200):
        counts = random_bundle(rng, rng.randint(1, 15), rng.randint(3, 7), alphabet="ACGTN")
        assert neighbors_hash(counts) == neighbors_pairs(counts)
        assert group_directional(counts, neighbors_hash) == group_directional(counts)


def test_partition_and_representative():
    rng = random.Random(13)
    for _ in range(300):
        counts = random_bundle(rng, rng.randint(1, 15), rng.randint(3, 6))
        groups = group_directional(counts)
        flat = [u for g in groups for u in g]
        assert sorted(flat) == sorted(counts)
        for g in groups:
            assert counts[g[0]] == max(counts[u] for u in g)


def test_counts_never_increase_along_an_edge():
    rng = random.Random(14)
    for _ in range(300):
        counts = random_bundle(rng, rng.randint(1, 15), rng.randint(3, 6))
        for u, out in directional_edges(counts).items():
            for v in out:
                assert hamming(u, v) == 1
                assert counts[u] >= counts[v]
                if counts[u] == counts[v]:
                    assert counts[u] == 1


def test_cluster_is_connected_components():
    rng = random.Random(15)
    for _ in range(150):
        counts = random_bundle(rng, rng.randint(1, 10), rng.randint(3, 6))
        assert sorted(sorted(g) for g in group_cluster(counts)) == components_brute(counts)


def test_bounds_between_cluster_and_unique():
    rng = random.Random(16)
    for _ in range(300):
        counts = random_bundle(rng, rng.randint(1, 15), rng.randint(3, 6))
        c, d, u = len(group_cluster(counts)), len(group_directional(counts)), len(group_unique(counts))
        assert c <= d <= u


def test_every_directional_group_is_inside_one_component():
    rng = random.Random(17)
    for _ in range(200):
        counts = random_bundle(rng, rng.randint(1, 15), rng.randint(3, 6))
        comp_of = {u: i for i, g in enumerate(group_cluster(counts)) for u in g}
        for g in group_directional(counts):
            assert len({comp_of[u] for u in g}) == 1


def test_far_apart_umis_are_all_kept():
    counts = {"AAAAAA": 9, "CCCCCC": 9, "GGGGGG": 1, "TTTTTT": 30}
    assert len(group_directional(counts)) == 4
    assert len(group_cluster(counts)) == 4


def test_two_singletons_join_in_both_directions():
    counts = {"AAAA": 1, "AAAC": 1}
    assert directional_edges(counts) == {"AAAA": ["AAAC"], "AAAC": ["AAAA"]}
    assert group_directional(counts) == [["AAAA", "AAAC"]]
    counts = {"AAAA": 2, "AAAC": 2}
    assert len(group_directional(counts)) == 2


def test_bundles_are_separate_and_dedup_keeps_one_read_per_molecule():
    reads = [("c1", "g1", "ACGT")] * 5 + [("c1", "g1", "ACGA")] * 2 + [("c1", "g2", "ACGA")] * 3
    reads += [("c2", "g1", "ACGA")] * 4 + [("c2", "g1", "TTTT")]
    assert count_molecules(reads) == {("c1", "g1"): 1, ("c1", "g2"): 1, ("c2", "g1"): 2}
    keep = deduplicate(reads)
    assert [reads[i] for i in keep] == [("c1", "g1", "ACGT"), ("c1", "g2", "ACGA"),
                                        ("c2", "g1", "ACGA"), ("c2", "g1", "TTTT")]


def test_errors():
    with pytest.raises(ValueError):
        count_molecules([("c", "g", "ACGT")], method="best")
    with pytest.raises(ValueError):
        group_directional({"ACG": 1, "ACGT": 1})


def test_simulated_pcr_and_sequencing_errors_measured():
    """A measurement, not a theorem: 40 molecules, 5 to 40 reads each, 1 percent base errors."""
    rng = random.Random(2017)
    err = {"unique": 0, "cluster": 0, "directional": 0}
    trials = 20
    for _ in range(trials):
        truth = set()
        while len(truth) < 40:
            truth.add(random_dna(rng, 10))
        reads = []
        for umi in sorted(truth):
            for _ in range(rng.randint(5, 40)):
                reads.append(("cell", "gene", mutate(rng, umi, 0.01)))
        for m in err:
            err[m] += abs(count_molecules(reads, m)[("cell", "gene")] - 40)
    # About 0.4 percent of the reads carry two errors, so every method that joins only
    # distance 1 keeps them as extra molecules; the measured excess is near 3 per bundle.
    assert err["directional"] <= 0.15 * 40 * trials
    assert err["directional"] * 10 < err["unique"]


def test_dense_umis_cluster_merges_distinct_molecules_measured():
    """A measurement: 150 molecules with 6-base UMIs, so true UMIs are often 1 apart."""
    rng = random.Random(2016)
    err = {"unique": 0, "cluster": 0, "directional": 0}
    for _ in range(5):
        truth = set()
        while len(truth) < 150:
            truth.add(random_dna(rng, 6))
        reads = []
        for umi in sorted(truth):
            for _ in range(rng.randint(5, 40)):
                reads.append(("cell", "gene", mutate(rng, umi, 0.01)))
        for m in err:
            err[m] += abs(count_molecules(reads, m)[("cell", "gene")] - 150)
    assert err["directional"] * 4 < err["cluster"]
    assert err["directional"] * 4 < err["unique"]
