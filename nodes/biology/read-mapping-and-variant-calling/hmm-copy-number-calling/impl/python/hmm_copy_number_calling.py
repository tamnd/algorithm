# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmm-copy-number-calling/. The authors are listed in prov/HP6C4B.jsonl.
"""Copy number calls from read depth with a hidden Markov model.

The input is a list of read counts, one for each window of the same size
along a chromosome. The hidden state of a window is its copy number c in
0, 1, ..., K - 1. The model is:

- emission: the count of a window with copy number c is Poisson with mean
  lam * max(c, eps) / 2, where lam is the mean count of a diploid window and
  eps > 0 stands for the reads that map to a deleted region by error;
- transition: a window keeps the state of the window before it with
  probability 1 - p, and moves to each of the other K - 1 states with
  probability p / (K - 1);
- start: each state with probability 1 / K.

viterbi gives the most probable state path and forward gives the
probability of the counts. Both work in log space and take O(K^2 n) time
for n windows; viterbi keeps an n by K table of back pointers.

What this code leaves out compared with tools such as CNVnator or the HMM of
PennCNV: correction of the counts for GC content and mappability, the
dispersion of real counts (a negative binomial emission fits better), the
B allele frequency, training of the parameters, and tumor purity.
"""

from __future__ import annotations

import math
from statistics import median
from typing import List, Sequence, Tuple

from biostoch import logsumexp


def emission_logs(counts: Sequence[int], lam: float, K: int, eps: float = 0.05) -> List[List[float]]:
    """E[t][c] = ln P(count t | copy number c) under the Poisson model."""
    E = []
    for x in counts:
        row = []
        for c in range(K):
            mu = lam * max(c, eps) / 2.0
            row.append(x * math.log(mu) - mu - math.lgamma(x + 1))
        E.append(row)
    return E


def transition_logs(K: int, p: float) -> List[List[float]]:
    """T[b][c] = ln P(state c at t | state b at t - 1)."""
    if K == 1:
        return [[0.0]]
    stay, move = math.log(1.0 - p), math.log(p / (K - 1))
    return [[stay if b == c else move for c in range(K)] for b in range(K)]


def viterbi(log_init: Sequence[float], T: Sequence[Sequence[float]],
            E: Sequence[Sequence[float]]) -> Tuple[List[int], float]:
    """The most probable state path and its log probability (joint with the counts).

    Ties go to the smaller state.
    """
    n = len(E)
    if n == 0:
        return [], 0.0
    K = len(log_init)
    V = [log_init[c] + E[0][c] for c in range(K)]  # @line L2
    back: List[List[int]] = []
    for t in range(1, n):  # @line L3
        new, ptr = [], []
        for c in range(K):  # @line L4
            b = max(range(K), key=lambda b: (V[b] + T[b][c], -b))
            new.append(V[b] + T[b][c] + E[t][c])  # @line L5
            ptr.append(b)  # @line L6
        V = new
        back.append(ptr)
    last = max(range(K), key=lambda c: (V[c], -c))  # @line L7
    path = [last]
    for t in range(n - 2, -1, -1):  # @line L8
        path.append(back[t][path[-1]])
    path.reverse()
    return path, V[last]


def forward(log_init: Sequence[float], T: Sequence[Sequence[float]],
            E: Sequence[Sequence[float]]) -> Tuple[List[List[float]], float]:
    """The forward table F[t][c] = ln P(counts 0..t, state c at t) and ln P(all counts)."""
    K = len(log_init)
    if not E:
        return [], 0.0
    F = [[log_init[c] + E[0][c] for c in range(K)]]
    for t in range(1, len(E)):
        F.append([E[t][c] + logsumexp(F[-1][b] + T[b][c] for b in range(K)) for c in range(K)])
    return F, logsumexp(F[-1])


def backward(T: Sequence[Sequence[float]], E: Sequence[Sequence[float]]) -> List[List[float]]:
    """The backward table B[t][c] = ln P(counts t+1..n-1 | state c at t)."""
    n = len(E)
    if n == 0:
        return []
    K = len(T)
    B = [[0.0] * K for _ in range(n)]
    for t in range(n - 2, -1, -1):
        B[t] = [logsumexp(T[c][d] + E[t + 1][d] + B[t + 1][d] for d in range(K)) for c in range(K)]
    return B


def posteriors(log_init, T, E) -> List[List[float]]:
    """P(state c at t | all counts), by the forward and backward tables."""
    F, total = forward(log_init, T, E)
    B = backward(T, E)
    return [[math.exp(f + b - total) for f, b in zip(Ft, Bt)] for Ft, Bt in zip(F, B)]


def segments(path: Sequence[int]) -> List[Tuple[int, int, int]]:
    """The runs (lo, hi, c) of equal states, half-open."""
    out = []
    lo = 0
    for t in range(1, len(path) + 1):
        if t == len(path) or path[t] != path[lo]:
            out.append((lo, t, path[lo]))
            lo = t
    return out


def call_copy_number(counts: Sequence[int], K: int = 5, p: float = 1e-3, lam: float = None,
                     eps: float = 0.05) -> Tuple[List[int], List[Tuple[int, int, int]]]:
    """Viterbi copy numbers of the windows and their segments.

    With lam not given, the median count stands for a diploid window, which
    assumes that most of the chromosome has copy number 2.
    """
    if not counts:
        return [], []
    if lam is None:
        lam = max(float(median(counts)), 1e-9)
    E = emission_logs(counts, lam, K, eps)  # @line L1
    T = transition_logs(K, p)
    init = [-math.log(K)] * K
    path, _ = viterbi(init, T, E)
    return path, segments(path)  # @line L9
