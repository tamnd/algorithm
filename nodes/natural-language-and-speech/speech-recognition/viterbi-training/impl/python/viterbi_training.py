# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/viterbi-training/. The authors are listed in prov/W6039V.jsonl.

"""Viterbi training (segmental k-means) of a discrete hidden Markov model.

lambda = (pi, A, B) with N states 0..N-1 and M symbols 0..M-1:
pi[i] = P(q_1 = i), A[i][j] = P(q_(t+1) = j | q_t = i), B[j][k] = P(o_t = k | q_t = j).

Each round aligns every training sequence with its best state path (the
Viterbi path) and then sets the parameters to the relative frequencies of the
hard counts along those paths. The objective is the sum over the sequences of
max_Q log P(O, Q | lambda), the log joint of the best path. It never decreases.
The total likelihood log P(O | lambda) can decrease; the tests show a case.

Tie rule of the alignment: the smallest state index wins (as on the
viterbi-algorithm page). A row with no counts keeps its old values.
"""

import math
from typing import List, Sequence

from nlslog import NEG_INF, log_sum, safe_log


def viterbi_path(log_pi, log_A, log_B, obs):
    """Return (path, score) of a most likely state path, in log space."""
    N, T = len(log_pi), len(obs)
    delta = [log_pi[j] + log_B[j][obs[0]] for j in range(N)]
    back = [[0] * N]
    for t in range(1, T):
        new, ptr = [], []
        for j in range(N):
            b = 0
            for i in range(1, N):
                if delta[i] + log_A[i][j] > delta[b] + log_A[b][j]:
                    b = i
            ptr.append(b)
            new.append(delta[b] + log_A[b][j] + log_B[j][obs[t]])
        delta = new
        back.append(ptr)
    last = 0
    for j in range(1, N):
        if delta[j] > delta[last]:
            last = j
    path = [last]
    for t in range(T - 1, 0, -1):
        path.append(back[t][path[-1]])
    path.reverse()
    return path, delta[last]


def _logs(m):
    return [[safe_log(p) for p in row] for row in m]


def hard_counts(seqs, paths, N, M):
    """Return the counts (n_pi, n_A, n_B) of starts, transitions and emissions on the paths."""
    n_pi = [0] * N
    n_A = [[0] * N for _ in range(N)]
    n_B = [[0] * M for _ in range(N)]
    for obs, q in zip(seqs, paths):
        n_pi[q[0]] += 1
        for t in range(len(obs)):
            n_B[q[t]][obs[t]] += 1
            if t > 0:
                n_A[q[t - 1]][q[t]] += 1
    return n_pi, n_A, n_B


def normalize_counts(counts, pi, A, B):
    """Return (pi, A, B) as relative frequencies; a row with no counts keeps its old values."""
    n_pi, n_A, n_B = counts

    def norm(row, old):
        s = sum(row)
        return [c / s for c in row] if s > 0 else list(old)

    return norm(n_pi, pi), [norm(r, o) for r, o in zip(n_A, A)], [norm(r, o) for r, o in zip(n_B, B)]


def reestimate(seqs, paths, pi, A, B):
    """Return (pi, A, B) from the hard counts along the given paths."""
    return normalize_counts(hard_counts(seqs, paths, len(pi), len(B[0])), pi, A, B)


def uniform_segmentation_start(seqs, N, M):
    """Return a left-to-right start model from equal segments of each sequence.

    Sequence t = 0..T-1 goes to state floor(N t / T). The transition rows allow
    only a self loop and a move to the next state, so zeros of this topology
    stay zero during training. Every sequence needs at least N frames.
    """
    paths = [[N * t // len(o) for t in range(len(o))] for o in seqs]
    flat_A = [[0.5 if j in (i, i + 1) else 0.0 for j in range(N)] for i in range(N)]
    flat_A[N - 1][N - 1] = 1.0
    flat_B = [[1.0 / M] * M for _ in range(N)]
    pi = [1.0] + [0.0] * (N - 1)
    return reestimate(seqs, paths, pi, flat_A, flat_B)


def viterbi_training(seqs: Sequence[Sequence[int]], pi, A, B, max_rounds: int = 100, tol: float = 1e-12):
    """Run Viterbi training from (pi, A, B).

    Return (pi, A, B, history) where history[k] is the objective F after the
    alignment of round k + 1. Stop when F does not grow by more than tol, or
    after max_rounds rounds. Raise ValueError if a sequence has probability 0.
    """
    pi, A, B = list(pi), [list(r) for r in A], [list(r) for r in B]
    history: List[float] = []
    F_old = NEG_INF  # @line L1
    for _ in range(max_rounds):  # @line L2
        lp, lA, lB = [safe_log(p) for p in pi], _logs(A), _logs(B)
        paths, F = [], 0.0
        for obs in seqs:  # @line L3
            q, s = viterbi_path(lp, lA, lB, obs)
            if s == NEG_INF:
                raise ValueError("a training sequence has probability 0")
            paths.append(q)
            F += s  # @line L4
        history.append(F)
        if F <= F_old + tol:  # @line L5
            break
        F_old = F  # @line L6
        counts = hard_counts(seqs, paths, len(pi), len(B[0]))  # @line L7
        pi, A, B = normalize_counts(counts, pi, A, B)  # @line L8
    return pi, A, B, history  # @line L9


def log_likelihood(seqs, pi, A, B):
    """Return sum over the sequences of log P(O | lambda), by the forward recursion."""
    lp, lA, lB = [safe_log(p) for p in pi], _logs(A), _logs(B)
    N = len(pi)
    total = 0.0
    for obs in seqs:
        a = [lp[j] + lB[j][obs[0]] for j in range(N)]
        for t in range(1, len(obs)):
            a = [log_sum(a[i] + lA[i][j] for i in range(N)) + lB[j][obs[t]] for j in range(N)]
        total += log_sum(a)
    return total
