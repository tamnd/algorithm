# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-distance/. The authors are listed in prov/PFEGKF.jsonl.
"""The minimum distance of a block code, and the decoders whose power it fixes.

A code is a list of distinct codewords, each a tuple of symbols of the same
length n. A received word is a tuple of the same length in which an erased
position holds None. The functions work for any code, linear or not.
"""

from itertools import combinations
from typing import Hashable, List, Optional, Sequence, Tuple

Word = Tuple[Hashable, ...]


def distance(x: Sequence[Hashable], y: Sequence[Hashable]) -> int:
    """The Hamming distance of two words of the same length."""
    return sum(1 for a, b in zip(x, y) if a != b)


def minimum_distance(code: Sequence[Word]) -> int:
    """d(C): the least distance between two different codewords.

    Precondition: at least two distinct codewords of the same length.
    Cost: M(M - 1)/2 distance computations of n symbols each, for M codewords.
    """
    if len(code) < 2:
        raise ValueError("the minimum distance needs at least two codewords")
    return min(distance(x, y) for x, y in combinations(code, 2))


def detect(code: Sequence[Word], received: Word) -> bool:
    """Error detection: True when the received word is not a codeword (an error is seen)."""
    return tuple(received) not in set(map(tuple, code))


def decode(code: Sequence[Word], received: Sequence[Optional[Hashable]], d: int) -> Optional[Word]:
    """Bounded distance decoding of errors and erasures (None marks an erasure).

    With e erasures, the decoder returns the codeword that agrees with the received word
    on all but at most t = floor((d - 1 - e) / 2) of the n - e positions that are not erased.
    It returns None (decoding failure) when e >= d or when no codeword is so close.
    If the channel made t errors and e erasures with 2t + e < d, the output is the sent codeword.
    Cost: M distance computations of n symbols each.
    """
    e = sum(1 for v in received if v is None)
    if e >= d:
        return None
    radius = (d - 1 - e) // 2
    best: Optional[Word] = None
    for c in code:
        mismatches = sum(1 for a, b in zip(c, received) if b is not None and a != b)
        if mismatches <= radius:
            if best is not None:  # cannot happen when the radius is right; kept as a guard
                return None
            best = tuple(c)
    return best


def detection_guarantee(d: int) -> int:
    """Every error pattern of weight 1 to d - 1 is detected."""
    return d - 1


def correction_radius(d: int) -> int:
    """Every error pattern of weight at most floor((d - 1) / 2) is corrected."""
    return (d - 1) // 2


def linear_code(rows: Sequence[Sequence[int]], q: int) -> List[Word]:
    """All q^k codewords m G of the linear code over Z_q (q prime) with the given generator rows."""
    k, n = len(rows), len(rows[0])
    words = []
    for idx in range(q ** k):
        m, v = [], idx
        for _ in range(k):
            m.append(v % q)
            v //= q
        words.append(tuple(sum(m[i] * rows[i][j] for i in range(k)) % q for j in range(n)))
    return words
