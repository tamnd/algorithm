# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/median-of-ratios-normalization/. The authors are listed in prov/NF2283.jsonl.
"""Median-of-ratios size factors (Anders and Huber 2010, DESeq and DESeq2).

counts is a list of rows, one row per gene and one column per sample. The
size factor of sample j is

    s_j = median over genes g in G of K[g][j] / geomean_k K[g][k],

where G is the set of genes with a positive count in every sample. The
median is taken on the log scale, so for an even number of genes it is the
geometric mean of the two middle ratios. This is what DESeq2 does in
estimateSizeFactorsForMatrix with its default settings.

A fixed reference can be given as log_geo_means (one value per gene, with
-inf or None for a gene that must not be used); then only the samples to be
scaled need to be in counts.
"""

from __future__ import annotations

import math
from statistics import median
from typing import List, Optional, Sequence


def log_geometric_means(counts: Sequence[Sequence[float]]) -> List[float]:
    """The mean of log K[g][j] over the samples j, or -inf when a count is 0."""
    out = []
    for row in counts:
        if len(row) == 0:
            raise ValueError("every gene needs at least one sample")
        if any(k < 0 for k in row):
            raise ValueError("counts must be >= 0")
        if all(k > 0 for k in row):  # @line L2
            out.append(sum(math.log(k) for k in row) / len(row))  # @line L3
        else:
            out.append(-math.inf)
    return out


def size_factors(counts: Sequence[Sequence[float]],
                 log_geo_means: Optional[Sequence[Optional[float]]] = None) -> List[float]:
    """The median-of-ratios size factors, one per sample (column)."""
    if not counts:
        raise ValueError("need at least one gene")
    m = len(counts[0])
    if any(len(row) != m for row in counts):
        raise ValueError("every gene needs the same number of samples")
    if log_geo_means is None:
        lg = log_geometric_means(counts)  # @line L1
    else:
        if len(log_geo_means) != len(counts):
            raise ValueError("need one reference value per gene")
        lg = [-math.inf if v is None else float(v) for v in log_geo_means]
    use = [g for g in range(len(counts)) if math.isfinite(lg[g])]  # @line L4
    if not use:  # @line L5
        raise ValueError("no gene has a positive count in every sample")
    s = []
    for j in range(m):  # @line L6
        r = [math.log(counts[g][j]) - lg[g] for g in use if counts[g][j] > 0]  # @line L7
        if not r:
            raise ValueError("sample %d has no usable gene" % j)
        s.append(math.exp(median(r)))  # @line L8
    return s  # @line L9


def normalized_counts(counts: Sequence[Sequence[float]],
                      factors: Optional[Sequence[float]] = None) -> List[List[float]]:
    """K[g][j] / s_j, with the median-of-ratios factors unless others are given."""
    s = size_factors(counts) if factors is None else list(factors)
    return [[row[j] / s[j] for j in range(len(s))] for row in counts]
