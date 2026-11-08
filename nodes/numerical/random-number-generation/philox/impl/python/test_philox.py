# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/philox/. The authors are listed in prov/JXHPPT.jsonl.

import random

from philox import Philox4x32Stream, philox, philox4x32, philox_inverse

# Known-answer vectors from the file examples/kat_vectors of the Random123 distribution:
# name, rounds, counter words, key words, expected output words (hexadecimal).
KAT = [
    "philox2x32 7 00000000 00000000 00000000 257a3673 cd26be2a",
    "philox2x32 7 ffffffff ffffffff ffffffff ab302c4d 3dc9d239",
    "philox2x32 7 243f6a88 85a308d3 13198a2e bedbbe6b e4c770b3",
    "philox2x32 10 00000000 00000000 00000000 ff1dae59 6cd10df2",
    "philox2x32 10 ffffffff ffffffff ffffffff 2c3f628b ab4fd7ad",
    "philox2x32 10 243f6a88 85a308d3 13198a2e dd7ce038 f62a4c12",
    "philox4x32 7 00000000 00000000 00000000 00000000 00000000 00000000 5f6fb709 0d893f64 4f121f81 4f730a48",
    "philox4x32 7 ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff 5207ddc2 45165e59 4d8ee751 8c52f662",
    "philox4x32 7 243f6a88 85a308d3 13198a2e 03707344 a4093822 299f31d0 4dfccaba 190a87f0 c47362ba b6b5242a",
    "philox4x32 10 00000000 00000000 00000000 00000000 00000000 00000000 6627e8d5 e169c58d bc57ac4c 9b00dbd8",
    "philox4x32 10 ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff 408f276d 41c83b0e a20bc7c6 6d5451fd",
    "philox4x32 10 243f6a88 85a308d3 13198a2e 03707344 a4093822 299f31d0 d16cfe09 94fdcceb 5001e420 24126ea1",
    "philox2x64 7 0000000000000000 0000000000000000 0000000000000000 b41da69fbfefc666 511e9ce1a5534056",
    "philox2x64 7 ffffffffffffffff ffffffffffffffff ffffffffffffffff a4696cc04462015d 724782dae17169e9",
    "philox2x64 7 243f6a8885a308d3 13198a2e03707344 a4093822299f31d0 98ed1534392bf372 67528b1568882fd5",
    "philox2x64 10 0000000000000000 0000000000000000 0000000000000000 ca00a0459843d731 66c24222c9a845b5",
    "philox2x64 10 ffffffffffffffff ffffffffffffffff ffffffffffffffff 65b021d60cd8310f 4d02f3222f86df20",
    "philox2x64 10 243f6a8885a308d3 13198a2e03707344 a4093822299f31d0 0a5e742c2997341c b0f883d38000de5d",
    "philox4x64 7 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 5dc8ee6268ec62cd 139bc570b6c125a0 84d6deb4fb65f49e aff7583376d378c2",
    "philox4x64 7 ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff 071dd84367903154 48e2bbdc722b37d1 6afa9890bb89f76c 9194c8d8ada56ac7",
    "philox4x64 7 243f6a8885a308d3 13198a2e03707344 a4093822299f31d0 082efa98ec4e6c89 452821e638d01377 be5466cf34e90c6c 513a366704edf755 f05d9924c07044d3 bef2cb9cbea74c6c 8db948de4caa1f8a",
    "philox4x64 10 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 16554d9eca36314c db20fe9d672d0fdc d7e772cee186176b 7e68b68aec7ba23b",
    "philox4x64 10 ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff 87b092c3013fe90b 438c3c67be8d0224 9cc7d7c69cd777b6 a09caebf594f0ba0",
    "philox4x64 10 243f6a8885a308d3 13198a2e03707344 a4093822299f31d0 082efa98ec4e6c89 452821e638d01377 be5466cf34e90c6c a528f45403e61d95 38c72dbd566e9788 a5a1610e72fd18b5 57bd43b5e52b7fe6",]


