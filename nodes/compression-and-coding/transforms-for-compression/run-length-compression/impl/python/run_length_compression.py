# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/run-length-compression/. The authors are listed in prov/Y9ZKV2.jsonl.

"""Run-length compression of a binary source with a Golomb code.

The source is a string of bits in which a 0 has probability theta and the
bits are independent. Cut it into runs: k zeros followed by a 1. The run
length k then has the geometric distribution P(k) = (1 - theta) theta^k, and
the Golomb code with parameter m is an optimal prefix code for it when m is
the smallest integer with theta^m + theta^(m+1) <= 1 (Gallager and Van
Voorhis, 1975). The last run of the string is closed by a virtual 1, which
the decoder drops because it knows n.

Golomb code of k with parameter m: q = k // m in unary (q ones, then a
zero), then r = k % m in truncated binary. Time O(n + output) for both
directions.
"""

import math
from collections.abc import Iterable


def golomb_parameter(theta: float) -> int:
    """The smallest m >= 1 with theta^m + theta^(m+1) <= 1, for 0 <= theta < 1."""
    if not 0 <= theta < 1:
        raise ValueError("theta must be in [0, 1)")
    m = 1
    while theta**m + theta ** (m + 1) > 1:
        m += 1
    return m


def golomb_encode(k: int, m: int) -> str:
    """The Golomb code of k >= 0 with parameter m >= 1, as a string of '0' and '1'."""
    q, r = divmod(k, m)
    out = "1" * q + "0"
    b = (m - 1).bit_length()  # ceil(log2 m)
    cutoff = (1 << b) - m
    if b == 0:  # m = 1: the code is unary
        return out
    if r < cutoff:  # then cutoff > 0, so m < 2^b and b >= 2
        return out + format(r, "b").zfill(b - 1)
    return out + format(r + cutoff, "b").zfill(b)


def golomb_decode(bits: str, pos: int, m: int) -> tuple[int, int]:
    """Read one Golomb code from bits at pos; return (k, the next position)."""
    q = 0
    while bits[pos] == "1":
        q += 1
        pos += 1
    pos += 1
    b = (m - 1).bit_length()
    cutoff = (1 << b) - m
    if b == 0:  # m = 1: the code is unary
        return q, pos
    r = int(bits[pos : pos + b - 1], 2) if b > 1 else 0
    if r < cutoff:  # short codeword of b - 1 bits
        pos += b - 1
    else:  # long codeword of b bits, holding r + cutoff
        r = int(bits[pos : pos + b], 2) - cutoff
        pos += b
    return q * m + r, pos


def golomb_length(k: int, m: int) -> int:
    return len(golomb_encode(k, m))


def runs_encode(bits: Iterable[int], theta: float) -> str:
    """Code the runs of zeros of a bit string with the Golomb code for theta."""
    m = golomb_parameter(theta)  # @line L1
    k = 0  # @line L2
    out: list[str] = []
    for b in bits:  # @line L3
        if b == 0:  # @line L4
            k += 1
        else:
            out.append(golomb_encode(k, m))  # @line L5
            k = 0
    out.append(golomb_encode(k, m))  # @line L6
    return "".join(out)  # @line L7


def runs_decode(code: str, n: int, theta: float) -> list[int]:
    """Inverse of runs_encode for a bit string of length n."""
    m = golomb_parameter(theta)
    out: list[int] = []
    pos = 0
    while len(out) <= n:
        k, pos = golomb_decode(code, pos, m)
        out.extend([0] * k)
        out.append(1)
    if len(out) != n + 1 or pos != len(code):
        raise ValueError("the code does not match the length")
    return out[:n]


def run_entropy(theta: float) -> float:
    """Entropy in bits of the geometric run length (1 - theta) theta^k."""
    if theta == 0:
        return 0.0
    h = -theta * math.log2(theta) - (1 - theta) * math.log2(1 - theta)
    return h / (1 - theta)


def expected_golomb_length(theta: float, m: int, terms: int = 20000) -> float:
    """E[length of the Golomb code] for the geometric run length, summed to `terms`."""
    total, p = 0.0, 1 - theta
    for k in range(terms):
        total += p * golomb_length(k, m)
        p *= theta
        if p < 1e-18:
            break
    return total
