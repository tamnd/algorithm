# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ntru-encrypt/. The authors are listed in prov/T0H5SG.jsonl.

import hashlib
import random

from ntru_encrypt import (
    CT_BYTES,
    FG_BYTES,
    PK_BYTES,
    SK_BYTES,
    WEIGHT,
    ClassicNTRU,
    cyclic_mul,
    decaps,
    encaps,
    keygen,
    sample_fixed_type,
    s3_frombytes,
    s3_tobytes,
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
# Official vector: NTRU round 3 submission package (NTRU-Round3.zip from the
# NIST PQC round 3 page), file KAT/ntruhps2048509/PQCkemKAT_935.rsp,
# count = 0. Digests are SHA-256 of the pk, sk and ct of that entry.
KAT_SEED = "061550234D158C5EC95595FE04EF7A25767F2E24CC2BC479D09D86DC9ABCFDE7056A8C266F9EF97ED08541DBD2E1FFA1"
KAT_PK_SHA256 = "64e3a7b0c00566bd6de876e7d4e5e2bbad1e960ccb4660893425c08edb524088"
KAT_SK_SHA256 = "3e493e7c4acab9f0b982d45c96405d40cfdc6a973f5433dfc13b66edba8c044a"
KAT_CT_SHA256 = "b5ada363ed2cf5a460da2bc017688d5820604f14f24312eadfda7cf049d511cd"
KAT_SS = "176FDBB009DD3F848B365AB7F18D9C0C91721931C8594C2C6F043C8600791A6C"


def test_hps2048509_kat_count0():
    rng = NistDrbg(bytes.fromhex(KAT_SEED))
    seed = rng.randombytes(FG_BYTES)
    prf = rng.randombytes(32)
    pk, sk = keygen(seed, prf)
    ct, ss = encaps(pk, rng.randombytes(FG_BYTES))
    assert (len(pk), len(sk), len(ct)) == (PK_BYTES, SK_BYTES, CT_BYTES) == (699, 935, 699)
    assert hashlib.sha256(pk).hexdigest() == KAT_PK_SHA256
    assert hashlib.sha256(sk).hexdigest() == KAT_SK_SHA256
    assert hashlib.sha256(ct).hexdigest() == KAT_CT_SHA256
    assert ss.hex().upper() == KAT_SS
    assert decaps(sk, ct) == ss
    # implicit rejection: a changed ciphertext gives SHA3-256(prf key || ct')
    bad = bytearray(ct)
    bad[17] ^= 4
    bad = bytes(bad)
    assert decaps(sk, bad) == hashlib.sha3_256(prf + bad).digest()


def test_fixed_type_and_trit_packing():
    rng = random.Random(4)
    m = sample_fixed_type(rng.randbytes(1905))
    assert m.count(1) == m.count(2) == WEIGHT // 2 and m[-1] == 0
    assert s3_frombytes(s3_tobytes(m)) == m


def test_classic_toy_round_trip():
    # N = 107, p = 3, q = 64, df = 15, dg = 12, dr = 5: the smallest set of the 1998 paper
    rng = random.Random(1998)
    ntru = ClassicNTRU(107, 3, 64, 15, 12, 5)
    h, sk = ntru.keygen(rng)
    f, fp = sk
    assert cyclic_mul(f, fp, 107, 3) == [1] + [0] * 106
    for _ in range(20):
        m = [rng.choice((-1, 0, 1)) for _ in range(107)]
        assert ntru.decrypt(sk, ntru.encrypt(h, m, rng)) == m


def test_classic_decryption_failure_needs_small_q():
    # With N = 11, p = 3 and the weights below, |p r g + f m| <= 3*6 + 7 = 25.
    # q = 256 > 2*25 never fails; q = 32 fails when a coefficient wraps.
    rng = random.Random(5)
    fails = {}
    for q in (32, 256):
        ntru = ClassicNTRU(11, 3, q, 4, 3, 3)
        h, sk = ntru.keygen(rng)
        bad = 0
        for _ in range(400):
            m = [rng.choice((-1, 0, 1)) for _ in range(11)]
            bad += ntru.decrypt(sk, ntru.encrypt(h, m, rng)) != m
        fails[q] = bad
    assert fails[256] == 0
    assert fails[32] > 0
