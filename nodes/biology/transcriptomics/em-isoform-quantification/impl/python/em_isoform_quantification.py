# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/em-isoform-quantification/. The authors are listed in prov/QSYASY.jsonl.

"""EM estimation of transcript abundances from read equivalence classes.

The model is the one of RSEM without the noise transcript and without
sequence or position bias. There are m transcripts with ids 0 to m - 1 and
effective lengths eff_len[t] > 0. A read comes from transcript t with
probability alpha[t], and then from one of its eff_len[t] start positions with
equal probability. A read is summarized by the set of transcripts it is
compatible with (its equivalence class e), and the likelihood of the reads is

    L(alpha) = prod over classes e of (sum over t in e of alpha[t] / eff_len[t]) ** c_e,

where c_e is the number of reads in class e. Classes are lists of
(transcripts, count) pairs, where transcripts is a tuple of distinct ids.
An empty tuple (an unmapped read) is skipped.
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

Classes = Sequence[Tuple[Tuple[int, ...], float]]


def effective_length(length: int, mean_frag: float) -> float:
    """The number of start positions of a fragment of the mean length, at least 1."""
    return max(length - mean_frag + 1.0, 1.0)


def equivalence_classes(read_sets: Iterable[Iterable[int]]) -> List[Tuple[Tuple[int, ...], int]]:
    """Group reads by their compatible sets: a sorted list of (sorted tuple, count)."""
    counts: Dict[Tuple[int, ...], int] = {}
    for s in read_sets:
        key = tuple(sorted(set(s)))
        counts[key] = counts.get(key, 0) + 1
    return sorted(counts.items())


def log_likelihood(alpha: Sequence[float], classes: Classes, eff_len: Sequence[float]) -> float:
    """log L(alpha); minus infinity if a class with reads gets probability 0."""
    total = 0.0
    for e, c in classes:
        if not e or c == 0:
            continue
        s = sum(alpha[u] / eff_len[u] for u in e)
        if s <= 0.0:
            return -math.inf
        total += c * math.log(s)
    return total


def em(classes: Classes, eff_len: Sequence[float], max_iter: int = 10000,
       eps: float = 1e-10, trace: Optional[List[float]] = None) -> List[float]:
    """Return the read fractions alpha after EM from the uniform start.

    The loop stops when no alpha[t] moves by eps or more, or after max_iter
    rounds. If trace is a list, the log-likelihood of each iterate is appended.
    """
    m = len(eff_len)
    live = [(e, c) for e, c in classes if e and c > 0]
    n_reads = sum(c for _, c in live)
    if m == 0 or n_reads == 0:
        raise ValueError("need at least one transcript and one mapped read")
    alpha = [1.0 / m] * m  # @line L1
    if trace is not None:
        trace.append(log_likelihood(alpha, live, eff_len))
    for _ in range(max_iter):  # @line L2
        n = [0.0] * m  # @line L3
        for e, c in live:  # @line L4
            s = sum(alpha[u] / eff_len[u] for u in e)  # @line L5
            for t in e:
                n[t] += c * (alpha[t] / eff_len[t]) / s  # @line L6
        new = [x / n_reads for x in n]  # @line L7
        if trace is not None:
            trace.append(log_likelihood(new, live, eff_len))
        if max(abs(a - b) for a, b in zip(new, alpha)) < eps:  # @line L8
            return new
        alpha = new  # @line L9
    return alpha  # @line L10


def transcript_fractions(alpha: Sequence[float], eff_len: Sequence[float]) -> List[float]:
    """tau[t]: the fraction of transcript molecules, alpha[t] / eff_len[t] normalized to sum 1."""
    rho = [a / l for a, l in zip(alpha, eff_len)]
    s = sum(rho)
    return [r / s for r in rho]


def tpm(alpha: Sequence[float], eff_len: Sequence[float]) -> List[float]:
    """Transcripts per million: 10**6 times the transcript fractions."""
    return [1e6 * x for x in transcript_fractions(alpha, eff_len)]
