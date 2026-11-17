# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gene-set-enrichment-analysis/. The authors are listed in prov/W39J2F.jsonl.
"""Gene set enrichment analysis (Subramanian et al. 2005).

enrichment_score walks down the genes in order of decreasing score r. A
member j of the set S adds |r_j|^p / N_R, with N_R the sum of |r_j|^p over
the members; a non-member subtracts 1 / (N - N_H), with N_H members among
N genes. The enrichment score ES is the value of the running sum farthest
from 0. With p = 0 it is the signed two-sample Kolmogorov-Smirnov statistic
of the member positions against the other positions. Genes with equal scores
keep the order in which they are given.

gsea scores the genes by the signal-to-noise ratio
(mean_A - mean_B) / (sd_A + sd_B), with sample standard deviations, and
builds a null by permuting the sample labels (all distinct assignments when
exact is True). It reports two p-values:

- p_sign, the GSEA convention: compare ES with the null scores of the same
  sign only, here with one added to both counts so that p is never 0;
- p_abs = (1 + #{|ES*| >= |ES|}) / (1 + B), a permutation p-value that is
  valid when the labels are exchangeable under the null hypothesis.

The normalized score is NES = ES / mean of the null scores with the sign of ES.
"""

from __future__ import annotations

import itertools
import math
from typing import Dict, Hashable, List, Mapping, Sequence, Tuple


def enrichment_score(genes: Sequence[Hashable], scores: Sequence[float],
                     gene_set, p: float = 1.0) -> Tuple[float, List[float]]:
    """(ES, running sum) for genes with these scores; the order is by decreasing score."""
    n = len(genes)
    if len(scores) != n:
        raise ValueError("need one score per gene")
    members = set(gene_set)
    order = sorted(range(n), key=lambda i: -scores[i])  # @line L1
    hits = [i for i in order if genes[i] in members]
    n_h = len(hits)
    if n_h == 0 or n_h == n:
        raise ValueError("the set must hold some but not all of the genes")
    weights = [abs(scores[i]) ** p for i in hits]  # @line L2
    n_r = sum(weights)
    if n_r == 0:
        weights = [1.0] * n_h
        n_r = float(n_h)
    weight = dict(zip(hits, weights))
    miss = 1.0 / (n - n_h)
    run = 0.0  # @line L3
    best = 0.0
    path = []
    for i in order:  # @line L4
        if i in weight:
            run += weight[i] / n_r  # @line L5
        else:
            run -= miss  # @line L6
        path.append(run)
        if abs(run) > abs(best):  # @line L7
            best = run
    return best, path  # @line L8


def leading_edge(genes: Sequence[Hashable], scores: Sequence[float], gene_set, p: float = 1.0) -> List[Hashable]:
    """The members at or before the peak (for ES > 0) or at or after it (for ES < 0)."""
    es, path = enrichment_score(genes, scores, gene_set, p)
    order = sorted(range(len(genes)), key=lambda i: -scores[i])
    peak = next(i for i, v in enumerate(path) if v == es)
    members = set(gene_set)
    part = order[: peak + 1] if es >= 0 else order[peak:]
    return [genes[i] for i in part if genes[i] in members]


def signal_to_noise(row: Sequence[float], labels: Sequence[int]) -> float:
    """(mean_A - mean_B) / (sd_A + sd_B), for label 1 (A) against label 0 (B)."""
    a = [x for x, c in zip(row, labels) if c == 1]
    b = [x for x, c in zip(row, labels) if c == 0]
    if len(a) < 2 or len(b) < 2:
        raise ValueError("need two samples in each group")
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    sa = math.sqrt(sum((x - ma) ** 2 for x in a) / (len(a) - 1))
    sb = math.sqrt(sum((x - mb) ** 2 for x in b) / (len(b) - 1))
    if sa + sb == 0:
        raise ValueError("a gene has no variation")
    return (ma - mb) / (sa + sb)


def _all_es(expr, genes, labels, gene_sets, p):
    r = [signal_to_noise(row, labels) for row in expr]
    return {name: enrichment_score(genes, r, s, p)[0] for name, s in gene_sets.items()}


def gsea(expr: Sequence[Sequence[float]], genes: Sequence[Hashable], labels: Sequence[int],
         gene_sets: Mapping[str, Sequence[Hashable]], rng=None, n_perm: int = 1000,
         p: float = 1.0, exact: bool = False) -> Dict[str, dict]:
    """ES, NES, p_sign and p_abs for each set, by phenotype permutation."""
    labels = list(labels)
    observed = _all_es(expr, genes, labels, gene_sets, p)
    null: Dict[str, List[float]] = {name: [] for name in gene_sets}
    if exact:
        n_a = sum(labels)
        for chosen in itertools.combinations(range(len(labels)), n_a):
            lab = [0] * len(labels)
            for i in chosen:
                lab[i] = 1
            if lab == labels:
                continue
            for name, v in _all_es(expr, genes, lab, gene_sets, p).items():
                null[name].append(v)
    else:
        if rng is None:
            raise ValueError("a random.Random object is needed for sampled permutations")
        lab = labels[:]
        for _ in range(n_perm):
            rng.shuffle(lab)
            for name, v in _all_es(expr, genes, lab, gene_sets, p).items():
                null[name].append(v)
    out = {}
    for name, es in observed.items():
        z = null[name]
        same = [v for v in z if (v >= 0) == (es >= 0)]
        if es >= 0:
            beyond = sum(v >= es for v in same)
        else:
            beyond = sum(v <= es for v in same)
        nes = es / (sum(abs(v) for v in same) / len(same)) if same else math.nan
        out[name] = {
            "es": es,
            "nes": nes,
            "p_sign": (1 + beyond) / (1 + len(same)),
            "p_abs": (1 + sum(abs(v) >= abs(es) for v in z)) / (1 + len(z)),
        }
    return out
