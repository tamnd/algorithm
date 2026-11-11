# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skein/. The authors are listed in prov/WAM1AS.jsonl.
"""Skein-256, Skein-512 and Skein-1024 (Skein 1.3, 1 October 2010), for study only.

The code follows Section 3 of the specification: Threefish (3.3), UBI (3.4) and
simple and keyed Skein (3.5.4, 3.5.5). It hashes whole bytes only (no BitPad) and
does not implement the optional tree mode (3.5.6). It is not constant time.
"""

M64 = (1 << 64) - 1
C240 = 0x1BD11BDAA9FC1A22

# Table 2 (rounds), Table 3 (word permutation) and Table 4 (rotation constants R[d mod 8][j]).
ROUNDS = {4: 72, 8: 72, 16: 80}
PERM = {
    4: (0, 3, 2, 1),
    8: (2, 1, 4, 7, 6, 5, 0, 3),
    16: (0, 9, 2, 13, 6, 11, 4, 15, 10, 7, 12, 3, 14, 5, 8, 1),
}
ROT = {
    4: ((14, 16), (52, 57), (23, 40), (5, 37), (25, 33), (46, 12), (58, 22), (32, 32)),
    8: (
        (46, 36, 19, 37), (33, 27, 14, 42), (17, 49, 36, 39), (44, 9, 54, 56),
        (39, 30, 34, 24), (13, 50, 10, 17), (25, 29, 39, 43), (8, 35, 56, 22),
    ),
    16: (
        (24, 13, 8, 47, 8, 17, 22, 37), (38, 19, 10, 55, 49, 18, 23, 52),
        (33, 4, 51, 13, 34, 41, 59, 17), (5, 20, 48, 41, 47, 28, 16, 25),
        (41, 9, 37, 31, 12, 47, 44, 30), (16, 34, 56, 51, 4, 53, 42, 41),
        (31, 44, 47, 46, 19, 42, 44, 25), (9, 48, 35, 52, 23, 31, 37, 20),
    ),
}

# Table 6: type values.
T_KEY, T_CFG, T_PRS, T_PK, T_KDF, T_NON, T_MSG, T_OUT = 0, 4, 8, 12, 16, 20, 48, 63


def _words(b: bytes) -> list[int]:
    return [int.from_bytes(b[i:i + 8], "little") for i in range(0, len(b), 8)]


def _bytes(w: list[int]) -> bytes:
    return b"".join(x.to_bytes(8, "little") for x in w)


def threefish_encrypt(key: bytes, tweak: bytes, block: bytes) -> bytes:
    """Threefish encryption E(K, T, P), Section 3.3."""
    nw = len(key) // 8
    k = _words(key)
    t = _words(tweak)
    k.append(C240 ^ _xor_all(k))  # @line L8
    t.append(t[0] ^ t[1])
    nr, perm, rot = ROUNDS[nw], PERM[nw], ROT[nw]

    def subkey(s: int) -> list[int]:
        ks = [k[(s + i) % (nw + 1)] for i in range(nw)]
        ks[nw - 3] = (ks[nw - 3] + t[s % 3]) & M64
        ks[nw - 2] = (ks[nw - 2] + t[(s + 1) % 3]) & M64
        ks[nw - 1] = (ks[nw - 1] + s) & M64
        return ks

    v = _words(block)
    for d in range(nr):  # @line L9
        if d % 4 == 0:
            v = [(x + y) & M64 for x, y in zip(v, subkey(d // 4))]
        f = [0] * nw
        for j in range(nw // 2):
            x0, x1 = v[2 * j], v[2 * j + 1]
            r = rot[d % 8][j]
            y0 = (x0 + x1) & M64
            f[2 * j] = y0
            f[2 * j + 1] = (((x1 << r) | (x1 >> (64 - r))) & M64) ^ y0
        v = [f[perm[i]] for i in range(nw)]
    return _bytes([(x + y) & M64 for x, y in zip(v, subkey(nr // 4))])  # @line L10


def _xor_all(ws: list[int]) -> int:
    acc = 0
    for w in ws:
        acc ^= w
    return acc


def ubi(g: bytes, msg: bytes, ts: int) -> bytes:
    """UBI(G, M, Ts) of Section 3.4, for a message of whole bytes."""
    nb = len(g)
    nm = len(msg)
    pad = nb if nm == 0 else (-nm) % nb  # @line L5
    m = msg + bytes(pad)
    h = g
    blocks = len(m) // nb
    for i in range(blocks):
        mi = m[i * nb:(i + 1) * nb]
        tw = ts + min(nm, (i + 1) * nb)  # @line L6
        if i == 0:
            tw += 1 << 126
        if i == blocks - 1:
            tw += 1 << 127
        e = threefish_encrypt(h, tw.to_bytes(16, "little"), mi)
        h = bytes(a ^ b for a, b in zip(e, mi))  # @line L7
    return h


def config(no: int, yl: int = 0, yf: int = 0, ym: int = 0) -> bytes:
    """The 32-byte configuration string C of Table 7."""
    return b"SHA3" + (1).to_bytes(2, "little") + bytes(2) + no.to_bytes(8, "little") + bytes([yl, yf, ym]) + bytes(13)


def output(g: bytes, no: int) -> bytes:
    """Output(G, No) of Section 3.5.3: counter mode of UBI with type Tout."""
    out = b""
    i = 0
    need = (no + 7) // 8
    while len(out) < need:
        out += ubi(g, i.to_bytes(8, "little"), T_OUT << 120)
        i += 1
    return out[:need]


def skein(nb: int, no: int, msg: bytes, key: bytes = b"", extra: tuple[tuple[int, bytes], ...] = ()) -> bytes:
    """Skein with state size nb bytes (32, 64 or 128) and output size no bits (a multiple of 8).

    extra is the list L of Section 3.5.5 without the message, as pairs (type, string),
    for example ((T_PRS, b"app"),) for a personalization string.
    """
    if nb not in (32, 64, 128):
        raise ValueError("the state size must be 32, 64 or 128 bytes")
    if no <= 0 or no % 8:
        raise ValueError("this code supports output sizes that are a multiple of 8 bits")
    k0 = bytes(nb) if not key else ubi(bytes(nb), key, T_KEY << 120)  # @line L1
    g = ubi(k0, config(no), T_CFG << 120)  # @line L2
    for t, s in sorted(list(extra) + [(T_MSG, msg)]):
        g = ubi(g, s, t << 120)  # @line L3
    return output(g, no)  # @line L4


def skein256(msg: bytes, no: int = 256, key: bytes = b"") -> bytes:
    return skein(32, no, msg, key)


def skein512(msg: bytes, no: int = 512, key: bytes = b"") -> bytes:
    return skein(64, no, msg, key)


def skein1024(msg: bytes, no: int = 1024, key: bytes = b"") -> bytes:
    return skein(128, no, msg, key)


def initial_chaining_value(nb: int, no: int) -> list[int]:
    """G0 for simple hashing, which Appendix B lists as precomputed words."""
    return _words(ubi(bytes(nb), config(no), T_CFG << 120))
