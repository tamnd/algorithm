# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hqc/. The authors are listed in prov/E4EFXK.jsonl.
"""Tests for the HQC-1 structure.

The official HQC KAT files are not used: the hashing, seed expansion,
sampling and encodings here are simplified, so the bytes cannot match. There
are no official test vectors for this code. The tests check the parameters,
the Reed-Solomon and Reed-Muller decoders against brute force, the noise
weight against its predicted mean, the PKE and KEM round trips, and implicit
rejection.
"""

import random
from math import exp

from hqc import (
    GF,
    GF256,
    N,
    N1,
    N2,
    RS,
    TRUNC,
    W,
    WE,
    WR,
    ReedSolomon,
    code_decode,
    code_encode,
    decaps,
    decrypt,
    encaps,
    encrypt,
    hash_k,
    kem_keygen,
    keygen,
    mul_sparse,
    rm_decode,
    rm_encode,
    support,
)


def test_parameters():
    assert all(N % p for p in range(2, int(N ** 0.5) + 1))
    x, order = 2, 1
    while x != 1:
        x, order = x * 2 % N, order + 1
    assert order == N - 1                      # x^n - 1 = (x - 1) times an irreducible factor
    assert N1 * N2 == 17664 <= N
    assert (RS.n, RS.k, RS.r) == (46, 16, 30)
    assert 40 + (N + 7) // 8 == 2249           # public key bytes in NIST IR 8545, Table 8 (seed plus s)


def test_gf256():
    for a in range(1, 256):
        assert GF256.mul(a, GF256.div(1, a)) == 1
    rng = random.Random(1)
    for _ in range(500):
        a, b, c = (rng.randrange(256) for _ in range(3))
        assert GF256.mul(a, b ^ c) == GF256.mul(a, b) ^ GF256.mul(a, c)


def test_reed_solomon_small_against_brute_force():
    """[7, 3] over GF(8) corrects 2 errors; compare with the nearest codeword."""
    gf = GF(3, 0b1011)
    rs = ReedSolomon(gf, 7, 3)
    book = {}
    for v in range(512):
        msg = [(v >> 6) & 7, (v >> 3) & 7, v & 7]
        book[tuple(rs.encode(msg))] = msg
    words = list(book)
    min_dist = min(sum(a != b for a, b in zip(c, [0] * 7)) for c in words if any(c))
    assert min_dist == 5
    rng = random.Random(2)
    for _ in range(500):
        y = list(rng.choice(words))
        for p in rng.sample(range(7), rng.randint(0, 2)):
            y[p] ^= rng.randrange(1, 8)
        nearest = min(words, key=lambda c: sum(a != b for a, b in zip(c, y)))
        assert rs.decode(y) == book[nearest]


def test_reed_solomon_hqc_corrects_15_errors():
    rng = random.Random(3)
    for _ in range(300):
        msg = [rng.randrange(256) for _ in range(16)]
        cw = RS.encode(msg)
        assert RS.syndromes(cw) == [0] * 30
        y = list(cw)
        for p in rng.sample(range(46), rng.randint(0, 15)):
            y[p] ^= rng.randrange(1, 256)
        assert RS.decode(y) == msg


def test_reed_muller_against_brute_force():
    """The repeated RM(1,7) code has minimum distance 192; with at most 95
    flipped bits the nearest codeword is unique, and the transform decoder
    must find it."""
    book = [rm_encode(b) for b in range(256)]
    assert min(bin(book[a] ^ book[b]).count("1") for a in range(0, 256, 17) for b in range(256) if a != b) == 192
    rng = random.Random(4)
    for _ in range(500):
        b = rng.randrange(256)
        noise = sum(1 << i for i in rng.sample(range(N2), rng.randint(0, 95)))
        y = book[b] ^ noise
        nearest = min(range(256), key=lambda c: bin(book[c] ^ y).count("1"))
        assert rm_decode(y) == nearest == b


def test_concatenated_code():
    rng = random.Random(5)
    for _ in range(5):
        m = rng.randbytes(16)
        word = code_encode(m)
        assert word.bit_length() <= N1 * N2
        noise = sum(1 << i for i in rng.sample(range(N1 * N2), 4000))
        assert code_decode(word ^ noise) == m


def test_ring_multiplication_against_naive():
    rng = random.Random(6)
    for _ in range(500):
        n = rng.choice([7, 11, 13])
        a, b = rng.getrandbits(n), rng.getrandbits(n)
        naive = 0
        for i in range(n):
            for j in range(n):
                if (a >> i) & 1 and (b >> j) & 1:
                    naive ^= 1 << ((i + j) % n)
        assert mul_sparse(a, support(b), n) == naive


def test_pke_round_trip_and_noise_weight():
    """The decryption noise x r2 + r1 y + e is a sum of about 2 w wr + we
    random positions, so each bit is 1 with probability (1 - exp(-2 L / n)) / 2
    with L = 2 w wr + we."""
    rng = random.Random(7)
    pk, sk = keygen(rng)
    weights = []
    for _ in range(10):
        m = rng.randbytes(16)
        u, v = encrypt(pk, m, rng.randbytes(32))
        assert decrypt(sk, (u, v)) == m
        noise = v ^ (mul_sparse(u, sk[1]) & TRUNC) ^ code_encode(m)
        weights.append(bin(noise).count("1"))
    predicted = N1 * N2 * (1 - exp(-2 * (2 * W * WR + WE) / N)) / 2
    mean = sum(weights) / len(weights)
    assert abs(mean - predicted) < 0.02 * predicted


def test_kem_round_trip():
    rng = random.Random(8)
    for _ in range(2):
        pk, sk = kem_keygen(rng)
        for _ in range(5):
            c, k = encaps(pk, rng)
            assert decaps(sk, c) == k


def test_implicit_rejection():
    """Flipping a bit of v does not change the decoded message (the code
    corrects it), but re-encryption no longer matches, so the KEM rejects."""
    rng = random.Random(9)
    pk, ksk = kem_keygen(rng)
    sigma = ksk[2]
    (u, v, salt), k = encaps(pk, rng)
    bad = (u, v ^ 1, salt)
    assert decrypt(ksk[0], (u, v ^ 1)) == decrypt(ksk[0], (u, v))
    assert decaps(ksk, bad) == hash_k(sigma, bad) != k
