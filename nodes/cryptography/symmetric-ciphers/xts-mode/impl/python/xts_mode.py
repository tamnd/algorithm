# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xts-mode/. The authors are listed in prov/9A46ZH.jsonl.
"""XTS-AES, IEEE Std 1619-2007 and NIST SP 800-38E, with ciphertext stealing.

For study only. The code is not constant time and gives no integrity. Do not
use it to protect real data; use the XTS of a FIPS 140 validated module or of
the disk encryption layer of your operating system.
"""

from aes import AES


def mul_alpha(t: bytes) -> bytes:
    """Multiply a tweak by alpha (the element x) in GF(2^128), IEEE 1619 byte order.

    The 16 bytes are read as a little-endian integer: byte 0 holds the lowest
    coefficients. Shift left by one; if bit 127 falls off, reduce by
    x^128 = x^7 + x^2 + x + 1, that is XOR 0x87 into byte 0.
    """
    v = int.from_bytes(t, "little") << 1
    if v >> 128:
        v = (v ^ 0x87) & ((1 << 128) - 1)
    return v.to_bytes(16, "little")


def tweak_from_data_unit(n: int) -> bytes:
    """The 128-bit tweak value i: the data unit number, little-endian."""
    return n.to_bytes(16, "little")


def _xex_enc(c1: AES, p: bytes, t: bytes) -> bytes:
    pp = bytes(a ^ b for a, b in zip(p, t))
    return bytes(a ^ b for a, b in zip(c1.encrypt_block(pp), t))


def _xex_dec(c1: AES, c: bytes, t: bytes) -> bytes:
    cc = bytes(a ^ b for a, b in zip(c, t))
    return bytes(a ^ b for a, b in zip(c1.decrypt_block(cc), t))


def _split_key(key: bytes, allow_equal_keys: bool) -> tuple[AES, AES]:
    if len(key) not in (32, 64):
        raise ValueError("an XTS-AES key is Key1 || Key2, 32 or 64 bytes")
    h = len(key) // 2
    if key[:h] == key[h:] and not allow_equal_keys:  # IEEE 1619 Vector 1 has equal keys
        raise ValueError("Key1 and Key2 must differ")
    return AES(key[:h]), AES(key[h:])


def xts_encrypt(key: bytes, i: bytes, p: bytes, allow_equal_keys: bool = False) -> bytes:
    """Encrypt one data unit p (at least 16 bytes) with tweak value i (16 bytes)."""
    if len(p) < 16 or len(i) != 16:
        raise ValueError("a data unit has at least 16 bytes and the tweak has 16")
    c1, c2 = _split_key(key, allow_equal_keys)
    m, r = divmod(len(p), 16)
    plain_blocks = m if r == 0 else m - 1
    t = c2.encrypt_block(i)  # @line L1
    out = bytearray()
    for j in range(plain_blocks):  # @line L2
        out += _xex_enc(c1, p[16 * j : 16 * j + 16], t)  # @line L3
        t = mul_alpha(t)  # @line L4
    if r:  # @line L5
        cc = _xex_enc(c1, p[16 * (m - 1) : 16 * m], t)  # @line L6
        pp = p[16 * m :] + cc[r:]  # @line L7
        out += _xex_enc(c1, pp, mul_alpha(t)) + cc[:r]  # @line L8
    return bytes(out)  # @line L9


def xts_decrypt(key: bytes, i: bytes, c: bytes, allow_equal_keys: bool = False) -> bytes:
    """Invert xts_encrypt. With stealing, the last full block uses the later tweak."""
    if len(c) < 16 or len(i) != 16:
        raise ValueError("a data unit has at least 16 bytes and the tweak has 16")
    c1, c2 = _split_key(key, allow_equal_keys)
    m, r = divmod(len(c), 16)
    plain_blocks = m if r == 0 else m - 1
    t = c2.encrypt_block(i)
    out = bytearray()
    for j in range(plain_blocks):
        out += _xex_dec(c1, c[16 * j : 16 * j + 16], t)
        t = mul_alpha(t)
    if r:
        pp = _xex_dec(c1, c[16 * (m - 1) : 16 * m], mul_alpha(t))
        cc = c[16 * m :] + pp[r:]
        out += _xex_dec(c1, cc, t) + pp[:r]
    return bytes(out)
