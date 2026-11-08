# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threefry/. The authors are listed in prov/SS4JEM.jsonl.

import random

from threefry import Threefry2x64Stream, threefry, threefry2x64, threefry_inverse

# Known-answer vectors from the file examples/kat_vectors of the Random123 distribution:
# name, rounds, counter words, key words, expected output words (hexadecimal).
KAT = [
    "threefry2x32 13 00000000 00000000 00000000 00000000 9d1c5ec6 8bd50731",
    "threefry2x32 13 ffffffff ffffffff ffffffff ffffffff fd36d048 2d17272c",
    "threefry2x32 13 243f6a88 85a308d3 13198a2e 03707344 ba3e4725 f27d669e",
    "threefry2x32 20 00000000 00000000 00000000 00000000 6b200159 99ba4efe",
    "threefry2x32 20 ffffffff ffffffff ffffffff ffffffff 1cb996fc bb002be7",
    "threefry2x32 20 243f6a88 85a308d3 13198a2e 03707344 c4923a9c 483df7a0",
    "threefry2x32 32 00000000 00000000 00000000 00000000 cee3d47e a23dfd5c",
    "threefry2x32 32 ffffffff ffffffff ffffffff ffffffff 6e2fe0d0 b1b76f82",
    "threefry2x32 32 243f6a88 85a308d3 13198a2e 03707344 e2827716 c3c05cdf",
    "threefry4x32 13 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 531c7e4f 39491ee5 2c855a92 3d6abf9a",
    "threefry4x32 13 ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff c4189358 1c9cc83a d5881c67 6a0a89e0",
    "threefry4x32 13 243f6a88 85a308d3 13198a2e 03707344 a4093822 299f31d0 082efa98 ec4e6c89 4aa71d8f 734738c2 431fc6a8 ae6debf1",
    "threefry4x32 20 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 9c6ca96a e17eae66 fc10ecd4 5256a7d8",
    "threefry4x32 20 ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff 2a881696 57012287 f6c7446e a16a6732",
    "threefry4x32 20 243f6a88 85a308d3 13198a2e 03707344 a4093822 299f31d0 082efa98 ec4e6c89 59cd1dbb b8879579 86b5d00c ac8b6d84",
    "threefry4x32 72 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 93171da6 9220326d b392b7b1 ff58a002",
    "threefry4x32 72 ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff 60743f3d 9961e684 aab21c34 8c65fb7d",
    "threefry4x32 72 243f6a88 85a308d3 13198a2e 03707344 a4093822 299f31d0 082efa98 ec4e6c89 09930adf 7f27bd55 9ed68ce1 97f803f6",
    "threefry2x64 13 0000000000000000 0000000000000000 0000000000000000 0000000000000000 f167b032c3b480bd e91f9fee4b7a6fb5",
    "threefry2x64 13 ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ccdec5c917a874b1 4df53abca26ceb01",
    "threefry2x64 13 243f6a8885a308d3 13198a2e03707344 a4093822299f31d0 082efa98ec4e6c89 c3aac71561042993 3fe7ae8801aff316",
    "threefry2x64 20 0000000000000000 0000000000000000 0000000000000000 0000000000000000 c2b6e3a8c2c69865 6f81ed42f350084d",
    "threefry2x64 20 ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff e02cb7c4d95d277a d06633d0893b8b68",
    "threefry2x64 20 243f6a8885a308d3 13198a2e03707344 a4093822299f31d0 082efa98ec4e6c89 263c7d30bb0f0af1 56be8361d3311526",
    "threefry2x64 32 0000000000000000 0000000000000000 0000000000000000 0000000000000000 38ba854d7f13cfb3 d02fca729d54fadc",
    "threefry2x64 32 ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff 6b532f4f6e288646 0388f1ec135ee18e",
    "threefry2x64 32 243f6a8885a308d3 13198a2e03707344 a4093822299f31d0 082efa98ec4e6c89 dad492f32efbd0c4 b6d7d0cd1f193e84",
    "threefry4x64 13 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 4071fabee1dc8e05 02ed3113695c9c62 397311b5b89f9d49 e21292c3258024bc",
    "threefry4x64 13 ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff 7eaed935479722b5 90994358c429f31c 496381083e07a75b 627ed0d746821121",
    "threefry4x64 13 243f6a8885a308d3 13198a2e03707344 a4093822299f31d0 082efa98ec4e6c89 452821e638d01377 be5466cf34e90c6c c0ac29b7c97c50dd 3f84d5b5b5470917 4361288ef9c1900c 8717291521782833 0d19db18c20cf47e a0b41d63ac8581e5",
    "threefry4x64 20 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 09218ebde6c85537 55941f5266d86105 4bd25e16282434dc ee29ec846bd2e40b",
    "threefry4x64 20 ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff 29c24097942bba1b 0371bbfb0f6f4e11 3c231ffa33f83a1c cd29113fde32d168",
    "threefry4x64 20 243f6a8885a308d3 13198a2e03707344 a4093822299f31d0 082efa98ec4e6c89 452821e638d01377 be5466cf34e90c6c be5466cf34e90c6c c0ac29b7c97c50dd a7e8fde591651bd9 baafd0c30138319b 84a5c1a729e685b9 901d406ccebc1ba4",
    "threefry4x64 72 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 94eeea8b1f2ada84 adf103313eae6670 952419a1f4b16d53 d83f13e63c9f6b11",
    "threefry4x64 72 ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff ffffffffffffffff 11518c034bc1ff4c 193f10b8bcdcc9f7 d024229cb58f20d8 563ed6e48e05183f",
    "threefry4x64 72 243f6a8885a308d3 13198a2e03707344 a4093822299f31d0 082efa98ec4e6c89 452821e638d01377 be5466cf34e90c6c be5466cf34e90c6c c0ac29b7c97c50dd acf412ccaa3b2270 c9e99bd53f2e9173 43dad469dc825948 fbb19d06c8a2b4dc",
]


