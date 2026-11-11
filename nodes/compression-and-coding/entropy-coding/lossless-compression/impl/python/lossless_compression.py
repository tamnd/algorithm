# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lossless-compression/. The authors are listed in prov/DRHZ6Y.jsonl.

"""A small harness for lossless compressors.

It generates four kinds of data, each with its exact information content
under the source that made it (the sum of -lg p over the emitted bytes):

    random   independent uniform bytes
    skewed   independent bytes from a skewed distribution on a few values
    markov   text from an order-2 Markov source over a small alphabet
    runs     long runs of the same byte

It compresses each with zlib, bz2, lzma and an adaptive order-0 arithmetic
coder written here, checks that each output decodes to the input, and reports
the sizes. The order-0 coder models each byte by its count so far (all counts
start at 1) and codes with the integer arithmetic coder of Witten, Neal and
Cleary; it writes the length of the input in 4 bytes first.
"""

import bz2
import lzma
import math
import random
import zlib
from typing import Callable

CODE_BITS = 32
TOP = (1 << CODE_BITS) - 1
QTR = 1 << (CODE_BITS - 2)
HALF = 2 * QTR
MAX_TOTAL = 1 << 16


class _Order0:
    """Adaptive byte frequencies with a Fenwick tree for the cumulative counts."""

    def __init__(self) -> None:
        self.freq = [1] * 256
        self.tree = [0] * 257
        for s in range(256):
            self._add(s, 1)
        self.total = 256

    def _add(self, s: int, d: int) -> None:
        i = s + 1
        while i <= 256:
            self.tree[i] += d
            i += i & -i

    def cum(self, s: int) -> int:
        """The sum of the counts of the bytes below s."""
        total, i = 0, s
        while i > 0:
            total += self.tree[i]
            i -= i & -i
        return total

    def find(self, target: int) -> int:
        """The byte s with cum(s) <= target < cum(s + 1)."""
        pos, step = 0, 256
        while step:
            if pos + step <= 256 and self.tree[pos + step] <= target:
                pos += step
                target -= self.tree[pos]
            step >>= 1
        return pos

    def update(self, s: int) -> None:
        self.freq[s] += 1
        self._add(s, 1)
        self.total += 1
        if self.total >= MAX_TOTAL:
            self.tree = [0] * 257
            self.total = 0
            for t in range(256):
                self.freq[t] = (self.freq[t] + 1) // 2
                self._add(t, self.freq[t])
                self.total += self.freq[t]


def order0_compress(data: bytes) -> bytes:
    model = _Order0()
    low, high, pending = 0, TOP, 0
    bits: list[int] = []

    def emit(b: int) -> None:
        nonlocal pending
        bits.append(b)
        bits.extend([1 - b] * pending)
        pending = 0

    for s in data:
        r = high - low + 1
        lo = model.cum(s)
        hi = lo + model.freq[s]
        high = low + r * hi // model.total - 1
        low = low + r * lo // model.total
        while True:
            if high < HALF:
                emit(0)
            elif low >= HALF:
                emit(1)
                low -= HALF
                high -= HALF
            elif low >= QTR and high < HALF + QTR:
                pending += 1
                low -= QTR
                high -= QTR
            else:
                break
            low, high = 2 * low, 2 * high + 1
        model.update(s)
    pending += 1
    emit(0 if low < QTR else 1)
    bits += [0] * (-len(bits) % 8)
    body = bytes(int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))
    return len(data).to_bytes(4, "big") + body


def order0_decompress(code: bytes) -> bytes:
    n = int.from_bytes(code[:4], "big")
    body = code[4:]
    nbits = 8 * len(body)
    pos = 0

    def bit() -> int:
        nonlocal pos
        i = pos
        pos += 1
        return (body[i >> 3] >> (7 - (i & 7))) & 1 if i < nbits else 0

    model = _Order0()
    low, high, value = 0, TOP, 0
    for _ in range(CODE_BITS):
        value = 2 * value + bit()
    out = bytearray()
    for _ in range(n):
        r = high - low + 1
        target = ((value - low + 1) * model.total - 1) // r
        s = model.find(target)
        lo = model.cum(s)
        hi = lo + model.freq[s]
        high = low + r * hi // model.total - 1
        low = low + r * lo // model.total
        while True:
            if high < HALF:
                pass
            elif low >= HALF:
                low -= HALF
                high -= HALF
                value -= HALF
            elif low >= QTR and high < HALF + QTR:
                low -= QTR
                high -= QTR
                value -= QTR
            else:
                break
            low, high = 2 * low, 2 * high + 1
            value = 2 * value + bit()
        out.append(s)
        model.update(s)
    return bytes(out)


