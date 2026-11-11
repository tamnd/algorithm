# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newhope/. The authors are listed in prov/8ZNYFG.jsonl.

import hashlib
import random

from newhope import (
    CT_BYTES,
    GAMMA,
    N,
    PK_BYTES,
    Q,
    SK_BYTES,
    decaps,
    encaps,
    invntt,
    keygen,
    ntt,
    pke_dec,
    pke_enc,
    pointwise,
)

# ------------------------------------------------------------------------
# The NIST AES-256 CTR_DRBG of rng.c, which the known answer tests use.
# AES-256 (FIPS 197) is written out because the standard library has none.


def _xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else a << 1


def _sbox():
    inv = [0] * 256
    for a in range(1, 256):
        for b in range(1, 256):
            x, y, p = a, b, 0
            while y:
                if y & 1:
                    p ^= x
                x = _xtime(x)
                y >>= 1
            if p == 1:
                inv[a] = b
                break
    box = []
    for a in range(256):
        x = s = inv[a]
        for _ in range(4):
            x = ((x << 1) | (x >> 7)) & 0xFF
            s ^= x
        box.append(s ^ 0x63)
    return box


SBOX = _sbox()


def aes256_encrypt(key, block):
    w = [list(key[4 * i:4 * i + 4]) for i in range(8)]
    rcon = 1
    for i in range(8, 60):
        t = list(w[i - 1])
        if i % 8 == 0:
            t = [SBOX[b] for b in t[1:] + t[:1]]
            t[0] ^= rcon
            rcon = _xtime(rcon)
        elif i % 8 == 4:
            t = [SBOX[b] for b in t]
        w.append([a ^ b for a, b in zip(w[i - 8], t)])
    rk = [sum(w[4 * r:4 * r + 4], []) for r in range(15)]
    s = [a ^ b for a, b in zip(block, rk[0])]
    for r in range(1, 15):
        s = [SBOX[b] for b in s]
        s = [s[(i + 4 * (i % 4)) % 16] for i in range(16)]
        if r != 14:
            t = []
            for c in range(4):
                a = s[4 * c:4 * c + 4]
                x = a[0] ^ a[1] ^ a[2] ^ a[3]
                t += [a[i] ^ x ^ _xtime(a[i] ^ a[(i + 1) % 4]) for i in range(4)]
            s = t
        s = [a ^ b for a, b in zip(s, rk[r])]
    return bytes(s)


class NistDrbg:
    def __init__(self, seed):
        self.key, self.v = bytes(32), bytes(16)
        self._update(seed)

    def _block(self):
        self.v = ((int.from_bytes(self.v, "big") + 1) % (1 << 128)).to_bytes(16, "big")
        return aes256_encrypt(self.key, self.v)

    def _update(self, data):
        temp = self._block() + self._block() + self._block()
        if data is not None:
            temp = bytes(a ^ b for a, b in zip(temp, data))
        self.key, self.v = temp[:32], temp[32:]

    def randombytes(self, n):
        out = b""
        while len(out) < n:
            out += self._block()
        self._update(None)
        return out[:n]


def test_aes256_fips197_c3():
    key = bytes(range(32))
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    assert aes256_encrypt(key, pt).hex() == "8ea2b7ca516745bfeafc49904b496089"


# ------------------------------------------------------------------------
# Official vector: NewHope round 2 submission package (NewHope-Round2.zip from
# the NIST PQC round 2 page), file KAT/newhope512cpa/PQCkemKAT_896.rsp,
# header "NewHope512-CPAKEM", count = 0. Digests are SHA-256 of pk, sk, ct.
KAT_SEED = "061550234D158C5EC95595FE04EF7A25767F2E24CC2BC479D09D86DC9ABCFDE7056A8C266F9EF97ED08541DBD2E1FFA1"
KAT_PK_SHA256 = "7f82c51b3c0da1daa58beafd7316a3df630de5445145c1ba672ec609295488c1"
KAT_SK_SHA256 = "67c6d61e8fadcfe2b6ec116827bc5922219c2d5e09515c2ba961f8f1a4647b2b"
KAT_CT_SHA256 = "4c4a842c43804a60d0b7e7849f95a543588da4de60e96bffb7e640fcf6abb832"
KAT_SS = "E2D149E453F227B4D96786194C365E4B4321E01277A37764D384C3103D4F978F"


def test_kat_count0():
    rng = NistDrbg(bytes.fromhex(KAT_SEED))
    pk, sk = keygen(rng.randombytes(32))
    ct, ss = encaps(pk, rng.randombytes(32))
    assert (len(pk), len(sk), len(ct)) == (PK_BYTES, SK_BYTES, CT_BYTES) == (928, 896, 1088)
    assert hashlib.sha256(pk).hexdigest() == KAT_PK_SHA256
    assert hashlib.sha256(sk).hexdigest() == KAT_SK_SHA256
    assert hashlib.sha256(ct).hexdigest() == KAT_CT_SHA256
    assert ss.hex().upper() == KAT_SS
    assert decaps(sk, ct) == ss


def test_tables_match_reference_heads():
    # First entries of precomp.c (Montgomery form, R = 2^18) in the same package.
    r = pow(2, 18, Q)
    br9 = [int(format(i, "09b")[::-1], 2) for i in range(6)]
    assert [pow(GAMMA, e, Q) * r % Q for e in br9] == [4075, 5315, 7965, 7373, 522, 10120]
    assert [pow(GAMMA, -i, Q) * pow(N, -1, Q) * r % Q for i in range(6)] == [512, 3944, 4267, 5411, 9615, 5900]


def test_ntt_gives_negacyclic_product():
    # The reference NTT reads its input in bit-reversed order and the inverse
    # writes natural order, so invntt(ntt(a) * ntt(b)) is the product of the
    # bit-reversed a and b in Z_q[x]/(x^512 + 1).
    rng = random.Random(1)
    br = [int(format(i, "09b")[::-1], 2) for i in range(N)]
    a0 = [rng.randrange(Q) for _ in range(N)]
    b0 = [rng.randrange(-8, 9) % Q for _ in range(N)]
    assert invntt(ntt(a0)) == [a0[br[i]] for i in range(N)]
    got = invntt(pointwise(ntt(a0), ntt(b0)))
    a = [a0[br[i]] for i in range(N)]
    b = [b0[br[i]] for i in range(N)]
    ref = [0] * N
    for i in range(N):
        if b[i]:
            for j in range(N):
                k = i + j
                if k < N:
                    ref[k] += a[j] * b[i]
                else:
                    ref[k - N] -= a[j] * b[i]
    assert got == [x % Q for x in ref]


def test_round_trips():
    rng = random.Random(9)
    for _ in range(3):
        pk, sk = keygen(rng.randbytes(32))
        m = rng.randbytes(32)
        assert pke_dec(sk, pke_enc(pk, m, rng.randbytes(32))) == m
        ct, ss = encaps(pk, rng.randbytes(32))
        assert decaps(sk, ct) == ss
