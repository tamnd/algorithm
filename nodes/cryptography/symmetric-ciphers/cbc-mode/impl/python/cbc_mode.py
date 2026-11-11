# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cbc-mode/. The authors are listed in prov/AAD84Q.jsonl.
"""Cipher block chaining (CBC) mode, NIST SP 800-38A Section 6.2, with PKCS #7 padding helpers.

For study only. The code is not constant time, and CBC alone gives no
integrity. Do not use it to protect real data. Use an AEAD mode such as
AES-GCM or ChaCha20-Poly1305 from a FIPS 140 validated module or libsodium.
"""

from typing import Protocol


class BlockCipher(Protocol):
    block_size: int

    def encrypt_block(self, block: bytes) -> bytes: ...

    def decrypt_block(self, block: bytes) -> bytes: ...


def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def cbc_encrypt(cipher: BlockCipher, iv: bytes, plaintext: bytes) -> bytes:
    """C[i] = E_K(P[i] xor C[i-1]) with C[0] = IV. Returns C[1..m] (the IV is not included).

    Precondition: len(iv) is the block size and len(plaintext) is a multiple of it.
    Cost: one block cipher call for each block, in sequence.
    """
    b = cipher.block_size
    if len(iv) != b or len(plaintext) % b:
        raise ValueError("CBC needs a one-block IV and whole plaintext blocks")
    prev = iv  # @line L1
    out = bytearray()
    for i in range(0, len(plaintext), b):  # @line L2
        prev = cipher.encrypt_block(_xor(plaintext[i : i + b], prev))  # @line L3
        out += prev
    return bytes(out)  # @line L4


def cbc_decrypt(cipher: BlockCipher, iv: bytes, ciphertext: bytes) -> bytes:
    """P[i] = D_K(C[i]) xor C[i-1] with C[0] = IV. The block calls are independent."""
    b = cipher.block_size
    if len(iv) != b or len(ciphertext) % b:
        raise ValueError("CBC needs a one-block IV and whole ciphertext blocks")
    c = iv + ciphertext  # @line L5
    out = bytearray()
    for i in range(b, len(c), b):  # @line L6
        out += _xor(cipher.decrypt_block(c[i : i + b]), c[i - b : i])  # @line L7
    return bytes(out)  # @line L8


def pkcs7_pad(data: bytes, b: int = 16) -> bytes:
    """Append k bytes of value k, with 1 <= k <= b, so that the length is a multiple of b."""
    k = b - len(data) % b
    return data + bytes([k]) * k


def pkcs7_unpad(data: bytes, b: int = 16) -> bytes:
    """Strict check: raise ValueError unless the last k bytes all have value k, 1 <= k <= b."""
    if not data or len(data) % b:
        raise ValueError("bad length")
    k = data[-1]
    if not 1 <= k <= b or data[-k:] != bytes([k]) * k:
        raise ValueError("bad padding")
    return data[:-k]
