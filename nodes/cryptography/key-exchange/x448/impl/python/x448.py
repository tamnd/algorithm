# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/x448/. The authors are listed in prov/J4FG25.jsonl.
"""X448, the Diffie-Hellman function on Curve448 (RFC 7748, Section 5).

The curve is v^2 = u^3 + 156326 u^2 + u over GF(p), p = 2^448 - 2^224 - 1.
The function takes a 56-byte scalar and a 56-byte u-coordinate and returns
the u-coordinate of the scalar multiple, computed with the Montgomery ladder
on the u-coordinate only.

For study only. The code is not constant time: Python integers leak timing
through their size, and the conditional swap below is a model of the real
one, not a safe version of it. Do not use it to protect real data. Use a
maintained library (OpenSSL, the Python package cryptography, libdecaf) or a
FIPS 140 validated module instead.

Cost: 448 ladder steps of 5 multiplications, 4 squarings and 1
multiplication by a24 in GF(p) each, then one inversion by Fermat's little
theorem (about 447 squarings and some multiplications).
"""

P = 2**448 - 2**224 - 1
A24 = 39081  # (156326 - 2) / 4, RFC 7748 Section 5
BASE_U = 5
BITS = 448
SIZE = 56


def decode_little_endian(b: bytes) -> int:
    """Read bytes as a little-endian integer."""
    return int.from_bytes(b, "little")


def decode_u_coordinate(u: bytes) -> int:
    """Decode a 56-byte u-coordinate. X448 masks no bit (448 bits fill 56 bytes)."""
    if len(u) != SIZE:
        raise ValueError("a u-coordinate has 56 bytes")
    return decode_little_endian(u)


def encode_u_coordinate(u: int) -> bytes:
    """Encode u modulo p as 56 little-endian bytes."""
    return (u % P).to_bytes(SIZE, "little")


def decode_scalar(k: bytes) -> int:
    """Clamp a 56-byte scalar (RFC 7748 decodeScalar448).

    Clear bits 0 and 1 (the scalar becomes a multiple of the cofactor 4) and
    set bit 447 (the ladder always does 448 steps).
    """
    if len(k) != SIZE:
        raise ValueError("a scalar has 56 bytes")
    b = bytearray(k)
    b[0] &= 252
    b[55] |= 128
    return decode_little_endian(bytes(b))


def cswap(swap: int, x2: int, x3: int) -> tuple[int, int]:
    """Swap x2 and x3 if swap is 1, with a mask instead of a branch."""
    mask = -swap
    dummy = mask & (x2 ^ x3)
    return x2 ^ dummy, x3 ^ dummy


def ladder_step(x1: int, x2: int, z2: int, x3: int, z3: int) -> tuple[int, int, int, int]:
    """One ladder step: (x2:z2) doubles, (x3:z3) becomes the sum (difference x1)."""
    a = (x2 + z2) % P
    aa = a * a % P
    b = (x2 - z2) % P
    bb = b * b % P
    e = (aa - bb) % P
    c = (x3 + z3) % P
    d = (x3 - z3) % P
    da = d * a % P
    cb = c * b % P
    x3 = (da + cb) % P
    x3 = x3 * x3 % P
    z3 = (da - cb) % P
    z3 = x1 * (z3 * z3) % P
    x2 = aa * bb % P
    z2 = e * (aa + A24 * e) % P
    return x2, z2, x3, z3


def x448(k: bytes, u: bytes) -> bytes:
    """X448(k, u) of RFC 7748 Section 5. Returns 56 bytes.

    The result is all zero when u has small order. Use x448_shared for key
    agreement: it rejects that output.
    """
    k_int = decode_scalar(k)  # @line L1
    x1 = decode_u_coordinate(u) % P  # @line L2
    x2, z2, x3, z3, swap = 1, 0, x1, 1, 0  # @line L3
    for t in range(BITS - 1, -1, -1):  # @line L4
        k_t = (k_int >> t) & 1  # @line L5
        swap ^= k_t  # @line L6
        x2, x3 = cswap(swap, x2, x3)  # @line L7
        z2, z3 = cswap(swap, z2, z3)  # @line L7
        swap = k_t  # @line L8
        x2, z2, x3, z3 = ladder_step(x1, x2, z2, x3, z3)  # @line L9
    x2, x3 = cswap(swap, x2, x3)  # @line L10
    z2, z3 = cswap(swap, z2, z3)  # @line L10
    return encode_u_coordinate(x2 * pow(z2, P - 2, P))  # @line L11


def public_key(private: bytes) -> bytes:
    """The public key X448(a, 5) of a 56-byte private key a."""
    return x448(private, encode_u_coordinate(BASE_U))


def x448_shared(private: bytes, peer_public: bytes) -> bytes:
    """The shared secret X448(a, K_B), rejecting the all-zero output (RFC 7748 Section 6.2)."""
    k = x448(private, peer_public)
    acc = 0
    for byte in k:
        acc |= byte
    if acc == 0:
        raise ValueError("X448 output is all zero: the peer key has small order")
    return k
