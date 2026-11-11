# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ccm-mode/. The authors are listed in prov/0AFYD8.jsonl.
"""Counter with CBC-MAC (CCM), NIST SP 800-38C and RFC 3610.

For study only. This code is not constant time (AES uses table lookups) and must
not protect real data. Use AES-CCM from a FIPS 140 validated module instead.

Parameters: M is the tag length in bytes (4, 6, ..., 16), L is the size in bytes of
the length field (2 to 8), and the nonce has 15 - L bytes.
"""

from typing import Protocol


class BlockCipher(Protocol):
    block_size: int

    def encrypt_block(self, block: bytes) -> bytes: ...


class InvalidTag(ValueError):
    """Verification failed. Nothing else is revealed."""


def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def _pad(x: bytes) -> bytes:
    return x + bytes(-len(x) % 16)


def _check(n: bytes, m_len: int, l_len: int, p_len: int) -> None:
    if m_len not in (4, 6, 8, 10, 12, 14, 16):
        raise ValueError("the tag length M must be even and from 4 to 16")
    if not 2 <= l_len <= 8 or len(n) != 15 - l_len:
        raise ValueError("L must be from 2 to 8 and the nonce must have 15 - L bytes")
    if p_len >= 1 << (8 * l_len):
        raise ValueError("the message is too long for the length field")


def encode_ad_length(a_len: int) -> bytes:
    """The prefix that encodes l(a), RFC 3610 Section 2.2 and SP 800-38C Appendix A.2.2."""
    if a_len < (1 << 16) - (1 << 8):
        return a_len.to_bytes(2, "big")
    if a_len < 1 << 32:
        return b"\xff\xfe" + a_len.to_bytes(4, "big")
    return b"\xff\xff" + a_len.to_bytes(8, "big")


def format_blocks(n: bytes, a: bytes, p: bytes, m_len: int, l_len: int) -> bytes:
    """B_0 || B_1 || ... || B_r: the input of the CBC-MAC."""
    flags = (64 if a else 0) + 8 * ((m_len - 2) // 2) + (l_len - 1)
    b0 = bytes([flags]) + n + len(p).to_bytes(l_len, "big")  # @line L1
    blocks = b0 + (_pad(encode_ad_length(len(a)) + a) if a else b"")  # @line L2
    return blocks + _pad(p)  # @line L3


def counter_block(n: bytes, i: int, l_len: int) -> bytes:
    """A_i = flags || N || [i]_L with flags = L - 1. Bits 3 to 5 are zero, so A_i differs from B_0."""
    return bytes([l_len - 1]) + n + i.to_bytes(l_len, "big")


def cbc_mac_tag(cipher: BlockCipher, blocks: bytes, m_len: int) -> bytes:
    x = bytes(16)  # @line L4
    for j in range(0, len(blocks), 16):  # @line L5
        x = cipher.encrypt_block(_xor(x, blocks[j : j + 16]))
    return x[:m_len]  # @line L6


def _keystream(cipher: BlockCipher, n: bytes, l_len: int, length: int) -> bytes:
    s = bytearray()
    for i in range(1, -(-length // 16) + 1):  # @line L7
        s += cipher.encrypt_block(counter_block(n, i, l_len))
    return bytes(s[:length])


def ccm_encrypt(cipher: BlockCipher, n: bytes, a: bytes, p: bytes, m_len: int = 16) -> bytes:
    """Return C || U. Precondition: n is never used twice under the key."""
    l_len = 15 - len(n)
    _check(n, m_len, l_len, len(p))
    t = cbc_mac_tag(cipher, format_blocks(n, a, p, m_len, l_len), m_len)  # first pass: CBC-MAC
    c = _xor(p, _keystream(cipher, n, l_len, len(p)))  # @line L8
    u = _xor(t, cipher.encrypt_block(counter_block(n, 0, l_len)))  # @line L9
    return c + u  # @line L10


def tags_equal(a: bytes, b: bytes) -> bool:
    if len(a) != len(b):
        return False
    d = 0
    for x, y in zip(a, b):
        d |= x ^ y
    return d == 0


def ccm_decrypt(cipher: BlockCipher, n: bytes, a: bytes, cu: bytes, m_len: int = 16) -> bytes:
    """Return P, or raise InvalidTag and release nothing. See the ccm-decryption-check page."""
    l_len = 15 - len(n)
    if len(cu) < m_len:
        raise InvalidTag("too short")
    c, u = cu[:-m_len], cu[-m_len:]
    _check(n, m_len, l_len, len(c))
    p = _xor(c, _keystream(cipher, n, l_len, len(c)))  # @line L11
    t = _xor(u, cipher.encrypt_block(counter_block(n, 0, l_len)))
    expected = cbc_mac_tag(cipher, format_blocks(n, a, p, m_len, l_len), m_len)  # @line L12
    if not tags_equal(expected, t):  # @line L13
        raise InvalidTag("authentication failed")
    return p  # @line L14
