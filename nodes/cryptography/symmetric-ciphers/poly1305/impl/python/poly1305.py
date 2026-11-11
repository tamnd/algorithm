# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/poly1305/. The authors are listed in prov/T94CVM.jsonl.
"""Poly1305 (RFC 8439, Section 2.5), the one-time authenticator of D. J. Bernstein.

For study only. Python big integers are not constant time, so this code leaks
timing about r and the message, and it must not protect real data. A key must
authenticate only one message. Use crypto_onetimeauth or the ChaCha20-Poly1305
AEAD of libsodium, or a FIPS 140 validated module, instead.
"""

P = (1 << 130) - 5
CLAMP = 0x0FFFFFFC0FFFFFFC0FFFFFFC0FFFFFFF


def clamp(r: int) -> int:
    """Clear the top 4 bits of bytes 3, 7, 11, 15 and the low 2 bits of bytes 4, 8, 12 (little-endian)."""
    return r & CLAMP


def poly1305_mac(key: bytes, msg: bytes) -> bytes:
    """The 16-byte tag of msg under the 32-byte one-time key (r, s)."""
    if len(key) != 32:
        raise ValueError("a Poly1305 key has 32 bytes")
    r = clamp(int.from_bytes(key[:16], "little"))  # @line L1
    s = int.from_bytes(key[16:], "little")  # @line L2
    a = 0  # @line L3
    for i in range(0, len(msg), 16):  # @line L4
        n = int.from_bytes(msg[i : i + 16] + b"\x01", "little")  # @line L5
        a = (a + n) * r % P  # @line L6
    a = (a + s) % (1 << 128)  # @line L7
    return a.to_bytes(16, "little")  # @line L8


def tags_equal(a: bytes, b: bytes) -> bool:
    """Compare two tags by reading every byte and folding the differences with OR."""
    if len(a) != len(b):
        return False
    d = 0
    for x, y in zip(a, b):
        d |= x ^ y
    return d == 0


def poly1305_verify(key: bytes, msg: bytes, tag: bytes) -> bool:
    return tags_equal(poly1305_mac(key, msg), tag)  # @line L9
