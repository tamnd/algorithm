# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hqc/. The authors are listed in prov/E4EFXK.jsonl.
"""The HQC public-key encryption scheme with the HQC-1 (HQC-128) parameters,
and a KEM on top of it with the HHK transform with implicit rejection.

What is real here: the ring F2[x] / (x^n - 1) with n = 17669, the weights
w = 66 and wr = we = 75, the public code (a shortened Reed-Solomon code
[46, 16, 31] over GF(256) concatenated with the Reed-Muller code RM(1, 7)
repeated 3 times), the structure of keys and ciphertexts, and decoding.

What is NOT the specification: the hash functions, the seed expansion, the
sampling of fixed weight vectors, the bit order of the codes, and all byte
encodings are simplified. So this code does not reproduce the official KAT
files, and the tests do not use them.

For study only. The code is not constant time and uses the random module.
Use a vetted library, for example a FIPS 140 validated module, to protect
real data.

A polynomial of F2[x] / (x^n - 1) is a Python int: bit i is the coefficient
of x^i. A sparse polynomial is also given by its support.
"""

import hashlib
import random
from typing import List, Optional, Sequence, Tuple

# HQC-1 parameters
N = 17669          # ring length, a prime with 2 primitive modulo N
N1, K1 = 46, 16    # Reed-Solomon length and dimension (bytes)
DELTA = 15         # Reed-Solomon correction capacity
N2 = 384           # RM(1, 7) repeated 3 times
W, WR, WE = 66, 75, 75


# ---------------------------------------------------------------- GF(256)

