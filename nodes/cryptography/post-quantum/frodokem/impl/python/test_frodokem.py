# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frodokem/. The authors are listed in prov/MD60D5.jsonl.

import hashlib

from frodokem import CT_BYTES, PK_BYTES, SK_BYTES, decaps, decode, encaps, encode, keygen, pack, sample, unpack

# ------------------------------------------------------------------------
# The NIST AES-256 CTR_DRBG of rng.c, which the known answer tests use.
# AES-256 is written out here (FIPS 197) because the standard library has
# no AES; it is a test helper only.


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
        x = inv[a]
        s = x
        for _ in range(4):
            x = ((x << 1) | (x >> 7)) & 0xFF
            s ^= x
        box.append(s ^ 0x63)
    return box


SBOX = _sbox()


def _expand_key(key):
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
    return [sum(w[4 * r:4 * r + 4], []) for r in range(15)]


def aes256_encrypt(key, block):
    rk = _expand_key(key)
    s = [a ^ b for a, b in zip(block, rk[0])]
    for r in range(1, 15):
        s = [SBOX[b] for b in s]
        s = [s[(i + 4 * (i % 4)) % 16] for i in range(16)]  # ShiftRows
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

    def _inc(self):
        self.v = ((int.from_bytes(self.v, "big") + 1) % (1 << 128)).to_bytes(16, "big")

    def _update(self, data):
        temp = b""
        for _ in range(3):
            self._inc()
            temp += aes256_encrypt(self.key, self.v)
        if data is not None:
            temp = bytes(a ^ b for a, b in zip(temp, data))
        self.key, self.v = temp[:32], temp[32:]

    def randombytes(self, n):
        out = b""
        while len(out) < n:
            self._inc()
            out += aes256_encrypt(self.key, self.v)
        self._update(None)
        return out[:n]


def test_aes256_fips197_c3():
    # FIPS 197, Appendix C.3 (AES-256 example vector)
    key = bytes(range(32))
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    assert aes256_encrypt(key, pt).hex() == "8ea2b7ca516745bfeafc49904b496089"


# ------------------------------------------------------------------------
# Official vector: FrodoKEM repository (github.com/microsoft/PQCrypto-LWEKE),
# file eFrodoKEM/KAT/PQCkemKAT_19888_shake.rsp, header "FrodoKEM-640-SHAKE",
# count = 0. pk, sk and ct are long, so the test compares SHA-256 digests.
KAT_SEED = "061550234D158C5EC95595FE04EF7A25767F2E24CC2BC479D09D86DC9ABCFDE7056A8C266F9EF97ED08541DBD2E1FFA1"
KAT_PK_SHA256 = "49a303460f0977339cbd2c1b5aa0e7af44c5024917f5f7aced4725e9d4a2c614"
KAT_SK_SHA256 = "85d0e3163f8caebee1b54837a470e6b04983784e3c3d2b2f036b7f95875508aa"
KAT_CT_SHA256 = "88ba537b536d89fd0b84f8604a6040a9dd96114ee6ad43235c951edf426c680d"
KAT_SS = "729780FC51657E21357F03A338116569"


def test_kat_count0_and_round_trip():
    rng = NistDrbg(bytes.fromhex(KAT_SEED))
    pk, sk = keygen(rng.randombytes(48))
    ct, ss = encaps(pk, rng.randombytes(16))
    assert (len(pk), len(sk), len(ct)) == (PK_BYTES, SK_BYTES, CT_BYTES) == (9616, 19888, 9720)
    assert hashlib.sha256(pk).hexdigest() == KAT_PK_SHA256
    assert hashlib.sha256(sk).hexdigest() == KAT_SK_SHA256
    assert hashlib.sha256(ct).hexdigest() == KAT_CT_SHA256
    assert ss.hex().upper() == KAT_SS
    assert decaps(sk, ct) == ss
    # implicit rejection: a changed ciphertext gives SHAKE128(ct' || s)
    bad = bytearray(ct)
    bad[5] ^= 0x40
    bad = bytes(bad)
    assert decaps(sk, bad) == hashlib.shake_128(bad + sk[:16]).digest(16)


def test_sampler_matches_table():
    # r = 2 p + sign; p <= 4643 gives 0, the largest p gives the largest value 12
    assert sample(0) == 0 and sample(2 * 4643) == 0
    assert sample(2 * 4644) == 1 and sample(2 * 4644 + 1) == -1
    assert sample(2 * 32767) == 12


def test_encode_decode_tolerates_small_noise():
    mu = bytes(range(16))
    m = encode(mu)
    noisy = [(x + d) % (1 << 15) for x, d in zip(m, [4095, -4096, 100, -1] * 16)]
    assert decode(noisy) == mu


def test_pack_round_trip():
    vals = [(i * 7919) % (1 << 15) for i in range(64)]
    assert unpack(pack(vals), 64) == vals
