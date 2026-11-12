# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-sum-decoding/. The authors are listed in prov/TA9NEY.jsonl.

"""Min-sum decoding of a binary linear code on its Tanner graph, with the
normalized and offset corrections of Chen and Fossorier (2002).

LLRs are L = ln P(c = 0 | y) / P(c = 1 | y); H is a list of rows of 0 and 1.
The check rule keeps the sign product of the tanh rule and replaces the
magnitude by the least incoming magnitude. The schedule is flooding.
"""

from typing import List, Sequence, Tuple

BIG = 1e9  # the message of a check with one edge, which forces its bit to 0


def check_message(others: Sequence[float], mode: str, alpha: float, beta: float) -> float:
    """sign product times the least magnitude, then the correction."""
    sign = 1.0
    least = BIG
    for x in others:
        if x < 0:
            sign = -sign
        least = min(least, abs(x))
    if mode == "normalized":
        least *= alpha
    elif mode == "offset":
        least = max(least - beta, 0.0)
    return sign * least


def min_sum_decode(h: Sequence[Sequence[int]], llr: Sequence[float], max_iter: int,
                   mode: str = "plain", alpha: float = 0.8, beta: float = 0.15,
                   early_stop: bool = True) -> Tuple[List[int], List[float], int, bool]:
    """Return (decision, posterior values, iterations used, syndrome is zero).

    mode is "plain", "normalized" (multiply by alpha) or "offset" (subtract
    beta, floor at zero). Cost Theta(E) per iteration for E edges: each check
    keeps its two least magnitudes, so the outgoing message to the holder of
    the least one uses the second least.
    """
    m, n = len(h), len(llr)
    chk = [[j for j in range(n) if h[i][j]] for i in range(m)]
    var = [[i for i in range(m) if h[i][j]] for j in range(n)]
    v2c = {(i, j): float(llr[j]) for i in range(m) for j in chk[i]}  # @line L1
    c2v = {e: 0.0 for e in v2c}
    post = [float(x) for x in llr]
    bits = [0 if x >= 0 else 1 for x in post]
    it = 0
    for it in range(1, max_iter + 1):  # @line L2
        for i in range(m):
            row = [v2c[(i, j)] for j in chk[i]]
            sign = 1.0
            for x in row:
                if x < 0:
                    sign = -sign
            mags = [abs(x) for x in row]
            a = min(range(len(mags)), key=mags.__getitem__) if mags else 0  # @line L3
            m1 = mags[a] if mags else BIG
            m2 = min((mags[b] for b in range(len(mags)) if b != a), default=BIG)
            for b, j in enumerate(chk[i]):
                least = m2 if b == a else m1
                s = -sign if row[b] < 0 else sign  # @line L4
                if mode == "normalized":
                    least *= alpha
                elif mode == "offset":
                    least = max(least - beta, 0.0)
                c2v[(i, j)] = s * least  # @line L5
        post = [llr[j] + sum(c2v[(i, j)] for i in var[j]) for j in range(n)]  # @line L6
        bits = [0 if x >= 0 else 1 for x in post]
        ok = all(sum(bits[j] for j in chk[i]) % 2 == 0 for i in range(m))
        if ok and early_stop:  # @line L7
            return bits, post, it, True
        for (i, j) in v2c:
            v2c[(i, j)] = post[j] - c2v[(i, j)]  # @line L8
    ok = all(sum(bits[j] for j in chk[i]) % 2 == 0 for i in range(m))
    return bits, post, it, ok  # @line L9