class GF:
    def __init__(self, m: int, modulus: int):
        self.q = 1 << m
        self.exp = [0] * (2 * self.q)
        self.log = [0] * self.q
        x = 1
        for i in range(self.q - 1):
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & self.q:
                x ^= modulus
        if x != 1:
            raise ValueError("modulus is not primitive")
        for i in range(self.q - 1, 2 * self.q):
            self.exp[i] = self.exp[i - (self.q - 1)]

    def mul(self, a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        return self.exp[self.log[a] + self.log[b]]

    def div(self, a: int, b: int) -> int:
        if b == 0:
            raise ZeroDivisionError
        if a == 0:
            return 0
        return self.exp[(self.log[a] - self.log[b]) % (self.q - 1)]

    def pow_alpha(self, i: int) -> int:
        return self.exp[i % (self.q - 1)]


GF256 = GF(8, 0x11D)   # x^8 + x^4 + x^3 + x^2 + 1


# ---------------------------------------------------------------- Reed-Solomon

class ReedSolomon:
    """A narrow-sense RS code of length n and dimension k over a field gf,
    with roots alpha^1 .. alpha^(n-k) of the generator polynomial.
    A codeword is a list of n symbols, lowest degree first: the n - k parity
    symbols, then the k message symbols (systematic encoding)."""

    def __init__(self, gf: GF, n: int, k: int):
        self.gf, self.n, self.k, self.r = gf, n, k, n - k
        g = [1]
        for i in range(1, self.r + 1):         # g(x) = prod (x - alpha^i)
            a = gf.pow_alpha(i)
            out = [0] * (len(g) + 1)
            for j, c in enumerate(g):
                out[j] ^= gf.mul(c, a)
                out[j + 1] ^= c
            g = out
        self.g = g

    def encode(self, msg: Sequence[int]) -> List[int]:
        gf, r = self.gf, self.r
        rem = [0] * r + list(msg)              # m(x) x^r
        for i in range(len(rem) - 1, r - 1, -1):
            c = rem[i]
            if c:
                for j, gj in enumerate(self.g):
                    rem[i - r + j] ^= gf.mul(c, gj)
        return rem[:r] + list(msg)

    def syndromes(self, y: Sequence[int]) -> List[int]:
        gf = self.gf
        out = []
        for j in range(1, self.r + 1):
            a, acc = gf.pow_alpha(j), 0
            for c in reversed(y):
                acc = gf.mul(acc, a) ^ c
            out.append(acc)
        return out

    def decode(self, y: Sequence[int]) -> Optional[List[int]]:
        """The message of the codeword nearest to y if at most (n - k) / 2
        symbols are wrong (syndromes, Berlekamp-Massey, Chien search, Forney)."""
        gf, n, r = self.gf, self.n, self.r
        s = self.syndromes(y)
        if not any(s):
            return list(y[r:])
        c, b, l, m, bb = [1], [1], 0, 1, 1      # Berlekamp-Massey
        for i in range(r):
            d = s[i]
            for j in range(1, l + 1):
                if j < len(c):
                    d ^= gf.mul(c[j], s[i - j])
            if d == 0:
                m += 1
                continue
            coef = gf.div(d, bb)
            new = c + [0] * max(0, len(b) + m - len(c))
            for j, bj in enumerate(b):
                new[j + m] ^= gf.mul(coef, bj)
            if 2 * l <= i:
                l, b, bb, m = i + 1 - l, c, d, 1
            else:
                m += 1
            c = new
        while len(c) > 1 and c[-1] == 0:
            c.pop()
        if len(c) - 1 != l or 2 * l > r:
            return None
        omega = [0] * r                          # Omega = S sigma mod x^r
        for i, si in enumerate(s):
            for j, cj in enumerate(c):
                if i + j < r:
                    omega[i + j] ^= gf.mul(si, cj)
        out = list(y)
        found = 0
        for pos in range(n):                     # Chien search: sigma(alpha^-pos) = 0
            xinv = gf.pow_alpha(-pos)
            acc = 0
            for cj in reversed(c):
                acc = gf.mul(acc, xinv) ^ cj
            if acc:
                continue
            found += 1
            num = 0
            for oj in reversed(omega):
                num = gf.mul(num, xinv) ^ oj
            den = 0                              # sigma'(x): odd terms only in characteristic 2
            for j in range(1, len(c), 2):
                den ^= gf.mul(c[j], gf.pow_alpha(-pos * (j - 1)))
            if den == 0:
                return None
            out[pos] ^= gf.div(num, den)
        if found != l:
            return None
        return out[r:]


RS = ReedSolomon(GF256, N1, K1)


# ---------------------------------------------------------------- Reed-Muller RM(1, 7), repeated

def parity(x: int) -> int:
    return bin(x).count("1") & 1


def rm_encode(byte: int, copies: int = 3) -> int:
    """Bit j of an RM(1,7) codeword is b0 xor <u, j>, where b0 is bit 0 of the
    byte and u its top 7 bits; the 128-bit word is repeated `copies` times."""
    b0, u = byte & 1, byte >> 1
    word = sum((b0 ^ parity(u & j)) << j for j in range(128))
    out = 0
    for c in range(copies):
        out |= word << (128 * c)
    return out


def rm_decode(block: int, copies: int = 3) -> int:
    """Maximum likelihood decoding with the fast Hadamard transform."""
    f = [0] * 128
    for c in range(copies):
        word = block >> (128 * c)
        for j in range(128):
            f[j] += 1 - 2 * ((word >> j) & 1)
    h = 1
    while h < 128:                               # in-place Walsh-Hadamard transform
        for i in range(0, 128, 2 * h):
            for j in range(i, i + h):
                a, b = f[j], f[j + h]
                f[j], f[j + h] = a + b, a - b
        h *= 2
    best = max(range(128), key=lambda u: abs(f[u]))
    return (best << 1) | (0 if f[best] > 0 else 1)


def code_encode(msg: bytes) -> int:
    """mG for the concatenated code: n1 n2 = 17664 bits."""
    out = 0
    for i, sym in enumerate(RS.encode(list(msg))):
        out |= rm_encode(sym) << (N2 * i)
    return out


def code_decode(word: int) -> Optional[bytes]:
    mask = (1 << N2) - 1
    syms = [rm_decode((word >> (N2 * i)) & mask) for i in range(N1)]
    m = RS.decode(syms)
    return None if m is None else bytes(m)


# ---------------------------------------------------------------- the ring

def rot(a: int, k: int, n: int = N) -> int:
    k %= n
    if k == 0:
        return a
    return ((a << k) | (a >> (n - k))) & ((1 << n) - 1)


def mul_sparse(a: int, supp: Sequence[int], n: int = N) -> int:
    out = 0
    for k in supp:
        out ^= rot(a, k, n)
    return out


def support(a: int) -> List[int]:
    return [i for i in range(a.bit_length()) if (a >> i) & 1]


def fixed_weight(seed: bytes, w: int, n: int = N) -> List[int]:
    """w distinct positions in [0, n) from SHAKE256, by rejection sampling."""
    bits = n.bit_length()
    pos: List[int] = []
    ln = 4 * w + 64
    i = 0
    stream = hashlib.shake_256(seed).digest(ln)
    while len(pos) < w:
        if i + 3 > len(stream):
            ln *= 2
            stream = hashlib.shake_256(seed).digest(ln)
        v = int.from_bytes(stream[i:i + 3], "little") & ((1 << bits) - 1)
        i += 3
        if v < n and v not in pos:
            pos.append(v)
    return pos


TRUNC = (1 << (N1 * N2)) - 1


# ---------------------------------------------------------------- the PKE

def keygen(rng: random.Random):
    h = rng.getrandbits(N)                                   # @line L1
    x = rng.sample(range(N), W)
    y = rng.sample(range(N), W)
    s = sum(1 << i for i in x) ^ mul_sparse(h, y)            # @line L2
    return (h, s), (x, y)                                    # @line L3


def encrypt(pk, m: bytes, theta: bytes) -> Tuple[int, int]:
    h, s = pk
    r1 = fixed_weight(b"r1" + theta, WR)                     # @line L4
    r2 = fixed_weight(b"r2" + theta, WR)
    e = sum(1 << i for i in fixed_weight(b"e" + theta, WE))
    u = sum(1 << i for i in r1) ^ mul_sparse(h, r2)          # @line L5
    v = (code_encode(m) ^ mul_sparse(s, r2) ^ e) & TRUNC
    return u, v                                              # @line L6


def decrypt(sk, c: Tuple[int, int]) -> Optional[bytes]:
    x, y = sk
    u, v = c
    return code_decode(v ^ (mul_sparse(u, y) & TRUNC))       # @line L7


# ---------------------------------------------------------------- the KEM (HHK with implicit rejection)

def nbytes(a: int, bits: int) -> bytes:
    return a.to_bytes((bits + 7) // 8, "little")


def pk_bytes(pk) -> bytes:
    return nbytes(pk[0], N) + nbytes(pk[1], N)


def hash_g(pk, m: bytes, salt: bytes) -> bytes:
    return hashlib.shake_256(b"G" + hashlib.sha3_256(pk_bytes(pk)).digest() + m + salt).digest(32)


def hash_k(m: bytes, c) -> bytes:
    u, v, salt = c
    return hashlib.sha3_256(b"K" + m + nbytes(u, N) + nbytes(v, N1 * N2) + salt).digest()


def kem_keygen(rng: random.Random):
    pk, sk = keygen(rng)
    return pk, (sk, pk, rng.randbytes(16))


def encaps(pk, rng: random.Random):
    m, salt = rng.randbytes(K1), rng.randbytes(16)           # @line L8
    u, v = encrypt(pk, m, hash_g(pk, m, salt))               # @line L9
    c = (u, v, salt)
    return c, hash_k(m, c)                                   # @line L10


def decaps(ksk, c) -> bytes:
    sk, pk, sigma = ksk
    u, v, salt = c
    m2 = decrypt(sk, (u, v))                                 # @line L11
    if m2 is not None and encrypt(pk, m2, hash_g(pk, m2, salt)) == (u, v):  # @line L12
        return hash_k(m2, c)                                 # @line L13
    return hash_k(sigma, c)
