# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crc-generator-polynomial/. The authors are listed in prov/TY4M8X.jsonl.

"""CRC generator polynomials: notations, factorization over GF(2), and the
Hamming distance profile by exhaustive search.

A polynomial is an int, bit i the coefficient of x^i. The full generator G
of degree r has both the x^r and the x^0 term.
"""

import random
from itertools import combinations

# ---- notations -------------------------------------------------------------


def reflect(value: int, width: int) -> int:
    out = 0
    for _ in range(width):
        out = (out << 1) | (value & 1)
        value >>= 1
    return out


def from_normal(normal: int, r: int) -> int:
    """Normal notation: G without the x^r term (0x04C11DB7 for CRC-32)."""
    return (1 << r) | normal


def to_normal(g: int) -> int:
    return g ^ (1 << (g.bit_length() - 1))


def from_reversed(rev: int, r: int) -> int:
    """Reversed notation: the normal notation with its r bits in reverse
    order (0xEDB88320 for CRC-32), as used in right-shifting code."""
    return from_normal(reflect(rev, r), r)


def to_reversed(g: int) -> int:
    r = g.bit_length() - 1
    return reflect(to_normal(g), r)


def from_koopman(k: int, r: int) -> int:
    """Koopman notation: G without the x^0 term, shifted right by one
    (0x82608EDB for CRC-32). The top bit shows the degree."""
    return (k << 1) | 1


def to_koopman(g: int) -> int:
    return g >> 1


def reciprocal(g: int) -> int:
    """x^r G(1/x): the polynomial with the coefficients in reverse order."""
    return reflect(g, g.bit_length())


# ---- GF(2)[x] arithmetic -------------------------------------------------


def deg(a: int) -> int:
    return a.bit_length() - 1


def pmod(a: int, m: int) -> int:
    dm = deg(m)
    while a and deg(a) >= dm:
        a ^= m << (deg(a) - dm)
    return a


def pdiv(a: int, m: int) -> int:
    q, dm = 0, deg(m)
    while a and deg(a) >= dm:
        s = deg(a) - dm
        q |= 1 << s
        a ^= m << s
    return q


def pmul(a: int, b: int) -> int:
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def mulmod(a: int, b: int, m: int) -> int:
    return pmod(pmul(a, b), m)


def powmod(a: int, e: int, m: int) -> int:
    r, a = 1, pmod(a, m)
    while e:
        if e & 1:
            r = mulmod(r, a, m)
        a = mulmod(a, a, m)
        e >>= 1
    return pmod(r, m)


def pgcd(a: int, b: int) -> int:
    while b:
        a, b = b, pmod(a, b)
    return a


