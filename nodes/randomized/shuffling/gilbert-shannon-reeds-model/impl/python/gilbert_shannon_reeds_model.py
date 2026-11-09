# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gilbert-shannon-reeds-model/. The authors are listed in prov/WYX8N8.jsonl.

"""The Gilbert-Shannon-Reeds riffle shuffle, its inverse, and exact distances.

A deck is a list, deck[0] is the top card. The cards are labelled 0..n-1 in
their first order, so a deck is also a permutation: deck[pos] = card.
"""

import itertools
import math
import random
from fractions import Fraction
from typing import TypeVar

T = TypeVar("T")


def gsr_shuffle(deck: list[T], rng: random.Random) -> list[T]:
    """One GSR riffle shuffle; returns a new list.

    Cut a Binomial(n, 1/2) number of cards off the top, then build the new
    deck from the top: take the next card from a packet with probability
    proportional to the number of cards left in it.
    """
    n = len(deck)
    k = sum(rng.randrange(2) for _ in range(n))  # @line L1
    left, right, out = deck[:k], deck[k:], []  # @line L2
    i = j = 0
    while i < len(left) and j < len(right):  # @line L3
        a, b = len(left) - i, len(right) - j
        if rng.randrange(a + b) < a:  # @line L4
            out.append(left[i])
            i += 1
        else:  # @line L5
            out.append(right[j])
            j += 1
    out.extend(left[i:])  # @line L6
    out.extend(right[j:])
    return out


def inverse_gsr_shuffle(deck: list[T], rng: random.Random) -> list[T]:
    """One inverse riffle: give each card a fair bit and move the 0 cards to the top, keeping order."""
    bits = [rng.randrange(2) for _ in deck]
    return [c for c, b in zip(deck, bits) if b == 0] + [c for c, b in zip(deck, bits) if b == 1]


def rising_sequences(deck: list[int] | tuple[int, ...]) -> int:
    """Number of maximal runs v, v+1, ..., w of card values that appear in increasing positions."""
    n = len(deck)
    if n == 0:
        return 0
    pos = [0] * n
    for p, c in enumerate(deck):
        pos[c] = p
    return 1 + sum(1 for v in range(n - 1) if pos[v + 1] < pos[v])


def eulerian(n: int) -> list[int]:
    """e[r] = number of permutations of n cards with r rising sequences, r = 0..n."""
    e = [0] * (n + 1)
    if n == 0:
        e[0] = 1
        return e
    row = [1]  # row[d] = permutations of m with d descents
    for m in range(2, n + 1):
        new = [0] * m
        for d, v in enumerate(row):
            new[d] += (d + 1) * v
            new[d + 1] += (m - d - 1) * v
        row = new
    for d, v in enumerate(row):
        e[d + 1] = v
    return e


def a_shuffle_probability(n: int, a: int, r: int) -> Fraction:
    """Bayer-Diaconis: an a-shuffle gives a fixed deck with r rising sequences with probability C(a + n - r, n) / a^n."""
    return Fraction(math.comb(a + n - r, n), a**n)


def total_variation(n: int, k: int) -> Fraction:
    """Exact distance to uniform after k GSR shuffles (one 2^k-shuffle)."""
    a = 2**k
    u = Fraction(1, math.factorial(n))
    e = eulerian(n)
    return sum(e[r] * abs(a_shuffle_probability(n, a, r) - u) for r in range(1, n + 1)) / 2


def separation(n: int, k: int) -> Fraction:
    """1 - n! min_deck P^k(deck); the minimum is at the reversed deck (r = n)."""
    return 1 - math.factorial(n) * a_shuffle_probability(n, 2**k, n)


def inverse_riffle_tail(n: int, k: int) -> Fraction:
    """Pr[T > k] for the strong uniform time 'all k-bit labels distinct'."""
    a = 2**k
    p = Fraction(1)
    for i in range(1, n):
        p *= Fraction(a - i, a) if a > i else 0
    return 1 - p


def one_shuffle_law(n: int) -> dict[tuple[int, ...], Fraction]:
    """Law of one GSR shuffle of 0..n-1, by brute force: each set S of positions has probability 2^-n.

    The top |S| cards go to the positions in S in order, and the rest fill the
    other positions in order.
    """
    law: dict[tuple[int, ...], Fraction] = {}
    w = Fraction(1, 2**n)
    for mask in range(2**n):
        s = [p for p in range(n) if mask >> p & 1]
        rest = [p for p in range(n) if not mask >> p & 1]
        out = [0] * n
        for c, p in enumerate(s + rest):
            out[p] = c
        key = tuple(out)
        law[key] = law.get(key, 0) + w
    return law


def brute_force_distribution(n: int, k: int) -> dict[tuple[int, ...], Fraction]:
    """Exact law of the deck after k GSR shuffles, by composing the one-shuffle law."""
    step = one_shuffle_law(n)
    d = {tuple(range(n)): Fraction(1)}
    for _ in range(k):
        nd: dict[tuple[int, ...], Fraction] = {}
        for deck, p in d.items():
            for perm, q in step.items():
                new = tuple(deck[perm[x]] for x in range(n))
                nd[new] = nd.get(new, 0) + p * q
        d = nd
    return d


def brute_force_total_variation(n: int, k: int) -> Fraction:
    d = brute_force_distribution(n, k)
    u = Fraction(1, math.factorial(n))
    return sum(abs(d.get(p, 0) - u) for p in itertools.permutations(range(n))) / 2
