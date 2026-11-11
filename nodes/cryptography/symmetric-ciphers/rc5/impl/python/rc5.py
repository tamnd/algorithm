# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rc5/. The authors are listed in prov/NB7K96.jsonl.
"""RC5-w/r/b (Rivest 1994; RFC 2040): key expansion, encryption, decryption.

For study only. This code is not constant time: the rotation amounts depend
on the data, and Python itself leaks timing. Do not use it to protect real
data. Use AES or ChaCha20 from a validated library instead.

w is the word size in bits (16, 32 or 64), r the number of rounds and b the
key length in bytes. Words are read little-endian from bytes, as in the RC5
paper and RFC 2040. Cost: 2r + 2 additions for the block, 2r rotations by a
data-dependent amount, and 3 * max(c, 2r + 2) steps for the key expansion,
where c is the number of key words.
"""

# The magic constants P_w = Odd((e - 2) 2^w) and Q_w = Odd((phi - 1) 2^w).
MAGIC = {
    16: (0xB7E1, 0x9E37),
    32: (0xB7E15163, 0x9E3779B9),
    64: (0xB7E151628AED2A6B, 0x9E3779B97F4A7C15),
}


def rotl(x: int, s: int, w: int) -> int:
    s %= w
    mask = (1 << w) - 1
    return ((x << s) | (x >> (w - s))) & mask


def rotr(x: int, s: int, w: int) -> int:
    return rotl(x, w - (s % w), w)


def expand_key(key: bytes, r: int, w: int = 32) -> list[int]:
    """Return the table S[0 .. 2r + 1] of the RC5 key expansion."""
    if w not in MAGIC:
        raise ValueError("w must be 16, 32 or 64")
    if not 0 <= r <= 255 or len(key) > 255:
        raise ValueError("r and b must be at most 255")
    u = w // 8
    mask = (1 << w) - 1
    c = max(1, -(-len(key) // u))
    big_l = [0] * c
    for i in range(len(key) - 1, -1, -1):
        big_l[i // u] = ((big_l[i // u] << 8) + key[i]) & mask  # @line L7
    p, q = MAGIC[w]
    t = 2 * r + 2  # @line L8
    s = [(p + i * q) & mask for i in range(t)]  # @line L9
    a = b = i = j = 0  # @line L10
    for _ in range(3 * max(t, c)):  # @line L11
        a = s[i] = rotl((s[i] + a + b) & mask, 3, w)  # @line L12
        b = big_l[j] = rotl((big_l[j] + a + b) & mask, a + b, w)  # @line L13
        i = (i + 1) % t  # @line L14
        j = (j + 1) % c
    return s  # @line L15


def encrypt_words(a: int, b: int, s: list[int], w: int = 32) -> tuple[int, int]:
    mask = (1 << w) - 1
    r = len(s) // 2 - 1
    a = (a + s[0]) & mask  # @line L1
    b = (b + s[1]) & mask  # @line L2
    for i in range(1, r + 1):  # @line L3
        a = (rotl(a ^ b, b, w) + s[2 * i]) & mask  # @line L4
        b = (rotl(b ^ a, a, w) + s[2 * i + 1]) & mask  # @line L5
    return a, b  # @line L6


def decrypt_words(a: int, b: int, s: list[int], w: int = 32) -> tuple[int, int]:
    mask = (1 << w) - 1
    r = len(s) // 2 - 1
    for i in range(r, 0, -1):
        b = rotr((b - s[2 * i + 1]) & mask, a, w) ^ a
        a = rotr((a - s[2 * i]) & mask, b, w) ^ b
    b = (b - s[1]) & mask
    a = (a - s[0]) & mask
    return a, b


def encrypt_block(key: bytes, block: bytes, r: int = 12, w: int = 32) -> bytes:
    u = w // 8
    if len(block) != 2 * u:
        raise ValueError("the block must have 2w/8 bytes")
    s = expand_key(key, r, w)
    a, b = encrypt_words(int.from_bytes(block[:u], "little"), int.from_bytes(block[u:], "little"), s, w)
    return a.to_bytes(u, "little") + b.to_bytes(u, "little")


def decrypt_block(key: bytes, block: bytes, r: int = 12, w: int = 32) -> bytes:
    u = w // 8
    if len(block) != 2 * u:
        raise ValueError("the block must have 2w/8 bytes")
    s = expand_key(key, r, w)
    a, b = decrypt_words(int.from_bytes(block[:u], "little"), int.from_bytes(block[u:], "little"), s, w)
    return a.to_bytes(u, "little") + b.to_bytes(u, "little")
