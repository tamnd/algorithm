# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cfb-mode/. The authors are listed in prov/MXBPBC.jsonl.
"""Cipher feedback (CFB) mode, NIST SP 800-38A Section 6.3, for segment sizes of whole bytes.

This code supports CFB-s for s = 8, 16, ..., 128 bits (s_bytes from 1 to the block
size). It does not implement CFB-1, the one-bit variant of the standard.

For study only. The code is not constant time and gives no integrity. Do not
use it to protect real data; use an AEAD mode from a FIPS 140 validated module
or libsodium.
"""

from typing import Protocol


class BlockCipher(Protocol):
    block_size: int

    def encrypt_block(self, block: bytes) -> bytes: ...


def _cfb(cipher: BlockCipher, iv: bytes, data: bytes, s_bytes: int, decrypt: bool) -> bytes:
    b = cipher.block_size
    if len(iv) != b or not 1 <= s_bytes <= b or len(data) % s_bytes:
        raise ValueError("CFB needs a one-block IV and whole segments of s_bytes")
    reg = iv  # @line L1
    out = bytearray()
    for j in range(0, len(data), s_bytes):  # @line L2
        o = cipher.encrypt_block(reg)  # @line L3
        seg = data[j : j + s_bytes]
        res = bytes(x ^ y for x, y in zip(seg, o[:s_bytes]))  # @line L4
        out += res
        c = seg if decrypt else res  # the ciphertext segment is fed back in both directions
        reg = reg[s_bytes:] + c  # @line L5
    return bytes(out)  # @line L6


def cfb_encrypt(cipher: BlockCipher, iv: bytes, plaintext: bytes, s_bytes: int = 16) -> bytes:
    """CFB-s encryption: C#[j] = P#[j] xor MSB_s(E_K(I[j])), I[j+1] = LSB_(b-s)(I[j]) || C#[j].

    Cost: one block cipher call per segment of s_bytes, in sequence.
    """
    return _cfb(cipher, iv, plaintext, s_bytes, decrypt=False)


def cfb_decrypt(cipher: BlockCipher, iv: bytes, ciphertext: bytes, s_bytes: int = 16) -> bytes:
    """CFB-s decryption. It uses only the forward cipher, and the calls can run in parallel."""
    return _cfb(cipher, iv, ciphertext, s_bytes, decrypt=True)
