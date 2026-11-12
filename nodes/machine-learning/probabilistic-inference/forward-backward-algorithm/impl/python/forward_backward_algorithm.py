# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-backward-algorithm/. The authors are listed in prov/JYNY94.jsonl.

"""The forward-backward algorithm for a discrete hidden Markov model (pi, A, B).

pi[i] = P(q_1 = i), A[i][j] = P(q_(t+1) = j | q_t = i), B[j][k] = P(o_t = k | q_t = j).
States are 0..N-1, symbols 0..M-1, and time indices in the code start at 0.
gamma[t][i] = P(q_t = i | O) and xi[t][i][j] = P(q_t = i, q_(t+1) = j | O).
"""

import math
from typing import Sequence


def forward_backward(pi: Sequence, A: Sequence[Sequence], B: Sequence[Sequence], obs: Sequence[int]):
    """Return (gamma, xi, P(O)) with plain (unscaled) recursions.

    Works with float or Fraction; with Fraction the result is exact.
    Precondition: obs is not empty and P(O) > 0 (else ValueError).
    Cost: O(T N^2) operations and O(T N) memory for alpha and beta.
    """
    n, T = len(pi), len(obs)
    if T == 0:
        raise ValueError("empty observation sequence")
    alpha = [[pi[j] * B[j][obs[0]] for j in range(n)]]  # @line L1: the forward pass
    for t in range(1, T):
        alpha.append([B[j][obs[t]] * sum(alpha[-1][i] * A[i][j] for i in range(n)) for j in range(n)])
    p = sum(alpha[-1])
    if p == 0:
        raise ValueError("the observation sequence has probability 0")
    beta = [None] * T
    beta[T - 1] = [type(p)(1)] * n  # @line L2: the number 1, in the number type of p
    for t in range(T - 2, -1, -1):  # @line L3
        nxt = beta[t + 1]
        beta[t] = [  # @line L4
            sum(A[i][j] * B[j][obs[t + 1]] * nxt[j] for j in range(n))  # @line L5
            for i in range(n)
        ]
    gamma = [[alpha[t][i] * beta[t][i] / p for i in range(n)] for t in range(T)]  # @line L6
    xi = [
        [[alpha[t][i] * A[i][j] * B[j][obs[t + 1]] * beta[t + 1][j] / p for j in range(n)] for i in range(n)]  # @line L7
        for t in range(T - 1)
    ]
    return gamma, xi, p  # @line L8


def forward_backward_scaled(pi: Sequence[float], A: Sequence[Sequence[float]], B: Sequence[Sequence[float]], obs: Sequence[int]):
    """Return (gamma, xi, log P(O)) with scaled recursions, safe for long sequences.

    The forward rows are normalized to sum 1 with n_t = P(o_t | o_1..o_(t-1)),
    and the backward rows are divided by the same n_(t+1).
    Precondition: obs is not empty and P(O) > 0 (else ValueError).
    Cost: O(T N^2) operations and O(T N) memory.
    """
    n, T = len(pi), len(obs)
    if T == 0:
        raise ValueError("empty observation sequence")
    ahat: list[list[float]] = []
    norms: list[float] = []
    for t, o in enumerate(obs):
        if t == 0:
            row = [pi[j] * B[j][o] for j in range(n)]
        else:
            row = [B[j][o] * sum(ahat[-1][i] * A[i][j] for i in range(n)) for j in range(n)]
        s = sum(row)
        if s == 0:
            raise ValueError("the observation sequence has probability 0")
        norms.append(s)
        ahat.append([x / s for x in row])
    bhat: list[list[float]] = [[1.0] * n for _ in range(T)]
    for t in range(T - 2, -1, -1):
        nxt, c = bhat[t + 1], norms[t + 1]
        bhat[t] = [sum(A[i][j] * B[j][obs[t + 1]] * nxt[j] for j in range(n)) / c for i in range(n)]
    gamma = [[ahat[t][i] * bhat[t][i] for i in range(n)] for t in range(T)]
    xi = [
        [[ahat[t][i] * A[i][j] * B[j][obs[t + 1]] * bhat[t + 1][j] / norms[t + 1] for j in range(n)] for i in range(n)]
        for t in range(T - 1)
    ]
    return gamma, xi, math.fsum(math.log(c) for c in norms)


def posterior_decode(gamma: Sequence[Sequence]) -> list[int]:
    """The state with the largest posterior at each step (smallest index on ties).

    This maximizes the expected number of correct states, but the sequence may
    use a transition of probability 0. It is not the Viterbi path.
    """
    return [max(range(len(g)), key=lambda i: (g[i], -i)) for g in gamma]
