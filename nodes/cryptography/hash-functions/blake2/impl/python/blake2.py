# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blake2/. The authors are listed in prov/9BR4W0.jsonl.
"""BLAKE2b and BLAKE2s as in RFC 7693, with the salt and personalization
fields of the BLAKE2 paper (Aumasson, Neves, Wilcox-O'Hearn, Winnerlein, 2013).

blake2b(data, nn, key) returns nn bytes, 1 <= nn <= 64, with a key of 0 to 64 bytes.
blake2s(data, nn, key) returns nn bytes, 1 <= nn <= 32, with a key of 0 to 32 bytes.

For study only. The code is not constant time and must not protect real data.
Use hashlib.blake2b and hashlib.blake2s, or crypto_generichash of libsodium.
"""

SIGMA = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
    (14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3),
    (11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4),
    (7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8),
    (9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13),
    (2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9),
    (12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11),
    (13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10),
    (6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5),
    (10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0),
)

# The first 64 (or 32) bits of the fractional parts of the square roots of the first
# eight primes: the SHA-512 and SHA-256 initial values (RFC 7693, Section 2.6).
IV_B = (
    0x6A09E667F3BCC908, 0xBB67AE8584CAA73B, 0x3C6EF372FE94F82B, 0xA54FF53A5F1D36F1,
    0x510E527FADE682D1, 0x9B05688C2B3E6C1F, 0x1F83D9ABFB41BD6B, 0x5BE0CD19137E2179,
)
IV_S = (
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
)


class Params:
    """The constants of one BLAKE2 instance (RFC 7693, Section 2.1)."""

    def __init__(self, w: int, r: int, rot: tuple, iv: tuple, offset_bytes: int) -> None:
        self.w = w  # bits in a word
        self.r = r  # rounds in F
        self.bb = 16 * w // 8  # block bytes
        self.nn_max = 8 * w // 8  # largest digest, in bytes
        self.rot = rot  # (R1, R2, R3, R4)
        self.iv = iv
        self.mask = (1 << w) - 1
        self.offset_bytes = offset_bytes  # size of the node offset field


BLAKE2B = Params(64, 12, (32, 24, 16, 63), IV_B, 8)
BLAKE2S = Params(32, 10, (16, 12, 8, 7), IV_S, 6)


def _rotr(x: int, n: int, w: int, mask: int) -> int:
    return ((x >> n) | (x << (w - n))) & mask


def g(p: Params, v: list[int], a: int, b: int, c: int, d: int, x: int, y: int) -> None:
    """The mixing function G of RFC 7693, Section 3.1 (pseudocode line L9)."""
    w, mask = p.w, p.mask
    r1, r2, r3, r4 = p.rot
    # @line L9
    v[a] = (v[a] + v[b] + x) & mask
    v[d] = _rotr(v[d] ^ v[a], r1, w, mask)
    v[c] = (v[c] + v[d]) & mask
    v[b] = _rotr(v[b] ^ v[c], r2, w, mask)
    v[a] = (v[a] + v[b] + y) & mask
    v[d] = _rotr(v[d] ^ v[a], r3, w, mask)
    v[c] = (v[c] + v[d]) & mask
    v[b] = _rotr(v[b] ^ v[c], r4, w, mask)


def compress(p: Params, h: list[int], block: bytes, t: int, last: bool, trace: list | None = None) -> list[int]:
    """The compression function F of RFC 7693, Section 3.2 (lines L6 to L8).

    If trace is a list, the work vector v is appended before round 0 and after each round,
    as in the "(i= k) v[16]" lines of Appendices A and B.
    """
    nb = p.w // 8
    m = [int.from_bytes(block[i * nb:(i + 1) * nb], "little") for i in range(16)]
    # @line L6
    v = list(h) + list(p.iv)
    v[12] ^= t & p.mask
    v[13] ^= (t >> p.w) & p.mask
    if last:
        v[14] ^= p.mask
    if trace is not None:
        trace.append(list(v))
    # @line L7
    for i in range(p.r):
        s = SIGMA[i % 10]
        g(p, v, 0, 4, 8, 12, m[s[0]], m[s[1]])
        g(p, v, 1, 5, 9, 13, m[s[2]], m[s[3]])
        g(p, v, 2, 6, 10, 14, m[s[4]], m[s[5]])
        g(p, v, 3, 7, 11, 15, m[s[6]], m[s[7]])
        g(p, v, 0, 5, 10, 15, m[s[8]], m[s[9]])
        g(p, v, 1, 6, 11, 12, m[s[10]], m[s[11]])
        g(p, v, 2, 7, 8, 13, m[s[12]], m[s[13]])
        g(p, v, 3, 4, 9, 14, m[s[14]], m[s[15]])
        if trace is not None:
            trace.append(list(v))
    # @line L8
    return [h[i] ^ v[i] ^ v[i + 8] for i in range(8)]


def parameter_block(p: Params, nn: int, kk: int, salt: bytes = b"", person: bytes = b"") -> bytes:
    """The parameter block for sequential hashing (fanout 1, depth 1, no tree fields).

    RFC 7693 sets only nn, kk and the bytes 01 01; the salt and personalization
    fields come from the BLAKE2 paper and are zero there.
    """
    side = p.bb // 8  # 16 bytes for BLAKE2b, 8 bytes for BLAKE2s
    if len(salt) > side or len(person) > side:
        raise ValueError("salt and personalization have at most %d bytes" % side)
    head = bytes([nn, kk, 1, 1]) + bytes(4 + p.offset_bytes + 2)  # leaf length, node offset, depth, inner length
    head += bytes(p.bb // 2 - 2 * side - len(head))  # reserved bytes (BLAKE2b only)
    return head + salt.ljust(side, b"\0") + person.ljust(side, b"\0")


def blake2(p: Params, data: bytes, nn: int, key: bytes = b"", salt: bytes = b"",
           person: bytes = b"", trace: list | None = None) -> bytes:
    """BLAKE2 of RFC 7693, Section 3.3 (lines L1 to L5)."""
    kk, ll, bb = len(key), len(data), p.bb
    if not 1 <= nn <= p.nn_max or kk > p.nn_max:
        raise ValueError("digest or key length out of range")
    nb = p.w // 8
    # @line L1
    pb = parameter_block(p, nn, kk, salt, person)
    h = [p.iv[i] ^ int.from_bytes(pb[i * nb:(i + 1) * nb], "little") for i in range(8)]
    # @line L2
    padded = (key.ljust(bb, b"\0") if kk else b"") + data
    if len(padded) == 0 or len(padded) % bb:
        padded = padded.ljust((len(padded) // bb + 1) * bb, b"\0")
    blocks = [padded[i:i + bb] for i in range(0, len(padded), bb)]  # a full last block gets no padding
    # @line L3
    for i, block in enumerate(blocks[:-1]):
        h = compress(p, h, block, (i + 1) * bb, False, trace)
    # @line L4
    h = compress(p, h, blocks[-1], ll + (bb if kk else 0), True, trace)
    # @line L5
    out = b"".join(x.to_bytes(nb, "little") for x in h)
    return out[:nn]


def blake2b(data: bytes, nn: int = 64, key: bytes = b"", salt: bytes = b"", person: bytes = b"") -> bytes:
    return blake2(BLAKE2B, data, nn, key, salt, person)


def blake2s(data: bytes, nn: int = 32, key: bytes = b"", salt: bytes = b"", person: bytes = b"") -> bytes:
    return blake2(BLAKE2S, data, nn, key, salt, person)
