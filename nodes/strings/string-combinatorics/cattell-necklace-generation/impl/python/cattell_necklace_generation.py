# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cattell-necklace-generation/. The authors are listed in prov/QYDXYF.jsonl.

"""Recursive CAT generation of prenecklaces, necklaces and Lyndon words.

The recursion GEN(t, p) of Cattell, Ruskey, Sawada, Serra and Miers is run
with an explicit stack, so the depth n does not hit the Python call limit.
"""

from typing import Iterator, List, Tuple


def prenecklaces(k: int, n: int) -> Iterator[Tuple[Tuple[int, ...], int]]:
    """Yield (a, p) for every prenecklace a of length n over {0, ..., k-1}.

    Precondition: k >= 1 and n >= 1. The words come in increasing
    lexicographic order, and p is the length of the longest Lyndon prefix
    of a. Cost: O(1) amortized per necklace for k >= 2, plus O(n) per word
    for the tuple that is yielded.
    """
    if k < 1 or n < 1:
        raise ValueError("need k >= 1 and n >= 1")
    a = [0] * n
    # A frame [t, p, c] stands for the call GEN(t, p) on the prefix a[0 .. t-1];
    # c is the next letter to try at index t. The frame with t = 0 is line L1.
    stack: List[List[int]] = [[0, 1, 0]]
    while stack:
        frame = stack[-1]
        t, p, c = frame
        # @line L2
        if t == n:
            # @line L3
            yield tuple(a), p
            stack.pop()
            continue
        if t == 0:
            # @line L1
            lo = 0
        else:
            # @line L4
            lo = a[t - p]
        if c < lo:
            c = lo
        # @line L6
        if c > k - 1:
            stack.pop()
            continue
        a[t] = c
        frame[2] = c + 1
        if t > 0 and c == a[t - p]:
            # @line L5
            stack.append([t + 1, p, 0])
        else:
            # @line L7
            stack.append([t + 1, t + 1, 0])


def necklaces(k: int, n: int) -> List[Tuple[int, ...]]:
    """All necklaces of length n over {0, ..., k-1}, in increasing order."""
    return [a for a, p in prenecklaces(k, n) if n % p == 0]


def lyndon_words(k: int, n: int) -> List[Tuple[int, ...]]:
    """All Lyndon words of length n over {0, ..., k-1}, in increasing order."""
    return [a for a, p in prenecklaces(k, n) if p == n]


def count_calls(k: int, n: int) -> int:
    """The number of calls of GEN in one run, including the root (line L1)."""
    calls = 1
    for t in range(1, n + 1):
        # each call GEN(t, p) is one prenecklace of length t
        calls += sum(1 for _ in prenecklaces(k, t))
    return calls
