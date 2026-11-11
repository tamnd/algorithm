# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bkw-algorithm/. The authors are listed in prov/R2MHB2.jsonl.
"""The Blum-Kalai-Wasserman (BKW) algorithm for learning parity with noise.

An LPN sample is (x, y) with x uniform in F_2^n and y = <x, s> + e, where
e = 1 with probability tau. Vectors are Python ints; block i (0-based) is
the bits i*b .. i*b + b - 1, and n = a b.

bkw() recovers s one block at a time, from the top block down. For block t
it keeps the first t blocks of each sample (and corrects y for the bits of
s already known), clears blocks 0 .. t-2 by adding samples that agree on a
block, and reads the bits of block t-1 by a majority vote over the samples
that are equal to a unit vector. After t-1 levels each sample is the sum
of 2^(t-1) original samples, so its bias is (1 - 2 tau)^(2^(t-1)).

Like most practical versions, this code reuses one batch of samples for
all levels and all votes, so the votes are not independent. The analysis
of Blum, Kalai and Wasserman draws fresh samples instead. The reuse is a
heuristic that works well on these toy sizes.

solve_block_wht() is the Walsh-Hadamard step of Levieil and Fouque (LF1),
which uses every reduced sample instead of only the unit vectors.

For study only. The attack runs only on toy sizes (n up to 32), the code
is not constant time and uses the random module.
"""

import random
from typing import Dict, List, Sequence, Tuple

Sample = Tuple[int, int]


def parity(v: int) -> int:
    return bin(v).count("1") & 1


def lpn_samples(n: int, m: int, tau: float, rng: random.Random, s: int = None) -> Tuple[List[Sample], int]:
    """m LPN samples (x, <x, s> + e) with Pr[e = 1] = tau. Returns (samples, s)."""
    if s is None:
        s = rng.getrandbits(n)
    out = []
    for _ in range(m):
        x = rng.getrandbits(n)
        e = 1 if rng.random() < tau else 0
        out.append((x, parity(x & s) ^ e))
    return out, s


def reduce_block(R: Sequence[Sample], i: int, b: int) -> List[Sample]:
    """Clear block i: group by its bits, add the first sample of each group
    to the others and drop it. About 2^b samples are lost."""
    mask = (1 << b) - 1
    first: Dict[int, Sample] = {}
    out = []
    for x, y in R:
        key = (x >> (i * b)) & mask  # @line L5
        rep = first.get(key)
        if rep is None:
            first[key] = (x, y)
            continue
        out.append((x ^ rep[0], y ^ rep[1]))  # @line L6
    return out


def solve_block_majority(R: Sequence[Sample], t: int, b: int) -> int:
    """Bits of block t by majority vote over samples with x = e_j (BKW)."""
    block = 0
    for j in range(b):  # @line L7
        unit = 1 << (t * b + j)
        votes = [y for x, y in R if x == unit]
        if 2 * sum(votes) > len(votes):  # @line L8
            block |= 1 << j
    return block


def solve_block_wht(R: Sequence[Sample], t: int, b: int) -> int:
    """Bits of block t by a Walsh-Hadamard transform over all samples (LF1).

    f[v] = sum of (-1)^y over samples whose block t equals v; then
    F[c] = sum_v f[v] (-1)^<v, c> is largest at c = the block of s.
    """
    size = 1 << b
    f = [0] * size
    for x, y in R:
        f[(x >> (t * b)) & (size - 1)] += -1 if y else 1
    h = 1
    while h < size:
        for start in range(0, size, 2 * h):
            for k in range(start, start + h):
                u, v = f[k], f[k + h]
                f[k], f[k + h] = u + v, u - v
        h *= 2
    return max(range(size), key=lambda c: f[c])


def bkw(samples: Sequence[Sample], a: int, b: int, final: str = "majority") -> int:
    """Recover s in F_2^(a b) from LPN samples. final is "majority" or "wht"."""
    s = 0  # @line L1
    for t in range(a, 0, -1):  # @line L2
        low = (1 << (t * b)) - 1
        R = [(x & low, y ^ parity(x & ~low & s)) for x, y in samples]  # @line L3
        for i in range(t - 1):  # @line L4
            R = reduce_block(R, i, b)
        if final == "wht":
            block = solve_block_wht(R, t - 1, b)
        else:
            block = solve_block_majority(R, t - 1, b)
        s |= block << ((t - 1) * b)
    return s  # @line L9


def bias_after(tau: float, levels: int) -> float:
    """Bias (1 - 2 tau)^(2^levels) of a sum of 2^levels samples (piling-up lemma)."""
    return (1 - 2 * tau) ** (2 ** levels)
