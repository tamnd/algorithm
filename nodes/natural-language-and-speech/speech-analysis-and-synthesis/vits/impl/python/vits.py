# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vits/. The authors are listed in prov/HW04HE.jsonl.

"""Monotonic alignment search (MAS), the alignment step of Glow-TTS and VITS.

The network is not here. The code takes as given the n x T matrix v, where
v[i][j] is the log-likelihood of latent frame j under the prior of text
token i, and finds the monotonic alignment of the largest total score.

An alignment gives each frame j a token a(j) with a(0) = 0, a(T - 1) = n - 1
and a(j + 1) - a(j) in {0, 1}. So every token gets at least one frame and the
tokens are read in order. There are C(T - 1, n - 1) such alignments.

The dynamic program works in the Viterbi semiring (max, +):

    Q[i][j] = v[i][j] + max(Q[i][j - 1], Q[i - 1][j - 1])

Tie rule in the traceback: the path stays on the same token when the two
predecessors have equal scores, so an earlier token ends as early as possible.
"""

import math
from typing import List, Sequence, Tuple

NEG_INF = float("-inf")


def monotonic_alignment_search(v: Sequence[Sequence[float]]) -> Tuple[List[int], float]:
    """Return (a, score): a[j] is the token of frame j, score is the sum of v[a[j]][j].

    Raise ValueError if v is empty, ragged, or has fewer frames than tokens.
    """
    n = len(v)
    if n == 0:
        raise ValueError("there must be at least one token")
    T = len(v[0])
    if any(len(row) != T for row in v):
        raise ValueError("every row must have T entries")
    if T < n:
        raise ValueError("there must be at least as many frames as tokens")
    Q = [[NEG_INF] * T for _ in range(n)]  # @line L1
    Q[0][0] = v[0][0]  # @line L2
    for j in range(1, T):  # @line L3
        for i in range(0, min(j, n - 1) + 1):  # @line L4
            stay = Q[i][j - 1]
            move = Q[i - 1][j - 1] if i > 0 else NEG_INF
            Q[i][j] = v[i][j] + max(stay, move)  # @line L5
    a = [0] * T
    i = n - 1  # @line L6
    for j in range(T - 1, -1, -1):  # @line L7
        a[j] = i  # @line L8
        if j > 0 and i > 0 and Q[i - 1][j - 1] > Q[i][j - 1]:  # @line L9
            i -= 1  # @line L10
    return a, Q[n - 1][T - 1]  # @line L11


def durations(a: Sequence[int], n: int) -> List[int]:
    """The number of frames of each token under the alignment a."""
    d = [0] * n
    for i in a:
        d[i] += 1
    return d


def gaussian_log_likelihoods(mu: Sequence[Sequence[float]], sigma: Sequence[Sequence[float]],
                             z: Sequence[Sequence[float]]) -> List[List[float]]:
    """v[i][j] = log N(z_j; mu_i, diag(sigma_i^2)) for n tokens and T frames of width d."""
    v = []
    for m, s in zip(mu, sigma):
        row = []
        for frame in z:
            ll = 0.0
            for x, mk, sk in zip(frame, m, s):
                ll += -0.5 * math.log(2.0 * math.pi * sk * sk) - (x - mk) ** 2 / (2.0 * sk * sk)
            row.append(ll)
        v.append(row)
    return v
