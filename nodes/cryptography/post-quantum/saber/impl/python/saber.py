# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/saber/. The authors are listed in prov/0XW32T.jsonl.
"""Saber KEM (the middle parameter set) as in the NIST round 3 submission.

Parameters: n = 256, l = 3, q = 2^13, p = 2^10, T = 2^4, and a centered
binomial secret with mu = 8 (values in -4..4). The secret key layout,
the hashing and the bit packing follow the round 3 reference code
(github.com/KULeuven-COSIC/SABER, Reference_Implementation_KEM), so the
known answer tests of the submission can be reproduced when the random bytes
are passed in.

All moduli are powers of two, so there is no NTT. The reference code
multiplies with Toom-Cook 4-way and Karatsuba; this file uses Karatsuba
alone, which gives the same products.

For study only. This code is not constant time and must not be used to
protect real data.
"""

import hashlib
import secrets

N, L, MU = 256, 3, 8
EQ, EP, ET = 13, 10, 4
H1 = 1 << (EQ - EP - 1)                                            # 4
H2 = (1 << (EP - 2)) - (1 << (EP - ET - 1)) + (1 << (EQ - EP - 1))  # 228
POLYBYTES = EQ * N // 8              # 416
POLYVECBYTES = L * POLYBYTES         # 1248
POLYCOMPBYTES = EP * N // 8          # 320
POLYVECCOMPBYTES = L * POLYCOMPBYTES  # 960
SCALEBYTES = ET * N // 8             # 128
PK_BYTES = POLYVECCOMPBYTES + 32     # 992
SK_BYTES = POLYVECBYTES + PK_BYTES + 64  # 2304
CT_BYTES = POLYVECCOMPBYTES + SCALEBYTES  # 1088


def sha3_256(b):
    return hashlib.sha3_256(b).digest()


def sha3_512(b):
    return hashlib.sha3_512(b).digest()


def shake128(b, n):
    return hashlib.shake_128(b).digest(n)


