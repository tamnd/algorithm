# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/avalanche-effect/. The authors are listed in prov/RP1KY4.jsonl.

import hashlib
import math
import random

from avalanche_effect import avalanche, flip_bit, popcount, weak_hash


def sha256(x: bytes) -> bytes:
    return hashlib.sha256(x).digest()


def test_sha256_flips_about_half() -> None:
    s = avalanche(sha256, 8, 100, random.Random(1973))
    assert s["out_bits"] == 256
    assert abs(s["mean_fraction"] - 0.5) < 0.005
    # a random function flips Binomial(256, 1/2) bits: standard deviation 8
    assert abs(s["std_flips"] - s["std_ideal"]) / s["std_ideal"] < 0.05
    # SAC: each estimate is a mean of 100 fair coins; E|p - 1/2| = sqrt(2/pi) * 0.05 = 0.0399
    want = math.sqrt(2 / math.pi) * 0.5 / math.sqrt(100)
    assert abs(s["sac_mean_dev"] - want) / want < 0.1
    assert s["sac_max_dev"] < 0.3


def test_weak_hash_fails() -> None:
    s = avalanche(weak_hash, 8, 100, random.Random(1985))
    assert s["mean_fraction"] == 1 / 32  # one input bit changes exactly one output bit
    assert s["std_flips"] == 0
    assert s["sac_max_dev"] == 0.5


def test_weak_hash_is_linear() -> None:
    # the toy hash is linear over GF(2): h(x ^ y) = h(x) ^ h(y) ^ h(0)
    rng = random.Random(5)
    for _ in range(500):
        x = bytes(rng.getrandbits(8) for _ in range(8))
        y = bytes(rng.getrandbits(8) for _ in range(8))
        xy = bytes(p ^ q for p, q in zip(x, y))
        hx, hy, hxy, h0 = (int.from_bytes(weak_hash(v), "big") for v in (x, y, xy, bytes(8)))
        assert hxy == hx ^ hy ^ h0


def test_helpers() -> None:
    assert flip_bit(b"\x00\x00", 0) == b"\x80\x00"
    assert flip_bit(b"\x00\x00", 15) == b"\x00\x01"
    assert popcount(b"\xff\x01") == 9
