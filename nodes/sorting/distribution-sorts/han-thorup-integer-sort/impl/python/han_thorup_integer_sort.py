# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/han-thorup-integer-sort/. The authors are listed in prov/B8DZ6B.jsonl.
import random
from bisect import bisect_left
from math import isqrt


def _insertion_sort(a: list[int]) -> list[int]:
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
    return a


def han_thorup_integer_sort(a: list[int], base: int = 8, seed: int | None = None) -> list[int]:
    """Return the integers of a in non-decreasing order.

    Precondition: a holds integers (any sign) and base >= 2. This is a model of
    the structure of the Han and Thorup algorithm: split the keys into ordered
    parts by a random sample of about sqrt(n) splitters, check that no part is
    too large, and recurse. The paper splits with signature sort and packed
    words in O(n sqrt(log log n)) expected time in total. Here each key is
    placed by binary search, so the expected time is O(n log n), and the extra
    space is O(n). The output does not depend on the seed.
    """
    if base < 2:
        raise ValueError("base must be at least 2")
    return _sort(list(a), base, random.Random(seed))


def _split(a: list[int], splitters: list[int]) -> tuple[list[list[int]], list[int]]:
    s = len(splitters)
    parts: list[list[int]] = [[] for _ in range(s + 1)]
    equal = [0] * s
    for x in a:
        j = bisect_left(splitters, x)
        if j < s and splitters[j] == x:
            equal[j] += 1
        else:
            parts[j].append(x)
    return parts, equal


def _sort(a: list[int], base: int, rng: random.Random) -> list[int]:
    n = len(a)
    if n <= base:  # @line L1
        return _insertion_sort(a)
    k = isqrt(n - 1) + 1  # @line L2
    for attempt in range(4):
        sample = [a[rng.randrange(n)] for _ in range(k)]  # @line L3
        p = _sort(sample, base, rng)  # @line L4
        splitters = [x for i, x in enumerate(p) if i == 0 or x != p[i - 1]]
        parts, equal = _split(a, splitters)  # @line L5
        if max(len(q) for q in parts) <= n // 2 or attempt == 3:  # @line L6
            break
    out: list[int] = []
    for j in range(len(parts)):  # @line L7
        out.extend(_sort(parts[j], base, rng))
        if j < len(equal):
            out.extend([splitters[j]] * equal[j])
    return out  # @line L8
