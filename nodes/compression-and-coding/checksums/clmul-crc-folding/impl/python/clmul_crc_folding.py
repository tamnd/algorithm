# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clmul-crc-folding/. The authors are listed in prov/W0AB8H.jsonl.

"""CRC folding with carry-less multiplication, after Gopal et al. (Intel, 2009).

A software clmul stands in for PCLMULQDQ. The data are folded 4 x 128 bits at
a time with k1 = x^576 mod P and k2 = x^512 mod P, then down to one 128-bit
value with k3 = x^192 mod P and k4 = x^128 mod P, then multiplied by x^32 and
reduced to 64 bits with k5 = x^96 mod P and k6 = x^64 mod P, and last reduced
to 32 bits by Barrett reduction with mu = floor(x^64 / P).

This code works in the normal (not reflected) domain for every CRC: for a
CRC with refin, it reverses the bits of each byte first. The white paper also
gives a reflected variant with reflected constants; this code checks those
constants but does not run that variant.
"""


def clmul(a: int, b: int) -> int:
    """Carry-less product of two polynomials over GF(2), as PCLMULQDQ does
    for two 64-bit operands."""
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def poly_mod(a: int, p: int) -> int:
    dp = p.bit_length() - 1
    while a.bit_length() - 1 >= dp:
        a ^= p << (a.bit_length() - 1 - dp)
    return a


def poly_div(a: int, p: int) -> int:
    dp = p.bit_length() - 1
    q = 0
    while a.bit_length() - 1 >= dp:
        s = a.bit_length() - 1 - dp
        q |= 1 << s
        a ^= p << s
    return q


def x_pow_mod(e: int, p: int) -> int:
    return poly_mod(1 << e, p)


def reflect(value: int, width: int) -> int:
    out = 0
    for _ in range(width):
        out = (out << 1) | (value & 1)
        value >>= 1
    return out


def constants(poly: int) -> dict[str, int]:
    """The folding constants of the white paper, computed with GF(2) code.
    P = x^32 + poly."""
    p = (1 << 32) | poly
    return {
        "P": p,
        "k1": x_pow_mod(4 * 128 + 64, p),
        "k2": x_pow_mod(4 * 128, p),
        "k3": x_pow_mod(128 + 64, p),
        "k4": x_pow_mod(128, p),
        "k5": x_pow_mod(96, p),
        "k6": x_pow_mod(64, p),
        "mu": poly_div(1 << 64, p),
    }


M64 = (1 << 64) - 1
M32 = (1 << 32) - 1


class Count:
    def __init__(self) -> None:
        self.clmul = 0


def fold(x: int, ka: int, kb: int, cnt: Count) -> int:
    """x * x^T mod P, up to a multiple of P, for a 128-bit x, with
    ka = x^(T+64) mod P and kb = x^T mod P. The result has degree < 96."""
    cnt.clmul += 2
    return clmul(x >> 64, ka) ^ clmul(x & M64, kb)


def barrett(t: int, c: dict[str, int], cnt: Count) -> int:
    """t mod P for deg t < 64, with two carry-less products."""
    q = clmul(t >> 32, c["mu"]) >> 32  # @line L9
    cnt.clmul += 2
    return (t ^ clmul(q, c["P"])) & M32  # @line L10


def crc32_fold(data: bytes, width_poly: int, init: int, refin: bool, refout: bool, xorout: int,
               cnt: Count | None = None) -> int:
    """A 32-bit CRC in the Rocksoft model, computed by folding."""
    cnt = cnt or Count()
    c = constants(width_poly)
    if refin:
        data = bytes(reflect(b, 8) for b in data)
    k = 8 * len(data)
    m = int.from_bytes(data, "big")
    if k < 32:
        # Too short to fold: (I x^k + M x^32) has degree < 64. Reduce it.
        reg = barrett((init << k) ^ (m << 32), c, cnt)
    else:
        v = m ^ (init << (k - 32))  # @line L1
        nchunks = (k + 127) // 128
        chunks = [(v >> (128 * (nchunks - 1 - i))) & ((1 << 128) - 1) for i in range(nchunks)]
        pos = 0
        if nchunks >= 4:
            acc = chunks[0:4]  # @line L2
            pos = 4
            while nchunks - pos >= 4:  # @line L3
                acc = [fold(acc[j], c["k1"], c["k2"], cnt) ^ chunks[pos + j] for j in range(4)]
                pos += 4
            x = acc[0]
            for j in range(1, 4):  # @line L4
                x = fold(x, c["k3"], c["k4"], cnt) ^ acc[j]
        else:
            x = chunks[0]
            pos = 1
        while pos < nchunks:  # @line L5
            x = fold(x, c["k3"], c["k4"], cnt) ^ chunks[pos]
            pos += 1
        # x is congruent to V modulo P and has degree < 128. Now x * x^32 mod P.
        t = clmul(x >> 64, c["k5"]) ^ ((x & M64) << 32)  # @line L6
        t = clmul(t >> 64, c["k6"]) ^ (t & M64)  # @line L7
        cnt.clmul += 2
        reg = barrett(t, c, cnt)  # @line L8
    if refout:  # @line L11
        reg = reflect(reg, 32)
    return reg ^ xorout


def crc32_iso_hdlc(data: bytes, cnt: Count | None = None) -> int:
    return crc32_fold(data, 0x04C11DB7, M32, True, True, M32, cnt)


def crc32c(data: bytes, cnt: Count | None = None) -> int:
    return crc32_fold(data, 0x1EDC6F41, M32, True, True, M32, cnt)


def reflected_constants(poly: int) -> dict[str, int]:
    """The constants of the bit-reflected variant of the white paper (the
    gzip example): the 33-bit reflection of x^e mod P. In the reflected
    domain a carry-less product gains one extra factor x, and the exponents
    shift by 32 or 64 against the normal domain."""
    p = (1 << 32) | poly

    def r(e: int) -> int:
        return reflect(x_pow_mod(e, p), 33)

    return {
        "P": reflect(p, 33),
        "k1": r(4 * 128 + 32),
        "k2": r(4 * 128 - 32),
        "k3": r(128 + 32),
        "k4": r(128 - 32),
        "k5": r(64),
        "k6": r(32),
        "mu": reflect(poly_div(1 << 64, p), 33),
    }
