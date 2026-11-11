# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gcm-mode/. The authors are listed in prov/74AABT.jsonl.
"""AES (FIPS 197) for 128, 192 and 256 bit keys, as the block cipher of the mode pages.

For study only. This code is not constant time (it uses table lookups that
depend on secret bytes) and must not protect real data. Use a FIPS 140
validated module or the cryptography library of your platform instead.
"""


def _xtime(a: int) -> int:
    a <<= 1
    return a ^ 0x11B if a & 0x100 else a


def _gmul(a: int, b: int) -> int:
    """Multiply two bytes in GF(2^8) modulo x^8 + x^4 + x^3 + x + 1."""
    r = 0
    while b:
        if b & 1:
            r ^= a
        a = _xtime(a)
        b >>= 1
    return r


def _make_sbox() -> tuple[list[int], list[int]]:
    """The S-box of FIPS 197 Section 5.1.1: the inverse in GF(2^8), then the affine map."""
    sbox, inv = [0] * 256, [0] * 256
    for x in range(256):
        y = 1
        for _ in range(254):  # x^254 is the inverse of x, and 0 maps to 0
            y = _gmul(y, x)
        y = y if x else 0
        s = y
        for k in range(1, 5):
            s ^= ((y << k) | (y >> (8 - k))) & 0xFF
        s ^= 0x63
        sbox[x] = s
        inv[s] = x
    return sbox, inv


SBOX, INV_SBOX = _make_sbox()
_M2 = [_gmul(x, 2) for x in range(256)]
_M3 = [_gmul(x, 3) for x in range(256)]
_M9 = [_gmul(x, 9) for x in range(256)]
_M11 = [_gmul(x, 11) for x in range(256)]
_M13 = [_gmul(x, 13) for x in range(256)]
_M14 = [_gmul(x, 14) for x in range(256)]
# ShiftRows on a column-major state: byte i is row i % 4, column i // 4.
_SHIFT = [(i + 4 * (i % 4)) % 16 for i in range(16)]
_INV_SHIFT = [_SHIFT.index(i) for i in range(16)]


class AES:
    """One AES key. encrypt_block and decrypt_block map 16 bytes to 16 bytes."""

    block_size = 16

    def __init__(self, key: bytes) -> None:
        if len(key) not in (16, 24, 32):
            raise ValueError("an AES key has 16, 24 or 32 bytes")
        nk = len(key) // 4
        self.rounds = nk + 6
        w = [list(key[4 * i : 4 * i + 4]) for i in range(nk)]
        rcon = 1
        for i in range(nk, 4 * (self.rounds + 1)):  # key expansion, FIPS 197 Section 5.2
            t = list(w[i - 1])
            if i % nk == 0:
                t = [SBOX[b] for b in t[1:] + t[:1]]
                t[0] ^= rcon
                rcon = _xtime(rcon)
            elif nk > 6 and i % nk == 4:
                t = [SBOX[b] for b in t]
            w.append([a ^ b for a, b in zip(w[i - nk], t)])
        self.round_keys = [sum(w[4 * r : 4 * r + 4], []) for r in range(self.rounds + 1)]

    def encrypt_block(self, block: bytes) -> bytes:
        if len(block) != 16:
            raise ValueError("an AES block has 16 bytes")
        s = [b ^ k for b, k in zip(block, self.round_keys[0])]
        for r in range(1, self.rounds + 1):
            s = [SBOX[s[_SHIFT[i]]] for i in range(16)]  # SubBytes and ShiftRows
            if r != self.rounds:  # MixColumns
                m = []
                for c in range(0, 16, 4):
                    a0, a1, a2, a3 = s[c : c + 4]
                    m += [
                        _M2[a0] ^ _M3[a1] ^ a2 ^ a3,
                        a0 ^ _M2[a1] ^ _M3[a2] ^ a3,
                        a0 ^ a1 ^ _M2[a2] ^ _M3[a3],
                        _M3[a0] ^ a1 ^ a2 ^ _M2[a3],
                    ]
                s = m
            s = [b ^ k for b, k in zip(s, self.round_keys[r])]
        return bytes(s)

    def decrypt_block(self, block: bytes) -> bytes:
        if len(block) != 16:
            raise ValueError("an AES block has 16 bytes")
        s = [b ^ k for b, k in zip(block, self.round_keys[self.rounds])]
        for r in range(self.rounds - 1, -1, -1):
            s = [INV_SBOX[s[_INV_SHIFT[i]]] for i in range(16)]
            s = [b ^ k for b, k in zip(s, self.round_keys[r])]
            if r != 0:  # InvMixColumns
                m = []
                for c in range(0, 16, 4):
                    a0, a1, a2, a3 = s[c : c + 4]
                    m += [
                        _M14[a0] ^ _M11[a1] ^ _M13[a2] ^ _M9[a3],
                        _M9[a0] ^ _M14[a1] ^ _M11[a2] ^ _M13[a3],
                        _M13[a0] ^ _M9[a1] ^ _M14[a2] ^ _M11[a3],
                        _M11[a0] ^ _M13[a1] ^ _M9[a2] ^ _M14[a3],
                    ]
                s = m
        return bytes(s)
