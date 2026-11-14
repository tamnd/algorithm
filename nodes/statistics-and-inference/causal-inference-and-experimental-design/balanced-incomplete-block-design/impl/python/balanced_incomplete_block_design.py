# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balanced-incomplete-block-design/. The authors are listed in prov/JG5X5V.jsonl.
"""Balanced incomplete block designs: checking, construction and intrablock analysis.

A BIBD(v, b, r, k, lambda) has v treatments in b blocks of size k < v, each treatment in
r blocks and each pair of treatments together in lambda blocks. Then b k = v r,
lambda (v - 1) = r (k - 1) and b >= v (Fisher's inequality).
"""

import math
from collections.abc import Sequence
from itertools import combinations

Block = Sequence[int]


def parameters(v: int, blocks: Sequence[Block]) -> tuple[int, int, int, int, int]:
    """(v, b, r, k, lambda) if the blocks on treatments 0..v-1 form a BIBD, else ValueError."""
    b = len(blocks)
    sizes = {len(set(blk)) for blk in blocks} | {len(blk) for blk in blocks}
    if len(sizes) != 1:
        raise ValueError("blocks must have one size and no repeated treatment")
    k = sizes.pop()
    reps = [sum(t in blk for blk in blocks) for t in range(v)]
    if len(set(reps)) != 1:
        raise ValueError("treatments are not equally replicated")
    pair = {}
    for blk in blocks:
        for x, y in combinations(sorted(blk), 2):
            pair[x, y] = pair.get((x, y), 0) + 1
    counts = {pair.get(xy, 0) for xy in combinations(range(v), 2)}
    if len(counts) != 1:
        raise ValueError("pairs do not occur together equally often")
    return v, b, reps[0], k, counts.pop()


def develop(base_blocks: Sequence[Block], v: int) -> list[list[int]]:
    """Cyclic development: each base block B gives the blocks B + i (mod v), i = 0..v-1."""
    return [sorted((x + i) % v for x in blk) for blk in base_blocks for i in range(v)]


def fano() -> list[list[int]]:
    """The Fano plane, a (7, 7, 3, 3, 1) design: the difference set {0, 1, 3} mod 7."""
    return develop([[0, 1, 3]], 7)


def kirkman_15() -> list[list[list[int]]]:
    """A resolution of a (15, 35, 7, 3, 1) design into 7 parallel classes of 5 blocks
    (Kirkman's schoolgirl problem). Points are the nonzero vectors of GF(2)^4 (as the
    integers 1..15, shifted to 0..14), blocks are the lines {x, y, x xor y} of PG(3, 2),
    and a backtracking search packs the 56 spreads (sets of 5 disjoint lines) into 7
    spreads that use every line once."""
    lines = sorted({tuple(sorted((x, y, x ^ y))) for x in range(1, 16) for y in range(1, 16) if x != y})
    spreads = []
    for combo in combinations(range(len(lines)), 5):
        pts = [p for i in combo for p in lines[i]]
        if len(set(pts)) == 15:
            spreads.append(frozenset(combo))

    def search(chosen, used):
        if len(chosen) == 7:
            return chosen
        first = min(set(range(len(lines))) - used)  # the first unused line must be covered
        for s in spreads:
            if first in s and not s & used:
                found = search(chosen + [s], used | s)
                if found:
                    return found
        return None

    days = search([], frozenset())
    return sorted([sorted([p - 1 for p in lines[i]] for i in s) for s in days])


def efficiency_factor(v: int, k: int, lam: int, r: int) -> float:
    """E = lambda v / (r k): the variance ratio of a complete block design to the BIBD."""
    return lam * v / (r * k)


def intrablock_estimates(v: int, blocks: Sequence[Block], y: Sequence[Sequence[float]]) -> list[float]:
    """Treatment effects tau_hat_i = k Q_i / (lambda v), with sum tau_hat_i = 0, where
    Q_i = T_i - (1/k) (sum of the totals of the blocks that hold i). y[j][m] is the
    response of treatment blocks[j][m] in block j."""
    v, b, r, k, lam = parameters(v, blocks)
    t = [0.0] * v
    adj = [0.0] * v
    for blk, ys in zip(blocks, y):
        total = math.fsum(ys)
        for trt, val in zip(blk, ys):
            t[trt] += val
            adj[trt] += total / k
    return [k * (t[i] - adj[i]) / (lam * v) for i in range(v)]
