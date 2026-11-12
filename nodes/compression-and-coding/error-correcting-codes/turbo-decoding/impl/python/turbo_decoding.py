# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/turbo-decoding/. The authors are listed in prov/SCF5ND.jsonl.

"""Iterative decoding of a rate 1/3 turbo code with two log-MAP BCJR decoders.

LLRs are L = ln P(bit = 0) / P(bit = 1); BPSK sends x = 1 - 2c, and on AWGN
with noise variance s^2 the channel LLR is 2 y / s^2. Both constituent codes
are the same recursive systematic code (1, ff/fb) with K - 1 tail steps each.
Taps are octal masks with the D^0 tap as the leftmost of K binary digits.
"""

import math
from typing import Dict, List, Sequence, Tuple

NEG = float("-inf")


def _max_star(a: float, b: float) -> float:
    if a == NEG:
        return b
    if b == NEG:
        return a
    return max(a, b) + math.log1p(math.exp(-abs(a - b)))


def rsc_trellis(fb: int, ff: int, k: int) -> List[Tuple[int, int, int, int]]:
    """All edges (state, input u, next state, parity) of the RSC encoder."""
    edges = []
    for s in range(1 << (k - 1)):
        for u in (0, 1):
            a = (u + bin(fb & s).count("1")) & 1
            w = (a << (k - 1)) | s
            edges.append((s, u, w >> 1, bin(ff & w).count("1") & 1))
    return edges


def encode(bits: Sequence[int], perm: Sequence[int], fb: int, ff: int, k: int) -> Dict[str, List[int]]:
    """Rate 1/3 turbo encoder. Each stream includes its K - 1 tail steps:
    sys1/par1 for encoder 1 on the bits, sys2/par2 for encoder 2 on the
    interleaved bits c'_i = c_perm(i); sys2 is sent only for the tail."""
    out: Dict[str, List[int]] = {}
    for name, seq in (("1", list(bits)), ("2", [bits[p] for p in perm])):
        state, us, ps = 0, [], []
        for u in seq:
            a = (u + bin(fb & state).count("1")) & 1
            w = (a << (k - 1)) | state
            us.append(u)
            ps.append(bin(ff & w).count("1") & 1)
            state = w >> 1
        for _ in range(k - 1):
            u = bin(fb & state).count("1") & 1
            us.append(u)
            ps.append(bin(ff & state).count("1") & 1)
            state >>= 1
        out["sys" + name], out["par" + name] = us, ps
    return out


def log_map(edges: List[Tuple[int, int, int, int]], nstates: int, ls: Sequence[float],
            lp: Sequence[float], la: Sequence[float]) -> List[float]:
    """Log-MAP BCJR on a terminated RSC trellis. ls, lp: channel LLRs of the
    systematic and parity bits for every step (tail included); la: a priori
    LLRs of the inputs (0 for the tail). Returns posterior input LLRs."""
    t_len = len(ls)
    gam = [[0.5 * ((1 - 2 * u) * (ls[t] + la[t]) + (1 - 2 * p) * lp[t]) for (_, u, _, p) in edges]
           for t in range(t_len)]
    alpha = [[NEG] * nstates for _ in range(t_len + 1)]
    alpha[0][0] = 0.0
    for t in range(t_len):
        a, nxt = alpha[t], alpha[t + 1]
        for (s, _, s2, _), g in zip(edges, gam[t]):
            if a[s] != NEG:
                nxt[s2] = _max_star(nxt[s2], a[s] + g)
    beta = [[NEG] * nstates for _ in range(t_len + 1)]
    beta[t_len][0] = 0.0
    for t in range(t_len - 1, -1, -1):
        b, cur = beta[t + 1], beta[t]
        for (s, _, s2, _), g in zip(edges, gam[t]):
            if b[s2] != NEG:
                cur[s] = _max_star(cur[s], g + b[s2])
    post = []
    for t in range(t_len):
        p = [NEG, NEG]
        for (s, u, s2, _), g in zip(edges, gam[t]):
            if alpha[t][s] != NEG and beta[t + 1][s2] != NEG:
                p[u] = _max_star(p[u], alpha[t][s] + g + beta[t + 1][s2])
        post.append(p[0] - p[1])
    return post


def turbo_decode(ch: Dict[str, Sequence[float]], perm: Sequence[int], fb: int, ff: int, k: int,
                 iterations: int) -> List[List[int]]:
    """Decode; return the hard decisions after each iteration.

    ch holds the channel LLRs of the streams of encode(). Cost: Theta(I K 2^k)
    max* operations for I iterations and K message bits.
    """
    n = len(perm)
    edges = rsc_trellis(fb, ff, k)
    ns = 1 << (k - 1)
    tail = k - 1
    lsys = list(ch["sys1"][:n])
    lsys_pi = [lsys[perm[i]] for i in range(n)] + list(ch["sys2"][n:])
    la1 = [0.0] * n  # @line L1
    history = []
    for _ in range(iterations):  # @line L2
        post1 = log_map(edges, ns, ch["sys1"], ch["par1"], la1 + [0.0] * tail)  # @line L3
        le1 = [post1[i] - la1[i] - lsys[i] for i in range(n)]  # @line L4
        la2 = [le1[perm[i]] for i in range(n)]  # @line L5
        post2 = log_map(edges, ns, lsys_pi, ch["par2"], la2 + [0.0] * tail)  # @line L6
        le2 = [post2[i] - la2[i] - lsys_pi[i] for i in range(n)]  # @line L7
        la1 = [0.0] * n
        for i in range(n):
            la1[perm[i]] = le2[i]  # @line L8
        final = [0.0] * n
        for i in range(n):
            final[perm[i]] = post2[i]
        history.append([0 if v >= 0 else 1 for v in final])  # @line L9
    return history
