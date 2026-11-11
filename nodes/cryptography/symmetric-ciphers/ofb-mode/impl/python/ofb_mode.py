# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ofb-mode/. The authors are listed in prov/K2XCQP.jsonl.
"""Output feedback (OFB) mode, NIST SP 800-38A Section 6.4.

For study only. The code is not constant time and gives no integrity. Do not
use it to protect real data; use an AEAD mode from a FIPS 140 validated module
or libsodium.
"""

from typing import Protocol


class BlockCipher(Protocol):
    block_size: int

    def encrypt_block(self, block: bytes) -> bytes: ...


def ofb_keystream(cipher: BlockCipher, iv: bytes, length: int) -> bytes:
    """The first `length` bytes of O[1] || O[2] || ..., with O[0] = IV and O[j] = E_K(O[j-1])."""
    if len(iv) != cipher.block_size:
        raise ValueError("OFB needs a one-block IV")
    o = iv  # @line L1
    out = bytearray()
    while len(out) < length:  # @line L2
        o = cipher.encrypt_block(o)  # @line L3
        out += o
    return bytes(out[:length])


def ofb_crypt(cipher: BlockCipher, iv: bytes, data: bytes) -> bytes:
    """Encrypt or decrypt (the same operation): XOR the data with the OFB keystream.

    The IV must be unique for each message under the key. The last block may be partial.
    Cost: ceil(len(data) / block size) block cipher calls, in sequence, and they do not
    depend on the data, so the keystream can be computed in advance.
    """
    ks = ofb_keystream(cipher, iv, len(data))
    out = bytes(x ^ y for x, y in zip(data, ks))  # @line L4
    return out  # @line L5
