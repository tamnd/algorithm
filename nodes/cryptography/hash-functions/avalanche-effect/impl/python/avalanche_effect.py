# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/avalanche-effect/. The authors are listed in prov/RP1KY4.jsonl.
"""Measure the avalanche effect and the strict avalanche criterion (SAC) of a hash.

For study only. The code is not constant time, and a good score here is a
heuristic: it is not a proof of security. The weak toy hash below must not be
used for anything; use SHA-256 or SHA-3 from the standard library, a FIPS 140
validated module, or libsodium.

Cost: samples * (in_bits + 1) calls of the hash, and in_bits * out_bits counters.
"""

import math
import random
from typing import Callable

Hash = Callable[[bytes], bytes]


def flip_bit(x: bytes, i: int) -> bytes:
    """x with bit i flipped (bit 0 is the top bit of byte 0)."""
    b = bytearray(x)
    b[i // 8] ^= 0x80 >> (i % 8)
    return bytes(b)


def popcount(x: bytes) -> int:
    return bin(int.from_bytes(x, "big")).count("1")


def avalanche(h: Hash, in_bytes: int, samples: int, rng: random.Random) -> dict[str, float]:
    """Flip each input bit of random inputs and count the output bits that change.

    Returns: mean fraction of output bits flipped, the standard deviation of
    the number flipped, the sqrt(out_bits)/2 that a random function would give
    for it, and the SAC deviation: max over (i, j) of
    |Pr[output bit j flips | input bit i flips] - 1/2|, and its mean.
    """
    in_bits = 8 * in_bytes
    out_bits = 8 * len(h(bytes(in_bytes)))
    counts = [[0] * out_bits for _ in range(in_bits)]
    flips: list[int] = []
    for _ in range(samples):
        x = bytes(rng.getrandbits(8) for _ in range(in_bytes))
        y = int.from_bytes(h(x), "big")
        for i in range(in_bits):
            d = y ^ int.from_bytes(h(flip_bit(x, i)), "big")
            flips.append(bin(d).count("1"))
            row = counts[i]
            for j in range(out_bits):
                if d >> (out_bits - 1 - j) & 1:
                    row[j] += 1
    mean = sum(flips) / len(flips)
    var = sum((f - mean) ** 2 for f in flips) / len(flips)
    devs = [abs(c / samples - 0.5) for row in counts for c in row]
    return {
        "mean_fraction": mean / out_bits,
        "std_flips": math.sqrt(var),
        "std_ideal": math.sqrt(out_bits) / 2,
        "sac_max_dev": max(devs),
        "sac_mean_dev": sum(devs) / len(devs),
        "out_bits": out_bits,
    }


def weak_hash(x: bytes) -> bytes:
    """A weak 32-bit toy hash: h = rotl(h, 5) XOR byte, with no nonlinear mixing."""
    h = 0
    for b in x:
        h = ((h << 5) | (h >> 27)) & 0xFFFFFFFF
        h ^= b
    return h.to_bytes(4, "big")
