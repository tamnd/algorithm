# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dense-max-cut-ptas/. The authors are listed in prov/SEQDJG.jsonl.

"""A sampling scheme for max-cut in dense graphs: split V into ell parts, sample t vertices outside each part,
try every labelling of the samples, and put each vertex on the side that cuts more sampled neighbours."""

import random
from itertools import product
from math import ceil
from typing import Optional, Sequence

Graph = Sequence[set]


def cut_value(adj: Graph, side: Sequence[int]) -> int:
    return sum(1 for u in range(len(adj)) for v in adj[u] if u < v and side[u] != side[v])


def split(n: int, ell: int) -> list[list[int]]:
    """The parts V_1, ..., V_ell of near-equal size."""
    return [list(range(j * n // ell, (j + 1) * n // ell)) for j in range(ell)]


def draw_samples(n: int, parts: list[list[int]], t: int, rng: random.Random) -> list[list[int]]:
    """For each part, t vertices drawn uniformly with replacement from outside the part."""
    out = []
    for part in parts:
        inside = set(part)
        rest = [v for v in range(n) if v not in inside]
        out.append([rng.choice(rest) for _ in range(t)] if rest else [])
    return out


def place(adj: Graph, parts: list[list[int]], samples: list[list[int]], labels: Sequence[Sequence[int]]) -> list[int]:
    """Given a label (side 0 or 1) for each sample of each part, place the vertices of each part."""
    side = [0] * len(adj)
    for j, part in enumerate(parts):  # @line L4
        for v in part:
            a = [0, 0]
            for u, s in zip(samples[j], labels[j]):  # @line L5
                if u in adj[v]:
                    a[s] += 1
            side[v] = 1 if a[0] >= a[1] else 0  # @line L6
    return side


def dense_max_cut(adj: Graph, ell: int, t: int, rng: random.Random, stats: Optional[dict] = None) -> list[int]:
    """The best cut over all 2^(ell t) labellings of one draw of samples."""
    n = len(adj)
    parts = split(n, ell)  # @line L1
    samples = draw_samples(n, parts, t, rng)  # @line L2
    best, best_val, guesses = [0] * n, -1, 0
    sizes = [len(s) for s in samples]
    for flat in product((0, 1), repeat=sum(sizes)):  # @line L3
        guesses += 1
        labels, pos = [], 0
        for size in sizes:
            labels.append(flat[pos:pos + size])
            pos += size
        side = place(adj, parts, samples, labels)
        val = cut_value(adj, side)  # @line L7
        if val > best_val:  # @line L8
            best, best_val = side, val
    if stats is not None:
        stats.update(guesses=guesses, parts=parts, samples=samples)
    return best  # @line L9


def parameters(eps: float, delta: float) -> tuple[int, int]:
    """ell and t with n^2 (1/sqrt(t) + 1/(2 ell)) <= eps OPT when the graph has at least delta n^2 edges."""
    return ceil(2 / (eps * delta)), ceil((4 / (eps * delta)) ** 2)
