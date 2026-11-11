# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snow-3g/. The authors are listed in prov/YDPQ53.jsonl.

"""The SNOW 3G keystream generator of ETSI/SAGE (UEA2 & UIA2, Document 2), for study only.

This code is not constant time as Python runs it (it uses table lookups) and
must not protect real data. Use a vetted, validated implementation instead.

Words are 32-bit integers. Key word k0 is the first 4 key bytes read big-endian,
and IV0 is the first 4 IV bytes, as in the ETSI/SAGE test data (Document 3).
"""

M32 = 0xFFFFFFFF


def mulx(v: int, c: int) -> int:
    """MULx(V, c) of Section 3.1.1: multiply V by x in GF(2^8) with reduction byte c."""
    return ((v << 1) & 0xFF) ^ c if v & 0x80 else v << 1


def mulxpow(v: int, i: int, c: int) -> int:
    """MULxPOW(V, i, c) of Section 3.1.2: MULx applied i times."""
    for _ in range(i):
        v = mulx(v, c)
    return v


def _gf_mul(a: int, b: int, poly: int) -> int:
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        if a & 0x100:
            a ^= poly
        b >>= 1
    return r


def _gf_pow(a: int, e: int, poly: int) -> int:
    r = 1
    while e:
        if e & 1:
            r = _gf_mul(r, a, poly)
        a = _gf_mul(a, a, poly)
        e >>= 1
    return r


def _make_sr() -> list[int]:
    """The Rijndael S-box: inverse in GF(2^8) mod x^8+x^4+x^3+x+1, then the affine map."""
    out = []
    for x in range(256):
        y = _gf_pow(x, 254, 0x11B)  # x^254 is the inverse, and 0 maps to 0
        s = y
        for k in range(1, 5):
            s ^= ((y << k) | (y >> (8 - k))) & 0xFF
        out.append(s ^ 0x63)
    return out


def _make_sq() -> list[int]:
    """SQ(x) = g49(x) + 0x25 in GF(2^8) mod x^8+x^6+x^5+x^3+1 (Annex 1.3), g49 a Dickson polynomial."""
    out = []
    for x in range(256):
        y = 0
        for e in (1, 9, 13, 15, 33, 41, 45, 47, 49):
            y ^= _gf_pow(x, e, 0x169)
        out.append(y ^ 0x25)
    return out


SR = _make_sr()
SQ = _make_sq()
MUL_ALPHA = [
    (mulxpow(c, 23, 0xA9) << 24) | (mulxpow(c, 245, 0xA9) << 16) | (mulxpow(c, 48, 0xA9) << 8) | mulxpow(c, 239, 0xA9)
    for c in range(256)
]
DIV_ALPHA = [
    (mulxpow(c, 16, 0xA9) << 24) | (mulxpow(c, 39, 0xA9) << 16) | (mulxpow(c, 6, 0xA9) << 8) | mulxpow(c, 64, 0xA9)
    for c in range(256)
]


def _mix(w: int, box: list[int], c: int) -> int:
    """S1 (box SR, c = 0x1B) or S2 (box SQ, c = 0x69) of Section 3.3: S-box per byte, then a MixColumn."""
    a0, a1, a2, a3 = (box[(w >> sh) & 0xFF] for sh in (24, 16, 8, 0))
    r0 = mulx(a0, c) ^ a1 ^ a2 ^ mulx(a3, c) ^ a3
    r1 = mulx(a0, c) ^ a0 ^ mulx(a1, c) ^ a2 ^ a3
    r2 = a0 ^ mulx(a1, c) ^ a1 ^ mulx(a2, c) ^ a3
    r3 = a0 ^ a1 ^ mulx(a2, c) ^ a2 ^ mulx(a3, c)
    return (r0 << 24) | (r1 << 16) | (r2 << 8) | r3


def s1(w: int) -> int:
    return _mix(w, SR, 0x1B)


def s2(w: int) -> int:
    return _mix(w, SQ, 0x69)


def _fsm(s: list[int], r: list[int]) -> int:
    """Clock the FSM (Section 3.4.6) and return its output word F."""
    f = ((s[15] + r[0]) & M32) ^ r[1]  # @line L11
    t = (r[1] + (r[2] ^ s[5])) & M32  # @line L12
    r[0], r[1], r[2] = t, s1(r[0]), s2(r[1])  # @line L13
    return f


def _lfsr(s: list[int], f: int) -> None:
    """Clock the LFSR (Sections 3.4.4 and 3.4.5); f = 0 is the keystream mode."""
    v = ((s[0] << 8) & M32) ^ MUL_ALPHA[s[0] >> 24] ^ s[2] ^ (s[11] >> 8) ^ DIV_ALPHA[s[11] & 0xFF] ^ f  # @line L14
    s[:] = s[1:] + [v]  # @line L15


def snow3g_keystream(key: bytes, iv: bytes, n: int) -> list[int]:
    """Return the keystream words z_1 .. z_n.

    Precondition: 16-byte key and 16-byte IV. Cost: Theta(33 + n) clocks of a
    16-word LFSR and a 3-word FSM, each a constant number of word operations.
    """
    if len(key) != 16 or len(iv) != 16:
        raise ValueError("SNOW 3G needs a 128-bit key and a 128-bit IV")
    k0, k1, k2, k3 = (int.from_bytes(key[4 * i : 4 * i + 4], "big") for i in range(4))
    v0, v1, v2, v3 = (int.from_bytes(iv[4 * i : 4 * i + 4], "big") for i in range(4))
    one = M32
    s = [  # @line L1
        k0 ^ one, k1 ^ one, k2 ^ one, k3 ^ one,
        k0, k1, k2, k3,
        k0 ^ one, k1 ^ one ^ v3, k2 ^ one ^ v2, k3 ^ one,
        k0 ^ v1, k1, k2, k3 ^ v0,
    ]
    r = [0, 0, 0]  # @line L1
    for _ in range(32):  # @line L2
        f = _fsm(s, r)  # @line L3
        _lfsr(s, f)  # @line L4
    _fsm(s, r)  # @line L5
    _lfsr(s, 0)  # @line L6
    out = []
    for _ in range(n):  # @line L7
        f = _fsm(s, r)  # @line L8
        out.append(f ^ s[0])  # @line L9
        _lfsr(s, 0)  # @line L10
    return out
