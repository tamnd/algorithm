# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/golay-code/. The authors are listed in prov/Q2MXRM.jsonl.

"""The binary Golay codes [23, 12, 7] and [24, 12, 8] and the ternary Golay code
[11, 6, 5]_3: cyclic encoding, a syndrome table decoder for the perfect code, and the
arithmetic decoder for the extended code.

Binary words and GF(2) polynomials are ints: bit i is position i, or the coefficient of x^i.
"""

from itertools import product

# g(x) = x^11 + x^10 + x^6 + x^5 + x^4 + x^2 + 1
GOLAY_G = (1 << 11) | (1 << 10) | (1 << 6) | (1 << 5) | (1 << 4) | (1 << 2) | 1
N, K = 23, 12


def gf2_mod(a: int, m: int) -> int:
    """a mod m in GF(2)[x]."""
    dm = m.bit_length() - 1
    while a and a.bit_length() - 1 >= dm:
        a ^= m << (a.bit_length() - 1 - dm)
    return a


def gf2_mul(a: int, b: int) -> int:
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        b >>= 1
    return out


def encode(msg: int) -> int:
    """Systematic cyclic encoding: c(x) = m(x) x^11 + (m(x) x^11 mod g(x)).
    The message sits in positions 11..22, the 11 check bits in positions 0..10."""
    shifted = msg << (N - K)
    return shifted | gf2_mod(shifted, GOLAY_G)


def syndrome(word: int) -> int:
    """The remainder of the received word mod g(x); zero exactly for codewords."""
    return gf2_mod(word, GOLAY_G)


def build_syndrome_table() -> dict[int, int]:
    """Map each syndrome to the unique error of weight <= 3 with that syndrome.
    The code is perfect, so these 1 + 23 + 253 + 1771 = 2048 errors fill all syndromes."""
    table: dict[int, int] = {}
    errors = [0] + [1 << i for i in range(N)]
    errors += [(1 << i) | (1 << j) for i in range(N) for j in range(i + 1, N)]
    errors += [(1 << i) | (1 << j) | (1 << k) for i in range(N) for j in range(i + 1, N) for k in range(j + 1, N)]
    for e in errors:
        s = syndrome(e)
        assert s not in table, "two errors of weight <= 3 share a syndrome"
        table[s] = e
    return table


_TABLE: dict[int, int] | None = None


def decode(word: int) -> int:
    """Correct up to 3 errors in a 23-bit word; returns the nearest codeword (always exists)."""
    global _TABLE
    if _TABLE is None:
        _TABLE = build_syndrome_table()
    return word ^ _TABLE[syndrome(word)]


# ---------------------------------------------------------------- extended [24, 12, 8] code

_BASE = [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0]


def b_matrix() -> list[int]:
    """Rows of the 12 x 12 matrix B: the 11 left cyclic shifts of 11011100010, each with a
    final 1, and the row 11111111111 0. B is symmetric and B^2 = I over GF(2).
    Row i is an int with bit j = B[i][j]."""
    rows = []
    for i in range(11):
        r = _BASE[i:] + _BASE[:i] + [1]
        rows.append(sum(b << j for j, b in enumerate(r)))
    rows.append(sum(1 << j for j in range(11)))
    return rows


B = b_matrix()


def vec_times_b(v: int) -> int:
    """v B for a 12-bit row vector v."""
    out = 0
    for i in range(12):
        if (v >> i) & 1:
            out ^= B[i]
    return out


def encode24(msg: int) -> int:
    """Codeword (m | m B) with G = [I | B]: bits 0..11 hold m, bits 12..23 hold m B."""
    return msg | (vec_times_b(msg) << 12)


def decode24(word: int) -> int | None:
    """Arithmetic decoding of the extended Golay code with H = [I | B].

    Returns the corrected codeword when at most 3 errors occurred, and None when the
    syndrome shows at least 4 errors (no codeword lies within distance 3).
    """
    r1, r2 = word & 0xFFF, word >> 12
    s = r1 ^ vec_times_b(r2)                   # syndrome s = r1 + r2 B
    e = None
    if s.bit_count() <= 3:                     # all errors in the first half
        e = s
    else:
        for i in range(12):
            if (s ^ B[i]).bit_count() <= 2:   # one error at position 12 + i
                e = (s ^ B[i]) | (1 << (12 + i))
                break
    if e is None:
        sb = vec_times_b(s)                    # s B, the syndrome seen from the second half
        if sb.bit_count() <= 3:
            e = sb << 12
        else:
            for i in range(12):
                if (sb ^ B[i]).bit_count() <= 2:
                    e = (1 << i) | ((sb ^ B[i]) << 12)
                    break
    if e is None:
        return None
    return word ^ e


# ---------------------------------------------------------------- ternary [11, 6, 5]_3 code

# g(x) = x^5 + x^4 - x^3 + x^2 - 1 over GF(3), low degree first
TERNARY_G = [2, 0, 1, 2, 1, 1]


def poly_mod_p(a: list[int], m: list[int], p: int) -> list[int]:
    """Remainder of a mod m over GF(p), lists low degree first (m monic)."""
    a = [x % p for x in a]
    dm = len(m) - 1
    for i in range(len(a) - 1, dm - 1, -1):
        c = a[i]
        if c:
            for j in range(dm + 1):
                a[i - dm + j] = (a[i - dm + j] - c * m[j]) % p
    return a[:dm]


def ternary_words() -> list[tuple[int, ...]]:
    """All 729 words of the cyclic ternary Golay code: m(x) g(x) for deg m < 6."""
    words = []
    for m in product(range(3), repeat=6):
        c = [0] * 11
        for i, a in enumerate(m):
            for j, b in enumerate(TERNARY_G):
                c[i + j] = (c[i + j] + a * b) % 3
        words.append(tuple(c))
    return words


def weight_distribution(words, n: int) -> list[int]:
    out = [0] * (n + 1)
    for w in words:
        out[(w.bit_count() if isinstance(w, int) else sum(1 for a in w if a))] += 1
    return out
