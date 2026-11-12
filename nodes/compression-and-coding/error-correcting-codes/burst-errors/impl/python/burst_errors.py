# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burst-errors/. The authors are listed in prov/0R3JDV.jsonl.
"""Burst errors: their length, the burst-correcting power of a binary linear code, the Reiger
bound, a Fire code, the binary image of a Reed-Solomon code, and the Gilbert-Elliott channel.

Binary words and polynomials over GF(2) are Python integers (bit i is position i, or the
coefficient of x^i).
"""

import random
from itertools import combinations, product
from math import lcm
from typing import Iterator, List, Sequence, Tuple


# ---- bursts ---------------------------------------------------------------

def burst_length(e: int) -> int:
    """Length of the shortest window holding all nonzero positions (first to last); 0 for e = 0."""
    if e == 0:
        return 0
    low = (e & -e).bit_length() - 1
    return e.bit_length() - low


def cyclic_burst_length(e: int, n: int) -> int:
    """Burst length when the n positions wrap around (an end-around burst): least over rotations."""
    if e == 0:
        return 0
    mask = (1 << n) - 1
    best = n
    for s in range(n):
        rot = ((e >> s) | (e << (n - s))) & mask
        best = min(best, burst_length(rot))
    return best


def bursts(n: int, b: int, cyclic: bool = False) -> Iterator[int]:
    """All nonzero binary patterns of length n whose (cyclic) burst length is at most b."""
    seen = set()
    for length in range(1, b + 1):
        for start in range(n if cyclic else n - length + 1):
            inner = length - 2
            for mid in range(1 << max(inner, 0)):
                if length == 1:
                    pos = [start]
                else:
                    pos = [start, start + length - 1] + [start + 1 + i for i in range(inner) if mid >> i & 1]
                e = 0
                for p in pos:
                    e |= 1 << (p % n)
                if e not in seen:
                    seen.add(e)
                    yield e


def count_bursts_of_length(n: int, b: int) -> int:
    """Number of binary patterns of length n with burst length exactly b (no wrap)."""
    if b == 1:
        return n
    return (n - b + 1) * 2 ** (b - 2)


# ---- linear codes and cosets --------------------------------------------

def reduce_basis(rows: Sequence[int]) -> List[int]:
    """A basis of the span with distinct leading bits, sorted from largest to smallest."""
    basis: List[int] = []
    for v in rows:
        for b in basis:
            v = min(v, v ^ b)
        if v:
            basis.append(v)
            basis.sort(reverse=True)
    return basis


def coset_leader_key(basis: Sequence[int], e: int) -> int:
    """A canonical member of the coset e + C: e with the leading bits of the basis cleared."""
    for b in basis:
        e = min(e, e ^ b)
    return e


def corrects_bursts(rows: Sequence[int], n: int, b: int, cyclic: bool = False) -> bool:
    """True if all bursts of length <= b lie in different cosets of the code (so a decoder can
    correct each one): equivalently, no nonzero codeword is the sum of two such bursts."""
    basis = reduce_basis(rows)
    keys = {0}  # the zero pattern (no error) lies in the code itself
    for e in bursts(n, b, cyclic):
        k = coset_leader_key(basis, e)
        if k in keys:
            return False
        keys.add(k)
    return True


def max_correctable_burst(rows: Sequence[int], n: int) -> int:
    b = 0
    while b < n and corrects_bursts(rows, n, b + 1):
        b += 1
    return b


def all_binary_linear_codes(n: int) -> Iterator[List[int]]:
    """Every subspace of GF(2)^n of dimension 1 .. n - 1, once, by its reduced row echelon basis."""
    for k in range(1, n):
        for pivots in combinations(range(n), k):
            free = [(i, j) for i, pc in enumerate(pivots) for j in range(pc + 1, n) if j not in pivots]
            for bitsv in product((0, 1), repeat=len(free)):
                rows = [1 << pc for pc in pivots]
                for (i, j), v in zip(free, bitsv):
                    if v:
                        rows[i] |= 1 << j
                yield rows


# ---- polynomials over GF(2) and a Fire code -----------------------------

def poly_mul(a: int, b: int) -> int:
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        b >>= 1
    return out


def poly_mod(a: int, m: int) -> int:
    dm = m.bit_length() - 1
    while a and a.bit_length() - 1 >= dm:
        a ^= m << (a.bit_length() - 1 - dm)
    return a


