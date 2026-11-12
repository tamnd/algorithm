# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spaced-seed/. The authors are listed in prov/0TDJNQ.jsonl.

"""Spaced seeds: hits, and the exact hit probability on a random region.

A seed is a string over {1, 0} that starts and ends with 1. Its weight is
the number of 1s and its span is its length. A seed hits a 0/1 string r
(1 = the two sequences match at this column) at offset i when r[i + t] = 1
for each t with seed[t] = 1.
"""

import itertools
from typing import Iterator


PATTERNHUNTER = "111010010100110111"


def check_seed(seed: str) -> None:
    if not seed or set(seed) - {"0", "1"} or seed[0] != "1" or seed[-1] != "1":
        raise ValueError("a seed is a 0/1 string that starts and ends with 1")


def weight(seed: str) -> int:
    return seed.count("1")


def hits(seed: str, region: str) -> list[int]:
    """Offsets where the seed hits a 0/1 region string."""
    check_seed(seed)
    care = [t for t, c in enumerate(seed) if c == "1"]
    return [i for i in range(len(region) - len(seed) + 1) if all(region[i + t] == "1" for t in care)]


def hit_probability(seed: str, length: int, p: float) -> float:
    """Probability that the seed hits a region of the given length whose
    columns are independent and match with probability p.

    The state is a bit mask of the live placements: bit t is set when a
    placement started t columns ago and has matched every care position so
    far. Each column adds a placement at t = 0, keeps a placement whose next
    seed position is a match or a don't-care, and shifts. A placement that
    reaches t = span is a hit; its probability mass leaves the DP.
    """
    check_seed(seed)
    span = len(seed)
    zero = 0  # bit t set when seed[t] == "0"
    for t, c in enumerate(seed):
        if c == "0":
            zero |= 1 << t
    full = 1 << span
    states: dict[int, float] = {0: 1.0}
    hit = 0.0
    for _ in range(length):
        nxt: dict[int, float] = {}
        for mask, pr in states.items():
            live = mask | 1
            for keep, q in ((live, p), (live & zero, 1.0 - p)):
                new = keep << 1
                if new & full:
                    hit += pr * q
                    continue
                nxt[new] = nxt.get(new, 0.0) + pr * q
        states = nxt
    return hit


def hit_probability_brute(seed: str, length: int, p: float) -> float:
    """Sum over all 2^length regions; for tests on short regions."""
    total = 0.0
    for bits in itertools.product("01", repeat=length):
        r = "".join(bits)
        if hits(seed, r):
            ones = r.count("1")
            total += p**ones * (1.0 - p) ** (length - ones)
    return total


def expected_hits(seed: str, length: int, p: float) -> float:
    """(length - span + 1) p^weight: the same for each seed of one weight and span."""
    return max(0, length - len(seed) + 1) * p ** weight(seed)


def spaced_words(s: str, seed: str) -> Iterator[tuple[str, int]]:
    """The spaced words of s: the letters at the care positions, with their offsets."""
    check_seed(seed)
    care = [t for t, c in enumerate(seed) if c == "1"]
    for i in range(len(s) - len(seed) + 1):
        yield "".join(s[i + t] for t in care), i


def seed_hit_pairs(x: str, y: str, seed: str) -> list[tuple[int, int]]:
    """All pairs (i, j) where the seed placed at x[i] and y[j] sees equal
    letters at every care position, found with a hash table of the spaced
    words of x."""
    table: dict[str, list[int]] = {}
    for w, i in spaced_words(x, seed):
        table.setdefault(w, []).append(i)
    out = []
    for w, j in spaced_words(y, seed):
        for i in table.get(w, ()):
            out.append((i, j))
    return sorted(out)
