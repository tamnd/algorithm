# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shannon-fano-coding/. The authors are listed in prov/M37AW1.jsonl.

"""Shannon-Fano coding, in its two historical forms.

fano_code: Fano (1949). Sort the symbols by non-increasing weight, split
the list into two parts of nearly equal weight, give 0 to the first part
and 1 to the second, and repeat inside each part.

shannon_code: Shannon (1948). Sort the symbols by non-increasing
probability; symbol s gets length ceil(log2(1/p_s)) and, as its
codeword, that many bits of the binary expansion of the sum of the
probabilities before it.
"""

from fractions import Fraction
from typing import Sequence


def fano_code(weights: Sequence[int]) -> list[str]:
    """Codewords of Fano's method; ties in the split go to the first,
    that is the smallest, split point."""
    n = len(weights)
    if n == 0:
        raise ValueError("need at least one symbol")
    if n == 1:
        return ["0"]
    order = sorted(range(n), key=lambda i: -weights[i])
    words = [""] * n
    stack = [(0, n, "")]  # a sublist order[lo:hi] and its prefix
    while stack:
        lo, hi, prefix = stack.pop()
        if hi - lo == 1:  # @line L1
            words[order[lo]] = prefix
            continue
        total = sum(weights[order[j]] for j in range(lo, hi))  # @line L2
        best_k, best_diff, left = lo + 1, None, 0
        for k in range(lo + 1, hi):  # @line L3  first k symbols go left
            left += weights[order[k - 1]]
            diff = abs(2 * left - total)
            if best_diff is None or diff < best_diff:
                best_k, best_diff = k, diff
        stack.append((best_k, hi, prefix + "1"))  # @line L5
        stack.append((lo, best_k, prefix + "0"))  # @line L4
    return words


def shannon_code(probs: Sequence[Fraction]) -> list[str]:
    """Codewords of Shannon's method. The probabilities must be positive
    and sum to 1; use Fractions to keep the arithmetic exact."""
    n = len(probs)
    if any(p <= 0 for p in probs) or sum(probs) != 1:
        raise ValueError("probabilities must be positive and sum to 1")
    order = sorted(range(n), key=lambda i: -probs[i])
    words = [""] * n
    cum = Fraction(0)
    for i in order:
        p = probs[i]
        m = 0
        while Fraction(1, 2**m) > p:  # m = ceil(log2(1/p)), exactly
            m += 1
        if m == 0:
            m = 1  # a single symbol of probability 1 still needs a bit
        x = cum
        bits = []
        for _ in range(m):  # the first m bits of the binary expansion of cum
            x *= 2
            bit = int(x >= 1)
            bits.append("1" if bit else "0")
            x -= bit
        words[i] = "".join(bits)
        cum += p
    return words


def cost(weights: Sequence, words: Sequence[str]):
    return sum(w * len(c) for w, c in zip(weights, words))


def is_prefix_free(words: Sequence[str]) -> bool:
    s = sorted(words)
    return all(not b.startswith(a) for a, b in zip(s, s[1:]))
