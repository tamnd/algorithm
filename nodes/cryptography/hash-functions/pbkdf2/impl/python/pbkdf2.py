# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pbkdf2/. The authors are listed in prov/G2X3X9.jsonl.
"""PBKDF2 with HMAC as the PRF (RFC 8018, Section 5.2).

The PRF is HMAC over a hash function from hashlib. HMAC is written out here
(RFC 2104): the password is the HMAC key, so its inner and outer padded
blocks are hashed once and the two hash states are copied for each of the
c iterations. This is the usual speed-up and it does not change the output.

For study only. The code is not constant time and must not protect real data.
Use hashlib.pbkdf2_hmac, or Argon2id from a library such as argon2-cffi or
libsodium for new password storage, instead.
"""

import hashlib


class _HmacKey:
    """HMAC-H with a fixed key: the inner and outer hash states after the padded key block."""

    def __init__(self, key: bytes, hash_name: str) -> None:
        probe = hashlib.new(hash_name)
        block = probe.block_size
        self.digest_size = probe.digest_size
        if len(key) > block:
            key = hashlib.new(hash_name, key).digest()
        key = key.ljust(block, b"\x00")
        self._inner = hashlib.new(hash_name, bytes(b ^ 0x36 for b in key))
        self._outer = hashlib.new(hash_name, bytes(b ^ 0x5C for b in key))

    def mac(self, msg: bytes) -> bytes:
        h = self._inner.copy()
        h.update(msg)
        o = self._outer.copy()
        o.update(h.digest())
        return o.digest()


def _xor(a: bytes, b: bytes) -> bytes:
    return (int.from_bytes(a, "big") ^ int.from_bytes(b, "big")).to_bytes(len(a), "big")


def pbkdf2_block(prf: _HmacKey, salt: bytes, c: int, i: int) -> bytes:
    """T_i = U_1 xor U_2 xor ... xor U_c (RFC 8018, Section 5.2, step 3)."""
    u = prf.mac(salt + i.to_bytes(4, "big"))  # @line L4
    t = u  # @line L4
    for _ in range(2, c + 1):
        u = prf.mac(u)  # @line L5
        t = _xor(t, u)  # @line L5
    return t


def pbkdf2(password: bytes, salt: bytes, c: int, dk_len: int, hash_name: str = "sha256") -> bytes:
    """PBKDF2-HMAC-H(P, S, c, dkLen) as bytes."""
    if c < 1:
        raise ValueError("the iteration count c must be at least 1")
    prf = _HmacKey(password, hash_name)
    h_len = prf.digest_size
    if dk_len > (2**32 - 1) * h_len:
        raise ValueError("derived key too long")  # @line L1
    blocks = -(-dk_len // h_len)  # @line L2
    out = b"".join(pbkdf2_block(prf, salt, c, i) for i in range(1, blocks + 1))  # @line L3
    return out[:dk_len]  # @line L6


def verify(password: bytes, salt: bytes, c: int, stored: bytes, hash_name: str = "sha256") -> bool:
    """Recompute and compare. A real verifier compares in constant time (hmac.compare_digest)."""
    return pbkdf2(password, salt, c, len(stored), hash_name) == stored  # @line L7
