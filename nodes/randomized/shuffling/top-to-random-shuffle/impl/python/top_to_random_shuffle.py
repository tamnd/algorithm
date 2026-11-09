# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/top-to-random-shuffle/. The authors are listed in prov/8HFMHV.jsonl.

import itertools
import math
import random
from fractions import Fraction
from typing import TypeVar

T = TypeVar("T")


def top_to_random_shuffle(deck: list[T], t: int, rng: random.Random) -> list[T]:
    """Do t top-to-random moves on deck (deck[0] is the top card); return it.

    Each move takes the top card and puts it back at one of the n places,
    uniformly: place 0 is the top, place n - 1 is the bottom. After about
    n ln n moves the deck is close to uniform. O(n) time per move here.
    """
    n = len(deck)
    if n <= 1:
        return deck
    for _ in range(t):  # @line L1
        x = deck.pop(0)  # @line L2
        p = rng.randrange(n)  # @line L3
        deck.insert(p, x)  # @line L4
    return deck


def top_to_random_until_uniform(deck: list[T], rng: random.Random) -> tuple[list[T], int]:
    """Run top-to-random moves until the strong uniform time T; return (deck, T).

    T is one move after the card that started at the bottom first reaches
    the top. The deck at time T is exactly uniform, and E[T] = n H_n.
    """
    n = len(deck)
    if n <= 1:
        return deck, 0
    bottom = deck[-1]
    t = 0
    while True:
        x = deck.pop(0)
        deck.insert(rng.randrange(n), x)
        t += 1
        if x == bottom:
            return deck, t


def exact_distribution(n: int, t: int) -> dict[tuple[int, ...], Fraction]:
    """The exact law of the deck after t moves, from the identity deck."""
    d = {tuple(range(n)): Fraction(1)}
    for _ in range(t):
        nd: dict[tuple[int, ...], Fraction] = {}
        for deck, p in d.items():
            for q in range(n):
                rest = list(deck[1:])
                rest.insert(q, deck[0])
                e = tuple(rest)
                nd[e] = nd.get(e, 0) + p / n
        d = nd
    return d


def total_variation_to_uniform(d: dict[tuple[int, ...], Fraction], n: int) -> Fraction:
    u = Fraction(1, math.factorial(n))
    return sum(abs(d.get(p, 0) - u) for p in itertools.permutations(range(n))) / 2


def tail_of_stopping_time(n: int, t: int) -> Fraction:
    """Pr[T > t], where T is a sum of independent Geometric(i/n), i = 1..n."""
    phase = {0: Fraction(1)}
    for _ in range(t):
        nph: dict[int, Fraction] = {}
        for k, p in phase.items():
            if k == n:
                nph[k] = nph.get(k, 0) + p
                continue
            q = Fraction(k + 1, n)
            nph[k + 1] = nph.get(k + 1, 0) + p * q
            nph[k] = nph.get(k, 0) + p * (1 - q)
        phase = nph
    return 1 - phase.get(n, 0)
