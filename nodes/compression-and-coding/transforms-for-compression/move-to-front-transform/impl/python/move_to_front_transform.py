# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/move-to-front-transform/. The authors are listed in prov/HBY4JR.jsonl.

"""The move-to-front transform and its inverse.

The encoder and the decoder keep the same list of the sigma symbols. For each
input symbol the encoder outputs its 0-based index in the list, then moves it
to the front. The decoder reads the symbol at the given index and moves it to
the front in the same way. Time O(n sigma) in the worst case with a plain
list, and O(sum of the output values + n), because finding and moving the
symbol at index r costs O(r + 1). Extra space O(sigma).
"""

from collections.abc import Hashable, Iterable, Sequence
from typing import TypeVar

S = TypeVar("S", bound=Hashable)


def mtf_encode(seq: Iterable[S], alphabet: Sequence[S]) -> list[int]:
    """Indices of the symbols of seq in the move-to-front list.

    Precondition: the symbols of alphabet are distinct, and each symbol of
    seq is in alphabet. alphabet is the initial order of the list.
    """
    table = list(alphabet)
    out: list[int] = []
    for x in seq:  # @line L1
        r = table.index(x)  # @line L2
        out.append(r)  # @line L3
        table.insert(0, table.pop(r))  # @line L4
    return out  # @line L5


def mtf_decode(ranks: Iterable[int], alphabet: Sequence[S]) -> list[S]:
    """Inverse of mtf_encode with the same initial list."""
    table = list(alphabet)
    out: list[S] = []
    for r in ranks:
        x = table[r]
        out.append(x)
        table.insert(0, table.pop(r))
    return out


def mtf_encode_bytes(data: bytes) -> bytes:
    """MTF over the byte alphabet 0, 1, ..., 255 in increasing order."""
    return bytes(mtf_encode(data, range(256)))


def mtf_decode_bytes(data: bytes) -> bytes:
    """Inverse of mtf_encode_bytes."""
    return bytes(mtf_decode(data, list(range(256))))


def elias_delta_length(k: int) -> int:
    """Length in bits of the Elias delta code of the integer k >= 1."""
    if k < 1:
        raise ValueError("k must be at least 1")
    big_n = k.bit_length() - 1
    return big_n + 2 * ((big_n + 1).bit_length() - 1) + 1
