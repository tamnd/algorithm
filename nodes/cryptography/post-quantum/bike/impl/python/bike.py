# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bike/. The authors are listed in prov/H257TC.jsonl.
"""A toy KEM in the shape of BIKE: a QC-MDPC code with the BGF decoder.

THIS IS NOT THE BIKE SPECIFICATION. It follows the structure of BIKE round 4
(the key h = h1 / h0, the ciphertext (e0 + e1 h, m xor L(e0, e1)), and
decapsulation with the Black-Gray-Flip decoder and implicit rejection), but
the block length is r = 587 instead of 12323, the hash functions, the
sampling of the error vector and all encodings are simplified, and the
threshold rule is computed from a counter model, not the fitted rule of the
specification. There are no KAT tests, and the parameters give no security.

For study only. The code is not constant time and uses the random module.
Use a vetted library, for example a FIPS 140 validated module, to protect
real data.

A polynomial of GF(2)[x] / (x^r - 1) is a Python int: bit i is the
coefficient of x^i. A sparse polynomial is also given by its support.
"""

import hashlib
import random
from functools import lru_cache
from math import comb, log
from typing import List, Optional, Sequence, Tuple

# Toy parameters: r is a prime with 2 primitive modulo r, d is the column
# weight of each circulant block (odd), t is the error weight.
R, D, T_ERR = 587, 15, 18


def popcount(a: int) -> int:
    return bin(a).count("1")


def rot(a: int, k: int, r: int) -> int:
    """x^k a mod x^r - 1."""
    k %= r
    if k == 0:
        return a
    return ((a << k) | (a >> (r - k))) & ((1 << r) - 1)


def support(a: int) -> List[int]:
    return [i for i in range(a.bit_length()) if (a >> i) & 1]


def mul_sparse(a: int, supp: Sequence[int], r: int) -> int:
    """a b mod x^r - 1, where b has the given support."""
    out = 0
    for k in supp:
        out ^= rot(a, k, r)
    return out


def inverse(a: int, r: int) -> int:
    """a^-1 mod x^r - 1 by the extended Euclidean algorithm on ints."""
    u, v = a, (1 << r) | 1
    g1, g2 = 1, 0                             # g1 a = u and g2 a = v (mod x^r - 1)
    while True:
        if u == 1:
            g = g1
            break
        if v == 1:
            g = g2
            break
        if u == 0 or v == 0:
            raise ZeroDivisionError("not invertible")
        j = u.bit_length() - v.bit_length()
        if j < 0:
            u, v, g1, g2, j = v, u, g2, g1, -j
        u ^= v << j
        g1 ^= g2 << j
    while g >> r:
        g = (g & ((1 << r) - 1)) ^ (g >> r)
    return g


def random_sparse(r: int, w: int, rng: random.Random) -> int:
    return sum(1 << i for i in rng.sample(range(r), w))


# ---------------------------------------------------------------- the BGF decoder

class Block:
    """One circulant block of H, with a packed form for the counters."""

    def __init__(self, h: int, r: int):
        self.h, self.r = h, r
        self.supp = support(h)
        self.packed = sum(1 << (8 * k) for k in self.supp)

    def counters(self, s: int) -> bytes:
        """ctr[j] = sum over k in supp(h) of s_(j + k mod r): the number of
        unsatisfied parity checks that touch position j of this block.
        One integer product computes all r counters (each is < 256)."""
        r = self.r
        rev = bytes((s >> ((-i) % r)) & 1 for i in range(r))
        p = (int.from_bytes(rev, "little") * self.packed).to_bytes(2 * r, "little")
        conv = [p[i] + p[i + r] for i in range(r)]
        return bytes(conv[(-j) % r] for j in range(r))


