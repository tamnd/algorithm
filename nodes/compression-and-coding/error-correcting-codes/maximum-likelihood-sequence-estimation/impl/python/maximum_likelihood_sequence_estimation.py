# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-sequence-estimation/. The authors are listed in prov/FM9AE7.jsonl.

"""Maximum likelihood sequence estimation with the Viterbi algorithm.

Two uses: decoding a rate 1/n feedforward convolutional code (generators in
octal, D^0 tap leftmost, constraint length K = memory + 1), and equalizing a
binary intersymbol interference channel y_t = sum_j h_j x_(t-j) + noise.
BPSK maps a code bit c to x = 1 - 2c.
"""

import math
from typing import List, Optional, Sequence, Tuple

INF = float("inf")


def _step(state: int, u: int, gens: Sequence[int], k: int) -> Tuple[int, Tuple[int, ...]]:
    w = (u << (k - 1)) | state
    return w >> 1, tuple(bin(g & w).count("1") & 1 for g in gens)


def conv_encode(bits: Sequence[int], gens: Sequence[int], k: int) -> List[int]:
    """Terminated encoding: the bits, then K - 1 zeros."""
    s, out = 0, []
    for u in list(bits) + [0] * (k - 1):
        s, o = _step(s, u, gens, k)
        out.extend(o)
    return out


def branch_metric(r: Sequence[float], out: Sequence[int], soft: bool) -> float:
    """Hard: Hamming distance to the received bits. Soft: squared Euclidean
    distance from the received values to the BPSK points 1 - 2c."""
    if soft:
        return sum((y - (1 - 2 * c)) ** 2 for y, c in zip(r, out))
    return sum(int(y) != c for y, c in zip(r, out))


def viterbi_decode(r: Sequence[float], gens: Sequence[int], k: int, soft: bool = True,
                   depth: Optional[int] = None) -> List[int]:
    """Viterbi decoding of a terminated rate 1/n code.

    r holds n received values per trellis step (hard bits or real samples).
    Returns the message bits of the most likely path (ties to the lower
    state). With depth = D, bit t is decided at time t + D from the best state
    of that time (truncated traceback); with None, one traceback at the end.
    Cost: Theta(T 2^K n) time for T steps, Theta(T 2^(K-1)) space.
    """
    n = len(gens)
    steps = len(r) // n
    nstates = 1 << (k - 1)
    metric = [0.0] + [INF] * (nstates - 1)  # @line L1
    surv: List[List[Tuple[int, int]]] = []
    decided: List[int] = []
    msg_len = steps - (k - 1)
    for t in range(steps):  # @line L2
        rt = r[n * t:n * t + n]
        inputs = (0,) if t >= msg_len else (0, 1)
        new = [INF] * nstates
        back = [(-1, -1)] * nstates
        for s in range(nstates):  # @line L3
            if metric[s] == INF:
                continue
            for u in inputs:
                ns, out = _step(s, u, gens, k)
                m = metric[s] + branch_metric(rt, out, soft)  # @line L4
                if m < new[ns]:  # @line L5
                    new[ns], back[ns] = m, (s, u)  # @line L6
        metric = new
        surv.append(back)
        if depth is not None and t >= depth and t - depth < msg_len:
            s = min(range(nstates), key=lambda x: metric[x])
            for j in range(t, t - depth, -1):
                s = surv[j][s][0]
            decided.append(surv[t - depth][s][1])
    s, bits = 0, []  # @line L7
    for t in range(steps - 1, -1, -1):  # @line L8
        p, u = surv[t][s]
        bits.append(u)
        s = p
    bits.reverse()
    if depth is None:
        return bits[:msg_len]
    return decided + bits[len(decided):msg_len]


def isi_mlse(y: Sequence[float], h: Sequence[float]) -> List[int]:
    """MLSE of x in {+1, -1}^T from y_t = sum_j h_j x_(t-j) + Gaussian noise,
    with x_t = +1 before time 0 (a known preamble). Viterbi over the
    2^(L-1) states of the last L - 1 symbols, L = len(h). Returns the bits
    b_t with x_t = 1 - 2 b_t. Cost: Theta(T 2^L L)."""
    mem = len(h) - 1
    nstates = 1 << mem
    metric = [0.0] + [INF] * (nstates - 1)
    surv = []
    for yt in y:
        new = [INF] * nstates
        back = [(-1, -1)] * nstates
        for s in range(nstates):
            if metric[s] == INF:
                continue
            for b in (0, 1):
                past = [(s >> j) & 1 for j in range(mem)]  # bit j = b_(t-1-j)
                mean = h[0] * (1 - 2 * b) + sum(h[j + 1] * (1 - 2 * past[j]) for j in range(mem))
                ns = ((s << 1) | b) & (nstates - 1)
                m = metric[s] + (yt - mean) ** 2
                if m < new[ns]:
                    new[ns], back[ns] = m, (s, b)
        metric = new
        surv.append(back)
    s = min(range(nstates), key=lambda x: metric[x])
    out = []
    for t in range(len(y) - 1, -1, -1):
        p, b = surv[t][s]
        out.append(b)
        s = p
    return out[::-1]


def q_function(x: float) -> float:
    """Gaussian tail Q(x) = P(N(0, 1) > x)."""
    return 0.5 * math.erfc(x / math.sqrt(2))


def union_bound_ber(spectrum: Sequence[Tuple[int, int]], rate: float, ebn0_db: float) -> float:
    """Union bound on the bit error rate of soft Viterbi decoding on BPSK
    AWGN: sum over d of B_d Q(sqrt(2 d R Eb/N0)), for k = 1 input bit per step."""
    g = 10 ** (ebn0_db / 10)
    return sum(b * q_function(math.sqrt(2 * d * rate * g)) for d, b in spectrum)
