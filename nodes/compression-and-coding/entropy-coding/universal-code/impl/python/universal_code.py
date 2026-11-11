# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-code/. The authors are listed in prov/WKVPS7.jsonl.

"""A harness for Elias's definition of a universal code.

A code for the positive integers is universal if there is a constant K with
E_P[l] <= K * max(1, H(P)) for every distribution P with P(1) >= P(2) >= ...
and finite entropy H(P). It is asymptotically optimal if the ratio
E_P[l] / max(1, H(P)) is at most R(H(P)) for a function R with R(h) -> 1 as
h -> infinity.

The harness computes expected codeword lengths and entropies for decreasing
distributions on a finite support {1, ..., N} and reports the ratios. Two
evaluators are given: an exact one that sums over every x, and a block one for
distributions that are uniform on each dyadic block [2^j, 2^(j+1)), which can
reach supports of size 2^65536 for codes whose length depends only on
floor(log2 x).
"""

import math
from collections.abc import Callable, Sequence

LengthFn = Callable[[int], int]

# ---------------------------------------------------------------------------
# Codeword lengths for x >= 1.
# ---------------------------------------------------------------------------


def unary_length(x: int) -> int:
    return x


def gamma_length(x: int) -> int:
    return 2 * (x.bit_length() - 1) + 1


def delta_length(x: int) -> int:
    n = x.bit_length() - 1
    return n + 2 * ((n + 1).bit_length() - 1) + 1


def omega_length(x: int) -> int:
    total = 1
    while x > 1:
        n = x.bit_length() - 1
        total += n + 1
        x = n
    return total


def _fibonacci_upto(limit: int) -> list[int]:
    fib = [1, 2]
    while fib[-1] <= limit:
        fib.append(fib[-1] + fib[-2])
    return fib


_FIB = _fibonacci_upto(1 << 64)


def fibonacci_length(x: int) -> int:
    """The Fibonacci codeword of x has one bit per Fibonacci number up to the
    largest one <= x, plus the final 1."""
    while _FIB[-1] <= x:
        _FIB.append(_FIB[-1] + _FIB[-2])
    i = 0
    while _FIB[i + 1] <= x:
        i += 1
    return i + 2


def exp_golomb_length(k: int) -> LengthFn:
    """Order-k exp-Golomb on x - 1, so that it covers x >= 1."""

    def length(x: int) -> int:
        n = (x - 1 + (1 << k)).bit_length() - 1
        return 2 * n - k + 1

    return length


def vbyte_length(x: int) -> int:
    return 8 * max(1, -(-x.bit_length() // 7))


CODES: dict[str, LengthFn] = {
    "unary": unary_length,
    "gamma": gamma_length,
    "delta": delta_length,
    "omega": omega_length,
    "fibonacci": fibonacci_length,
    "expgolomb2": exp_golomb_length(2),
    "vbyte": vbyte_length,
}

# ---------------------------------------------------------------------------
# Decreasing distributions on {1, ..., N}. Index i of the list is x = i + 1.
# ---------------------------------------------------------------------------


def normalize(weights: Sequence[float]) -> list[float]:
    total = math.fsum(weights)
    return [w / total for w in weights]


def zipf(n: int) -> list[float]:
    return normalize([1.0 / x for x in range(1, n + 1)])


def power_law(s: float, n: int) -> list[float]:
    return normalize([x ** (-s) for x in range(1, n + 1)])


def geometric(theta: float, n: int) -> list[float]:
    return normalize([theta ** (x - 1) for x in range(1, n + 1)])


def uniform(n: int) -> list[float]:
    return [1.0 / n] * n


def is_decreasing(p: Sequence[float]) -> bool:
    return all(p[i] >= p[i + 1] for i in range(len(p) - 1))


def entropy(p: Sequence[float]) -> float:
    return math.fsum(-q * math.log2(q) for q in p if q > 0)


def expected_length(p: Sequence[float], length: LengthFn) -> float:
    return math.fsum(q * length(i + 1) for i, q in enumerate(p) if q > 0)


def ratio(p: Sequence[float], length: LengthFn) -> float:
    """E_P[l] / max(1, H(P)), the quantity in Elias's definition."""
    return expected_length(p, length) / max(1.0, entropy(p))


# ---------------------------------------------------------------------------
# Block evaluator: P is uniform on each block [2^j, 2^(j+1)), with mass w[j].
# ---------------------------------------------------------------------------


def block_is_decreasing(w: Sequence[float]) -> bool:
    """The per-element probability w[j] / 2^j must not increase with j."""
    return all(w[j + 1] <= 2 * w[j] for j in range(len(w) - 1))


def block_entropy(w: Sequence[float]) -> float:
    return math.fsum(m * (j - math.log2(m)) for j, m in enumerate(w) if m > 0)


def block_expected_length(w: Sequence[float], length: LengthFn) -> float:
    """Valid for a length that depends only on floor(log2 x)."""
    return math.fsum(m * length(1 << j) for j, m in enumerate(w) if m > 0)


def block_ratio(w: Sequence[float], length: LengthFn) -> float:
    return block_expected_length(w, length) / max(1.0, block_entropy(w))


def block_uniform(levels: int) -> list[float]:
    """The uniform law on {1, ..., 2^levels - 1}, as block masses."""
    scale = 1.0 - math.ldexp(1.0, -levels)
    return [math.ldexp(1.0, j - levels) / scale for j in range(levels)]


def block_power_law(s: float, levels: int) -> list[float]:
    """Per-element probability proportional to 2^(-j s) on block j."""
    return normalize([2.0 ** (j * (1 - s)) for j in range(levels)])


def report(dists: dict[str, list[float]], codes: dict[str, LengthFn]) -> list[tuple[str, float, dict[str, float]]]:
    rows = []
    for name, p in dists.items():
        rows.append((name, entropy(p), {c: ratio(p, f) for c, f in codes.items()}))
    return rows


if __name__ == "__main__":
    n = 1 << 16
    dists = {
        "geometric 0.5": geometric(0.5, n),
        "geometric 0.99": geometric(0.99, n),
        "zipf 2^16": zipf(n),
        "power law s=2": power_law(2.0, n),
        "uniform 2^16": uniform(n),
    }
    for name, h, r in report(dists, CODES):
        print(f"{name:16} H={h:7.3f} " + " ".join(f"{c}={v:.3f}" for c, v in r.items()))
    for levels in (16, 256, 4096, 65536):
        w = block_uniform(levels)
        print(levels, {c: round(block_ratio(w, CODES[c]), 4) for c in ("gamma", "delta", "omega", "vbyte")})
