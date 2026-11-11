# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tiger-hash/. The authors are listed in prov/6RCPBE.jsonl.
"""Tiger and Tiger2 (Anderson and Biham, 1996): 192-bit hash on 64-bit words.

For study only. This code is not constant time (it indexes tables by secret
bytes) and is not for real data. Tiger is not in hashlib or in FIPS; use
SHA-256, SHA-512/256 or SHA-3 from hashlib or OpenSSL instead.

The four S-boxes of 256 words of 64 bits are generated here by the procedure of
the designers' gen-sboxes.c: start from tables whose words repeat the byte i,
then swap bytes in columns under the control of Tiger compressions of a fixed
string. The tests check the tables against words printed in the paper.

Words are little-endian. Tiger pads with the byte 0x01 and Tiger2 with 0x80;
nothing else differs. Cost: 24 rounds of 8 table lookups per 64-byte block.
"""

MASK = (1 << 64) - 1
GEN_STRING = b"Tiger - A Fast New Hash Function, by Ross Anderson and Eli Biham"
IV = (0x0123456789ABCDEF, 0xFEDCBA9876543210, 0xF096A5B4C3B2E187)


def key_schedule(x: list[int]) -> None:
    """Mix the 8 message words between passes."""
    x[0] = (x[0] - (x[7] ^ 0xA5A5A5A5A5A5A5A5)) & MASK
    x[1] ^= x[0]
    x[2] = (x[2] + x[1]) & MASK
    x[3] = (x[3] - (x[2] ^ ((~x[1] << 19) & MASK))) & MASK
    x[4] ^= x[3]
    x[5] = (x[5] + x[4]) & MASK
    x[6] = (x[6] - (x[5] ^ ((~x[4] & MASK) >> 23))) & MASK
    x[7] ^= x[6]
    x[0] = (x[0] + x[7]) & MASK
    x[1] = (x[1] - (x[0] ^ ((~x[7] << 19) & MASK))) & MASK
    x[2] ^= x[1]
    x[3] = (x[3] + x[2]) & MASK
    x[4] = (x[4] - (x[3] ^ ((~x[2] & MASK) >> 23))) & MASK
    x[5] ^= x[4]
    x[6] = (x[6] + x[5]) & MASK
    x[7] = (x[7] - (x[6] ^ 0x0123456789ABCDEF)) & MASK


def compress_with(t: list[int], state: tuple[int, int, int], words: list[int]) -> tuple[int, int, int]:
    """The Tiger compression function with the 1024-word table t = t1 || t2 || t3 || t4."""
    r = list(state)  # registers a, b, c
    x = list(words)
    for p, mul in enumerate((5, 7, 9)):  # @line L6
        if p:
            key_schedule(x)  # @line L7
        order = ((0, 1, 2), (2, 0, 1), (1, 2, 0))[p]  # pass(a,b,c), pass(c,a,b), pass(b,c,a)
        for i in range(8):  # @line L8
            ia, ib, ic = (order[i % 3], order[(i + 1) % 3], order[(i + 2) % 3])
            c = r[ic] ^ x[i]  # @line L9
            r[ic] = c
            r[ia] = (r[ia] - (t[c & 255] ^ t[256 + ((c >> 16) & 255)] ^ t[512 + ((c >> 32) & 255)]
                              ^ t[768 + ((c >> 48) & 255)])) & MASK  # @line L10
            r[ib] = (r[ib] + (t[768 + ((c >> 8) & 255)] ^ t[512 + ((c >> 24) & 255)]
                              ^ t[256 + ((c >> 40) & 255)] ^ t[(c >> 56) & 255])) & MASK  # @line L11
            r[ib] = (r[ib] * mul) & MASK  # @line L12
    a, b, c = r
    return a ^ state[0], (b - state[1]) & MASK, (c + state[2]) & MASK  # @line L13


def generate_sboxes() -> list[int]:
    """The procedure of gen-sboxes.c: 5 passes of byte swaps driven by compressions of GEN_STRING."""
    t = [(i & 255) * 0x0101010101010101 for i in range(1024)]
    words = [int.from_bytes(GEN_STRING[8 * i:8 * i + 8], "little") for i in range(8)]
    state = IV
    abc = 2
    for _ in range(5):
        for i in range(256):
            for sb in (0, 256, 512, 768):
                abc += 1
                if abc == 3:
                    abc = 0
                    state = compress_with(t, state, words)
                s = state[abc]
                for col in range(8):
                    sh = 8 * col
                    j = sb + ((s >> sh) & 255)
                    u, v = t[sb + i], t[j]
                    diff = ((u >> sh) ^ (v >> sh)) & 255
                    t[sb + i] = u ^ (diff << sh)
                    t[j] = v ^ (diff << sh)  # when j == sb + i, diff is 0 and nothing changes
    return t


TABLE = generate_sboxes()


def compress(state: tuple[int, int, int], block: bytes) -> tuple[int, int, int]:
    words = [int.from_bytes(block[8 * i:8 * i + 8], "little") for i in range(8)]  # @line L5
    return compress_with(TABLE, state, words)


def pad(msg: bytes, first: int) -> bytes:
    """The pad byte (0x01 for Tiger, 0x80 for Tiger2), zeros to 56 mod 64, then the bit length, little-endian."""
    n = len(msg)
    return msg + bytes([first]) + b"\x00" * ((55 - n) % 64) + (8 * n).to_bytes(8, "little")


def _hash(msg: bytes, first: int) -> bytes:
    data = pad(msg, first)  # @line L1
    state = IV  # @line L2
    for i in range(0, len(data), 64):  # @line L3
        state = compress(state, data[i:i + 64])  # @line L4
    return b"".join(w.to_bytes(8, "little") for w in state)  # @line L14


def tiger(msg: bytes) -> bytes:
    """The 24-byte Tiger digest, as bytes: each of the three words in little-endian order."""
    return _hash(msg, 0x01)


def tiger2(msg: bytes) -> bytes:
    """Tiger2: the same function with the MD4-style padding byte 0x80."""
    return _hash(msg, 0x80)
