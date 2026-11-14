# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/factorial-design/. The authors are listed in prov/NCP43N.jsonl.
"""Two-level full factorial designs 2^k and Yates's algorithm.

Runs are in standard order: run x = 0, ..., 2^k - 1 sets factor i (A = 0, B = 1, ...)
to its high level when bit i of x is 1, so the order is (1), a, b, ab, c, ac, bc, abc, ...
The contrast of the effect with factor set S (bit mask s) is sum_x y_x prod_{i in S} (+1 if
bit i of x is set, else -1). Yates's algorithm computes all 2^k contrasts in k passes:
each pass writes the sums of consecutive pairs into the first half and the differences
(second minus first) into the second half. It is a fast Walsh-Hadamard transform, so it
costs k 2^k additions instead of the 4^k of the direct sums.
"""

from string import ascii_uppercase


def runs(k: int) -> list[tuple[int, ...]]:
    """The 2^k runs in standard order, as tuples of -1 / +1 levels for A, B, ..."""
    return [tuple(1 if (x >> i) & 1 else -1 for i in range(k)) for x in range(2 ** k)]


def effect_name(s: int) -> str:
    """The label of the effect with bit mask s: 0 -> I, 1 -> A, 3 -> AB, 5 -> AC."""
    return "".join(ascii_uppercase[i] for i in range(s.bit_length()) if (s >> i) & 1) or "I"


def yates(y: list[float]) -> list[float]:
    """All 2^k contrasts of responses y in standard order, in effect order I, A, B, AB, C, ..."""
    n = len(y)
    k = n.bit_length() - 1
    if n == 0 or n != 1 << k:
        raise ValueError("the number of runs must be a power of two")
    col = list(y)  # @line L1
    for _ in range(k):  # @line L2
        half = n // 2
        sums = [col[2 * i] + col[2 * i + 1] for i in range(half)]  # @line L3
        diffs = [col[2 * i + 1] - col[2 * i] for i in range(half)]  # @line L4
        col = sums + diffs  # @line L5
    return col  # @line L6


def contrasts_direct(y: list[float]) -> list[float]:
    """The same contrasts by their definition, 4^k operations: the reference for tests."""
    n = len(y)
    out = []
    for s in range(n):
        total = 0
        for x, v in enumerate(y):
            sign = 1
            for i in range(n.bit_length() - 1):
                if (s >> i) & 1:
                    sign *= 1 if (x >> i) & 1 else -1
            total += sign * v
        out.append(total)
    return out


def effects(y: list[float]) -> dict[str, float]:
    """Effect estimates: contrast / (N / 2) for each effect, and the grand mean for I."""
    n = len(y)
    c = yates(y)
    return {effect_name(s): (c[s] / n if s == 0 else 2.0 * c[s] / n) for s in range(n)}
