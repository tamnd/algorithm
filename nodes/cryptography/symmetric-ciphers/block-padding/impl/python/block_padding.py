# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-padding/. The authors are listed in prov/YE2JDS.jsonl.
"""Four padding schemes for block modes, and CBC ciphertext stealing (variant CS3) as an alternative.

For study only. The code is not constant time: the unpad functions branch on
secret bytes and so can act as padding oracles. Do not use it to protect real
data; use an AEAD mode from a FIPS 140 validated module or libsodium.
"""

from typing import Protocol


class BlockCipher(Protocol):
    block_size: int

    def encrypt_block(self, block: bytes) -> bytes: ...

    def decrypt_block(self, block: bytes) -> bytes: ...


def _check(b: int) -> None:
    if not 1 <= b <= 255:
        raise ValueError("the block size must be 1 to 255 bytes")


def pad_pkcs7(m: bytes, b: int) -> bytes:
    """PKCS #7 (RFC 5652, Section 6.3): add k bytes of value k, 1 <= k <= b."""
    _check(b)
    k = b - len(m) % b
    return m + bytes([k]) * k


def unpad_pkcs7(x: bytes, b: int) -> bytes:
    _check(b)
    if not x or len(x) % b:
        raise ValueError("bad length")
    k = x[-1]
    if not 1 <= k <= b or x[-k:] != bytes([k]) * k:
        raise ValueError("bad padding")
    return x[:-k]


def pad_iso7816(m: bytes, b: int) -> bytes:
    """ISO/IEC 7816-4 (also ISO/IEC 9797-1 padding method 2): add 0x80, then zeros."""
    _check(b)
    k = b - len(m) % b
    return m + b"\x80" + bytes(k - 1)


def unpad_iso7816(x: bytes, b: int) -> bytes:
    _check(b)
    if not x or len(x) % b:
        raise ValueError("bad length")
    i = len(x) - 1
    while i >= len(x) - b and x[i] == 0:
        i -= 1
    if i < len(x) - b or x[i] != 0x80:
        raise ValueError("bad padding")
    return x[:i]


def pad_x923(m: bytes, b: int) -> bytes:
    """ANSI X9.23: add k - 1 zero bytes, then one byte of value k, 1 <= k <= b."""
    _check(b)
    k = b - len(m) % b
    return m + bytes(k - 1) + bytes([k])


def unpad_x923(x: bytes, b: int) -> bytes:
    _check(b)
    if not x or len(x) % b:
        raise ValueError("bad length")
    k = x[-1]
    if not 1 <= k <= b or x[-k:-1] != bytes(k - 1):
        raise ValueError("bad padding")
    return x[:-k]


def pad_zero(m: bytes, b: int) -> bytes:
    """Zero padding (ISO/IEC 9797-1 padding method 1): add zeros only if needed. Ambiguous."""
    _check(b)
    return m + bytes(-len(m) % b)


def unpad_zero(x: bytes) -> bytes:
    """The best guess: strip all trailing zeros. Wrong for messages that end in 0x00."""
    return x.rstrip(b"\x00")


def _xor(a: bytes, c: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, c))


def cbc_cs3_encrypt(cipher: BlockCipher, iv: bytes, p: bytes) -> bytes:
    """CBC with ciphertext stealing, variant CS3 (SP 800-38A Addendum; the Kerberos order).

    Needs at least one block. The ciphertext has the length of the plaintext.
    """
    b = cipher.block_size
    if len(p) < b or len(iv) != b:
        raise ValueError("CBC-CS3 needs at least one block and a one-block IV")
    d = len(p) % b or b  # bytes in the last block
    n = (len(p) + b - 1) // b
    padded = p + bytes(b - d)  # zero fill of the last block; these zeros are never sent
    prev, blocks = iv, []
    for j in range(n):
        prev = cipher.encrypt_block(_xor(padded[j * b : (j + 1) * b], prev))
        blocks.append(prev)
    if n == 1:
        return blocks[0]
    return b"".join(blocks[:-2]) + blocks[-1] + blocks[-2][:d]


def cbc_cs3_decrypt(cipher: BlockCipher, iv: bytes, c: bytes) -> bytes:
    b = cipher.block_size
    if len(c) < b or len(iv) != b:
        raise ValueError("CBC-CS3 needs at least one block and a one-block IV")
    n = (len(c) + b - 1) // b
    if n == 1:
        return _xor(cipher.decrypt_block(c), iv)
    d = len(c) - (n - 1) * b
    head = c[: (n - 2) * b]
    x, tail = c[(n - 2) * b : (n - 1) * b], c[(n - 1) * b :]
    z = cipher.decrypt_block(x)  # = C[n-1] XOR (P[n] || zeros)
    c_prev = tail + z[d:]  # rebuild the full C[n-1]
    p_last = _xor(z[:d], c_prev[:d])
    out, prev = bytearray(), iv
    for blk in [head[j * b : (j + 1) * b] for j in range(n - 2)] + [c_prev]:
        out += _xor(cipher.decrypt_block(blk), prev)
        prev = blk
    return bytes(out) + p_last
