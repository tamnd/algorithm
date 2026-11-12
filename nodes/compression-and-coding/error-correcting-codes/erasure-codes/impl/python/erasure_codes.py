# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/erasure-codes/. The authors are listed in prov/KSMYGE.jsonl.
"""Two erasure codes over GF(2^8): RAID-6 P+Q and a Cauchy Reed-Solomon code.

GF(2^8) is GF(2)[x] / (x^8 + x^4 + x^3 + x^2 + 1), the polynomial 0x11D. The element
{02} = x generates the multiplicative group. Addition is XOR. A disk or a block is a
list of bytes, and each operation acts byte by byte.
"""

from typing import Dict, List, Sequence

POLY = 0x11D
EXP = [0] * 512
LOG = [0] * 256
_v = 1
for _i in range(255):
    EXP[_i] = _v
    LOG[_v] = _i
    _v <<= 1
    if _v & 0x100:
        _v ^= POLY
for _i in range(255, 512):
    EXP[_i] = EXP[_i - 255]

Block = List[int]


def mul(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return EXP[LOG[a] + LOG[b]]


def inv(a: int) -> int:
    if a == 0:
        raise ZeroDivisionError("0 has no inverse")
    return EXP[255 - LOG[a]]


def gpow(k: int) -> int:
    """{02}^k for each integer k, negative ones included."""
    return EXP[k % 255]


def xor_blocks(a: Sequence[int], b: Sequence[int]) -> Block:
    return [p ^ q for p, q in zip(a, b)]


def scale(c: int, a: Sequence[int]) -> Block:
    return [mul(c, p) for p in a]


# RAID-6 (Anvin, "The mathematics of RAID-6", Section 2, equations (1) to (20))

def raid6_syndromes(data: Sequence[Sequence[int]]):
    """P = sum D_i and Q = sum g^i D_i with g = {02}."""
    size = len(data[0])
    p, q = [0] * size, [0] * size
    for i, d in enumerate(data):
        p = xor_blocks(p, d)
        q = xor_blocks(q, scale(gpow(i), d))
    return p, q


def raid6_recover(data: List, p, q):
    """Rebuild at most two lost blocks. A lost block is None; data, p and q may be None.

    Returns (data, p, q) with every block present."""
    lost = [i for i, d in enumerate(data) if d is None]
    if len(lost) + (p is None) + (q is None) > 2:
        raise ValueError("RAID-6 recovers at most two lost blocks")
    size = len(next(b for b in list(data) + [p, q] if b is not None))
    zero = [0] * size
    filled = [zero if d is None else d for d in data]
    pp, qq = raid6_syndromes(filled)  # P_xy and Q_xy: the syndromes with lost blocks set to 0
    data = list(data)
    if len(lost) == 2:
        x, y = lost
        dp, dq = xor_blocks(p, pp), xor_blocks(q, qq)
        t = inv(gpow(y - x) ^ 1)
        a, b = mul(gpow(y - x), t), mul(gpow(-x), t)  # Anvin, equations (17) and (18)
        dx = xor_blocks(scale(a, dp), scale(b, dq))  # equation (19)
        data[x], data[y] = dx, xor_blocks(dp, dx)  # equation (20)
    elif len(lost) == 1:
        x = lost[0]
        if p is not None:
            data[x] = xor_blocks(p, pp)
        else:
            data[x] = scale(gpow(-x), xor_blocks(q, qq))  # Anvin, equation (5)
    full_p, full_q = raid6_syndromes(data)
    return data, full_p if p is None else p, full_q if q is None else q


# Cauchy Reed-Solomon (Blomer, Kalfane, Karp, Karpinski, Luby and Zuckerman, 1995)

def cauchy_matrix(m: int, k: int) -> List[List[int]]:
    """m x k matrix C[i][j] = 1 / (x_i + y_j) with x_i = i and y_j = m + j, all distinct."""
    if m + k > 256:
        raise ValueError("need m + k <= 256 distinct field elements")
    return [[inv(i ^ (m + j)) for j in range(k)] for i in range(m)]


def cauchy_encode(data: Sequence[Sequence[int]], m: int) -> List[Block]:
    """The m parity blocks of a systematic [k + m, k] code with generator [I | C^T]."""
    k = len(data)
    c = cauchy_matrix(m, k)
    out = []
    for i in range(m):
        acc = [0] * len(data[0])
        for j in range(k):
            acc = xor_blocks(acc, scale(c[i][j], data[j]))
        out.append(acc)
    return out


def invert(a: List[List[int]]) -> List[List[int]]:
    """Inverse of a square matrix over GF(2^8) by Gauss-Jordan elimination."""
    n = len(a)
    m = [list(row) + [int(i == j) for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        piv = next((r for r in range(col, n) if m[r][col]), None)
        if piv is None:
            raise ValueError("singular matrix")
        m[col], m[piv] = m[piv], m[col]
        f = inv(m[col][col])
        m[col] = [mul(f, v) for v in m[col]]
        for r in range(n):
            if r != col and m[r][col]:
                c = m[r][col]
                m[r] = [v ^ mul(c, w) for v, w in zip(m[r], m[col])]
    return [row[n:] for row in m]


def cauchy_decode(blocks: Dict[int, Sequence[int]], k: int, m: int) -> List[Block]:
    """Recover the k data blocks from any k of the k + m blocks.

    blocks maps a position to its block: 0..k-1 are data, k..k+m-1 are parity."""
    if len(blocks) < k:
        raise ValueError("need at least k blocks")
    c = cauchy_matrix(m, k)
    rows, have = [], []
    for pos in sorted(blocks)[:k]:
        rows.append([int(pos == j) for j in range(k)] if pos < k else c[pos - k])
        have.append(blocks[pos])
    r = invert(rows)
    out = []
    for i in range(k):
        acc = [0] * len(have[0])
        for j in range(k):
            acc = xor_blocks(acc, scale(r[i][j], have[j]))
        out.append(acc)
    return out


def bit_matrix(e: int) -> List[List[int]]:
    """8 x 8 matrix over GF(2) of the map v -> e v, with bit 0 the least significant.

    This is the trick of Blomer et al.: each product becomes XORs of bits."""
    cols = [mul(e, 1 << j) for j in range(8)]
    return [[(cols[j] >> i) & 1 for j in range(8)] for i in range(8)]


def mul_by_bits(e: int, v: int) -> int:
    mat = bit_matrix(e)
    out = 0
    for i in range(8):
        bit = 0
        for j in range(8):
            bit ^= mat[i][j] & (v >> j)
        out |= (bit & 1) << i
    return out