@lru_cache(maxsize=None)
def threshold(s_weight: int, r: int, d: int, t: int) -> int:
    """The smallest T at which a counter value is more likely to come from an
    error position than from a correct one, in the counter model of Sendrier
    and Vasseur; never below (d + 1) / 2."""
    n, w = 2 * r, 2 * d
    rho = {l: comb(w, l) * comb(n - w, t - l) for l in range(1, min(w, t) + 1, 2)}
    total = sum(rho.values())
    x = s_weight * sum((l - 1) * v for l, v in rho.items()) / total
    pi1 = min(max((s_weight + x) / (t * d), 1e-12), 1 - 1e-12)
    pi0 = min(max(((w - 1) * s_weight - x) / ((n - t) * d), 1e-12), 1 - 1e-12)
    for tt in range(d + 1):
        lhs = log(t) + tt * log(pi1) + (d - tt) * log(1 - pi1)
        rhs = log(n - t) + tt * log(pi0) + (d - tt) * log(1 - pi0)
        if lhs >= rhs:
            return max(tt, (d + 1) // 2)
    return d + 1


def bgf(s: int, h0: Block, h1: Block, t: int, iters: int = 5, tau: int = 3) -> Optional[Tuple[int, int]]:
    """Black-Gray-Flip decoding: (e0, e1) with e0 h0 + e1 h1 = s, or None."""
    r, d = h0.r, len(h0.supp)
    blocks = (h0, h1)
    e = [0, 0]

    def residue() -> int:
        return s ^ mul_sparse(e[0], h0.supp, r) ^ mul_sparse(e[1], h1.supp, r)

    for i in range(1, iters + 1):                            # B1
        syn = residue()
        thr = threshold(popcount(syn), r, d, t)              # B2
        black, gray = [0, 0], [0, 0]
        for b in range(2):                                   # B3
            ctr = blocks[b].counters(syn)
            for j in range(r):
                if ctr[j] >= thr:
                    e[b] ^= 1 << j
                    black[b] |= 1 << j
                elif ctr[j] >= thr - tau:
                    gray[b] |= 1 << j
        if i == 1:                                           # B4
            for mask in (black, gray):
                syn = residue()
                for b in range(2):
                    ctr = blocks[b].counters(syn)
                    for j in range(r):
                        if ctr[j] >= (d + 1) // 2 + 1 and (mask[b] >> j) & 1:
                            e[b] ^= 1 << j
    if residue() == 0:                                       # B5
        return e[0], e[1]
    return None


def bit_flip(s: int, h0: Block, h1: Block, t: int, iters: int = 5) -> Optional[Tuple[int, int]]:
    """Plain parallel bit flipping with the same threshold and no masks, for comparison."""
    r, d = h0.r, len(h0.supp)
    e = [0, 0]
    for _ in range(iters):
        syn = s ^ mul_sparse(e[0], h0.supp, r) ^ mul_sparse(e[1], h1.supp, r)
        if syn == 0:
            break
        thr = threshold(popcount(syn), r, d, t)
        for b, blk in enumerate((h0, h1)):
            ctr = blk.counters(syn)
            for j in range(r):
                if ctr[j] >= thr:
                    e[b] ^= 1 << j
    if s ^ mul_sparse(e[0], h0.supp, r) ^ mul_sparse(e[1], h1.supp, r) == 0:
        return e[0], e[1]
    return None


# ---------------------------------------------------------------- hashing (simplified)

def sample_error(m: bytes, r: int, t: int) -> Tuple[int, int]:
    """H(m): t distinct positions in [0, 2r) from SHAKE256, by rejection."""
    n = 2 * r
    bits = n.bit_length()
    stream = hashlib.shake_256(b"H" + m).digest(8 * t + 64)
    pos: List[int] = []
    i = 0
    while len(pos) < t:
        if i + 2 > len(stream):
            stream = hashlib.shake_256(b"H" + m).digest(2 * len(stream))
        v = int.from_bytes(stream[i:i + 2], "little") & ((1 << bits) - 1)
        i += 2
        if v < n and v not in pos:
            pos.append(v)
    e = sum(1 << p for p in pos)
    return e & ((1 << r) - 1), e >> r


def enc(a: int, r: int) -> bytes:
    return a.to_bytes((r + 7) // 8, "little")


def hash_l(e0: int, e1: int, r: int) -> bytes:
    return hashlib.sha3_384(b"L" + enc(e0, r) + enc(e1, r)).digest()[:32]


def hash_k(m: bytes, c0: int, c1: bytes, r: int) -> bytes:
    return hashlib.sha3_384(b"K" + m + enc(c0, r) + c1).digest()[:32]


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


# ---------------------------------------------------------------- the KEM

def keygen(rng: random.Random, r: int = R, d: int = D):
    h0 = random_sparse(r, d, rng)                            # @line L1
    h1 = random_sparse(r, d, rng)
    h = mul_sparse(inverse(h0, r), support(h1), r)           # @line L2
    sigma = rng.randbytes(32)
    return h, (h0, h1, sigma)                                # @line L3


def encaps(h: int, rng: random.Random, r: int = R, t: int = T_ERR):
    m = rng.randbytes(32)                                    # @line L4
    e0, e1 = sample_error(m, r, t)                           # @line L5
    c = (e0 ^ mul_sparse(h, support(e1), r), xor(m, hash_l(e0, e1, r)))  # @line L6
    return c, hash_k(m, c[0], c[1], r)                       # @line L7


def decaps(sk, c, r: int = R, t: int = T_ERR) -> bytes:
    h0, h1, sigma = sk
    c0, c1 = c
    s = mul_sparse(c0, support(h0), r)
    e = bgf(s, Block(h0, r), Block(h1, r), t)                # @line L8
    if e is None:
        return hash_k(sigma, c0, c1, r)
    m2 = xor(c1, hash_l(e[0], e[1], r))                      # @line L9
    if sample_error(m2, r, t) == e:                          # @line L10
        return hash_k(m2, c0, c1, r)
    return hash_k(sigma, c0, c1, r)
