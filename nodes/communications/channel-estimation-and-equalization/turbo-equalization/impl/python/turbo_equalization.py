# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/turbo-equalization/. The authors are listed in prov/XNK681.jsonl.

"""Turbo equalization of a convolutional code over a known ISI channel.

Transmitter: information bits u_0..u_(K-1), the rate 1/2 feedforward code with
generators 7 and 5 (octal) and two zero tail bits, so 2 (K + 2) code bits c;
an interleaver x[i] = 1 - 2 c[perm[i]]; a real channel h of L taps;
y_m = sum_l h_l x_(m-l) + w_m with w_m ~ N(0, sigma2), m = 0..N+L-2.

Receiver: a BCJR equalizer on the ISI trellis and a BCJR decoder on the code
trellis exchange extrinsic LLRs through the interleaver. All LLRs are
L = ln P(bit = 0) / P(bit = 1), and a symbol x = 1 - 2 bit has the LLR of its bit.
"""

import math

NEG = -math.inf


def _lse(a: float, b: float) -> float:
    """ln(e^a + e^b) without overflow."""
    if a == NEG:
        return b
    if b == NEG:
        return a
    if a < b:
        a, b = b, a
    return a + math.log1p(math.exp(b - a))


def encode(u: list[int]) -> list[int]:
    """The (7, 5) feedforward code with two tail bits: c = (c1_0, c2_0, c1_1, c2_1, ...)."""
    s1 = s2 = 0
    out = []
    for b in list(u) + [0, 0]:
        if b not in (0, 1):
            raise ValueError("bits must be 0 or 1")
        out += [b ^ s1 ^ s2, b ^ s2]
        s1, s2 = b, s1
    return out


def interleave(v: list, perm: list[int]) -> list:
    """The transmit order: out[i] = v[perm[i]]."""
    return [v[p] for p in perm]


def deinterleave(w: list, perm: list[int]) -> list:
    """The inverse of interleave: out[perm[i]] = w[i]."""
    out = [0.0] * len(w)
    for i, p in enumerate(perm):
        out[p] = w[i]
    return out


def bcjr_equalizer(y: list[float], h: list[float], sigma2: float, la: list[float]) -> list[float]:
    """Extrinsic LLRs of the N symbols from y (length N + L - 1), the channel and prior LLRs.

    The state is the tuple of the last L - 1 symbols. Symbols before the block are
    zero (the channel starts empty), and the last L - 1 samples only see the final state.
    """
    taps, n = len(h), len(la)
    if taps < 1 or sigma2 <= 0 or len(y) != n + taps - 1:
        raise ValueError("need L >= 1, sigma2 > 0 and len(y) = N + L - 1")
    m = taps - 1
    # The states (x_(t-1), ..., x_(t-m)) that can occur, with 0 for a symbol before the block.
    start = (0,) * m
    index = {start: 0}
    states = [start]
    edges = []  # edges[s] = [(next state, x, interference of the state)]
    q = 0
    while q < len(states):
        st = states[q]
        isi = sum(h[l] * st[l - 1] for l in range(1, taps))
        out = []
        for x in (1, -1):
            ns = ((x,) + st)[:m]
            if ns not in index:
                index[ns] = len(states)
                states.append(ns)
            out.append((index[ns], x, isi))
        edges.append(out)
        q += 1
    size = len(states)
    c = 1.0 / (2 * sigma2)
    h0 = h[0]

    alphas = [[NEG] * size for _ in range(n + 1)]
    alphas[0][0] = 0.0
    for t in range(n):
        a_t, a_n, yt, half = alphas[t], alphas[t + 1], y[t], la[t] / 2
        for s in range(size):
            a = a_t[s]
            if a == NEG:
                continue
            for ns, x, isi in edges[s]:
                z = yt - h0 * x - isi
                a_n[ns] = _lse(a_n[ns], a - z * z * c + x * half)
    beta = [NEG] * size
    for s in range(size):
        if alphas[n][s] == NEG:
            continue
        st = states[s]
        tail = 0.0
        for i in range(m):
            z = y[n + i] - sum(h[l] * st[l - i - 1] for l in range(i + 1, taps))
            tail -= z * z * c
        beta[s] = tail
    post = [0.0] * n
    for t in range(n - 1, -1, -1):
        a_t, yt, half = alphas[t], y[t], la[t] / 2
        num, den = NEG, NEG
        prev = [NEG] * size
        for s in range(size):
            a = a_t[s]
            if a == NEG:
                continue
            for ns, x, isi in edges[s]:
                b = beta[ns]
                if b == NEG:
                    continue
                z = yt - h0 * x - isi
                gb = b - z * z * c + x * half
                if x == 1:
                    num = _lse(num, a + gb)
                else:
                    den = _lse(den, a + gb)
                prev[s] = _lse(prev[s], gb)
        post[t] = num - den
        beta = prev
    return [p - a for p, a in zip(post, la)]