# ---------------------------------------------------------------- packing
def pack_bits(values, bits):
    """Little-endian bit packing, as POLq2BS, POLp2BS and POLT2BS do."""
    acc, mask = 0, (1 << bits) - 1
    for i, v in enumerate(values):
        acc |= (v & mask) << (bits * i)
    return acc.to_bytes(len(values) * bits // 8, "little")


def unpack_bits(data, bits, count):
    acc, mask = int.from_bytes(data, "little"), (1 << bits) - 1
    return [(acc >> (bits * i)) & mask for i in range(count)]


def unpack_vec(data, bits):
    size = bits * N // 8
    return [unpack_bits(data[i * size:(i + 1) * size], bits, N) for i in range(L)]


# ---------------------------------------------------------------- arithmetic
def _karatsuba(a, b):
    n = len(a)
    if n <= 16:
        out = [0] * (2 * n - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    out[i + j] += x * y
        return out
    h = n // 2
    a0, a1, b0, b1 = a[:h], a[h:], b[:h], b[h:]
    lo = _karatsuba(a0, b0)
    hi = _karatsuba(a1, b1)
    mid = _karatsuba([x + y for x, y in zip(a0, a1)], [x + y for x, y in zip(b0, b1)])
    out = [0] * (2 * n - 1)
    for i in range(2 * h - 1):
        out[i] += lo[i]
        out[i + 2 * h] += hi[i]
        out[i + h] += mid[i] - lo[i] - hi[i]
    return out


def poly_mul(a, b):
    """Product in Z[x]/(x^256 + 1), exact integers (the caller reduces)."""
    c = _karatsuba(a, b)
    return [c[i] - (c[i + N] if i + N < len(c) else 0) for i in range(N)]


def gen_matrix(seed_a):
    buf = shake128(seed_a, L * POLYVECBYTES)
    return [unpack_vec(buf[i * POLYVECBYTES:(i + 1) * POLYVECBYTES], EQ) for i in range(L)]


def gen_secret(seed):
    """Centered binomial with mu = 8: each byte gives popcount(low 4) - popcount(high 4)."""
    buf = shake128(seed, L * MU * N // 8)
    return [[bin(x & 15).count("1") - bin(x >> 4).count("1") for x in buf[i * N:(i + 1) * N]] for i in range(L)]


def mat_vec(a, s, transpose):
    out = []
    for i in range(L):
        acc = [0] * N
        for j in range(L):
            prod = poly_mul(a[j][i] if transpose else a[i][j], s[j])
            acc = [x + y for x, y in zip(acc, prod)]
        out.append(acc)
    return out


def inner(b, s):
    acc = [0] * N
    for j in range(L):
        acc = [x + y for x, y in zip(acc, poly_mul(b[j], s[j]))]
    return acc


# ---------------------------------------------------------------- Saber.PKE
def pke_keygen(seed_a_raw, seed_s):
    # @line L1
    seed_a = shake128(seed_a_raw, 32)
    a = gen_matrix(seed_a)
    # @line L2
    s = gen_secret(seed_s)
    # @line L3
    b = [[((x + H1) >> (EQ - EP)) for x in row] for row in mat_vec(a, s, True)]
    # @line L4
    sk = b"".join(pack_bits(row, EQ) for row in s)
    pk = b"".join(pack_bits(row, EP) for row in b) + seed_a
    return pk, sk


def pke_enc(m, seed_sp, pk):
    # @line L5
    a = gen_matrix(pk[POLYVECCOMPBYTES:])
    sp = gen_secret(seed_sp)
    # @line L6
    bp = [[((x + H1) >> (EQ - EP)) for x in row] for row in mat_vec(a, sp, False)]
    # @line L7
    b = unpack_vec(pk[:POLYVECCOMPBYTES], EP)
    vp = inner(b, sp)
    # @line L8
    bits = [(m[i // 8] >> (i % 8)) & 1 for i in range(N)]
    cm = [(v - (mb << (EP - 1)) + H1) >> (EP - ET) for v, mb in zip(vp, bits)]
    # @line L9
    return b"".join(pack_bits(row, EP) for row in bp) + pack_bits(cm, ET)


def pke_dec(sk, ct):
    s = unpack_vec(sk[:POLYVECBYTES], EQ)
    s = [[x - (1 << EQ) if x >= 1 << (EQ - 1) else x for x in row] for row in s]
    b = unpack_vec(ct[:POLYVECCOMPBYTES], EP)
    # @line L10
    v = inner(b, s)
    cm = unpack_bits(ct[POLYVECCOMPBYTES:], ET, N)
    # @line L11
    bits = [((x + H2 - (c << (EP - ET))) >> (EP - 1)) & 1 for x, c in zip(v, cm)]
    # @line L12
    return bytes(sum(bits[8 * j + i] << i for i in range(8)) for j in range(N // 8))


# ---------------------------------------------------------------- Saber.KEM
def keygen(randomness=None):
    """randomness = seedA || seed_s || z (96 bytes), in the order the reference code draws them."""
    if randomness is None:
        randomness = secrets.token_bytes(96)
    # @line L13
    pk, sk_pke = pke_keygen(randomness[:32], randomness[32:64])
    sk = sk_pke + pk + sha3_256(pk) + randomness[64:96]
    return pk, sk


def encaps(pk, coins=None):
    if coins is None:
        coins = secrets.token_bytes(32)
    # @line L14
    m = sha3_256(coins)
    # @line L15
    kr = sha3_512(m + sha3_256(pk))
    # @line L16
    ct = pke_enc(m, kr[32:], pk)
    # @line L17
    return ct, sha3_256(kr[:32] + sha3_256(ct))


def decaps(sk, ct):
    pk = sk[POLYVECBYTES:POLYVECBYTES + PK_BYTES]
    # @line L18
    m = pke_dec(sk, ct)
    # @line L19
    kr = sha3_512(m + sk[SK_BYTES - 64:SK_BYTES - 32])
    # @line L20
    ok = pke_enc(m, kr[32:], pk) == ct
    # @line L21
    first = kr[:32] if ok else sk[SK_BYTES - 32:]
    return sha3_256(first + sha3_256(ct))
