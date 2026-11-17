# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/umi-deduplication/. The authors are listed in prov/5HMHYS.jsonl.
"""UMI deduplication with the directional network method of UMI-tools.

Smith, Heger and Sudbery (2017), Genome Research 27(3), 491-499.

A read is a tuple (cell, locus, umi). The locus is a mapping position and
strand for bulk data, or a gene for droplet single-cell data. Reads with the
same cell and locus form one bundle. In one bundle, n[u] is the number of
reads with UMI u. The directional graph has an edge u -> v when the UMIs u and
v differ at exactly one position and n[u] >= 2 n[v] - 1. The UMIs are visited
in order of decreasing count (ties by the UMI string). Each UMI that no earlier
search has reached starts a breadth-first search along the edges; the UMIs it
reaches and that are not yet taken form one group. Each group is one molecule,
and its first UMI (the one with the highest count) represents it.

Two simpler methods are here for comparison: "unique" (each distinct UMI is a
molecule) and "cluster" (each connected component of the undirected graph of
Hamming distance 1 is a molecule).
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, Hashable, Iterable, List, Sequence, Tuple

from bioseq import hamming

ALPHABET = "ACGTN"


def bundle_counts(reads: Iterable[Tuple[Hashable, Hashable, str]]) -> Dict[tuple, Dict[str, int]]:
    """The read count of each UMI in each bundle (cell, locus)."""
    out: Dict[tuple, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for cell, locus, umi in reads:
        out[(cell, locus)][umi] += 1  # @line L1
    return {k: dict(v) for k, v in out.items()}


def visit_order(counts: Dict[str, int]) -> List[str]:
    """The UMIs by decreasing count; equal counts in the order of the UMI string."""
    return sorted(counts, key=lambda u: (-counts[u], u))  # @line L3


def neighbors_pairs(counts: Dict[str, int]) -> Dict[str, List[str]]:
    """For each UMI, the UMIs at Hamming distance 1, by comparing all pairs (as UMI-tools)."""
    umis = visit_order(counts)
    lengths = {len(u) for u in umis}
    if len(lengths) > 1:
        raise ValueError("all UMIs of a bundle must have the same length")
    nb: Dict[str, List[str]] = {u: [] for u in umis}
    for i, u in enumerate(umis):
        for v in umis[i + 1:]:
            if hamming(u, v) == 1:
                nb[u].append(v)
                nb[v].append(u)
    return nb


def neighbors_hash(counts: Dict[str, int]) -> Dict[str, List[str]]:
    """The same neighbors, by looking up every one-substitution variant of each UMI."""
    umis = visit_order(counts)
    rank = {u: i for i, u in enumerate(umis)}
    nb: Dict[str, List[str]] = {}
    for u in umis:
        found = []
        for p in range(len(u)):
            for b in ALPHABET:
                if b != u[p]:
                    v = u[:p] + b + u[p + 1:]
                    if v in counts:
                        found.append(v)
        found.sort(key=rank.__getitem__)
        nb[u] = found
    return nb


def directional_edges(counts: Dict[str, int], neighbors=neighbors_pairs) -> Dict[str, List[str]]:
    """The edges u -> v of the directional graph, in visit order."""
    nb = neighbors(counts)
    adj: Dict[str, List[str]] = {}
    for u in visit_order(counts):
        out = []
        for v in nb[u]:  # @line L4
            if counts[u] >= 2 * counts[v] - 1:  # @line L5
                out.append(v)
        adj[u] = out
    return adj


def group_directional(counts: Dict[str, int], neighbors=neighbors_pairs) -> List[List[str]]:
    """The molecules of one bundle as lists of UMIs; the first UMI of a list represents it."""
    adj = directional_edges(counts, neighbors)
    taken = set()  # @line L6
    groups = []
    for u in visit_order(counts):  # @line L7
        if u in taken:  # @line L8
            continue
        reached, seen, queue = [], {u}, deque([u])  # @line L9
        while queue:
            x = queue.popleft()
            reached.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    queue.append(y)
        group = [x for x in visit_order({x: counts[x] for x in reached}) if x not in taken]  # @line L10
        taken.update(group)
        groups.append(group)
    return groups


def group_cluster(counts: Dict[str, int], neighbors=neighbors_pairs) -> List[List[str]]:
    """Connected components of the undirected graph of Hamming distance 1."""
    nb = neighbors(counts)
    taken, groups = set(), []
    for u in visit_order(counts):
        if u in taken:
            continue
        comp, queue = [], deque([u])
        taken.add(u)
        while queue:
            x = queue.popleft()
            comp.append(x)
            for y in nb[x]:
                if y not in taken:
                    taken.add(y)
                    queue.append(y)
        groups.append(visit_order({x: counts[x] for x in comp}))
    return groups


def group_unique(counts: Dict[str, int]) -> List[List[str]]:
    """Each distinct UMI is one molecule."""
    return [[u] for u in visit_order(counts)]


METHODS = {"directional": group_directional, "cluster": group_cluster, "unique": group_unique}


def count_molecules(reads: Iterable[Tuple[Hashable, Hashable, str]],
                    method: str = "directional") -> Dict[tuple, int]:
    """The number of molecules of each bundle (cell, locus)."""
    if method not in METHODS:
        raise ValueError(f"unknown method {method!r}")
    out = {}
    for key, counts in bundle_counts(reads).items():  # @line L2
        out[key] = len(METHODS[method](counts))  # @line L11
    return out  # @line L12


def deduplicate(reads: Sequence[Tuple[Hashable, Hashable, str]],
                method: str = "directional") -> List[int]:
    """The indices of the reads to keep: one read per molecule, with the UMI that represents it."""
    groups_of = {}
    for key, counts in bundle_counts(reads).items():
        groups_of[key] = {g[0] for g in METHODS[method](counts)}
    keep, done = [], set()
    for i, (cell, locus, umi) in enumerate(reads):
        key = (cell, locus)
        if umi in groups_of[key] and (key, umi) not in done:
            done.add((key, umi))
            keep.append(i)
    return keep
