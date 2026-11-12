# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/viterbi-algorithm/. The authors are listed in prov/KSAB3R.jsonl.

"""The Viterbi algorithm for a discrete hidden Markov model, in log space.

pi[i] = P(q_1 = i), A[i][j] = P(q_(t+1) = j | q_t = i), B[j][k] = P(o_t = k | q_t = j).
States are 0..N-1 and time indices in the code start at 0.

Tie rule: line L4 and line L6 take the smallest index among the maximizers.
The returned path is then the optimal path whose reversed sequence
(q_T, q_(T-1), ..., q_1) is the smallest in lexicographic order.
"""

import math
from typing import Sequence

NEG_INF = -math.inf


def viterbi_log(log_pi: Sequence, log_A: Sequence[Sequence], log_B: Sequence[Sequence], obs: Sequence[int]):
    """Return (path, score) that maximizes log_pi[q_1] + log_B[q_1][o_1] + sum (log_A + log_B).

    The weights may be any numbers with + and < (float, int, Fraction), and
    -inf stands for a probability of 0. Raises ValueError if obs is empty or
    every path has score -inf. Cost: O(T N^2) time, O(T N) memory for the
    backpointers.
    """
    n, T = len(log_pi), len(obs)
    if T == 0:
        raise ValueError("empty observation sequence")
    delta = [log_pi[j] + log_B[j][obs[0]] for j in range(n)]  # @line L1
    psi: list[list[int]] = [[0] * n]
    for t in range(1, T):  # @line L2
        new, back = [], []
        for j in range(n):  # @line L3
            best_i = 0
            for i in range(1, n):  # @line L4: strict > keeps the smallest maximizer
                if delta[i] + log_A[i][j] > delta[best_i] + log_A[best_i][j]:
                    best_i = i
            back.append(best_i)
            new.append(delta[best_i] + log_A[best_i][j] + log_B[j][obs[t]])  # @line L5
        delta = new
        psi.append(back)
    last = 0
    for j in range(1, n):  # @line L6
        if delta[j] > delta[last]:
            last = j
    if delta[last] == NEG_INF:
        raise ValueError("every state path has probability 0")
    path = [last]
    for t in range(T - 1, 0, -1):  # @line L7
        path.append(psi[t][path[-1]])
    path.reverse()
    return path, delta[last]  # @line L8


def _log(p) -> float:
    return math.log(p) if p > 0 else NEG_INF


def viterbi(pi: Sequence, A: Sequence[Sequence], B: Sequence[Sequence], obs: Sequence[int]):
    """Return (path, log P(path, O)) for the most likely state path of the HMM."""
    return viterbi_log([_log(p) for p in pi], [[_log(p) for p in r] for r in A], [[_log(p) for p in r] for r in B], obs)
