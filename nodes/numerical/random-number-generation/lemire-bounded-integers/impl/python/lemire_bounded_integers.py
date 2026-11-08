# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lemire-bounded-integers/. The authors are listed in prov/N47W7S.jsonl.

"""Lemire's nearly divisionless method for uniform integers in [0, s) from w-bit words."""

from typing import Callable, Dict, Iterator, List, Tuple


def lemire_bounded(s: int, random_word: Callable[[], int], w: int = 64) -> int:
    """A uniform integer in [0, s), for 1 <= s <= 2^w, from uniform w-bit words."""
    return lemire_bounded_counted(s, random_word, w)[0]


def lemire_bounded_counted(s: int, random_word: Callable[[], int], w: int = 64) -> Tuple[int, int, int]:
    """Return (value, words drawn, divisions done)."""
    if not 1 <= s <= 1 << w:
        raise ValueError("need 1 <= s <= 2^w")
    mask = (1 << w) - 1
    draws, divisions = 1, 0
    x = random_word() & mask  # @line L1
    m = x * s  # @line L2
    low = m & mask  # @line L3
    if low < s:  # @line L4
        t = ((1 << w) - s) % s  # @line L5
        divisions = 1
        while low < t:  # @line L6
            x = random_word() & mask  # @line L7
            draws += 1
            m = x * s
            low = m & mask
    return m >> w, draws, divisions  # @line L8


def accepted_outputs(s: int, w: int) -> Dict[int, int]:
    """For every w-bit word x, the output if x is accepted; counts per output value.

    Used to check exact uniformity by enumeration for small w.
    """
    mask = (1 << w) - 1
    t = (1 << w) % s
    counts: Dict[int, int] = {}
    for x in range(1 << w):
        m = x * s
        if (m & mask) >= t:
            counts[m >> w] = counts.get(m >> w, 0) + 1
    return counts


def rejected_words(s: int, w: int) -> List[int]:
    """The words x that the method rejects: those with (x s mod 2^w) < 2^w mod s."""
    mask = (1 << w) - 1
    t = (1 << w) % s
    return [x for x in range(1 << w) if (x * s) & mask < t]


def division_rejection(s: int, random_word: Callable[[], int], w: int = 64) -> Tuple[int, int, int]:
    """The classic method of OpenBSD's arc4random_uniform: always one division, then x mod s.

    Returns (value, words drawn, divisions or remainders computed).
    """
    if not 1 <= s <= 1 << w:
        raise ValueError("need 1 <= s <= 2^w")
    mask = (1 << w) - 1
    threshold = ((1 << w) - s) % s
    draws, divisions = 0, 1
    while True:
        x = random_word() & mask
        draws += 1
        if x >= threshold:
            divisions += 1
            return x % s, draws, divisions


def word_stream(words: List[int]) -> Callable[[], int]:
    it: Iterator[int] = iter(words)
    return lambda: next(it)


def splitmix64(seed: int) -> Callable[[], int]:
    """A SplitMix64 word source, for tests."""
    state = [seed & 0xFFFFFFFFFFFFFFFF]

    def nxt() -> int:
        state[0] = (state[0] + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
        z = state[0]
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
        return z ^ (z >> 31)

    return nxt
