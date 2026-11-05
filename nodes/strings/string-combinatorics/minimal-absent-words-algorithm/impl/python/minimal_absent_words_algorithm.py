# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimal-absent-words-algorithm/. The authors are listed in prov/DEK3N2.jsonl.

from collections.abc import Hashable, Iterable, Sequence
from typing import TypeVar

T = TypeVar("T", bound=Hashable)


def suffix_automaton(
    y: Sequence[T],
) -> tuple[list[dict[T, int]], list[int], list[int], list[int]]:
    """Build the suffix automaton of y online.

    Returns (nxt, link, length, end): the transition maps, the suffix links
    (link[0] = -1 for the initial state 0), the length of the longest word of
    each state, and one end position of the words of each state (-1 for 0).
    Cost: O(len(y)) expected time with hash maps, at most 2 len(y) states.
    """
    nxt: list[dict[T, int]] = [{}]
    link = [-1]
    length = [0]
    end = [-1]
    last = 0
    for i, c in enumerate(y):
        cur = len(length)
        nxt.append({})
        link.append(0)
        length.append(length[last] + 1)
        end.append(i)
        p = last
        while p != -1 and c not in nxt[p]:
            nxt[p][c] = cur
            p = link[p]
        if p != -1:
            q = nxt[p][c]
            if length[p] + 1 == length[q]:
                link[cur] = q
            else:
                clone = len(length)
                nxt.append(dict(nxt[q]))
                link.append(link[q])
                length.append(length[p] + 1)
                end.append(end[q])
                while p != -1 and nxt[p].get(c) == q:
                    nxt[p][c] = clone
                    p = link[p]
                link[q] = clone
                link[cur] = clone
        last = cur
    return nxt, link, length, end


def minimal_absent_words(y: Sequence[T], alphabet: Iterable[T]) -> list[tuple[int, int, T]]:
    """Return the minimal absent words of y over the alphabet as triples (i, l, b).

    The triple stands for the word y[i:i + l] followed by the letter b; a
    missing letter b is reported as (0, 0, b). Precondition: every letter of y
    is in the alphabet. Cost: O(len(y) + |alphabet| + z) expected time, where
    z is the number of words reported, and O(len(y)) extra space.
    """
    nxt, link, length, end = suffix_automaton(y)  # @line L1
    result: list[tuple[int, int, T]] = []  # @line L2
    for b in alphabet:  # @line L3
        if b not in nxt[0]:  # @line L4
            result.append((0, 0, b))
    for p in range(1, len(length)):  # @line L5
        l = length[link[p]] + 1  # @line L6
        for b in nxt[link[p]]:  # @line L7
            if b not in nxt[p]:  # @line L8
                result.append((end[p] - l + 1, l, b))  # @line L9
    return result  # @line L10


def minimal_absent_strings(y: str, alphabet: Iterable[str]) -> list[str]:
    """Return the minimal absent words of the string y as sorted strings."""
    return sorted(y[i : i + l] + b for i, l, b in minimal_absent_words(y, alphabet))
