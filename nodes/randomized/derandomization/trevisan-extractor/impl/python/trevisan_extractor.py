# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trevisan-extractor/. The authors are listed in prov/ENJAWZ.jsonl.

"""Trevisan's extractor with a Hadamard code or a Reed-Solomon code concatenated with
the Hadamard code, and a polynomial design.

A string of bits is a tuple of 0s and 1s. The source x has n bits. The seed y has d
bits. A design is a list of sorted tuples of positions in range(d). A code is given
by a function code_bit(x, z) that returns bit z of the codeword of x, where z is a
tuple of l bits. The codeword is never built in full.
"""

from fractions import Fraction
from itertools import product
from typing import Callable, Dict, List, Sequence, Tuple

Bits = Tuple[int, ...]
CodeBit = Callable[[Bits, Bits], int]

# An irreducible polynomial of degree t over GF(2), for t = 1 .. 8.
IRREDUCIBLE = {
    1: 0b11,
    2: 0b111,
    3: 0b1011,
    4: 0b10011,
    5: 0b100101,
    6: 0b1000011,
    7: 0b10000011,
    8: 0x11B,
}


def gf_mul(a: int, b: int, t: int) -> int:
    """The product of a and b in GF(2^t) = GF(2)[u] / (IRREDUCIBLE[t])."""
    poly = IRREDUCIBLE[t]
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if (a >> t) & 1:
            a ^= poly
    return result


def to_int(bits: Sequence[int]) -> int:
    """Bit j of the result is bits[j]."""
    v = 0
    for j, b in enumerate(bits):
        v |= b << j
    return v


def inner(u: Sequence[int], v: Sequence[int]) -> int:
    return sum(a & b for a, b in zip(u, v)) & 1


def hadamard_bit(x: Bits, z: Bits) -> int:
    """Bit z of the Hadamard code of x: <x, z> mod 2. Here l = n."""
    return inner(x, z)


def rs_value(x: Bits, alpha: int, t: int) -> int:
    """p_x(alpha) in GF(2^t), where p_x has the coefficients x_0, x_1, ... of t bits each."""
    coeffs = [to_int(x[j : j + t]) for j in range(0, len(x), t)]
    v = 0
    for c in reversed(coeffs):  # Horner's rule
        v = gf_mul(v, alpha, t) ^ c
    return v


def rsh_bit(x: Bits, z: Bits, t: int) -> int:
    """Bit z of the Reed-Solomon code concatenated with the Hadamard code.

    z has 2t bits: alpha is the first t, beta the last t. The bit is <p_x(alpha), beta>.
    The source length n must be a multiple of t, with n / t <= 2^t."""
    alpha = to_int(z[:t])  # @line L5
    v = rs_value(x, alpha, t)  # @line L6
    return inner([(v >> j) & 1 for j in range(t)], z[t:])  # @line L7


def codeword(x: Bits, code_bit: CodeBit, ell: int) -> Bits:
    """The full codeword, with positions z in the order of product((0, 1), repeat=ell)."""
    return tuple(code_bit(x, z) for z in product((0, 1), repeat=ell))


def polynomial_design(q: int, r: int, ell: int) -> List[Tuple[int, ...]]:
    """The sets {(alpha, p(alpha)) : alpha < ell} for all p over GF(q) of degree < r.

    q is prime and r <= ell <= q. The point (alpha, beta) has number alpha * q + beta,
    so d = ell * q. There are q^r sets of size ell, and two of them share at most
    r - 1 points."""
    design = []
    for coeffs in product(range(q), repeat=r):
        s = []
        for alpha in range(ell):
            v = 0
            for c in reversed(coeffs):
                v = (v * alpha + c) % q
            s.append(alpha * q + v)
        design.append(tuple(s))
    return design


def max_intersection(design: Sequence[Sequence[int]]) -> int:
    sets = [set(s) for s in design]
    return max((len(sets[i] & sets[j]) for i in range(len(sets)) for j in range(i + 1, len(sets))), default=0)


