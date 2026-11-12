# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belief-propagation-decoding/. The authors are listed in prov/RMPGHV.jsonl.

"""Sum-product (belief propagation) decoding of a binary linear code on its
Tanner graph, in the LLR domain with the tanh rule and a flooding schedule.

LLRs are L = ln P(c = 0 | y) / P(c = 1 | y). For BPSK x = 1 - 2c on AWGN
with noise variance s^2, the channel LLR is 2 y / s^2; on BSC(p) it is
+-ln((1 - p) / p). H is a list of rows of 0 and 1.
"""

import math
from typing import List, Sequence, Tuple

CLIP = 1 - 1e-15  # keeps atanh finite; messages stay below about 35 in size


def bp_decode(h: Sequence[Sequence[int]], llr: Sequence[float], max_iter: int,
              early_stop: bool = True) -> Tuple[List[int], List[float], int, bool]:
    """Return (decision, posterior LLRs, iterations used, syndrome is zero).

    Cost: Theta(sum over checks of degree^2) per iteration, which is
    Theta(E) for E edges (ones in H) when the degrees are bounded; so
    Theta(I E) for I iterations of an LDPC code. Theta(E) memory for the
    messages.
    """
    m, n = len(h), len(llr)
    chk = [[j for j in range(n) if h[i][j]] for i in range(m)]
    var = [[i for i in range(m) if h[i][j]] for j in range(n)]
    v2c = {(i, j): llr[j] for i in range(m) for j in chk[i]}  # @line L1
    c2v = {e: 0.0 for e in v2c}
    post = list(llr)
    bits = [0 if x >= 0 else 1 for x in post]
    it = 0
    for it in range(1, max_iter + 1):  # @line L2
        for i in range(m):
            t = [math.tanh(v2c[(i, j)] / 2) for j in chk[i]]
            for a, j in enumerate(chk[i]):
                prod = 1.0
                for b, x in enumerate(t):
                    if b != a:
                        prod *= x
                prod = max(-CLIP, min(CLIP, prod))
                c2v[(i, j)] = 2 * math.atanh(prod)  # @line L3
        post = [llr[j] + sum(c2v[(i, j)] for i in var[j]) for j in range(n)]  # @line L4
        bits = [0 if x >= 0 else 1 for x in post]  # @line L5
        ok = all(sum(bits[j] for j in chk[i]) % 2 == 0 for i in range(m))
        if ok and early_stop:  # @line L6
            return bits, post, it, True
        for (i, j) in v2c:
            v2c[(i, j)] = post[j] - c2v[(i, j)]  # @line L7
    ok = all(sum(bits[j] for j in chk[i]) % 2 == 0 for i in range(m))
    return bits, post, it, ok  # @line L8