def _parse(line):
    f = line.split()
    n, w, rounds = int(f[0][6]), int(f[0][8:]), int(f[1])
    v = [int(x, 16) for x in f[2:]]
    return n, w, rounds, v[:n], v[n : n + n // 2], v[n + n // 2 :]


def test_known_answers():
    assert len(KAT) == 24
    for line in KAT:
        n, w, rounds, ctr, key, out = _parse(line)
        assert philox(n, w, ctr, key, rounds) == out, line
        if (n, w) == (4, 32):
            assert philox4x32(ctr, key, rounds) == out


def test_inverse_round_trip():
    rng = random.Random(1)
    for line in KAT:
        n, w, rounds, ctr, key, out = _parse(line)
        assert philox_inverse(n, w, out, key, rounds) == ctr
    for n, w in ((2, 32), (4, 32), (2, 64), (4, 64)):
        for _ in range(50):
            ctr = [rng.getrandbits(w) for _ in range(n)]
            key = [rng.getrandbits(w) for _ in range(n // 2)]
            assert philox_inverse(n, w, philox(n, w, ctr, key), key) == ctr


def test_toy_versions_are_bijections():
    # Philox2x8 and Philox4x4 with odd multipliers: every counter of 16 bits maps to a distinct output.
    toy2 = ([0xD3], [0x9F])
    for key in ([0x00], [0x5A]):
        outs = {tuple(philox(2, 8, [c & 255, c >> 8], key, 6, toy2)) for c in range(1 << 16)}
        assert len(outs) == 1 << 16
    toy4 = ([0xD, 0xB], [0x9, 0xB])
    outs = {tuple(philox(4, 4, [(c >> s) & 15 for s in (0, 4, 8, 12)], [3, 7], 6, toy4)) for c in range(1 << 16)}
    assert len(outs) == 1 << 16


def _avalanche(rounds, rng, samples=64):
    flips, per_bit = 0, [0] * 128
    for _ in range(samples):
        c = [rng.getrandbits(32) for _ in range(4)]
        k = [rng.getrandbits(32) for _ in range(2)]
        base = philox4x32(c, k, rounds)
        for b in range(128):
            c2 = list(c)
            c2[b // 32] ^= 1 << (b % 32)
            diff = [x ^ y for x, y in zip(base, philox4x32(c2, k, rounds))]
            for i, d in enumerate(diff):
                flips += bin(d).count("1")
                for j in range(32):
                    per_bit[32 * i + j] += (d >> j) & 1
    trials = samples * 128
    return flips / trials, [p / trials for p in per_bit]


def test_avalanche():
    rng = random.Random(7)
    mean10, per_bit = _avalanche(10, rng)
    assert 63 < mean10 < 65  # half of the 128 output bits flip on average
    assert all(0.46 < p < 0.54 for p in per_bit)  # 8192 trials per bit: about 7 standard deviations
    mean2, _ = _avalanche(2, rng, samples=16)
    assert mean2 < 35  # two rounds are far from enough


def test_stream_uniformity_and_counters():
    s = Philox4x32Stream([0x12345678, 0x9ABCDEF0])
    words = [s.next32() for _ in range(1 << 14)]
    assert words[:4] == philox4x32([0, 0, 0, 0], [0x12345678, 0x9ABCDEF0])
    assert words[4:8] == philox4x32([1, 0, 0, 0], [0x12345678, 0x9ABCDEF0])
    counts = [0] * 16
    for x in words:
        counts[x >> 28] += 1
    e = len(words) / 16
    chi2 = sum((c - e) ** 2 / e for c in counts)
    assert chi2 < 37.70  # 15 degrees of freedom, upper 0.001 point
    # Random access: block i does not depend on blocks before it.
    t = Philox4x32Stream([0x12345678, 0x9ABCDEF0], start=1000)
    assert [t.next32() for _ in range(4)] == words[4000:4004]
    # Different keys give unrelated streams.
    u = Philox4x32Stream([0x12345679, 0x9ABCDEF0])
    same = sum(a == u.next32() for a in words[:1000])
    assert same <= 1