def bcjr_decoder(lc: list[float]) -> tuple[list[float], list[float]]:
    """BCJR on the terminated (7, 5) trellis.

    lc holds one prior LLR per code bit, length 2 (K + 2). Returns the posterior
    LLRs of the K information bits and the extrinsic LLRs of the code bits.
    """
    if len(lc) % 2 or len(lc) < 4:
        raise ValueError("need 2 (K + 2) code bit LLRs")
    steps = len(lc) // 2
    k = steps - 2

    # The state is (u_(t-1), u_(t-2)) as the integer 2 u_(t-1) + u_(t-2).
    table = []  # table[s] = [(input bit, next state, c1, c2)]
    for s in range(4):
        s1, s2 = s >> 1, s & 1
        table.append([(b, (b << 1) | s1, b ^ s1 ^ s2, b ^ s2) for b in (0, 1)])

    def edges(t: int, s: int) -> list:
        return table[s] if t < k else table[s][:1]

    alpha = [[NEG] * 4 for _ in range(steps + 1)]
    alpha[0][0] = 0.0
    for t in range(steps):
        l1, l2 = lc[2 * t] / 2, lc[2 * t + 1] / 2
        for s in range(4):
            a = alpha[t][s]
            if a == NEG:
                continue
            for _, ns, c1, c2 in edges(t, s):
                g = (l1 if c1 == 0 else -l1) + (l2 if c2 == 0 else -l2)
                alpha[t + 1][ns] = _lse(alpha[t + 1][ns], a + g)
    beta = [[NEG] * 4 for _ in range(steps + 1)]
    beta[steps][0] = 0.0
    lu = [0.0] * k
    le = [0.0] * len(lc)
    for t in range(steps - 1, -1, -1):
        l1, l2 = lc[2 * t] / 2, lc[2 * t + 1] / 2
        acc = [NEG] * 6  # u = 0, u = 1, c1 = 0, c1 = 1, c2 = 0, c2 = 1
        for s in range(4):
            for b, ns, c1, c2 in edges(t, s):
                g = (l1 if c1 == 0 else -l1) + (l2 if c2 == 0 else -l2)
                gb = g + beta[t + 1][ns]
                beta[t][s] = _lse(beta[t][s], gb)
                v = alpha[t][s] + gb
                if v == NEG:
                    continue
                acc[b] = _lse(acc[b], v)
                acc[2 + c1] = _lse(acc[2 + c1], v)
                acc[4 + c2] = _lse(acc[4 + c2], v)
        if t < k:
            lu[t] = acc[0] - acc[1]
        le[2 * t] = acc[2] - acc[3] - lc[2 * t]
        le[2 * t + 1] = acc[4] - acc[5] - lc[2 * t + 1]
    return lu, le


def turbo_equalize(
    y: list[float], h: list[float], sigma2: float, perm: list[int], iterations: int
) -> list[list[float]]:
    """Run the loop and return the information bit LLRs after each iteration."""
    if iterations < 1 or sorted(perm) != list(range(len(perm))):
        raise ValueError("need iterations >= 1 and a permutation")
    la_eq = [0.0] * len(perm)  # @line L1
    history = []
    for _ in range(iterations):  # @line L2
        le_eq = bcjr_equalizer(y, h, sigma2, la_eq)  # @line L3
        la_dec = deinterleave(le_eq, perm)  # @line L4
        lu, le_dec = bcjr_decoder(la_dec)  # @line L5
        la_eq = interleave(le_dec, perm)  # @line L6
        history.append(lu)  # @line L7
    return history  # @line L8
