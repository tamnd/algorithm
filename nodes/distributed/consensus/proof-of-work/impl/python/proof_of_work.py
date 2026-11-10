# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proof-of-work/. The authors are listed in prov/GDRFMD.jsonl.

"""Hash puzzles and difficulty adjustment.

A solution is a nonce such that SHA-256(data || nonce), read as a 256-bit
number, is below a target. Each try succeeds with probability
p = target / 2**256, independently, so the number of tries is geometric with
mean 1/p. Checking a solution takes one hash.

The retarget rule follows Bitcoin: every `window` blocks, scale the target by
the time the window took over the time it should take, with the factor clamped
to [1/4, 4].
"""

from __future__ import annotations

import hashlib
import random
from fractions import Fraction

HASH_BITS = 256


def h(data: bytes, nonce: int) -> int:
    return int.from_bytes(hashlib.sha256(data + nonce.to_bytes(8, "big")).digest(), "big")


def solve(data: bytes, target: int, start: int = 0) -> tuple[int, int]:
    """Return (nonce, tries)."""
    nonce = start  # @line L1
    while h(data, nonce) >= target:  # @line L2
        nonce += 1
    return nonce, nonce - start + 1  # @line L3


def verify(data: bytes, nonce: int, target: int) -> bool:
    return h(data, nonce) < target  # @line L4


def success_probability(target: int) -> Fraction:
    return Fraction(target, 2 ** HASH_BITS)


def retarget(target: int, actual: float, expected: float, max_target: int) -> int:
    """Scale the target by actual / expected, clamped to [1/4, 4], and capped at max_target."""
    ratio = min(max(actual / expected, 0.25), 4.0)  # @line L5
    return min(int(target * ratio), max_target)


def simulate_chain(hashrates: list[float], target: int, window: int, spacing: float,
                   seed: int) -> tuple[list[float], list[int]]:
    """Block intervals when the hash rate of block i is hashrates[i] hashes per second.

    The time to find a block is exponential with rate hashrate * p, the limit of the
    geometric number of tries. Returns the intervals and the target used for each block.
    """
    rng = random.Random(seed)
    max_target = target
    intervals, targets = [], []
    since = 0.0
    for i, rate in enumerate(hashrates):
        p = target / 2 ** HASH_BITS
        dt = rng.expovariate(rate * p)
        intervals.append(dt)
        targets.append(target)
        since += dt
        if (i + 1) % window == 0:
            target = retarget(target, since, window * spacing, max_target)
            since = 0.0
    return intervals, targets
