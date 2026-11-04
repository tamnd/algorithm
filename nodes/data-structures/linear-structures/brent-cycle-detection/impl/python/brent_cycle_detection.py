# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brent-cycle-detection/. The authors are listed in prov/AW3RN4.jsonl.

from typing import Callable, TypeVar

T = TypeVar("T")


def brent(f: Callable[[T], T], x0: T) -> tuple[int, int]:
    """Return (lam, mu): the cycle length and the tail length of x0, f(x0), ...

    Precondition: the sequence is eventually periodic (always true when f
    maps a finite set into itself). Uses O(1) memory and fewer than
    2 * max(mu + 1, lam) + 2 * lam + 2 * mu evaluations of f.
    """
    power = lam = 1  # @line L1
    tortoise, hare = x0, f(x0)  # @line L2
    while tortoise != hare:  # @line L3
        if power == lam:  # @line L4
            tortoise = hare  # @line L5
            power *= 2
            lam = 0
        hare = f(hare)  # @line L6
        lam += 1
    tortoise = hare = x0  # @line L7
    for _ in range(lam):  # @line L8
        hare = f(hare)
    mu = 0  # @line L9
    while tortoise != hare:  # @line L10
        tortoise, hare = f(tortoise), f(hare)
        mu += 1
    return lam, mu  # @line L11


def count_evaluations(f: Callable[[T], T], x0: T) -> tuple[int, int, int]:
    """Run brent and also return the number of calls of f."""
    calls = 0

    def g(x: T) -> T:
        nonlocal calls
        calls += 1
        return f(x)

    lam, mu = brent(g, x0)
    return lam, mu, calls