def derivative(a: int) -> int:
    # d/dx x^i = i x^(i-1): only odd i survive in characteristic 2.
    return (a >> 1) & int("01" * ((a.bit_length() + 1) // 2 + 1), 2)


def _equal_degree_split(f: int, d: int, rng: random.Random) -> list[int]:
    """Split a product of irreducible factors, all of degree d (Cantor and
    Zassenhaus, characteristic 2 form with the trace map)."""
    if deg(f) == d:
        return [f]
    while True:
        a = rng.getrandbits(deg(f)) | 2
        t, s = a, a
        for _ in range(d - 1):
            s = mulmod(s, s, f)
            t ^= s
        g = pgcd(f, t)
        if 0 < deg(g) < deg(f):
            return _equal_degree_split(g, d, rng) + _equal_degree_split(pdiv(f, g), d, rng)


def factor(f: int, seed: int = 1) -> list[int]:
    """Irreducible factors of f, with repetition, sorted by degree then value."""
    rng = random.Random(seed)
    out: list[int] = []
    # Square-free part: in characteristic 2, f' = 0 means f is a square.
    stack = [f]
    while stack:
        g = stack.pop()
        if deg(g) < 1:
            continue
        dg = derivative(g)
        if dg == 0:
            # g = h^2 with h the polynomial of the even coefficients.
            h = 0
            for i in range(0, deg(g) + 1, 2):
                if (g >> i) & 1:
                    h |= 1 << (i // 2)
            stack += [h, h]
            continue
        c = pgcd(g, dg)
        if deg(c) > 0:
            stack += [c, pdiv(g, c)]
            continue
        # g is square-free: distinct-degree factorization.
        x_pow, d = 2, 0
        while deg(g) > 0:
            d += 1
            if 2 * d > deg(g):
                out.append(g)
                break
            x_pow = mulmod(x_pow, x_pow, g)
            h = pgcd(g, x_pow ^ 2)
            if deg(h) > 0:
                out += _equal_degree_split(h, d, rng)
                g = pdiv(g, h)
                x_pow = pmod(x_pow, g)
    return sorted(out, key=lambda p: (deg(p), p))


def prime_factors(n: int) -> list[int]:
    ps, p = [], 2
    while p * p <= n:
        if n % p == 0:
            ps.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        ps.append(n)
    return ps


def order_of_x(f: int) -> int:
    """The least e > 0 with x^e = 1 mod f, for f(0) = 1, by trying the
    divisors of the order of the group. Works when f is irreducible."""
    d = deg(f)
    e = (1 << d) - 1
    for p in prime_factors(e):
        while e % p == 0 and powmod(2, e // p, f) == 1:
            e //= p
    return e


def is_primitive(f: int) -> bool:
    return len(factor(f)) == 1 and order_of_x(f) == (1 << deg(f)) - 1


# ---- Hamming distance profile ------------------------------------------


def min_distance_by_length(g: int, max_data_bits: int) -> list[int]:
    """d[L] = minimum weight of a nonzero codeword with L data bits, for
    L = 1 .. max_data_bits (d[0] is unused). Exhaustive over all error
    patterns of each weight, made fast with syndromes s_i = x^i mod G: a
    pattern is a codeword exactly when its syndromes XOR to 0. A codeword of
    length N that does not use position N - 1 is a codeword of length N - 1,
    so only patterns that use the new position need a check."""
    r = deg(g)
    s = [pmod(1 << i, g) for i in range(max_data_bits + r)]
    singles: set[int] = set()
    pairs: set[int] = set()
    best = bin(g).count("1")  # weight of G itself, the codeword with L = 1
    d = [0]
    for n in range(max_data_bits + r):
        new = s[n]
        if n >= r:  # positions 0 .. n form a codeword of length n + 1
            for w in range(2, best):
                t = w - 1  # number of other positions
                if t == 1:
                    hit = new in singles
                elif t == 2:
                    hit = new in pairs
                elif t == 3:
                    hit = any((new ^ s[j]) in pairs for j in range(n))
                else:
                    hit = any(_xor(s, c) == new for c in combinations(range(n), t))
                if hit:
                    best = w
                    break
            d.append(best)
        for j in range(n):
            pairs.add(new ^ s[j])
        singles.add(new)
    return d


def _xor(s: list[int], idx: tuple[int, ...]) -> int:
    v = 0
    for i in idx:
        v ^= s[i]
    return v


def hd_profile(g: int, max_data_bits: int) -> list[int]:
    """Koopman's list: for HD = 3, 4, 5, ..., the largest data length in
    bits (at most max_data_bits) at which the code still has that HD."""
    d = min_distance_by_length(g, max_data_bits)
    out = []
    h = 3
    while True:
        lengths = [L for L in range(1, len(d)) if d[L] >= h]
        if not lengths:
            return out
        out.append(max(lengths))
        h += 1


def min_distance_brute(g: int, data_bits: int) -> int:
    """Minimum weight over all 2^L - 1 nonzero multiples of G with L data bits."""
    return min(bin(pmul(m, g)).count("1") for m in range(1, 1 << data_bits))
