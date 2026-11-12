# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hidden-semi-markov-model/. The authors are listed in prov/YCP2N2.jsonl.

"""The forward recursion of an explicit-duration hidden semi-Markov model.

States are 0..N-1, symbols 0..M-1, durations 1..D.
pi[j]       P(the first segment has state j)
A[i][j]     P(the next segment has state j | this segment has state i), with A[i][i] = 0
P[j][d-1]   P(a segment of state j lasts d steps), d = 1..D
B[j][k]     P(symbol k | state j); the symbols of one segment are independent given its state

The numbers may be floats or fractions.Fraction. Times in the comments run 1..T.
"""

import math
from typing import Sequence

NEG_INF = -math.inf


def validate(pi, A, P, B) -> None:
    n = len(pi)
    if not (len(A) == len(P) == len(B) == n) or any(A[i][i] != 0 for i in range(n)):
        raise ValueError("need N rows in A, P and B, and A[i][i] = 0 (a state change at each segment end)")


def forward(pi: Sequence, A: Sequence[Sequence], P: Sequence[Sequence], B: Sequence[Sequence], obs: Sequence[int]):
    """Return (alpha, p_end, p_censored).

    alpha[t-1][j] = P(o_1..o_t, a segment of state j ends at time t).
    p_end         = P(o_1..o_T, the last segment ends exactly at T) = sum_j alpha_T(j).
    p_censored    = P(o_1..o_T): the last segment may go on after T, so it uses the
                    survival S_j(d) = P(duration >= d) in place of P_j(d).

    The segment-start term s_t(j) = sum_i alpha_(t-1)(i) A[i][j] is computed once per t and
    the emission product is extended one step at a time, so the cost is
    O(T N^2 + T N D) time and O(T N) memory.
    """
    n, T = len(pi), len(obs)
    if T == 0:
        raise ValueError("empty observation sequence")
    D = max(len(row) for row in P)
    surv = []
    for row in P:  # S_j(d) = sum over d' >= d of P_j(d')
        s, acc = [], 0
        for x in reversed(row):
            acc = acc + x
            s.append(acc)
        surv.append(s[::-1])
    zero = pi[0] * 0
    start: list[list] = []  # start[t-1][j] = P(o_1..o_(t-1), a segment of j starts at t)
    alpha: list[list] = []
    p_cens = zero
    for t in range(1, T + 1):
        if t == 1:
            start.append(list(pi))
        else:
            prev = alpha[t - 2]
            start.append([sum((prev[i] * A[i][j] for i in range(n)), zero) for j in range(n)])
        row = []
        for j in range(n):
            total = zero
            emit = 1
            for d in range(1, min(D, t) + 1):  # the segment covers times t-d+1 .. t
                emit = emit * B[j][obs[t - d]]
                if emit == 0:
                    break
                s = start[t - d][j]
                if d <= len(P[j]):
                    total = total + s * P[j][d - 1] * emit
                    if t == T:
                        p_cens = p_cens + s * surv[j][d - 1] * emit
            row.append(total)
        alpha.append(row)
    return alpha, sum(alpha[-1], zero), p_cens


def _lse(xs: list[float]) -> float:
    m = max(xs, default=NEG_INF)
    if m == NEG_INF:
        return NEG_INF
    return m + math.log(math.fsum(math.exp(x - m) for x in xs))


def _log(x: float) -> float:
    return math.log(x) if x > 0 else NEG_INF


def forward_log(pi, A, P, B, obs: Sequence[int]):
    """The same recursion in log space, for long sequences. Return (log p_end, log p_censored)."""
    n, T = len(pi), len(obs)
    if T == 0:
        raise ValueError("empty observation sequence")
    lA = [[_log(x) for x in r] for r in A]
    lB = [[_log(x) for x in r] for r in B]
    lP = [[_log(x) for x in r] for r in P]
    lS = []
    for row in P:
        s, acc = [], 0.0
        for x in reversed(row):
            acc += x
            s.append(_log(acc))
        lS.append(s[::-1])
    start: list[list[float]] = []
    alpha: list[list[float]] = []
    cens: list[float] = []
    for t in range(1, T + 1):
        if t == 1:
            start.append([_log(x) for x in pi])
        else:
            prev = alpha[t - 2]
            start.append([_lse([prev[i] + lA[i][j] for i in range(n)]) for j in range(n)])
        row = []
        for j in range(n):
            terms = []
            emit = 0.0
            for d in range(1, min(len(P[j]), t) + 1):
                emit += lB[j][obs[t - d]]
                if emit == NEG_INF:
                    break
                terms.append(start[t - d][j] + lP[j][d - 1] + emit)
                if t == T:
                    cens.append(start[t - d][j] + lS[j][d - 1] + emit)
            row.append(_lse(terms))
        alpha.append(row)
    return _lse(alpha[-1]), _lse(cens)


def from_hmm(pi, A, B, D: int):
    """An HSMM that matches the HMM (pi, A, B) on sequences of length T.

    For T <= D the censored likelihood equals the HMM likelihood P(O). For T < D also
    p_end equals P(O, the HMM changes state after time T). A stay in state j of the HMM lasts d steps with the geometric probability
    a^(d-1) (1 - a), a = A[j][j]. The last entry P_j(D) = a^(D-1) holds the whole
    tail, so P_j sums to 1 and S_j(d) = a^(d-1) for d <= D. The next segment state
    is drawn from the off-diagonal part of row j, rescaled: A'[j][k] = A[j][k] / (1 - a).
    Needs A[j][j] < 1 for every j.
    """
    n = len(pi)
    P, A2 = [], []
    for j in range(n):
        a = A[j][j]
        P.append([a ** (d - 1) * (1 - a) for d in range(1, D)] + [a ** (D - 1)])
        A2.append([0 * a if k == j else A[j][k] / (1 - a) for k in range(n)])
    return list(pi), A2, P, [list(r) for r in B]
