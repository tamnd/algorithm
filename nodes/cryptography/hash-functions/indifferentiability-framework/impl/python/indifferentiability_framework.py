# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/indifferentiability-framework/. The authors are listed in prov/C3GSSY.jsonl.
"""A toy indifferentiability experiment: the length-extension distinguisher against plain
Merkle-Damgard, and its failure against chop-MD and NMAC.

For study only. The random functions are lazily sampled from Python's random
module, which is not a cryptographic generator. Nothing here is a hash for real
data; use SHA-256, SHA-512/256 or SHA-3 from hashlib instead.

A message is a list of 32-bit blocks. The padding appends one block holding the
number of message blocks (MD strengthening on whole blocks). The compression
function f maps a 32-bit chaining value and a 32-bit block to 32 bits.
"""

import random

N = 32
MASK = (1 << N) - 1
IV = 0


class LazyRandomFunction:
    """A random function, sampled one point at a time and remembered."""

    def __init__(self, seed: int, out_bits: int = N) -> None:
        self.rng = random.Random(seed)
        self.table: dict = {}
        self.out_bits = out_bits

    def __call__(self, *x):
        if x not in self.table:
            self.table[x] = self.rng.getrandbits(self.out_bits)
        return self.table[x]


def pad(blocks: list[int]) -> list[int]:
    return list(blocks) + [len(blocks)]


def md(f, blocks: list[int]) -> int:
    h = IV
    for m in pad(blocks):
        h = f(h, m)
    return h


def chop_md(f, blocks: list[int], s: int) -> int:
    """chop-MD: drop the low s bits of the MD output."""
    return md(f, blocks) >> s


def nmac(f, g, blocks: list[int]) -> int:
    """NMAC-style: an independent function g applied to the MD output."""
    return g(md(f, blocks))


class NaiveSimulator:
    """A simulator for f in the ideal world. It answers with fresh random values; it cannot see
    which messages the distinguisher sent to the random oracle."""

    def __init__(self, ro, seed: int) -> None:
        self.ro = ro
        self.f = LazyRandomFunction(seed)

    def __call__(self, h: int, m: int) -> int:
        return self.f(h, m)


def length_extension_distinguisher(left, right, rng: random.Random) -> int:
    """D: output 1 if the left oracle behaves like plain MD over the right oracle.
    left(blocks) is H or the random oracle; right(h, m) is f or the simulator."""
    m1 = rng.getrandbits(N)  # @line L1
    s = rng.getrandbits(N)  # @line L2
    y = left([m1])  # @line L3
    z = right(right(y, s), 3)  # @line L4
    return int(left([m1, 1, s]) == z)  # @line L5


def chop_extension_attempt(f, s_bits: int, rng: random.Random) -> int:
    """The same attack on chop-MD in the real world: D must guess the s_bits dropped bits."""
    m1, s = rng.getrandbits(N), rng.getrandbits(N)
    y = chop_md(f, [m1], s_bits)
    guess = (y << s_bits) | rng.getrandbits(s_bits)
    z = f(f(guess, s), 3) >> s_bits
    return int(chop_md(f, [m1, 1, s], s_bits) == z)


def advantage(trials: int, seed: int = 1) -> tuple[float, float]:
    """Pr[D = 1] in the real world (MD^f, f) and in the ideal world (RO, S^RO)."""
    rng = random.Random(seed)
    real = ideal = 0
    for t in range(trials):
        f = LazyRandomFunction(10_000 + t)
        real += length_extension_distinguisher(lambda b: md(f, b), f, rng)
        ro = LazyRandomFunction(20_000 + t)
        sim = NaiveSimulator(ro, 30_000 + t)
        ideal += length_extension_distinguisher(lambda b: ro(tuple(b)), sim, rng)
    return real / trials, ideal / trials
