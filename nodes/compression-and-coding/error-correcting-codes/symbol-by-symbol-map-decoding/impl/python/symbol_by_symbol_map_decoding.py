# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symbol-by-symbol-map-decoding/. The authors are listed in prov/M3KJWK.jsonl.

"""Bitwise MAP decoding against block MAP (ML) decoding, by brute force.

A code is a list of codewords (tuples of bits), sent with equal prior
probability over a memoryless binary input channel. The channel is given by
the LLRs L_j = ln p(y_j | 0) / p(y_j | 1). Then
P(c | y) is proportional to exp(sum_j (1 - 2 c_j) L_j / 2).
These functions take time Theta(|C| n); they define the targets that trellis
and graph decoders (BCJR, belief propagation) compute faster.
"""

import itertools
import math
from typing import Dict, List, Sequence, Tuple

Word = Tuple[int, ...]


def _log_weight(c: Word, llr: Sequence[float]) -> float:
    return 0.5 * sum((1 - 2 * b) * l for b, l in zip(c, llr))


def bitwise_map(code: Sequence[Word], llr: Sequence[float]) -> Tuple[List[int], List[float]]:
    """The a posteriori LLR of each position and the bitwise MAP decision
    (0 when the LLR is >= 0). The decision vector need not be a codeword."""
    w = [_log_weight(c, llr) for c in code]
    top = max(w)
    post = []
    for i in range(len(code[0])):
        p0 = math.fsum(math.exp(x - top) for c, x in zip(code, w) if c[i] == 0)
        p1 = math.fsum(math.exp(x - top) for c, x in zip(code, w) if c[i] == 1)
        post.append(math.inf if p1 == 0 else (-math.inf if p0 == 0 else math.log(p0 / p1)))
    return [0 if v >= 0 else 1 for v in post], post


def block_map(code: Sequence[Word], llr: Sequence[float]) -> Word:
    """The codeword of largest posterior (ties to the first in the list).
    With equal priors this is ML decoding."""
    best = max(range(len(code)), key=lambda j: (_log_weight(code[j], llr), -j))
    return code[best]


def exact_rates_bsc(code: Sequence[Word], p: float) -> Dict[str, float]:
    """Exact bit and word error rates of both decoders on BSC(p), 0 < p < 1/2,
    averaged over the codewords and all 2^n error patterns."""
    n = len(code[0])
    lam = math.log((1 - p) / p)
    acc = {"map_ber": 0.0, "map_wer": 0.0, "ml_ber": 0.0, "ml_wer": 0.0}
    for c in code:
        for e in itertools.product((0, 1), repeat=n):
            y = [a ^ b for a, b in zip(c, e)]
            pr = p ** sum(e) * (1 - p) ** (n - sum(e))
            llr = [lam if b == 0 else -lam for b in y]
            m, _ = bitwise_map(code, llr)
            d = block_map(code, llr)
            bm = sum(a != b for a, b in zip(m, c))
            bd = sum(a != b for a, b in zip(d, c))
            acc["map_ber"] += pr * bm / n
            acc["ml_ber"] += pr * bd / n
            acc["map_wer"] += pr * (bm > 0)
            acc["ml_wer"] += pr * (bd > 0)
    return {k: v / len(code) for k, v in acc.items()}


def linear_code(g: Sequence[Sequence[int]]) -> List[Word]:
    """All codewords m G of a binary generator matrix, in the order of m."""
    n = len(g[0])
    return [tuple(sum(m[r] * g[r][j] for r in range(len(g))) % 2 for j in range(n))
            for m in itertools.product((0, 1), repeat=len(g))]
