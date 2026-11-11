# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/argon2/. The authors are listed in prov/3Y7XXB.jsonl.
"""Argon2d, Argon2i and Argon2id, version 0x13, as in RFC 9106.

The module is self-contained: it has its own BLAKE2b (RFC 7693, unkeyed),
the variable-length hash H', the compression function G with the
multiply-add permutation P, the data-dependent and data-independent indexing,
and the main loop over passes, slices and lanes.

For study only. The code is not constant time and must not protect real data.
It is also far too slow for real parameters: 64 MiB would take many minutes.
Use the argon2-cffi package, libsodium (crypto_pwhash) or the reference C
implementation (phc-winner-argon2) instead.
"""

import struct

M64 = (1 << 64) - 1
M32 = (1 << 32) - 1
ARGON2D, ARGON2I, ARGON2ID = 0, 1, 2
SYNC_POINTS = 4  # slices per pass

# ---------------------------------------------------------------- BLAKE2b (RFC 7693)

_IV = [
    0x6A09E667F3BCC908, 0xBB67AE8584CAA73B, 0x3C6EF372FE94F82B, 0xA54FF53A5F1D36F1,
    0x510E527FADE682D1, 0x9B05688C2B3E6C1F, 0x1F83D9ABFB41BD6B, 0x5BE0CD19137E2179,
]
_SIGMA = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
    [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
    [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
    [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
    [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
    [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
    [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
    [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
    [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0],
]
_LANES = [(0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
          (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14)]


def _rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (64 - n))) & M64


def _blake2b_compress(h: list[int], block: bytes, t: int, last: bool) -> None:
    m = struct.unpack("<16Q", block)
    v = h + _IV
    v[12] ^= t & M64
    v[13] ^= t >> 64
    if last:
        v[14] ^= M64
    for i in range(12):
        s = _SIGMA[i % 10]
        for k, (a, b, c, d) in enumerate(_LANES):
            x, y = m[s[2 * k]], m[s[2 * k + 1]]
            v[a] = (v[a] + v[b] + x) & M64
            v[d] = _rotr(v[d] ^ v[a], 32)
            v[c] = (v[c] + v[d]) & M64
            v[b] = _rotr(v[b] ^ v[c], 24)
            v[a] = (v[a] + v[b] + y) & M64
            v[d] = _rotr(v[d] ^ v[a], 16)
            v[c] = (v[c] + v[d]) & M64
            v[b] = _rotr(v[b] ^ v[c], 63)
    for i in range(8):
        h[i] ^= v[i] ^ v[i + 8]


def blake2b(data: bytes, nn: int = 64) -> bytes:
    """Unkeyed BLAKE2b with an nn-byte digest, as in RFC 7693, Section 3.3."""
    h = list(_IV)
    h[0] ^= 0x01010000 ^ nn
    n = len(data)
    blocks = max(1, (n + 127) // 128)
    for i in range(blocks - 1):
        _blake2b_compress(h, data[128 * i : 128 * i + 128], 128 * (i + 1), False)
    last = data[128 * (blocks - 1) :]
    _blake2b_compress(h, last.ljust(128, b"\x00"), n, True)
    return struct.pack("<8Q", *h)[:nn]


# ---------------------------------------------------------------- H' and G


def _le32(x: int) -> bytes:
    return struct.pack("<I", x)


def h_prime(data: bytes, t: int) -> bytes:
    """The variable-length hash H'^T of RFC 9106, Section 3.3."""
    if t <= 64:
        return blake2b(_le32(t) + data, t)  # @line L7
    r = (t + 31) // 32 - 2
    v = blake2b(_le32(t) + data, 64)  # @line L7
    out = v[:32]
    for _ in range(r - 1):
        v = blake2b(v, 64)  # @line L7
        out += v[:32]
    return out + blake2b(v, t - 32 * r)  # @line L7


def _gb(v: list[int], a: int, b: int, c: int, d: int) -> None:
    """GB of RFC 9106, Section 3.6: the BLAKE2b G with a 32x32-bit product added."""
    va, vb, vc, vd = v[a], v[b], v[c], v[d]
    va = (va + vb + 2 * (va & M32) * (vb & M32)) & M64
    vd = _rotr(vd ^ va, 32)
    vc = (vc + vd + 2 * (vc & M32) * (vd & M32)) & M64
    vb = _rotr(vb ^ vc, 24)
    va = (va + vb + 2 * (va & M32) * (vb & M32)) & M64
    vd = _rotr(vd ^ va, 16)
    vc = (vc + vd + 2 * (vc & M32) * (vd & M32)) & M64
    vb = _rotr(vb ^ vc, 63)
    v[a], v[b], v[c], v[d] = va, vb, vc, vd


def _permute(q: list[int], idx: list[int]) -> None:
    """Apply P to the 16 words q[idx[0]], ..., q[idx[15]] in place."""
    v = [q[k] for k in idx]
    for a, b, c, d in _LANES:
        _gb(v, a, b, c, d)
    for k, w in zip(idx, v):
        q[k] = w


_ROW_IDX = [list(range(16 * i, 16 * i + 16)) for i in range(8)]
_COL_IDX = [[2 * j + 16 * k + e for k in range(8) for e in (0, 1)] for j in range(8)]


def compress(x: list[int], y: list[int]) -> list[int]:
    """G(X, Y) of RFC 9106, Section 3.5, on blocks of 128 words of 64 bits."""
    r = [a ^ b for a, b in zip(x, y)]  # @line L8
    q = list(r)
    for idx in _ROW_IDX:
        _permute(q, idx)  # @line L8
    for idx in _COL_IDX:
        _permute(q, idx)  # @line L8
    return [a ^ b for a, b in zip(q, r)]  # @line L8


def _to_words(b: bytes) -> list[int]:
    return list(struct.unpack("<128Q", b))


def _to_bytes(w: list[int]) -> bytes:
    return struct.pack("<128Q", *w)


# ---------------------------------------------------------------- Argon2


def pre_hash(password: bytes, salt: bytes, t: int, m: int, p: int, tag_len: int, y: int,
             secret: bytes = b"", ad: bytes = b"", version: int = 0x13) -> bytes:
    """H_0 of RFC 9106, Section 3.2, step 1."""
    data = b"".join(_le32(v) for v in (p, tag_len, m, t, version, y))
    for field in (password, salt, secret, ad):
        data += _le32(len(field)) + field
    return blake2b(data, 64)  # @line L1


def argon2(password: bytes, salt: bytes, t: int, m: int, p: int, tag_len: int, y: int = ARGON2ID,
           secret: bytes = b"", ad: bytes = b"", trace: list | None = None) -> bytes:
    """Argon2 version 0x13 with t passes, m KiB of memory, p lanes and type y."""
    if not (p >= 1 and t >= 1 and tag_len >= 4 and m >= 8 * p and y in (0, 1, 2)):
        raise ValueError("bad Argon2 parameters")
    h0 = pre_hash(password, salt, t, m, p, tag_len, y, secret, ad)
    m2 = 4 * p * (m // (4 * p))  # m', the number of 1 KiB blocks
    q = m2 // p  # lane length
    seg = q // SYNC_POINTS  # segment length
    mem = [[[] for _ in range(q)] for _ in range(p)]
    for i in range(p):
        mem[i][0] = _to_words(h_prime(h0 + _le32(0) + _le32(i), 1024))  # @line L2
        mem[i][1] = _to_words(h_prime(h0 + _le32(1) + _le32(i), 1024))  # @line L2
    zero = [0] * 128
    for r in range(t):
        for s in range(SYNC_POINTS):
            for lane in range(p):
                indep = y == ARGON2I or (y == ARGON2ID and r == 0 and s < SYNC_POINTS // 2)
                start = 2 if r == 0 and s == 0 else 0
                addr: list[int] = []
                inp = [r, lane, s, m2, t, y, 0] + [0] * 121
                if indep and start == 2:
                    inp[6] += 1
                    addr = compress(zero, compress(zero, inp))
                for idx in range(start, seg):
                    j = s * seg + idx
                    prev = mem[lane][j - 1] if j > 0 else mem[lane][q - 1]
                    if indep:  # J_1, J_2 from the address blocks (data independent)
                        if idx % 128 == 0:
                            inp[6] += 1
                            addr = compress(zero, compress(zero, inp))  # @line L3
                        rand = addr[idx % 128]  # @line L3
                    else:  # J_1, J_2 from the previous block (data dependent)
                        rand = prev[0]  # @line L3
                    j1, j2 = rand & M32, rand >> 32
                    ref_lane = lane if (r == 0 and s == 0) else j2 % p  # @line L4
                    same = ref_lane == lane
                    if r == 0:
                        if s == 0:
                            area = idx - 1
                        else:
                            area = s * seg + (idx - 1 if same else (-1 if idx == 0 else 0))
                    else:
                        area = q - seg + (idx - 1 if same else (-1 if idx == 0 else 0))
                    xx = (j1 * j1) >> 32
                    rel = area - 1 - ((area * xx) >> 32)  # @line L4
                    first = 0 if r == 0 or s == SYNC_POINTS - 1 else (s + 1) * seg
                    z = (first + rel) % q  # @line L4
                    new = compress(prev, mem[ref_lane][z])  # @line L5
                    if r > 0:
                        new = [a ^ b for a, b in zip(new, mem[lane][j])]  # @line L5
                    mem[lane][j] = new
        if trace is not None:
            trace.append((mem[0][0][:4], mem[p - 1][q - 1][-4:]))
    c = list(mem[0][q - 1])
    for i in range(1, p):
        c = [a ^ b for a, b in zip(c, mem[i][q - 1])]  # @line L6
    return h_prime(_to_bytes(c), tag_len)  # @line L6
