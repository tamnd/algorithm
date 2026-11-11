# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ccm-decryption-check/. The authors are listed in prov/PYJ12X.jsonl.
"""The CCM decryption-verification process, NIST SP 800-38C Section 6.2, and two wrong versions.

For study only. This code is not constant time (AES uses table lookups) and must
not protect real data. Use AES-CCM from a FIPS 140 validated module instead.

decrypt_verify follows the ten steps of Section 6.2: it decrypts into a private
buffer, recomputes the CBC-MAC, compares the tags without an early exit, and
returns either the payload or the single error INVALID. The two functions at the
end break the rule "release nothing on failure" and exist only for the tests.
"""

from typing import Protocol

INVALID = "INVALID"


class BlockCipher(Protocol):
    block_size: int

    def encrypt_block(self, block: bytes) -> bytes: ...


def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def _pad(x: bytes) -> bytes:
    return x + bytes(-len(x) % 16)


def valid(n: bytes, a: bytes, p_len: int, tlen: int) -> bool:
    """The restrictions of the formatting function of SP 800-38C, Appendix A.1, in bytes."""
    q = 15 - len(n)
    return 7 <= len(n) <= 13 and tlen in (4, 6, 8, 10, 12, 14, 16) and p_len < 1 << (8 * q) and len(a) < 1 << 64


def format_blocks(n: bytes, a: bytes, p: bytes, tlen: int) -> bytes:
    """B_0 || B_1 || ... || B_r, SP 800-38C Appendix A.2."""
    q = 15 - len(n)
    flags = (64 if a else 0) + 8 * ((tlen - 2) // 2) + (q - 1)
    out = bytes([flags]) + n + len(p).to_bytes(q, "big")
    if a:
        if len(a) < (1 << 16) - (1 << 8):
            enc = len(a).to_bytes(2, "big")
        elif len(a) < 1 << 32:
            enc = b"\xff\xfe" + len(a).to_bytes(4, "big")
        else:
            enc = b"\xff\xff" + len(a).to_bytes(8, "big")
        out += _pad(enc + a)
    return out + _pad(p)


def counter(n: bytes, j: int) -> bytes:
    """Ctr_j of SP 800-38C Appendix A.3."""
    q = 15 - len(n)
    return bytes([q - 1]) + n + j.to_bytes(q, "big")


def _cbc_mac(cipher: BlockCipher, blocks: bytes) -> bytes:
    y = bytes(16)
    for i in range(0, len(blocks), 16):
        y = cipher.encrypt_block(_xor(y, blocks[i : i + 16]))
    return y


def _keystream(cipher: BlockCipher, n: bytes, length: int) -> bytes:
    s = b"".join(cipher.encrypt_block(counter(n, j)) for j in range(1, -(-length // 16) + 1))
    return s[:length]


def generate_encrypt(cipher: BlockCipher, n: bytes, a: bytes, p: bytes, tlen: int) -> bytes:
    """Section 6.1: C = (P xor MSB_Plen(S)) || (T xor MSB_Tlen(S_0))."""
    if not valid(n, a, len(p), tlen):
        raise ValueError("invalid input")
    t = _cbc_mac(cipher, format_blocks(n, a, p, tlen))[:tlen]
    return _xor(p, _keystream(cipher, n, len(p))) + _xor(t, cipher.encrypt_block(counter(n, 0)))


def tags_equal(a: bytes, b: bytes) -> bool:
    """Read every byte and fold the differences with OR: no early exit."""
    d = len(a) ^ len(b)
    for x, y in zip(a, b):
        d |= x ^ y
    return d == 0


def decrypt_verify(cipher: BlockCipher, n: bytes, a: bytes, c: bytes, tlen: int) -> bytes | str:
    """Return the payload P, or the string INVALID. Nothing else leaves this function."""
    if len(c) <= tlen:  # @line L1
        return INVALID
    m = -(-(len(c) - tlen) // 16)  # @line L2
    s0 = cipher.encrypt_block(counter(n, 0))  # @line L3
    s = b"".join(cipher.encrypt_block(counter(n, j)) for j in range(1, m + 1))  # @line L4
    p = _xor(c[: len(c) - tlen], s)  # @line L5
    t = _xor(c[len(c) - tlen :], s0)  # @line L6
    ok = valid(n, a, len(p), tlen)  # @line L7
    blocks = format_blocks(n, a, p, tlen) if ok else bytes(16)
    y = _cbc_mac(cipher, blocks)  # @line L8
    ok = tags_equal(t, y[:tlen]) and ok  # @line L9
    if not ok:  # @line L10
        return INVALID  # one error for step 7 and step 10; p and t are dropped here
    return p  # @line L11


# ---- Two wrong versions, for the tests only. ----


def decrypt_release_first(cipher: BlockCipher, n: bytes, a: bytes, c: bytes, tlen: int) -> tuple[bytes, bool]:
    """WRONG: a streaming decryptor that hands out the payload and reports the tag result after."""
    s = _keystream(cipher, n, len(c) - tlen)
    p = _xor(c[: len(c) - tlen], s)
    t = _xor(c[len(c) - tlen :], cipher.encrypt_block(counter(n, 0)))
    return p, tags_equal(t, _cbc_mac(cipher, format_blocks(n, a, p, tlen))[:tlen])


def decrypt_parse_first(cipher: BlockCipher, n: bytes, a: bytes, c: bytes, tlen: int) -> bytes | str:
    """WRONG: checks the payload format (version byte 0x01) before the tag, with its own error."""
    p = _xor(c[: len(c) - tlen], _keystream(cipher, n, len(c) - tlen))
    if not p or p[0] != 0x01:
        return "BAD VERSION"
    t = _xor(c[len(c) - tlen :], cipher.encrypt_block(counter(n, 0)))
    if not tags_equal(t, _cbc_mac(cipher, format_blocks(n, a, p, tlen))[:tlen]):
        return INVALID
    return p
