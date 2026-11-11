# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ocb-mode/. The authors are listed in prov/0FNP6K.jsonl.
"""OCB3 as specified in RFC 7253 (Krovetz and Rogaway), Section 4.

For study only. This code is not constant time (the AES in aes.py uses table
lookups, and double() branches on a secret bit) and must not protect real data.
Use AES-OCB from a maintained library instead, such as the OCB mode of OpenSSL
(EVP_aes_128_ocb) or Botan; where a FIPS 140 validated module is required, use
AES-GCM, because OCB is not a NIST approved mode.

Blocks are handled as 128-bit integers, so the bit strings of the RFC map
directly: bit 1 of a string is the most significant bit of the integer.
"""

from typing import Protocol

INVALID = "INVALID"
MASK = (1 << 128) - 1


class BlockCipher(Protocol):
    block_size: int

    def encrypt_block(self, block: bytes) -> bytes: ...

    def decrypt_block(self, block: bytes) -> bytes: ...


def _enc(cipher: BlockCipher, x: int) -> int:
    return int.from_bytes(cipher.encrypt_block(x.to_bytes(16, "big")), "big")


def _dec(cipher: BlockCipher, x: int) -> int:
    return int.from_bytes(cipher.decrypt_block(x.to_bytes(16, "big")), "big")


def double(s: int) -> int:
    """RFC 7253 Section 2: shift left by one bit; if the top bit fell out, xor 0x87."""
    return ((s << 1) & MASK) ^ (0x87 if s >> 127 else 0)


def ntz(i: int) -> int:
    """The number of trailing zero bits of the positive integer i."""
    return (i & -i).bit_length() - 1


def _pad_block(part: bytes) -> int:
    """part || 1 || zeros, for 0 < len(part) < 16 bytes."""
    return int.from_bytes(part + b"\x80" + bytes(15 - len(part)), "big")


class OcbKey:
    """The key-dependent values L_*, L_$ and L_0, L_1, ... of Section 4."""

    def __init__(self, cipher: BlockCipher) -> None:
        self.cipher = cipher
        self.l_star = _enc(cipher, 0)  # @line L5
        self.l_dollar = double(self.l_star)
        self.l = [double(self.l_dollar)]

    def l_i(self, i: int) -> int:
        while len(self.l) <= i:
            self.l.append(double(self.l[-1]))
        return self.l[i]


def ocb_hash(key: OcbKey, a: bytes) -> int:
    """Section 4.1, HASH(K, A)."""
    total, offset = 0, 0  # @line L1
    m = len(a) // 16
    for i in range(1, m + 1):  # @line L2
        offset ^= key.l_i(ntz(i))
        total ^= _enc(key.cipher, int.from_bytes(a[16 * (i - 1) : 16 * i], "big") ^ offset)
    if len(a) % 16:  # @line L3
        offset ^= key.l_star
        total ^= _enc(key.cipher, _pad_block(a[16 * m :]) ^ offset)
    return total  # @line L4


def initial_offset(key: OcbKey, n: bytes, taglen: int) -> int:
    """Offset_0 from the nonce: Nonce, bottom, Ktop and Stretch of Section 4.2. taglen in bits."""
    if not 1 <= len(n) <= 15:
        raise ValueError("the nonce has 1 to 15 bytes (at most 120 bits)")
    nonce = ((taglen % 128) << 121) | (1 << (8 * len(n))) | int.from_bytes(n, "big")  # @line L6
    bottom = nonce & 63
    ktop = _enc(key.cipher, nonce & ~63 & MASK)  # @line L7
    stretch = (ktop << 64) | ((ktop >> 64) ^ ((ktop >> 56) & ((1 << 64) - 1)))  # 192 bits
    return (stretch >> (64 - bottom)) & MASK  # @line L8


def tags_equal(a: bytes, b: bytes) -> bool:
    """Read every byte and fold the differences with OR: no early exit."""
    d = len(a) ^ len(b)
    for x, y in zip(a, b):
        d |= x ^ y
    return d == 0


def ocb_encrypt(cipher: BlockCipher, n: bytes, a: bytes, p: bytes, taglen: int = 128) -> bytes:
    """Section 4.2, OCB-ENCRYPT. taglen is in bits, a multiple of 8 up to 128."""
    key = OcbKey(cipher)
    offset, checksum = initial_offset(key, n, taglen), 0
    out = bytearray()
    m = len(p) // 16
    for i in range(1, m + 1):  # @line L9
        pi = int.from_bytes(p[16 * (i - 1) : 16 * i], "big")
        offset ^= key.l_i(ntz(i))
        out += (offset ^ _enc(cipher, pi ^ offset)).to_bytes(16, "big")
        checksum ^= pi
    if len(p) % 16:  # @line L10
        offset ^= key.l_star
        pad = _enc(cipher, offset).to_bytes(16, "big")
        out += bytes(x ^ y for x, y in zip(p[16 * m :], pad))
        checksum ^= _pad_block(p[16 * m :])
    tag = _enc(cipher, checksum ^ offset ^ key.l_dollar) ^ ocb_hash(key, a)  # @line L11
    return bytes(out) + tag.to_bytes(16, "big")[: taglen // 8]  # @line L12


def ocb_decrypt(cipher: BlockCipher, n: bytes, a: bytes, c: bytes, taglen: int = 128) -> bytes | str:
    """Section 4.3, OCB-DECRYPT. The plaintext stays in a buffer until the tag is checked."""
    if len(c) < taglen // 8:
        return INVALID
    key = OcbKey(cipher)
    offset, checksum = initial_offset(key, n, taglen), 0  # @line L13
    body, t = c[: len(c) - taglen // 8], c[len(c) - taglen // 8 :]
    out = bytearray()
    m = len(body) // 16
    for i in range(1, m + 1):  # @line L14
        ci = int.from_bytes(body[16 * (i - 1) : 16 * i], "big")
        offset ^= key.l_i(ntz(i))
        pi = offset ^ _dec(cipher, ci ^ offset)
        out += pi.to_bytes(16, "big")
        checksum ^= pi
    if len(body) % 16:  # @line L15
        offset ^= key.l_star
        pad = _enc(cipher, offset).to_bytes(16, "big")
        tail = bytes(x ^ y for x, y in zip(body[16 * m :], pad))
        out += tail
        checksum ^= _pad_block(tail)
    tag = _enc(cipher, checksum ^ offset ^ key.l_dollar) ^ ocb_hash(key, a)  # @line L16
    if not tags_equal(tag.to_bytes(16, "big")[: taglen // 8], t):  # @line L17
        return INVALID
    return bytes(out)  # @line L18
