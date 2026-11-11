# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cbc-mac/. The authors are listed in prov/3RSETN.jsonl.
"""CBC-MAC with a zero IV, the two classic repairs, and a broken random-IV variant.

For study only. This code is not constant time (the AES in aes.py uses table
lookups) and must not protect real data. Plain CBC-MAC is secure only for
messages of one fixed length. Use CMAC or HMAC from a FIPS 140 validated module,
or crypto_auth in libsodium, instead.
"""

from typing import Protocol


class BlockCipher(Protocol):
    block_size: int

    def encrypt_block(self, block: bytes) -> bytes: ...


def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def tags_equal(a: bytes, b: bytes) -> bool:
    """Compare two tags by reading every byte and folding the differences with OR."""
    if len(a) != len(b):
        return False
    d = 0
    for x, y in zip(a, b):
        d |= x ^ y
    return d == 0


def cbc_mac(cipher: BlockCipher, m: bytes) -> bytes:
    """The tag Y_m of Y_0 = 0^n, Y_j = E_K(Y_{j-1} xor M_j). No padding: |m| must be a positive multiple of n."""
    n = cipher.block_size
    if len(m) == 0 or len(m) % n:
        raise ValueError("CBC-MAC here takes a positive whole number of blocks")
    y = bytes(n)  # @line L1
    for j in range(0, len(m), n):  # @line L2
        y = cipher.encrypt_block(_xor(y, m[j : j + n]))  # @line L3
    return y  # @line L4


def cbc_mac_verify(cipher: BlockCipher, m: bytes, tag: bytes) -> bool:
    return tags_equal(cbc_mac(cipher, m), tag)  # @line L5


def cbc_mac_length_prepended(cipher: BlockCipher, m: bytes) -> bytes:
    """Repair 1: put the length in bits, as one n-byte big-endian block, before the message."""
    n = cipher.block_size
    return cbc_mac(cipher, (8 * len(m)).to_bytes(n, "big") + m)


def emac(cipher1: BlockCipher, cipher2: BlockCipher, m: bytes) -> bytes:
    """Repair 2 (EMAC, ISO/IEC 9797-1 MAC algorithm 2 without padding): encrypt the CBC-MAC under a second key."""
    return cipher2.encrypt_block(cbc_mac(cipher1, m))


def cbc_mac_random_iv(cipher: BlockCipher, m: bytes, iv: bytes) -> tuple[bytes, bytes]:
    """A broken variant: start the chain at a random IV and send (iv, tag). Shown only to be attacked."""
    n = cipher.block_size
    y = cbc_mac(cipher, _xor(iv, m[:n]) + m[n:])
    return iv, y


def cbc_mac_random_iv_verify(cipher: BlockCipher, m: bytes, iv: bytes, tag: bytes) -> bool:
    return tags_equal(cbc_mac_random_iv(cipher, m, iv)[1], tag)