COMPRESSORS: dict[str, tuple[Callable[[bytes], bytes], Callable[[bytes], bytes]]] = {
    "zlib": (lambda d: zlib.compress(d, 9), zlib.decompress),
    "bz2": (lambda d: bz2.compress(d, 9), bz2.decompress),
    "lzma": (lambda d: lzma.compress(d, preset=9), lzma.decompress),
    "order0": (order0_compress, order0_decompress),
}


def gen_random(n: int, seed: int) -> tuple[bytes, float]:
    rng = random.Random(seed)
    return bytes(rng.randrange(256) for _ in range(n)), 8.0 * n


def gen_skewed(n: int, seed: int, probs: tuple[float, ...] = (0.6, 0.2, 0.1, 0.05, 0.05)) -> tuple[bytes, float]:
    rng = random.Random(seed)
    symbols = [ord(c) for c in "etaoi"[:len(probs)]]
    data = rng.choices(symbols, weights=probs, k=n)
    p = dict(zip(symbols, probs))
    return bytes(data), -sum(math.log2(p[s]) for s in data)


def gen_markov(n: int, seed: int, letters: str = "abcdefghijklmnop ") -> tuple[bytes, float]:
    """Order-2 Markov text: each pair of letters has three likely successors."""
    rng = random.Random(seed)
    m = len(letters)
    table = {}
    for a in range(m):
        for b in range(m):
            w = [0.02] * m
            for c, share in zip(rng.sample(range(m), 3), (8.0, 4.0, 2.0)):
                w[c] += share
            z = sum(w)
            table[(a, b)] = [x / z for x in w]
    seq = [0, 1]
    info = 2 * math.log2(m)
    while len(seq) < n:
        row = table[(seq[-2], seq[-1])]
        c = rng.choices(range(m), weights=row)[0]
        info -= math.log2(row[c])
        seq.append(c)
    return bytes(ord(letters[c]) for c in seq[:n]), info


def gen_runs(n: int, seed: int, mean_run: int = 200) -> tuple[bytes, float]:
    """Runs of a random byte from 16 values, with geometric run lengths of the given mean."""
    rng = random.Random(seed)
    stop = 1 / mean_run
    out = bytearray()
    info = 0.0
    s = rng.randrange(16)
    info += 4
    while len(out) < n:
        out.append(65 + s)
        if rng.random() < stop:
            s = rng.randrange(16)
            info += 4 - math.log2(stop)
        else:
            info -= math.log2(1 - stop)
    return bytes(out[:n]), info


GENERATORS = {"random": gen_random, "skewed": gen_skewed, "markov": gen_markov, "runs": gen_runs}


def entropy0(data: bytes) -> float:
    """n times the empirical order-0 entropy of data, in bits."""
    n = len(data)
    counts: dict[int, int] = {}
    for s in data:
        counts[s] = counts.get(s, 0) + 1
    return -sum(c * math.log2(c / n) for c in counts.values())


def run(data: bytes) -> dict[str, int]:
    """Compress data with every compressor, check the round trip, and return the sizes in bytes."""
    sizes = {}
    for name, (comp, decomp) in COMPRESSORS.items():
        code = comp(data)
        if decomp(code) != data:
            raise AssertionError(f"{name} failed the round trip")
        sizes[name] = len(code)
    return sizes


def report(n: int = 20000, seed: int = 1948) -> dict[str, dict[str, float]]:
    table = {}
    for kind, gen in GENERATORS.items():
        data, info = gen(n, seed)
        row: dict[str, float] = dict(run(data))
        row["source bits / 8"] = info / 8
        row["n H0 / 8"] = entropy0(data) / 8
        table[kind] = row
    return table


if __name__ == "__main__":
    for kind, row in report().items():
        print(kind, {k: round(v, 1) for k, v in row.items()})
