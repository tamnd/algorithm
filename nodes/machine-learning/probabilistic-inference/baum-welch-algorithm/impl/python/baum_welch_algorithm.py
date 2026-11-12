# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baum-welch-algorithm/. The authors are listed in prov/X13Y7R.jsonl.

"""The Baum-Welch algorithm: EM for the parameters of a discrete HMM.

pi[i] = P(q_1 = i), A[i][j] = P(q_(t+1) = j | q_t = i), B[j][k] = P(o_t = k | q_t = j).
The input is a list of observation sequences, each a list of symbols 0..M-1.
"""

import math
import random
from typing import Sequence

Matrix = list[list[float]]


def posteriors(pi: Sequence[float], A: Sequence[Sequence[float]], B: Sequence[Sequence[float]], obs: Sequence[int]):
    """Scaled forward-backward. Return (gamma, xi_sum, log P(O)).

    gamma[t][i] = P(q_t = i | O); xi_sum[i][j] = sum over t of P(q_t = i, q_(t+1) = j | O).
    Raises ValueError if P(O) = 0. Cost: O(T N^2).
    """
    n, T = len(pi), len(obs)
    ahat: Matrix = []
    norms: list[float] = []
    for t, o in enumerate(obs):
        if t == 0:
            row = [pi[j] * B[j][o] for j in range(n)]
        else:
            row = [B[j][o] * sum(ahat[-1][i] * A[i][j] for i in range(n)) for j in range(n)]
        s = sum(row)
        if s == 0:
            raise ValueError("a sequence has probability 0 under the current parameters")
        norms.append(s)
        ahat.append([x / s for x in row])
    bhat: Matrix = [[1.0] * n for _ in range(T)]
    for t in range(T - 2, -1, -1):
        c = norms[t + 1]
        bhat[t] = [sum(A[i][j] * B[j][obs[t + 1]] * bhat[t + 1][j] for j in range(n)) / c for i in range(n)]
    gamma = [[ahat[t][i] * bhat[t][i] for i in range(n)] for t in range(T)]
    xi_sum = [[0.0] * n for _ in range(n)]
    for t in range(T - 1):
        c = norms[t + 1]
        for i in range(n):
            for j in range(n):
                xi_sum[i][j] += ahat[t][i] * A[i][j] * B[j][obs[t + 1]] * bhat[t + 1][j] / c
    return gamma, xi_sum, math.fsum(math.log(c) for c in norms)


def _normalize(row: list[float], old: Sequence[float]) -> list[float]:
    s = math.fsum(row)
    return [x / s for x in row] if s > 0 else list(old)  # a state with no expected visits keeps its row


def baum_welch_step(pi: Sequence[float], A: Sequence[Sequence[float]], B: Sequence[Sequence[float]], seqs: Sequence[Sequence[int]]):
    """One EM round. Return (new_pi, new_A, new_B, total log-likelihood under the OLD parameters).

    Cost: O(L N^2 + N M) time for L symbols in total, O(T N + N M) memory for a longest sequence of length T.
    """
    n, m = len(pi), len(B[0])
    s = [0.0] * n
    e = [[0.0] * n for _ in range(n)]
    f = [[0.0] * m for _ in range(n)]
    total = 0.0
    for obs in seqs:  # @line L2
        gamma, xi_sum, lp = posteriors(pi, A, B, obs)  # @line L3
        total += lp
        for i in range(n):  # @line L4: add the expected counts
            s[i] += gamma[0][i]
            for j in range(n):
                e[i][j] += xi_sum[i][j]
        for t, o in enumerate(obs):
            for j in range(n):
                f[j][o] += gamma[t][j]
    new_pi = _normalize(s, pi)  # @line L5: equals s_i / R
    new_A = [_normalize(e[i], A[i]) for i in range(n)]  # @line L6
    new_B = [_normalize(f[j], B[j]) for j in range(n)]  # @line L7
    return new_pi, new_A, new_B, total


def baum_welch(pi, A, B, seqs, iterations: int = 100, tol: float = 1e-10):
    """Run EM rounds until the gain in log-likelihood is below tol or after `iterations` rounds.

    Return (pi, A, B, history), where history[k] is the total log-likelihood of the
    parameters before round k+1, and history[-1] is that of the returned parameters.
    The history never decreases (up to rounding); the end point is in general a local maximum.
    """
    history: list[float] = []
    pi, A, B = list(pi), [list(r) for r in A], [list(r) for r in B]
    for _ in range(iterations):  # @line L1
        new_pi, new_A, new_B, ll = baum_welch_step(pi, A, B, seqs)
        history.append(ll)
        pi, A, B = new_pi, new_A, new_B
        if len(history) >= 2 and history[-1] - history[-2] < tol:
            break
    history.append(sum(posteriors(pi, A, B, o)[2] for o in seqs))
    return pi, A, B, history  # @line L8


def random_parameters(n: int, m: int, rng: random.Random):
    """Random strictly positive stochastic (pi, A, B), a usual starting point for EM."""

    def row(k: int) -> list[float]:
        w = [rng.uniform(0.5, 1.5) for _ in range(k)]
        s = sum(w)
        return [x / s for x in w]

    return row(n), [row(n) for _ in range(n)], [row(m) for _ in range(n)]
