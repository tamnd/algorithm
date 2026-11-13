# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-threshold-theorem/. The authors are listed in prov/SATJ60.jsonl.
"""The concatenation recursion behind the threshold theorem, in two models that can be computed exactly.

This is NOT a fault-tolerant simulation. Both models assume that the decoding itself is perfect
("code capacity"); in the theorem the gates of the decoder fail too, which lowers the threshold.

1. Classical: the 3-bit repetition code with majority vote, concatenated. Level k uses 3^k bits.
   One level maps an independent bit-flip rate p to f(p) = 3p^2 - 2p^3, with threshold 1/2.
2. Quantum: the Steane code [[7, 1, 3]], concatenated. Each qubit gets an independent Pauli
   error with rates (pX, pY, pZ). Each block of 7 is decoded with the Hamming syndrome; the
   residual is a logical Pauli. One level maps the physical Pauli channel to an exact logical
   Pauli channel, by summing over all 4^7 = 16384 error patterns.

Qubit order: qubit 0 is the least significant bit of a mask (as in qsim.py and on steane-code).
"""

from fractions import Fraction

# rows of the Hamming parity-check matrix, as qubit sets (position j is qubit j - 1)
ROWS = [[3, 4, 5, 6], [1, 2, 5, 6], [0, 2, 4, 6]]
MASKS = [sum(1 << q for q in r) for r in ROWS]
N = 7


def parity(x: int) -> int:
    return bin(x).count("1") & 1


def majority_level(p):
    """Error rate of a majority vote of 3 independent copies with error rate p."""
    return 3 * p * p - 2 * p * p * p


def concatenated_majority(p, k: int):
    for _ in range(k):
        p = majority_level(p)
    return p


def majority_tree(bits: list[int]) -> int:
    """Decode a level-k word of 3^k bits by majority votes in a tree."""
    while len(bits) > 1:
        bits = [int(bits[i] + bits[i + 1] + bits[i + 2] >= 2) for i in range(0, len(bits), 3)]
    return bits[0]


def steane_residual(xs: int, zs: int) -> tuple[int, int]:
    """Decode the X part and the Z part of an error with the Hamming syndrome. Returns the
    logical error as (x, z) bits: the residual is a logical X if its X part has odd weight."""
    sz = sum(parity(xs & m) << (2 - i) for i, m in enumerate(MASKS))  # Z checks see X errors
    sx = sum(parity(zs & m) << (2 - i) for i, m in enumerate(MASKS))
    if sz:
        xs ^= 1 << (sz - 1)
    if sx:
        zs ^= 1 << (sx - 1)
    return parity(xs), parity(zs)


# for each of the 16384 patterns: (number of X, Y, Z letters, logical (x, z))
_PATTERNS = []
for _xs in range(1 << N):
    for _zs in range(1 << N):
        _ny = bin(_xs & _zs).count("1")
        _PATTERNS.append((bin(_xs).count("1") - _ny, _ny, bin(_zs).count("1") - _ny, steane_residual(_xs, _zs)))


def steane_level(channel):
    """One level of concatenation. channel = (pI, pX, pY, pZ) per physical qubit, independent.
    Returns the exact logical channel (qI, qX, qY, qZ). Works with Fraction or float."""
    p_i, p_x, p_y, p_z = channel
    out = [0 * p_i, 0 * p_i, 0 * p_i, 0 * p_i]
    index = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}
    for nx, ny, nz, lz in _PATTERNS:
        prob = p_i ** (N - nx - ny - nz) * p_x ** nx * p_y ** ny * p_z ** nz
        out[index[lz]] += prob
    return tuple(out)


def depolarizing(p):
    """Each Pauli X, Y, Z with probability p/3."""
    return (1 - p, p / 3, p / 3, p / 3)


def concatenated_steane(p, k: int):
    """The logical failure rate 1 - qI after k levels, starting from depolarizing noise of rate p."""
    ch = depolarizing(p)
    for _ in range(k):
        ch = steane_level(ch)
    return 1 - ch[0]


def failures_by_weight() -> list[int]:
    """The number of Pauli error patterns of each weight that the Steane decoder turns into a logical error."""
    out = [0] * (N + 1)
    for nx, ny, nz, lz in _PATTERNS:
        if lz != (0, 0):
            out[nx + ny + nz] += 1
    return out


def pseudo_threshold(lo: float = 1e-4, hi: float = 0.5, steps: int = 60) -> float:
    """The rate p at which one level of the Steane code under depolarizing noise neither helps nor hurts."""
    for _ in range(steps):
        mid = (lo + hi) / 2
        if concatenated_steane(mid, 1) < mid:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def levels_needed(p: float, p_th: float, target: float) -> int:
    """Smallest k with p_th (p / p_th)^(2^k) <= target, for p < p_th (the bound of the theorem)."""
    k = 0
    while p_th * (p / p_th) ** (2 ** k) > target:
        k += 1
    return k


def exact_majority_rate(p: Fraction, k: int) -> Fraction:
    """The failure rate of the level-k majority tree by brute force over all 2^(3^k) flip patterns."""
    n = 3 ** k
    total = Fraction(0)
    for pattern in range(1 << n):
        bits = [pattern >> i & 1 for i in range(n)]
        if majority_tree(bits):
            w = sum(bits)
            total += p ** w * (1 - p) ** (n - w)
    return total
