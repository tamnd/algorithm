# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/x25519/. The authors are listed in prov/J2GJN1.jsonl.
"""X25519, the Diffie-Hellman function on Curve25519 (RFC 7748, Section 5).

The curve is v^2 = u^3 + 486662 u^2 + u over GF(p), p = 2^255 - 19. The
function takes a 32-byte scalar and a 32-byte u-coordinate and returns the
u-coordinate of the scalar multiple, computed with the Montgomery ladder on
the u-coordinate only.

For study only. The code is not constant time: Python integers leak timing
through their size, and the conditional swap below is a model of the real
one, not a safe version of it. Do not use it to protect real data. Use
libsodium, the X25519 of a maintained library such as the Python package
cryptography, or a FIPS 140 validated module instead.

Cost: 255 ladder steps of 5 multiplications, 4 squarings and 1
multiplication by a24 in GF(p) each, then one inversion by Fermat's little
theorem (about 254 squarings and 11 multiplications).
"""

P = 2**255 - 19
A24 = 121665  # (486662 - 2) / 4, RFC 7748 Section 5
BASE_U = 9
BITS = 255


def decode_little_endian(b: bytes) -> int:
    """Read bytes as a little-endian integer (RFC 7748, decodeLittleEndian)."""
    return int.from_bytes(b, "little")


def decode_u_coordinate(u: bytes) -> int:
    """Decode a 32-byte u-coordinate: clear bit 255, keep the value as is.

    The value may be p or larger (a non-canonical encoding). It is used
    modulo p, as RFC 7748 Section 5 requires.
    """
    if len(u) != 32:
        raise ValueError("a u-coordinate has 32 bytes")
    b = bytearray(u)
    b[31] &= 0x7F  # mask the most significant bit
    return decode_little_endian(bytes(b))


def encode_u_coordinate(u: int) -> bytes:
    """Encode u modulo p as 32 little-endian bytes."""
    return (u % P).to_bytes(32, "little")


def decode_scalar(k: bytes) -> int:
    """Clamp a 32-byte scalar (RFC 7748 decodeScalar25519).

    Clear bits 0, 1 and 2 (the scalar becomes a multiple of the cofactor 8),
    clear bit 255 and set bit 254 (the top bit is fixed, so the ladder always
    does 255 steps and the scalar is in [2^254, 2^255)).
    """
    if len(k) != 32:
        raise ValueError("a scalar has 32 bytes")
    b = bytearray(k)
    b[0] &= 248
    b[31] &= 127
    b[31] |= 64
    return decode_little_endian(bytes(b))


def cswap(swap: int, x2: int, x3: int) -> tuple[int, int]:
    """Swap x2 and x3 if swap is 1, with a mask instead of a branch."""
    mask = -swap  # 0 or -1 (all ones)
    dummy = mask & (x2 ^ x3)
    return x2 ^ dummy, x3 ^ dummy


def ladder_step(x1: int, x2: int, z2: int, x3: int, z3: int) -> tuple[int, int, int, int]:
    """One step of the ladder: (x2:z2) doubles, (x3:z3) becomes the sum.

    x1 is the u-coordinate of the difference of the two points.
    """
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


def x25519(k: bytes, u: bytes) -> bytes:
    """X25519(k, u) of RFC 7748 Section 5. Returns 32 bytes.

    The result can be the all-zero string when u is a point of small order.
    Use x25519_shared for key agreement: it rejects that output.
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
    """The public key X25519(a, 9) of a 32-byte private key a."""
    return x25519(private, encode_u_coordinate(BASE_U))


def x25519_shared(private: bytes, peer_public: bytes) -> bytes:
    """The shared secret X25519(a, K_B), with the all-zero check of RFC 7748 Section 6.1.

    Raises ValueError when the result is all zero, which happens exactly when
    the peer sent a point whose order divides the cofactor 8.
    """
    k = x25519(private, peer_public)
    acc = 0
    for byte in k:  # OR all bytes, as RFC 7748 Section 6.1 suggests
        acc |= byte
    if acc == 0:
        raise ValueError("X25519 output is all zero: the peer key has small order")
    return k
