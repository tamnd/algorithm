# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-bruijn-assembly/. The authors are listed in prov/0WN504.jsonl.

import random

import pytest

from de_bruijn_assembly import count_kmers, de_bruijn_assembly, spell, unitig_paths


def random_genome(rng: random.Random, n: int, w: int) -> str:
    """Return a random DNA string of length n with no repeated w-mer."""
    while True:
        s = "".join(rng.choice("ACGT") for _ in range(n))
        ws = [s[i : i + w] for i in range(n - w + 1)]
        if len(set(ws)) == len(ws):
            return s


def sample_reads(rng: random.Random, s: str, length: int, count: int, k: int) -> list[str]:
    """Return count random reads of s, plus reads that cover each k-mer of s that was missed."""
    starts = [rng.randrange(len(s) - length + 1) for _ in range(count)]
    reads = [s[p : p + length] for p in starts]
    seen = set(count_kmers(reads, k))
    for i in range(len(s) - k + 1):
        if s[i : i + k] not in seen:
            p = min(i, len(s) - length)
            reads.append(s[p : p + length])
            seen |= set(count_kmers([reads[-1]], k))
    return reads


def reference_unitigs(kmers: list[str]) -> set[frozenset[str]]:
    """Group the edges by the rule: e and f are joined when head(e) = tail(f) has in- and out-degree 1."""
    edges = sorted(set(kmers))
    indeg: dict[str, int] = {}
    outdeg: dict[str, int] = {}
    for x in edges:
        outdeg[x[:-1]] = outdeg.get(x[:-1], 0) + 1
        indeg[x[1:]] = indeg.get(x[1:], 0) + 1
    parent = {x: x for x in edges}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in edges:
        for f in edges:
            v = e[1:]
            if v == f[:-1] and indeg.get(v, 0) == 1 and outdeg.get(v, 0) == 1:
                parent[find(e)] = find(f)
    groups: dict[str, set[str]] = {}
    for x in edges:
        groups.setdefault(find(x), set()).add(x)
    return {frozenset(g) for g in groups.values()}


def test_example() -> None:
    reads = ["GATGCATA", "GCATACGC", "TACGCCTT", "CGCCTTTA"]
    assert count_kmers(reads, 4)["CATA"] == 2
    assert len(count_kmers(reads, 4)) == 13
    assert de_bruijn_assembly(reads, 4) == ["GATGCATACGCCTTTA"]


def test_triple_repeat_example() -> None:
    s = "CCGTAAGTATTGTAG"
    reads = [s[i : i + 4] for i in range(len(s) - 3)]
    assert de_bruijn_assembly(reads, 4) == ["CCGTA", "GTAAGTA", "GTAG", "GTATTGTA"]


def test_edges() -> None:
    assert de_bruijn_assembly([], 3) == []
    assert de_bruijn_assembly(["AC"], 3) == []
    assert de_bruijn_assembly(["ACG"], 3) == ["ACG"]
    assert de_bruijn_assembly(["ACGT", "ACGT"], 2) == ["ACGT"]
    assert de_bruijn_assembly(["ACAC"], 3) == ["ACAC"]
    assert de_bruijn_assembly(["ACGTT"], 3, simplify=lambda xs: [x for x in xs if x != "GTT"]) == ["ACGT"]
    with pytest.raises(ValueError):
        de_bruijn_assembly(["ACGT"], 1)


def test_cycle() -> None:
    # The genome AACGT read as a circle: every vertex is 1-in-1-out.
    paths = unitig_paths(["AAC", "ACG", "CGT", "GTA", "TAA"])
    assert len(paths) == 1
    assert sorted(paths[0]) == ["AAC", "ACG", "CGT", "GTA", "TAA"]
    assert spell(paths[0]) == "AACGTAA"


def test_genome_without_repeats_assembles_back() -> None:
    rng = random.Random(11)
    for _ in range(60):
        k = rng.randint(9, 14)
        s = random_genome(rng, rng.randint(30, 150), k - 1)
        reads = sample_reads(rng, s, rng.randint(k, k + 20), rng.randint(5, 40), k)
        assert de_bruijn_assembly(reads, k) == [s]


def test_unitigs_match_reference() -> None:
    rng = random.Random(5)
    for _ in range(300):
        k = rng.randint(2, 5)
        s = "".join(rng.choice("AC") for _ in range(rng.randint(k, 25)))
        kmers = [s[i : i + k] for i in range(len(s) - k + 1)]
        paths = unitig_paths(kmers)
        flat = [x for p in paths for x in p]
        assert sorted(flat) == sorted(set(kmers))
        for p in paths:
            assert all(a[1:] == b[:-1] for a, b in zip(p, p[1:]))
        assert {frozenset(p) for p in paths} == reference_unitigs(kmers)


def test_unitigs_are_substrings_when_ends_are_unique() -> None:
    rng = random.Random(3)
    tested = 0
    for _ in range(4000):
        k = rng.randint(2, 6)
        s = "".join(rng.choice("AB") for _ in range(rng.randint(k, 16)))
        first, last = s[: k - 1], s[len(s) - k + 1 :]
        windows = [s[i : i + k - 1] for i in range(len(s) - k + 2)]
        if windows.count(first) != 1 or windows.count(last) != 1:
            continue
        tested += 1
        kmers = [s[i : i + k] for i in range(len(s) - k + 1)]
        for contig in de_bruijn_assembly(kmers, k):
            assert contig in s
    assert tested > 500


def test_count_filter_removes_error_kmers() -> None:
    rng = random.Random(8)
    for _ in range(30):
        k = 9
        s = random_genome(rng, 80, k - 1)
        reads = [s[i : i + 30] for i in range(0, 51, 5)] * 3
        r = list(reads[rng.randrange(len(reads))])
        j = rng.randrange(len(r))
        r[j] = "ACGT"[("ACGT".index(r[j]) + 1) % 4]
        reads.append("".join(r))
        assert de_bruijn_assembly(reads, k, min_count=2) == [s]
