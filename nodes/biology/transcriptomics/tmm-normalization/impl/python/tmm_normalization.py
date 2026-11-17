# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tmm-normalization/. The authors are listed in prov/TKHD07.jsonl.
"""The trimmed mean of M-values (Robinson and Oshlack 2010).

tmm_factor follows .calcFactorTMM of edgeR: for each gene with a positive
count in both samples,

    M = log2((obs / N_obs) / (ref / N_ref)),
    A = (log2(obs / N_obs) + log2(ref / N_ref)) / 2,
    v = (N_obs - obs) / (N_obs obs) + (N_ref - ref) / (N_ref ref).

Genes are kept when the rank of M (average ranks for ties) lies in
[floor(n m_trim) + 1, n - floor(n m_trim)] and the rank of A lies in
[floor(n a_trim) + 1, n - floor(n a_trim)]. The factor is 2^f with f the
mean of the kept M values weighted by 1 / v.

norm_factors follows calcNormFactors(method = "TMM"): drop genes that are 0
in every sample, take as reference the sample whose upper quartile of
count / library size is closest to the mean of these quartiles (or, when the
median of the quartiles is below 1e-20, the sample with the largest sum of
square roots of counts), compute each factor against it, and divide by the
geometric mean of the factors so that their product is 1.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence


def average_ranks(xs: Sequence[float]) -> List[float]:
    """Ranks 1..n, with tied values given the mean of their ranks."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for t in range(i, j + 1):
            ranks[order[t]] = r
        i = j + 1
    return ranks


def tmm_factor(obs: Sequence[float], ref: Sequence[float],
               lib_obs: Optional[float] = None, lib_ref: Optional[float] = None,
               m_trim: float = 0.3, a_trim: float = 0.05,
               weighted: bool = True, a_cutoff: float = -1e10) -> float:
    """The TMM factor of sample obs against sample ref."""
    if len(obs) != len(ref):
        raise ValueError("obs and ref need the same genes")
    n_obs = float(sum(obs)) if lib_obs is None else float(lib_obs)
    n_ref = float(sum(ref)) if lib_ref is None else float(lib_ref)
    if n_obs <= 0 or n_ref <= 0:
        raise ValueError("library sizes must be positive")
    ms, avals, vs = [], [], []
    for o, r in zip(obs, ref):
        if o <= 0 or r <= 0:  # @line L1
            continue
        po, pr = o / n_obs, r / n_ref
        a = (math.log2(po) + math.log2(pr)) / 2
        if not a > a_cutoff:
            continue
        ms.append(math.log2(po / pr))  # @line L2
        avals.append(a)  # @line L3
        vs.append((n_obs - o) / n_obs / o + (n_ref - r) / n_ref / r)  # @line L4
    if not ms or max(abs(x) for x in ms) < 1e-6:
        return 1.0
    n = len(ms)
    lo_m = math.floor(n * m_trim) + 1  # @line L5
    hi_m = n + 1 - lo_m
    lo_a = math.floor(n * a_trim) + 1
    hi_a = n + 1 - lo_a
    rm = average_ranks(ms)  # @line L6
    ra = average_ranks(avals)
    keep = [g for g in range(n) if lo_m <= rm[g] <= hi_m and lo_a <= ra[g] <= hi_a]  # @line L7
    if not keep:
        return 1.0
    if weighted:
        num = sum(ms[g] / vs[g] for g in keep)  # @line L8
        den = sum(1.0 / vs[g] for g in keep)
        f = num / den if den > 0 and math.isfinite(num / den) else 0.0
    else:
        f = sum(ms[g] for g in keep) / len(keep)
    return 2.0 ** f  # @line L9


def quantile7(xs: Sequence[float], p: float) -> float:
    """The quantile of type 7 (the R default): linear between order statistics."""
    s = sorted(xs)
    h = (len(s) - 1) * p
    lo = math.floor(h)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (h - lo) * (s[hi] - s[lo])


def reference_column(counts: Sequence[Sequence[float]], lib: Sequence[float]) -> int:
    """The edgeR reference sample: upper quartile closest to the mean of the upper quartiles."""
    m = len(lib)
    f75 = [quantile7([row[j] for row in counts], 0.75) / lib[j] for j in range(m)]
    s = sorted(f75)
    med = s[m // 2] if m % 2 else (s[m // 2 - 1] + s[m // 2]) / 2
    if med < 1e-20:
        roots = [sum(math.sqrt(row[j]) for row in counts) for j in range(m)]
        return max(range(m), key=lambda j: (roots[j], -j))
    mean = sum(f75) / m
    return min(range(m), key=lambda j: (abs(f75[j] - mean), j))


def norm_factors(counts: Sequence[Sequence[float]], ref_column: Optional[int] = None,
                 **kwargs) -> List[float]:
    """TMM factors of all samples (columns of counts), scaled to product 1."""
    if not counts:
        raise ValueError("need at least one gene")
    m = len(counts[0])
    lib = [float(sum(row[j] for row in counts)) for j in range(m)]
    rows = [row for row in counts if any(k > 0 for k in row)]
    if ref_column is None:
        ref_column = reference_column(rows, lib)
    ref = [row[ref_column] for row in rows]
    f = [tmm_factor([row[j] for row in rows], ref, lib[j], lib[ref_column], **kwargs)
         for j in range(m)]
    g = math.exp(sum(math.log(x) for x in f) / m)
    return [x / g for x in f]


def effective_library_sizes(counts: Sequence[Sequence[float]], factors: Sequence[float]) -> List[float]:
    """Library size times the normalization factor, the offset used by edgeR."""
    m = len(factors)
    return [sum(row[j] for row in counts) * factors[j] for j in range(m)]
