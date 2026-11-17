# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gibbs-motif-sampler/. The authors are listed in prov/2BA89G.jsonl.
"""The site sampler of Lawrence et al. (1993) for one motif site per sequence.

The motif columns have a symmetric pseudocount b on every letter, and the
background letter probabilities q are fixed. Each update removes the site of
one sequence, scores every window of that sequence by
prod_j (c_j(x_j) + b) / ((n - 1 + 4b) q(x_j)) and draws the new site with
probability proportional to the score.

Positions are 0-based in this code; the page numbers them from 1.
"""

import math
import random
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

from bioseq import DNA, kmers

_INDEX = {a: k for k, a in enumerate(DNA)}


class GibbsResult(NamedTuple):
    """The best state seen: windows, 0-based starts, log target, and the
    iteration (0 for the start) at which it was first seen."""

    motifs: Tuple[str, ...]
    starts: Tuple[int, ...]
    log_target: float
    iteration: int


def background_from(seqs: Sequence[str]) -> Dict[str, float]:
    """Letter frequencies over all sequences (a letter that never occurs gets one count)."""
    counts = {a: max(1, sum(s.count(a) for s in seqs)) for a in DNA}
    total = sum(counts.values())
    return {a: counts[a] / total for a in DNA}


def column_counts(windows: Sequence[str], L: int) -> List[List[int]]:
    """counts[j][a] = the number of windows with letter a in column j."""
    counts = [[0] * 4 for _ in range(L)]
    for w in windows:
        for j, a in enumerate(w):
            counts[j][_INDEX[a]] += 1
    return counts


def site_weights(seq: str, counts: List[List[int]], n_other: int, b, q) -> list:
    """The weight of each window x of seq: prod_j (c_j(x_j) + b) / ((n_other + 4b) q(x_j)).

    counts are the column counts of the other n_other sites. With Fraction
    values for b and q the weights are exact.
    """
    L = len(counts)
    denom = n_other + 4 * b
    out = []
    for w in kmers(seq, L):
        v = 1
        for j, a in enumerate(w):
            v = v * (counts[j][_INDEX[a]] + b) / (denom * q[a])
        out.append(v)
    return out


def _rising_log(b: float, m: int) -> float:
    """log of b (b + 1) ... (b + m - 1)."""
    return math.lgamma(b + m) - math.lgamma(b)


def log_target(seqs: Sequence[str], starts: Sequence[int], L: int, b: float, q) -> float:
    """log pi(starts) up to a constant: sum over columns and letters of the log
    rising factorial (b)_c, minus the log background probability of the sites."""
    windows = [s[p:p + L] for s, p in zip(seqs, starts)]
    v = 0.0
    for col in column_counts(windows, L):
        v += sum(_rising_log(b, c) for c in col)
    for w in windows:
        v -= sum(math.log(q[a]) for a in w)
    return v


def draw(rng: random.Random, weights: Sequence[float]) -> int:
    """An index drawn with probability weights[k] / sum(weights), using one rng.random()."""
    u = rng.random() * sum(weights)
    acc = 0.0
    for k, w in enumerate(weights):
        acc += w
        if u < acc:
            return k
    return len(weights) - 1


def _check(seqs, L, b, q):
    if L <= 0:
        raise ValueError("L must be positive")
    if len(seqs) < 2:
        raise ValueError("need at least two sequences")
    for s in seqs:
        if len(s) < L or set(s) - set(DNA):
            raise ValueError("sequences must be over ACGT with length at least L")
    if b <= 0:
        raise ValueError("the pseudocount b must be positive")
    if any(q[a] <= 0 for a in DNA):
        raise ValueError("background probabilities must be positive")


def gibbs_motif_sampler(seqs: Sequence[str], L: int, iterations: int, seed: int = 0, b: float = 1.0,
                        background: Optional[Dict[str, float]] = None,
                        scan: str = "systematic") -> GibbsResult:
    """Run the site sampler and return the state with the largest log target seen.

    Draw order: random.Random(seed); first one rng.randrange(W_i) per sequence
    for the start; then for each update one rng.randrange(n) (only when scan is
    "random") and one rng.random() for the draw. An iteration is n updates; the
    systematic scan updates sequences 1 to n in order. Cost: O(n W L) time per
    iteration and O(n L) extra space.
    """
    q = background if background is not None else background_from(seqs)
    _check(seqs, L, b, q)
    if iterations < 0:
        raise ValueError("iterations must be at least 0")
    if scan not in ("systematic", "random"):
        raise ValueError("scan must be 'systematic' or 'random'")
    rng = random.Random(seed)
    n = len(seqs)
    starts = [rng.randrange(len(s) - L + 1) for s in seqs]  # @line L1
    counts = column_counts([s[p:p + L] for s, p in zip(seqs, starts)], L)
    logq = {a: math.log(q[a]) for a in DNA}
    log_denom = math.log(n - 1 + 4 * b)
    cur = log_target(seqs, starts, L, b, q)
    best = GibbsResult(tuple(s[p:p + L] for s, p in zip(seqs, starts)), tuple(starts), cur, 0)  # @line L2
    for it in range(1, iterations + 1):  # @line L3
        for k in range(n):  # @line L4
            i = k if scan == "systematic" else rng.randrange(n)
            s = seqs[i]
            for j, a in enumerate(s[starts[i]:starts[i] + L]):  # @line L5
                counts[j][_INDEX[a]] -= 1
            logw = []
            for x in range(len(s) - L + 1):  # @line L6
                v = 0.0
                for j in range(L):
                    a = s[x + j]
                    v += math.log(counts[j][_INDEX[a]] + b) - log_denom - logq[a]
                logw.append(v)
            top = max(logw)
            starts[i] = draw(rng, [math.exp(v - top) for v in logw])  # @line L7
            for j, a in enumerate(s[starts[i]:starts[i] + L]):  # @line L8
                counts[j][_INDEX[a]] += 1
        cur = log_target(seqs, starts, L, b, q)  # @line L9
        if cur > best.log_target:
            best = GibbsResult(tuple(s[p:p + L] for s, p in zip(seqs, starts)), tuple(starts), cur, it)
    return best  # @line L10
