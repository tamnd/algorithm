# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ld-score-regression/. The authors are listed in prov/E6NC45.jsonl.
"""A small version of LD score regression (Bulik-Sullivan et al. 2015).

Under a polygenic model, the chi-squared statistic of SNP j in a GWAS of N
people satisfies

    E[chi2_j | l_j] = N h2 l_j / M + N a + 1,

where l_j = sum_k r2_jk is the LD score of SNP j, M is the number of SNPs,
h2 is the SNP heritability and N a measures confounding such as population
stratification. Regressing chi2_j on l_j gives h2 from the slope and the
confounding from the intercept.

What this version leaves out, compared with the ldsc software:
- LD scores come from one small reference panel given as genotypes, with
  SNP windows by genetic position; no reading of real panels or annotations.
- No partitioned (stratified) regression over functional annotations.
- No genetic correlation between two traits.
- No filtering of SNPs (minor allele frequency, strand, large chi2 values)
  and no two-step estimator that fixes the intercept from SNPs with small
  chi2 first.
- The regression weight 1/max(l_j, 1) uses the LD score over all SNPs, not
  over the regression SNPs only.
- No transformation of h2 to the liability scale for case-control studies.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence


def r2_unbiased(r2: float, n: int) -> float:
    """The approximately unbiased estimate r2 - (1 - r2) / (n - 2) of the squared correlation."""
    return r2 - (1.0 - r2) / (n - 2)


def ld_scores(G: Sequence[Sequence[int]], pos: Sequence[float], window: float) -> List[float]:
    """LD scores from a reference panel.

    G is n_ref people by M SNPs, pos the sorted genetic positions of the SNPs,
    and window the half width: l_j sums the corrected r2_jk over the SNPs k with
    |pos_k - pos_j| <= window, including k = j, which adds exactly 1.
    """
    n = len(G)
    M = len(pos)
    cols = []
    for j in range(M):
        x = [float(G[i][j]) for i in range(n)]
        mu = sum(x) / n
        c = [v - mu for v in x]
        s = math.sqrt(sum(v * v for v in c))
        cols.append([v / s for v in c] if s > 0 else None)
    l = [1.0 if cols[j] is not None else 0.0 for j in range(M)]
    for j in range(M):
        if cols[j] is None:
            continue
        cj = cols[j]
        k = j + 1
        while k < M and pos[k] - pos[j] <= window:  # @line L1
            if cols[k] is not None:
                r = sum(a * b for a, b in zip(cj, cols[k]))
                v = r2_unbiased(r * r, n)  # @line L2
                l[j] += v
                l[k] += v
            k += 1
    return l


def _wls_line(x: Sequence[float], y: Sequence[float], w: Sequence[float]):
    """Weighted least squares fit of y = a + b x. Returns (a, b)."""
    sw = sum(w)
    mx = sum(wi * xi for wi, xi in zip(w, x)) / sw
    my = sum(wi * yi for wi, yi in zip(w, y)) / sw
    sxx = sum(wi * (xi - mx) ** 2 for wi, xi in zip(w, x))
    sxy = sum(wi * (xi - mx) * (yi - my) for wi, xi, yi in zip(w, x, y))
    b = sxy / sxx
    return my - b * mx, b


def ldsc(chi2: Sequence[float], l: Sequence[float], N: float, M: int,
         n_blocks: int = 20, rounds: int = 3) -> Dict[str, float]:
    """LD score regression of chi2 on l, with a block jackknife.

    Returns h2, intercept, their jackknife standard errors, and the ratio
    (intercept - 1) / (mean chi2 - 1).
    """
    J = len(chi2)
    if n_blocks < 2 or J < 2 * n_blocks:
        raise ValueError("need at least two SNPs per block and two blocks")
    mean_chi2 = sum(chi2) / J
    mean_l = sum(l) / J
    h2 = min(max(M * (mean_chi2 - 1.0) / (N * mean_l), 0.0), 1.0)  # @line L3
    a = 1.0
    w: List[float] = []
    for _ in range(rounds):
        w = [1.0 / (max(lj, 1.0) * max(a + N * h2 * lj / M, 1.0) ** 2) for lj in l]  # @line L4
        a, b = _wls_line(l, chi2, w)  # @line L5
        h2 = min(max(b * M / N, 0.0), 1.0)  # @line L6
    h2_hat = b * M / N
    # Delete-one-block jackknife over contiguous blocks, with the weights fixed.
    bounds = [round(t * J / n_blocks) for t in range(n_blocks + 1)]
    ps_a, ps_h = [], []
    for t in range(n_blocks):
        keep = [j for j in range(J) if not bounds[t] <= j < bounds[t + 1]]
        aa, bb = _wls_line([l[j] for j in keep], [chi2[j] for j in keep], [w[j] for j in keep])  # @line L7
        ps_a.append(aa)
        ps_h.append(bb * M / N)

    def jk_se(vals):
        m = sum(vals) / n_blocks
        return math.sqrt((n_blocks - 1) / n_blocks * sum((v - m) ** 2 for v in vals))

    ratio = (a - 1.0) / (mean_chi2 - 1.0) if mean_chi2 > 1.0 else float("nan")
    return {"h2": h2_hat, "intercept": a, "se_h2": jk_se(ps_h),
            "se_intercept": jk_se(ps_a), "ratio": ratio}  # @line L8
