# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sobol-sequence/. The authors are listed in prov/Z7GN5H.jsonl.

"""Sobol points in Gray-code order (Antonov and Saleev), with the direction numbers of
Joe and Kuo (2008), file new-joe-kuo-6.21201, for dimensions 2 to 21.

Coordinates are integers X with 0 <= X < 2^W; the point is X / 2^W.
"""

W = 32
MASK = (1 << W) - 1

# (s, a, [m_1, ..., m_s]) for dimensions 2, 3, ..., 21. The primitive polynomial is
# x^s + a_1 x^(s-1) + ... + a_(s-1) x + 1, where a = a_1 a_2 ... a_(s-1) in binary.
JOE_KUO = [
    (1, 0, [1]),
    (2, 1, [1, 3]),
    (3, 1, [1, 3, 1]),
    (3, 2, [1, 1, 1]),
    (4, 1, [1, 1, 3, 3]),
    (4, 4, [1, 3, 5, 13]),
    (5, 2, [1, 1, 5, 5, 17]),
    (5, 4, [1, 1, 5, 5, 5]),
    (5, 7, [1, 1, 7, 11, 19]),
    (5, 11, [1, 1, 5, 1, 1]),
    (5, 13, [1, 1, 1, 3, 11]),
    (5, 14, [1, 3, 5, 5, 31]),
    (6, 1, [1, 3, 3, 9, 7, 49]),
    (6, 13, [1, 1, 1, 15, 21, 21]),
    (6, 16, [1, 3, 1, 13, 27, 49]),
    (6, 19, [1, 1, 1, 15, 7, 5]),
    (6, 22, [1, 3, 1, 15, 13, 25]),
    (6, 25, [1, 1, 5, 5, 19, 61]),
    (7, 1, [1, 3, 7, 11, 23, 15, 103]),
    (7, 4, [1, 3, 7, 13, 13, 15, 69]),
]
MAX_DIM = 1 + len(JOE_KUO)


def polynomial(s: int, a: int) -> int:
    """The primitive polynomial of a dimension as a bit mask (bit i is the coefficient of x^i)."""
    return (1 << s) | (a << 1) | 1


def direction_numbers(s: int, a: int, m: list[int], bits: int = W) -> list[int]:
    """V[1..bits] (V[0] unused): V[k] = m_k 2^(bits-k), with m_k from the Sobol recurrence
    m_k = 2 a_1 m_(k-1) xor 4 a_2 m_(k-2) xor ... xor 2^s m_(k-s) xor m_(k-s)."""
    v = [0] * (bits + 1)
    for k in range(1, bits + 1):
        if k <= s:
            v[k] = m[k - 1] << (bits - k)
        else:
            x = v[k - s] ^ (v[k - s] >> s)
            for i in range(1, s):
                if (a >> (s - 1 - i)) & 1:
                    x ^= v[k - i]
            v[k] = x
    return v


def direction_table(dims: int, bits: int = W) -> list[list[int]]:
    if not 1 <= dims <= MAX_DIM:
        raise ValueError(f"dims must be between 1 and {MAX_DIM}")
    table = [[0] + [1 << (bits - k) for k in range(1, bits + 1)]]  # dimension 1: all m_k = 1
    for s, a, m in JOE_KUO[: dims - 1]:
        table.append(direction_numbers(s, a, m, bits))
    return table


class Sobol:
    """The Sobol sequence in Gray-code order: X_0 = 0, X_(n+1) = X_n xor V[c(n)]."""

    def __init__(self, dims: int, bits: int = W):
        self.bits = bits
        self.v = direction_table(dims, bits)
        self.x = [0] * dims
        self.n = 0

    def next_int(self) -> list[int]:
        if self.n >= 1 << self.bits:
            raise OverflowError("only 2^bits points are available")
        out = list(self.x)  # @line L1
        c, k = 1, self.n  # @line L2
        while k & 1:  # @line L3
            k >>= 1
            c += 1
        if c <= self.bits:  # the last point, of index 2^bits - 1, has no successor
            for j, vj in enumerate(self.v):  # @line L4
                self.x[j] ^= vj[c]
        self.n += 1  # @line L5
        return out  # @line L6

    def next(self) -> list[float]:
        return [x / (1 << self.bits) for x in self.next_int()]

    def skip_to(self, n: int) -> None:
        """Jump to index n in O(dims * bits) operations: X_n is the point of index gray(n)."""
        self.x = sobol_point(n ^ (n >> 1), len(self.v), self.bits)
        self.n = n


def sobol_point(i: int, dims: int, bits: int = W) -> list[int]:
    """The Sobol point of index i in natural order: the xor of V[k] over the set bits k of i."""
    table = direction_table(dims, bits)
    out = []
    for vj in table:
        x, k, r = 0, 1, i
        while r:
            if r & 1:
                x ^= vj[k]
            r >>= 1
            k += 1
        out.append(x & ((1 << bits) - 1))
    return out


# ---------------------------------------------------------------- GF(2) tools


def poly_mulmod(p: int, q: int, f: int) -> int:
    deg = f.bit_length() - 1
    r = 0
    while q:
        if q & 1:
            r ^= p
        q >>= 1
        p <<= 1
        if (p >> deg) & 1:
            p ^= f
    return r


def poly_powmod(p: int, e: int, f: int) -> int:
    r = 1
    while e:
        if e & 1:
            r = poly_mulmod(r, p, f)
        p = poly_mulmod(p, p, f)
        e >>= 1
    return r


def prime_factors(n: int) -> list[int]:
    out, d = [], 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def is_primitive(f: int) -> bool:
    """Exact test: x has order 2^deg - 1 modulo f over GF(2)."""
    deg = f.bit_length() - 1
    if deg < 1 or not f & 1:
        return False
    order = (1 << deg) - 1
    if poly_powmod(2, order, f) != 1:
        return False
    return all(poly_powmod(2, order // q, f) != 1 for q in prime_factors(order))


def generator_rows(v: list[int], bits: int, m: int) -> list[int]:
    """Rows of the generator matrix restricted to the first m columns: row r (r = 1..bits) is a
    bit mask over k = 1..m with bit k-1 set when digit r of V[k] is 1."""
    rows = []
    for r in range(1, bits + 1):
        row = 0
        for k in range(1, m + 1):
            if (v[k] >> (bits - r)) & 1:
                row |= 1 << (k - 1)
        rows.append(row)
    return rows


def gf2_rank(rows: list[int]) -> int:
    basis: dict[int, int] = {}
    for x in rows:
        while x:
            h = x.bit_length() - 1
            if h in basis:
                x ^= basis[h]
            else:
                basis[h] = x
                break
    return len(basis)


def _compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in _compositions(total - first, parts - 1):
            yield (first,) + rest


def t_value(dims: int, m: int, bits: int = W) -> int:
    """The least t such that every aligned block of 2^m points is a (t, m, dims)-net:
    for all d_1 + ... + d_dims = m - t, the top d_j rows of the generator matrices
    (first m columns) are linearly independent."""
    table = direction_table(dims, bits)
    gens = [generator_rows(v, bits, m) for v in table]
    for t in range(m + 1):
        if all(
            gf2_rank([row for j, d in enumerate(ds) for row in gens[j][:d]]) == m - t
            for ds in _compositions(m - t, dims)
        ):
            return t
    return m
