# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/saber/. The authors are listed in prov/0XW32T.jsonl.

import hashlib
import random

from saber import CT_BYTES, PK_BYTES, SK_BYTES, decaps, encaps, keygen, pke_dec, pke_enc, poly_mul

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
# Official vector: github.com/KULeuven-COSIC/SABER, file
# KAT/Saber/PQCkemKAT_2304.rsp, count = 0. The digests are SHA-256 of the
# pk, sk and ct hex strings of that entry.
KAT_SEED = "061550234D158C5EC95595FE04EF7A25767F2E24CC2BC479D09D86DC9ABCFDE7056A8C266F9EF97ED08541DBD2E1FFA1"
KAT_PK_SHA256 = "36c12760ea8e750fa3f7c2d67546755bf6fc5fe827ee2eb9e149035dba0b69d0"
KAT_SK_SHA256 = "f19206e46989c05603d3bc7a61e2fb68e386f1864129e7ef0618f037ecd5af54"
KAT_CT_SHA256 = "c6bc6eb78b5b6adcadd7c484a142dac626c1c59fc53d3715b4a9174f10d46310"
KAT_SS = "156533536C8435F82CC36FC1EF9528DEDC49223DDA0091617DC1ACAF6058D1CA"


def test_kat_count0():
    rng = NistDrbg(bytes.fromhex(KAT_SEED))
    seed_a = rng.randombytes(32)
    seed_s = rng.randombytes(32)
    z = rng.randombytes(32)
    pk, sk = keygen(seed_a + seed_s + z)
    ct, ss = encaps(pk, rng.randombytes(32))
    assert (len(pk), len(sk), len(ct)) == (PK_BYTES, SK_BYTES, CT_BYTES) == (992, 2304, 1088)
    assert hashlib.sha256(pk).hexdigest() == KAT_PK_SHA256
    assert hashlib.sha256(sk).hexdigest() == KAT_SK_SHA256
    assert hashlib.sha256(ct).hexdigest() == KAT_CT_SHA256
    assert ss.hex().upper() == KAT_SS
    assert decaps(sk, ct) == ss


def test_implicit_rejection():
    rng = random.Random(7)
    pk, sk = keygen(rng.randbytes(96))
    ct, ss = encaps(pk, rng.randbytes(32))
    bad = bytearray(ct)
    bad[1000] ^= 1
    bad = bytes(bad)
    z = sk[-32:]
    assert decaps(sk, bad) == hashlib.sha3_256(z + hashlib.sha3_256(bad).digest()).digest()
    assert decaps(sk, bad) != ss


def test_pke_round_trips():
    rng = random.Random(11)
    pk, sk = keygen(rng.randbytes(96))
    for _ in range(3):
        m = rng.randbytes(32)
        assert pke_dec(sk[:1248], pke_enc(m, rng.randbytes(32), pk)) == m


def test_karatsuba_matches_schoolbook():
    rng = random.Random(3)
    a = [rng.randrange(-4096, 4096) for _ in range(256)]
    b = [rng.randrange(-4, 5) for _ in range(256)]
    ref = [0] * 256
    for i in range(256):
        for j in range(256):
            k = i + j
            if k < 256:
                ref[k] += a[i] * b[j]
            else:
                ref[k - 256] -= a[i] * b[j]
    assert poly_mul(a, b) == ref
