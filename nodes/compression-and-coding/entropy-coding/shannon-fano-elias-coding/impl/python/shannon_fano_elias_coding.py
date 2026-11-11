# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shannon-fano-elias-coding/. The authors are listed in prov/C2GA8M.jsonl.

"""Shannon-Fano-Elias coding with exact rational arithmetic.

sfe_code gives each symbol, in the given order and without sorting, the
first ceil(log2(1/p)) + 1 bits of the midpoint F + p/2 of its interval
[F, F + p), where F is the sum of the probabilities before it.

sfe_block_encode and sfe_block_decode apply the same rule to a whole
block of symbols from a memoryless source. The interval of the block is
found symbol by symbol, which is the core of arithmetic coding.
"""

from fractions import Fraction
from typing import Sequence


def ceil_log2_inv(p: Fraction) -> int:
    """ceil(log2(1/p)) for 0 < p <= 1, computed exactly."""
    m = 0
    while Fraction(1, 2**m) > p:
        m += 1
    return m


def first_bits(x: Fraction, m: int) -> str:
    """The first m bits after the binary point of 0 <= x < 1."""
    bits = []
    for _ in range(m):
        x *= 2
        bit = int(x >= 1)
        bits.append("1" if bit else "0")
        x -= bit
    return "".join(bits)


def _check(probs: Sequence[Fraction]) -> None:
    if not probs or any(p <= 0 for p in probs) or sum(probs) != 1:
        raise ValueError("probabilities must be positive and sum to 1")


def sfe_code(probs: Sequence[Fraction]) -> list[str]:
    """Codewords of Shannon-Fano-Elias coding, in the given symbol order."""
    _check(probs)
    words = []
    f = Fraction(0)  # @line L1
    for p in probs:  # @line L2
        mid = f + p / 2  # @line L3
        length = ceil_log2_inv(p) + 1  # @line L4
        words.append(first_bits(mid, length))  # @line L5
        f += p  # @line L6
    return words


def block_interval(probs: Sequence[Fraction], block: Sequence[int]) -> tuple[Fraction, Fraction]:
    """The interval [low, low + width) of a block, in lexicographic order of blocks."""
    cum = [Fraction(0)]
    for p in probs:
        cum.append(cum[-1] + p)
    low, width = Fraction(0), Fraction(1)
    for s in block:
        low += width * cum[s]
        width *= probs[s]
    return low, width


def sfe_block_encode(probs: Sequence[Fraction], block: Sequence[int]) -> str:
    """The Shannon-Fano-Elias codeword of a block of symbol indices."""
    _check(probs)
    low, width = block_interval(probs, block)
    return first_bits(low + width / 2, ceil_log2_inv(width) + 1)


def sfe_block_decode(probs: Sequence[Fraction], word: str, k: int) -> list[int]:
    """Recover a block of k symbols from its codeword."""
    _check(probs)
    v = Fraction(int(word, 2), 2 ** len(word)) if word else Fraction(0)
    out = []
    low, width = Fraction(0), Fraction(1)
    for _ in range(k):
        f = low
        for s, p in enumerate(probs):
            if v < f + width * p:
                out.append(s)
                low, width = f, width * p
                break
            f += width * p
        else:
            raise ValueError("codeword out of range")
    return out


def is_prefix_free(words: Sequence[str]) -> bool:
    s = sorted(words)
    return all(not b.startswith(a) for a, b in zip(s, s[1:]))
