# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/turbo-code/. The authors are listed in prov/NXDXWC.jsonl.

"""Parallel concatenated convolutional (turbo) encoders.

Taps are octal masks; the leftmost of the K binary digits is the D^0 tap.
A constituent code is recursive systematic with transfer function
(1, ff(D) / fb(D)). Each constituent encoder is terminated separately with
K - 1 tail steps, as in 3GPP TS 36.212, Section 5.1.3.2.2.
"""

from typing import Dict, List, Sequence, Tuple


def rsc_parity(bits: Sequence[int], fb: int, ff: int, k: int, terminate: bool = True) -> Tuple[List[int], List[Tuple[int, int]]]:
    """Parity bits of an RSC encoder, and the (tail input, tail parity) pairs
    that drive it back to state 0."""
    state, par = 0, []
    for u in bits:
        a = (u + bin(fb & state).count("1")) & 1
        w = (a << (k - 1)) | state
        par.append(bin(ff & w).count("1") & 1)
        state = w >> 1
    tail = []
    if terminate:
        for _ in range(k - 1):
            u = bin(fb & state).count("1") & 1  # makes the register input zero
            w = state
            tail.append((u, bin(ff & w).count("1") & 1))
            state = w >> 1
    return par, tail


def turbo_encode(bits: Sequence[int], perm: Sequence[int], fb: int, ff: int, k: int) -> Dict[str, list]:
    """Rate 1/3 turbo encoding: systematic bits, parity of encoder 1 on the
    bits, parity of encoder 2 on the interleaved bits c'_i = c_perm(i)."""
    p1, t1 = rsc_parity(bits, fb, ff, k)
    p2, t2 = rsc_parity([bits[perm[i]] for i in range(len(bits))], fb, ff, k)
    return {"sys": list(bits), "par1": p1, "par2": p2, "tail1": t1, "tail2": t2}


def puncture_half(enc: Dict[str, list]) -> List[int]:
    """Rate 1/2 by alternate puncturing of the two parity streams:
    u_0 p1_0 u_1 p2_1 u_2 p1_2 ... (tails sent in full)."""
    out = []
    for i, u in enumerate(enc["sys"]):
        out += [u, enc["par1"][i] if i % 2 == 0 else enc["par2"][i]]
    for u, p in enc["tail1"] + enc["tail2"]:
        out += [u, p]
    return out


def codeword_weight(bits: Sequence[int], perm: Sequence[int], fb: int, ff: int, k: int) -> int:
    """Hamming weight of the rate 1/3 codeword with both tails."""
    e = turbo_encode(bits, perm, fb, ff, k)
    return sum(e["sys"]) + sum(e["par1"]) + sum(e["par2"]) + sum(a + b for a, b in e["tail1"] + e["tail2"])


def qpp_interleaver(size: int, f1: int, f2: int) -> List[int]:
    """Quadratic permutation polynomial interleaver of LTE:
    perm(i) = (f1 i + f2 i^2) mod K (TS 36.212, Section 5.1.3.2.3)."""
    return [(f1 * i + f2 * i * i) % size for i in range(size)]


# TS 36.212 V10.2.0, Table 5.1.3-3, rows i = 1, 4, 48, 51, 95, 98, 142 and 145.
LTE_QPP = {40: (3, 10), 64: (7, 16), 416: (25, 52), 440: (91, 110),
           1120: (67, 140), 1216: (39, 76), 3200: (111, 240), 3392: (51, 212)}


def ccsds_permutation(k: int, k1: int = 8) -> List[int]:
    """The CCSDS turbo code permutation pi(s), s = 1 .. k, of CCSDS 131.0-B-5,
    Section 6.3 g), with k = k1 k2 (Table 6-3). Returns 1-based values."""
    k2 = k // k1
    primes = [31, 37, 43, 47, 53, 59, 61, 67]
    out = []
    for s in range(1, k + 1):
        m = (s - 1) % 2
        i = (s - 1) // (2 * k2)
        j = (s - 1) // 2 - i * k2
        t = (19 * i + 1) % (k1 // 2)
        q = t % 8 + 1
        c = (primes[q - 1] * j + 21 * m) % k2
        out.append(2 * (t + c * (k1 // 2) + 1) - m)
    return out


def min_weight_two_inputs(perm: Sequence[int], fb: int, ff: int, k: int) -> Tuple[int, Tuple[int, int]]:
    """The least codeword weight over all inputs of weight 2, by brute force
    over the K (K - 1) / 2 pairs. Weight 2 inputs that the feedback divides
    give the low weight codewords behind the error floor."""
    n = len(perm)
    best = (1 << 30, (0, 0))
    for a in range(n):
        for b in range(a + 1, n):
            u = [0] * n
            u[a] = u[b] = 1
            w = codeword_weight(u, perm, fb, ff, k)
            if w < best[0]:
                best = (w, (a, b))
    return best
