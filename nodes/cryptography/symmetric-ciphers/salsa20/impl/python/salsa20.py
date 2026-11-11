# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/salsa20/. The authors are listed in prov/12PMYB.jsonl.

"""Salsa20/20 as in Bernstein's Salsa20 specification (2005), for study only.

This code is not constant time and must not protect real data. Use
XSalsa20-Poly1305 or ChaCha20-Poly1305 from libsodium instead.
"""

M32 = 0xFFFFFFFF
SIGMA = b"expand 32-byte k"
TAU = b"expand 16-byte k"


def rotl32(v: int, c: int) -> int:
    """Rotate the 32-bit word v left by c places, 0 < c < 32."""
    return ((v << c) & M32) | (v >> (32 - c))


def quarterround(y0: int, y1: int, y2: int, y3: int) -> tuple[int, int, int, int]:
    """Return quarterround(y0, y1, y2, y3) of the specification, Section 3.

    Cost: 4 additions, 4 XORs and 4 rotations.
    """
    z1 = y1 ^ rotl32((y0 + y3) & M32, 7)  # @line L1
    z2 = y2 ^ rotl32((z1 + y0) & M32, 9)  # @line L2
    z3 = y3 ^ rotl32((z2 + z1) & M32, 13)  # @line L3
    z0 = y0 ^ rotl32((z3 + z2) & M32, 18)  # @line L4
    return z0, z1, z2, z3


def _qr(x: list[int], a: int, b: int, c: int, d: int) -> None:
    x[a], x[b], x[c], x[d] = quarterround(x[a], x[b], x[c], x[d])


def columnround(x: list[int]) -> list[int]:
    """Return columnround(x), Section 5. Precondition: 16 words."""
    y = list(x)
    _qr(y, 0, 4, 8, 12)
    _qr(y, 5, 9, 13, 1)
    _qr(y, 10, 14, 2, 6)
    _qr(y, 15, 3, 7, 11)
    return y


def rowround(y: list[int]) -> list[int]:
    """Return rowround(y), Section 4. Precondition: 16 words."""
    z = list(y)
    _qr(z, 0, 1, 2, 3)
    _qr(z, 5, 6, 7, 4)
    _qr(z, 10, 11, 8, 9)
    _qr(z, 15, 12, 13, 14)
    return z


def doubleround(x: list[int]) -> list[int]:
    """Return doubleround(x) = rowround(columnround(x)), Section 6."""
    return rowround(columnround(x))


def salsa20_hash(block: bytes, rounds: int = 20) -> bytes:
    """Return the Salsa20 hash (core) of a 64-byte block, Section 8.

    Precondition: len(block) == 64 and rounds is even.
    Cost: rounds/2 double rounds, that is 2 * rounds quarterrounds.
    """
    x = [int.from_bytes(block[4 * i:4 * i + 4], "little") for i in range(16)]
    z = list(x)  # @line L5
    for _ in range(rounds // 2):  # @line L6
        z = columnround(z)  # @line L7
        z = rowround(z)  # @line L8
    return b"".join(((z[i] + x[i]) & M32).to_bytes(4, "little") for i in range(16))  # @line L9


def salsa20_expand(k: bytes, n: bytes, rounds: int = 20) -> bytes:
    """Return Salsa20_k(n), the expansion of Section 9.

    Precondition: len(k) in (16, 32), len(n) == 16 (nonce then counter).
    Cost: one call of the hash.
    """
    if len(n) != 16 or len(k) not in (16, 32):
        raise ValueError("Salsa20 needs a 16- or 32-byte key and a 16-byte input")
    c = SIGMA if len(k) == 32 else TAU
    k0, k1 = k[:16], k[-16:]
    block = c[0:4] + k0 + c[4:8] + n + c[8:12] + k1 + c[12:16]  # @line L10
    return salsa20_hash(block, rounds)


def salsa20_encrypt(k: bytes, v: bytes, m: bytes, rounds: int = 20) -> bytes:
    """Encrypt or decrypt m with key k and 8-byte nonce v, Section 10.

    Precondition: len(k) in (16, 32), len(v) == 8, len(m) < 2**70.
    Cost: ceil(len(m)/64) calls of the hash.
    """
    if len(v) != 8:
        raise ValueError("Salsa20 needs an 8-byte nonce")
    out = bytearray()
    for i in range((len(m) + 63) // 64):
        ks = salsa20_expand(k, v + i.to_bytes(8, "little"), rounds)  # @line L11
        out += bytes(a ^ b for a, b in zip(m[64 * i:64 * i + 64], ks))  # @line L12
    return bytes(out)
