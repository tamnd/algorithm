# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simple-9/. The authors are listed in prov/QCGBFK.jsonl.

# The nine layouts of a 32-bit word: selector s gives COUNT[s] values of WIDTH[s] bits.
COUNT = (28, 14, 9, 7, 5, 4, 3, 2, 1)
WIDTH = (1, 2, 3, 4, 5, 7, 9, 14, 28)
LIMIT = 1 << 28


def fits(x: list[int], i: int, k: int, w: int) -> bool:
    """True when x[i], ..., x[i + k - 1] are all below 2^w."""
    bound = 1 << w
    for j in range(i, i + k):
        if x[j] >= bound:
            return False
    return True


def encode(x: list[int]) -> list[int]:
    """Simple-9 encoding of a list of integers, each in [0, 2^28).

    Each output word is a 32-bit unsigned integer: a 4-bit selector in the top
    bits and up to 28 data bits. The greedy rule takes, at each word, the first
    selector (the one with the most values) whose values all fit. The last word
    may be partly filled, so the decoder needs len(x). Cost O(9 * 28) per word,
    O(n) for n values.
    """
    for v in x:
        if v < 0 or v >= LIMIT:
            raise ValueError("Simple-9 codes integers in [0, 2^28)")
    out: list[int] = []  # @line L1
    i, n = 0, len(x)
    while i < n:  # @line L2
        for s in range(9):  # @line L3
            k = min(COUNT[s], n - i)  # @line L4
            if fits(x, i, k, WIDTH[s]):  # @line L5
                break
        word = s << 28  # @line L6
        for j in range(k):  # @line L7
            word |= x[i + j] << (j * WIDTH[s])
        out.append(word)  # @line L8
        i += k
    return out  # @line L9


def decode(words: list[int], n: int) -> list[int]:
    """Decode n integers from Simple-9 words. Cost O(n + len(words))."""
    x: list[int] = []  # @line L10
    for word in words:  # @line L11
        s = word >> 28  # @line L12
        if s > 8:
            raise ValueError("selector out of range")
        w, mask = WIDTH[s], (1 << WIDTH[s]) - 1
        for j in range(COUNT[s]):  # @line L13
            if len(x) == n:
                break
            x.append((word >> (j * w)) & mask)
    if len(x) != n:
        raise ValueError("the words hold fewer than n integers")
    return x  # @line L14


def bits(words: list[int]) -> int:
    """The size of an encoding in bits: 32 for each word."""
    return 32 * len(words)


def optimal_word_count(x: list[int]) -> int:
    """The least number of Simple-9 words for x over all ways to split it.

    Dynamic programming over suffixes, for comparison with the greedy rule.
    Cost O(9 * 28 * n).
    """
    n = len(x)
    best = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        m = n + 1
        for s in range(9):
            k = min(COUNT[s], n - i)
            if fits(x, i, k, WIDTH[s]):
                m = min(m, 1 + best[i + k])
        best[i] = m
    return best[0]
