# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frodokem/. The authors are listed in prov/MD60D5.jsonl.
"""FrodoKEM-640-SHAKE as in the NIST round 3 specification (2021).

This is the KEM of the round 3 submission, which the current FrodoKEM
repository calls eFrodoKEM (the ephemeral variant). The standard FrodoKEM of
the ISO proposal adds a salt and a longer seed; it is described on the page
but not implemented here. The parameters are n = 640, nbar = 8, q = 2^15,
B = 2 extracted binary digits per entry, 16-byte seeds and keys, SHAKE128 for
the matrix A and for all other hashing, and the 13-entry CDF table of the
error distribution. SHAKE128 comes from hashlib: the page is about the KEM.

The randomness can be passed in, so that the known answer tests of the
submission can be reproduced with the NIST AES-CTR random generator.

For study only. This code is not constant time (it branches on secret data in
the sampler and the comparison), it is slow, and it must not be used to
protect real data. Use the reference code of the FrodoKEM team or liboqs.
"""

import hashlib
import secrets
import struct

N = 640
NBAR = 8
LOGQ = 15
Q = 1 << LOGQ
B = 2
LEN = 16  # bytes of s, seedSE, z, mu, k, pkh, ss and seedA
CDF = (4643, 13363, 20579, 25843, 29227, 31145, 32103, 32525, 32689, 32745, 32762, 32766, 32767)

PK_BYTES = LEN + N * NBAR * LOGQ // 8          # 9616
SK_BYTES = LEN + PK_BYTES + 2 * N * NBAR + LEN  # 19888
CT_BYTES = (N * NBAR + NBAR * NBAR) * LOGQ // 8  # 9720


def shake(data, n):
    return hashlib.shake_128(data).digest(n)


def gen_a(seed_a):
    """Frodo.Gen with SHAKE128: row i is SHAKE128(i as 2 bytes LE || seedA), 640 entries LE."""
    rows = []
    for i in range(N):
        raw = shake(struct.pack("<H", i) + seed_a, 2 * N)
        rows.append([x & (Q - 1) for x in struct.unpack("<%dH" % N, raw)])
    return rows


def sample(r):
    """Frodo.Sample: inversion sampling from the CDF table, the low binary digit is the sign."""
    t = 0
    p = r >> 1
    for z in range(len(CDF) - 1):
        if p > CDF[z]:
            t += 1
    return -t if r & 1 else t


def sample_list(raw, count):
    return [sample(x) for x in struct.unpack("<%dH" % count, raw[:2 * count])]


