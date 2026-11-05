# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fkm-algorithm/. The authors are listed in prov/YSK2J8.jsonl.

"""The FKM algorithm: prenecklaces, necklaces, Lyndon words and de Bruijn sequences."""

from typing import Iterator, List, Tuple


def prenecklaces(k: int, n: int) -> Iterator[Tuple[Tuple[int, ...], int]]:
    """Yield (a, p) for every prenecklace a of length n over {0, ..., k-1}.

    Precondition: k >= 1 and n >= 1. The words come in increasing
    lexicographic order and p is the length of the longest Lyndon prefix of a.
    Cost: O(1) amortized per necklace for k >= 2, plus O(n) per word for the
    tuple that is yielded.
    """
    if k < 1 or n < 1:
        raise ValueError("need k >= 1 and n >= 1")
    # @line L1
    a = [0] * n
    p = 1
    # @line L2
    while True:
        # @line L3
        yield tuple(a), p
        # @line L4
        j = n - 1
        # @line L5
        while j >= 0 and a[j] == k - 1:
            j -= 1
        # @line L6
        if j < 0:
            return
        # @line L7
        a[j] += 1
        p = j + 1
        # @line L8
        for i in range(p, n):
            a[i] = a[i - p]


def necklaces(k: int, n: int) -> List[Tuple[int, ...]]:
    """All necklaces of length n over {0, ..., k-1}, in increasing order."""
    return [a for a, p in prenecklaces(k, n) if n % p == 0]


def lyndon_words(k: int, n: int) -> List[Tuple[int, ...]]:
    """All Lyndon words of length n over {0, ..., k-1}, in increasing order."""
    return [a for a, p in prenecklaces(k, n) if p == n]


def de_bruijn(k: int, n: int) -> List[int]:
    """The lexicographically least de Bruijn sequence of order n, length k**n."""
    out: List[int] = []
    for a, p in prenecklaces(k, n):
        if n % p == 0:
            out.extend(a[:p])
    return out
