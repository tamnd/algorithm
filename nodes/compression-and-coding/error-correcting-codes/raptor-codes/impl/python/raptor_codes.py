# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/raptor-codes/. The authors are listed in prov/GTWFNH.jsonl.
"""A small non-systematic Raptor code in the style of RFC 5053. It is NOT RFC 5053.

What follows RFC 5053 (Section 5.4.2.3, 5.4.4.2, 5.4.4.3):
  * the parameters X, S, H, L of the precode;
  * the precode: S LDPC symbols (each source symbol enters 3 of them) and H Half symbols
    (columns are Gray codes of weight ceil(H/2));
  * the degree table (Table 1) and the LT encoding symbol generator LTEnc (steps b, b + a,
    b + 2a, ... modulo the prime L' >= L, skipping values >= L).
What differs:
  * the triple (d, a, b) comes from Python's random module, not from the Rand[] tables V0, V1;
  * the code is not systematic: the first K intermediate symbols are the source symbols
    (RFC 5053 solves for intermediate symbols so that encoded symbols 0..K-1 equal the source);
  * the decoder is peeling followed by plain Gaussian elimination on what is left.
So the output does not interoperate with RFC 5053 and has no official test vectors.
"""

import math
import random
from typing import List, Optional, Sequence, Tuple

DEG_F = [0, 10241, 491582, 712794, 831695, 948446, 1032189, 1048576]  # RFC 5053 Table 1
DEG_D = [0, 1, 2, 3, 4, 10, 11, 40]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def prime_at_least(n: int) -> int:
    while not is_prime(n):
        n += 1
    return n


def popcount(x: int) -> int:
    return bin(x).count("1")


