# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ecb-mode/. The authors are listed in prov/3HG8V8.jsonl.
"""Electronic codebook (ECB) mode, NIST SP 800-38A Section 6.1.

For study only. The code is not constant time and ECB is not a secure way to
encrypt more than one block. Do not use it to protect real data. Use an AEAD
mode such as AES-GCM from a FIPS 140 validated module or from libsodium.
"""

from typing import Protocol


class BlockCipher(Protocol):
    block_size: int

    def encrypt_block(self, block: bytes) -> bytes: ...

    def decrypt_block(self, block: bytes) -> bytes: ...


def ecb_encrypt(cipher: BlockCipher, plaintext: bytes) -> bytes:
    """Encrypt each block on its own. The length must be a multiple of the block size.

    Cost: one block cipher call for each block. The calls are independent.
    """
    b = cipher.block_size
    if len(plaintext) % b:
        raise ValueError("ECB needs a whole number of blocks; pad the message first")
    out = bytearray()
    for i in range(0, len(plaintext), b):  # @line L1
        out += cipher.encrypt_block(plaintext[i : i + b])  # @line L2
    return bytes(out)  # @line L3


def ecb_decrypt(cipher: BlockCipher, ciphertext: bytes) -> bytes:
    """Invert ecb_encrypt with the inverse cipher, one block at a time."""
    b = cipher.block_size
    if len(ciphertext) % b:
        raise ValueError("ECB ciphertext must be a whole number of blocks")
    out = bytearray()
    for i in range(0, len(ciphertext), b):  # @line L4
        out += cipher.decrypt_block(ciphertext[i : i + b])  # @line L5
    return bytes(out)  # @line L6
