# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goppa-code/. The authors are listed in prov/WVJW9K.jsonl.
"""Binary Goppa codes Gamma(L, g) and Patterson's decoder.

The support L = (a_0, ..., a_{n-1}) is a list of distinct elements of GF(2^m)
and the Goppa polynomial g in GF(2^m)[x] has degree t and no root in L.
A binary word c of length n is in Gamma(L, g) exactly when

    S_c(x) = sum_i c_i / (x - a_i)  is 0 modulo g(x),

where 1 / (x - a) is the inverse of x - a in GF(2^m)[x] / (g). Equivalently,
H c = 0 for the t x n matrix H[i][j] = a_j^i / g(a_j) over GF(2^m), and
over GF(2) after each entry is written as m bits.

Binary words are lists of 0 and 1, or ints whose bit j is position j.
"""

from gf import GF2m


def check_goppa(f: GF2m, support: list[int], g: list[int]) -> None:
    """Raise ValueError unless the support is distinct and g has degree >= 1 and no root in it."""
    if len(set(support)) != len(support):
        raise ValueError("the support must have distinct elements")
    if len(f.trim(g)) < 2:
        raise ValueError("g must have degree at least 1")
    if any(f.peval(g, a) == 0 for a in support):
        raise ValueError("g must have no root in the support")


def parity_check(f: GF2m, support: list[int], g: list[int]) -> list[list[int]]:
    """The t x n matrix H[i][j] = a_j^i / g(a_j) over GF(2^m)."""
    check_goppa(f, support, g)
    t = len(f.trim(g)) - 1
    inv_g = [f.inv(f.peval(g, a)) for a in support]
    return [[f.mul(f.pow(a, i) if a or i else 1, h) for a, h in zip(support, inv_g)] for i in range(t)]


def binary_parity_check(f: GF2m, support: list[int], g: list[int]) -> list[int]:
    """The m t rows over GF(2) of the expanded H, each an int with bit j for position j."""
    h = parity_check(f, support, g)
    rows = []
    for row in h:
        for bit in range(f.m):
            rows.append(sum(((v >> bit) & 1) << j for j, v in enumerate(row)))
    return rows


def gf2_nullspace(rows: list[int], n: int) -> list[int]:
    """A basis of {c : popcount(row & c) is even for every row}, as ints of n bits."""
    pivots: dict[int, int] = {}  # pivot column -> row; no row has another row's pivot bit
    for r in rows:
        for col, pr in pivots.items():
            if (r >> col) & 1:
                r ^= pr
        if r == 0:
            continue
        col = (r & -r).bit_length() - 1
        for c2 in pivots:
            if (pivots[c2] >> col) & 1:
                pivots[c2] ^= r
        pivots[col] = r
    free = [j for j in range(n) if j not in pivots]
    basis = []
    for j in free:
        v = 1 << j
        for col, pr in pivots.items():
            if (pr >> j) & 1:
                v |= 1 << col
        basis.append(v)
    return basis


def goppa_basis(f: GF2m, support: list[int], g: list[int]) -> list[int]:
    """A basis of the binary Goppa code Gamma(L, g); its size is the dimension k >= n - m t."""
    return gf2_nullspace(binary_parity_check(f, support, g), len(support))


def pinv_mod(f: GF2m, a: list[int], g: list[int]) -> list[int] | None:
    """The inverse of a modulo g by the extended Euclidean algorithm, or None if gcd(a, g) != 1."""
    r0, r1 = f.trim(g), f.pmod(a, g)
    v0, v1 = [], [1]
    while r1:
        q, rem = f.pdivmod(r0, r1)
        r0, r1 = r1, rem
        v0, v1 = v1, f.padd(v0, f.pmul(q, v1))
    if len(r0) != 1:
        return None
    return f.pmod(f.pscale(v0, f.inv(r0[0])), g)


def syndrome(f: GF2m, support: list[int], g: list[int], word: list[int]) -> list[int]:
    """S(x) = sum over c_i = 1 of 1 / (x - a_i) modulo g (in characteristic 2, x - a = x + a)."""
    s: list[int] = []
    for a, bit in zip(support, word):
        if bit:
            inv = pinv_mod(f, [a, 1], g)
            assert inv is not None  # g(a) != 0, so x + a is a unit
            s = f.padd(s, inv)
    return s


def is_codeword(f: GF2m, support: list[int], g: list[int], word: list[int]) -> bool:
    return not syndrome(f, support, g, word)


def psqrt_mod(f: GF2m, a: list[int], g: list[int]) -> list[int]:
    """The square root of a in GF(2^m)[x] / (g) for g irreducible of degree t: a^(2^(m t - 1))."""
    t = len(f.trim(g)) - 1
    r = f.pmod(a, g)
    for _ in range(f.m * t - 1):
        r = f.pmod(f.pmul(r, r), g)
    return r


def patterson(f: GF2m, support: list[int], g: list[int], word: list[int]) -> list[int] | None:
    """Patterson's algorithm: the positions of an error of weight <= t, or None for a detected failure.

    Precondition: g is irreducible of degree t over GF(2^m) and the support has no root of g.
    Then every error of weight at most t is found.
    Cost: O(t^2) per multiplication modulo g, O(m t) of them for the square root,
    O(t^2) for the Euclidean step and O(n t) for the root search.
    """
    t = len(f.trim(g)) - 1
    s = syndrome(f, support, g, word)
    if not s:
        return []
    tinv = pinv_mod(f, s, g)  # T = S^-1 mod g
    if tinv is None:
        return None
    tx = f.padd(tinv, [0, 1])  # T + x
    if not tx:
        sigma = [0, 1]  # sigma = x: one error at the support element 0
    else:
        r = psqrt_mod(f, tx, g)  # R^2 = T + x mod g
        # Euclid on (g, R), keeping b_i R = r_i mod g, until deg r_i <= t / 2.
        r0, r1 = f.trim(g), r
        b0, b1 = [], [1]
        while len(r1) - 1 > t // 2:
            q, rem = f.pdivmod(r0, r1)
            r0, r1 = r1, rem
            b0, b1 = b1, f.padd(b0, f.pmul(q, b1))
        a, b = r1, b1
        sigma = f.padd(f.pmul(a, a), f.pmul([0, 1], f.pmul(b, b)))  # sigma = a^2 + x b^2
    deg = len(sigma) - 1
    pos = [i for i, a in enumerate(support) if f.peval(sigma, a) == 0]
    if len(pos) != deg or deg > t:
        return None
    return pos


def decode(f: GF2m, support: list[int], g: list[int], word: list[int]) -> list[int] | None:
    """The codeword within distance t of the word, by Patterson's algorithm, or None."""
    pos = patterson(f, support, g, word)
    if pos is None:
        return None
    c = list(word)
    for i in pos:
        c[i] ^= 1
    return c if is_codeword(f, support, g, c) else None
