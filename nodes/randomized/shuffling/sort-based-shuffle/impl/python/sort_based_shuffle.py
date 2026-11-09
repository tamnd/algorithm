# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sort-based-shuffle/. The authors are listed in prov/JTAPRN.jsonl.
#
# The first two functions are the WRONG idiom "sort with a random comparator".
# They are here to show and test the bias. The last one is the right way to
# shuffle with a sort: random keys, drawn again on a tie.

import random
from typing import TypeVar

T = TypeVar("T")


def random_comparator_insertion_sort(a: list[T], rng: random.Random) -> list[T]:
    """Insertion sort whose test 'x < A[j]' is a fair coin. BIASED; returns a.

    Item i moves k places to the left with probability 2^-(k+1) for k < i,
    and i places with probability 2^-i, so the identity has probability
    2^-(n-1), not 1/n!.
    """
    for i in range(1, len(a)):  # @line L1
        x, j = a[i], i - 1  # @line L2
        while j >= 0 and rng.randrange(2) == 0:  # @line L3
            a[j + 1] = a[j]  # @line L4
            j -= 1
        a[j + 1] = x  # @line L5
    return a


def random_comparator_merge_sort(a: list[T], rng: random.Random) -> list[T]:
    """Top-down merge sort whose comparison is a fair coin. BIASED.

    The left half has floor(n/2) items. In a merge, a coin 0 takes the head
    of the right run, a coin 1 takes the head of the left run.
    """
    if len(a) <= 1:
        return list(a)
    m = len(a) // 2
    left = random_comparator_merge_sort(a[:m], rng)
    right = random_comparator_merge_sort(a[m:], rng)
    out: list[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if rng.randrange(2) == 0:
            out.append(right[j])
            j += 1
        else:
            out.append(left[i])
            i += 1
    return out + left[i:] + right[j:]


def random_key_shuffle(a: list[T], rng: random.Random) -> list[T]:
    """The correct sort-based shuffle: sort by distinct random 64-bit keys.

    Keys are drawn again if two are equal, which has probability at most
    n(n - 1)/2^65. See permute-by-sorting for the proof.
    """
    n = len(a)
    while True:
        keys = [rng.getrandbits(64) for _ in range(n)]
        if len(set(keys)) == n:
            break
    order = sorted(range(n), key=keys.__getitem__)
    return [a[i] for i in order]
