# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/groestl/. The authors are listed in prov/AE3QKK.jsonl.
"""Grøstl, the final-round version (specification of 2 March 2011), for study only.

The state is a list of bytes in column order: entry a[i][j] (row i, column j) is
s[8 * j + i], which is the byte mapping of Section 3.4.1. The code hashes whole
bytes only and is not constant time: the s-box is a table lookup.
"""


def _xtime(a: int) -> int:
    a <<= 1
    return a ^ 0x11B if a & 0x100 else a


def _gmul(a: int, b: int) -> int:
    r = 0
    while b:
        if b & 1:
            r ^= a
        a = _xtime(a)
        b >>= 1
    return r


def _make_sbox() -> list[int]:
    """The Rijndael s-box (Appendix B): inverse in GF(2^8), then the affine map."""
    sbox = []
    for x in range(256):
        inv = 0 if x == 0 else next(y for y in range(1, 256) if _gmul(x, y) == 1)
        s = inv
        for k in range(1, 5):
            s ^= ((inv << k) | (inv >> (8 - k))) & 0xFF
        sbox.append(s ^ 0x63)
    return sbox


SBOX = _make_sbox()
B_ROW = (2, 2, 3, 4, 5, 3, 5, 7)  # B = circ(02, 02, 03, 04, 05, 03, 05, 07), Section 3.4.5
MUL = {c: [_gmul(x, c) for x in range(256)] for c in set(B_ROW)}

SHIFT = {
    ("P", 8): (0, 1, 2, 3, 4, 5, 6, 7),
    ("Q", 8): (1, 3, 5, 7, 0, 2, 4, 6),
    ("P", 16): (0, 1, 2, 3, 4, 5, 6, 11),
    ("Q", 16): (1, 3, 5, 11, 0, 2, 4, 6),
}


def permutation(which: str, state: list[int]) -> list[int]:
    """P or Q on an 8 x v state, v = 8 (512 bits, 10 rounds) or v = 16 (1024 bits, 14 rounds)."""
    v = len(state) // 8
    rounds = 10 if v == 8 else 14
    sigma = SHIFT[(which, v)]
    a = list(state)
    for i in range(rounds):  # @line L5
        if which == "P":  # @line L6
            for j in range(v):
                a[8 * j] ^= (j << 4) ^ i
        else:
            for j in range(v):
                for r in range(7):
                    a[8 * j + r] ^= 0xFF
                a[8 * j + 7] ^= 0xFF ^ (j << 4) ^ i
        a = [SBOX[x] for x in a]  # @line L7
        a = [a[8 * ((j + sigma[r]) % v) + r] for j in range(v) for r in range(8)]  # @line L8
        out = []
        for j in range(v):  # @line L9
            col = a[8 * j:8 * j + 8]
            for r in range(8):
                acc = 0
                for c in range(8):
                    acc ^= MUL[B_ROW[(c - r) % 8]][col[c]]
                out.append(acc)
        a = out
    return a


def compress(h: bytes, m: bytes) -> bytes:
    """f(h, m) = P(h xor m) xor Q(m) xor h, Section 3.2."""
    p = permutation("P", [x ^ y for x, y in zip(h, m)])
    q = permutation("Q", list(m))
    return bytes(x ^ y ^ z for x, y, z in zip(p, q, h))


def pad(msg: bytes, block: int) -> bytes:
    """Section 3.6 for a message of whole bytes: a 1 bit, zeros, and the 64-bit block count."""
    nbits = 8 * len(msg)
    w = (-nbits - 65) % (8 * block)
    count = (nbits + w + 65) // (8 * block)
    return msg + b"\x80" + bytes((w - 7) // 8) + count.to_bytes(8, "big")


def groestl(msg: bytes, n: int = 256, trace: list[bytes] | None = None) -> bytes:
    """Grøstl-n for n a multiple of 8 from 8 to 512."""
    if n % 8 or not 8 <= n <= 512:
        raise ValueError("n must be a multiple of 8 from 8 to 512")
    block = 64 if n <= 256 else 128  # @line L1
    h = n.to_bytes(block, "big")
    padded = pad(msg, block)  # @line L2
    for k in range(0, len(padded), block):
        h = compress(h, padded[k:k + block])  # @line L3
        if trace is not None:
            trace.append(h)
    x = bytes(a ^ b for a, b in zip(permutation("P", list(h)), h))  # @line L4
    return x[block - n // 8:]


def groestl256(msg: bytes) -> bytes:
    return groestl(msg, 256)


def groestl512(msg: bytes) -> bytes:
    return groestl(msg, 512)
