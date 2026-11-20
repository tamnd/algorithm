# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constant-composition-distribution-matching/. The authors are listed in prov/EKQBW6.jsonl.

"""Constant composition distribution matching (CCDM) with exact integer arithmetic.

The output alphabet is a list of distinct symbols in a fixed order, and the
composition c gives how often each symbol appears in every output word of
length n = sum(c). The set of such words has T = n! / prod(c_s!) elements,
and the matcher maps k = floor(log2 T) input bits to one of them.

Encoder: the input bits, most significant first, form the integer v, and the
output is the word of lexicographic rank r = ceil(v T / 2^k) among all words
of the composition. Decoder: rank the word to get r, then v = floor(r 2^k / T).
This is the codebook of the arithmetic coder of Schulte and Boecherer (2016)
with infinite precision.
"""

import math


def multinomial(c: list[int]) -> int:
    """The number n! / prod(c_s!) of words with the composition c."""
    total, n = 1, 0
    for cs in c:
        if cs < 0:
            raise ValueError("counts must be nonnegative")
        for t in range(1, cs + 1):
            n += 1
            total = total * n // t
    return total


def num_bits(c: list[int]) -> int:
    """k = floor(log2 T), the number of input bits per word."""
    return multinomial(c).bit_length() - 1


def unrank(r: int, c: list[int], symbols: list) -> list:
    """The word of lexicographic rank r (0 <= r < T) among all words of the composition c."""
    c = list(c)
    n = sum(c)
    big_n = multinomial(c)
    if not 0 <= r < big_n:
        raise ValueError("rank out of range")
    out = []
    for ell in range(n, 0, -1):  # @line L5
        for s in range(len(c)):  # @line L6
            if c[s] == 0:
                continue
            ns = big_n * c[s] // ell  # @line L7
            if r < ns:  # @line L8
                out.append(symbols[s])
                c[s] -= 1
                big_n = ns
                break
            r -= ns  # @line L9
    return out  # @line L10


def rank(word: list, c: list[int], symbols: list) -> int:
    """The lexicographic rank of word among all words of the composition c."""
    c = list(c)
    if len(word) != sum(c):
        raise ValueError("the word has the wrong length")
    index = {a: s for s, a in enumerate(symbols)}
    big_n = multinomial(c)
    r = 0  # @line L11
    ell = len(word)
    for a in word:  # @line L12
        x = index[a]
        if c[x] == 0:
            raise ValueError("the word does not have the composition c")
        for s in range(x):  # @line L13
            r += big_n * c[s] // ell
        big_n = big_n * c[x] // ell  # @line L14
        c[x] -= 1
        ell -= 1
    return r


def encode(bits: list[int], c: list[int], symbols: list) -> list:
    """Map k = floor(log2 T) bits (most significant first) to a word of composition c."""
    big_t = multinomial(c)  # @line L1
    k = big_t.bit_length() - 1
    if len(bits) != k:
        raise ValueError("the encoder needs exactly k bits")
    v = 0
    for b in bits:  # @line L2
        if b not in (0, 1):
            raise ValueError("bits must be 0 or 1")
        v = 2 * v + b
    r = -((-v * big_t) >> k)  # @line L3
    return unrank(r, c, symbols)  # @line L4


def decode(word: list, c: list[int], symbols: list) -> list[int]:
    """Recover the k input bits from a word that encode produced."""
    big_t = multinomial(c)
    k = big_t.bit_length() - 1
    v = (rank(word, c, symbols) << k) // big_t  # @line L15
    return [(v >> (k - 1 - t)) & 1 for t in range(k)]


def composition(probs: list[float], n: int) -> list[int]:
    """The counts c (sum n) whose type c/n has the smallest divergence D(c/n || P) from P.

    D is separable and convex in each count, so adding one unit at a time to the
    symbol with the smallest increase of n D is optimal. Ties go to the lower index.
    Symbols with probability 0 get count 0.
    """
    if n < 1 or any(p < 0 for p in probs) or not math.isclose(sum(probs), 1.0, rel_tol=0, abs_tol=1e-9):
        raise ValueError("need n >= 1 and a probability vector")
    c = [0] * len(probs)

    def f(cs: int, p: float) -> float:
        return 0.0 if cs == 0 else cs * math.log(cs / (n * p))

    for _ in range(n):
        best, arg = math.inf, -1
        for s, p in enumerate(probs):
            if p == 0:
                continue
            inc = f(c[s] + 1, p) - f(c[s], p)
            if inc < best - 1e-12:
                best, arg = inc, s
        c[arg] += 1
    return c


def rate(c: list[int]) -> float:
    """The rate k / n in input bits per output symbol."""
    return num_bits(c) / sum(c)
