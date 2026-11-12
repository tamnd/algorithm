# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-algorithm/. The authors are listed in prov/T75G2W.jsonl.

"""The forward algorithm for a discrete hidden Markov model (pi, A, B).

pi[i] is P(q_1 = i), A[i][j] is P(q_{t+1} = j | q_t = i) and B[j][k] is
P(o_t = k | q_t = j). States are 0..N-1 and symbols are 0..M-1.
"""

import math
from typing import Sequence


def forward(pi: Sequence, A: Sequence[Sequence], B: Sequence[Sequence], obs: Sequence[int]):
    """Return (alpha, P(O)), where alpha[t][j] = P(o_1..o_(t+1), q_(t+1) = j).

    Works with any number type that has + and * (float, Fraction).
    Cost: O(T N^2) operations and O(T N) memory. With floats the values
    underflow for long sequences; use forward_scaled for those.
    For an empty sequence, P(O) = 1.
    """
    n = len(pi)
    if not obs:
        return [], 1
    alpha = [[pi[j] * B[j][obs[0]] for j in range(n)]]  # @line L1
    for t in range(1, len(obs)):  # @line L2
        prev, row = alpha[-1], []
        for j in range(n):  # @line L3
            s = 0  # @line L4
            for i in range(n):  # @line L5
                s = s + prev[i] * A[i][j]
            row.append(B[j][obs[t]] * s)  # @line L6
        alpha.append(row)
    return alpha, sum(alpha[-1])  # @line L7


def forward_scaled(pi: Sequence[float], A: Sequence[Sequence[float]], B: Sequence[Sequence[float]], obs: Sequence[int]):
    """Return (alpha_hat, norms, log P(O)).

    alpha_hat[t][j] = P(q_(t+1) = j | o_1..o_(t+1)), the filtered distribution,
    and norms[t] = P(o_(t+1) | o_1..o_t), so log P(O) = sum of log norms[t].
    Rabiner's scale factor c_t is 1 / norms[t]. If the sequence has
    probability 0, the result stops at the first zero norm and log P(O) = -inf.
    Cost: O(T N^2) operations and O(T N) memory.
    """
    n = len(pi)
    alpha_hat: list[list[float]] = []
    norms: list[float] = []
    log_p = 0.0
    for t, o in enumerate(obs):  # @line L8
        if t == 0:
            row = [pi[j] * B[j][o] for j in range(n)]  # @line L9
        else:
            prev = alpha_hat[-1]
            row = [B[j][o] * sum(prev[i] * A[i][j] for i in range(n)) for j in range(n)]  # @line L10
        s = sum(row)  # @line L11
        if s == 0:
            return alpha_hat, norms, -math.inf
        alpha_hat.append([x / s for x in row])  # @line L12
        norms.append(s)
        log_p += math.log(s)  # @line L13
    return alpha_hat, norms, log_p


def _log(x: float) -> float:
    return math.log(x) if x > 0 else -math.inf


def _log_sum_exp(xs: Sequence[float]) -> float:
    m = max(xs)
    if m == -math.inf:
        return -math.inf
    return m + math.log(sum(math.exp(x - m) for x in xs))


def forward_log(pi: Sequence[float], A: Sequence[Sequence[float]], B: Sequence[Sequence[float]], obs: Sequence[int]) -> float:
    """Return log P(O) with the forward recursion in log space (log-sum-exp).

    Cost: O(T N^2) operations, each with one exp, and O(N) memory.
    """
    n = len(pi)
    if not obs:
        return 0.0
    la = [_log(pi[j]) + _log(B[j][obs[0]]) for j in range(n)]
    for o in obs[1:]:
        la = [_log(B[j][o]) + _log_sum_exp([la[i] + _log(A[i][j]) for i in range(n)]) for j in range(n)]
    return _log_sum_exp(la)