def rfc5053_params(k: int) -> Tuple[int, int, int, int]:
    """(X, S, H, L) of RFC 5053 Section 5.4.2.3."""
    x = 1
    while x * (x - 1) < 2 * k:
        x += 1
    s = prime_at_least(-(-k // 100) + x)
    h = 1
    while math.comb(h, -(-h // 2)) < k + s:
        h += 1
    return x, s, h, k + s + h


def gray_of_weight(w: int, count: int) -> List[int]:
    """The first count elements of m[w]: Gray codes g[i] = i ^ (i >> 1), i >= 1, with w ones."""
    out, i = [], 1
    while len(out) < count:
        g = i ^ (i >> 1)
        if popcount(g) == w:
            out.append(g)
        i += 1
    return out


def ldpc_triples(k: int, s: int):
    """For each source index i, the 3 LDPC symbols (offsets 0..S-1) it is XORed into."""
    for i in range(k):
        a = 1 + (i // s) % (s - 1)
        b = i % s
        out = []
        for _ in range(3):
            out.append(b)
            b = (b + a) % s
        yield i, out


def precode_rows(k: int) -> List[int]:
    """S + H constraints on the L intermediate symbols, as bit masks; each row XORs to zero."""
    _, s, h, _ = rfc5053_params(k)
    rows = [1 << (k + b) for b in range(s)]
    for i, bs in ldpc_triples(k, s):
        for b in bs:
            rows[b] ^= 1 << i
    m = gray_of_weight(-(-h // 2), k + s)
    for hh in range(h):
        row = 1 << (k + s + hh)
        for j in range(k + s):
            if m[j] >> hh & 1:
                row ^= 1 << j
        rows.append(row)
    return rows


def intermediate_symbols(source: Sequence[int]) -> List[int]:
    """C[0..L-1]: the source, then the S LDPC symbols, then the H Half symbols."""
    k = len(source)
    _, s, h, l = rfc5053_params(k)
    c = list(source) + [0] * (s + h)
    for i, bs in ldpc_triples(k, s):
        for b in bs:
            c[k + b] ^= c[i]
    m = gray_of_weight(-(-h // 2), k + s)
    for hh in range(h):
        for j in range(k + s):
            if m[j] >> hh & 1:
                c[k + s + hh] ^= c[j]
    return c


def degree(v: int) -> int:
    """Deg[v] of RFC 5053 Section 5.4.4.2, for 0 <= v < 2^20."""
    for j in range(1, 8):
        if v < DEG_F[j]:
            return DEG_D[j]
    raise ValueError("v out of range")


def triple(key: int, esi: int, lp: int) -> Tuple[int, int, int]:
    """(d, a, b) for encoding symbol esi. A stand-in for Trip[K, X] of RFC 5053."""
    rng = random.Random(key * (1 << 32) + esi)
    d = degree(rng.randrange(1 << 20))
    a = 1 + rng.randrange(lp - 1)
    b = rng.randrange(lp)
    return d, a, b


def lt_neighbors(d: int, a: int, b: int, l: int, lp: int) -> List[int]:
    """The intermediate symbols used by LTEnc of RFC 5053 Section 5.4.4.3."""
    while b >= l:
        b = (b + a) % lp
    out = [b]
    for _ in range(min(d - 1, l - 1)):
        b = (b + a) % lp
        while b >= l:
            b = (b + a) % lp
        out.append(b)
    return out


class RaptorCode:
    """precode=False gives the plain LT code with the same degrees (for comparison)."""

    def __init__(self, k: int, key: int = 0, precode: bool = True):
        self.k, self.key, self.precode = k, key, precode
        self.l = rfc5053_params(k)[3] if precode else k
        self.lp = prime_at_least(self.l)
        self.constraints = precode_rows(k) if precode else []

    def neighbors(self, esi: int) -> List[int]:
        return lt_neighbors(*triple(self.key, esi, self.lp), self.l, self.lp)

    def encode(self, source: Sequence[int], esis: Sequence[int]) -> List[int]:
        c = intermediate_symbols(source) if self.precode else list(source)
        out = []
        for esi in esis:
            v = 0
            for i in self.neighbors(esi):
                v ^= c[i]
            out.append(v)
        return out

    def decode(self, esis: Sequence[int], values: Sequence[int],
               peel_only: bool = False) -> Optional[List[int]]:
        """Returns the k source symbols, or None if the received symbols do not determine
        all L intermediate symbols (or if peeling stops, when peel_only is set)."""
        masks = list(self.constraints) + [sum(1 << i for i in self.neighbors(e)) for e in esis]
        vals = [0] * len(self.constraints) + list(values)
        known: List[Optional[int]] = [None] * self.l
        where: List[List[int]] = [[] for _ in range(self.l)]
        for r, m in enumerate(masks):
            for i in range(self.l):
                if m >> i & 1:
                    where[i].append(r)
        # phase 1: peeling (the LT decoder, also using the sparse LDPC rows)
        stack = [r for r, m in enumerate(masks) if popcount(m) == 1]
        while stack:
            r = stack.pop()
            if popcount(masks[r]) != 1:
                continue
            i = masks[r].bit_length() - 1
            known[i] = vals[r]
            for r2 in where[i]:
                if masks[r2] >> i & 1:
                    masks[r2] ^= 1 << i
                    vals[r2] ^= known[i]
                    if popcount(masks[r2]) == 1:
                        stack.append(r2)
        unknown = [i for i in range(self.l) if known[i] is None]
        if unknown and peel_only:
            return None
        # phase 2: Gaussian elimination on the rows that are left (unknown columns only)
        basis = {}
        for m, v in zip(masks, vals):
            while m:
                top = m.bit_length() - 1
                if top not in basis:
                    basis[top] = (m, v)
                    break
                m2, v2 = basis[top]
                m, v = m ^ m2, v ^ v2
        if len(basis) < len(unknown):
            return None
        for top in sorted(basis):  # lower unknowns are solved first
            m, v = basis[top]
            rest = m ^ (1 << top)
            i = 0
            while rest:
                if rest & 1:
                    v ^= known[i]
                rest >>= 1
                i += 1
            known[top] = v
        return known[:self.k]


def success_rate(k: int, extra: int, trials: int, seed: int, precode: bool = True,
                 peel_only: bool = False) -> float:
    """Fraction of trials that decode from k + extra encoded symbols with random ESIs."""
    ok = 0
    for t in range(trials):
        rng = random.Random(seed * 100003 + t)
        code = RaptorCode(k, key=seed * 1000 + t, precode=precode)
        source = [rng.getrandbits(16) for _ in range(k)]
        esis = rng.sample(range(20 * k), k + extra)  # the symbols that were not lost
        got = code.decode(esis, code.encode(source, esis), peel_only=peel_only)
        ok += got == source
    return ok / trials
