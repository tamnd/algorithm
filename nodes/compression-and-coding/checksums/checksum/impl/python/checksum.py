# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/checksum/. The authors are listed in prov/B82EKR.jsonl.

"""Five checksums and a harness that measures how often each one misses
random errors of a given kind.

A checksum here is a function from bytes to a short int. The harness flips
bits of a random message and counts the trials in which the checksum of the
damaged message equals the checksum of the original.
"""

import random
import zlib
from collections.abc import Callable


def parity(data: bytes) -> int:
    """1 bit: the XOR of all bits (even parity)."""
    return int.from_bytes(data, "big").bit_count() & 1


def lrc(data: bytes) -> int:
    """8 bits: the XOR of all bytes, one parity bit per bit column."""
    x = 0
    for b in data:
        x ^= b
    return x


def sum8(data: bytes) -> int:
    """8 bits: the sum of the bytes modulo 256."""
    return sum(data) & 0xFF


def _crc8_table(poly: int) -> list[int]:
    table = []
    for v in range(256):
        reg = v
        for _ in range(8):
            reg = ((reg << 1) ^ poly) & 0xFF if reg & 0x80 else (reg << 1) & 0xFF
        table.append(reg)
    return table


_CRC8 = _crc8_table(0x07)


def crc8(data: bytes) -> int:
    """8 bits: CRC-8/SMBUS, poly 0x07, init 0, no reflection, check 0xF4."""
    reg = 0
    for b in data:
        reg = _CRC8[reg ^ b]
    return reg


def crc32(data: bytes) -> int:
    """32 bits: CRC-32/ISO-HDLC from zlib, check 0xCBF43926."""
    return zlib.crc32(data)


CHECKS: dict[str, Callable[[bytes], int]] = {
    "parity": parity, "lrc": lrc, "sum8": sum8, "crc8": crc8, "crc32": crc32,
}


def flip(data: bytes, positions: list[int]) -> bytes:
    """Flip bits by position; bit 0 is the most significant bit of byte 0,
    the order in which a non-reflected CRC reads the bits."""
    n = len(data) * 8
    x = int.from_bytes(data, "big")
    for p in positions:
        x ^= 1 << (n - 1 - p)
    return x.to_bytes(len(data), "big")


def error_single(rng: random.Random, nbits: int) -> list[int]:
    return [rng.randrange(nbits)]


def error_double(rng: random.Random, nbits: int) -> list[int]:
    return rng.sample(range(nbits), 2)


def error_burst(lo: int, hi: int) -> Callable[[random.Random, int], list[int]]:
    """A burst of length b in [lo, hi]: the first and the last bit flip,
    and each bit between flips with probability 1/2."""

    def make(rng: random.Random, nbits: int) -> list[int]:
        b = rng.randint(lo, hi)
        start = rng.randrange(nbits - b + 1)
        inner = [start + i for i in range(1, b - 1) if rng.getrandbits(1)]
        return [start, *inner, start + b - 1] if b > 1 else [start]

    return make


ERRORS = {
    "single": error_single,
    "double": error_double,
    "burst 2-8": error_burst(2, 8),
    "burst 9-32": error_burst(9, 32),
}


def miss_rates(trials: int, length: int, seed: int) -> dict[str, dict[str, int]]:
    """For each error kind and each checksum, the number of missed errors in
    `trials` random messages of `length` bytes."""
    rng = random.Random(seed)
    out = {e: dict.fromkeys(CHECKS, 0) for e in ERRORS}
    for ename, make in ERRORS.items():
        for _ in range(trials):
            msg = rng.randbytes(length)
            bad = flip(msg, make(rng, length * 8))
            for cname, f in CHECKS.items():
                if f(msg) == f(bad):
                    out[ename][cname] += 1
    return out


if __name__ == "__main__":
    t = 10_000
    res = miss_rates(t, 64, seed=2024)
    print("errors      " + "".join(f"{c:>9}" for c in CHECKS))
    for e, row in res.items():
        print(f"{e:<12}" + "".join(f"{row[c] / t:9.4f}" for c in CHECKS))
