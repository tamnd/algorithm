# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/occams-razor/. The authors are listed in prov/XZEN4M.jsonl.
"""An Occam algorithm for conjunctions: greedy set cover, a prefix-free code and the Occam bound.

A literal is an index j in 0..2d-1: variable j // 2, negated when j is odd. A conjunction is a sorted
tuple of literals; the empty tuple is the constant 1. The learner keeps only literals that are true on
every positive example and then picks, greedily, literals that are false on the most negative examples
not yet excluded. If some conjunction of k literals fits the sample, the greedy choice has at most
k (ln m + 1) literals, where m is the number of negative examples (the set cover bound).
"""

import math
import random
from itertools import product

Conj = tuple[int, ...]
Example = tuple[tuple[int, ...], int]


def literal_value(j: int, x: tuple[int, ...]) -> int:
    v = x[j // 2]
    return 1 - v if j % 2 else v


def predict(h: Conj, x: tuple[int, ...]) -> int:
    return int(all(literal_value(j, x) for j in h))


def greedy_occam(sample: list[Example], d: int) -> Conj:
    """A short conjunction consistent with the sample. Raises ValueError if no conjunction is consistent."""
    pos = [x for x, y in sample if y == 1]
    neg = [x for x, y in sample if y == 0]
    cand = [j for j in range(2 * d) if all(literal_value(j, x) for x in pos)]
    left = list(range(len(neg)))
    chosen: list[int] = []
    while left:
        best, gain = -1, 0
        for j in cand:
            g = sum(1 for i in left if not literal_value(j, neg[i]))
            if g > gain:
                best, gain = j, g
        if best < 0:
            raise ValueError("no conjunction is consistent with the sample")
        chosen.append(best)
        left = [i for i in left if literal_value(best, neg[i])]
    return tuple(sorted(chosen))


def gamma_code(n: int) -> str:
    """Elias gamma code of n >= 1: floor(log2 n) zeros, then n in binary."""
    b = bin(n)[2:]
    return "0" * (len(b) - 1) + b


def literal_bits(d: int) -> int:
    return (2 * d - 1).bit_length()


def encode(h: Conj, d: int) -> str:
    """The gamma code of s + 1 (s = number of literals), then each literal in literal_bits(d) bits."""
    w = literal_bits(d)
    return gamma_code(len(h) + 1) + "".join(format(j, f"0{w}b") for j in h)


def decode(bits: str, d: int) -> tuple[Conj, str]:
    """Read one hypothesis from the front of a bit string; return it and the rest of the string."""
    z = 0
    while bits[z] == "0":
        z += 1
    s = int(bits[z:2 * z + 1], 2) - 1
    rest = bits[2 * z + 1:]
    w = literal_bits(d)
    lits = tuple(int(rest[i * w:(i + 1) * w], 2) for i in range(s))
    return lits, rest[s * w:]


def description_length(h: Conj, d: int) -> int:
    return len(encode(h, d))


def occam_bound(bits: int, n: int, delta: float) -> float:
    """With probability at least 1 - delta, every consistent h has true error at most this value."""
    return (bits * math.log(2) + math.log(1 / delta)) / n


def sample_size(bits: int, eps: float, delta: float) -> int:
    """n >= (|h| ln 2 + ln(1/delta)) / eps examples suffice for a consistent h of |h| bits."""
    return math.ceil((bits * math.log(2) + math.log(1 / delta)) / eps)


def true_error(h: Conj, target: Conj, d: int) -> float:
    """Exact error under the uniform distribution on {0, 1}^d, by enumeration."""
    bad = sum(predict(h, x) != predict(target, x) for x in product((0, 1), repeat=d))
    return bad / 2 ** d


def draw(target: Conj, d: int, n: int, rng: random.Random) -> list[Example]:
    out = []
    for _ in range(n):
        x = tuple(rng.getrandbits(1) for _ in range(d))
        out.append((x, predict(target, x)))
    return out


def random_target(d: int, k: int, rng: random.Random) -> Conj:
    vs = rng.sample(range(d), k)
    return tuple(sorted(2 * v + rng.getrandbits(1) for v in vs))


if __name__ == "__main__":
    d, delta = 12, 0.05
    target = (0, 7, 12, 17)  # x0 and (not x3) and x6 and (not x8)
    rng = random.Random(1)
    for n in (10, 20, 40, 80, 160, 320):
        s = draw(target, d, n, rng)
        h = greedy_occam(s, d)
        bits = description_length(h, d)
        negs = sum(1 for _, y in s if y == 0)
        print(n, negs, h, len(h), bits, round(occam_bound(bits, n, delta), 4), true_error(h, target, d))
