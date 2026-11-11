# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nmac/. The authors are listed in prov/81YGXR.jsonl.
"""NMAC (Bellare, Canetti and Krawczyk 1996) over the SHA-256 compression function.

NMAC(k1, k2, m) = F_k1(F_k2(m)), where F_k is the Merkle-Damgard iteration of
the SHA-256 compression function f started from the chaining value k (a key of
32 bytes) instead of the standard IV. The compression function is written here
in pure Python (FIPS 180-4, Section 6.2.2), because hashlib does not let a
caller set the IV.

For study only. The code is not constant time and must not protect real data.
Use HMAC from the standard library or a FIPS 140 validated module instead.
"""

MASK = 0xFFFFFFFF

# FIPS 180-4, Section 4.2.2: the first 32 bits of the fractional parts of the
# cube roots of the first 64 primes.
K256 = [
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
]

# FIPS 180-4, Section 5.3.3: the initial hash value of SHA-256.
IV = bytes.fromhex("6a09e667bb67ae853c6ef372a54ff53a510e527f9b05688c1f83d9ab5be0cd19")

BLOCK = 64  # bytes in one message block
CHAIN = 32  # bytes in one chaining value, also the key length of NMAC


def _rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK


def compress(h: bytes, block: bytes) -> bytes:
    """f(h, block): the SHA-256 compression function, with the feed-forward."""
    assert len(h) == CHAIN and len(block) == BLOCK
    w = [int.from_bytes(block[4 * i : 4 * i + 4], "big") for i in range(16)]
    for t in range(16, 64):
        s0 = _rotr(w[t - 15], 7) ^ _rotr(w[t - 15], 18) ^ (w[t - 15] >> 3)
        s1 = _rotr(w[t - 2], 17) ^ _rotr(w[t - 2], 19) ^ (w[t - 2] >> 10)
        w.append((w[t - 16] + s0 + w[t - 7] + s1) & MASK)
    hv = [int.from_bytes(h[4 * i : 4 * i + 4], "big") for i in range(8)]
    a, b, c, d, e, f, g, hh = hv
    for t in range(64):
        t1 = (hh + (_rotr(e, 6) ^ _rotr(e, 11) ^ _rotr(e, 25)) + ((e & f) ^ (~e & g)) + K256[t] + w[t]) & MASK
        t2 = ((_rotr(a, 2) ^ _rotr(a, 13) ^ _rotr(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))) & MASK
        hh, g, f, e, d, c, b, a = g, f, e, (d + t1) & MASK, c, b, a, (t1 + t2) & MASK
    out = [(x + y) & MASK for x, y in zip(hv, [a, b, c, d, e, f, g, hh])]
    return b"".join(x.to_bytes(4, "big") for x in out)


def md_pad(length: int) -> bytes:
    """The SHA-256 padding for an input of `length` bytes: 0x80, zeros, the bit length."""
    zeros = (55 - length) % BLOCK
    return b"\x80" + bytes(zeros) + (8 * length).to_bytes(8, "big")


def iterate(k: bytes, data: bytes) -> bytes:
    """f*(k, data): run f over the 64-byte blocks of data, starting from k."""
    assert len(data) % BLOCK == 0
    h = k
    for i in range(0, len(data), BLOCK):
        h = compress(h, data[i : i + BLOCK])
    return h


def keyed_hash(k: bytes, x: bytes, offset: int = 0) -> bytes:
    """F_k(x) = f*(k, x || pad(offset + |x|)).

    With k = IV and offset = 0 this is SHA-256. The offset counts bytes that
    were hashed before k was reached; HMAC uses offset = 64.
    """
    if len(k) != CHAIN:
        raise ValueError("an NMAC key is a 32-byte chaining value")
    return iterate(k, x + md_pad(offset + len(x)))


def sha256(x: bytes) -> bytes:
    """SHA-256 from the compression function, to check it against hashlib."""
    return keyed_hash(IV, x)


def nmac(k1: bytes, k2: bytes, m: bytes, offset: int = 0) -> bytes:
    """NMAC(k1, k2, m) = F_k1(F_k2(m))."""
    inner = keyed_hash(k2, m, offset)  # @line L1
    return keyed_hash(k1, inner, offset)  # @line L2


def hmac_keys(key: bytes) -> tuple[bytes, bytes]:
    """The NMAC keys (k1, k2) hidden in HMAC-SHA-256 with key K (keys of at most 64 bytes)."""
    if len(key) > BLOCK:
        raise ValueError("this helper takes keys of at most 64 bytes")
    kp = key + bytes(BLOCK - len(key))  # @line L3
    k1 = compress(IV, bytes(x ^ 0x5C for x in kp))  # @line L4
    k2 = compress(IV, bytes(x ^ 0x36 for x in kp))  # @line L4
    return k1, k2


def hmac_via_nmac(key: bytes, m: bytes) -> bytes:
    """HMAC-SHA-256(K, m) computed as NMAC with the derived keys and offset 64."""
    k1, k2 = hmac_keys(key)
    return nmac(k1, k2, m, offset=BLOCK)  # @line L5
