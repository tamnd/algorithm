# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/authenticated-encryption/. The authors are listed in prov/NRR0YJ.jsonl.
"""Generic composition of AES-CTR and AES-CMAC: encrypt-then-MAC, and the two weaker orders.

For study only. This code is not constant time (the AES in aes.py uses table
lookups) and must not protect real data. Use a standard AEAD such as AES-GCM
from a FIPS 140 validated module, or crypto_aead_xchacha20poly1305_ietf in
libsodium, instead. The MAC-then-encrypt and encrypt-and-MAC functions are here
only to show how they fail.
"""

from aes import AES


class InvalidCiphertext(ValueError):
    """Decryption found a bad tag. No plaintext is returned."""


def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def ctr(key: bytes, nonce: bytes, data: bytes) -> bytes:
    """AES-CTR with a 12-byte nonce and a 4-byte block counter that starts at 0."""
    if len(nonce) != 12:
        raise ValueError("the nonce has 12 bytes")
    if len(data) > 16 * (1 << 32):
        raise ValueError("too long for a 32-bit block counter")
    e = AES(key)
    out = bytearray()
    for j in range(0, len(data), 16):
        out += _xor(data[j : j + 16], e.encrypt_block(nonce + (j // 16).to_bytes(4, "big")))
    return bytes(out)


def _dbl(x: bytes) -> bytes:
    v = int.from_bytes(x, "big") << 1
    if v >> 128:
        v ^= (1 << 128) | 0x87
    return v.to_bytes(16, "big")


def cmac(key: bytes, m: bytes) -> bytes:
    """AES-CMAC (SP 800-38B), a PRF on strings of any length, used here as the MAC."""
    e = AES(key)
    k1 = _dbl(e.encrypt_block(bytes(16)))
    k2 = _dbl(k1)
    n = max(1, -(-len(m) // 16))
    last = m[16 * (n - 1) :]
    last = _xor(last, k1) if len(last) == 16 else _xor(last + b"\x80" + bytes(15 - len(last)), k2)
    c = bytes(16)
    for i in range(n - 1):
        c = e.encrypt_block(_xor(c, m[16 * i : 16 * i + 16]))
    return e.encrypt_block(_xor(c, last))


def tags_equal(a: bytes, b: bytes) -> bool:
    """Compare two tags by reading every byte and folding the differences with OR."""
    if len(a) != len(b):
        return False
    d = 0
    for x, y in zip(a, b):
        d |= x ^ y
    return d == 0


def _mac_input(nonce: bytes, ad: bytes, c: bytes) -> bytes:
    """An injective encoding: nonce, associated data and ciphertext, then both lengths in 8 bytes."""
    return nonce + ad + c + len(ad).to_bytes(8, "big") + len(c).to_bytes(8, "big")


def etm_encrypt(ke: bytes, km: bytes, nonce: bytes, ad: bytes, p: bytes) -> bytes:
    """Encrypt-then-MAC: C = CTR(ke, N, P), T = CMAC(km, N, A, C). Output C || T."""
    c = ctr(ke, nonce, p)
    return c + cmac(km, _mac_input(nonce, ad, c))


def etm_decrypt(ke: bytes, km: bytes, nonce: bytes, ad: bytes, ct: bytes) -> bytes:
    """Check the tag first; decrypt only if it is valid."""
    if len(ct) < 16:
        raise InvalidCiphertext("too short")
    c, t = ct[:-16], ct[-16:]
    if not tags_equal(cmac(km, _mac_input(nonce, ad, c)), t):
        raise InvalidCiphertext("bad tag")
    return ctr(ke, nonce, c)


def eam_encrypt(ke: bytes, km: bytes, nonce: bytes, p: bytes) -> bytes:
    """Encrypt-and-MAC: C = CTR(ke, N, P), T = CMAC(km, P). The tag of P is sent in the clear."""
    return ctr(ke, nonce, p) + cmac(km, p)


def eam_decrypt(ke: bytes, km: bytes, nonce: bytes, ct: bytes) -> bytes:
    c, t = ct[:-16], ct[-16:]
    p = ctr(ke, nonce, c)
    if not tags_equal(cmac(km, p), t):
        raise InvalidCiphertext("bad tag")
    return p


# A secure but redundant encryption scheme, used to build the MAC-then-encrypt counterexample of
# Bellare and Namprempre: CTR, followed by one extra byte that decryption ignores. It is still
# IND-CPA (the extra byte is a constant), but its ciphertexts are malleable in that byte.
def redundant_encrypt(ke: bytes, nonce: bytes, x: bytes) -> bytes:
    return ctr(ke, nonce, x) + b"\x00"


def redundant_decrypt(ke: bytes, nonce: bytes, y: bytes) -> bytes:
    return ctr(ke, nonce, y[:-1])


def mte_encrypt(ke: bytes, km: bytes, nonce: bytes, p: bytes) -> bytes:
    """MAC-then-encrypt: T = CMAC(km, P), C = E(ke, N, P || T)."""
    return redundant_encrypt(ke, nonce, p + cmac(km, p))


def mte_decrypt(ke: bytes, km: bytes, nonce: bytes, ct: bytes) -> bytes:
    x = redundant_decrypt(ke, nonce, ct)
    p, t = x[:-16], x[-16:]
    if len(x) < 16 or not tags_equal(cmac(km, p), t):
        raise InvalidCiphertext("bad tag")
    return p
