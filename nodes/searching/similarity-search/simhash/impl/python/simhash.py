# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simhash/. The authors are listed in prov/A430AD.jsonl.

import hashlib
import math
import random
from typing import Callable, Hashable, Mapping, Optional

BitHash = Callable[[Hashable], int]


def default_hash(b: int, seed: int = 0) -> BitHash:
    """A b-bit hash of repr(f), from keyed BLAKE2b."""
    key = f"simhash:{seed}".encode()
    nbytes = (b + 7) // 8

    def h(f: Hashable) -> int:
        out = b""
        block = 0
        while len(out) < nbytes:
            out += hashlib.blake2b(f"{block}:{f!r}".encode(), digest_size=64, key=key).digest()
            block += 1
        return int.from_bytes(out[:nbytes], "big") >> (8 * nbytes - b)

    return h


def simhash(weights: Mapping[Hashable, float], b: int = 64, h: Optional[BitHash] = None) -> int:
    """The b-bit SimHash of a weighted feature set, as an int; bit 1 is the most significant.

    Cost O(m b) for m features.
    """
    if h is None:
        h = default_hash(b)
    v = [0.0] * b  # @line L1
    for f, w in weights.items():  # @line L2
        s = h(f)  # @line L3
        for i in range(b):  # @line L4
            if (s >> (b - 1 - i)) & 1:  # @line L5
                v[i] += w
            else:
                v[i] -= w
    fp = 0
    for i in range(b):  # @line L6
        fp = (fp << 1) | (1 if v[i] > 0 else 0)
    return fp  # @line L7


def simhash_gaussian(weights: Mapping[Hashable, float], b: int = 64, seed: int = 0) -> int:
    """The Gaussian variant: feature f votes w(f) * g_i(f) on bit i, with g_i(f) ~ N(0, 1) from a hash."""
    v = [0.0] * b
    for f, w in weights.items():
        digest = hashlib.blake2b(f"{seed}:{f!r}".encode(), digest_size=16).digest()
        rng = random.Random(int.from_bytes(digest, "big"))
        for i in range(b):
            v[i] += w * rng.gauss(0.0, 1.0)
    fp = 0
    for i in range(b):
        fp = (fp << 1) | (1 if v[i] > 0 else 0)
    return fp


def distance(fp1: int, fp2: int) -> int:
    """The Hamming distance of two fingerprints."""
    return bin(fp1 ^ fp2).count("1")  # @line L8


def angle(x: Mapping[Hashable, float], y: Mapping[Hashable, float]) -> float:
    """The angle between two sparse weight vectors, in radians."""
    dot = sum(w * y.get(f, 0.0) for f, w in x.items())
    nx = math.sqrt(sum(w * w for w in x.values()))
    ny = math.sqrt(sum(w * w for w in y.values()))
    return math.acos(max(-1.0, min(1.0, dot / (nx * ny))))
