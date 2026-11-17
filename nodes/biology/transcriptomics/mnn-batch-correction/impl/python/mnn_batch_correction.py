# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mnn-batch-correction/. The authors are listed in prov/MTE8PT.jsonl.
"""Batch correction by mutual nearest neighbors (Haghverdi, Lun, Morgan and Marioni 2018).

A batch is a list of cells and a cell is a list of expression values (for
example log counts of the highly variable genes). The first batch is the
reference. For each further batch B, against the reference R:

1. Cosine normalization: each cell is divided by its Euclidean norm.
2. A cell r of R and a cell b of B are a mutual nearest neighbor (MNN) pair
   when r is among the k nearest cells of R to b and b is among the k nearest
   cells of B to r.
3. Each pair gives the vector r - b.
4. Each cell x of B gets the average of the pair vectors, weighted by a
   Gaussian kernel exp(-|x - b|^2 / sigma^2) of its distance to the cell b of
   the pair, and moves by that average.
5. The corrected batch joins the reference, and the next batch is corrected
   against the union.

Left out: the variance adjustment and the other options of the R function
mnnCorrect, approximate neighbor search, and the choice of the batch order.
Neighbor search is brute force with ties broken by index.
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple

from rq3lin import knn, sqdist

Matrix = List[List[float]]


def cosine_normalize(X: Sequence[Sequence[float]]) -> Matrix:
    out = []
    for row in X:
        norm = math.sqrt(sum(v * v for v in row))
        if norm == 0:
            raise ValueError("a cell with all values 0 has no direction")
        out.append([v / norm for v in row])  # @line L1
    return out


def mnn_pairs(R: Sequence[Sequence[float]], B: Sequence[Sequence[float]], k: int) -> List[Tuple[int, int]]:
    """All pairs (r, b) with r in the k nearest of b in R and b in the k nearest of r in B, sorted."""
    near_r = knn(R, k, queries=B)  # @line L2
    near_b = [set(row) for row in knn(B, k, queries=R)]
    return sorted((r, b) for b in range(len(B)) for r in near_r[b] if b in near_b[r])  # @line L3


def correction_vectors(R, B, pairs, sigma: float) -> Matrix:
    """The kernel-weighted average of the pair vectors r - b, for every cell of B."""
    if not pairs:
        raise ValueError("no mutual nearest neighbor pairs: the batches share no cell type")
    vecs = [[x - y for x, y in zip(R[r], B[b])] for r, b in pairs]  # @line L4
    out = []
    for x in B:
        d = [sqdist(x, B[b]) for _, b in pairs]
        m = min(d)
        w = [math.exp(-(di - m) / (sigma * sigma)) for di in d]  # the factor exp(-m / sigma^2) cancels
        tot = sum(w)
        out.append([sum(wi * v[a] for wi, v in zip(w, vecs)) / tot for a in range(len(x))])  # @line L5
    return out


def correct_pair(R, B, k: int, sigma: float) -> Matrix:
    pairs = mnn_pairs(R, B, k)
    corr = correction_vectors(R, B, pairs, sigma)
    return [[x + c for x, c in zip(row, cr)] for row, cr in zip(B, corr)]  # @line L6


def mnn_correct(batches: Sequence[Sequence[Sequence[float]]], k: int = 20, sigma: float = 0.1,
                cos_norm: bool = True) -> List[Matrix]:
    """The corrected batches, in the input order; the first batch is only normalized."""
    data = [cosine_normalize(b) if cos_norm else [list(map(float, r)) for r in b] for b in batches]
    out = [data[0]]
    ref = list(data[0])
    for B in data[1:]:
        kk = min(k, len(ref), len(B))
        C = correct_pair(ref, B, kk, sigma)
        out.append(C)
        ref = ref + C  # @line L7
    return out
