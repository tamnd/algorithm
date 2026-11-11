# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/length-extension-attack/. The authors are listed in prov/8W23N6.jsonl.
"""Length extension on SHA-256: forge H(k || m || pad || x) from H(k || m) and the length of k.

For study only. The code is not constant time, and the attack runs only on a
local simulated MAC in the tests. Never build a MAC as H(k || m). Use HMAC
(hmac.new(key, msg, hashlib.sha256) in Python, FIPS 198-1), KMAC, or the keyed
mode of BLAKE2, from the standard library, a FIPS 140 validated module, or
libsodium.

SHA-256 below follows FIPS 180-4, Sections 4.1.2, 4.2.2, 5.1.1 and 6.2. The
attack needs one extra entry point: start the hash from a given state and a
given count of bytes already processed.
"""

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
H0 = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]
M32 = 0xFFFFFFFF


def _rotr(x: int, r: int) -> int:
    return ((x >> r) | (x << (32 - r))) & M32


def compress(state: list[int], block: bytes) -> list[int]:
    """The SHA-256 compression function on one 64-byte block."""
    w = [int.from_bytes(block[4 * i : 4 * i + 4], "big") for i in range(16)]
    for i in range(16, 64):
        s0 = _rotr(w[i - 15], 7) ^ _rotr(w[i - 15], 18) ^ (w[i - 15] >> 3)
        s1 = _rotr(w[i - 2], 17) ^ _rotr(w[i - 2], 19) ^ (w[i - 2] >> 10)
        w.append((w[i - 16] + s0 + w[i - 7] + s1) & M32)
    a, b, c, d, e, f, g, h = state
    for i in range(64):
        t1 = (h + (_rotr(e, 6) ^ _rotr(e, 11) ^ _rotr(e, 25)) + ((e & f) ^ (~e & g)) + K256[i] + w[i]) & M32
        t2 = ((_rotr(a, 2) ^ _rotr(a, 13) ^ _rotr(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))) & M32
        a, b, c, d, e, f, g, h = (t1 + t2) & M32, a, b, c, (d + t1) & M32, e, f, g
    return [(x + y) & M32 for x, y in zip(state, [a, b, c, d, e, f, g, h])]


def padding(byte_len: int) -> bytes:
    """The SHA-256 padding of a message of byte_len bytes: 0x80, zeros, the 64-bit bit length."""
    zeros = (55 - byte_len) % 64
    return b"\x80" + b"\x00" * zeros + (8 * byte_len).to_bytes(8, "big")


def sha256(data: bytes, state: list[int] | None = None, done: int = 0) -> bytes:
    """SHA-256 of data; or, with state and done, continue a hash that has already processed done bytes
    (done a multiple of 64) and reached state."""
    if done % 64:
        raise ValueError("done must be a multiple of 64")
    st = list(H0 if state is None else state)
    msg = data + padding(done + len(data))
    for i in range(0, len(msg), 64):
        st = compress(st, msg[i : i + 64])
    return b"".join(x.to_bytes(4, "big") for x in st)


def extend(tag: bytes, key_len: int, msg: bytes, extra: bytes) -> tuple[bytes, bytes]:
    """Given tag = SHA-256(k || msg) with len(k) = key_len, return (msg2, tag2) with
    msg2 = msg || pad || extra and tag2 = SHA-256(k || msg2). The key is not needed."""
    glue = padding(key_len + len(msg))  # @line L1
    state = [int.from_bytes(tag[4 * i : 4 * i + 4], "big") for i in range(8)]  # @line L2
    done = key_len + len(msg) + len(glue)  # @line L3
    tag2 = sha256(extra, state, done)  # @line L4
    return msg + glue + extra, tag2  # @line L5
