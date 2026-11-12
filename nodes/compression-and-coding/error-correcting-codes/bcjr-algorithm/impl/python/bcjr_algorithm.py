# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bcjr-algorithm/. The authors are listed in prov/PCHCXC.jsonl.

"""The BCJR algorithm on the trellis of a binary convolutional code.

LLRs are L = ln P(bit = 0) / P(bit = 1). On BPSK (x = 1 - 2c) over AWGN with
noise variance s^2, the channel LLR of a sample y is 2 y / s^2. The trellis
is a list of steps; a step is a list of edges (s, u, s2, out), where u is
the input bit and out the tuple of code bits on the edge.
"""

import math
from typing import List, Optional, Sequence, Tuple

Edge = Tuple[int, int, int, Tuple[int, ...]]
NEG = float("-inf")


def build_trellis(gens: Sequence[int], k: int, length: int, fb: Optional[int] = None,
                  terminate: bool = True) -> List[List[Edge]]:
    """Trellis of a rate 1/n code over length message steps, plus K - 1 tail
    steps if terminate. Feedforward when fb is None; otherwise recursive
    systematic with feedback taps fb, and out = (u, parities by gens).
    Taps are octal masks with the D^0 tap as bit K - 1."""
    ns = 1 << (k - 1)
    steps: List[List[Edge]] = []
    reach = {0}
    total = length + (k - 1 if terminate else 0)
    for t in range(total):
        tail = t >= length
        edges: List[Edge] = []
        for s in sorted(reach):
            for u in (0, 1):
                if fb is None:
                    if tail and u:
                        continue
                    a = u
                else:
                    f = bin(fb & s).count("1") & 1
                    if tail and u != f:
                        continue  # the tail input that feeds a zero into the register
                    a = u ^ f
                w = (a << (k - 1)) | s
                par = tuple(bin(g & w).count("1") & 1 for g in gens)
                out = par if fb is None else (u,) + par
                edges.append((s, u, w >> 1, out))
        steps.append(edges)
        reach = {e[2] for e in edges}
    return steps


def branch_log_gamma(edge: Edge, lc: Sequence[float], la: float) -> float:
    """ln gamma of an edge, up to a constant of the step:
    (1 - 2u) La / 2 + sum_j (1 - 2c_j) Lc_j / 2."""
    _, u, _, out = edge
    return 0.5 * ((1 - 2 * u) * la + sum((1 - 2 * c) * l for c, l in zip(out, lc)))


def max_star(a: float, b: float) -> float:
    """Jacobian logarithm: ln(e^a + e^b) = max(a, b) + ln(1 + e^(-|a - b|))."""
    if a == NEG:
        return b
    if b == NEG:
        return a
    return max(a, b) + math.log1p(math.exp(-abs(a - b)))


def bcjr(trellis: List[List[Edge]], lc: Sequence[float], la: Optional[Sequence[float]] = None,
         mode: str = "prob", terminated: bool = True) -> List[float]:
    """A posteriori LLRs of the input bits of every step.

    lc holds n channel LLRs per step; la the a priori LLRs of the inputs
    (zero if None). mode is "prob" (sums of products with normalization),
    "log" (log-MAP with the exact max*) or "maxlog" (max-log-MAP).
    If not terminated, the backward pass starts uniform over the end states.
    Cost: Theta(E) for E edges in the trellis, Theta(T S) space for T steps
    and S states.
    """
    n = len(trellis[0][0][3]) if trellis and trellis[0] else 0
    steps = len(trellis)
    la = la if la is not None else [0.0] * steps
    nst = 1 + max((e[2] for st in trellis for e in st), default=0)
    nst = max(nst, 1 + max((e[0] for st in trellis for e in st), default=0))
    lg = [[branch_log_gamma(e, lc[n * t:n * t + n], la[t]) for e in trellis[t]] for t in range(steps)]
    if mode == "prob":
        gam = [[math.exp(x) for x in row] for row in lg]
        alpha = [[0.0] * nst for _ in range(steps + 1)]
        alpha[0][0] = 1.0  # @line L1
        for t in range(steps):  # @line L2
            for (s, _, s2, _), g in zip(trellis[t], gam[t]):
                alpha[t + 1][s2] += alpha[t][s] * g
            z = sum(alpha[t + 1])
            alpha[t + 1] = [a / z for a in alpha[t + 1]]  # @line L3
        beta = [[0.0] * nst for _ in range(steps + 1)]
        ends = {e[2] for e in trellis[-1]} if trellis else {0}
        for s in range(nst):  # @line L4
            beta[steps][s] = 1.0 if (s == 0 or not terminated) and (s in ends) else 0.0
        for t in range(steps - 1, -1, -1):  # @line L5
            for (s, _, s2, _), g in zip(trellis[t], gam[t]):
                beta[t][s] += g * beta[t + 1][s2]
            z = sum(beta[t])
            beta[t] = [b / z for b in beta[t]]  # @line L6
        out = []
        for t in range(steps):
            p = [0.0, 0.0]
            for (s, u, s2, _), g in zip(trellis[t], gam[t]):
                p[u] += alpha[t][s] * g * beta[t + 1][s2]  # @line L7
            out.append(math.log(p[0]) - math.log(p[1]) if p[0] > 0 and p[1] > 0
                       else (math.inf if p[1] == 0 else -math.inf))  # @line L8
        return out
    comb = max_star if mode == "log" else max
    la_ = [[NEG] * nst for _ in range(steps + 1)]
    la_[0][0] = 0.0
    for t in range(steps):
        for (s, _, s2, _), g in zip(trellis[t], lg[t]):
            if la_[t][s] != NEG:
                la_[t + 1][s2] = comb(la_[t + 1][s2], la_[t][s] + g)
    lb = [[NEG] * nst for _ in range(steps + 1)]
    ends = {e[2] for e in trellis[-1]} if trellis else {0}
    for s in ends:
        if s == 0 or not terminated:
            lb[steps][s] = 0.0
    for t in range(steps - 1, -1, -1):
        for (s, _, s2, _), g in zip(trellis[t], lg[t]):
            if lb[t + 1][s2] != NEG:
                lb[t][s] = comb(lb[t][s], g + lb[t + 1][s2])
    out = []
    for t in range(steps):
        p = [NEG, NEG]
        for (s, u, s2, _), g in zip(trellis[t], lg[t]):
            if la_[t][s] != NEG and lb[t + 1][s2] != NEG:
                p[u] = comb(p[u], la_[t][s] + g + lb[t + 1][s2])
        out.append(p[0] - p[1])
    return out