def restrict(y: Sequence[int], s: Sequence[int]) -> Bits:
    return tuple(y[p] for p in s)


def trevisan(x: Bits, y: Bits, design: Sequence[Sequence[int]], code_bit: CodeBit) -> Bits:
    """Trevisan's extractor: output bit i is bit y|S_i of the codeword of x.

    The codeword is read one bit at a time through code_bit."""
    out = []
    for s in design:  # @line L1
        z = restrict(y, s)  # @line L2
        out.append(code_bit(x, z))  # @line L3
    return tuple(out)  # @line L4


def strong_distance(
    source: Dict[Bits, Fraction], design: Sequence[Sequence[int]], code_bit: CodeBit, d: int
) -> Fraction:
    """The exact distance between (Y, Ext(X, Y)) and (Y, U_m)."""
    m = len(design)
    u = Fraction(1, 1 << m)
    total = Fraction(0)
    for y in product((0, 1), repeat=d):
        out: Dict[Bits, Fraction] = {}
        for x, p in source.items():
            o = trevisan(x, y, design, code_bit)
            out[o] = out.get(o, Fraction(0)) + p
        total += sum((abs(out.get(o, Fraction(0)) - u) for o in product((0, 1), repeat=m)), Fraction(0)) / 2
    return total / (1 << d)


def hybrid_probs(
    x: Bits, design: Sequence[Sequence[int]], code_bit: CodeBit, d: int, test: Callable[[Bits], int]
) -> List[Fraction]:
    """p_j = Pr[test(Ext(x, Y)_1..j, uniform rest) = 1] for j = 0..m, exactly."""
    m = len(design)
    outs = [trevisan(x, y, design, code_bit) for y in product((0, 1), repeat=d)]
    probs = []
    for j in range(m + 1):
        hits = 0
        for o in outs:
            for tail in product((0, 1), repeat=m - j):
                hits += test(o[:j] + tail)
        probs.append(Fraction(hits, len(outs) << (m - j)))
    return probs


def reconstruct(
    x: Bits,
    design: Sequence[Sequence[int]],
    code_bit: CodeBit,
    test: Callable[[Bits], int],
    i: int,
    w: Sequence[int],
    r: Sequence[int],
) -> Tuple[Callable[[Bits], int], List[Dict[Bits, int]]]:
    """The word R of the reconstruction proof, for position i (1-based).

    w holds the seed bits outside S_i (values on S_i are ignored) and r = (r_i .. r_m).
    For j < i, the table g_j maps the bits of z on S_i and S_j together to output bit
    j. R(z) is computed from the tables and r alone, never from x."""
    s_i = design[i - 1]
    tables: List[Dict[Bits, int]] = []
    for j in range(i - 1):
        common = [k for k, pos in enumerate(s_i) if pos in design[j]]
        table: Dict[Bits, int] = {}
        for z in product((0, 1), repeat=len(s_i)):
            y = list(w)
            for pos, bit in zip(s_i, z):
                y[pos] = bit
            key = tuple(z[k] for k in common)
            table[key] = code_bit(x, restrict(y, design[j]))
        tables.append(table)
    commons = [[k for k, pos in enumerate(s_i) if pos in design[j]] for j in range(i - 1)]

    def word(z: Bits) -> int:
        prefix = tuple(tables[j][tuple(z[k] for k in commons[j])] for j in range(i - 1))
        return r[0] if test(prefix + tuple(r)) else 1 - r[0]

    return word, tables


def agreement(word: Callable[[Bits], int], x: Bits, code_bit: CodeBit, ell: int) -> Fraction:
    zs = list(product((0, 1), repeat=ell))
    return Fraction(sum(1 for z in zs if word(z) == code_bit(x, z)), len(zs))


def list_decode(
    word: Callable[[Bits], int], n: int, code_bit: CodeBit, ell: int, threshold: Fraction
) -> List[Bits]:
    """All messages whose codeword agrees with word on more than threshold of the positions."""
    return [x for x in product((0, 1), repeat=n) if agreement(word, x, code_bit, ell) > threshold]
