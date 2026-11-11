# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tunstall-coding/. The authors are listed in prov/D6TXZ9.jsonl.

"""Tunstall coding (1967), a variable-to-fixed code for a memoryless source.

The dictionary is grown as a tree: start with the sigma one-symbol words
and, while one more split still fits in 2^B words, replace the most
probable word by its sigma one-symbol extensions. The words are the
leaves of a complete tree, so every long enough string starts with
exactly one of them. The encoder parses the input into dictionary words
and sends each as a B-bit index.

Symbols are integers 0..sigma-1; probabilities are Fractions, so the
expected parse length is exact.
"""

import heapq
from fractions import Fraction
from typing import Sequence

Word = tuple[int, ...]


def word_prob(probs: Sequence[Fraction], word: Word) -> Fraction:
    p = Fraction(1)
    for s in word:
        p *= probs[s]
    return p


def build_dictionary(probs: Sequence[Fraction], bits: int) -> list[Word]:
    """The Tunstall dictionary for B = bits, sorted; index i is word i.

    Ties between equally probable words go to the lexicographically
    smallest word."""
    sigma = len(probs)
    if sigma < 2 or any(p <= 0 for p in probs) or sum(probs) != 1:
        raise ValueError("need two or more positive probabilities that sum to 1")
    if sigma > 2**bits:
        raise ValueError("2^B must be at least the alphabet size")
    heap = [(-probs[s], (s,)) for s in range(sigma)]  # @line L1
    heapq.heapify(heap)
    while len(heap) + sigma - 1 <= 2**bits:  # @line L2
        neg_p, word = heapq.heappop(heap)  # @line L3
        for s in range(sigma):  # @line L4
            heapq.heappush(heap, (neg_p * probs[s], word + (s,)))
    return sorted(word for _, word in heap)  # @line L5


def expected_parse_length(probs: Sequence[Fraction], words: Sequence[Word]) -> Fraction:
    """Sum over the words of p(word) * len(word)."""
    return sum((word_prob(probs, w) * len(w) for w in words), Fraction(0))


def inner_node_sum(probs: Sequence[Fraction], words: Sequence[Word]) -> Fraction:
    """Sum of the probabilities of the inner nodes, the root included."""
    inner = {w[:k] for w in words for k in range(len(w))}
    return sum((word_prob(probs, u) for u in inner), Fraction(0))


def encode(message: Sequence[int], words: Sequence[Word], sigma: int) -> list[int]:
    """Parse the message into dictionary words and return their indices.

    The last, incomplete word is completed with the symbol 0, so the
    decoder must also be told the message length."""
    index = {w: i for i, w in enumerate(words)}
    out, cur = [], ()
    for s in message:
        cur += (s,)
        if cur in index:
            out.append(index[cur])
            cur = ()
    if cur:
        while cur not in index:
            cur += (0,)
        out.append(index[cur])
    return out


def decode(indices: Sequence[int], words: Sequence[Word], length: int) -> list[int]:
    out: list[int] = []
    for i in indices:
        out.extend(words[i])
    return out[:length]