def pack(values):
    """Frodo.Pack: each entry in LOGQ binary digits, most significant first."""
    acc = 0
    for v in values:
        acc = (acc << LOGQ) | (v & (Q - 1))
    return acc.to_bytes(len(values) * LOGQ // 8, "big")


def unpack(data, count):
    acc = int.from_bytes(data, "big")
    m = Q - 1
    return [(acc >> (LOGQ * (count - 1 - i))) & m for i in range(count)]


def encode(mu):
    """Frodo.Encode: B binary digits of mu (little-endian order) per entry, times q / 2^B."""
    v = int.from_bytes(mu, "little")
    return [((v >> (B * i)) & ((1 << B) - 1)) << (LOGQ - B) for i in range(NBAR * NBAR)]


def decode(m):
    """Frodo.Decode: round each entry to the nearest multiple of q / 2^B."""
    v = 0
    for i, x in enumerate(m):
        t = (((x & (Q - 1)) + (1 << (LOGQ - B - 1))) >> (LOGQ - B)) & ((1 << B) - 1)
        v |= t << (B * i)
    return v.to_bytes(NBAR * NBAR * B // 8, "little")


def mul_as_plus_e(a, st, e):
    """B = A S + E with S given as its transpose (nbar rows of length n)."""
    out = []
    for i, row in enumerate(a):
        for k in range(NBAR):
            out.append((sum(x * y for x, y in zip(row, st[k])) + e[i * NBAR + k]) & (Q - 1))
    return out


def mul_sa_plus_e(sp, a, ep):
    """B' = S' A + E' (nbar by n)."""
    out = []
    for k in range(NBAR):
        acc = [0] * N
        s = sp[k]
        for i, row in enumerate(a):
            c = s[i]
            if c:
                acc = [x + c * y for x, y in zip(acc, row)]
        out.extend((x + y) & (Q - 1) for x, y in zip(acc, ep[k * N:(k + 1) * N]))
    return out


def mul_sb_plus_e(sp, bmat, epp):
    """V = S' B + E'' (nbar by nbar); bmat is n by nbar, row major."""
    out = []
    for k in range(NBAR):
        for j in range(NBAR):
            acc = sum(sp[k][i] * bmat[i * NBAR + j] for i in range(N))
            out.append((acc + epp[k * NBAR + j]) & (Q - 1))
    return out


def keygen(randomness=None):
    """FrodoKEM.KeyGen. randomness = s || seedSE || z (48 bytes)."""
    if randomness is None:
        randomness = secrets.token_bytes(3 * LEN)
    # @line L1
    s, seed_se, z = randomness[:LEN], randomness[LEN:2 * LEN], randomness[2 * LEN:3 * LEN]
    # @line L2
    seed_a = shake(z, LEN)
    a = gen_a(seed_a)
    # @line L3
    raw = shake(b"\x5f" + seed_se, 4 * N * NBAR)
    st_flat = sample_list(raw, N * NBAR)
    e = sample_list(raw[2 * N * NBAR:], N * NBAR)
    st = [st_flat[k * N:(k + 1) * N] for k in range(NBAR)]
    # @line L4
    bmat = mul_as_plus_e(a, st, e)
    # @line L5
    pk = seed_a + pack(bmat)
    # @line L6
    st_bytes = struct.pack("<%dH" % (N * NBAR), *[x & 0xFFFF for x in st_flat])
    sk = s + pk + st_bytes + shake(pk, LEN)
    return pk, sk


def _encrypt(pk, a, mu, seed_se):
    # @line L9
    raw = shake(b"\x96" + seed_se, 2 * (2 * N + NBAR) * NBAR)
    sp_flat = sample_list(raw, N * NBAR)
    ep = sample_list(raw[2 * N * NBAR:], N * NBAR)
    epp = sample_list(raw[4 * N * NBAR:], NBAR * NBAR)
    sp = [sp_flat[k * N:(k + 1) * N] for k in range(NBAR)]
    # @line L10
    bp = mul_sa_plus_e(sp, a, ep)
    bmat = unpack(pk[LEN:], N * NBAR)
    v = mul_sb_plus_e(sp, bmat, epp)
    # @line L11
    c = [(x + y) & (Q - 1) for x, y in zip(v, encode(mu))]
    return bp, c


def encaps(pk, mu=None):
    """FrodoKEM.Encaps. Returns (ct, ss)."""
    if mu is None:
        # @line L7
        mu = secrets.token_bytes(LEN)
    # @line L8
    pkh = shake(pk, LEN)
    g2 = shake(pkh + mu, 2 * LEN)
    seed_se, k = g2[:LEN], g2[LEN:]
    bp, c = _encrypt(pk, gen_a(pk[:LEN]), mu, seed_se)
    # @line L12
    ct = pack(bp) + pack(c)
    # @line L13
    return ct, shake(ct + k, LEN)


def decaps(sk, ct):
    """FrodoKEM.Decaps with the re-encryption check and implicit rejection with s."""
    s = sk[:LEN]
    pk = sk[LEN:LEN + PK_BYTES]
    st_flat = list(struct.unpack("<%dh" % (N * NBAR), sk[LEN + PK_BYTES:LEN + PK_BYTES + 2 * N * NBAR]))
    pkh = sk[LEN + PK_BYTES + 2 * N * NBAR:]
    c1_len = N * NBAR * LOGQ // 8
    bp = unpack(ct[:c1_len], N * NBAR)
    c = unpack(ct[c1_len:], NBAR * NBAR)
    # M = C - B' S, where B' is nbar by n and S is n by nbar
    # @line L14
    m = []
    for i in range(NBAR):
        row = bp[i * N:(i + 1) * N]
        for j in range(NBAR):
            m.append((c[i * NBAR + j] - sum(x * y for x, y in zip(row, st_flat[j * N:(j + 1) * N]))) & (Q - 1))
    # @line L15
    mu2 = decode(m)
    # @line L16
    g2 = shake(pkh + mu2, 2 * LEN)
    seed_se2, k2 = g2[:LEN], g2[LEN:]
    # @line L17
    bp2, c2 = _encrypt(pk, gen_a(pk[:LEN]), mu2, seed_se2)
    # @line L18
    if bp2 == bp and c2 == c:
        return shake(ct + k2, LEN)
    # @line L19
    return shake(ct + s, LEN)