def poly_period(p: int) -> int:
    """The least e >= 1 with p(x) dividing x^e + 1 (p with nonzero constant term)."""
    e, power = 1, poly_mod(0b10, p)
    while power != 1:
        power = poly_mod(power << 1, p)
        e += 1
    return e


def fire_code(b: int, p: int) -> Tuple[int, int, int]:
    """Generator g(x) = (x^(2b-1) + 1) p(x) of the Fire code, with n = lcm(2b - 1, e) and k = n - deg g.

    p must be irreducible of degree m >= b, and its period e must not divide 2b - 1.
    The code corrects every burst of length at most b.
    """
    e = poly_period(p)
    if (2 * b - 1) % e == 0:
        raise ValueError("the period of p(x) must not divide 2b - 1")
    g = poly_mul((1 << (2 * b - 1)) | 1, p)
    n = lcm(2 * b - 1, e)
    return g, n, n - (g.bit_length() - 1)


def cyclic_code_rows(g: int, n: int) -> List[int]:
    """Generator rows x^i g(x), i = 0 .. k - 1, of the cyclic code of length n."""
    k = n - (g.bit_length() - 1)
    return [g << i for i in range(k)]


# ---- GF(2^m) and the binary image of a Reed-Solomon code ----------------

def gf_tables(m: int, prim: int) -> Tuple[List[int], List[int]]:
    """Exponential and logarithm tables of GF(2^m) built from a primitive polynomial."""
    size = 1 << m
    exp = [0] * (2 * size)
    log = [0] * size
    x = 1
    for i in range(size - 1):
        exp[i] = x
        log[x] = i
        x <<= 1
        if x & size:
            x ^= prim
    for i in range(size - 1, 2 * size):
        exp[i] = exp[i - (size - 1)]
    return exp, log


def rs_codewords(m: int, prim: int, k: int) -> List[List[int]]:
    """All codewords (lists of n = 2^m - 1 symbols) of the narrow-sense RS code of dimension k,
    generated by g(x) = (x - a)(x - a^2)...(x - a^(n-k)), as m(x) g(x)."""
    exp, log = gf_tables(m, prim)
    n = (1 << m) - 1

    def mul(a: int, b: int) -> int:
        return 0 if a == 0 or b == 0 else exp[log[a] + log[b]]

    g = [1]
    for i in range(1, n - k + 1):
        root = exp[i]
        ng = [0] * (len(g) + 1)
        for j, c in enumerate(g):
            ng[j] ^= mul(c, root)  # constant part: c * a^i (minus is plus in characteristic 2)
            ng[j + 1] ^= c
        g = ng
    words = []
    for msg in product(range(1 << m), repeat=k):
        c = [0] * n
        for i, mi in enumerate(msg):
            if mi:
                for j, gj in enumerate(g):
                    c[i + j] ^= mul(mi, gj)
        words.append(c)
    return words


def binary_image(word: Sequence[int], m: int) -> int:
    """Concatenate the m-bit symbols: symbol j occupies bits j m .. j m + m - 1."""
    out = 0
    for j, s in enumerate(word):
        out |= s << (j * m)
    return out


def symbols_hit(e: int, m: int) -> int:
    """The number of m-bit symbols that a binary error pattern touches."""
    count = 0
    while e:
        if e & ((1 << m) - 1):
            count += 1
        e >>= m
    return count


# ---- the Gilbert-Elliott channel -----------------------------------------

def gilbert_elliott(n: int, p_gb: float, p_bg: float, e_good: float, e_bad: float,
                    rng: random.Random) -> List[int]:
    """Error bits from a two-state Markov channel, started in its stationary law.

    In state G a bit is in error with probability e_good, in state B with probability e_bad.
    After each bit the state moves G -> B with probability p_gb and B -> G with probability p_bg.
    Gilbert's model has e_good = 0; Elliott's allows errors in both states.
    """
    bad = rng.random() < p_gb / (p_gb + p_bg)
    out = []
    for _ in range(n):
        out.append(1 if rng.random() < (e_bad if bad else e_good) else 0)
        if bad:
            bad = rng.random() >= p_bg
        else:
            bad = rng.random() < p_gb
    return out


def gilbert_elliott_error_rate(p_gb: float, p_bg: float, e_good: float, e_bad: float) -> float:
    """Average bit error rate: pi_G e_good + pi_B e_bad with pi_B = p_gb / (p_gb + p_bg)."""
    pi_b = p_gb / (p_gb + p_bg)
    return (1 - pi_b) * e_good + pi_b * e_bad
