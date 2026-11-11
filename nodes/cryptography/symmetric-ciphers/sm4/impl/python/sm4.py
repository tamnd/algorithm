# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sm4/. The authors are listed in prov/9DN8TB.jsonl.
"""SM4 (GB/T 32907-2016), as described in draft-ribose-cfrg-sm4-10.

For study only. This code is not constant time: the S-box is a table indexed
by secret bytes, and Python itself leaks timing. Do not use it to protect real
data. Use a validated library, for example OpenSSL or GmSSL, instead.

A block and a key are 16 bytes, read as four big-endian 32-bit words. Cost:
32 rounds, each with 4 S-box lookups, 4 rotations and some XORs, and a key
schedule of 32 rounds of the same shape.
"""

MASK32 = 0xFFFFFFFF

# draft-ribose-cfrg-sm4-10, Section 6.2.3, Figure 1 (the S-box of GB/T 32907-2016).
SBOX = list(bytes.fromhex("""
    D6 90 E9 FE CC E1 3D B7 16 B6 14 C2 28 FB 2C 05
    2B 67 9A 76 2A BE 04 C3 AA 44 13 26 49 86 06 99
    9C 42 50 F4 91 EF 98 7A 33 54 0B 43 ED CF AC 62
    E4 B3 1C A9 C9 08 E8 95 80 DF 94 FA 75 8F 3F A6
    47 07 A7 FC F3 73 17 BA 83 59 3C 19 E6 85 4F A8
    68 6B 81 B2 71 64 DA 8B F8 EB 0F 4B 70 56 9D 35
    1E 24 0E 5E 63 58 D1 A2 25 22 7C 3B 01 21 78 87
    D4 00 46 57 9F D3 27 52 4C 36 02 E7 A0 C4 C8 9E
    EA BF 8A D2 40 C7 38 B5 A3 F7 F2 CE F9 61 15 A1
    E0 AE 5D A4 9B 34 1A 55 AD 93 32 30 F5 8C B1 E3
    1D F6 E2 2E 82 66 CA 60 C0 29 23 AB 0D 53 4E 6F
    D5 DB 37 45 DE FD 8E 2F 03 FF 6A 72 6D 6C 5B 51
    8D 1B AF 92 BB DD BC 7F 11 D9 5C 41 1F 10 5A D8
    0A C1 31 88 A5 CD 7B BD 2D 74 D0 12 B8 E5 B4 B0
    89 69 97 4A 0C 96 77 7E 65 B9 F1 09 C5 6E C6 84
    18 F0 7D EC 3A DC 4D 20 79 EE 5F 3E D7 CB 39 48
"""))

# Section 7.3.1, the family key FK.
FK = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]


def ck(i: int) -> int:
    """CK_i: its byte j is (4i + j) * 7 mod 256 (Section 7.3.2)."""
    v = 0
    for j in range(4):
        v = (v << 8) | ((4 * i + j) * 7 % 256)
    return v


CK = [ck(i) for i in range(32)]


def rotl(x: int, s: int) -> int:
    return ((x << s) | (x >> (32 - s))) & MASK32


def tau(a: int) -> int:
    return (SBOX[a >> 24] << 24) | (SBOX[(a >> 16) & 0xFF] << 16) | (SBOX[(a >> 8) & 0xFF] << 8) | SBOX[a & 0xFF]


def t(x: int) -> int:
    """T = L(tau(.)), with L(B) = B ^ (B <<< 2) ^ (B <<< 10) ^ (B <<< 18) ^ (B <<< 24)."""
    b = tau(x)  # @line L4
    return b ^ rotl(b, 2) ^ rotl(b, 10) ^ rotl(b, 18) ^ rotl(b, 24)  # @line L5


def t_prime(x: int) -> int:
    """T' = L'(tau(.)), with L'(B) = B ^ (B <<< 13) ^ (B <<< 23)."""
    b = tau(x)
    return b ^ rotl(b, 13) ^ rotl(b, 23)


def _words(b: bytes) -> list[int]:
    return [int.from_bytes(b[4 * i:4 * i + 4], "big") for i in range(4)]


def round_keys(key: bytes) -> list[int]:
    """Return rk_0, ..., rk_31 (Section 7.3)."""
    if len(key) != 16:
        raise ValueError("the key must have 16 bytes")
    k = [m ^ f for m, f in zip(_words(key), FK)]  # @line L6
    for i in range(32):  # @line L7
        k.append(k[i] ^ t_prime(k[i + 1] ^ k[i + 2] ^ k[i + 3] ^ CK[i]))  # @line L8
    return k[4:]  # @line L9


def _crypt(block: bytes, rk: list[int]) -> bytes:
    if len(block) != 16:
        raise ValueError("the block must have 16 bytes")
    x = _words(block)
    for i in range(32):  # @line L1
        x.append(x[i] ^ t(x[i + 1] ^ x[i + 2] ^ x[i + 3] ^ rk[i]))  # @line L2
    return b"".join(w.to_bytes(4, "big") for w in (x[35], x[34], x[33], x[32]))  # @line L3


def encrypt_block(key: bytes, block: bytes) -> bytes:
    return _crypt(block, round_keys(key))


def decrypt_block(key: bytes, block: bytes) -> bytes:
    """Decryption is the same process with the round keys in reverse order."""
    return _crypt(block, round_keys(key)[::-1])
