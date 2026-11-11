# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rc6/. The authors are listed in prov/FKPS33.jsonl.
"""RC6-w/r/b (Rivest, Robshaw, Sidney and Yin, 1998).

For study only. This code is not constant time: the rotation amounts depend
on the data, and Python itself leaks timing. Do not use it to protect real
data. Use AES from a validated library instead.

The AES submission is RC6-32/20/b with b = 16, 24 or 32. The block is four
w-bit words A, B, C, D, read little-endian from the bytes, so the first byte
of the block is the low byte of A. Cost: r rounds, each with 2 multiplications
modulo 2^w, 4 rotations (2 by a data-dependent amount) and 2 additions, and
a key schedule of 3 * max(c, 2r + 4) steps, where c is the number of key words.
"""

MAGIC = {
    16: (0xB7E1, 0x9E37),
    32: (0xB7E15163, 0x9E3779B9),
    64: (0xB7E151628AED2A6B, 0x9E3779B97F4A7C15),
}


def rotl(x: int, s: int, w: int) -> int:
    s %= w
    return ((x << s) | (x >> (w - s))) & ((1 << w) - 1)


def rotr(x: int, s: int, w: int) -> int:
    return rotl(x, w - (s % w), w)


def key_schedule(key: bytes, r: int = 20, w: int = 32) -> list[int]:
    """Return the round keys S[0 .. 2r + 3]."""
    if w not in MAGIC:
        raise ValueError("w must be 16, 32 or 64")
    u = w // 8
    mask = (1 << w) - 1
    c = max(1, -(-len(key) // u))
    big_l = [0] * c
    for i in range(len(key) - 1, -1, -1):
        big_l[i // u] = ((big_l[i // u] << 8) + key[i]) & mask
    p, q = MAGIC[w]
    t = 2 * r + 4
    s = [(p + i * q) & mask for i in range(t)]  # @line L12
    a = b = i = j = 0  # @line L13
    for _ in range(3 * max(c, t)):  # @line L14
        a = s[i] = rotl((s[i] + a + b) & mask, 3, w)  # @line L15
        b = big_l[j] = rotl((big_l[j] + a + b) & mask, a + b, w)
        i = (i + 1) % t  # @line L16
        j = (j + 1) % c
    return s  # @line L17


def _lgw(w: int) -> int:
    return w.bit_length() - 1


def encrypt_words(regs: list[int], s: list[int], w: int = 32) -> list[int]:
    mask = (1 << w) - 1
    r = len(s) // 2 - 2
    a, b, c, d = regs
    b = (b + s[0]) & mask  # @line L1
    d = (d + s[1]) & mask  # @line L2
    for i in range(1, r + 1):  # @line L3
        t = rotl((b * (2 * b + 1)) & mask, _lgw(w), w)  # @line L4
        u = rotl((d * (2 * d + 1)) & mask, _lgw(w), w)  # @line L5
        a = (rotl(a ^ t, u, w) + s[2 * i]) & mask  # @line L6
        c = (rotl(c ^ u, t, w) + s[2 * i + 1]) & mask  # @line L7
        a, b, c, d = b, c, d, a  # @line L8
    a = (a + s[2 * r + 2]) & mask  # @line L9
    c = (c + s[2 * r + 3]) & mask  # @line L10
    return [a, b, c, d]  # @line L11


def decrypt_words(regs: list[int], s: list[int], w: int = 32) -> list[int]:
    mask = (1 << w) - 1
    r = len(s) // 2 - 2
    a, b, c, d = regs
    c = (c - s[2 * r + 3]) & mask
    a = (a - s[2 * r + 2]) & mask
    for i in range(r, 0, -1):
        a, b, c, d = d, a, b, c
        u = rotl((d * (2 * d + 1)) & mask, _lgw(w), w)
        t = rotl((b * (2 * b + 1)) & mask, _lgw(w), w)
        c = rotr((c - s[2 * i + 1]) & mask, t, w) ^ u
        a = rotr((a - s[2 * i]) & mask, u, w) ^ t
    d = (d - s[1]) & mask
    b = (b - s[0]) & mask
    return [a, b, c, d]


def _split(block: bytes, w: int) -> list[int]:
    u = w // 8
    if len(block) != 4 * u:
        raise ValueError("the block must have 4w/8 bytes")
    return [int.from_bytes(block[k * u:(k + 1) * u], "little") for k in range(4)]


def _join(regs: list[int], w: int) -> bytes:
    return b"".join(x.to_bytes(w // 8, "little") for x in regs)


def encrypt_block(key: bytes, block: bytes, r: int = 20, w: int = 32) -> bytes:
    return _join(encrypt_words(_split(block, w), key_schedule(key, r, w), w), w)


def decrypt_block(key: bytes, block: bytes, r: int = 20, w: int = 32) -> bytes:
    return _join(decrypt_words(_split(block, w), key_schedule(key, r, w), w), w)
