# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/doublet-detection/. The authors are listed in prov/WZKYKW.jsonl.
"""Doublet scores in the manner of Scrublet (Wolock, Lopez and Klein 2019).

Steps: simulate doublets by adding the raw counts of two random observed cells,
normalize every profile to the same total, standardize each gene with the mean
and standard deviation of the observed cells, fit principal components on the
observed cells and project all profiles, find the k_adj nearest neighbors of
every profile among observed and simulated profiles, and turn the fraction of
simulated neighbors into a doublet probability with Bayes' rule.

What this small version leaves out, compared with the Scrublet package: the
selection of highly variable genes (the caller passes the genes to use), the
approximate neighbor search (the search here is brute force), the randomized
and sparse PCA solvers (here a full Jacobi eigendecomposition of the gene
covariance), the score of the simulated doublets of each observed cell, and
the error bars and z-scores of the scores. The defaults follow the package:
sim_ratio 2, expected doublet rate 0.1, k = round(0.5 sqrt(n)).
"""

from __future__ import annotations

import math
import random
from typing import List, Optional, Sequence, Tuple

from rq3lin import knn, pca_fit, pca_project

Matrix = List[List[float]]


def simulate_doublets(counts: Sequence[Sequence[float]], n_sim: int,
                      rng: random.Random) -> Tuple[Matrix, List[Tuple[int, int]]]:
    """n_sim profiles, each the sum of the raw counts of two observed cells.

    Draw order: for each doublet, rng.randrange(n) twice. As in Scrublet, the two
    cells are drawn with replacement, so a pair can repeat one cell.
    """
    n = len(counts)
    pairs, sims = [], []
    for _ in range(n_sim):
        a, b = rng.randrange(n), rng.randrange(n)
        pairs.append((a, b))
        sims.append([x + y for x, y in zip(counts[a], counts[b])])  # @line L1
    return sims, pairs


def normalize_total(X: Sequence[Sequence[float]], target: float) -> Matrix:
    """Scale each row to sum to target; a row of zeros stays zero."""
    out = []
    for row in X:
        t = sum(row)
        out.append([x * target / t for x in row] if t > 0 else [0.0] * len(row))
    return out


def standardize(obs: Matrix, sim: Matrix) -> Tuple[Matrix, Matrix]:
    """Z-scores of each gene, with the mean and standard deviation of the observed cells."""
    n, d = len(obs), len(obs[0])
    mu = [sum(r[g] for r in obs) / n for g in range(d)]
    sd = []
    for g in range(d):
        v = sum((r[g] - mu[g]) ** 2 for r in obs) / max(n - 1, 1)
        sd.append(math.sqrt(v) if v > 0 else 1.0)

    def z(X):
        return [[(r[g] - mu[g]) / sd[g] for g in range(d)] for r in X]

    return z(obs), z(sim)


def adjusted_k(k: int, n_obs: int, n_sim: int) -> int:
    """The neighbor count that keeps about k observed neighbors: round(k (1 + n_sim / n_obs))."""
    return int(round(k * (1.0 + n_sim / n_obs)))


def bayes_score(n_doublet_neighbors: int, k_adj: int, rho: float, r: float) -> float:
    """The doublet probability of Scrublet from the number of simulated neighbors.

    q = (nd + 1) / (k_adj + 2) and score = q rho / r / (1 - rho - q (1 - rho - rho / r)).
    """
    q = (n_doublet_neighbors + 1.0) / (k_adj + 2.0)  # @line L7
    return q * rho / r / (1.0 - rho - q * (1.0 - rho - rho / r))  # @line L8


def doublet_scores(counts: Sequence[Sequence[float]], rng: random.Random, sim_ratio: float = 2.0,
                   expected_rate: float = 0.1, k: Optional[int] = None, n_pcs: int = 10,
                   log_transform: bool = False) -> Tuple[List[float], List[float]]:
    """(scores of the observed cells, scores of the simulated doublets).

    counts holds one row of raw counts per cell, over the genes to use.
    """
    n = len(counts)
    if n < 3:
        raise ValueError("need at least 3 cells")
    if not 0.0 < expected_rate < 1.0:
        raise ValueError("expected_rate must be in (0, 1)")
    n_sim = int(round(sim_ratio * n))
    sim, _ = simulate_doublets(counts, n_sim, rng)
    target = sum(sum(r) for r in counts) / n
    obs_n = normalize_total(counts, target)  # @line L2
    sim_n = normalize_total(sim, target)
    if log_transform:
        obs_n = [[math.log1p(x) for x in r] for r in obs_n]
        sim_n = [[math.log1p(x) for x in r] for r in sim_n]
    obs_z, sim_z = standardize(obs_n, sim_n)  # @line L3
    mu, axes, _ = pca_fit(obs_z, min(n_pcs, len(obs_z[0])))  # @line L4
    emb = pca_project(obs_z, mu, axes) + pca_project(sim_z, mu, axes)
    if k is None:
        k = int(round(0.5 * math.sqrt(n)))
    k_adj = adjusted_k(k, n, n_sim)  # @line L5
    k_adj = min(k_adj, n + n_sim - 1)
    neighbors = knn(emb, k_adj)  # @line L6
    r = n_sim / n
    scores = [bayes_score(sum(1 for j in nb if j >= n), k_adj, expected_rate, r) for nb in neighbors]
    return scores[:n], scores[n:]


def threshold_minimum(values: Sequence[float], nbins: int = 50, max_iter: int = 10000) -> float:
    """The threshold at the valley of a bimodal histogram (the method of skimage threshold_minimum).

    Smooth the histogram with a 3-bin mean until it has exactly two local maxima,
    then return the center of the lowest bin between them.
    """
    lo, hi = min(values), max(values)
    if hi == lo:
        raise ValueError("all values are equal")
    width = (hi - lo) / nbins
    h = [0.0] * nbins
    for v in values:
        h[min(int((v - lo) / width), nbins - 1)] += 1.0
    for _ in range(max_iter):
        peaks = local_maxima(h)
        if len(peaks) == 2:
            a, b = peaks
            valley = min(range(a, b + 1), key=lambda i: (h[i], i))
            return lo + (valley + 0.5) * width  # @line L9
        if len(peaks) < 2:
            break
        h = [(h[max(i - 1, 0)] + h[i] + h[min(i + 1, nbins - 1)]) / 3.0 for i in range(nbins)]
    raise ValueError("the histogram does not become bimodal")


def local_maxima(h: Sequence[float]) -> List[int]:
    """The bins where the histogram stops rising and starts falling, as skimage finds them."""
    out, rising = [], True
    for i in range(len(h) - 1):
        if rising and h[i + 1] < h[i]:
            out.append(i)
            rising = False
        elif not rising and h[i + 1] > h[i]:
            rising = True
    return out


def call_doublets(scores: Sequence[float], threshold: float) -> List[bool]:
    """True for each cell whose score is above the threshold."""
    return [s > threshold for s in scores]  # @line L10