def _parse(line):
    f = line.split()
    n, w, rounds = int(f[0][8]), int(f[0][10:]), int(f[1])
    v = [int(x, 16) for x in f[2:]]
    return n, w, rounds, v[:n], v[n : 2 * n], v[2 * n :]


def test_known_answers():
    assert len(KAT) == 36
    for line in KAT:
        n, w, rounds, ctr, key, out = _parse(line)
        assert threefry(n, w, ctr, key, rounds) == out, line
        if (n, w) == (2, 64):
            assert threefry2x64(ctr, key, rounds) == out


def test_inverse_round_trip():
    rng = random.Random(1)
    for line in KAT:
        n, w, rounds, ctr, key, out = _parse(line)
        assert threefry_inverse(n, w, out, key, rounds) == ctr
    for n, w in ((2, 32), (4, 32), (2, 64), (4, 64)):
        for rounds in (1, 4, 13, 20):
            ctr = [rng.getrandbits(w) for _ in range(n)]
            key = [rng.getrandbits(w) for _ in range(n)]
            assert threefry_inverse(n, w, threefry(n, w, ctr, key, rounds), key, rounds) == ctr


def test_toy_versions_are_bijections():
    # Threefry2x8 and Threefry4x4 with small rotations: all 2^16 counters give distinct outputs.
    rot2 = [(3,), (5,), (1,), (6,), (2,), (7,), (4,), (3,)]
    for key in ([0x5A, 0xC3],):
        outs = {tuple(threefry(2, 8, [c & 255, c >> 8], key, 12, rot2)) for c in range(1 << 16)}
        assert len(outs) == 1 << 16
    rot4 = [(1, 3), (2, 1), (3, 2), (1, 1), (2, 3), (3, 1), (1, 2), (2, 2)]
    ctrs = ([(c >> s) & 15 for s in (0, 4, 8, 12)] for c in range(1 << 16))
    outs = {tuple(threefry(4, 4, x, [1, 2, 3, 4], 12, rot4)) for x in ctrs}
    assert len(outs) == 1 << 16


def _avalanche(rounds, rng, samples):
    flips, per_bit = 0, [0] * 128
    for _ in range(samples):
        c = [rng.getrandbits(64) for _ in range(2)]
        k = [rng.getrandbits(64) for _ in range(2)]
        base = threefry2x64(c, k, rounds)
        for b in range(128):
            c2 = list(c)
            c2[b // 64] ^= 1 << (b % 64)
            diff = [x ^ y for x, y in zip(base, threefry2x64(c2, k, rounds))]
            for i, d in enumerate(diff):
                flips += bin(d).count("1")
                for j in range(64):
                    per_bit[64 * i + j] += (d >> j) & 1
    trials = samples * 128
    return flips / trials, [p / trials for p in per_bit]


def test_avalanche():
    rng = random.Random(7)
    mean20, per_bit = _avalanche(20, rng, 64)
    assert 63 < mean20 < 65  # half of the 128 output bits flip on average
    assert all(0.46 < p < 0.54 for p in per_bit)  # 8192 trials per bit: about 7 standard deviations
    mean3, _ = _avalanche(3, rng, 16)
    assert mean3 < 30  # three rounds are far from enough


def test_stream_uniformity_and_random_access():
    s = Threefry2x64Stream([0x0123456789ABCDEF, 0xFEDCBA9876543210])
    words = [s.next64() for _ in range(1 << 13)]
    assert words[:2] == threefry2x64([0, 0], [0x0123456789ABCDEF, 0xFEDCBA9876543210])
    counts = [0] * 16
    for x in words:
        counts[x >> 60] += 1
    e = len(words) / 16
    assert sum((c - e) ** 2 / e for c in counts) < 37.70  # 15 degrees of freedom, upper 0.001 point
    t = Threefry2x64Stream([0x0123456789ABCDEF, 0xFEDCBA9876543210], start=777)
    assert [t.next64(), t.next64()] == words[1554:1556]
    big = Threefry2x64Stream([1, 2], start=(1 << 64) + 5)
    assert [big.next64(), big.next64()] == threefry2x64([5, 1], [1, 2])
