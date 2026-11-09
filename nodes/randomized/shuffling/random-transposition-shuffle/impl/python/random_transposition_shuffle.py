# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-transposition-shuffle/. The authors are listed in prov/56XJ14.jsonl.

import itertools
import math
import random
from fractions import Fraction
from typing import TypeVar

T = TypeVar("T")


def random_transposition_shuffle(deck: list[T], t: int, rng: random.Random) -> list[T]:
    """Do t random transpositions on deck in place and return it.

    Each move picks two positions L and R, independent and uniform on
    0..n-1, and swaps them; L = R (probability 1/n) leaves the deck as it is.
    About (1/2) n ln n moves bring the deck close to uniform.
    """
    n = len(deck)
    if n == 0:
        return deck
    for _ in range(t):  # @line L1
        i = rng.randrange(n)  # @line L2
        j = rng.randrange(n)  # @line L3
        deck[i], deck[j] = deck[j], deck[i]  # @line L4
    return deck


def broder_until_uniform(deck: list[T], rng: random.Random) -> tuple[list[T], int]:
    """Random transpositions until Broder's strong uniform time; return (deck, T).

    A card is marked at a move when it is the card at position R, it is not
    marked yet, and the card at position L is marked or L = R. T is the move
    at which the last card is marked; the deck is then exactly uniform.
    """
    n = len(deck)
    if n == 0:
        return deck, 0
    marked = [False] * n  # indexed by position; moves with the cards
    count = 0
    t = 0
    while count < n:
        i = rng.randrange(n)
        j = rng.randrange(n)
        if not marked[j] and (marked[i] or i == j):
            marked[j] = True
            count += 1
        deck[i], deck[j] = deck[j], deck[i]
        marked[i], marked[j] = marked[j], marked[i]
        t += 1
    return deck, t


def exact_distribution(n: int, t: int) -> dict[tuple[int, ...], Fraction]:
    """The exact law of the deck after t moves, from the identity, by brute force."""
    d = {tuple(range(n)): Fraction(1)}
    w = Fraction(1, n * n)
    for _ in range(t):
        nd: dict[tuple[int, ...], Fraction] = {}
        for deck, p in d.items():
            for i in range(n):
                for j in range(n):
                    e = list(deck)
                    e[i], e[j] = e[j], e[i]
                    k = tuple(e)
                    nd[k] = nd.get(k, 0) + p * w
        d = nd
    return d


def total_variation_to_uniform(d: dict[tuple[int, ...], Fraction], n: int) -> Fraction:
    u = Fraction(1, math.factorial(n))
    return sum(abs(d.get(p, 0) - u) for p in itertools.permutations(range(n))) / 2


def cycle_type_distribution(n: int, t: int, exact: bool = True) -> dict[tuple[int, ...], object]:
    """The law of the cycle type after t moves, as a Markov chain on partitions of n.

    The law of the deck is constant on cycle types (conjugacy classes), so this
    law gives the distance to uniform for large n. Weights per move: 1/n for
    L = R; a/n^2 to split a cycle of length a into s and a - s, for each s;
    2ab/n^2 to merge two cycles of lengths a and b.
    """
    one = Fraction(1) if exact else 1.0
    nn = n * n
    d = {tuple([1] * n): one}
    for _ in range(t):
        nd: dict[tuple[int, ...], object] = {}
        for lam, p in d.items():
            parts = list(lam)
            nd[lam] = nd.get(lam, 0) + p * one / n
            for x, a in enumerate(parts):
                rest = parts[:x] + parts[x + 1 :]
                for s in range(1, a):
                    key = tuple(sorted(rest + [s, a - s], reverse=True))
                    nd[key] = nd.get(key, 0) + p * one * a / nn
                for y in range(x + 1, len(parts)):
                    b = parts[y]
                    rest2 = [parts[z] for z in range(len(parts)) if z != x and z != y]
                    key = tuple(sorted(rest2 + [a + b], reverse=True))
                    nd[key] = nd.get(key, 0) + p * one * 2 * a * b / nn
        d = nd
    return d


def class_probability(lam: tuple[int, ...], exact: bool = True) -> object:
    """The probability that a uniform permutation has cycle type lam."""
    denom = 1
    for a in set(lam):
        m = lam.count(a)
        denom *= a**m * math.factorial(m)
    return Fraction(1, denom) if exact else 1.0 / denom


def total_variation_by_cycle_type(n: int, t: int, exact: bool = True) -> object:
    d = cycle_type_distribution(n, t, exact)
    total = 0
    seen = set()
    for lam, p in d.items():
        seen.add(lam)
        total += abs(p - class_probability(lam, exact))
    # cycle types not reached yet have probability 0 under the chain
    total += 1 - sum(class_probability(lam, exact) for lam in seen)
    return total / 2


def broder_tail(n: int, t: int) -> Fraction:
    """Pr[T > t] for Broder's time: with k cards marked, a mark comes with probability (n-k)(k+1)/n^2."""
    phase = {0: Fraction(1)}
    for _ in range(t):
        nph: dict[int, Fraction] = {}
        for k, p in phase.items():
            if k == n:
                nph[k] = nph.get(k, 0) + p
                continue
            q = Fraction((n - k) * (k + 1), n * n)
            nph[k + 1] = nph.get(k + 1, 0) + p * q
            nph[k] = nph.get(k, 0) + p * (1 - q)
        phase = nph
    return 1 - phase.get(n, 0)
