# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ctr-mode/. The authors are listed in prov/ZGS9FV.jsonl.
"""Counter (CTR) mode, NIST SP 800-38A Section 6.5 and Appendix B.

For study only. The code is not constant time and gives no integrity. Do not
use it to protect real data; use an AEAD mode such as AES-GCM from a FIPS 140
validated module, or ChaCha20-Poly1305 from libsodium.
"""

from typing import Protocol


class BlockCipher(Protocol):
    block_size: int

    def encrypt_block(self, block: bytes) -> bytes: ...


def counter_block(t1: bytes, j: int, m_bits: int) -> bytes:
    """T[j+1]: apply the standard incrementing function (SP 800-38A B.1) j times to T[1].

    Only the rightmost m_bits bits change; they count modulo 2^m. A wrap is an error,
    because it would repeat a counter block.
    """
    b = len(t1) * 8
    v = int.from_bytes(t1, "big")
    low = v & ((1 << m_bits) - 1)
    if low + j >= 1 << m_bits:
        raise OverflowError("the counter field would wrap and repeat a counter block")
    return (v + j).to_bytes(b // 8, "big")


def keystream_block(cipher: BlockCipher, t1: bytes, j: int, m_bits: int = 128) -> bytes:
    """O[j+1] = E_K(T[j+1]). Each block is independent: this is the random access of CTR."""
    return cipher.encrypt_block(counter_block(t1, j, m_bits))


def ctr_crypt(cipher: BlockCipher, t1: bytes, data: bytes, m_bits: int = 128) -> bytes:
    """Encrypt or decrypt (the same operation) with initial counter block t1.

    Precondition: no counter block T[j] is ever used twice under the key, in this
    message or any other. Cost: ceil(len(data) / block size) independent block calls.
    """
    b = cipher.block_size
    if len(t1) != b or not 1 <= m_bits <= 8 * b:
        raise ValueError("CTR needs a one-block initial counter and 1 <= m_bits <= block bits")
    out = bytearray()
    for j in range(0, (len(data) + b - 1) // b):  # @line L1
        t = counter_block(t1, j, m_bits)  # @line L2
        o = cipher.encrypt_block(t)  # @line L3
        chunk = data[j * b : (j + 1) * b]
        out += bytes(x ^ y for x, y in zip(chunk, o))  # @line L4
    return bytes(out)  # @line L5
